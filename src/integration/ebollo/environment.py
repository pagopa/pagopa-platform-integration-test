import logging
import os

from behave import fixture
from behave import use_fixture
from playwright.sync_api import sync_playwright

from src.conf.configuration import load_commondata
from src.conf.configuration import load_secrets
from src.conf.configuration import load_settings
from src.utility.constants import INTEGRATION_ROOT


def before_all(context):
    """Initialize suite configuration, secrets, common data, and browser fixture."""
    # load settings and secrets into context
    suite_name = "ebollo"
    target_env = os.getenv("TARGET_ENV") or "uat"

    os.environ["TARGET_ENV"] = str(target_env)
    os.environ["suite"] = suite_name

    context.settings = load_settings(config_folder_root=INTEGRATION_ROOT)
    context.secrets = load_secrets(
        suite=suite_name,
        target_env=target_env,
        settings=context.settings,
    )
    context.commondata = load_commondata(config_folder_root=INTEGRATION_ROOT)

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)
    use_fixture(playwright_browser_with_page, context)


@fixture
def playwright_browser_with_page(context):
    """Create and tear down a Playwright browser page for the test run."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context.page = browser.new_page()
        yield context.page
        context.page.close()
        browser.close()
