from src.utility.soap.soap_raw_client import send_raw_soap_request


def send_soap_request(url: str, soap_action: str, body: str, description: str = None) -> tuple:
    """Send a SOAP request and return (status_code, xml_root_or_None, response_headers).

    Uses the common zeep-based raw SOAP utility for consistency across suites.
    The ``description`` argument is kept for backward compatibility.
    """
    service_config = {
        "url": url,
        "verify_ssl": False,
    }

    return send_raw_soap_request(
        service_config=service_config,
        soap_action=soap_action,
        body=body,
        auth_config=None,
    )
