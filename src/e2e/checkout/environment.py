import os
import sys
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

# Behave puo' eseguire questo file con cwd locale; garantiamo l'import di `src.*`.
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CHECKOUT_ROOT = Path(__file__).resolve().parent
if str(CHECKOUT_ROOT) not in sys.path:
    sys.path.insert(0, str(CHECKOUT_ROOT))

from src.utility.config.config_loader import _parse_config_content

def _resolve_config_file(config_file: str) -> Path:
    candidate = Path(config_file)
    if candidate.is_file():
        return candidate

    local_candidate = Path(__file__).resolve().parent / config_file
    if local_candidate.is_file():
        return local_candidate

    raise RuntimeError(f"File config non trovato: {config_file}")


def _load_test_config(config_file: str) -> dict:
    path = _resolve_config_file(config_file)
    raw_content = path.read_text(encoding="utf-8")
    return _parse_config_content(raw_content, path)

def before_all(context):
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        force=True)
    # Opzionale: carica un file config passando ENV_FILE (es. .\dev.env)
    config_file = os.getenv("ENV_FILE")
    context.test_config = _load_test_config(config_file) if config_file else {}

    timeout_raw = context.test_config.get("E2E_TIMEOUT_MS", os.getenv("E2E_TIMEOUT_MS", "80000"))
    context.timeout_ms = int(timeout_raw)

    context._playwright = sync_playwright().start()
    headless_raw = str(context.test_config.get("HEADLESS", os.getenv("HEADLESS", "true"))).lower()
    headless = headless_raw in {"1", "true", "yes", "on"}
    context.browser = context._playwright.chromium.launch(
        channel="chrome",
        headless=headless,
        args=["--no-sandbox"],
    )


def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context(
        viewport={"width": 1200, "height": 907}
    )
    context.page = context.browser_context.new_page()
    context.page.set_default_timeout(context.timeout_ms)
    context.page.set_default_navigation_timeout(context.timeout_ms)

def after_scenario(context, scenario):
    if hasattr(context, "browser_context"):
        context.browser_context.close()


def after_all(context):
    if hasattr(context, "browser"):
        context.browser.close()
    if hasattr(context, "_playwright"):
        context._playwright.stop()