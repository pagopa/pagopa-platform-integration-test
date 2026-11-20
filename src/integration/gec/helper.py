"""Helper utilities for GEC behave steps.

This module centralizes helper functions used by step definition
modules under src.integration.gec.steps. Functions are internal helpers
(leading underscore) and intended to be imported from step modules.
"""

import json
import logging
from src.utility.rest import build_rest_client
from src.conf.configuration import load_commondata

LOGGER = logging.getLogger("gec.helper")


def _ensure_vars_container(context):
    """Ensure context.vars and context.payloads exist."""
    if not hasattr(context, "vars"):
        context.vars = {}
    if not hasattr(context, "payloads"):
        context.payloads = {}


def _get_client(context):
    """Get REST client from context."""
    client = getattr(context, "gec", None)
    if client and getattr(client, "rest", None) and getattr(client.rest, "client", None):
        return context.gec.rest.client
    raise AssertionError("No RestClient available in context.gec.rest.client")


def _load_payload(context):
    """Load payloads from configuration."""
    if not hasattr(context, "config") or context.config is None:
        raise AssertionError("No configuration loaded in context")
    
    if not hasattr(context, "payload_templates") or context.payload_templates is None:
        payload_file = getattr(context.config, "payload_file", "payload.yaml")
        payload_data = load_commondata(payload_file, 
                                      context.config.get("suite_path"))
        # load_commondata returns the full dict; extract TEST_DATA if present
        if isinstance(payload_data, dict) and "TEST_DATA" in payload_data:
            context.payload_templates = payload_data["TEST_DATA"]
        else:
            context.payload_templates = payload_data
    
    return context.payload_templates if isinstance(context.payload_templates, dict) else {}


def _get_request_payload(context, primary_name: str, fallback_name: str = None):
    """Get a payload by name, with fallback."""
    payloads = _load_payload(context)
    
    if primary_name in payloads:
        payload_str = payloads[primary_name]
    elif fallback_name and fallback_name in payloads:
        payload_str = payloads[fallback_name]
    else:
        raise AssertionError(f"Payload '{primary_name}' not found in TEST_DATA")
    
    # Parse JSON string from YAML
    try:
        return json.loads(payload_str)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Payload '{primary_name}' is not valid JSON: {e}")


def _substitute_placeholders(text: str, context) -> str:
    """Substitute $var$ tokens from context.vars."""
    if not text:
        return text
    
    result = text
    vars_dict = getattr(context, "vars", {})
    
    for key, value in vars_dict.items():
        placeholder = f"${key}$"
        result = result.replace(placeholder, str(value))
    
    return result


def _send_request(context, operation: str, payload_name: str):
    """Send a request to GEC API."""
    _ensure_vars_container(context)
    
    client = _get_client(context)
    
    # Map operation to HTTP method and endpoint
    operation_lower = operation.lower()
    
    # Determine method and endpoint based on operation
    if "recupero commissioni v2" in operation_lower:
        method = "post"
        endpoint = "/commissions/v2"
    elif "recupero commissioni" in operation_lower:
        method = "post"
        endpoint = "/commissions"
    elif "ricerca metodi di pagamento" in operation_lower:
        method = "post"
        endpoint = "/payment-methods"
    else:
        raise AssertionError(f"Unknown operation: {operation}")
    
    # Get payload
    payload_data = _get_request_payload(context, payload_name)
    
    # Apply substitutions
    payload_json = json.dumps(payload_data)
    payload_json = _substitute_placeholders(payload_json, context)
    payload_data = json.loads(payload_json)
    
    # Add query parameters if set
    params = context.vars.get("request_params", {})
    psp_id = context.vars.get("psp_id")
    
    if psp_id:
        # Append PSP to endpoint
        endpoint = f"{endpoint}/{psp_id}"
    
    # Send request using RestClient API (json_body parameter, not json)
    try:
        if method == "post":
            context.response = client.post(endpoint, json_body=payload_data, params=params)
        elif method == "get":
            context.response = client.get(endpoint, params=params)
        else:
            raise AssertionError(f"Unsupported HTTP method: {method}")
        
        LOGGER.info(
            "Request sent: %s %s, status=%d",
            method.upper(),
            endpoint,
            context.response.status_code
        )
    except Exception as e:
        raise AssertionError(f"Request failed: {e}")


def _get_bundled_response(response_body: dict) -> list:
    """Extract bundle options from response body."""
    # Try common field names for bundle options
    bundles = response_body.get("bundleOptions")
    if bundles is None:
        bundles = response_body.get("bundles")
    if bundles is None:
        bundles = response_body.get("options")
    if bundles is None:
        # If response is an array, treat it as bundles
        if isinstance(response_body, list):
            bundles = response_body
    
    if not isinstance(bundles, list):
        bundles = []
    
    return bundles

