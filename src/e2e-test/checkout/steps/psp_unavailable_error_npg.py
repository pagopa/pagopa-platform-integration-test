import logging
from behave import when, then
from helper import _get_page, _get_required_env, _locate_and_click


logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# WHEN steps — notice form (only notice code)
# ──────────────────────────────────────────────

@when('I enter only the notice data with the generated notice code')
def step_enter_only_notice_code(context):
    """
    Open the manual keyboard form and type only the notice code stored in context.
    The fiscal code is entered in a separate step.
    Different from psp_sorting_npg.py which enters both fields in one step.
    """
    page = _get_page(context)

    if not hasattr(context, "notice_code") or not context.notice_code:
        raise RuntimeError("notice_code not set in context — check 'a random notice code with prefix' step")

    logger.info("Opening keyboard form and entering notice code: %s", context.notice_code)

    # Open manual input form via keyboard icon
    _locate_and_click(page, "[data-testid='KeyboardIcon']")

    _locate_and_click(page, "#billCode")
    page.keyboard.type(context.notice_code)
    logger.info("Notice code typed: %s", context.notice_code)


@when('I enter the taxpayer fiscal code from env "{env_key}"')
def step_enter_fiscal_code_from_env(context, env_key):
    """
    Read the fiscal code from the given env variable and type it into the #cf field.
    Used when the value must be resolved at runtime from environment (not hardcoded in feature).
    """
    page = _get_page(context)
    fiscal_code = _get_required_env(env_key)
    context.fiscal_code = fiscal_code
    logger.info("Typing fiscal code from env '%s': %s", env_key, fiscal_code)
    _locate_and_click(page, "#cf")
    page.keyboard.type(fiscal_code)


# ──────────────────────────────────────────────
# THEN steps — PSP not found error page
# ──────────────────────────────────────────────

@then('a PSP not found error page should be displayed')
def step_psp_not_found_page_displayed(context):
    """
    Assert that the PSP not found error page is visible.
    Waits for the title element #pspNotFoundTitleId to appear.
    Selector from TypeScript: '#pspNotFoundTitleId'.
    """
    page = _get_page(context)
    logger.info("Waiting for PSP not found error page (#pspNotFoundTitleId)")
    page.locator("#pspNotFoundTitleId").wait_for(state="visible", timeout=15000)
    logger.info("PSP not found error page is displayed")


@then('the error title should contain "{expected_title}"')
def step_error_title_contains(context, expected_title):
    """
    Assert the PSP not found error title text.
    Selector: #pspNotFoundTitleId
    TypeScript expected: "Il metodo di pagamento selezionato non è disponibile"
    """
    page = _get_page(context)
    logger.info("Checking error title contains: '%s'", expected_title)
    title_elem = page.locator("#pspNotFoundTitleId")
    title_elem.wait_for(state="visible", timeout=5000)
    title_text = title_elem.inner_text()
    logger.info("Error title text: %s", title_text)
    assert expected_title in title_text, (
        f"Expected error title to contain '{expected_title}', but got: '{title_text}'"
    )


@then('the CTA button should contain "{expected_cta}"')
def step_cta_button_contains(context, expected_cta):
    """
    Assert the CTA button text and store the element in context for later click.
    Selector: #pspNotFoundCtaId
    TypeScript expected: "Scegli un altro metodo"
    NOTE: checked BEFORE description to match TypeScript assertion order.
    """
    page = _get_page(context)
    logger.info("Checking CTA button contains: '%s'", expected_cta)
    cta_elem = page.locator("#pspNotFoundCtaId")
    cta_elem.wait_for(state="visible", timeout=5000)
    cta_text = cta_elem.inner_text()
    logger.info("CTA button text: %s", cta_text)
    assert expected_cta in cta_text, (
        f"Expected CTA button to contain '{expected_cta}', but got: '{cta_text}'"
    )


@then('the error description should contain "{expected_description}"')
def step_error_description_contains(context, expected_description):
    """
    Assert the PSP not found error body/description text.
    Selector: #pspNotFoundBodyId
    TypeScript expected: "Può succedere quando l'importo da pagare è particolarmente elevato..."
    NOTE: checked AFTER CTA to match TypeScript assertion order.
    """
    page = _get_page(context)
    logger.info("Checking error description contains: '%s'", expected_description)
    body_elem = page.locator("#pspNotFoundBodyId")
    body_elem.wait_for(state="visible", timeout=5000)
    body_text = body_elem.inner_text()
    logger.info("Error description text: %s", body_text)
    assert expected_description in body_text, (
        f"Expected error description to contain '{expected_description}', but got: '{body_text}'"
    )


# ──────────────────────────────────────────────
# WHEN step — click CTA
# ──────────────────────────────────────────────

@when('I click the PSP not found CTA button')
def step_click_cta_button(context):
    """
    Click the CTA button (#pspNotFoundCtaId) to navigate to the payment method selection page.
    TypeScript: await pspNotFoundCtaElem.click()
    """
    page = _get_page(context)
    logger.info("Clicking PSP not found CTA button (#pspNotFoundCtaId)")
    _locate_and_click(page, "#pspNotFoundCtaId")
    logger.info("CTA button clicked")


# ──────────────────────────────────────────────
# THEN step — URL check
# ──────────────────────────────────────────────

@then('the current URL should contain "{expected_path}"')
def step_url_contains(context, expected_path):
    """
    Assert that the current page URL contains the expected path segment.
    TypeScript: expect(await page.evaluate(() => location.href)).toContain("/scegli-metodo")
    """
    page = _get_page(context)
    current_url = page.url
    logger.info("Current URL: %s — expecting to contain: '%s'", current_url, expected_path)
    assert expected_path in current_url, (
        f"Expected URL to contain '{expected_path}', but current URL is: '{current_url}'"
    )
