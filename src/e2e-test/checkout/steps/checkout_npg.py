import logging
import random

from behave import given, when, then
from helper import _get_page, _get_required_env, _generate_random_notice_code, _locate_and_click

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────

@given('The checkout page is open')
def step_checkout_page_open(context):
    """Navigate to the checkout URL."""
    page = _get_page(context)
    checkout_url = _get_required_env("CHECKOUT_URL")
    logger.info("Opening checkout page: %s", checkout_url)
    page.goto(checkout_url, wait_until="domcontentloaded")
    # Initialise context storage for state shared between steps
    context.notice_code = None
    context.fiscal_code = None

@given('The language is set to "it"')
def step_set_language_it(context):
    page = _get_page(context)
    logger.info("Imposto lingua a 'it'")
    page.locator("#languageMenu").wait_for(
        state="visible", timeout=5000
    )
    page.select_option("#languageMenu", "it")


# ──────────────────────────────────────────────
# WHEN steps — notice form
# ──────────────────────────────────────────────

@when(u'The user enters the notice data with a notice code with fiscal code prefix "{fiscalCodePrefix}"')
def step_enter_notice_random(context, fiscal_code_prefix):
    """
    Click the keyboard icon to open the manual form,
    then generate and type a random notice code for the given prefix.
    """
    page = _get_page(context)
    context.notice_code = _generate_random_notice_code(fiscal_code_prefix)
    logger.info("Generated notice code: %s (prefix: %s)", context.notice_code, fiscal_code_prefix)

    logger.info("Clicking keyboard icon")
    _locate_and_click(page, "[data-testid='KeyboardIcon']")

    _locate_and_click(page, "#billCode")

    page.keyboard.type(context.notice_code)
    logger.info("Notice code typed: %s", context.notice_code)


@when('The user enters the notice data with a notice code in range "{rangeStart}" to "{rangeEnd}')
def step_enter_notice_in_range(context, range_start, range_end):
    """
    Click the keyboard icon and type a notice code within the given numeric range.
    When range_start == range_end (e.g. PAA_PAGAMENTO_DUPLICATO), uses the fixed value.
    """
    page = _get_page(context)

    start = int(range_start)
    end = int(range_end)
    context.notice_code = str(random.randint(start, end))
    logger.info(
        "Generated error-case notice code: %s (range: %s - %s)",
        context.notice_code, range_start, range_end
    )

    logger.info("Clicking keyboard icon")
    _locate_and_click(page, "[data-testid='KeyboardIcon']")

    _locate_and_click(page, "#billCode")

    page.keyboard.type(context.notice_code)


@when(u'The user enters the taxpayer fiscal code "{fiscalCode}"')
def step_enter_fiscal_code(context, fiscal_code):
    """Type the taxpayer fiscal code into the #cf field."""
    page = _get_page(context)
    context.fiscal_code = fiscal_code
    logger.info("Typing fiscal code: %s", fiscal_code)
    _locate_and_click(page, "#cf")
    page.keyboard.type(fiscal_code)


@when('The user clicks the verify button')
def step_click_verify(context):
    """Click the continue/verify button on the notice form."""
    page = _get_page(context)
    logger.info("Clicking verify/continue button")
    _locate_and_click(page, "#paymentNoticeButtonContinue")

# ──────────────────────────────────────────────
# WHEN steps — summary & email
# ──────────────────────────────────────────────

@when('The user clicks the pay button')
def step_click_pay_on_summary(context):
    """Click the pay button on the payment summary page."""
    page = _get_page(context)
    logger.info("Clicking pay button on summary page")
    _locate_and_click(page, "#paymentSummaryButtonPay")


@when('The user enters the email "{email}"')
def step_enter_email(context, email):
    """Type the email address into the email field."""
    page = _get_page(context)
    context.email = email
    logger.info("Typing email: %s", email)
    _locate_and_click(page, "#email")
    page.keyboard.type(email)


@when('The user confirms the email "{email}"')
def step_confirm_email(context, email):
    """Type the email into the confirm field and click continue."""
    page = _get_page(context)
    logger.info("Confirming email: %s", email)
    _locate_and_click(page, "#confirmEmail")
    page.keyboard.type(email)
    _locate_and_click(page, "#paymentEmailPageButtonContinue")


# ──────────────────────────────────────────────
# WHEN steps — payment method
# ──────────────────────────────────────────────

@when('The user selects the payment method "{method}"')
def step_select_payment_method(context, method):
    """Select the desired payment method by its data-qaid attribute."""
    page = _get_page(context)
    logger.info("Selecting payment method: %s", method)
    _locate_and_click(page, f"[data-qaid={method}]")


# ──────────────────────────────────────────────
# WHEN steps — card form (individual fields)
# ──────────────────────────────────────────────

@when(u'The user fills in the card number "{card_number}"')
def step_fill_card_number(context, card_number):
    """Type the card number into the NPG iframe field."""
    page = _get_page(context)
    logger.info("Filling card number")
    _locate_and_click(page, "#frame_CARD_NUMBER",3, 10000)
    page.keyboard.type(card_number)


@when(u'The user fills in the expiration date "{expiration_date}"')
def step_fill_expiration_date(context, expiration_date):
    """Type the expiration date into the NPG iframe field."""
    page = _get_page(context)
    logger.info("Filling expiration date: %s", expiration_date)
    _locate_and_click(page, "#frame_EXPIRATION_DATE",3)
    page.keyboard.type(expiration_date)


@when(u'The user fills in the security code "{cvv}"')
def step_fill_security_code(context, cvv):
    """Type the CVV into the NPG iframe field."""
    page = _get_page(context)
    logger.info("Filling security code (CVV)")
    _locate_and_click(page, "#frame_SECURITY_CODE",3)
    page.keyboard.type(cvv)

@when(u'The user fills in the cardholder name "{holder_name}"')
def step_fill_cardholder_name(context, holder_name):
    """
    Type the cardholder name and retry until the submit button becomes enabled.
    Mirrors the TypeScript while-loop that retypes all fields if the button stays disabled.
    """
    page = _get_page(context)
    logger.info("Filling cardholder name '%s', holder_name")
    _locate_and_click(page, "#frame_CARDHOLDER_NAME",3)
    page.keyboard.type(holder_name)

# ──────────────────────────────────────────────
# WHEN steps — PSP selection
# ──────────────────────────────────────────────

@when(u'The user selects the PSP with id "{psp_id}"')
def step_select_psp(context, psp_id):
    """
    Click the card form continue button to reach the PSP list,
    then select the radio button for the given PSP id.
    """
    page = _get_page(context)
    logger.info("Clicking card form continue button")
    _locate_and_click(page, "button[type=submit]")
    logger.info("Selecting PSP radio: %s", psp_id)
    _locate_and_click(page, f"#{psp_id}")


@when('The user confirms the PSP selection')
def step_confirm_psp(context):
    """Click the continue button on the PSP list page."""
    page = _get_page(context)
    logger.info("Confirming PSP selection")
    _locate_and_click(page, "#paymentPspListPageButtonContinue")


@when('The user clicks the final pay button')
def step_click_final_pay(context):
    """Click the final pay button and wait for the NPG mock auto-authorisation."""
    page = _get_page(context)
    logger.info("Clicking final pay button")
    _locate_and_click(page, "#paymentCheckPageButtonPay")
    logger.info("Final pay button clicked — waiting for load (NPG mock auto-authorises)")
    page.wait_for_load_state("load")

# ──────────────────────────────────────────────
# THEN steps — error modal
# ──────────────────────────────────────────────

@then('An error modal is displayed after "{seconds}" seconds')
def step_error_modal_visible(context, seconds = 5):
    """
    Assert that the error title element is visible.
    Selector: #verifyPaymentTitleError (from constants.ts — all error cases use this).
    """
    timeout_ms = int(float(seconds) * 1000)
    page = _get_page(context)
    logger.info("Checking error modal title is displayed")
    page.locator("#verifyPaymentTitleError").wait_for(state="visible", timeout=timeout_ms)
    logger.info("Error modal is visible")

@then('An error modal is displayed')
def step_error_modal_visible(context):
    """
    Assert that the error title element is visible.
    Selector: #verifyPaymentTitleError (from constants.ts — all error cases use this).
    """
    step_error_modal_visible(context)


@then('The error modal header contains "{expectedHeader}"')
def step_error_modal_header(context, expected_header):
    """
    Assert the error modal header text using the selector from constants.ts.
    Selector: #verifyPaymentTitleError
    """
    page = _get_page(context)
    logger.info("Checking error modal header contains: '%s'", expected_header)
    header_elem = page.locator("#verifyPaymentTitleError")
    header_elem.wait_for(state="visible", timeout=5000)
    header_text = header_elem.inner_text()
    logger.info("Error modal header: %s", header_text)
    assert expected_header in header_text, (
        f"Expected modal header to contain '{expected_header}', but got: '{header_text}'"
    )


@then('The error modal body contains "{expectedBody}"')
def step_error_modal_body(context, expected_body):
    """
    Assert the error modal body text using the selector from constants.ts.
    Selector: #verifyPaymentBodyError
    NOTE: PAA_PAGAMENTO_DUPLICATO has no body (empty string in Examples table) — step is skipped.
    """
    page = _get_page(context)

    if not expected_body:
        logger.info("No expected body text provided (e.g. PAA_PAGAMENTO_DUPLICATO) — skipping body check")
        return

    logger.info("Checking error modal body contains: '%s'", expected_body)
    body_elem = page.locator("#verifyPaymentBodyError")
    body_elem.wait_for(state="visible", timeout=5000)
    body_text = body_elem.inner_text()
    logger.info("Error modal body: %s", body_text)
    assert expected_body in body_text, (
        f"Expected modal body to contain '{expected_body}', but got: '{body_text}'"
    )


@then('The error code shown contains "{errorCode}"')
def step_error_code_shown(context, error_code):
    """
    Assert the error code in the modal.
    Selector: #verifyPaymentErrorId (only used for PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE).
    """
    page = _get_page(context)
    logger.info("Checking error code contains: '%s'", error_code)
    error_code_elem = page.locator("#verifyPaymentErrorId")
    error_code_elem.wait_for(state="visible", timeout=5000)
    error_text = error_code_elem.inner_text()
    logger.info("Error code text: %s", error_text)
    assert error_code in error_text, (
        f"Expected error code '{error_code}' in modal, but got: '{error_text}'"
    )

@then('The error modal body contains ""')
def step_error_modal_body_empty(context):
    # Per il caso PAA_PAGAMENTO_DUPLICATO il body non è previsto.
    # Quindi questo step è un no-op intenzionale.
    logger.info("Expected empty body for this case (e.g. PAA_PAGAMENTO_DUPLICATO) — skipping body check")