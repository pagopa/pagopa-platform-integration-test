import os
import logging
from types import SimpleNamespace

from src.utility.rest import build_rest_client, build_api_key_auth_from_config
from src.conf.configuration import load_commondata, load_configurations


LOGGER = logging.getLogger("gec")

def _config_value(node, *keys):
    """Read a value from a Dynaconf node or a regular mapping."""
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

def _ensure_actor(context, name: str):
    """Ensure context.<name> exists and has a .rest attribute with a client slot."""
    if not hasattr(context, name) or getattr(context, name) is None:
        setattr(context, name, SimpleNamespace(rest=SimpleNamespace(client=None)))

def _populate_placeholder_vars(context):
    """Expose configured global and GEC values to the placeholder resolver."""
    if not hasattr(context, "vars"):
        context.vars = {}

    global_conf = _config_value(context.config, "global_configuration")
    
    configured = {
        "environment": os.environ.get("TARGET_ENV", "dev"),
    }

    for key, value in configured.items():
        if value is not None:
            context.vars[key] = str(value)
    
    LOGGER.info("Placeholder variables populated: %s", list(configured.keys()))


def _setup_azure_storage(context):
    """Setup Azure Table Storage for issuer ranges (optional).
    
    If azure_connection_string is configured, initializes issuer entities.
    If not configured or fails, continues without it (some tests may fail).
    Uses the utility/blob/azure_table module for consistency.
    """
    gec_config = getattr(context.config, "gec", None)
    if not gec_config:
        return
    
    azure_conn_str = _config_value(gec_config, "azure_connection_string")
    if not azure_conn_str:
        LOGGER.info("No Azure Storage connection string configured - skipping issuer range setup")
        return
    
    try:
        from src.utility.blob import build_issuer_table_client
        from src.integration.gec.azure_table_client import ISSUER_ENTITIES
        
        table_client = build_issuer_table_client(azure_conn_str)
        if table_client:
            # Setup pre-defined issuer entities (idempotent)
            table_client.setup_issuer_ranges(ISSUER_ENTITIES)
            context.gec.azure_table_client = table_client
            LOGGER.info("Azure Table Storage issuer ranges setup completed")
    except ImportError as e:
        LOGGER.warning(f"Azure Tables not installed: {e}")
        LOGGER.info("Install with: pip install azure-data-tables")
    except Exception as e:
        LOGGER.warning(f"Azure Table Storage setup failed (tests may fail): {e}")


def before_all(context):
    """Hook to run before all tests."""
    LOGGER.info("Running before_all hook for GEC integration tests.")
    
    suite_path = os.path.dirname(os.path.abspath(__file__))
    
    # Load configurations and common data
    context.config = load_configurations(suite_path)
    context.config["suite_path"] = suite_path
    
    context.payload_templates = load_commondata("payload.yaml", suite_path)
    
    # Initialize GEC client
    _ensure_actor(context, "gec")
    gec_service_config = getattr(context.config, "gec", None)
    if gec_service_config:
        auth_config = _config_value(gec_service_config, "auth")
        if auth_config:
            auth = build_api_key_auth_from_config(auth_config)
        else:
            from src.utility.rest import NoAuthConfig
            auth = NoAuthConfig()
        context.gec.rest.client = build_rest_client(gec_service_config, auth)
        LOGGER.info("GEC REST client initialized")
    else:
        LOGGER.warning("GEC service configuration not found")
    
    # Setup Azure Storage (optional)
    _setup_azure_storage(context)
    
    # Populate placeholder variables
    _populate_placeholder_vars(context)
    
    LOGGER.info("before_all hook completed successfully")


def before_scenario(context, scenario):
    """Hook to run before each scenario."""
    LOGGER.info("Starting scenario: %s", scenario.name)
    # Initialize scenario-specific state
    if not hasattr(context, "vars"):
        context.vars = {}
    context.response = None
    # Reset request parameters for each scenario
    context.vars["request_params"] = {}


def after_scenario(context, scenario):
    """Hook to run after each scenario."""
    if hasattr(scenario, "status"):
        LOGGER.info("Scenario %s finished with status: %s", scenario.name, scenario.status)