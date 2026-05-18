import json
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
    create_transaction_without_order_id,
    delete_transaction,
    extract_session_data,
    fill_npg_card_fields,
    generate_notice_code,
    get_all_payment_methods_v1,
    get_all_payment_methods_v2,
    get_card_data,
    get_card_data_without_token,
    get_payment_method_details,
    get_required_env,
    get_transaction_outcomes_v1,
    get_transaction_v1,
    get_transaction_v2,
    poll_transaction_until_status,
    request_authorization,
    request_authorization_without_token,
    resolve_credit_card_payment_method_id,
    verify_payment,
)


# ---------------------------------------------------------------------------
# Environment / Background steps
# ---------------------------------------------------------------------------

@given("that checkout host is configured through environment variable")
def step_checkout_host_configured(context):
    from checkout_helpers import get_checkout_host
    host = get_checkout_host()
    print(f"  -> CHECKOUT_HOST: {host}")


@given("the checkout NPG environment variables are configured")
def step_npg_env_configured(context):
    required = [
        "NOTICE_CODE_PREFIX",
        "VALID_FISCAL_CODE_PA",
        "UNKNOWN_FISCAL_CODE_PA",
        "UNKNOWN_NOTICE_CODE",
        "UNKNOWN_STAZIONE_FISCAL_CODE_PA",
        "UNKNOWN_STAZIONE_NOTICE_CODE",
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
# Setup (Given) steps
# ---------------------------------------------------------------------------

@given("a random valid notice code is generated")
def step_generate_notice_code(context):
    context.notice_code = generate_notice_code()
    print(f"  -> VALID_NOTICE_CODE: {context.notice_code}")


@given("the credit card payment method id is resolved")
def step_resolve_payment_method_id(context):
    context.payment_method_id = resolve_credit_card_payment_method_id()
    print(f"  -> PAYMENT_METHOD_ID: {context.payment_method_id}")


@given("an NPG session is created")
def step_create_npg_session(context):
    response = create_session(context.payment_method_id, language="it")
    response.raise_for_status()
    session_data = extract_session_data(response.json())
    _save_session_data(context, session_data)
    print(f"  -> ORDER_ID: {context.order_id}")


@given('an NPG session is created with language "{lang}"')
def step_create_npg_session_with_lang(context, lang):
    response = create_session(context.payment_method_id, language=lang)
    response.raise_for_status()
    session_data = extract_session_data(response.json())
    _save_session_data(context, session_data)
    print(f"  -> ORDER_ID: {context.order_id} (lang: {lang})")


@given("a transaction is created for the current session")
def step_create_transaction(context):
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


@given("the NPG card fields are filled with test card data")
def step_fill_npg_card_fields(context):
    response = fill_npg_card_fields(context.npg_correlation_id, context.npg_session_id)
    print(f"  -> NPG fill card fields status: {response.status_code}")


@given("the full NPG authorization flow is executed")
def step_full_npg_auth_flow(context):
    """Esegue il flusso completo: session → transaction → fill card → authorization → polling."""
    context.payment_method_id = resolve_credit_card_payment_method_id()
    response = create_session(context.payment_method_id, language="it")
    response.raise_for_status()
    session_data = extract_session_data(response.json())
    _save_session_data(context, session_data)

    context.notice_code = generate_notice_code()
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    tx_response = create_transaction(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        order_id=context.order_id,
        correlation_id=context.correlation_id,
    )
    tx_response.raise_for_status()
    _save_transaction_data(context, tx_response.json())

    fill_npg_card_fields(context.npg_correlation_id, context.npg_session_id)

    auth_response = request_authorization(
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        amount=context.amount,
        lang="it",
    )
    auth_response.raise_for_status()

    poll_transaction_until_status(
        context.transaction_id, context.auth_token, "AUTHORIZATION_REQUESTED"
    )
    print(f"  -> Full NPG auth flow complete. TRANSACTION_ID: {context.transaction_id}")


# ---------------------------------------------------------------------------
# Action (When) steps — Payment Verify
# ---------------------------------------------------------------------------

@when("the user verifies the payment for the valid notice code")
def step_verify_valid_payment(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = verify_payment(fiscal_code, context.notice_code)


@when("the user verifies the payment for the unknown domain notice code")
def step_verify_unknown_domain(context):
    fiscal_code = get_required_env("UNKNOWN_FISCAL_CODE_PA")
    notice_code = get_required_env("UNKNOWN_NOTICE_CODE")
    context.response = verify_payment(fiscal_code, notice_code)


@when("the user verifies the payment for the unknown station notice code")
def step_verify_unknown_station(context):
    fiscal_code = get_required_env("UNKNOWN_STAZIONE_FISCAL_CODE_PA")
    notice_code = get_required_env("UNKNOWN_STAZIONE_NOTICE_CODE")
    context.response = verify_payment(fiscal_code, notice_code)


@when("the user verifies the cached payment")
def step_verify_cached_payment(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = verify_payment(fiscal_code, context.notice_code)


# ---------------------------------------------------------------------------
# Action (When) steps — Payment Methods
# ---------------------------------------------------------------------------

@when("the user retrieves all payment methods v1")
def step_get_payment_methods_v1(context):
    context.response = get_all_payment_methods_v1()


@when("the user retrieves all payment methods v2")
def step_post_payment_methods_v2(context):
    context.response = get_all_payment_methods_v2()


@when("the user retrieves the credit card payment method details")
def step_get_payment_method_details(context):
    context.response = get_payment_method_details(context.payment_method_id)


@when("the user computes the fee for credit card payment")
def step_compute_fee(context):
    context.response = compute_fee(
        method_id=context.payment_method_id,
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
    )


# ---------------------------------------------------------------------------
# Action (When) steps — Sessions
# ---------------------------------------------------------------------------

@when('the user creates an NPG card session with language "{lang}"')
def step_create_session_with_lang(context, lang):
    context.response = create_session(context.payment_method_id, language=lang)
    if context.response.status_code == 200:
        session_data = extract_session_data(context.response.json())
        _save_session_data(context, session_data)


# ---------------------------------------------------------------------------
# Action (When) steps — Transactions
# ---------------------------------------------------------------------------

@when("the user creates a transaction without order id")
def step_create_transaction_without_order_id(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = create_transaction_without_order_id(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        correlation_id="",
    )


@when("the user creates a transaction with mixed case email")
def step_create_transaction_mixed_case_email(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = create_transaction(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        order_id=context.order_id,
        correlation_id=context.correlation_id,
        email="TEST@test.IT",
    )
    if context.response.status_code == 200:
        _save_transaction_data(context, context.response.json())


@when("the user creates a transaction with standard email")
def step_create_transaction_standard_email(context):
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    context.response = create_transaction(
        fiscal_code=fiscal_code,
        notice_code=context.notice_code,
        order_id=context.order_id,
        correlation_id=context.correlation_id,
        email="mario.rossi@example.com",
    )
    if context.response.status_code == 200:
        _save_transaction_data(context, context.response.json())


@when("the user deletes the transaction")
def step_delete_transaction(context):
    context.response = delete_transaction(context.transaction_id, context.auth_token)


@when("the user retrieves the transaction by id v1")
def step_get_transaction_v1(context):
    context.response = get_transaction_v1(context.transaction_id, context.auth_token)


@when("the user retrieves the transaction by id v2")
def step_get_transaction_v2(context):
    context.response = get_transaction_v2(context.transaction_id, context.auth_token)


@when("the user retrieves the transaction outcomes v1")
def step_get_transaction_outcomes(context):
    context.response = get_transaction_outcomes_v1(context.transaction_id, context.auth_token)


# ---------------------------------------------------------------------------
# Action (When) steps — Card Data
# ---------------------------------------------------------------------------

@when("the user retrieves the card data for the current session")
def step_get_card_data(context):
    context.response = get_card_data(
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
    )


@when("the user retrieves the card data with a wrong order id")
def step_get_card_data_wrong_order_id(context):
    context.response = get_card_data(
        payment_method_id=context.payment_method_id,
        order_id=context.order_id + "1",
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
    )


@when("the user retrieves the card data with a wrong transaction id")
def step_get_card_data_wrong_transaction_id(context):
    context.response = get_card_data(
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        transaction_id=context.transaction_id + "1",
        auth_token=context.auth_token,
    )


@when("the user retrieves the card data without auth token")
def step_get_card_data_no_token(context):
    context.response = get_card_data_without_token(
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        transaction_id=context.transaction_id,
    )


# ---------------------------------------------------------------------------
# Action (When) steps — Authorization
# ---------------------------------------------------------------------------

@when('the user requests authorization without JWT token using language "{lang}"')
def step_request_auth_no_token(context, lang):
    context.response = request_authorization_without_token(
        transaction_id=context.transaction_id,
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        amount=context.amount,
        lang=lang,
    )


@when('the user requests authorization with JWT token using language "{lang}"')
def step_request_auth_with_token(context, lang):
    context.response = request_authorization(
        transaction_id=context.transaction_id,
        auth_token=context.auth_token,
        payment_method_id=context.payment_method_id,
        order_id=context.order_id,
        amount=context.amount,
        lang=lang,
    )


# ---------------------------------------------------------------------------
# Assertion (Then) steps — HTTP status
# ---------------------------------------------------------------------------

@then("the response has status code {expected_code:d}")
def step_check_status_code(context, expected_code):
    actual = context.response.status_code
    assert actual == expected_code, (
        f"Expected HTTP {expected_code}, got {actual}. "
        f"Body: {context.response.text[:500]}"
    )


# ---------------------------------------------------------------------------
# Assertion (Then) steps — Payment Verify
# ---------------------------------------------------------------------------

@then("the payment verification response contains valid payment data")
def step_payment_verify_positive(context):
    body = context.response.json()
    fiscal_code = get_required_env("VALID_FISCAL_CODE_PA")
    assert body.get("paFiscalCode") == fiscal_code, (
        f"paFiscalCode mismatch: {body.get('paFiscalCode')!r} != {fiscal_code!r}"
    )
    assert isinstance(body.get("amount"), (int, float)) and body.get("amount") > 0, (
        f"amount non valido: {body.get('amount')}"
    )
    assert isinstance(body.get("rptId"), str) and body.get("rptId"), (
        "rptId mancante o non stringa"
    )
    assert isinstance(body.get("description"), str), "description mancante"
    assert isinstance(body.get("paName"), str), "paName mancante"
    print(f"  -> Payment verified: amount={body['amount']}, rptId={body['rptId']}")


@then('the fault code detail contains "{expected_detail}"')
def step_fault_code_contains(context, expected_detail):
    body = context.response.json()
    fault_code = body.get("faultCodeDetail", "")
    assert expected_detail in fault_code, (
        f"Expected {expected_detail!r} in faultCodeDetail, got: {fault_code!r}"
    )


@then('the fault code detail equals "{expected_detail}"')
def step_fault_code_equals(context, expected_detail):
    body = context.response.json()
    fault_code = body.get("faultCodeDetail", "")
    assert fault_code == expected_detail, (
        f"Expected faultCodeDetail={expected_detail!r}, got: {fault_code!r}"
    )


@then("the cached payment verification returns valid payment data")
def step_cached_payment_verify(context):
    step_payment_verify_positive(context)


# ---------------------------------------------------------------------------
# Assertion (Then) steps — Payment Methods
# ---------------------------------------------------------------------------

EXPECTED_PAYMENT_METHOD_KEYS_V1 = {
    "asset", "description", "id", "name", "paymentTypeCode", "ranges", "status", "methodManagement"
}

EXPECTED_PAYMENT_METHOD_KEYS_V2 = {
    "id", "name", "description", "status", "validityDateFrom", "paymentTypeCode",
    "paymentMethodTypes", "paymentMethodAsset", "methodManagement", "feeRange",
    "paymentMethodsBrandAssets", "metadata",
}

_BRAND_ASSET_URL_VISA = "https://assets.cdn.platform.pagopa.it/creditcard/visa.png"
_BRAND_ASSET_URL_MC = "https://assets.cdn.platform.pagopa.it/creditcard/mastercard.png"


@then("the payment methods v1 response contains expected fields and brand assets")
def step_payment_methods_v1_fields(context):
    body = context.response.json()
    methods = body.get("paymentMethods", [])
    assert methods, "paymentMethods vuoto o assente"

    for method in methods:
        method_without_brand = {k: v for k, v in method.items() if k != "brandAssets"}
        for key in method_without_brand:
            assert key in EXPECTED_PAYMENT_METHOD_KEYS_V1, (
                f"Campo inatteso nel metodo v1: {key!r}"
            )

    cp_methods = [m for m in methods if m.get("paymentTypeCode") == "CP"]
    for cp in cp_methods:
        brand_assets = cp.get("brandAssets", {})
        assert brand_assets.get("VISA") == _BRAND_ASSET_URL_VISA, (
            f"VISA asset mismatch: {brand_assets.get('VISA')!r}"
        )
        assert brand_assets.get("MC") == _BRAND_ASSET_URL_MC, (
            f"MC asset mismatch: {brand_assets.get('MC')!r}"
        )
        assert brand_assets.get("MASTERCARD") == _BRAND_ASSET_URL_MC, (
            f"MASTERCARD asset mismatch: {brand_assets.get('MASTERCARD')!r}"
        )
    print(f"  -> Payment methods v1: {len(methods)} methods found")


@then("the payment methods v2 response contains expected fields")
def step_payment_methods_v2_fields(context):
    body = context.response.json()
    methods = body.get("paymentMethods", [])
    assert methods, "paymentMethods vuoto o assente"

    for method in methods:
        method_without_brand = {k: v for k, v in method.items() if k != "paymentMethodsBrandAssets"}
        for key in method_without_brand:
            assert key in EXPECTED_PAYMENT_METHOD_KEYS_V2, (
                f"Campo inatteso nel metodo v2: {key!r}"
            )

    cp_methods = [m for m in methods if m.get("paymentTypeCode") == "CP"]
    for cp in cp_methods:
        brand_assets = cp.get("paymentMethodsBrandAssets", {})
        assert brand_assets.get("VISA") == _BRAND_ASSET_URL_VISA, (
            f"VISA asset mismatch: {brand_assets.get('VISA')!r}"
        )
        assert brand_assets.get("MASTERCARD") == _BRAND_ASSET_URL_MC, (
            f"MASTERCARD asset mismatch: {brand_assets.get('MASTERCARD')!r}"
        )
    print(f"  -> Payment methods v2: {len(methods)} methods found")


@then("the payment method is CARDS with paymentTypeCode CP")
def step_payment_method_is_cards(context):
    body = context.response.json()
    assert body.get("name") == "CARDS", (
        f"Atteso name='CARDS', ricevuto: {body.get('name')!r}"
    )
    assert body.get("paymentTypeCode") == "CP", (
        f"Atteso paymentTypeCode='CP', ricevuto: {body.get('paymentTypeCode')!r}"
    )
    assert body.get("id") == context.payment_method_id, (
        f"id mismatch: {body.get('id')!r} != {context.payment_method_id!r}"
    )
    assert body.get("asset"), "asset assente o vuoto"
    assert body.get("ranges"), "ranges assente o vuoto"

    context.payment_method_description = body.get("description", "")
    context.payment_method_name = body.get("name", "")
    print(f"  -> Payment method: {body['name']} ({body['paymentTypeCode']})")


@then("the fee response contains an enabled method with bundles")
def step_fee_response(context):
    body = context.response.json()
    assert body.get("paymentMethodStatus") == "ENABLED", (
        f"paymentMethodStatus atteso ENABLED, ricevuto: {body.get('paymentMethodStatus')!r}"
    )
    assert body.get("belowThreshold") is False, (
        f"belowThreshold atteso False, ricevuto: {body.get('belowThreshold')!r}"
    )
    assert body.get("bundles"), "bundles assente o vuoto"
    print(f"  -> Fee response: {len(body.get('bundles', []))} bundles")


# ---------------------------------------------------------------------------
# Assertion (Then) steps — Sessions
# ---------------------------------------------------------------------------

_EXPECTED_FORM_FIELDS = [
    {"type": "TEXT", "class": "CARD_FIELD", "id": "CARD_NUMBER"},
    {"type": "TEXT", "class": "CARD_FIELD", "id": "EXPIRATION_DATE"},
    {"type": "TEXT", "class": "CARD_FIELD", "id": "SECURITY_CODE"},
    {"type": "TEXT", "class": "CARD_FIELD", "id": "CARDHOLDER_NAME"},
]


@then("the NPG session response contains valid card form fields with payment method CARDS")
def step_npg_session_form_fields(context):
    body = context.response.json()
    assert isinstance(body.get("orderId"), str) and body.get("orderId"), (
        "orderId mancante nella risposta della sessione"
    )
    payment_method_data = body.get("paymentMethodData", {})
    assert payment_method_data.get("paymentMethod") == "CARDS", (
        f"paymentMethod atteso 'CARDS', ricevuto: {payment_method_data.get('paymentMethod')!r}"
    )
    form = payment_method_data.get("form", [])
    form_without_src = [{"type": f["type"], "class": f["class"], "id": f["id"]} for f in form]
    assert form_without_src == _EXPECTED_FORM_FIELDS, (
        f"Campi form NPG non attesi:\nRicevuto: {json.dumps(form_without_src, indent=2)}\n"
        f"Atteso:   {json.dumps(_EXPECTED_FORM_FIELDS, indent=2)}"
    )
    print(f"  -> NPG session orderId: {body['orderId']}")


# ---------------------------------------------------------------------------
# Assertion (Then) steps — Transactions
# ---------------------------------------------------------------------------

_EXPECTED_PAYMENT_TOKEN_KEYS = {"rptId", "reason", "amount", "isAllCCP"}
_EXPECTED_TRANSFER_LIST_KEYS = {"paFiscalCode", "digitalStamp", "transferAmount", "transferCategory"}


@then("the transaction response is in ACTIVATED status for checkout client")
def step_transaction_activated(context):
    body = context.response.json()
    assert body.get("status") == "ACTIVATED", (
        f"status atteso 'ACTIVATED', ricevuto: {body.get('status')!r}"
    )
    assert body.get("clientId") == "CHECKOUT", (
        f"clientId atteso 'CHECKOUT', ricevuto: {body.get('clientId')!r}"
    )
    assert isinstance(body.get("authToken"), str) and body.get("authToken"), (
        "authToken mancante o non stringa"
    )
    assert isinstance(body.get("transactionId"), str) and body.get("transactionId"), (
        "transactionId mancante o non stringa"
    )
    payments = body.get("payments", [])
    assert len(payments) == 1, f"Atteso 1 payment, ricevuto: {len(payments)}"

    payment = payments[0]
    keys_without_token_and_transfer = {k for k in payment if k not in ("paymentToken", "transferList")}
    for key in keys_without_token_and_transfer:
        assert key in _EXPECTED_PAYMENT_TOKEN_KEYS, (
            f"Campo inatteso nel payment: {key!r}"
        )
    assert isinstance(payment.get("amount"), (int, float)), "payment.amount non numerico"
    assert isinstance(payment.get("isAllCCP"), bool), "payment.isAllCCP non booleano"
    assert isinstance(payment.get("paymentToken"), str), "paymentToken non stringa"

    transfer_list = payment.get("transferList", [])
    for item in transfer_list:
        for key in item:
            assert key in _EXPECTED_TRANSFER_LIST_KEYS, (
                f"Campo inatteso in transferList: {key!r}"
            )
        assert isinstance(item.get("paFiscalCode"), str), "transferList.paFiscalCode non stringa"
        assert isinstance(item.get("digitalStamp"), bool), "transferList.digitalStamp non booleano"
        assert isinstance(item.get("transferAmount"), (int, float)), "transferList.transferAmount non numerico"

    print(f"  -> Transaction ACTIVATED: id={body['transactionId']}")


@then("the transaction v1 status is AUTHORIZATION_REQUESTED")
def step_transaction_v1_status(context):
    body = context.response.json()
    assert body.get("status") == "AUTHORIZATION_REQUESTED", (
        f"status atteso 'AUTHORIZATION_REQUESTED', ricevuto: {body.get('status')!r}"
    )
    assert body.get("clientId") == "CHECKOUT", (
        f"clientId atteso 'CHECKOUT', ricevuto: {body.get('clientId')!r}"
    )
    assert len(body.get("payments", [])) == 1, "Atteso 1 payment"


@then("the transaction v1 gateway is NPG")
def step_transaction_v1_gateway(context):
    body = context.response.json()
    assert body.get("gateway") == "NPG", (
        f"gateway atteso 'NPG', ricevuto: {body.get('gateway')!r}"
    )


@then("the outcomes response contains a valid outcome code")
def step_outcomes_valid(context):
    valid_outcomes = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 25, 99, 116, 117, 121}
    body = context.response.json()
    outcome = body.get("outcome")
    assert isinstance(outcome, int) and outcome in valid_outcomes, (
        f"outcome non valido: {outcome!r}. Attesi: {sorted(valid_outcomes)}"
    )
    assert isinstance(body.get("isFinalStatus"), bool), "isFinalStatus non booleano"
    if body.get("totalAmount") is not None:
        assert isinstance(body["totalAmount"], (int, float)), "totalAmount non numerico"
    if body.get("fees") is not None:
        assert isinstance(body["fees"], (int, float)), "fees non numerico"
    print(f"  -> Transaction outcome: {outcome}, isFinalStatus={body['isFinalStatus']}")


@then("the transaction v2 status is AUTHORIZATION_REQUESTED")
def step_transaction_v2_status(context):
    body = context.response.json()
    assert body.get("status") == "AUTHORIZATION_REQUESTED", (
        f"status atteso 'AUTHORIZATION_REQUESTED', ricevuto: {body.get('status')!r}"
    )
    assert body.get("clientId") == "CHECKOUT", (
        f"clientId atteso 'CHECKOUT', ricevuto: {body.get('clientId')!r}"
    )
    assert len(body.get("payments", [])) == 1, "Atteso 1 payment"


@then("the transaction v2 gatewayInfo is NPG")
def step_transaction_v2_gateway_info(context):
    body = context.response.json()
    gateway_info = body.get("gatewayInfo", {})
    assert gateway_info.get("gateway") == "NPG", (
        f"gatewayInfo.gateway atteso 'NPG', ricevuto: {gateway_info.get('gateway')!r}"
    )


# ---------------------------------------------------------------------------
# Assertion (Then) steps — Card Data
# ---------------------------------------------------------------------------

@then("the card data matches the test card values")
def step_card_data_matches(context):
    body = context.response.json()
    card_pan = get_required_env("NPG_TEST_CARD_PAN")
    expected_bin = card_pan[:8]
    expected_last_four = card_pan[-4:]
    expected_expiry = get_required_env("NPG_TEST_EXPIRATION_DATE")
    expected_brand = get_required_env("NPG_TEST_CARD_BRAND")

    npg_session_id = context.npg_session_id
    encoded_session_id = (
        npg_session_id.replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")
    )

    assert body.get("sessionId") == encoded_session_id, (
        f"sessionId mismatch: {body.get('sessionId')!r} != {encoded_session_id!r}"
    )
    assert body.get("bin") == expected_bin, (
        f"bin atteso {expected_bin!r}, ricevuto: {body.get('bin')!r}"
    )
    assert body.get("lastFourDigits") == expected_last_four, (
        f"lastFourDigits atteso {expected_last_four!r}, ricevuto: {body.get('lastFourDigits')!r}"
    )
    assert body.get("expiringDate") == expected_expiry, (
        f"expiringDate atteso {expected_expiry!r}, ricevuto: {body.get('expiringDate')!r}"
    )
    assert body.get("brand") == expected_brand, (
        f"brand atteso {expected_brand!r}, ricevuto: {body.get('brand')!r}"
    )
    print(f"  -> Card data verified: bin={expected_bin}, brand={expected_brand}")


# ---------------------------------------------------------------------------
# Assertion (Then) steps — Authorization
# ---------------------------------------------------------------------------

@then("the authorization response contains a valid authorization URL")
def step_auth_response_url(context):
    body = context.response.json()
    auth_url = body.get("authorizationUrl")
    assert isinstance(auth_url, str) and auth_url, (
        f"authorizationUrl mancante o non stringa: {body!r}"
    )
    print(f"  -> Authorization URL: {auth_url[:80]}...")


@then("the authorization request id matches the order id")
def step_auth_request_id_matches_order(context):
    body = context.response.json()
    auth_request_id = body.get("authorizationRequestId")
    assert auth_request_id == context.order_id, (
        f"authorizationRequestId {auth_request_id!r} != order_id {context.order_id!r}"
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _save_session_data(context, session_data: dict) -> None:
    context.order_id = session_data["order_id"]
    context.correlation_id = session_data["correlation_id"]
    context.npg_correlation_id = session_data["npg_correlation_id"]
    context.npg_session_id = session_data["npg_session_id"]
    context.npg_field_id = session_data["npg_field_id"]


def _save_transaction_data(context, body: dict) -> None:
    context.transaction_id = body["transactionId"]
    context.auth_token = body["authToken"]
    context.amount = sum(p["amount"] for p in body.get("payments", []))
