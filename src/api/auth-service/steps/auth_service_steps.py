import json
import sys
from pathlib import Path

from behave import given, then, when

HELPERS_DIR = Path(__file__).resolve().parents[3] / "utility" / "api_test" / "auth_service"
if str(HELPERS_DIR) not in sys.path:
    sys.path.insert(0, str(HELPERS_DIR))

from auth_service_helpers import (  # noqa: E402
    LOGOUT_ENDPOINT,
    TOKEN_ENDPOINT,
    USERS_ENDPOINT,
    build_auth_token_body,
    build_login_url,
    build_payment_requests_endpoint,
    extract_auth_code_from_html,
    get_checkout_host,
    get_required_env,
    parse_login_redirect_payload,
    request,
)


@given("that checkout host is configured through environment variable")
def step_checkout_host_configured(context):
    host = get_checkout_host()
    print(f"  -> CHECKOUT_HOST: {host}")


@given("the auth service environment variables are configured")
def step_auth_env_configured(context):
    required_names = [
        "FAKE_RECAPTCHA_NOT_VALIDATED",
        "AUTH_USER_EXPECT_NAME",
        "AUTH_USER_EXPECT_SURNAME",
    ]
    for name in required_names:
        value = get_required_env(name)
        print(f"  -> {name}: {value}")


@when("the user requests the auth login URL")
def step_request_auth_login(context):
    context.response = request("GET", build_login_url(), absolute_url=True)


@then("the auth login response exposes a valid redirect URL")
def step_login_response_has_redirect(context):
    payload = context.response.json()
    redirect_data = parse_login_redirect_payload(payload)
    context.login_payload = payload
    context.redirect_url = redirect_data["redirect_url"]
    context.state = redirect_data["state"]
    context.nonce = redirect_data["nonce"]
    print(f"  -> REDIRECT_URL: {context.redirect_url}")


@when("the user opens the auth redirect URL")
def step_open_auth_redirect(context):
    context.response = request("GET", context.redirect_url, absolute_url=True)


@then("the auth code is extracted from the redirect response")
def step_extract_auth_code(context):
    context.auth_code = extract_auth_code_from_html(context.response.text)
    print(f"  -> AUTH_CODE: {context.auth_code}")


@when("the user exchanges the auth code for a session token")
def step_exchange_auth_code(context):
    body = build_auth_token_body(context.state, context.auth_code)
    context.response = request("POST", TOKEN_ENDPOINT, json=body)


@when("the user exchanges an invalid auth code for a session token")
def step_exchange_invalid_auth_code(context):
    body = build_auth_token_body("some-invalid-state", "some-invalid-code")
    context.response = request("POST", TOKEN_ENDPOINT, json=body)


@then("the auth token is returned in the response")
def step_auth_token_returned(context):
    payload = context.response.json()
    auth_token = payload.get("authToken")
    assert isinstance(auth_token, str) and auth_token, (
        f"Expected authToken in response body, received: {json.dumps(payload, indent=2)}"
    )
    context.session_token = auth_token
    print("  -> SESSION_TOKEN acquired")


@given("an invalid auth session token")
def step_invalid_auth_session_token(context):
    context.session_token = context.invalid_session_token


@when("the user requests the authenticated user profile with the active session token")
def step_request_user_profile_active_token(context):
    context.response = request("GET", USERS_ENDPOINT, token=context.session_token)


@when("the user requests the authenticated user profile with the invalid session token")
def step_request_user_profile_invalid_token(context):
    context.response = request("GET", USERS_ENDPOINT, token=context.invalid_session_token)


@then("the authenticated user profile matches the configured auth user")
def step_verify_user_profile(context):
    payload = context.response.json()
    expected_name = get_required_env("AUTH_USER_EXPECT_NAME")
    expected_surname = get_required_env("AUTH_USER_EXPECT_SURNAME")
    assert payload.get("name") == expected_name, (
        f"Expected name {expected_name}, received {payload.get('name')}. Body: {json.dumps(payload, indent=2)}"
    )
    assert payload.get("familyName") == expected_surname, (
        f"Expected familyName {expected_surname}, received {payload.get('familyName')}. Body: {json.dumps(payload, indent=2)}"
    )
    context.user_profile = payload


@when("the user requests an authenticated payment request with the invalid session token")
def step_request_payment_with_invalid_token(context):
    endpoint = build_payment_requests_endpoint()
    context.response = request("GET", endpoint, token=context.invalid_session_token)


@when("the user logs out from auth service with the active session token")
def step_logout_auth_service(context):
    context.response = request("POST", LOGOUT_ENDPOINT, token=context.session_token)


@then("the response has status code {status_code:d}")
def step_response_status_code(context, status_code):
    actual = context.response.status_code
    assert actual == status_code, (
        f"Expected status code {status_code}, received {actual}. Body: {context.response.text}"
    )