import os

from behave import given, when, then

from src.utility.api_test.cart.cart_helpers import (
    get_checkout_host,
    generate_notice_code,
    build_cart_body,
    build_multiple_notices_body,
    post_cart,
    INVALID_CART_BODY,
)


# ---------------------------------------------------------------------------
# Given — Context / Background
# ---------------------------------------------------------------------------

@given("that checkout host is configured through environment variable")
def step_host_configurato(context):
    host = get_checkout_host()
    print(f"  → CHECKOUT_HOST: {host}")


@given('a valid random notice code generated from the prefix configured in "{prefix}"')
def step_codice_avviso(context, prefix: str):
    context.notice_code = generate_notice_code()
    print(f"  → VALID_NOTICE_CODE generated: {context.notice_code}")

@given('a valid PA fiscal code configured in "{cod_fis}"')
def step_codice_fiscale(context, cod_fis: str):
    fiscal_code = os.environ.get(cod_fis)
    if not fiscal_code:
        raise EnvironmentError(f"Environment variable {cod_fis} not set.")
    context.fiscal_code = fiscal_code
    print(f"  → {cod_fis}: {context.fiscal_code}")


# ---------------------------------------------------------------------------
# When — Actions
# ---------------------------------------------------------------------------

@when('I send a POST to "{endpoint}" with cart data and email "{email}"')
def step_post_cart_ok(context, endpoint: str, email: str):
    body = build_cart_body(context.notice_code, context.fiscal_code, email)
    context.response = post_cart(endpoint, body)


@when('I send a POST to "{endpoint}" with invalid body')
def step_post_cart_ko_invalid(context, endpoint: str):
    context.response = post_cart(endpoint, INVALID_CART_BODY)


@when('I send a POST to "{endpoint}" with {count:d} payment notices')
def step_post_cart_ko_multiple(context, endpoint: str, count: int):
    body = build_multiple_notices_body()
    context.response = post_cart(endpoint, body)


# ---------------------------------------------------------------------------
# Then — Assertions
# ---------------------------------------------------------------------------

@then("the response has status code {status_code:d}")
def step_verifica_status_code(context, status_code: int):
    actual = context.response.status_code
    assert actual == status_code, \
        f"Expected status code: {status_code}, received: {actual}.\nBody: {context.response.text}"


@then('the response contains the header "{header_name}"')
def step_verifica_header(context, header_name: str):
    headers_lower = {k.lower(): v for k, v in context.response.headers.items()}
    assert header_name.lower() in headers_lower, \
        f'Header "{header_name}" not found. Available headers: {list(context.response.headers.keys())}'
    header_value = headers_lower[header_name.lower()]
    setattr(context, header_name, header_value)


@then('the CART_ID is extracted from the header "{header_name}"')
def step_estrai_cart_id(context, header_name: str):
    header_value = context.get(header_name)
    assert header_value, f'Header "{header_name}" not present in response.'
    context.cart_id = header_value[header_value.rfind("/") + 1:]
    assert context.cart_id, "CART_ID not extracted from Location header"
    print(f"  → CART_ID extracted: {context.cart_id}")
