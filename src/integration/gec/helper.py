"""Helper utilities for GEC Behave steps."""

import json
import logging
import os
from copy import deepcopy
from urllib.parse import parse_qsl


LOGGER = logging.getLogger("gec.helper")


def _config_value(node, *keys):
    """Read a value from a mapping-like node with case-insensitive keys."""
    if node is None:
        return None
    if hasattr(node, "to_dict"):
        node = node.to_dict()
    for key in keys:
        if isinstance(node, dict):
            if key in node:
                return node[key]
            for configured_key, value in node.items():
                if str(configured_key).lower() == key.lower():
                    return value
        if hasattr(node, key):
            return getattr(node, key)
    return None


def _ensure_vars_container(context):
    """Ensure context vars containers exist."""
    if not hasattr(context, "vars"):
        context.vars = {}
    if not hasattr(context, "payloads"):
        context.payloads = {}


def _get_client(context, client_name: str = "v1"):
    """Return a configured REST client for the requested logical endpoint."""
    actor = getattr(context, "gec", None)
    if not actor or not getattr(actor, "rest", None):
        raise AssertionError("No GEC client container available in context")

    rest = actor.rest
    if client_name == "v1":
        client = getattr(rest, "client_v1", None) or getattr(rest, "client", None)
    elif client_name == "v2":
        client = getattr(rest, "client_v2", None)
    elif client_name == "marketplace":
        client = getattr(rest, "client_marketplace", None)
    else:
        raise AssertionError(f"Unsupported client selector: {client_name}")

    if client is None:
        raise AssertionError(f"No RestClient available for '{client_name}'")
    return client


def _load_payload(context):
    """Load payload templates from payload.yaml once."""
    if not hasattr(context, "config") or context.config is None:
        raise AssertionError("No configuration loaded in context")
    if hasattr(context, "payload_templates") and isinstance(context.payload_templates, dict):
        return context.payload_templates
    raise AssertionError("Payload templates not available in context")


def _get_request_payload(context, primary_name: str, fallback_name: str = None):
    """Return parsed payload JSON by name with optional fallback key."""
    payloads = _load_payload(context)
    if primary_name in payloads:
        payload_str = payloads[primary_name]
    elif fallback_name and fallback_name in payloads:
        payload_str = payloads[fallback_name]
    else:
        raise AssertionError(f"Payload '{primary_name}' not found in TEST_DATA")
    try:
        return json.loads(payload_str)
    except json.JSONDecodeError as error:
        raise AssertionError(f"Payload '{primary_name}' is not valid JSON: {error}") from error


def _substitute_placeholders(text: str, context) -> str:
    """Substitute $var$ tokens from context vars."""
    if not text:
        return text
    result = text
    for key, value in getattr(context, "vars", {}).items():
        result = result.replace(f"${key}$", str(value))
    return result


def _sort_bundles_v1_onUs_first(bundles: list) -> list:
    """Return bundles sorted with onUs=true first, preserving relative order."""
    true_first = []
    rest = []
    for bundle in bundles or []:
        value = bundle.get("onUs")
        if value is True or str(value).lower() == "true":
            true_first.append(bundle)
        else:
            rest.append(bundle)
    return true_first + rest


def _normalize_boolean_cell(value: str) -> str:
    """Normalize boolean text to lowercase true/false."""
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in ("true", "false"):
        return normalized
    return str(value).strip()


def _get_bundled_response(response_body: dict) -> list:
    """Extract bundle options from a response payload."""
    bundles = response_body.get("bundleOptions")
    if bundles is None:
        bundles = response_body.get("bundles")
    if bundles is None:
        bundles = response_body.get("options")
    if bundles is None and isinstance(response_body, list):
        bundles = response_body
    return bundles if isinstance(bundles, list) else []


def _load_config_file(context, config_name: str, file_type: str = "json"):
    """Load and parse a config file from the suite config directory."""
    suite_path = context.config.get("suite_path") if hasattr(context, "config") else "."
    config_dir = os.path.join(suite_path, "config")
    config_path = os.path.join(config_dir, f"{config_name}.{file_type}")
    if not os.path.exists(config_path):
        raise AssertionError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8-sig") as file:
        if file_type == "json":
            return json.load(file)
        if file_type == "yaml":
            import yaml

            return yaml.safe_load(file)
    raise AssertionError(f"Unsupported file type: {file_type}")


def _map_to_valid_bundles(config_data: dict) -> list:
    """Build AFM-compatible bundle payload with nested ciBundleList."""
    bundles = config_data.get("bundles", [])
    ci_bundles = config_data.get("ciBundles", [])
    valid_bundles = []
    for bundle in bundles:
        mapped_bundle = deepcopy(bundle)
        mapped_bundle["ciBundleList"] = [
            deepcopy(ci_bundle)
            for ci_bundle in ci_bundles
            if ci_bundle.get("idBundle") == bundle.get("id")
        ]
        valid_bundles.append(mapped_bundle)
    return valid_bundles


def _track_uploaded_bundles(context, bundles: list):
    """Track full bundle payloads for AFM-compatible teardown."""
    if not hasattr(context.gec, "uploaded_bundles") or context.gec.uploaded_bundles is None:
        context.gec.uploaded_bundles = []
    context.gec.uploaded_bundles.extend(deepcopy(bundles))


def _upload_test_data_configuration(context, config_data: dict):
    """Upload data.json sections following AFM sequence and endpoints."""
    client = _get_client(context, "v1")
    valid_bundles = _map_to_valid_bundles(config_data)
    bundle_response = client.post("/configuration/bundles/add", json_body=valid_bundles)
    if bundle_response.status_code != 201:
        raise AssertionError(
            f"Bundles upload failed: expected 201, got {bundle_response.status_code}: {bundle_response.text}"
        )
    _track_uploaded_bundles(context, valid_bundles)

    for section, endpoint in (
        ("touchpoints", "/configuration/touchpoint/add"),
        ("paymenttypes", "/configuration/paymenttypes/add"),
    ):
        response = client.post(endpoint, json_body=config_data.get(section, []))
        if response.status_code != 201:
            raise AssertionError(
                f"{section} upload failed: expected 201, got {response.status_code}: {response.text}"
            )


def _ensure_scenario_data_loaded(context):
    """Upload test data configuration at most once per scenario."""
    _ensure_vars_container(context)
    if context.vars.get("scenario_data_loaded"):
        return
    config_data = _load_config_file(context, "data", "json")
    _upload_test_data_configuration(context, config_data)
    context.vars["scenario_data_loaded"] = True


def _setup_poste_bundles(context):
    """Upload Poste bundles according to ALL_CCP_NEW_FILTER_ENABLED policy."""
    _ensure_vars_container(context)
    try:
        config_data = _load_config_file(context, "bundle_poste", "json")
    except AssertionError:
        suite_path = context.config.get("suite_path") if hasattr(context, "config") else "."
        bundle_path = os.path.join(suite_path, "bundle_poste.json")
        if not os.path.exists(bundle_path):
            raise
        with open(bundle_path, "r", encoding="utf-8-sig") as file:
            config_data = json.load(file)
    poste_bundles = deepcopy(config_data.get("bundles", []))
    global_conf = getattr(context.config, "global_configuration", {})
    is_all_ccp_new_filter_enabled = bool(
        _config_value(global_conf, "all_ccp_new_filter_enabled") is True
        or str(_config_value(global_conf, "all_ccp_new_filter_enabled")).lower() == "true"
    )
    id_psp_poste = str(_config_value(global_conf, "id_psp_poste") or "BPPIITRRZZZ")
    poste_channel_ids = _config_value(global_conf, "poste_channel_ids") or []
    if isinstance(poste_channel_ids, str):
        poste_channel_ids = [item.strip() for item in poste_channel_ids.split(",") if item.strip()]
    if not poste_channel_ids:
        poste_channel_ids = ["65434098438_01"]

    for index, bundle in enumerate(poste_bundles):
        if is_all_ccp_new_filter_enabled:
            bundle["idPsp"] = "ABI50004"
            bundle["idChannel"] = poste_channel_ids[index] if index < len(poste_channel_ids) else poste_channel_ids[0]
        else:
            bundle["idPsp"] = id_psp_poste
            bundle["idChannel"] = "65434098438_01"

    response = _get_client(context, "v1").post("/configuration/bundles/add", json_body=poste_bundles)
    if response.status_code != 201:
        raise AssertionError(
            f"Poste bundles upload failed: expected 201, got {response.status_code}: {response.text}"
        )
    _track_uploaded_bundles(context, poste_bundles)


def _upload_payment_methods(context, config_data: dict):
    """Upload test payment methods to marketplace endpoint."""
    payment_methods = config_data.get("paymentmethods", [])
    if len(payment_methods) < 2:
        raise AssertionError("Expected at least two payment methods in configuration")
    marketplace_client = _get_client(context, "marketplace")
    for payment_method in payment_methods[:2]:
        response = marketplace_client.post("/payment-methods", json_body=payment_method)
        if response.status_code != 201:
            raise AssertionError(
                f"Payment method upload failed: expected 201, got {response.status_code}: {response.text}"
            )


def _extract_extension_params(extension: str) -> dict:
    """Parse static query string extension into params dictionary."""
    if not extension:
        return {}
    query = extension[1:] if extension.startswith("?") else extension
    return {key: value for key, value in parse_qsl(query, keep_blank_values=True)}


def _send_request(context, operation: str, payload_name: str):
    """Send request to the correct AFM-aligned endpoint and host."""
    _ensure_vars_container(context)
    operation_lower = operation.lower()
    if "recupero commissioni v2" in operation_lower:
        endpoint = "/fees/multi"
        client = _get_client(context, "v2")
        api_version = "v2"
    elif "recupero commissioni" in operation_lower:
        endpoint = "/fees"
        client = _get_client(context, "v1")
        api_version = "v1"
    elif "ricerca metodi di pagamento" in operation_lower:
        endpoint = "/payment-methods/search"
        client = _get_client(context, "v1")
        api_version = "v1"
    else:
        raise AssertionError(f"Unknown operation: {operation}")

    payload_data = _get_request_payload(context, payload_name)
    payload_json = _substitute_placeholders(json.dumps(payload_data), context)
    payload_data = json.loads(payload_json)

    params = dict(context.vars.get("request_params", {}))
    if api_version == "v2":
        gec_conf = getattr(context.config, "gec", {})
        default_extension = str(_config_value(gec_conf, "extension") or "")
        for key, value in _extract_extension_params(default_extension).items():
            params.setdefault(key, value)
    if "allCcp" in context.vars:
        params["allCcp"] = "true" if bool(context.vars["allCcp"]) else "false"

    psp_id = context.vars.get("psp_id")
    if api_version == "v1" and endpoint == "/fees" and psp_id:
        endpoint = f"/psps/{psp_id}/fees"

    context.response = client.post(endpoint, json_body=payload_data, params=params)
    LOGGER.info(
        "Request sent: POST %s status=%s params=%s",
        endpoint,
        getattr(context.response, "status_code", "n/a"),
        params,
    )
