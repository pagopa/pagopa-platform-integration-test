import src.utility.constants as constants
from enum import Enum
from src.conf.configuration import secrets


# The method permits to retrieve the SOAP URL starting from request primitive
def get_primitive_url(context, primitive):
    services = context.config.userdata.get("h")
    match primitive.lower():
        case "nodoinviarpt":
            return context.settings.services.nodo_per_pa.url, context.secrets.NUOVA_CONNETTIVITA_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case "nodoinviacarrellorpt":
            return context.settings.services.nodo_per_pa.url, context.secrets.NUOVA_CONNETTIVITA_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case "checkposition":
            url = context.settings.services.nodo_per_pm_v1.url + "/checkPosition"
            return url, context.secrets.NODO_SUBSCRIPTION_KEY, constants.ResponseType.JSON
        case "activatepaymentnoticev2":
            return context.settings.services.node_for_psp.url, context.secrets.NODO_SUBSCRIPTION_KEY, constants.ResponseType.XML
        case "closepaymentv2":
            url = context.settings.services.nodo_per_pm_v2.url + "/closepayment"
            return url, context.secrets.TEST_NODO_SUBSCRIPTION_KEY, constants.ResponseType.JSON
        case "sendpaymentoutcomev2":
            service_data = services.get("node-for-psp")
            return service_data['url'], context.secrets.TECHNICAL_SUPPORT_SUBSCRIPTION_KEY, constants.ResponseType.XML


# The method permits to retrieve the REST URL starting from action
def get_rest_url(context, action):
    # services = context.config.userdata.get("services")
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


# class ResponseType(Enum):
#     XML = 1
#     JSON = 2
#     HTML = 3
