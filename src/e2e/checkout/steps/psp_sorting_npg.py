import logging
import re

from behave import given, when, then
from src.e2e.checkout import get_page, get_required_config, generate_random_notice_code, locate_and_click, locate_click_and_type

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Selectors map
# ──────────────────────────────────────────────
# Summary page sort buttons
_SORT_BUTTON_SELECTORS = {
    "ordina per commissione": "#sortByFee",
    "ordina per nome": "#sortByName",
}
# PSP selection page radio options
_SORT_RADIO_SELECTORS = {
    "ordina per nome": "#sort-psp-list-drawer-order-by-name",
    "ordina per importo": "#sort-psp-list-drawer-order-by-amount",
}


# ──────────────────────────────────────────────
# GIVEN steps (Background)
# ──────────────────────────────────────────────

@given('L\'utente inserisce un codice avviso valido con prefisso "30202"')
def step_generate_notice_code(context):
    """
    Generate a random notice code with the given prefix (e.g. "30202")
    and store it in context for later steps.
    """
    context.notice_code = generate_random_notice_code("30202")
    logger.debug("Generated notice code: %s (prefix: %s)", context.notice_code, "30202")


@given('L\'utente inserisce un codice fiscale valido del pagatore')
def step_store_fiscal_code(context):
    """
    Store the fiscal code in context.
    If the value is the literal placeholder '<VALID_FISCAL_CODE>', read it from env instead.
    """
    context.fiscal_code = get_required_config(context, "VALID_FISCAL_CODE")
    logger.debug("Stored taxpayer fiscal code: %s", context.fiscal_code)


# ──────────────────────────────────────────────
# WHEN steps — notice form
# ──────────────────────────────────────────────

@when('L\'utente inserisce le informazioni dell\'avviso')
def step_enter_notice_data(context):
    """
    Open the manual keyboard form and fill in the notice code and fiscal code
    previously stored in context (from Background steps).
    """
    page = get_page(context)

    if not hasattr(context, "notice_code") or not context.notice_code:
        raise RuntimeError("notice_code not set in context — check Background step")
    if not hasattr(context, "fiscal_code") or not context.fiscal_code:
        raise RuntimeError("fiscal_code not set in context — check Background step")

    logger.debug(
        "Entering notice data — notice code: %s, fiscal code: %s",
        context.notice_code, context.fiscal_code
    )

    # Open manual input form via keyboard icon
    locate_and_click(page, "[data-testid='KeyboardIcon']")

    locate_click_and_type(page, "#billCode", context.notice_code)

    locate_click_and_type(page, "#cf", context.fiscal_code)


# ──────────────────────────────────────────────
# WHEN steps — summary page
# ──────────────────────────────────────────────

@when('L\'utente clicca il pulsante paga nella pagina di riepilogo')
def step_click_pay_summary(context):
    """Click the pay button on the payment summary page."""
    page = get_page(context)
    logger.debug("Clicking pay button on summary page")
    locate_and_click(page, "#paymentSummaryButtonPay")


@when('L\'utente inserisce e conferma l\'email')
def step_enter_and_confirm_email(context):
    """
    Fill in the email and confirm email fields using EMAIL from env,
    then click the continue button.
    """
    page = get_page(context)
    email = get_required_config(context, "EMAIL")
    logger.debug("Entering email: %s", email)

    locate_click_and_type(page, "#email", email)

    locate_click_and_type(page, "#confirmEmail", email)

    locate_and_click(page, "#paymentEmailPageButtonContinue")
    logger.debug("Email confirmed and continued")


# ──────────────────────────────────────────────
# WHEN steps — PSP list page (after PPAL selection)
# ──────────────────────────────────────────────

@when('L\'utente seleziona il PSP con id radio "{psp_radio_id}"')
def step_select_psp_radio(context, psp_radio_id):
    """Click the PSP radio button by its id (used on the PSP list page)."""
    page = get_page(context)
    logger.debug("Selecting PSP radio: %s", psp_radio_id)
    locate_and_click(page, f"#psp-radio-{psp_radio_id}")


@when('L\'utente clicca il pulsante continua della lista PSP')
def step_click_psp_list_continue(context):
    """Click the continue button on the PSP list page."""
    page = get_page(context)
    logger.debug("Clicking PSP list continue button")
    locate_and_click(page, "#paymentPspListPageButtonContinue")


# ──────────────────────────────────────────────
# WHEN steps — summary page PSP edit
# ──────────────────────────────────────────────

@when('L\'utente clicca il pulsante modifica PSP nella pagina di riepilogo')
def step_click_psp_edit_summary(context):
    """Click the PSP edit/change button on the summary page (#pspEdit)."""
    page = get_page(context)
    logger.debug("Clicking PSP edit button on summary page")
    locate_and_click(page, "#pspEdit")
    # Wait for the fee values to render before asserting sort order
    page.locator(".pspFeeValue").first.wait_for(state="visible", timeout=5000)
    logger.debug("PSP fee list loaded")


@when('L\'utente clicca il pulsante "{sort_type}"')
def step_click_sort_button(context, sort_type):
    """
    Click a sort button on the summary page PSP list.
    Supported: "sort by fee" (#sortByFee), "sort by name" (#sortByName).
    Stores the locator in context so 'button again' can reuse it.
    """
    page = get_page(context)
    selector = _SORT_BUTTON_SELECTORS.get(sort_type)
    if not selector:
        raise ValueError(f"Unknown sort type: '{sort_type}'. Known: {list(_SORT_BUTTON_SELECTORS)}")

    logger.debug("Clicking sort button '%s' (%s)", sort_type, selector)
    locate_and_click(page, selector)  # ensure click is registered (sometimes the first doesn'T work)

# ──────────────────────────────────────────────
# WHEN steps — PSP selection page sorting (drawer)
# ──────────────────────────────────────────────

@when('La pagina di selezione PSP è caricata')
def step_psp_selection_page_loaded(context):
    """Wait for the PSP selection page to render (at least one .pspFeeName visible)."""
    page = get_page(context)
    logger.debug("Waiting for PSP selection page to load (.pspFeeName)")
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    logger.debug("PSP selection page loaded")


@when('L\'utente clicca il pulsante ordina lista PSP')
def step_click_sort_psp_list_button(context):
    """Click the sort/filter button on the PSP selection page (#sort-psp-list)."""
    page = get_page(context)
    logger.debug("Clicking sort PSP list button (#sort-psp-list)")
    locate_and_click(page, "#sort-psp-list")
    logger.debug("Sort drawer opened")


@when('L\'utente seleziona l\'opzione radio "{radio_option}"')
def step_select_sort_radio(context, radio_option):
    """
    Select a sort radio option inside the sort drawer.
    Supported: "order by name", "order by amount".
    """
    page = get_page(context)
    selector = _SORT_RADIO_SELECTORS.get(radio_option)
    if not selector:
        raise ValueError(f"Unknown radio option: '{radio_option}'. Known: {list(_SORT_RADIO_SELECTORS)}")

    logger.debug("Selecting radio option '%s' (%s)", radio_option, selector)
    locate_and_click(page, selector)


@when('L\'utente clicca il pulsante mostra risultati')
def step_click_show_results(context):
    """Click the show results / apply sort button (#sort-psp-list-drawer)."""
    page = get_page(context)
    logger.debug("Clicking show results button (#sort-psp-list-drawer)")
    locate_and_click(page, "#sort-psp-list-drawer")
    logger.debug("Sort applied")

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
    for idx, elem in enumerate(elements):
        text = elem.inner_text()
        numbers = re.findall(r"[\d,]+", text)
        if not numbers:
            raise AssertionError(
                f"Cannot parse PSP fee value at index {idx}. Raw text: '{text}'"
            )

        result = "".join(numbers).replace(",", ".")
        try:
            values.append(float(result))
        except ValueError as exc:
            raise AssertionError(
                f"Invalid parsed PSP fee value at index {idx}: '{result}' from raw text '{text}'"
            ) from exc
    logger.debug("Extracted fee values: %s", values)
    return values


@then('La lista delle commissioni PSP è ordinata in ordine crescente')
def step_fee_list_ascending(context):
    """Assert that all .pspFeeValue elements are in ascending (non-decreasing) order."""
    page = get_page(context)
    values = _get_fee_values(page)
    assert len(values) > 0, "No PSP fee values found on the page"
    for i in range(len(values) - 1):
        assert values[i] <= values[i + 1], (
            f"Fee list not ascending at index {i}: {values[i]} > {values[i + 1]}\nFull list: {values}"
        )
    logger.debug("PSP fee list is correctly sorted ascending")


@then('La lista delle commissioni PSP è ordinata in ordine decrescente')
def step_fee_list_descending(context):
    """Assert that all .pspFeeValue elements are in descending (non-increasing) order."""
    page = get_page(context)
    values = _get_fee_values(page)
    assert len(values) > 0, "No PSP fee values found on the page"
    for i in range(len(values) - 1):
        assert values[i] >= values[i + 1], (
            f"Fee list not descending at index {i}: {values[i]} < {values[i + 1]}\nFull list: {values}"
        )
    logger.debug("PSP fee list is correctly sorted descending")


# ──────────────────────────────────────────────
# THEN steps — name sorting assertions
# ──────────────────────────────────────────────

def _get_name_values(page) -> list:
    """Extract all text values from .pspFeeName elements."""
    page.locator(".pspFeeName").first.wait_for(state="visible", timeout=5000)
    elements = page.locator(".pspFeeName").all()
    values = [elem.inner_text() for elem in elements]
    logger.debug("Extracted name values: %s", values)
    return values


@then('La lista dei nomi PSP è ordinata in ordine alfabetico decrescente')
def step_name_list_descending(context):
    """
    Assert that .pspFeeName elements are in descending alphabetical order.
    Mirrors: localeCompare(next) >= 0 (current >= next).
    """
    page = get_page(context)
    values = _get_name_values(page)
    assert len(values) > 0, "No PSP name values found on the page"
    for i in range(len(values) - 1):
        cmp = (values[i] > values[i + 1]) - (values[i] < values[i + 1])  # Python equivalent of localeCompare
        assert cmp >= 0, (
            f"Name list not descending at index {i}: '{values[i]}' < '{values[i + 1]}'\nFull list: {values}"
        )
    logger.debug("PSP name list is correctly sorted descending")


@then('La lista dei nomi PSP è ordinata in ordine alfabetico crescente')
def step_name_list_ascending(context):
    """
    Assert that .pspFeeName elements are in ascending alphabetical order.
    Mirrors: localeCompare(next) <= 0 (current <= next).
    """
    page = get_page(context)
    values = _get_name_values(page)
    assert len(values) > 0, "No PSP name values found on the page"
    for i in range(len(values) - 1):
        cmp = (values[i] > values[i + 1]) - (values[i] < values[i + 1])
        assert cmp <= 0, (
            f"Name list not ascending at index {i}: '{values[i]}' > '{values[i + 1]}'\nFull list: {values}"
        )
    logger.debug("PSP name list is correctly sorted ascending")


@then('L\'utente annulla il pagamento')
def step_cancel_payment(context):
    """Cancel the payment from check page and wait for the redirection button."""
    page = get_page(context)

    page.evaluate("document.querySelector('#paymentCheckPageButtonCancel').click()")
    locate_and_click(page, "#confirm")
    page.locator("#redirect-button").wait_for(state="visible", timeout=5000)
