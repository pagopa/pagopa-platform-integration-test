from .constants import SOAP_ACTION_DEMAND_PAYMENT_NOTICE
from .transport import send_soap_request


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
