import constants as const
from src.conf.configuration import secrets


# The method permits to retrieve the SOAP URL starting from request primitive
def get_primitive_url(context, primitive):
    services = context.config.userdata.get("h")
    match primitive.lower():
        case "nodoinviarpt":
            service_data = services.get("nodo-per-pa")
            return service_data['url'], service_data['subscription_key'], const.ResponseType.XML
        case "nodoinviacarrellorpt":
            service_data = services.get("nodo-per-pa")
            return service_data['url'], service_data['subscription_key'], const.ResponseType.XML
        case "checkposition":
            service_data = services.get("nodo-per-pm-v1")
            url = service_data['url'] + "/checkPosition"
            return url, service_data['subscription_key'], const.ResponseType.JSON
        case "activatepaymentnoticev2":
            service_data = services.get("node-for-psp")
            return service_data['url'], service_data['subscription_key'], const.ResponseType.XML
        case "closepaymentv2":
            service_data = services.get("nodo-per-pm-v2")
            url = service_data['url'] + "/closepayment"
            return url, service_data['subscription_key'], const.ResponseType.JSON
        case "sendpaymentoutcomev2":
            service_data = services.get("node-for-psp")
            return service_data['url'], service_data['subscription_key'], const.ResponseType.XML


# The method permits to retrieve the REST URL starting from action
def get_rest_url(context, action):
    services = context.config.userdata.get("services")
    match action.lower():

        case "redirect":
            # service_data = services.get("wisp-converter")
            service_data = context.settings.services.wisp_converter
            # return service_data['url'] + "/payments?idSession=", ""
            return service_data.url + "/payments?idSession=", ""

        case "search_in_re_by_iuv":
            # service_data = services.get("technical-support")
            service_data = context.settings.services.technical_support
            # url = service_data['url'] + "/organizations/{creditor_institution}/iuv/{iuv}?dateFrom={date_from}&dateTo={date_to}"
            url = service_data.url + "/organizations/{creditor_institution}/iuv/{iuv}?dateFrom={date_from}&dateTo={date_to}"
            return url, context.secrets.TECHNICAL_SUPPORT_SUBSCRIPTION_KEY

        case "get_paymentposition_by_iuv":
            # service_data = services.get("gpd-core")
            service_data = context.settings.services.gpd_core
            # url = service_data['url'] + "/organizations/{creditor_institution}/paymentoptions/{iuv}/debtposition"
            url = service_data.url + "/organizations/{creditor_institution}/paymentoptions/{iuv}/debtposition"
            return url, context.secrets.GPD_SUBSCRIPTION_KEY

        case "create_paymentposition_and_publish":
            # service_data = services.get("gpd-core")
            service_data = context.settings.services.gpd_core
            # url = service_data['url'] + "/organizations/{creditor_institution}/debtpositions?toPublish=true"
            url = service_data.url + "/organizations/{creditor_institution}/debtpositions?toPublish=true"
            return url, context.secrets.GPD_SUBSCRIPTION_KEY

        case "create_paymentposition":
            # service_data = services.get("gpd-core")
            service_data = context.settings.services.gpd_core

            # url = service_data['url'] + "/organizations/{creditor_institution}/debtpositions?toPublish=false"
            url = service_data.url + "/organizations/{creditor_institution}/debtpositions?toPublish=false"
            return url, context.secrets.GPD_SUBSCRIPTION_KEY