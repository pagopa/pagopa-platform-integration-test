import time

import pytest
from playwright.sync_api import sync_playwright

from src.conf.configuration import secrets

card_number = str(secrets.card_number)

@pytest.fixture(scope='session')
def playwright_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(playwright_browser):
    page = playwright_browser.new_page()
    yield page
    page.close()


def test_rtp_form_submission(page):
    page_url = 'https://api.uat.platform.pagopa.it/ecommerce/checkout/v1/carts/xxx/redirect?clientId=CHECKOUT_CART'
    page.goto(page_url)

    page.wait_for_selector('#confirmEmail')
    page.click('#confirmEmail')
    page.type('#confirmEmail', 'test@test.it')

    page.wait_for_selector('#paymentEmailPageButtonContinue')
    page.click('#paymentEmailPageButtonContinue')

    page.get_by_text('Carta di credito o debito').click()

    time.sleep(5)

    page.frame_locator('#frame_CARD_NUMBER').get_by_placeholder('0000 0000 0000').fill(card_number)

    time.sleep(10000)
