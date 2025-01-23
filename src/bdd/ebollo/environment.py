import logging

from behave import fixture
from behave import use_fixture
from playwright.sync_api import sync_playwright

from src.conf.configuration import commondata
from src.conf.configuration import secrets
from src.conf.configuration import settings


def before_all(context):
    # load settings and secrets into context
    context.settings = settings
    context.secrets = secrets
    context.commondata = commondata

    # configure logging setup
    logging.basicConfig(level=logging.DEBUG)
    use_fixture(playwright_browser_with_page, context)


@fixture
def playwright_browser_with_page(context):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context.page = browser.new_page()
        yield context.page
        context.page.close()
        browser.close()
