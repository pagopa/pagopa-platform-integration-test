import re
from datetime import datetime
from typing import Any, Dict, Optional

from requests import Response

from src.utility.rest.rest_client import RestClient


DEFAULT_ENDPOINTS = {
    "create": ("POST", "/psps/#psp#/fdrs/$flow_name$"),
    "add_payments": ("PUT", "/psps/#psp#/fdrs/$flow_name$/payments/add"),
    "publish": ("POST", "/psps/#psp#/fdrs/$flow_name$/publish"),
    "delete_flow": ("DELETE", "/psps/#psp#/fdrs/$flow_name$"),
    "get_published": ("GET", "/psps/#psp#/published/fdrs/$flow_name$/revisions/$revision$/organizations/#organization#"),
    "get_created_payments": ("GET", "/psps/#psp#/created/fdrs/$flow_name$/organizations/#organization#/payments"),
    "get_created_fdr": ("GET", "/psps/#psp#/created/fdrs/$flow_name$/organizations/#organization#"),
    "get_all_created": ("GET", "/psps/#psp#/created"),
    "delete_payments": ("PUT", "/psps/#psp#/fdrs/$flow_name$/payments/del"),
    "org_get_all_published_fdr": ("GET", "/organizations/#organization#/fdrs"),
    "org_get_published_fdr": ("GET", "/organizations/#organization#/fdrs/$flow_name$/revisions/$revision$/psps/#psp#"),
    "org_get_payments": ("GET", "/organizations/#organization#/fdrs/$flow_name$/revisions/$revision$/psps/#psp#/payments"),
    "org_get_all_published_fdr_by_psp": ("GET", "/organizations/#organization#/fdrs?pspId=#psp#&page=1&size=1000&publishedGt=$today_date$"),
    "psp_get_published_payments": ("GET", "/psps/#psp#/published/fdrs/$flow_name$/revisions/$revision$/organizations/#organization#/payments"),
    "psp_get_published_fdr": ("GET", "/psps/#psp#/published/fdrs/$flow_name$/revisions/$revision$/organizations/#organization#"),
    "psp_get_all_published_fdr": ("GET", "/psps/#psp#/published")

}

REQUEST_ACTIONS = {
    "create a new flow structure": "create",
    "add payments": "add_payments",
    "publish": "publish",
    "get published fdr": "get_published",
    "delete flow": "delete_flow",
    "delete payments": "delete_payments",
    "get created fdr": "get_created_fdr",
    "get created payments": "get_created_payments",
    "get all created": "get_all_created",
    "get all created fdr": "get_all_created",
    "get all published fdr by psp": "org_get_all_published_fdr_by_psp",
    "get published payments": "psp_get_published_payments",
    "psp get published fdr": "psp_get_published_fdr",
    "psp get all published fdr": "psp_get_all_published_fdr",
    "org get all published fdr": "org_get_all_published_fdr",
}


def resolve_fdr_action(request: str) -> str:
    """Convert the API request label used in a feature into an endpoint action."""
    key = " ".join(request.strip().lower().split())
    action = REQUEST_ACTIONS.get(key)
    if action is None:
        normalized = re.sub(r"[^a-z0-9]+", "_", key).strip("_")
        if normalized in DEFAULT_ENDPOINTS:
            action = normalized
    if action is None:
        raise ValueError(
            f"Unknown FdR request '{request}'. "
            f"Available: {sorted(REQUEST_ACTIONS)}"
        )
    return action


def perform_fdr_action(
    client: RestClient,
    action: str,
    *,
    flow_name: Optional[str] = None,
    flow_date: Optional[str] = None,
    payload_override: Optional[Dict[str, Any]] = None,
    n_payments: Optional[int] = None,
    expected_status: Optional[int] = None,
    checks: Optional[Dict[str, Any]] = None,
    endpoints: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
    context: Optional[Any] = None,
    omit_payload: bool = False,
    headers: Optional[Dict[str, str]] = None,
) -> Response:
    """Esegue un'azione FdR parametrica utilizzando RestClient.

    Args:
        client: istanza di RestClient (vedi src.utility.rest)
        action: nome dell'azione (es. "create", "add_payments", "publish", ...)
        flow_name / flow_date: usati per costruire path o payload quando necessari
        payload_override: body JSON completo (se presente viene usato al posto del payload factory)
        n_payments: usato per il payload di cancellazione pagamenti
        expected_status: se fornito, viene assertato che response.status_code == expected_status
        checks: mappa chiave->valore da verificare nella response.json()
        endpoints: mappatura custom per sovrascrivere DEFAULT_ENDPOINTS
        query_params: query string da passare alla chiamata
        context: behave context per sostituire placeholder #psp#, $flow_name$, ecc.

    Ritorna:
        requests.Response

    Nota: le path di DEFAULT_ENDPOINTS sono indicative e devono essere adattate se
    l'API reale usa nomi differenti.
    """
    endpoints = {**DEFAULT_ENDPOINTS, **(endpoints or {})}

    if action not in endpoints:
        raise ValueError(f"Unknown action '{action}'. Available: {list(endpoints.keys())}")

    method, path_template = endpoints[action]
    # first allow {flow_name} style formatting
    path = path_template.format(flow_name=flow_name or "", flow_date=flow_date or "")

    # helper to resolve placeholder keys from multiple sources
    def _resolve_key(key: str):
        # prefer explicit args
        if key in ("flow_name", "flowName", "fdr") and flow_name:
            return flow_name
        if key in ("flow_date", "flowDate") and flow_date:
            return flow_date
        # today date helper
        if key == "today_date":
            return datetime.utcnow().strftime("%Y-%m-%d")
        # lookup in context.vars if available
        if context is not None and hasattr(context, "vars"):
            v = context.vars.get(key)
            if v is not None:
                return str(v)
        if key == "revision":
            return "1"
        # fallback to empty string
        return ""

    # replace $var$ placeholders
    def _replace_dollar(match):
        k = match.group(1)
        return _resolve_key(k)

    path = re.sub(r"\$(.+?)\$", _replace_dollar, path)
    # replace #var# placeholders
    def _replace_hash(match):
        k = match.group(1)
        return _resolve_key(k)

    path = re.sub(r"#(.+?)#", _replace_hash, path)

    # Build JSON body if needed
    json_body = None
    if action == "create" and not omit_payload:
        json_body = payload_override

    elif action == "add_payments" and not omit_payload:
        json_body = payload_override

    elif action == "delete_payments" and not omit_payload:
        json_body = payload_override or {"deleteCount": n_payments or 0}

    # Substitute placeholders inside json_body strings if any
    def _substitute_in_obj(obj):
        if isinstance(obj, str):
            s = obj
            s = re.sub(r"\$(.+?)\$", _replace_dollar, s)
            s = re.sub(r"#(.+?)#", _replace_hash, s)
            return s
        if isinstance(obj, dict):
            return {k: _substitute_in_obj(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_substitute_in_obj(v) for v in obj]
        return obj

    if json_body is not None:
        json_body = _substitute_in_obj(json_body)

    response = client.request(
        method,
        path,
        json_body=json_body,
        params=query_params,
        headers=headers,
    )

    if expected_status is not None:
        assert (
            response.status_code == expected_status
        ), f"Expected status {expected_status} for action {action}, got {response.status_code}: {response.text}"

    if checks:
        try:
            body = response.json()
        except ValueError:
            raise AssertionError("Response body is not JSON for checks")
        for key, expected in checks.items():
            # support nested keys with dot notation
            parts = key.split(".")
            val = body
            for p in parts:
                if isinstance(val, dict) and p in val:
                    val = val[p]
                else:
                    raise AssertionError(f"Missing key '{key}' in response body")
            assert val == expected, f"Check {key} expected {expected} got {val}"

    return response
