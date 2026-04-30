import logging
import re

from behave import given, when, then
from helper import _get_page, _get_required_env, _generate_random_notice_code, _locate_and_click

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Selectors map
# ──────────────────────────────────────────────
# Summary page sort buttons
_SORT_BUTTON_SELECTORS = {
    "sort by fee": "#sortByFee",
    "sort by name": "#sortByName",
}
# PSP selection page radio options
_SORT_RADIO_SELECTORS = {
    "order by name": "#sort-psp-list-drawer-order-by-name",
    "order by amount": "#sort-psp-list-drawer-order-by-amount",
}


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────

@given('The user enters a valid notice code with prefix "30202"')
def step_generate_notice_code(context):
    """
    Generate a random notice code with the given prefix (e.g. "30202")
    and store it in context for later steps.
    """
    context.notice_code = _generate_random_notice_code("30202")
    logger.info("Generated notice code: %s (prefix: %s)", context.notice_code, "30202")


@given('The user enters a valid taxpayer fiscal code')
def step_store_fiscal_code(context):
    """
    Store the fiscal code in context.
    If the value is the literal placeholder '<VALID_FISCAL_CODE>', read it from env instead.
    """
    context.fiscal_code = _get_required_env("VALID_FISCAL_CODE")
    logger.info("Stored taxpayer fiscal code: %s", context.fiscal_code)


# ──────────────────────────────────────────────
# WHEN steps — notice form
# ──────────────────────────────────────────────

@when('The user enters the notice information')
def step_enter_notice_data(context):
    """
    Open the manual keyboard form and fill in the notice code and fiscal code
    previously stored in context (from Background steps).
    """
    page = _get_page(context)

    if not hasattr(context, "notice_code") or not context.notice_code:
        raise RuntimeError("notice_code not set in context — check Background step")
    if not hasattr(context, "fiscal_code") or not context.fiscal_code:
        raise RuntimeError("fiscal_code not set in context — check Background step")

    logger.info(
        "Entering notice data — notice code: %s, fiscal code: %s",
        context.notice_code, context.fiscal_code
    )

    # Open manual input form via keyboard icon
    _locate_and_click(page, "[data-testid='KeyboardIcon']")

    _locate_and_click(page, "#billCode")
    page.keyboard.type(context.notice_code)

    _locate_and_click(page, "#cf")
    page.keyboard.type(context.fiscal_code)


# ──────────────────────────────────────────────
# WHEN steps — summary page
# ──────────────────────────────────────────────

@when('The user clicks the pay button on the summary page')
def step_click_pay_summary(context):
    """Click the pay button on the payment summary page."""
    page = _get_page(context)
    logger.info("Clicking pay button on summary page")
    _locate_and_click(page, "#paymentSummaryButtonPay")


@when('The user enters and confirm the email')
def step_enter_and_confirm_email(context):
    """
    Fill in the email and confirm email fields using EMAIL from env,
    then click the continue button.
    """
    page = _get_page(context)
    email = _get_required_env("EMAIL")
    logger.info("Entering email: %s", email)

    _locate_and_click(page, "#email")
    page.keyboard.type(email)

    _locate_and_click(page, "#confirmEmail")
    page.keyboard.type(email)

    _locate_and_click(page, "#paymentEmailPageButtonContinue")
    logger.info("Email confirmed and continued")


# ──────────────────────────────────────────────
# WHEN steps — PSP list page (after PPAL selection)
# ──────────────────────────────────────────────

@when('The user selects the PSP with radio id "{psp_radio_id}"')
def step_select_psp_radio(context, psp_radio_id):
    """Click the PSP radio button by its id (used on the PSP list page)."""
    page = _get_page(context)
    logger.info("Selecting PSP radio: %s", psp_radio_id)
    _locate_and_click(page, f"#psp-radio-{psp_radio_id}")


@when('The user clicks the PSP list continue button')
def step_click_psp_list_continue(context):
    """Click the continue button on the PSP list page."""
    page = _get_page(context)
    logger.info("Clicking PSP list continue button")
    _locate_and_click(page, "#paymentPspListPageButtonContinue")


# ──────────────────────────────────────────────
# WHEN steps — summary page PSP edit
# ──────────────────────────────────────────────

@when('The user clicks the PSP edit button on the summary page')
def step_click_psp_edit_summary(context):
    """Click the PSP edit/change button on the summary page (#pspEdit)."""
    page = _get_page(context)
    logger.info("Clicking PSP edit button on summary page")
    _locate_and_click(page, "#pspEdit")
    # Wait for the fee values to render before asserting sort order
    page.locator(".pspFeeValue").first.wait_for(state="visible", timeout=5000)
    logger.info("PSP fee list loaded")


@when('The user clicks the "{sort_type}" button')
def step_click_sort_button(context, sort_type):
    """
    Click a sort button on the summary page PSP list.
    Supported: "sort by fee" (#sortByFee), "sort by name" (#sortByName).
    Stores the locator in context so 'button again' can reuse it.
    """
    page = _get_page(context)
    selector = _SORT_BUTTON_SELECTORS.get(sort_type)
    if not selector:
        raise ValueError(f"Unknown sort type: '{sort_type}'. Known: {list(_SORT_BUTTON_SELECTORS)}")

    logger.info("Clicking sort button '%s' (%s)", sort_type, selector)
    _locate_and_click(page, selector)  # ensure click is registered (sometimes the first doesn'T work)

# ──────────────────────────────────────────────
# WHEN steps — PSP selection page sorting (drawer)
# ──────────────────────────────────────────────

@when('The PSP selection page is loaded')
def step_psp_selection_page_loaded(context):
    """Wait for the PSP selection page to render (at least one .pspFeeName visible)."""
    page = _get_page(context)
    logger.info("Waiting for PSP selection page to load (.pspFeeName)")
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    logger.info("PSP selection page loaded")


@when('The user clicks the sort PSP list button')
def step_click_sort_psp_list_button(context):
    """Click the sort/filter button on the PSP selection page (#sort-psp-list)."""
    page = _get_page(context)
    logger.info("Clicking sort PSP list button (#sort-psp-list)")
    _locate_and_click(page, "#sort-psp-list")
    logger.info("Sort drawer opened")


@when('The user selects the "{radio_option}" radio option')
def step_select_sort_radio(context, radio_option):
    """
    Select a sort radio option inside the sort drawer.
    Supported: "order by name", "order by amount".
    """
    page = _get_page(context)
    selector = _SORT_RADIO_SELECTORS.get(radio_option)
    if not selector:
        raise ValueError(f"Unknown radio option: '{radio_option}'. Known: {list(_SORT_RADIO_SELECTORS)}")

    logger.info("Selecting radio option '%s' (%s)", radio_option, selector)
    _locate_and_click(page, selector)


@when('The user clicks the show results button')
def step_click_show_results(context):
    """Click the show results / apply sort button (#sort-psp-list-drawer)."""
    page = _get_page(context)
    logger.info("Clicking show results button (#sort-psp-list-drawer)")
    _locate_and_click(page, "#sort-psp-list-drawer")
    logger.info("Sort applied")


# ──────────────────────────────────────────────
# WHEN steps — cancel payment
# ──────────────────────────────────────────────

@when('The user cancels the payment')
def step_cancel_payment(context):
    """
    Cancel the current payment:
    click the cancel button (via JS evaluate to bypass animation),
    confirm in the modal, and wait for the redirect button.
    """
    page = _get_page(context)
    logger.info("Cancelling payment")

    # Use evaluate() — direct click doesn'T work after animation (matches TypeScript page.$eval)
    page.evaluate("document.querySelector('#paymentCheckPageButtonCancel').click()")
    logger.info("Cancel button clicked via evaluate")

    _locate_and_click(page, "#confirm")
    logger.info("Confirmation dialog confirmed")

    page.locator("#redirect-button").wait_for(state="visible", timeout=5000)
    logger.info("Payment cancelled — redirect button visible")


# ──────────────────────────────────────────────
# THEN steps — fee sorting assertions
# ──────────────────────────────────────────────

def _get_fee_values(page) -> list:
    """
    Extract all numeric fee values from .pspFeeValue elements.
    Matches the TypeScript regex: /[\\d,]+/g → join → replace ',' with '.' → parseFloat.
    """
    page.locator(".pspFeeValue").first.wait_for(state="visible", timeout=5000)
    elements = page.locator(".pspFeeValue").all()
    values = []
    for elem in elements:
        text = elem.inner_text()
        numbers = re.findall(r"[\d,]+", text)
        result = "".join(numbers).replace(",", ".") if numbers else ""
        try:
            values.append(float(result))
        except ValueError:
            values.append(0.0)
    logger.info("Extracted fee values: %s", values)
    return values


@then('The PSP fee list is sorted in ascending order')
def step_fee_list_ascending(context):
    """Assert that all .pspFeeValue elements are in ascending (non-decreasing) order."""
    page = _get_page(context)
    values = _get_fee_values(page)
    assert len(values) > 0, "No PSP fee values found on the page"
    for i in range(len(values) - 1):
        assert values[i] <= values[i + 1], (
            f"Fee list not ascending at index {i}: {values[i]} > {values[i + 1]}\nFull list: {values}"
        )
    logger.info("PSP fee list is correctly sorted ascending")


@then('The PSP fee list is sorted in descending order')
def step_fee_list_descending(context):
    """Assert that all .pspFeeValue elements are in descending (non-increasing) order."""
    page = _get_page(context)
    values = _get_fee_values(page)
    assert len(values) > 0, "No PSP fee values found on the page"
    for i in range(len(values) - 1):
        assert values[i] >= values[i + 1], (
            f"Fee list not descending at index {i}: {values[i]} < {values[i + 1]}\nFull list: {values}"
        )
    logger.info("PSP fee list is correctly sorted descending")


# ──────────────────────────────────────────────
# THEN steps — name sorting assertions
# ──────────────────────────────────────────────

def _get_name_values(page) -> list:
    """Extract all text values from .pspFeeName elements."""
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    elements = page.locator(".pspFeeName").all()
    values = [elem.inner_text() for elem in elements]
    logger.info("Extracted name values: %s", values)
    return values


@then('The PSP name list is sorted in descending alphabetical order')
def step_name_list_descending(context):
    """
    Assert that .pspFeeName elements are in descending alphabetical order.
    Mirrors: localeCompare(next) >= 0 (current >= next).
    """
    page = _get_page(context)
    values = _get_name_values(page)
    assert len(values) > 0, "No PSP name values found on the page"
    for i in range(len(values) - 1):
        cmp = (values[i] > values[i + 1]) - (values[i] < values[i + 1])  # Python equivalent of localeCompare
        assert cmp >= 0, (
            f"Name list not descending at index {i}: '{values[i]}' < '{values[i + 1]}'\nFull list: {values}"
        )
    logger.info("PSP name list is correctly sorted descending")


@then('The PSP name list is sorted in ascending alphabetical order')
def step_name_list_ascending(context):
    """
    Assert that .pspFeeName elements are in ascending alphabetical order.
    Mirrors: localeCompare(next) <= 0 (current <= next).
    """
    page = _get_page(context)
    values = _get_name_values(page)
    assert len(values) > 0, "No PSP name values found on the page"
    for i in range(len(values) - 1):
        cmp = (values[i] > values[i + 1]) - (values[i] < values[i + 1])
        assert cmp <= 0, (
            f"Name list not ascending at index {i}: '{values[i]}' > '{values[i + 1]}'\nFull list: {values}"
        )
    logger.info("PSP name list is correctly sorted ascending")


@then('The user cancels the payment')
def step_cancel_payment(context):
    page = _get_page(context)

    page.evaluate("document.querySelector('#paymentCheckPageButtonCancel').click()")
    _locate_and_click(page, "#confirm")
    page.locator("#redirect-button").wait_for(state="visible", timeout=5000)
