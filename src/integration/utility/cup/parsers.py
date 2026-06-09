import xml.etree.ElementTree as ET


def get_fault_code(xml_root) -> str | None:
    """Extract <faultCode> from a SOAP response XML root."""
    if xml_root is None:
        return None
    el = xml_root.find('.//faultCode')
    return el.text if el is not None else None


def get_outcome(xml_root) -> str | None:
    """Extract <outcome> from a SOAP response XML root (OK / KO)."""
    if xml_root is None:
        return None
    el = xml_root.find('.//outcome')
    return el.text if el is not None else None


def get_remittance_information(xml_root) -> str | None:
    """Extract <remittanceInformation> from a SOAP response XML root."""
    if xml_root is None:
        return None
    el = xml_root.find('.//remittanceInformation')
    return el.text if el is not None else None


def get_payment_option_description(xml_root) -> str | None:
    """Extract <description> nested under <option> in a SOAP response XML root."""
    if xml_root is None:
        return None
    # Try nested path first
    el = xml_root.find('.//option/description')
    if el is None:
        el = xml_root.find('.//description')
    return el.text if el is not None else None
