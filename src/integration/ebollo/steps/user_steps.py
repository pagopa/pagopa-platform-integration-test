from behave import when

from src.integration.ebollo.utility.api import post_mbd
from src.integration.ebollo.utility.ui import mbd_checkout_payment
from src.integration.ebollo.utility.utils import generate_mbd_payload


@when('the user pays the eBollo on the checkout page')
def user_pays_mbd_ok_checkout(context):
    """Create an MBD payment and complete checkout with test card data."""
    payload = generate_mbd_payload()
    url = context.settings.services['mbd']['url'] + str(context.secrets.organization_id) + \
          context.settings.services['mbd']['path']
    res = post_mbd(url=url, api_key=context.secrets.MDB_SUBSCRIPTION_KEY, mbd_payload=payload)
    assert res.status_code == 200
    # assert res.status_code == 201
    mbd_checkout_payment(page=context.page, checkout_url=res.json()['checkoutRedirectUrl'], mbd_data=payload,
                         card_info=context.secrets.card_info)
