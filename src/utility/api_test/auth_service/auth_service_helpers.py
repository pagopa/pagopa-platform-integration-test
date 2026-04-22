import os
import random
import re
from typing import Any
from urllib.parse import parse_qs, urlparse

import requests


LOGIN_ENDPOINT = "/checkout/auth-service/v1/auth/login"
TOKEN_ENDPOINT = "/checkout/auth-service/v1/auth/token"
USERS_ENDPOINT = "/checkout/auth-service/v1/auth/users"
LOGOUT_ENDPOINT = "/checkout/auth-service/v1/auth/logout"
PAYMENT_REQUESTS_ENDPOINT_TEMPLATE = "/ecommerce/checkout/v3/auth/payment-requests/77777777777302016{suffix}"


def get_checkout_host() -> str:
    return os.environ.get("CHECKOUT_HOST", "https://api.dev.platform.pagopa.it")


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(f"Environment variable {name} not set.")
    return value


def get_deployment_headers() -> dict[str, str]:
    deployment = os.environ.get("USE_BETA_BACKEND_HEADER")
    if not deployment:
        return {}
    return {"deployment": deployment}


def build_login_url() -> str:
    recaptcha = get_required_env("FAKE_RECAPTCHA_NOT_VALIDATED")
    return f"{get_checkout_host()}{LOGIN_ENDPOINT}?recaptcha={recaptcha}"


def build_auth_token_body(state: str, auth_code: str) -> dict[str, str]:
    return {
        "state": state,
        "authCode": auth_code,
    }


def build_payment_requests_endpoint() -> str:
    suffix = "".join(random.choice("0123456789") for _ in range(12))
    return PAYMENT_REQUESTS_ENDPOINT_TEMPLATE.format(suffix=suffix)


def parse_login_redirect_payload(payload: dict[str, Any]) -> dict[str, str]:
    redirect_url = payload.get("urlRedirect")
    if not isinstance(redirect_url, str) or not redirect_url:
        raise AssertionError(f"Missing or invalid urlRedirect in payload: {payload}")

    parsed = urlparse(redirect_url)
    query_params = parse_qs(parsed.query)

    response_type = query_params.get("response_type", [""])[0]
    scope = query_params.get("scope", [""])[0]
    client_id = query_params.get("client_id", [""])[0]
    state = query_params.get("state", [""])[0]
    nonce = query_params.get("nonce", [""])[0]
    redirect_uri = query_params.get("redirect_uri", [""])[0]

    if response_type != "CODE":
        raise AssertionError(f"Unexpected response_type: {response_type}")
    if scope != "openid":
        raise AssertionError(f"Unexpected scope: {scope}")

    for field_name, field_value in {
        "client_id": client_id,
        "state": state,
        "nonce": nonce,
        "redirect_uri": redirect_uri,
    }.items():
        if not field_value:
            raise AssertionError(f"Missing {field_name} in redirect URL: {redirect_url}")

    return {
        "redirect_url": redirect_url,
        "response_type": response_type,
        "scope": scope,
        "client_id": client_id,
        "state": state,
        "nonce": nonce,
        "redirect_uri": redirect_uri,
    }


def extract_auth_code_from_html(html: str) -> str:
    match = re.search(r"code=([^&\"']+)", html)
    if not match:
        raise AssertionError("Auth code not found in redirect response body.")
    return match.group(1)


def request(
    method: str,
    endpoint: str,
    *,
    json: dict[str, Any] | None = None,
    token: str | None = None,
    absolute_url: bool = False,
) -> requests.Response:
    headers = dict(get_deployment_headers())
    if json is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = endpoint if absolute_url else f"{get_checkout_host()}{endpoint}"
    return requests.request(
        method=method,
        url=url,
        headers=headers,
        json=json,
        allow_redirects=False,
        timeout=30,
    )