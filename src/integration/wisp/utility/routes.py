from . import constants as constants


# The method permits to retrieve the SOAP URL starting from request primitive
def get_primitive_url(context, primitive):
    services = context.config.userdata.get('h')
    match primitive.lower():
        case 'nodoinviarpt':
            return context.environment.services.nodo_per_pa.url, context.environment.NUOVA_CONNETTIVITA_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case 'nodoinviacarrellorpt':
            return context.environment.services.nodo_per_pa.url, context.environment.NUOVA_CONNETTIVITA_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case 'checkposition':
            url = context.environment.services.nodo_per_pm_v1.url + '/checkPosition'
            return url, context.environment.NODO_SUBSCRIPTION_KEY, constants.ResponseType.JSON
        case 'activatepaymentnoticev2':
            return context.environment.services.node_for_psp.url, context.environment.NODO_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case 'closepaymentv2':
            url = context.environment.services.nodo_per_pm_v2.url + '/closepayment'
            return url, context.environment.NODO_SUBSCRIPTION_KEY, constants.ResponseType.JSON
        case 'sendpaymentoutcomev2':
            service_data = services.get('node-for-psp')
            return service_data['url'], context.environment.TECHNICAL_SUPPORT_SUBSCRIPTION_KEY, constants.ResponseType.XML


# The method permits to retrieve the REST URL starting from action
def get_rest_url(context, action):
    match action.lower():

        case 'redirect':
            service_data = context.environment.services.wisp_converter
            return service_data.url + '/payments?idSession=', ''

        case 'search_in_re_by_iuv':
            service_data = context.environment.services.technical_support
            url = service_data.url + '/organizations/{creditor_institution}/iuv/{iuv}?dateFrom={date_from}&dateTo={date_to}'
            return url, context.environment.TECHNICAL_SUPPORT_SUBSCRIPTION_KEY

        case 'get_paymentposition_by_iuv':
            service_data = context.environment.services.gpd_core
            url = service_data.url + '/organizations/{creditor_institution}/paymentoptions/{iuv}/debtposition'
            return url, context.environment.GPD_SUBSCRIPTION_KEY

        case 'create_paymentposition_and_publish':
            service_data = context.environment.services.gpd_core
            url = service_data.url + '/organizations/{creditor_institution}/debtpositions?toPublish=true'
            return url, context.environment.GPD_SUBSCRIPTION_KEY

        case 'create_paymentposition':
            service_data = context.environment.services.gpd_core
            url = service_data.url + '/organizations/{creditor_institution}/debtpositions?toPublish=false'
            return url, context.environment.GPD_SUBSCRIPTION_KEY
