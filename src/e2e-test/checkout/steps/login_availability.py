import logging
from behave import when, then
from helper import _get_page, _get_required_env, _generate_random_notice_code, _locate_and_click

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

@when("I enter the notice data")
def step_enter_notice_data(context):
    page = _get_page(context)
    logger.info("Apro tastiera e porto il focus su campo avviso")
    _locate_and_click(page, SELECTORS["keyboard_icon"])
    _locate_and_click(page, SELECTORS["bill_code"])


@when("I enter the payment data")
def step_enter_payment_data(context):
    page = _get_page(context)
    notice_code = _generate_random_notice_code("30201")
    fiscal_code = _get_required_env("VALID_FISCAL_CODE")

    logger.info("Inserisco dati pagamento (notice + fiscal code)")
    page.keyboard.type(notice_code)

    _locate_and_click(page, SELECTORS["fiscal_code"])
    page.keyboard.type(fiscal_code)

    _locate_and_click(page, SELECTORS["verify_payment"])

@when("I enter the email")
def step_enter_email(context):
    page = _get_page(context)
    logger.info("Confermo riepilogo e apro step email")
    _locate_and_click(page, SELECTORS["pay_notice"])


@when("I select the payment method")
def step_select_payment_method(context):
    page = _get_page(context)
    email = _get_required_env("EMAIL")

    logger.info("Inserisco email e proseguo al metodo di pagamento")
    _locate_and_click(page, SELECTORS["email"])
    page.keyboard.type(email)

    _locate_and_click(page, SELECTORS["confirm_email"])
    page.keyboard.type(email)

    _locate_and_click(page, SELECTORS["continue_email"])


@then("the login button should be visible")
def step_login_button_visible(context):
    page = _get_page(context)
    logger.info("Verifico visibilita pulsante login")
    page.locator(SELECTORS["login_button"]).wait_for(
        state="visible", timeout=DEFAULT_TIMEOUT_MS
    )


@then('the login button title should be "Accedi"')
def step_login_button_title(context):
    page = _get_page(context)
    title = page.locator(SELECTORS["login_button"]).get_attribute("title")
    logger.info("Titolo pulsante login trovato: %r", title)
    assert title == "Accedi", f"Titolo atteso 'Accedi', ottenuto: {title!r}"
