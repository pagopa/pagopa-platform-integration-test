import os
import random
import logging
import json

logger = logging.getLogger(__name__)

def _get_page(context):
    if not hasattr(context, "page"):
        raise RuntimeError(
            "context.page non trovato. Inizializzalo in features/environment.py "
            "(es. Playwright page condivisa per scenario)."
        )
    return context.page

def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variabile ambiente obbligatoria non trovata: {name}")
    return value

def _get_required_json_env(name: str):
    """
    Read required env var and parse it as JSON.
    Raises RuntimeError with clear context if missing or invalid.
    """
    raw = _get_required_env(name)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Variabile ambiente '{name}' non contiene JSON valido: {exc}"
        ) from exc

def _generate_random_notice_code(notice_code_prefix: str) -> str:
    # Build inclusive range: <prefix>000... to <prefix>999...
    valid_range_end = int(str(notice_code_prefix) + "9999999999999")
    valid_range_start = int(str(notice_code_prefix) + "0000000000000")
    code = str(random.randint(valid_range_start, valid_range_end))
    logger.debug("Generated notice code with prefix %s: %s", notice_code_prefix, code)
    return code

def _perform_mock_login(page):
    logger.info("Performing mock login")

    logger.info("Waiting navigation state (networkidle)")
    page.wait_for_load_state("networkidle")

    logger.info("Waiting for visible button")
    page.wait_for_selector("button")

    logger.info("Searching AccountCircleRoundIcon")
    icon = page.query_selector("[data-testid='AccountCircleRoundedIcon']")

    assert icon is not None, "Icon 'AccountCircleRoundedIcon' non trovato"
    logger.info("Login successful")

def _locate_and_click(page, locator, click_count=1, timeout=5000):
    to_click = page.locator(locator)
    to_click.wait_for(state="visible", timeout=timeout)
    to_click.click(click_count=click_count)