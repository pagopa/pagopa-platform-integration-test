import re
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from requests import Response

from src.utility.rest.rest_client import RestClient


LOGGER = logging.getLogger("fdr3")


DEFAULT_ENDPOINTS = {
    "creazione di una nuova struttura di flusso": ("POST", "/psps/#psp#/fdrs/$flow_name$"),
    "aggiunta pagamenti": ("PUT", "/psps/#psp#/fdrs/$flow_name$/payments/add"),
    "pubblicazione": ("POST", "/psps/#psp#/fdrs/$flow_name$/publish"),
    "cancellazione flusso": ("DELETE", "/psps/#psp#/fdrs/$flow_name$"),
    "recupero fdr pubblicato": ("GET", "/psps/#psp#/published/fdrs/$flow_name$/revisions/$revision$/organizations/#organization#"),
    "recupero pagamenti creati": ("GET", "/psps/#psp#/created/fdrs/$flow_name$/organizations/#organization#/payments"),
    "recupero fdr creato": ("GET", "/psps/#psp#/created/fdrs/$flow_name$/organizations/#organization#"),
    "cancellazione pagamenti": ("PUT", "/psps/#psp#/fdrs/$flow_name$/payments/del"),
    "recupero di tutti i fdr pubblicati dal psp": ("GET", "/psps/#psp#/published"),
}


def resolve_fdr_action(request: str) -> str:
    """Resolve the Italian request label directly to an endpoint key."""
    key = " ".join(request.strip().casefold().split())
    if key not in DEFAULT_ENDPOINTS:
        LOGGER.error("Unknown FdR request label: %s", request)
        raise ValueError(
            f"Unknown FdR request '{request}'. "
            f"Available: {sorted(DEFAULT_ENDPOINTS)}"
        )
    return key


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
        action: dicitura italiana dell'azione definita in DEFAULT_ENDPOINTS
        flow_name: nome del flusso usato per costruire il path o il payload
        flow_date: data del flusso usata per costruire il payload
        payload_override: body JSON completo (se presente viene usato al posto del payload factory)
        n_payments: usato per il payload di cancellazione pagamenti
        expected_status: se fornito, viene assertato che response.status_code == expected_status
        checks: mappa chiave->valore da verificare nella response.json()
        endpoints: mappatura custom per sovrascrivere DEFAULT_ENDPOINTS
        query_params: query string da passare alla chiamata
        context: behave context per sostituire placeholder #psp#, $flow_name$, ecc.
        omit_payload: evita l'invio del body JSON quando impostato a True
        headers: header aggiuntivi o sostitutivi per la singola richiesta

    Ritorna:
        requests.Response

    Nota: le path di DEFAULT_ENDPOINTS rappresentano gli endpoint API utilizzati
    dalla suite FdR3.
    """
    endpoints = {**DEFAULT_ENDPOINTS, **(endpoints or {})}

    if action not in endpoints:
        LOGGER.error("Unknown FdR action: %s", action)
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
    if action == "creazione di una nuova struttura di flusso" and not omit_payload:
        json_body = payload_override

    elif action == "aggiunta pagamenti" and not omit_payload:
        json_body = payload_override

    elif action == "cancellazione pagamenti" and not omit_payload:
        json_body = payload_override or {
            "indexList": list(range(1, (n_payments or 0) + 1))
        }

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

    LOGGER.info(
        "FdR request: action=%s method=%s path=%s body=%s query=%s headers_override=%s",
        action,
        method,
        path,
        json_body is not None,
        bool(query_params),
        bool(headers),
    )
    response = client.request(
        method,
        path,
        json_body=json_body,
        params=query_params,
        headers=headers,
    )
    LOGGER.info(
        "FdR response: action=%s status=%s",
        action,
        response.status_code,
    )

    if expected_status is not None:
        if response.status_code != expected_status:
            LOGGER.error(
                "Unexpected FdR status: action=%s expected=%s actual=%s",
                action,
                expected_status,
                response.status_code,
            )
            raise AssertionError(
                f"Expected status {expected_status} for action {action}, "
                f"got {response.status_code}: {response.text}"
            )

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
            if val != expected:
                LOGGER.error(
                    "FdR response check failed: action=%s key=%s expected=%s actual=%s",
                    action,
                    key,
                    expected,
                    val,
                )
                raise AssertionError(
                    f"Check {key} expected {expected} got {val}"
                )

    return response
