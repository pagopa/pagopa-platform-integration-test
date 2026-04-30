import logging
from behave import given, when, then
from helper import _get_page, _get_required_env, _generate_random_notice_code, _perform_mock_login, _locate_and_click, _get_required_json_env

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# GIVEN steps
# ──────────────────────────────────────────────

@given('The user is logged in')
def step_logged_in(context):
    page = _get_page(context)
    checkout_url = _get_required_env("CHECKOUT_URL")

    logger.info("Clicking login button")
    _locate_and_click(page, "#login-header button")

    if "uat" in checkout_url:
        # _perform_identity_login(page)  # not yet implemented
        raise NotImplementedError("OneIdentity login not yet implemented for UAT")
    else:
        logger.info("Performing mock login")
        _perform_mock_login(page)


# ──────────────────────────────────────────────
# WHEN steps
# ──────────────────────────────────────────────

@when('The user insert the payment notice details')
def step_insert_notice_details(context):
    page = _get_page(context)

    # Read card data from env and find the Worldpay card
    cards_obj = _get_required_json_env("CARD_TEST_DATA")
    logger.info("Parsed CARD_TEST_DATA from environment: %s", cards_obj)
    cards = cards_obj.get("cards", [])

    card_data = next(
        (card for card in cards if card.get("testingPsp") == "Worldpay"),
        None
    )
    if card_data is None:
        raise RuntimeError("No card found for testingPsp='Worldpay' in CARD_TEST_DATA")

    logger.info("Card data found for PSP: %s", card_data.get("testingPsp"))
    context.card_data = card_data

    _fill_notice_form(page, card_data)
    logger.info("Clicking pay button on summary page")
    _locate_and_click(page, "#paymentSummaryButtonPay")
    _fill_email_form(page)
    _choose_payment_method(page, "CP")
    _fill_card_data_form(page, card_data)


# ──────────────────────────────────────────────
# THEN steps
# ──────────────────────────────────────────────

@then('A successful payment message is shown')
def step_check_payment_success(context):
    page = _get_page(context)
    result_title_selector = "#responsePageMessageTitle"

    logger.info("Waiting for result page title (max 120s)...")
    page.locator(result_title_selector).wait_for(
        state="visible", timeout=120000
    )
    message_text = page.locator(result_title_selector).inner_text()
    logger.info("Result message found: %s", message_text)

    assert "Hai pagato" in message_text, (
        f"Expected 'Hai pagato' in result message, but got: '{message_text}'"
    )


# ──────────────────────────────────────────────
# Private helper functions
# ──────────────────────────────────────────────

def _fill_notice_form(page, card_data):
    """Fill the notice code form: keyboard icon → notice code → fiscal code → continue."""
    # Generate a random notice code using the card's fiscal code prefix
    fiscal_code_prefix = str(card_data.get("fiscalCodePrefix", "30201"))
    notice_code = _generate_random_notice_code(fiscal_code_prefix)
    fiscal_code = _get_required_env("VALID_FISCAL_CODE")

    logger.info("Generated notice code: %s, fiscal code: %s", notice_code, fiscal_code)

    # Click the keyboard icon to open the manual input form
    logger.info("Clicking keyboard icon to open manual form")
    _locate_and_click(page, "[data-testid='KeyboardIcon']")

    # Fill notice code
    _locate_and_click(page, "#billCode")
    page.keyboard.type(notice_code)

    # Fill fiscal code
    _locate_and_click(page, "#cf")
    page.keyboard.type(fiscal_code)

    # Click continue / verify button
    _locate_and_click(page, "#paymentNoticeButtonContinue")


def _fill_email_form(page):
    """Fill the email form and click continue."""
    email = _get_required_env("EMAIL")
    logger.info("Filling email form with: %s", email)

    _locate_and_click(page, "#email")
    page.keyboard.type(email)

    _locate_and_click(page, "#confirmEmail")
    page.keyboard.type(email)

    _locate_and_click(page, "#paymentEmailPageButtonContinue")


def _choose_payment_method(page, method):
    """Select the payment method by its data-qaid attribute."""
    logger.info("Choosing payment method: %s", method)
    # FIX: corrected selector (was missing closing bracket and had extra '[')
    _locate_and_click(page,f"[data-qaid={method}]")


def _fill_card_data_form(page, card_data):
    """
    Fill the NPG card iframe fields in a loop until the submit button is enabled,
    then select the PSP, confirm and click the final pay button.
    """
    psp_id = card_data.get("pspId")
    iteration = 0
    completed = False

    while not completed:
        iteration += 1
        logger.info("Compiling card fields... attempt %d", iteration)

        # Card number
        _locate_and_click(page, "#frame_CARD_NUMBER",3,15000)
        page.keyboard.type(str(card_data["pan"]))
        logger.info("Card number filled")

        # Expiration date
        _locate_and_click(page, "#frame_EXPIRATION_DATE",3)
        page.keyboard.type(str(card_data["expirationDate"]))
        logger.info("Expiration date filled")

        # Security code (CVV)
        _locate_and_click(page, "#frame_SECURITY_CODE",3)
        page.keyboard.type(str(card_data["cvv"]))
        logger.info("CVV filled")

        # Cardholder name
        _locate_and_click(page, "#frame_CARDHOLDER_NAME",3)
        page.keyboard.type("Test test")
        logger.info("Cardholder name filled")

        # Check if the submit button is still disabled
        # FIX: corrected f-string with escaped quotes
        disabled_btn = page.query_selector('button[type=submit][disabled=""]')
        completed = disabled_btn is None

        if not completed:
            page.wait_for_timeout(80)  # wait 80ms before retrying

    # Click continue button
    logger.info("Clicking continue button")
    _locate_and_click(page, "button[type=submit]")

    # Select PSP radio button
    logger.info("Selecting PSP with id: %s", psp_id)
    _locate_and_click(page,f"#psp-radio-{psp_id}")

    # Click PSP list continue button
    _locate_and_click(page,"#paymentPspListPageButtonContinue")

    # Click final pay button (wait until enabled)
    logger.info("Clicking final pay button")
    _locate_and_click(page,"#paymentCheckPageButtonPay")

    logger.info("Pay button clicked, waiting for navigation")
    # NPG mock: authorization is automatic, just wait for page load
    page.wait_for_load_state("load")
