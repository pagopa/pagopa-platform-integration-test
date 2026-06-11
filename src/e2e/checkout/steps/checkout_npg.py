import logging
import random

from behave import given, when, then
from src.e2e.checkout import get_page, get_required_config, generate_random_notice_code, locate_and_click, locate_click_and_type

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────

@given('La pagina di checkout è aperta')
def step_checkout_page_open(context):
    """Navigate to the checkout URL."""
    page = get_page(context)
    checkout_url = get_required_config(context, "CHECKOUT_URL")
    logger.debug("Opening checkout page: %s", checkout_url)
    page.goto(checkout_url, wait_until="domcontentloaded")
    # Initialise context storage for state shared between steps
    context.notice_code = None
    context.fiscal_code = None

@given('La lingua è impostata su "it"')
def step_set_language_it(context):
    page = get_page(context)
    logger.debug("Imposto lingua a 'it'")
    page.locator("#languageMenu").wait_for(
        state="visible", timeout=5000
    )
    page.select_option("#languageMenu", "it")


# ──────────────────────────────────────────────
# WHEN steps — notice form
# ──────────────────────────────────────────────

@when(u'L\'utente inserisce i dati dell\'avviso con un codice avviso con prefisso "{notice_code_prefix}"')
def step_enter_notice_random(context, notice_code_prefix):
    """
    Click the keyboard icon to open the manual form,
    then generate and type a random notice code for the given prefix.
    """
    page = get_page(context)
    context.notice_code = generate_random_notice_code(notice_code_prefix)
    logger.debug("Generated notice code: %s (prefix: %s)", context.notice_code, notice_code_prefix)

    logger.debug("Clicking keyboard icon")
    locate_and_click(page, "[data-testid='KeyboardIcon']")

    locate_click_and_type(page, "#billCode", context.notice_code)
    logger.debug("Notice code typed: %s", context.notice_code)


@when('L\'utente inserisce i dati dell\'avviso con un codice avviso nell\'intervallo "{range_start}" a "{range_end}"')
def step_enter_notice_in_range(context, range_start, range_end):
    """
    Click the keyboard icon and type a notice code within the given numeric range.
    When range_start == range_end (e.g. PAA_PAGAMENTO_DUPLICATO), uses the fixed value.
    """
    page = get_page(context)

    start = int(range_start)
    end = int(range_end)
    context.notice_code = str(random.randint(start, end))
    logger.debug(
        "Generated error-case notice code: %s (range: %s - %s)",
        context.notice_code, range_start, range_end
    )

    logger.debug("Clicking keyboard icon")
    locate_and_click(page, "[data-testid='KeyboardIcon']")

    locate_click_and_type(page, "#billCode", context.notice_code)


@when(u'L\'utente inserisce il codice fiscale del pagatore "{fiscal_code}"')
def step_enter_fiscal_code(context, fiscal_code):
    """Type the taxpayer fiscal code into the #cf field."""
    page = get_page(context)
    context.fiscal_code = fiscal_code
    logger.debug("Typing fiscal code: %s", fiscal_code)
    locate_click_and_type(page, "#cf", fiscal_code)


@when('L\'utente clicca il pulsante verifica')
def step_click_verify(context):
    """Click the continue/verify button on the notice form."""
    page = get_page(context)
    logger.debug("Clicking verify/continue button")
    locate_and_click(page, "#paymentNoticeButtonContinue")

# ──────────────────────────────────────────────
# WHEN steps — summary & email
# ──────────────────────────────────────────────

@when('L\'utente clicca il pulsante paga')
def step_click_pay_on_summary(context):
    """Click the pay button on the payment summary page."""
    page = get_page(context)
    logger.debug("Clicking pay button on summary page")
    locate_and_click(page, "#paymentSummaryButtonPay")


@when('L\'utente inserisce l\'email "{email}"')
def step_enter_email(context, email):
    """Type the email address into the email field."""
    page = get_page(context)
    context.email = email
    logger.debug("Typing email: %s", email)
    locate_click_and_type(page, "#email", email)


@when('L\'utente conferma l\'email "{email}"')
def step_confirm_email(context, email):
    """Type the email into the confirm field and click continue."""
    page = get_page(context)
    logger.debug("Confirming email: %s", email)
    locate_click_and_type(page, "#confirmEmail", email)
    locate_and_click(page, "#paymentEmailPageButtonContinue")


# ──────────────────────────────────────────────
# WHEN steps — payment method
# ──────────────────────────────────────────────

@when('L\'utente seleziona il metodo di pagamento "{method}"')
def step_select_payment_method(context, method):
    """Select the desired payment method by its data-qaid attribute."""
    page = get_page(context)
    logger.debug("Selecting payment method: %s", method)
    locate_and_click(page, f"[data-qaid={method}]")


# ──────────────────────────────────────────────
# WHEN steps — card form (individual fields)
# ──────────────────────────────────────────────

@when(u'L\'utente inserisce il numero carta "{card_number}"')
def step_fill_card_number(context, card_number):
    """Type the card number into the NPG iframe field."""
    page = get_page(context)
    logger.debug("Waiting for NPG iframe to load")
    page.locator("#frame_CARD_NUMBER").wait_for(state="visible", timeout=30000)
    page.wait_for_load_state("networkidle")
    logger.debug("Filling card number")
    locate_click_and_type(page, "#frame_CARD_NUMBER", card_number, click_count=3, timeout=10000)


@when(u'L\'utente inserisce la data di scadenza "{expiration_date}"')
def step_fill_expiration_date(context, expiration_date):
    """Type the expiration date into the NPG iframe field."""
    page = get_page(context)
    logger.debug("Filling expiration date: %s", expiration_date)
    locate_click_and_type(page, "#frame_EXPIRATION_DATE", expiration_date, click_count=3)


@when(u'L\'utente inserisce il codice di sicurezza "{cvv}"')
def step_fill_security_code(context, cvv):
    """Type the CVV into the NPG iframe field."""
    page = get_page(context)
    logger.debug("Filling security code (CVV)")
    locate_click_and_type(page, "#frame_SECURITY_CODE", cvv, click_count=3)

@when(u'L\'utente inserisce il nome dell\'intestatario carta "{holder_name}"')
def step_fill_cardholder_name(context, holder_name):
    """Type the cardholder name into the NPG iframe field."""
    page = get_page(context)
    logger.debug("Filling cardholder name: %s", holder_name)
    locate_click_and_type(page, "#frame_CARDHOLDER_NAME", holder_name, click_count=3)

# ──────────────────────────────────────────────
# WHEN steps — PSP selection
# ──────────────────────────────────────────────

@when(u'L\'utente seleziona il PSP con id "{psp_id}"')
def step_select_psp(context, psp_id):
    """
    Click the card form continue button to reach the PSP list,
    then select the radio button for the given PSP id.
    """
    page = get_page(context)
    logger.debug("Clicking card form continue button")
    locate_and_click(page, "button[type=submit]")
    logger.debug("Selecting PSP radio: %s", psp_id)
    locate_and_click(page, f"#psp-radio-{psp_id}")


@when('L\'utente conferma la selezione del PSP')
def step_confirm_psp(context):
    """Click the continue button on the PSP list page."""
    page = get_page(context)
    logger.debug("Confirming PSP selection")
    locate_and_click(page, "#paymentPspListPageButtonContinue")


@when('L\'utente clicca il pulsante paga finale')
def step_click_final_pay(context):
    """Click the final pay button and wait for the NPG mock auto-authorisation."""
    page = get_page(context)
    logger.debug("Clicking final pay button")
    locate_and_click(page, "#paymentCheckPageButtonPay")
    logger.debug("Final pay button clicked — waiting for load (NPG mock auto-authorises)")
    page.wait_for_load_state("load")

# ──────────────────────────────────────────────
# THEN steps — error modal
# ──────────────────────────────────────────────

@then('Viene mostrata una modale di errore dopo "{seconds}" secondi')
def step_error_modal_visible_after(context, seconds = 5):
    """
    Assert that the error title element is visible.
    Selector: #verifyPaymentTitleError (from constants.ts — all error cases use this).
    """
    timeout_ms = int(float(seconds) * 1000)
    page = get_page(context)
    logger.debug("Checking error modal title is displayed")
    page.locator("#verifyPaymentTitleError").wait_for(state="visible", timeout=timeout_ms)
    logger.debug("Error modal is visible")

@then('Viene mostrata una modale di errore')
def step_error_modal_visible(context):
    """
    Assert that the error title element is visible.
    Selector: #verifyPaymentTitleError (from constants.ts — all error cases use this).
    """
    step_error_modal_visible_after(context,5)


@then('L\'intestazione della modale di errore contiene "{expected_header}"')
def step_error_modal_header(context, expected_header):
    """
    Assert the error modal header text using the selector from constants.ts.
    Selector: #verifyPaymentTitleError
    """
    page = get_page(context)
    logger.debug("Checking error modal header contains: '%s'", expected_header)
    header_elem = page.locator("#verifyPaymentTitleError")
    header_elem.wait_for(state="visible", timeout=5000)
    header_text = header_elem.inner_text()
    logger.debug("Error modal header: %s", header_text)
    assert expected_header in header_text, (
        f"Expected modal header to contain '{expected_header}', but got: '{header_text}'"
    )


@then('Il corpo della modale di errore contiene "{expected_body}"')
def step_error_modal_body(context, expected_body):
    """
    Assert the error modal body text using the selector from constants.ts.
    Selector: #verifyPaymentBodyError
    NOTE: PAA_PAGAMENTO_DUPLICATO has no body (empty string in Examples table) — step is skipped.
    """
    page = get_page(context)

    if not expected_body:
        logger.debug("No expected body text provided (e.g. PAA_PAGAMENTO_DUPLICATO) — skipping body check")
        return

    logger.debug("Checking error modal body contains: '%s'", expected_body)
    body_elem = page.locator("#verifyPaymentBodyError")
    body_elem.wait_for(state="visible", timeout=5000)
    body_text = body_elem.inner_text()
    logger.debug("Error modal body: %s", body_text)
    assert expected_body in body_text, (
        f"Expected modal body to contain '{expected_body}', but got: '{body_text}'"
    )


@then('Il codice di errore mostrato contiene "{error_code}"')
def step_error_code_shown(context, error_code):
    """
    Assert the error code in the modal.
    Selector: #verifyPaymentErrorId (only used for PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE).
    """
    page = get_page(context)
    logger.debug("Checking error code contains: '%s'", error_code)
    error_code_elem = page.locator("#verifyPaymentErrorId")
    error_code_elem.wait_for(state="visible", timeout=5000)
    error_text = error_code_elem.inner_text()
    logger.debug("Error code text: %s", error_text)
    assert error_code in error_text, (
        f"Expected error code '{error_code}' in modal, but got: '{error_text}'"
    )

@then('Il corpo della modale di errore contiene ""')
def step_error_modal_body_empty(context):
    # Per il caso PAA_PAGAMENTO_DUPLICATO il body non è previsto.
    # Quindi questo step è un no-op intenzionale.
    logger.debug("Expected empty body for this case (e.g. PAA_PAGAMENTO_DUPLICATO) — skipping body check")

@then('Viene mostrato un messaggio di pagamento completato con successo')
def step_check_payment_success(context):
    page = get_page(context)
    result_title_selector = "#responsePageMessageTitle"

    logger.debug("Waiting for result page title (max 120s)...")
    page.locator(result_title_selector).wait_for(
        state="visible", timeout=120000
    )
    message_text = page.locator(result_title_selector).inner_text()
    logger.debug("Result message found: %s", message_text)

    assert "Hai pagato" in message_text, (
        f"Expected 'Hai pagato' in result message, but got: '{message_text}'"
    )