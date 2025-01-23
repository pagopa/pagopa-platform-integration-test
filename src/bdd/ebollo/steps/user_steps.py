from src.conf.configuration import secrets
from src.utility.ebollo.api import post_mbd
from src.utility.ebollo.ui import mbd_checkout_payment
from src.utility.ebollo.utils import generate_mbd_payload


def user_pays_mbd_ok_checkout(context):
    payload = generate_mbd_payload()
    url = context.settings.services['mbd']['url'] + str(context.secrets.organization_id) + \
          context.settings.services['mbd']['path']
    res = post_mbd(url=url, api_key=context.secrets.MDB_SUBSCRIPTION_KEY, mbd_payload=payload)
    assert res.status_code == 200
    # assert res.status_code == 201
    mbd_checkout_payment(page=context.page, checkout_url=res.json()['checkoutRedirectUrl'], mbd_data=payload,
                         card_info=secrets.card_info)
