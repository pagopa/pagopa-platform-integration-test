import os

from behave import given, when, then

from src.api.utility.cart.cart_helpers import (
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

@given("l'host di checkout configurato tramite variabile d'ambiente")
def step_host_configurato(context):
    host = get_checkout_host()
    print(f"  → CHECKOUT_HOST: {host}")


@given('un codice avviso casuale valido generato dal prefisso configurato in "{prefix}"')
def step_codice_avviso(context, prefix: str):
    context.notice_code = generate_notice_code(prefix)
    print(f"  → VALID_NOTICE_CODE generated: {context.notice_code}")

@given('un codice fiscale PA valido configurato in "{cod_fis}"')
def step_codice_fiscale(context, cod_fis: str):
    fiscal_code = os.environ.get(cod_fis)
    if not fiscal_code:
        raise EnvironmentError(f"Environment variable {cod_fis} not set.")
    context.fiscal_code = fiscal_code
    print(f"  → {cod_fis}: {context.fiscal_code}")


# ---------------------------------------------------------------------------
# When — Actions
# ---------------------------------------------------------------------------

CART_ENDPOINT = "/checkout/ec/v1/carts"


@when('l\'utente invia un carrello con email "{email}"')
def step_post_cart_ok(context, email: str):
    body = build_cart_body(context.notice_code, context.fiscal_code, email)
    context.response = post_cart(CART_ENDPOINT, body)


@when('l\'utente invia un carrello con un body non valido')
def step_post_cart_ko_invalid(context):
    context.response = post_cart(CART_ENDPOINT, INVALID_CART_BODY)


@when('l\'utente invia un carrello con {count:d} avvisi di pagamento')
def step_post_cart_ko_multiple(context, count: int):
    body = build_multiple_notices_body(count)
    context.response = post_cart(CART_ENDPOINT, body)


# ---------------------------------------------------------------------------
# Then — Assertions
# ---------------------------------------------------------------------------

@then("la risposta ha codice di stato {status_code:d}")
def step_verifica_status_code(context, status_code: int):
    actual = context.response.status_code
    assert actual == status_code, \
        f"Expected status code: {status_code}, received: {actual}.\nBody: {context.response.text}"


@then('la risposta contiene l\'header "{header_name}"')
def step_verifica_header(context, header_name: str):
    headers_lower = {k.lower(): v for k, v in context.response.headers.items()}
    assert header_name.lower() in headers_lower, \
        f'Header "{header_name}" not found. Available headers: {list(context.response.headers.keys())}'
    header_value = headers_lower[header_name.lower()]
    setattr(context, header_name, header_value)


@then('l\'id del carrello viene estratto dall\'header "{header_name}"')
def step_estrai_cart_id(context, header_name: str):
    header_value = getattr(context, header_name, None)
    assert header_value, f'Header "{header_name}" not present in response.'
    context.cart_id = header_value[header_value.rfind("/") + 1:]
    assert context.cart_id, "cart id not extracted from Location header"
    print(f"  → CART_ID extracted: {context.cart_id}")
