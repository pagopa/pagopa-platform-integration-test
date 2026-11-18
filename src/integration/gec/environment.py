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
    """Expose configured global and FdR values to the placeholder resolver."""
    if not hasattr(context, "vars"):
        context.vars = {}

    global_conf = _config_value(context.config, "global_configuration")
    
    configured = {
            "xxx": _config_value(global_conf, "xxx"),#TODO actual configuration
    }

    for key, value in configured.items():
        if value is not None:
            context.vars[key] = str(value)
    LOGGER.info

def before_all(context):
    """Hook to run before all tests."""
    LOGGER.info("Running before_all hook for GEC integration tests.")
    # Load configurations and common data
    context.config = load_configurations(os.path.dirname(os.path.abspath(__file__)))
    context.payload_templates = load_commondata("payload.yaml", os.path.dirname(os.path.abspath(__file__)))
    # Populate placeholder variables
    _populate_placeholder_vars(context)