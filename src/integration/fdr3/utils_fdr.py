from typing import Any, Dict, Optional

from requests import Response

from src.utility.rest.rest_client import RestClient


DEFAULT_ENDPOINTS = {
    # These are generic mappings and may need to be adapted to the real API paths
    "create": ("POST", "/fdr"),
    "add_payments": ("POST", "/fdr/{flow_name}/payments"),
    "publish": ("POST", "/fdr/{flow_name}/publish"),
    "delete_flow": ("DELETE", "/fdr/{flow_name}"),
    "get_published": ("GET", "/fdr/published/{flow_name}"),
    "get_all_published": ("GET", "/fdr/published"),
    "get_created_payments": ("GET", "/fdr/{flow_name}/payments/created"),
    "delete_payments": ("DELETE", "/fdr/{flow_name}/payments"),
}


def _build_create_payload(flow_name: str, flow_date: str, tot_payments: int, sum_payments: int) -> Dict[str, Any]:
    """Factory payload minimale per la creazione di un FdR.

    Se il test/feature richiede campi aggiuntivi, passare "payload_override" a
    perform_fdr_action() con il body completo.
    """
    return {
        "fdr": flow_name,
        "fdrDate": flow_date,
        "sender": {
            "type": "LEGAL_PERSON",
            "id": "SELBIT2B",
            "pspId": "#psp#",
            "pspName": "Bank",
            "pspBrokerId": "#broker_psp#",
            "channelId": "#channel#",
            "password": "#channel_password#",
        },
        "receiver": {
            "id": "APPBIT2B",
            "organizationId": "#organization#",
            "organizationName": "Comune di XYZ",
        },
        "regulation": "SEPA - Bonifico xzy",
        "regulationDate": flow_date,
        "bicCodePouringBank": "UNCRITMMXXX",
        "totPayments": tot_payments,
        "sumPayments": sum_payments,
    }


def perform_fdr_action(
    client: RestClient,
    action: str,
    *,
    flow_name: Optional[str] = None,
    flow_date: Optional[str] = None,
    payload_override: Optional[Dict[str, Any]] = None,
    n_payments: Optional[int] = None,
    sum_payments: Optional[int] = None,
    expected_status: Optional[int] = None,
    checks: Optional[Dict[str, Any]] = None,
    endpoints: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
) -> Response:
    """Esegue un'azione FdR parametrica utilizzando RestClient.

    Args:
        client: istanza di RestClient (vedi src.utility.rest)
        action: nome dell'azione (es. "create", "add_payments", "publish", ...)
        flow_name / flow_date: usati per costruire path o payload quando necessari
        payload_override: body JSON completo (se presente viene usato al posto del payload factory)
        n_payments, sum_payments: usati per costruire il payload di add_payments
        expected_status: se fornito, viene assertato che response.status_code == expected_status
        checks: mappa chiave->valore da verificare nella response.json()
        endpoints: mappatura custom per sovrascrivere DEFAULT_ENDPOINTS
        query_params: query string da passare alla chiamata

    Ritorna:
        requests.Response

    Nota: le path di DEFAULT_ENDPOINTS sono indicative e devono essere adattate se
    l'API reale usa nomi differenti.
    """
    endpoints = {**DEFAULT_ENDPOINTS, **(endpoints or {})}

    if action not in endpoints:
        raise ValueError(f"Unknown action '{action}'. Available: {list(endpoints.keys())}")

    method, path_template = endpoints[action]
    path = path_template.format(flow_name=flow_name or "", flow_date=flow_date or "")

    json_body = None
    if action == "create":
        if payload_override is not None:
            json_body = payload_override
        else:
            if flow_name is None or flow_date is None or n_payments is None or sum_payments is None:
                raise ValueError("create requires flow_name, flow_date, n_payments and sum_payments when payload_override is not provided")
            json_body = _build_create_payload(flow_name, flow_date, n_payments, sum_payments)

    elif action == "add_payments":
        if payload_override is not None:
            json_body = payload_override
        else:
            if n_payments is None or sum_payments is None:
                raise ValueError("add_payments requires n_payments and sum_payments when payload_override is not provided")
            # minimal payments payload: lista sintetica con n elementi e somma totale
            payments = [{"amount": max(1, sum_payments // n_payments)} for _ in range(n_payments)]
            # adjust last element to match exact sum
            if n_payments > 0:
                diff = sum_payments - sum(p["amount"] for p in payments)
                payments[-1]["amount"] += diff
            json_body = {"payments": payments}

    elif action == "delete_payments":
        json_body = payload_override or {"deleteCount": n_payments or 0}

    # altre azioni non necessitano di body

    response = client.request(method, path, json_body=json_body, params=query_params)

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
