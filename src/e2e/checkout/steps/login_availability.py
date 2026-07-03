import logging

from behave import given, then, when

from src.e2e.checkout import (
    generate_random_notice_code,
    get_page,
    get_required_config,
    locate_and_click,
    locate_click_and_type,
)

logger = logging.getLogger(__name__)

# Shared selectors
SELECTORS = {
    "language_menu": "#languageMenu",
    "keyboard_icon": "[data-testid='KeyboardIcon']",
    "bill_code": "#billCode",
    "fiscal_code": "#cf",
    "verify_payment": "#paymentNoticeButtonContinue",
    "login_button": "#login-header button",
    "pay_notice": "#paymentSummaryButtonPay",
    "email": "#email",
    "confirm_email": "#confirmEmail",
    "continue_email": "#paymentEmailPageButtonContinue",
}

DEFAULT_TIMEOUT_MS = 5000


@given("L'utente inserisce i dati dell'avviso")
@when("L'utente inserisce i dati dell'avviso")
def step_enter_notice_data(context):
    """Prepare the notice input step by focusing the notice field."""
    page = get_page(context)
    logger.debug("Apro tastiera e porto il focus su campo avviso")
    locate_and_click(page, SELECTORS["keyboard_icon"])
    locate_and_click(page, SELECTORS["bill_code"])


@given("L'utente inserisce i dati di pagamento")
@when("L'utente inserisce i dati di pagamento")
def step_enter_payment_data(context):
    """Fill notice and fiscal code, then verify the payment notice."""
    page = get_page(context)
    notice_code = generate_random_notice_code("30201")
    fiscal_code = get_required_config(context, "VALID_FISCAL_CODE")

    logger.debug("Inserisco dati pagamento (notice + fiscal code)")
    locate_click_and_type(page, SELECTORS["bill_code"], notice_code)
    locate_click_and_type(page, SELECTORS["fiscal_code"], fiscal_code)
    locate_and_click(page, SELECTORS["verify_payment"])


@given("L'utente inserisce l'email")
@when("L'utente inserisce l'email")
def step_enter_email(context):
    """Open the email step from the payment summary page."""
    page = get_page(context)
    logger.debug("Confermo riepilogo e apro step email")
    locate_and_click(page, SELECTORS["pay_notice"])


@when("L'utente seleziona il metodo di pagamento")
def step_select_payment_method(context):
    """Fill and confirm email, then continue to payment method selection."""
    page = get_page(context)
    email = get_required_config(context, "EMAIL")

    logger.debug("Inserisco email e proseguo al metodo di pagamento")
    locate_click_and_type(page, SELECTORS["email"], email)
    locate_click_and_type(page, SELECTORS["confirm_email"], email)
    locate_and_click(page, SELECTORS["continue_email"])


@then("Il pulsante di login è visibile e abilitato")
def step_login_button_visible(context):
    """Assert that the login button is visible and enabled."""
    page = get_page(context)
    logger.debug("Verifico visibilita e stato abilitato del pulsante login")
    login_button = page.locator(SELECTORS["login_button"])
    login_button.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
    assert login_button.is_enabled(), "Il pulsante di login non e abilitato"


@then('Il titolo del pulsante di login è "Accedi"')
def step_login_button_title(context):
    """Assert that the login button title is exactly 'Accedi'."""
    page = get_page(context)
    title = page.locator(SELECTORS["login_button"]).get_attribute("title")
    logger.debug("Titolo pulsante login trovato: %r", title)
    assert title == "Accedi", f"Titolo atteso 'Accedi', ottenuto: {title!r}"