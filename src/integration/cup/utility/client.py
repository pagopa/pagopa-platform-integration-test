import logging

from .constants import SOAP_ACTION_DEMAND_PAYMENT_NOTICE
from .transport import send_soap_request


def _build_client_from_service(service_config: dict) -> "CupClient":
    """Build a CUP client from suite service configuration."""
    soap_action = service_config.get('soap_action')
    if soap_action:
        return CupClient(url=service_config['url'], soap_action=soap_action)
    return CupClient(url=service_config['url'])


def send_demand_payment_notice(service_config: dict, xml_body: str, description: str = None) -> tuple:
    """Send paDemandPaymentNotice using service config and log raw response details."""
    cup_client = _build_client_from_service(service_config)
    status_code, response_body = cup_client.demand_payment_notice(
        xml_body=xml_body,
        description=description,
    )
    logging.debug('[demandPaymentNotice] status_code=%s | response_body=%s', status_code, response_body)
    return status_code, response_body


class CupClient:
    """HTTP client for the CUP paDemandPaymentNotice SOAP endpoint."""

    def __init__(self, url: str, soap_action: str = SOAP_ACTION_DEMAND_PAYMENT_NOTICE):
        self.url = url
        self.soap_action = soap_action

    def demand_payment_notice(self, xml_body: str, description: str = None) -> tuple:
        """Send a paDemandPaymentNotice request.

        Returns (status_code, xml_root_or_None).
        """
        status_code, xml_root, _ = send_soap_request(
            url=self.url,
            soap_action=self.soap_action,
            body=xml_body,
            description=description or "paDemandPaymentNotice",
        )
        return status_code, xml_root
