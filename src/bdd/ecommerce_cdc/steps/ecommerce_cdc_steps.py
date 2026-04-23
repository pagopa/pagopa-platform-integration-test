"""
Step definitions per i test eCommerce CDC.

I test verificano l'integrazione del servizio eCommerce CDC eseguendo il flusso
completo di pagamento attraverso le API Checkout e validando la propagazione
degli stati della transazione tramite polling (pattern CDC).

Migrati dalla Postman collection "eCommerce CDC service".
"""
import sys
from pathlib import Path

from behave import given, then, when

HELPERS_DIR = Path(__file__).resolve().parents[3] / "utility" / "api_test" / "checkout"
if str(HELPERS_DIR) not in sys.path:
    sys.path.insert(0, str(HELPERS_DIR))

from checkout_helpers import (  # noqa: E402
    compute_fee,
    create_session,
    create_transaction,
    delete_transaction,
    extract_session_data,
    fill_npg_card_fields,
    generate_notice_code,
    get_all_payment_methods_v1,
    get_card_data,
    get_payment_method_details,
    get_required_env,
    poll_transaction_until_status,
    populate_npg_cookies,
    request_authorization,
    resolve_credit_card_payment_method_id,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _save_session_data(context, session_data: dict) -> None:
    context.order_id = session_data["order_id"]
    context.correlation_id = session_data["correlation_id"]
    context.field_url = session_data["field_url"]
    context.npg_correlation_id = session_data["npg_correlation_id"]
    context.npg_session_id = session_data["npg_session_id"]
    context.npg_field_id = session_data["npg_field_id"]


def _save_transaction_data(context, body: dict) -> None:
    context.transaction_id = body["transactionId"]
    context.auth_token = body["authToken"]
    context.amount = sum(p["amount"] for p in body.get("payments", []))


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------

@given("the eCommerce CDC environment variables are configured")
def step_cdc_env_configured(context):
    required = [
        "CHECKOUT_HOST",
        "NPG_HOST",
        "NOTICE_CODE_PREFIX",
        "VALID_FISCAL_CODE_PA",
        "PSP_ID",
        "NPG_TEST_CARD_PAN",
        "NPG_TEST_EXPIRATION_DATE",
        "NPG_TEST_SECURITY_CODE",
        "NPG_TEST_CARDHOLDER_NAME",
        "NPG_TEST_CARD_BRAND",
    ]
    for name in required:
        value = get_required_env(name)
        print(f"  -> {name}: {value}")


# ---------------------------------------------------------------------------
# Given — Setup steps
# ---------------------------------------------------------------------------

@given("the CDC credit card payment method id is resolved")
def step_cdc_resolve_payment_method_id(context):
    context.payment_method_id = resolve_credit_card_payment_method_id()
    print(f"  -> PAYMENT_METHOD_ID: {context.payment_method_id}")


@given("a random CDC notice code is generated")
def step_cdc_generate_notice_code(context):
    context.notice_code = generate_notice_code()
    print(f"  -> NOTICE_CODE: {context.notice_code}")


@given("a CDC NPG session is prepared")
def step_cdc_prepare_npg_session(context):
    response = create_session(context.payment_method_id, language="it")
    response.raise_for_status()
    session_data = extract_session_data(response.json())
    _save_session_data(context, session_data)
    print(f"  -> ORDER_ID: {context.order_id}")


@given("the NPG cookies are populated")
def step_cdc_populate_npg_cookies(context):
    response = populate_npg_cookies(
        context.npg_correlation_id,
        context.npg_session_id,
        context.npg_field_id,
    )
    print(f"  -> NPG cookies populated: HTTP {response.status_code}")


@given("a CDC transaction is created for the current session")
def step_cdc_create_transaction_given(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    response = create_transaction(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        order_id=context.order_id,
        correlation_id=context.correlation_id,
    )
    response.raise_for_status()
    _save_transaction_data(context, response.json())
    print(f"  -> TRANSACTION_ID: {context.transaction_id}")


@given('the transaction status reaches "{wanted_status}" via polling')
def step_cdc_poll_transaction_given(context, wanted_status: str):
    reached = poll_transaction_until_status(
        context.transaction_id, context.auth_token, wanted_status
    )
    print(f"  -> Transaction reached status: {reached}")


@given("the card data matches the test card values after filling NPG fields")
def step_cdc_fill_and_validate_card(context):
    fill_response = fill_npg_card_fields(context.npg_correlation_id, context.npg_session_id)
    print(f"  -> NPG card fields filled: HTTP {fill_response.status_code}")

    card_response = get_card_data(
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
    )
    card_response.raise_for_status()
    body = card_response.json()

    card_pan = get_required_env("NPG_TEST_CARD_PAN")
    session_id = context.npg_session_id.replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")
    expected_bin = card_pan[:8]
    expected_last_four = card_pan[-4:]

    assert body.get("sessionId") == session_id, (
        f"sessionId mismatch: {body.get('sessionId')!r} != {session_id!r}"
    )
    assert body.get("bin") == expected_bin, (
        f"bin mismatch: {body.get('bin')!r} != {expected_bin!r}"
    )
    assert body.get("lastFourDigits") == expected_last_four, (
        f"lastFourDigits mismatch: {body.get('lastFourDigits')!r} != {expected_last_four!r}"
    )
    assert body.get("expiringDate") == get_required_env("NPG_TEST_EXPIRATION_DATE"), (
        f"expiringDate mismatch: {body.get('expiringDate')!r}"
    )
    assert body.get("brand") == get_required_env("NPG_TEST_CARD_BRAND"), (
        f"brand mismatch: {body.get('brand')!r}"
    )
    print(f"  -> Card data validated: bin={expected_bin}, lastFour={expected_last_four}")


# ---------------------------------------------------------------------------
# When — Action steps
# ---------------------------------------------------------------------------

@when("I create a CDC transaction with a static order id")
def step_cdc_create_static_order_transaction(context):
    """
    Replica il prerequest del test 'Delete transaction' nella collection Postman:
    crea una transazione con orderId letterale 'orderId' e correlation-id statico.
    """
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = create_transaction(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        order_id="orderId",
        correlation_id="b6bb9f02-a20d-409b-8699-8603b83cd950",
    )
    if context.response.status_code == 200:
        _save_transaction_data(context, context.response.json())
    print(f"  -> Create transaction for delete: HTTP {context.response.status_code}")


@when("I delete the CDC transaction")
def step_cdc_delete_transaction(context):
    context.response = delete_transaction(context.transaction_id, context.auth_token)


@when("I create a CDC NPG card session")
def step_cdc_create_session(context):
    context.response = create_session(context.payment_method_id, language="it")
    if context.response.status_code == 200:
        session_data = extract_session_data(context.response.json())
        _save_session_data(context, session_data)


@when("I create a CDC transaction for the current session")
def step_cdc_create_transaction_when(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = create_transaction(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        order_id=context.order_id,
        correlation_id=context.correlation_id,
    )
    if context.response.status_code == 200:
        _save_transaction_data(context, context.response.json())


@when("I get the CDC payment method details")
def step_cdc_get_payment_method_details(context):
    context.response = get_payment_method_details(context.payment_method_id)


@when("I compute the CDC fee for credit card payment")
def step_cdc_compute_fee(context):
    context.response = compute_fee(
        method_id=context.payment_method_id,
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
    )


@when("I get all CDC payment methods v1")
def step_cdc_get_all_payment_methods(context):
    context.response = get_all_payment_methods_v1()


@when("I request CDC authorization for the transaction")
def step_cdc_request_authorization(context):
    context.response = request_authorization(
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        amount=context.amount,
        lang="it",
    )


# ---------------------------------------------------------------------------
# Then — Assertion steps — Generic
# ---------------------------------------------------------------------------

@then("the CDC response has status code {expected_code:d}")
def step_cdc_check_status_code(context, expected_code: int):
    actual = context.response.status_code
    assert actual == expected_code, (
        f"Expected HTTP {expected_code}, got {actual}. "
        f"Body: {context.response.text[:500]}"
    )


@then('the transaction status reaches "{wanted_status}" via polling')
def step_cdc_poll_transaction_then(context, wanted_status: str):
    reached = poll_transaction_until_status(
        context.transaction_id, context.auth_token, wanted_status
    )
    assert reached == wanted_status, (
        f"Polling: stato atteso {wanted_status!r}, raggiunto {reached!r}"
    )
    print(f"  -> Transaction reached status: {reached}")


# ---------------------------------------------------------------------------
# Then — Session assertions
# ---------------------------------------------------------------------------

_EXPECTED_CARD_FORM_FIELDS = {"CARD_NUMBER", "EXPIRATION_DATE", "SECURITY_CODE", "CARDHOLDER_NAME"}


@then("the NPG session contains four card form fields")
def step_cdc_session_form_fields(context):
    body = context.response.json()
    form = body.get("paymentMethodData", {}).get("form", [])
    assert len(form) == 4, f"Attesi 4 campi form, trovati {len(form)}: {form}"
    field_ids = {f["id"] for f in form}
    assert field_ids == _EXPECTED_CARD_FORM_FIELDS, (
        f"Campi form inattesi: {field_ids} != {_EXPECTED_CARD_FORM_FIELDS}"
    )
    for field in form:
        assert field.get("type") == "TEXT", f"Campo con type inatteso: {field}"
        assert field.get("class") == "CARD_FIELD", f"Campo con class inatteso: {field}"
    print(f"  -> Form fields validated: {field_ids}")


@then("the NPG session has payment method CARDS")
def step_cdc_session_payment_method(context):
    body = context.response.json()
    actual = body.get("paymentMethodData", {}).get("paymentMethod")
    assert actual == "CARDS", f"paymentMethod atteso 'CARDS', trovato {actual!r}"


@then("the NPG session has a valid order id")
def step_cdc_session_order_id(context):
    body = context.response.json()
    order_id = body.get("orderId")
    assert isinstance(order_id, str) and order_id, (
        f"orderId non valido nella risposta: {order_id!r}"
    )
    print(f"  -> orderId: {order_id}")


# ---------------------------------------------------------------------------
# Then — Transaction creation assertions
# ---------------------------------------------------------------------------

_EXPECTED_PAYMENT_KEYS = {"rptId", "reason", "amount", "isAllCCP", "paymentToken"}
_EXPECTED_TRANSFER_LIST_KEYS = {"paFiscalCode", "digitalStamp", "transferAmount", "transferCategory"}


@then("the transaction response has status ACTIVATED")
def step_cdc_transaction_status_activated(context):
    body = context.response.json()
    assert body.get("status") == "ACTIVATED", (
        f"status atteso 'ACTIVATED', trovato {body.get('status')!r}"
    )


@then("the transaction response has a valid transactionId and authToken")
def step_cdc_transaction_ids(context):
    body = context.response.json()
    assert isinstance(body.get("transactionId"), str) and body["transactionId"], (
        "transactionId mancante o non stringa"
    )
    assert isinstance(body.get("authToken"), str) and body["authToken"], (
        "authToken mancante o non stringa"
    )
    print(f"  -> transactionId: {body['transactionId']}")


@then("the transaction payments have the expected structure")
def step_cdc_transaction_payments_structure(context):
    body = context.response.json()
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    expected_reason = get_required_env("EXPECTED_PAYMENT_REASON")

    assert body.get("clientId") == "CHECKOUT", (
        f"clientId atteso 'CHECKOUT', trovato {body.get('clientId')!r}"
    )

    payments = body.get("payments", [])
    assert len(payments) == 1, f"Atteso 1 payment, trovati {len(payments)}"

    payment = payments[0]
    rpt_id = payment.get("rptId", "")
    assert rpt_id.startswith(fiscal_code), (
        f"rptId {rpt_id!r} non inizia con {fiscal_code!r}"
    )
    assert payment.get("reason") == expected_reason, (
        f"reason atteso {expected_reason!r}, trovato {payment.get('reason')!r}"
    )
    assert isinstance(payment.get("amount"), (int, float)), "amount non numerico"
    assert isinstance(payment.get("isAllCCP"), bool), "isAllCCP non booleano"
    assert isinstance(payment.get("paymentToken"), str), "paymentToken non stringa"

    transfer_list = payment.get("transferList", [])
    assert transfer_list, "transferList vuota o assente"
    for transfer in transfer_list:
        for key in transfer:
            assert key in _EXPECTED_TRANSFER_LIST_KEYS, (
                f"Campo inatteso in transferList: {key!r}"
            )


# ---------------------------------------------------------------------------
# Then — Payment method detail assertions
# ---------------------------------------------------------------------------

@then('the payment method has name "{expected_name}" and paymentTypeCode "{expected_type_code}"')
def step_cdc_payment_method_name_type(context, expected_name: str, expected_type_code: str):
    body = context.response.json()
    assert body.get("name") == expected_name, (
        f"name atteso {expected_name!r}, trovato {body.get('name')!r}"
    )
    assert body.get("paymentTypeCode") == expected_type_code, (
        f"paymentTypeCode atteso {expected_type_code!r}, trovato {body.get('paymentTypeCode')!r}"
    )
    context.payment_method_name = body.get("name")
    context.payment_method_description = body.get("description")


@then("the payment method has a non-empty asset and ranges")
def step_cdc_payment_method_asset_ranges(context):
    body = context.response.json()
    assert body.get("asset"), "asset vuoto o assente"
    assert body.get("ranges"), "ranges vuoto o assente"


# ---------------------------------------------------------------------------
# Then — Fee assertions
# ---------------------------------------------------------------------------

@then('the fee response has paymentMethodStatus "{expected_status}"')
def step_cdc_fee_payment_method_status(context, expected_status: str):
    body = context.response.json()
    actual = body.get("paymentMethodStatus")
    assert actual == expected_status, (
        f"paymentMethodStatus atteso {expected_status!r}, trovato {actual!r}"
    )


@then("the fee response has belowThreshold false")
def step_cdc_fee_below_threshold(context):
    body = context.response.json()
    assert body.get("belowThreshold") is False, (
        f"belowThreshold atteso False, trovato {body.get('belowThreshold')!r}"
    )


@then("the fee response has non-empty bundles")
def step_cdc_fee_bundles(context):
    body = context.response.json()
    assert body.get("bundles"), "bundles vuoto o assente"


# ---------------------------------------------------------------------------
# Then — All payment methods assertions
# ---------------------------------------------------------------------------

_BRAND_ASSET_VISA = "https://assets.cdn.platform.pagopa.it/creditcard/visa.png"
_BRAND_ASSET_MC = "https://assets.cdn.platform.pagopa.it/creditcard/mastercard.png"

_EXPECTED_METHOD_KEYS = {
    "asset", "description", "id", "name", "paymentTypeCode",
    "ranges", "status", "methodManagement",
}


@then("the payment methods list is not empty")
def step_cdc_payment_methods_not_empty(context):
    body = context.response.json()
    methods = body.get("paymentMethods") or body
    assert methods, "paymentMethods vuota o assente"
    print(f"  -> {len(methods)} payment method(s) found")


@then("the credit card methods have VISA and Mastercard brand assets")
def step_cdc_brand_assets(context):
    body = context.response.json()
    methods = body.get("paymentMethods", [])
    cp_methods = [m for m in methods if m.get("paymentTypeCode") == "CP"]
    assert cp_methods, "Nessun metodo CP trovato in paymentMethods"

    for method in cp_methods:
        brand_assets = method.get("brandAssets", {})
        assert brand_assets.get("VISA") == _BRAND_ASSET_VISA, (
            f"VISA brand asset non valido: {brand_assets.get('VISA')!r}"
        )
        assert brand_assets.get("MC") == _BRAND_ASSET_MC, (
            f"MC brand asset non valido: {brand_assets.get('MC')!r}"
        )
        assert brand_assets.get("MASTERCARD") == _BRAND_ASSET_MC, (
            f"MASTERCARD brand asset non valido: {brand_assets.get('MASTERCARD')!r}"
        )
    print(f"  -> Brand assets validated for {len(cp_methods)} CP method(s)")


# ---------------------------------------------------------------------------
# Then — Authorization assertions
# ---------------------------------------------------------------------------

@then("the authorization response has a valid authorizationUrl")
def step_cdc_auth_url(context):
    body = context.response.json()
    url = body.get("authorizationUrl")
    assert isinstance(url, str) and url, (
        f"authorizationUrl non valido o assente: {url!r}"
    )
    print(f"  -> authorizationUrl: {url[:80]}...")


@then("the authorization requestId matches the current order id")
def step_cdc_auth_request_id(context):
    body = context.response.json()
    request_id = body.get("authorizationRequestId")
    assert request_id == context.order_id, (
        f"authorizationRequestId {request_id!r} != orderId {context.order_id!r}"
    )
    print(f"  -> authorizationRequestId matches orderId: {request_id}")
