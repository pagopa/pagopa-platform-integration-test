import logging

from behave import given

from src.conf.configuration import secrets
from src.utility.wisp import constants
from src.utility.wisp import utils


@given('systems up')
def system_up(context):
    responses = True

    for key, value in context.settings.services.items():
        if 'healthcheck' in value:
            url = value.get('url') + value.get('healthcheck')
            logging.debug(f'[Health check] calling: {key} -> {url}')
            subscription_key = secrets.get(value.get('subscription_key'))
            headers = {'Content-Type': 'application/json'}
            if subscription_key is not None:
                headers[constants.OCP_APIM_SUBSCRIPTION_KEY] = subscription_key
            status_code, _, _ = utils.execute_request(url, 'get', headers, payload=None,
                                                      type=constants.ResponseType.JSON)
            logging.debug(f'[Health check] Received response: {status_code}')
            responses &= (status_code == 200)

    assert responses, f'health-check systems or subscription-key errors'
