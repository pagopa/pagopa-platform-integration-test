import re

from playwright.sync_api import expect


def mbd_checkout_payment(page, checkout_url, mbd_data, card_info):
    page.goto(checkout_url)

    page.wait_for_selector('#confirmEmail')
    page.click('#confirmEmail')
    page.type('#confirmEmail', mbd_data['paymentNotices'][0]['email'])

    page.wait_for_selector('#paymentEmailPageButtonContinue')
    page.click('#paymentEmailPageButtonContinue')

    page.get_by_text('Carta di credito o debito').click()

    page.frame_locator('#frame_CARD_NUMBER').get_by_placeholder('0000 0000 0000').fill(str(card_info.card_number))

    page.frame_locator('#frame_EXPIRATION_DATE').get_by_placeholder('MM/AA').fill(card_info.expiration_date)

    page.frame_locator('#frame_SECURITY_CODE').get_by_placeholder('123').fill(str(card_info.security_code))

    page.frame_locator('#frame_CARDHOLDER_NAME').get_by_placeholder('Nome riportato sulla carta').fill(
        'TestCardHolderName TestCardHolderSurname')

    page.get_by_role(role='button', name='Continue', exact=True).click()

    page.get_by_role(role='button', name=re.compile(r'^Pay')).click()

    page.get_by_role(role='button', name='Continue', exact=True).click(timeout=60000)

    expect(page).to_have_url(mbd_data['returnUrls']['successUrl'])
