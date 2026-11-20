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
    gec_service_config = _config_value(context.config, "services", "gec")
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