import logging
import os

from behave import given

from src.integration.wisp.utility import constants
from src.integration.wisp.utility import utils


def _resolve_services(settings):
    """Resolve services config from root settings or the active TARGET_ENV section."""
    services = getattr(settings, 'services', None)
    if services:
        return services

    target_env = os.getenv('TARGET_ENV', 'uat')
    env_settings = settings.get(target_env) if hasattr(settings, 'get') else None
    if env_settings is not None:
        services = env_settings.get('services') if hasattr(env_settings, 'get') else None
        if services:
            return services

    raise AssertionError(f"services configuration not found for TARGET_ENV={target_env}")


@given('i sistemi sono operativi')
def system_up(context):
    """Check health endpoints for configured services and assert they are reachable."""
    responses = True
    services = _resolve_services(context.settings)

    for key, value in services.items():
        if 'healthcheck' in value:
            url = value.get('url') + value.get('healthcheck')
            logging.debug(f'[Health check] calling: {key} -> {url}')
            subscription_key = context.secrets.get(value.get('subscription_key'))
            headers = {'Content-Type': 'application/json'}
            if subscription_key is not None:
                headers[constants.OCP_APIM_SUBSCRIPTION_KEY] = subscription_key
            status_code, _, _ = utils.execute_request(url, 'get', headers, payload=None,
                                                      type=constants.ResponseType.JSON)
            logging.debug(f'[Health check] Received response: {status_code}')
            responses &= (status_code == 200)

    assert responses, f'health-check systems or subscription-key errors'
