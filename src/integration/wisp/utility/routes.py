import os

from . import constants as constants


def _resolve_services(context):
    """Resolve services from root settings or active TARGET_ENV section."""
    settings = context.settings
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


def _get_service(services, service_name):
    """Get a single service entry by name from Dynaconf object or dict."""
    if hasattr(services, service_name):
        return getattr(services, service_name)
    if hasattr(services, 'get'):
        return services.get(service_name)
    return None


def _get_service_url(service_data):
    """Extract service URL from Dynaconf object or dict service entry."""
    if hasattr(service_data, 'url'):
        return service_data.url
    if isinstance(service_data, dict):
        return service_data.get('url')
    return None


# The method permits to retrieve the SOAP URL starting from request primitive
def get_primitive_url(context, primitive):
    """Return URL, subscription key, and response type for SOAP primitives."""
    services_cfg = _resolve_services(context)
    services = context.config.userdata.get('h')
    match primitive.lower():
        case 'nodoinviarpt':
            service_data = _get_service(services_cfg, 'nodo_per_pa')
            return _get_service_url(service_data), context.secrets.NUOVA_CONNETTIVITA_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case 'nodoinviacarrellorpt':
            service_data = _get_service(services_cfg, 'nodo_per_pa')
            return _get_service_url(service_data), context.secrets.NUOVA_CONNETTIVITA_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case 'checkposition':
            service_data = _get_service(services_cfg, 'nodo_per_pm_v1')
            url = _get_service_url(service_data) + '/checkPosition'
            return url, context.secrets.NODO_SUBSCRIPTION_KEY, constants.ResponseType.JSON
        case 'activatepaymentnoticev2':
            service_data = _get_service(services_cfg, 'node_for_psp')
            return _get_service_url(service_data), context.secrets.NODO_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case 'closepaymentv2':
            service_data = _get_service(services_cfg, 'nodo_per_pm_v2')
            url = _get_service_url(service_data) + '/closepayment'
            return url, context.secrets.NODO_SUBSCRIPTION_KEY, constants.ResponseType.JSON
        case 'sendpaymentoutcomev2':
            service_data = services.get('node-for-psp')
            return service_data['url'], context.secrets.TECHNICAL_SUPPORT_SUBSCRIPTION_KEY, constants.ResponseType.XML


# The method permits to retrieve the REST URL starting from action
def get_rest_url(context, action):
    """Return URL and subscription key for REST actions used in WISP flows."""
    services_cfg = _resolve_services(context)
    match action.lower():

        case 'redirect':
            service_data = _get_service(services_cfg, 'wisp_converter')
            return _get_service_url(service_data) + '/payments?idSession=', ''

        case 'search_in_re_by_iuv':
            service_data = _get_service(services_cfg, 'technical_support')
            url = _get_service_url(service_data) + '/organizations/{creditor_institution}/iuv/{iuv}?dateFrom={date_from}&dateTo={date_to}'
            return url, context.secrets.TECHNICAL_SUPPORT_SUBSCRIPTION_KEY

        case 'get_paymentposition_by_iuv':
            service_data = _get_service(services_cfg, 'gpd_core')
            url = _get_service_url(service_data) + '/organizations/{creditor_institution}/paymentoptions/{iuv}/debtposition'
            return url, context.secrets.GPD_SUBSCRIPTION_KEY

        case 'create_paymentposition_and_publish':
            service_data = _get_service(services_cfg, 'gpd_core')
            url = _get_service_url(service_data) + '/organizations/{creditor_institution}/debtpositions?toPublish=true'
            return url, context.secrets.GPD_SUBSCRIPTION_KEY

        case 'create_paymentposition':
            service_data = _get_service(services_cfg, 'gpd_core')
            url = _get_service_url(service_data) + '/organizations/{creditor_institution}/debtpositions?toPublish=false'
            return url, context.secrets.GPD_SUBSCRIPTION_KEY
