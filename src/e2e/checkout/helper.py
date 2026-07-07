import random
import logging
import json
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

def get_page(context):
    if not hasattr(context, "page"):
        raise RuntimeError(
            "context.page non trovato. Inizializzalo in features/environment.py "
            "(es. Playwright page condivisa per scenario)."
        )
    return context.page

def get_required_config(context, name: str):
    config = getattr(context, "test_config", None)
    if not isinstance(config, dict):
        raise RuntimeError("context.test_config non disponibile o non valido")

    value = config.get(name)
    if value is None:
        raise RuntimeError(f"Proprieta obbligatoria non trovata nel config: {name}")
    return value

def get_required_json_config(context, name: str):
    """
    Read required config value and parse it as JSON.
    Raises RuntimeError with clear context if missing or invalid.
    """
    raw = get_required_config(context, name)
    if not isinstance(raw, str):
        return raw
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Proprieta config '{name}' non contiene JSON valido: {exc}"
        ) from exc

def generate_random_notice_code(notice_code_prefix: str) -> str:
    # Build inclusive range: <prefix>000... to <prefix>999...
    valid_range_end = int(str(notice_code_prefix) + "9999999999999")
    valid_range_start = int(str(notice_code_prefix) + "0000000000000")
    code = str(random.randint(valid_range_start, valid_range_end))
    logger.debug("Generated notice code with prefix %s: %s", notice_code_prefix, code)
    return code

def perform_mock_login(page):
    logger.info("Performing mock login")

    logger.debug("Waiting navigation state (networkidle)")
    page.wait_for_load_state("networkidle")

    logger.debug("Waiting for visible button")
    page.wait_for_selector("button")

    logger.debug("Searching AccountCircleRoundIcon")
    icon = page.query_selector("[data-testid='AccountCircleRoundedIcon']")

    assert icon is not None, "Icon 'AccountCircleRoundedIcon' non trovato"
    logger.info("Login successful")

def locate_and_click(page, locator, click_count=1, timeout=5000):
    to_click = page.locator(locator)
    try:
        to_click.wait_for(state="visible", timeout=timeout)
        to_click.click(click_count=click_count)
    except PlaywrightTimeoutError as exc:
        current_url = ""
        try:
            current_url = page.url
        except Exception :
            current_url = "<unavailable>"

        logger.error("Timeout waiting for %s after %d ms at page %s", locator, timeout, current_url)
        raise RuntimeError(
            f"Timeout on locator '{locator}' after {timeout} ms (url: {current_url})"
        ) from exc

def locate_click_and_type(page, locator, text, click_count=1, timeout=5000):
    """Click a locator, clear it and type text."""
    target = page.locator(locator)
    locate_and_click(page, locator, click_count=click_count, timeout=timeout)
    try:
        target.fill("")
    except Exception:
        pass
    page.keyboard.type(str(text))
    logger.debug("Typed value into %s", locator)

