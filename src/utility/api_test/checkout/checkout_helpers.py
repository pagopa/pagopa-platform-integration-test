"""
Helper specifici per i checkout-tests NPG:
- Client HTTP per CHECKOUT_HOST e NPG_HOST
- Builder per request body
- Generazione dati, estrazione dati da response NPG iframe URL
- Polling transazione
"""
import os
import random
import time
import uuid
from typing import Any
from urllib.parse import parse_qs, urlparse

import requests


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

PAYMENT_REQUESTS_V1 = "/ecommerce/checkout/v1/payment-requests/{rpt_id}"
PAYMENT_METHODS_V1 = "/ecommerce/checkout/v1/payment-methods"
PAYMENT_METHODS_V2 = "/ecommerce/checkout/v2/payment-methods"
PAYMENT_METHOD_DETAILS_V1 = "/ecommerce/checkout/v1/payment-methods/{method_id}"
PAYMENT_METHOD_FEES_V1 = "/ecommerce/checkout/v1/payment-methods/{method_id}/fees"
PAYMENT_METHOD_SESSIONS_V1 = "/ecommerce/checkout/v1/payment-methods/{method_id}/sessions"
PAYMENT_METHOD_SESSION_V1 = "/ecommerce/checkout/v1/payment-methods/{method_id}/sessions/{order_id}"
TRANSACTIONS_V2 = "/ecommerce/checkout/v2/transactions"
TRANSACTION_V1 = "/ecommerce/checkout/v1/transactions/{transaction_id}"
TRANSACTION_V2 = "/ecommerce/checkout/v2/transactions/{transaction_id}"
TRANSACTION_AUTH_V1 = "/ecommerce/checkout/v1/transactions/{transaction_id}/auth-requests"
TRANSACTION_OUTCOMES_V1 = "/ecommerce/checkout/v1/transactions/{transaction_id}/outcomes"
NPG_FIELD_SETTINGS = "/fe/build/field_settings/{field_id}"
NPG_TEXT_FILL = "/fe/build/text/"


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

def get_checkout_host() -> str:
    return os.environ.get("CHECKOUT_HOST", "https://api.dev.platform.pagopa.it")


def get_npg_host() -> str:
    return os.environ.get("NPG_HOST", "https://stg-ta.nexigroup.com")


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(f"Environment variable {name!r} not set.")
    return value


def get_deployment_header() -> dict[str, str]:
    value = os.environ.get("USE_BETA_BACKEND_HEADER")
    if not value:
        return {}
    return {"deployment": value}


def get_specific_deployment_header(env_key: str) -> dict[str, str]:
    value = os.environ.get(env_key)
    if not value:
        return get_deployment_header()
    return {"deployment": value}


def generate_notice_code() -> str:
    """Genera un notice code casuale a partire dal prefisso NOTICE_CODE_PREFIX."""
    prefix = get_required_env("NOTICE_CODE_PREFIX")
    min_val = int(prefix + "10000000000000")
    max_val = int(prefix + "19999999999999")
    return str(random.randint(min_val, max_val))


def build_rpt_id(fiscal_code: str, notice_code: str) -> str:
    return fiscal_code + notice_code


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------

def _request(
    method: str,
    url: str,
    *,
    json: dict | None = None,
    token: str | None = None,
    extra_headers: dict | None = None,
    allow_redirects: bool = False,
) -> requests.Response:
    headers: dict[str, str] = {}
    if json is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if extra_headers:
        headers.update(extra_headers)
    return requests.request(
        method=method,
        url=url,
        headers=headers,
        json=json,
        allow_redirects=allow_redirects,
        timeout=30,
    )


def request_checkout(
    method: str,
    endpoint: str,
    *,
    json: dict | None = None,
    token: str | None = None,
    extra_headers: dict | None = None,
    deployment_env_key: str = "USE_BETA_BACKEND_HEADER",
) -> requests.Response:
    deployment_hdrs = get_specific_deployment_header(deployment_env_key)
    all_headers = {**deployment_hdrs, **(extra_headers or {})}
    return _request(
        method,
        f"{get_checkout_host()}{endpoint}",
        json=json,
        token=token,
        extra_headers=all_headers,
    )


def request_npg(
    method: str,
    endpoint: str,
    *,
    json: dict | None = None,
    extra_headers: dict | None = None,
) -> requests.Response:
    return _request(
        method,
        f"{get_npg_host()}{endpoint}",
        json=json,
        extra_headers=extra_headers,
    )


# ---------------------------------------------------------------------------
# Payment method helpers
# ---------------------------------------------------------------------------

def get_all_payment_methods_v1() -> requests.Response:
    return request_checkout(
        "GET",
        PAYMENT_METHODS_V1,
        deployment_env_key="DEPLOYMENT_PAYMENT_METHODS",
    )


def get_all_payment_methods_v2() -> requests.Response:
    body = {
        "userTouchpoint": "CHECKOUT",
        "totalAmount": 12000,
        "paymentNotice": [
            {"paymentAmount": 12000, "primaryCreditorInstitution": "77777777777"},
        ],
    }
    return request_checkout(
        "POST",
        PAYMENT_METHODS_V2,
        json=body,
        deployment_env_key="DEPLOYMENT",
    )


def resolve_credit_card_payment_method_id() -> str:
    """Recupera l'id del metodo di pagamento carte di credito (paymentTypeCode=CP) via v2."""
    response = get_all_payment_methods_v2()
    response.raise_for_status()
    methods = response.json().get("paymentMethods", [])
    cp_methods = [m for m in methods if m.get("paymentTypeCode") == "CP"]
    if not cp_methods:
        raise AssertionError("Nessun metodo di pagamento CP trovato nella risposta.")
    return cp_methods[0]["id"]


def get_payment_method_details(method_id: str) -> requests.Response:
    endpoint = PAYMENT_METHOD_DETAILS_V1.format(method_id=method_id)
    return request_checkout(
        "GET",
        endpoint,
        deployment_env_key="DEPLOYMENT_PAYMENT_METHODS",
    )


def compute_fee(method_id: str, transaction_id: str, auth_token: str) -> requests.Response:
    endpoint = PAYMENT_METHOD_FEES_V1.format(method_id=method_id)
    body = {
        "bin": "511111",
        "touchpoint": "CHECKOUT",
        "paymentAmount": 100,
        "isAllCCP": False,
        "primaryCreditorInstitution": "77777777777",
        "transferList": [
            {"creditorInstitution": "77777777777", "digitalStamp": False}
        ],
    }
    extra_headers = {"x-transaction-id-from-client": transaction_id}
    return request_checkout(
        "POST",
        endpoint,
        json=body,
        token=auth_token,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_PAYMENT_METHODS",
    )


# ---------------------------------------------------------------------------
# Payment requests (verify) helpers
# ---------------------------------------------------------------------------

def verify_payment(fiscal_code: str, notice_code: str) -> requests.Response:
    rpt_id = build_rpt_id(fiscal_code, notice_code)
    endpoint = PAYMENT_REQUESTS_V1.format(rpt_id=rpt_id) + "?recaptchaResponse=token"
    return request_checkout(
        "GET",
        endpoint,
        deployment_env_key="DEPLOYMENT_PAYMENT_REQUESTS",
    )


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def _extract_npg_params_from_url(field_url: str) -> dict[str, str]:
    """Estrae correlationid, sessionid, id dall'URL dell'iframe NPG."""
    parsed = urlparse(field_url)
    query_params = parse_qs(parsed.query)

    def get_param(key: str) -> str:
        values = query_params.get(key, [])
        if not values:
            raise AssertionError(f"Parametro NPG mancante nell'iframe URL: {key}")
        value = values[0]
        return value.replace("%2F", "/").replace("%2B", "+").replace("%3D", "=")

    return {
        "correlationid": get_param("correlationid"),
        "sessionid": get_param("sessionid"),
        "id": get_param("id"),
    }


def create_session(payment_method_id: str, language: str = "it") -> requests.Response:
    endpoint = (
        PAYMENT_METHOD_SESSIONS_V1.format(method_id=payment_method_id)
        + "?recaptchaResponse=test"
    )
    extra_headers = {"lang": language}
    return request_checkout(
        "POST",
        endpoint,
        json={},
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def extract_session_data(response_body: dict) -> dict[str, str]:
    """Estrae e restituisce i dati NPG dalla risposta di create session."""
    order_id = response_body["orderId"]
    correlation_id = response_body.get("correlationId", "")
    field_url = response_body["paymentMethodData"]["form"][0]["src"]
    npg_params = _extract_npg_params_from_url(field_url)
    return {
        "order_id": order_id,
        "correlation_id": correlation_id,
        "field_url": field_url,
        "npg_correlation_id": npg_params["correlationid"],
        "npg_session_id": npg_params["sessionid"],
        "npg_field_id": npg_params["id"],
    }


# ---------------------------------------------------------------------------
# NPG external service helpers
# ---------------------------------------------------------------------------

def populate_npg_cookies(
    npg_correlation_id: str, npg_session_id: str, npg_field_id: str
) -> requests.Response:
    """GET NPG field settings per popolare i cookie NPG."""
    endpoint = NPG_FIELD_SETTINGS.format(field_id=npg_field_id) + "?lang=ITA"
    extra_headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Idempotency-Key": str(uuid.uuid4()),
        "Correlation-Id": npg_correlation_id,
        "session": npg_session_id,
    }
    return request_npg("GET", endpoint, extra_headers=extra_headers)


def fill_npg_card_fields(
    npg_correlation_id: str, npg_session_id: str
) -> requests.Response:
    """POST dati carta di test ai campi NPG."""
    extra_headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Idempotency-Key": str(uuid.uuid4()),
        "Correlation-Id": npg_correlation_id,
        "session": npg_session_id,
    }
    body = {
        "fieldValues": [
            {"id": "EXPIRATION_DATE", "value": get_required_env("NPG_TEST_EXPIRATION_DATE")},
            {"id": "CARD_NUMBER", "value": get_required_env("NPG_TEST_CARD_PAN")},
            {"id": "SECURITY_CODE", "value": get_required_env("NPG_TEST_SECURITY_CODE")},
            {"id": "CARDHOLDER_NAME", "value": get_required_env("NPG_TEST_CARDHOLDER_NAME")},
        ]
    }
    return request_npg("POST", NPG_TEXT_FILL, json=body, extra_headers=extra_headers)


# ---------------------------------------------------------------------------
# Transaction helpers
# ---------------------------------------------------------------------------

def create_transaction(
    fiscal_code: str,
    notice_code: str,
    order_id: str,
    correlation_id: str,
    email: str = "mario.rossi@example.com",
) -> requests.Response:
    rpt_id = build_rpt_id(fiscal_code, notice_code)
    endpoint = f"{TRANSACTIONS_V2}?recaptchaResponse=token"
    body = {
        "paymentNotices": [{"rptId": rpt_id, "amount": 100}],
        "orderId": order_id,
        "email": email,
    }
    extra_headers = {"x-correlation-id": correlation_id}
    return request_checkout(
        "POST",
        endpoint,
        json=body,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def create_transaction_without_order_id(
    fiscal_code: str,
    notice_code: str,
    correlation_id: str,
) -> requests.Response:
    rpt_id = build_rpt_id(fiscal_code, notice_code)
    endpoint = f"{TRANSACTIONS_V2}?recaptchaResponse=token"
    body = {
        "paymentNotices": [{"rptId": rpt_id, "amount": 100}],
        "email": "mario.rossi@example.com",
    }
    extra_headers = {"x-correlation-id": correlation_id}
    return request_checkout(
        "POST",
        endpoint,
        json=body,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def delete_transaction(transaction_id: str, auth_token: str) -> requests.Response:
    endpoint = TRANSACTION_V1.format(transaction_id=transaction_id)
    return request_checkout(
        "DELETE",
        endpoint,
        token=auth_token,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def get_transaction_v1(transaction_id: str, auth_token: str) -> requests.Response:
    endpoint = TRANSACTION_V1.format(transaction_id=transaction_id)
    extra_headers = {"lang": "it"}
    return request_checkout(
        "GET",
        endpoint,
        token=auth_token,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def get_transaction_v2(transaction_id: str, auth_token: str) -> requests.Response:
    endpoint = TRANSACTION_V2.format(transaction_id=transaction_id)
    extra_headers = {"lang": "it"}
    return request_checkout(
        "GET",
        endpoint,
        token=auth_token,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def get_transaction_outcomes_v1(transaction_id: str, auth_token: str) -> requests.Response:
    endpoint = TRANSACTION_OUTCOMES_V1.format(transaction_id=transaction_id)
    extra_headers = {"lang": "it"}
    return request_checkout(
        "GET",
        endpoint,
        token=auth_token,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def request_authorization(
    transaction_id: str,
    auth_token: str,
    payment_method_id: str,
    order_id: str,
    amount: int,
    lang: str = "it",
) -> requests.Response:
    psp_id = get_required_env("PSP_ID")
    fee = int(os.environ.get("FEE", "100"))
    endpoint = TRANSACTION_AUTH_V1.format(transaction_id=transaction_id)
    body = {
        "amount": amount,
        "fee": fee,
        "paymentInstrumentId": payment_method_id,
        "pspId": psp_id,
        "isAllCCP": False,
        "language": "IT",
        "details": {
            "detailType": "cards",
            "orderId": order_id,
        },
    }
    extra_headers = {"lang": lang}
    return request_checkout(
        "POST",
        endpoint,
        json=body,
        token=auth_token,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


def request_authorization_without_token(
    transaction_id: str,
    payment_method_id: str,
    order_id: str,
    amount: int,
    lang: str = "it",
) -> requests.Response:
    """Richiesta di autorizzazione senza JWT token (test negativo)."""
    psp_id = get_required_env("PSP_ID") + "1"  # wrong psp_id as per original collection
    fee = int(os.environ.get("FEE", "100"))
    endpoint = TRANSACTION_AUTH_V1.format(transaction_id=transaction_id)
    body = {
        "amount": amount,
        "fee": fee,
        "paymentInstrumentId": payment_method_id,
        "pspId": psp_id,
        "isAllCCP": False,
        "language": "IT",
        "details": {
            "detailType": "cards",
            "orderId": order_id,
        },
    }
    extra_headers = {"lang": lang}
    return request_checkout(
        "POST",
        endpoint,
        json=body,
        # no token
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT_TRANSACTION_SERVICE",
    )


# ---------------------------------------------------------------------------
# Card data helpers
# ---------------------------------------------------------------------------

def get_card_data(
    payment_method_id: str,
    order_id: str,
    transaction_id: str,
    auth_token: str,
) -> requests.Response:
    endpoint = PAYMENT_METHOD_SESSION_V1.format(
        method_id=payment_method_id, order_id=order_id
    )
    extra_headers = {"x-transaction-id-from-client": transaction_id}
    return request_checkout(
        "GET",
        endpoint,
        token=auth_token,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT",
    )


def get_card_data_without_token(
    payment_method_id: str,
    order_id: str,
    transaction_id: str,
) -> requests.Response:
    endpoint = PAYMENT_METHOD_SESSION_V1.format(
        method_id=payment_method_id, order_id=order_id
    )
    extra_headers = {"x-transaction-id-from-client": transaction_id}
    return request_checkout(
        "GET",
        endpoint,
        extra_headers=extra_headers,
        deployment_env_key="DEPLOYMENT",
    )


# ---------------------------------------------------------------------------
# Polling helper
# ---------------------------------------------------------------------------

def poll_transaction_until_status(
    transaction_id: str,
    auth_token: str,
    wanted_status: str,
    max_attempts: int = 10,
    interval_sec: float = 1.0,
) -> str:
    """Polling su GET /v2/transactions/:id fino al raggiungimento di wanted_status."""
    endpoint = TRANSACTION_V2.format(transaction_id=transaction_id)
    last_status = None
    for _ in range(max_attempts):
        time.sleep(interval_sec)
        response = request_checkout("GET", endpoint, token=auth_token)
        if response.status_code == 200:
            last_status = response.json().get("status")
            if last_status == wanted_status:
                return last_status
    raise AssertionError(
        f"Transazione {transaction_id!r} non ha raggiunto lo stato {wanted_status!r} "
        f"dopo {max_attempts} tentativi. Ultimo stato: {last_status!r}"
    )
