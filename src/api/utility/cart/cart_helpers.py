"""
Helper specifici per i cart-test:
- client HTTP (post_cart)
- data builders (build_cart_body, build_multiple_notices_body)
- utility di generazione dati (generate_notice_code, get_checkout_host)
"""
import os
import random

import requests

from src.api.utility.http_client import request as http_request


# ---------------------------------------------------------------------------
# Utility — environment readers
# ---------------------------------------------------------------------------

def get_checkout_host() -> str:
    return os.environ.get("CHECKOUT_HOST", "https://api.dev.platform.pagopa.it")


def generate_notice_code(prefix_env_var: str = "NOTICE_CODE_PREFIX") -> str:
    """Genera un notice code casuale valido dal prefisso letto da una env var."""
    prefix = os.environ.get(prefix_env_var)
    if not prefix:
        raise EnvironmentError(f"Environment variable {prefix_env_var} not set.")
    min_val = int(prefix + "10000000000000")
    max_val = int(prefix + "19999999999999")
    return str(random.randint(min_val, max_val))


# ---------------------------------------------------------------------------
# Utility — data builders
# ---------------------------------------------------------------------------

VALID_CART_BODY_TEMPLATE = {
    "amount": 12000,
    "companyName": "Nome EC",
    "description": "Oggetto del pagamento",
}

INVALID_CART_BODY = {
    "paymentNotices": [
        {
            "noticeNumber": "302000100440009424",
            "fiscalCode": "1",
            "amount": 10000,
            "companyName": None,
            "description": None,
        }
    ],
    "returnurls": {
        "returnOkUrl": "https://returnOkUrl",
        "returnCancelUrl": "https://returnCancelUrl",
        "returnErrorUrl": "https://returnErrorUrl",
    },
    "emailNotice": "test@test.it",
}

MULTIPLE_PAYMENT_NOTICES = [
    {"noticeNumber": "302010000000000001", "fiscalCode": "77777777777", "amount": 10000, "companyName": "Nome EC", "description": "Oggetto del pagamento"},
    {"noticeNumber": "302010000000000002", "fiscalCode": "77777777777", "amount": 10000, "companyName": "Nome EC", "description": "Oggetto del pagamento"},
    {"noticeNumber": "302010000000000003", "fiscalCode": "77777777777", "amount": 10000, "companyName": "Nome EC", "description": "Oggetto del pagamento"},
    {"noticeNumber": "302010000000000004", "fiscalCode": "77777777777", "amount": 10000, "companyName": "Nome EC", "description": "Oggetto del pagamento"},
    {"noticeNumber": "302010000000000005", "fiscalCode": "77777777777", "amount": 10000, "companyName": "Nome EC", "description": "Oggetto del pagamento"},
    {"noticeNumber": "302010000000000006", "fiscalCode": "77777777777", "amount": 10000, "companyName": "Nome EC", "description": "Oggetto del pagamento"},
]


def build_cart_body(notice_code: str, fiscal_code: str, email: str) -> dict:
    """Costruisce il body per una richiesta cart valida."""
    return {
        "paymentNotices": [
            {
                "noticeNumber": notice_code,
                "fiscalCode": fiscal_code,
                "amount": VALID_CART_BODY_TEMPLATE["amount"],
                "companyName": VALID_CART_BODY_TEMPLATE["companyName"],
                "description": VALID_CART_BODY_TEMPLATE["description"],
            }
        ],
        "returnUrls": {
            "returnOkUrl": "https://returnOkUrl",
            "returnCancelUrl": "https://returnCancelUrl",
            "returnErrorUrl": "https://returnErrorUrl",
        },
        "emailNotice": email,
        "idCart": "3de77d19-1655-4eaa-8bbb-14be203584d4",
        "allCCP": False,
    }


def build_multiple_notices_body(count: int = 6) -> dict:
    if count < 1:
        raise ValueError("count must be >= 1")

    notices = []
    for i in range(count):
        base_notice = MULTIPLE_PAYMENT_NOTICES[i % len(MULTIPLE_PAYMENT_NOTICES)]
        notice = dict(base_notice)
        if i >= len(MULTIPLE_PAYMENT_NOTICES):
            notice["noticeNumber"] = str(int(base_notice["noticeNumber"]) + i)
        notices.append(notice)

    return {
        "paymentNotices": notices,
        "returnUrls": {
            "returnOkUrl": "https://returnOkUrl",
            "returnCancelUrl": "https://returnCancelUrl",
            "returnErrorUrl": "https://returnErrorUrl",
        },
        "emailNotice": "test@test.it",
    }


# ---------------------------------------------------------------------------
# HTTP Client
# ---------------------------------------------------------------------------

def post_cart(endpoint: str, body: dict) -> requests.Response:
    """POST senza seguire redirect (allow_redirects=False)."""
    url = f"{get_checkout_host()}{endpoint}"
    return http_request("POST", url, json=body, allow_redirects=False, timeout=30)
