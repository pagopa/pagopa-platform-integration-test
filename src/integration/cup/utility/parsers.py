from src.utility.soap.soap_raw_client import get_raw_soap_text


def get_pa_demand_payment_notice_fault_code(xml_root) -> str | None:
    """Extract <faultCode> from a paDemandPaymentNotice SOAP response XML root."""
    return get_raw_soap_text(xml_root, "faultCode")


def get_pa_demand_payment_notice_outcome(xml_root) -> str | None:
    """Extract <outcome> from a paDemandPaymentNotice SOAP response XML root (OK / KO)."""
    return get_raw_soap_text(xml_root, "outcome")


def get_pa_demand_payment_notice_remittance_information(xml_root) -> str | None:
    """Extract <remittanceInformation> from a paDemandPaymentNotice SOAP response XML root."""
    return get_raw_soap_text(xml_root, "remittanceInformation")


def get_pa_demand_payment_notice_payment_option_description(xml_root) -> str | None:
    """Extract payment option description from a paDemandPaymentNotice SOAP response XML root."""
    # Try nested path first.
    nested_description = get_raw_soap_text(xml_root, "option/description")
    if nested_description is not None:
        return nested_description

    return get_raw_soap_text(xml_root, "description")
