import logging
from behave import given, when, then
from helper import _get_page, _get_required_env, _perform_mock_login, _locate_and_click

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# GIVEN steps
# ──────────────────────────────────────────────
@given('The user is logged in with SPID')
def step_login_with_spid(context):
    step_click_login_button(context)
    step_check_account_icon_visible(context)

# ──────────────────────────────────────────────
# WHEN steps
# ──────────────────────────────────────────────

@when('The user clicks on the login button')
def step_click_login_button(context):
    """Click the login button in the header and complete the mock/identity login flow."""
    page = _get_page(context)
    checkout_url = _get_required_env("CHECKOUT_URL")

    logger.info("Clicking login button in header")
    _locate_and_click(page, "#login-header button")

    if "uat" in checkout_url:
        # oneIdentityLogin not yet implemented
        raise NotImplementedError("OneIdentity login not yet implemented for UAT")
    else:
        logger.info("Performing mock login")
        _perform_mock_login(page)


@when('The user clicks on user button')
def step_click_user_button(context):
    """
    Click the first button (user avatar) to open the user menu.
    Uses evaluate() to match the original TypeScript behaviour
    (document.getElementsByTagName('button')[0].click()).
    """
    page = _get_page(context)
    logger.info("Clicking user button to open user menu")
    page.wait_for_selector("button", state="visible")
    page.evaluate("document.getElementsByTagName('button')[0].click()")


@when('The user clicks on exit submenu')
def step_click_exit_submenu(context):
    """
    Click the first list item (exit/logout submenu entry).
    Uses evaluate() to match the original TypeScript behaviour
    (document.getElementsByTagName('li')[0].click()).
    """
    page = _get_page(context)
    logger.info("Clicking exit submenu item")
    page.evaluate("document.getElementsByTagName('li')[0].click()")


@when('The user confirm the logout action')
def step_confirm_logout(context):
    """Click the confirm button in the logout modal."""
    page = _get_page(context)
    logger.info("Confirming logout")
    _locate_and_click(page, "#logoutModalConfirmButton")
    # Short pause to allow the logout animation/redirect to complete
    page.wait_for_timeout(500)


# ──────────────────────────────────────────────
# THEN steps
# ──────────────────────────────────────────────

@then('The user is logged in')
def step_check_account_icon_visible(context):
    """Assert that the user avatar icon is visible after login."""
    page = _get_page(context)
    logger.info("Checking AccountCircleRoundedIcon is visible")
    icon = page.query_selector("[data-testid='AccountCircleRoundedIcon']")
    assert icon is not None, "Expected AccountCircleRoundedIcon to be visible after login, but it was not found"
    logger.info("AccountCircleRoundedIcon found — login confirmed")


@then('The user is succesfully logged out')
def step_check_login_button_visible_after_logout(context):
    """Assert that the login button reappears after logout."""
    page = _get_page(context)
    logger.info("Checking login button is visible after logout")
    login_button = page.locator("#login-header button")
    login_button.wait_for(state="visible", timeout=10000)
    assert login_button.is_visible(), "Expected login button to be visible after logout, but it was not found"
    logger.info("Login button visible — logout confirmed")
