"""Behave hooks for GEC integration suite."""

import logging
import os
from types import SimpleNamespace

from src.conf.configuration import load_commondata, load_configurations
from src.integration.gec.helper import _config_value
from src.utility.rest import build_api_key_auth_from_config, build_rest_client


LOGGER = logging.getLogger("gec")


def _ensure_actor(context, name: str):
    """Ensure context actor namespace exists."""
    if not hasattr(context, name) or getattr(context, name) is None:
        setattr(context, name, SimpleNamespace(rest=SimpleNamespace()))


def _populate_placeholder_vars(context):
    """Expose runtime placeholder variables to step payload substitution."""
    if not hasattr(context, "vars"):
        context.vars = {}
    context.vars["environment"] = os.environ.get("TARGET_ENV", "dev")


def _build_service_config(base_url: str, gec_config) -> dict:
    """Build rest_client_factory-compatible service config."""
    return {
        "url": base_url,
        "timeout": _config_value(gec_config, "timeout", "request_timeout") or 30,
        "verify_ssl": _config_value(gec_config, "verify_ssl", "ssl_verify")
        if _config_value(gec_config, "verify_ssl", "ssl_verify") is not None
        else True,
        "default_headers": _config_value(gec_config, "default_headers") or {},
    }


def _build_clients(context):
    """Create V1, V2 and marketplace clients from suite configuration."""
    gec_config = _config_value(context.config, "gec")
    if not gec_config:
        raise AssertionError("Missing 'gec' configuration section")

    auth_config = _config_value(gec_config, "auth")
    if not auth_config:
        raise AssertionError("Missing gec.auth configuration")
    if hasattr(auth_config, "to_dict"):
        auth_config = auth_config.to_dict()
    v1_auth = build_api_key_auth_from_config(auth_config)

    v1_url = _config_value(gec_config, "url")
    v2_url = _config_value(gec_config, "url_v2")
    marketplace_url = _config_value(gec_config, "marketplace_host")
    marketplace_key = _config_value(gec_config, "marketplace_key")

    if not v1_url or not v2_url or not marketplace_url:
        raise AssertionError("Missing one or more required hosts: gec.url, gec.url_v2, gec.marketplace_host")
    if not marketplace_key:
        raise AssertionError("Missing required marketplace key: gec.marketplace_key")

    v2_auth = build_api_key_auth_from_config(auth_config)
    marketplace_auth_cfg = dict(auth_config)
    marketplace_auth_cfg["key_value"] = marketplace_key
    marketplace_auth = build_api_key_auth_from_config(marketplace_auth_cfg)

    rest = context.gec.rest
    rest.client_v1 = build_rest_client(_build_service_config(v1_url, gec_config), v1_auth)
    rest.client_v2 = build_rest_client(_build_service_config(v2_url, gec_config), v2_auth)
    rest.client_marketplace = build_rest_client(
        _build_service_config(marketplace_url, gec_config), marketplace_auth
    )
    rest.client = rest.client_v1


def _setup_azure_storage(context):
    """Setup issuer table data when Azure connection string is configured."""
    gec_config = _config_value(context.config, "gec")
    global_conf = _config_value(context.config, "global_configuration")
    connection_string = _config_value(gec_config, "azure_connection_string")
    if not connection_string:
        LOGGER.info("Azure issuer setup skipped: no connection string configured")
        return

    try:
        from src.integration.gec.azure_table_client import ISSUER_ENTITIES
        from src.utility.blob import build_issuer_table_client

        table_name = _config_value(global_conf, "issuer_range_table") or "issuerrangetable"
        table_client = build_issuer_table_client(connection_string, table_name=table_name)
        if table_client:
            _delete_issuer_entities_by_partition(table_client, ISSUER_ENTITIES)
            table_client.setup_issuer_ranges(ISSUER_ENTITIES)
            context.gec.azure_table_client = table_client
            LOGGER.info("Azure issuer setup completed on table '%s'", table_name)
    except Exception as error:
        LOGGER.warning("Azure issuer setup failed (continuing): %s", error)


def _delete_issuer_entities_by_partition(table_client, issuer_entities):
    """Delete all entities by partition key before issuer setup."""
    partition_keys = {
        str(entity.get("partition_key")).strip()
        for entity in issuer_entities
        if entity.get("partition_key") is not None
    }
    if not partition_keys:
        return
    if not hasattr(table_client, "list_entities") or not hasattr(table_client, "delete_entity"):
        LOGGER.warning("Issuer table client does not expose list/delete APIs for delete-by-partition")
        return

    for partition_key in partition_keys:
        for entity in table_client.list_entities(partition_key=partition_key):
            entity_partition_key = entity.get("PartitionKey") or entity.get("partitionKey") or entity.get("partition_key")
            entity_row_key = entity.get("RowKey") or entity.get("rowKey") or entity.get("row_key")
            if entity_partition_key is None or entity_row_key is None:
                continue
            table_client.delete_entity(str(entity_partition_key), str(entity_row_key))


def before_all(context):
    """Load suite configuration and initialize all required clients."""
    suite_path = os.path.dirname(os.path.abspath(__file__))
    context.config = load_configurations(suite_path)
    context.config["suite_path"] = suite_path
    context.payload_templates = load_commondata("payload.yaml", suite_path)

    _ensure_actor(context, "gec")
    _build_clients(context)
    context.gec.uploaded_bundles = []
    _setup_azure_storage(context)
    _populate_placeholder_vars(context)


def before_scenario(context, scenario):
    """Reset scenario state."""
    LOGGER.info("Starting scenario: %s", scenario.name)
    environment_value = None
    if hasattr(context, "vars") and isinstance(context.vars, dict):
        environment_value = context.vars.get("environment")
    if environment_value is None:
        environment_value = os.environ.get("TARGET_ENV", "dev")
    context.vars = {
        "environment": environment_value,
        "request_params": {},
        "scenario_data_loaded": False,
    }
    context.response = None


def after_scenario(context, scenario):
    """Log scenario completion status."""
    LOGGER.info("Scenario %s finished with status: %s", scenario.name, getattr(scenario, "status", "unknown"))


def _delete_uploaded_bundles(context):
    """Delete tracked bundles from configuration service."""
    uploaded = getattr(context.gec, "uploaded_bundles", []) or []
    if not uploaded:
        return
    client = context.gec.rest.client_v1
    response = client.post("/configuration/bundles/delete", json_body=uploaded)
    if response.status_code != 200:
        LOGGER.warning(
            "Bundle teardown returned status %s (expected 200): %s",
            response.status_code,
            response.text,
        )


def _delete_payment_methods(context):
    """Delete marketplace payment methods created by tests."""
    global_conf = _config_value(context.config, "global_configuration")
    payment_methods = [
        _config_value(global_conf, "payment_method_cards") or "CARDS-test",
        _config_value(global_conf, "payment_method_paypal") or "PAYPAL-test",
    ]
    client = context.gec.rest.client_marketplace
    for payment_method in payment_methods:
        response = client.delete(f"/payment-methods/{payment_method}")
        if response.status_code != 200:
            LOGGER.warning(
                "Payment method teardown for '%s' returned status %s (expected 200): %s",
                payment_method,
                response.status_code,
                response.text,
            )


def after_all(context):
    """Cleanup configured bundles and payment methods without masking test outcomes."""
    if not hasattr(context, "gec") or not getattr(context.gec, "rest", None):
        LOGGER.warning("Skipping after_all teardown: no GEC client context")
        return
    try:
        _delete_uploaded_bundles(context)
    except Exception as error:
        LOGGER.warning("Bundle teardown failed: %s", error)
    try:
        _delete_payment_methods(context)
    except Exception as error:
        LOGGER.warning("Payment method teardown failed: %s", error)
