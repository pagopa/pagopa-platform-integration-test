import logging
from behave import given, when, then
from src.e2e.checkout import get_page, get_required_config, perform_mock_login, locate_and_click

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# GIVEN steps
# ──────────────────────────────────────────────
@given('L\'utente ha effettuato l\'accesso con SPID')
def step_login_with_spid(context):
    """Authenticate the user with SPID and verify that login is completed."""
    step_click_login_button(context)
    step_check_account_icon_visible(context)

# ──────────────────────────────────────────────
# WHEN steps
# ──────────────────────────────────────────────

@when('L\'utente clicca sul pulsante di login')
def step_click_login_button(context):
    """Click the login button in the header and complete the mock/identity login flow."""
    page = get_page(context)
    checkout_url = get_required_config(context, "CHECKOUT_URL")

    logger.debug("Clicking login button in header")
    locate_and_click(page, "#login-header button")

    if "uat" in checkout_url:
        # oneIdentityLogin not yet implemented
        raise NotImplementedError("OneIdentity login not yet implemented for UAT")
    else:
        logger.debug("Performing mock login")
        perform_mock_login(page)


@when('L\'utente clicca sul pulsante utente')
def step_click_user_button(context):
    """
    Click the first button (user avatar) to open the user menu.
    Uses evaluate() to match the original TypeScript behaviour
    (document.getElementsByTagName('button')[0].click()).
    """
    page = get_page(context)
    logger.debug("Clicking user button to open user menu")
    page.wait_for_selector("button", state="visible")
    page.evaluate("document.getElementsByTagName('button')[0].click()")


@when('L\'utente clicca sul sottomenu esci')
def step_click_exit_submenu(context):
    """
    Click the first list item (exit/logout submenu entry).
    Uses evaluate() to match the original TypeScript behaviour
    (document.getElementsByTagName('li')[0].click()).
    """
    page = get_page(context)
    logger.debug("Clicking exit submenu item")
    page.evaluate("document.getElementsByTagName('li')[0].click()")


@when('L\'utente conferma l\'azione di logout')
def step_confirm_logout(context):
    """Click the confirm button in the logout modal."""
    page = get_page(context)
    logger.debug("Confirming logout")
    locate_and_click(page, "#logoutModalConfirmButton")
    # Short pause to allow the logout animation/redirect to complete
    page.wait_for_timeout(500)


# ──────────────────────────────────────────────
# THEN steps
# ──────────────────────────────────────────────

@then('L\'utente ha effettuato l\'accesso')
def step_check_account_icon_visible(context):
    """Assert that the user avatar icon is visible after login."""
    page = get_page(context)
    logger.debug("Checking AccountCircleRoundedIcon is visible")
    icon = page.query_selector("[data-testid='AccountCircleRoundedIcon']")
    assert icon is not None, "Expected AccountCircleRoundedIcon to be visible after login, but it was not found"
    logger.debug("AccountCircleRoundedIcon found — login confirmed")


@then('L\'utente ha effettuato correttamente il logout')
def step_check_login_button_visible_after_logout(context):
    """Assert that the login button reappears after logout."""
    page = get_page(context)
    logger.debug("Checking login button is visible after logout")
    login_button = page.locator("#login-header button")
    login_button.wait_for(state="visible", timeout=10000)
    assert login_button.is_visible(), "Expected login button to be visible after logout, but it was not found"
    logger.debug("Login button visible — logout confirmed")
