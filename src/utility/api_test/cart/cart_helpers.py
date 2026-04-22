"""
Helper specifici per i cart-test:
- client HTTP (post_cart)
- data builders (build_cart_body, build_multiple_notices_body)
- utility di generazione dati (generate_notice_code, get_checkout_host)
"""
import os
import random

import requests


# ---------------------------------------------------------------------------
# Utility — environment readers
# ---------------------------------------------------------------------------

def get_checkout_host() -> str:
    return os.environ.get("CHECKOUT_HOST", "https://api.dev.platform.pagopa.it")


def generate_notice_code() -> str:
    """Genera un notice code casuale valido a partire dal prefisso NOTICE_CODE_PREFIX."""
    prefix = os.environ.get("NOTICE_CODE_PREFIX")
    if not prefix:
        raise EnvironmentError("Environment variable NOTICE_CODE_PREFIX not set.")
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
    {"noticeNumber": "302000100440009421", "fiscalCode": "11111111111", "amount": 10000, "companyName": "AA", "description": "BB"},
    {"noticeNumber": "302000100440009422", "fiscalCode": "11111111111", "amount": 10000, "companyName": "CC", "description": "DD"},
    {"noticeNumber": "302000100440009423", "fiscalCode": "11111111111", "amount": 10000, "companyName": "EE", "description": "FF"},
    {"noticeNumber": "302000100440009424", "fiscalCode": "11111111111", "amount": 10000, "companyName": "GG", "description": "HH"},
    {"noticeNumber": "302000100440009425", "fiscalCode": "11111111111", "amount": 10000, "companyName": "JJ", "description": "KK"},
    {"noticeNumber": "302000100440009426", "fiscalCode": "11111111111", "amount": 10000, "companyName": "II", "description": "LL"},
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


def build_multiple_notices_body() -> dict:
    return {
        "paymentNotices": MULTIPLE_PAYMENT_NOTICES,
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
    return requests.post(url, json=body, allow_redirects=False, timeout=30)
