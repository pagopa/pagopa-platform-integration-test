import xml.etree.ElementTree as ET
import requests

from src.integration.utility.wisp.utils import obfuscate_secrets, remove_namespace


def send_soap_request(url: str, soap_action: str, body: str, description: str = None) -> tuple:
    """Send a SOAP request and return (status_code, xml_root_or_None, response_headers).

    Uses requests directly (no Allure dependency at this layer) so it can be
    used from unit tests without a behave context.
    """
    if description is None:
        description = url

    headers = {
        "Content-Type": "application/xml",
        "soapAction": soap_action,
    }

    response = requests.post(url, headers=headers, data=body.encode("utf-8"), verify=False)

    xml_root = None
    if response.text:
        cleaned = remove_namespace(response.text)
        try:
            xml_root = ET.fromstring(cleaned)
        except ET.ParseError:
            xml_root = None

    return response.status_code, xml_root, response.headers
