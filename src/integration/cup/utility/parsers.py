import re
import xml.etree.ElementTree as ET

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


def get_pa_demand_payment_notice_qr_code_fiscal_code(xml_root) -> str | None:
    """Extract <fiscalCode> from <qrCode> in a paDemandPaymentNotice SOAP response XML root."""
    return get_raw_soap_text(xml_root, "qrCode/fiscalCode")


def get_pa_demand_payment_notice_notice_number(xml_root) -> str | None:
    """Extract <noticeNumber> from <qrCode> in a paDemandPaymentNotice SOAP response XML root."""
    return get_raw_soap_text(xml_root, "qrCode/noticeNumber")


def get_pa_demand_payment_notice_amount(xml_root) -> str | None:
    """Extract <amount> from paymentList/paymentOptionDescription in response XML."""
    return get_raw_soap_text(xml_root, "paymentList/paymentOptionDescription/amount")


def get_pa_demand_payment_notice_options(xml_root) -> str | None:
    """Extract <options> from paymentList/paymentOptionDescription in response XML."""
    return get_raw_soap_text(xml_root, "paymentList/paymentOptionDescription/options")


def get_pa_demand_payment_notice_payment_note(xml_root) -> str | None:
    """Extract <paymentNote> from paymentList/paymentOptionDescription in response XML."""
    return get_raw_soap_text(xml_root, "paymentList/paymentOptionDescription/paymentNote")


def get_pa_demand_payment_notice_payment_description(xml_root) -> str | None:
    """Extract <paymentDescription> from a paDemandPaymentNotice response XML root."""
    return get_raw_soap_text(xml_root, "paymentDescription")


def get_pa_demand_payment_notice_fiscal_code_pa(xml_root) -> str | None:
    """Extract <fiscalCodePA> from a paDemandPaymentNotice response XML root."""
    return get_raw_soap_text(xml_root, "fiscalCodePA")


def get_pa_demand_payment_notice_company_name(xml_root) -> str | None:
    """Extract <companyName> from a paDemandPaymentNotice response XML root."""
    return get_raw_soap_text(xml_root, "companyName")


def get_pa_demand_payment_notice_request_debtor_fiscal_code(xml_body: str) -> str | None:
    """Extract <debtorFiscalCode> from a paDemandPaymentNotice SOAP request XML body."""
    if not xml_body:
        return None

    try:
        xml_root = ET.fromstring(xml_body)
    except ET.ParseError:
        return None

    for element in xml_root.iter():
        tag_name = element.tag.rsplit('}', 1)[-1]
        if tag_name == "debtorFiscalCode":
            if element.text is None:
                return None
            value = element.text.strip()
            return value if value else None

    return None


def resolve_cup_pattern(
    pattern: str,
    iuv: str | None = None,
    debtor_fiscal_code: str | None = None,
    anno: str | None = None,
) -> str:
    """Replace CUP placeholders in a pattern string using runtime values.

    Supported placeholders are:
    - <IUV>
    - <CF_Debitore>
    - <anno> (resolved to the provided year, or to a 4-digit year regex fragment)
    """
    resolved_anno = re.escape(str(anno)) if anno not in (None, "") else r'\d{4}'
    substitutions = {
        '<IUV>': re.escape(str(iuv or '')),
        '<CF_Debitore>': re.escape(str(debtor_fiscal_code or '')),
        '<anno>': resolved_anno,
    }
    result = pattern
    for token, replacement in substitutions.items():
        result = result.replace(token, replacement)
    return result


def get_payment_option_transfer_remittance_values(payment_options) -> list[str]:
    """Collect remittanceInformation values from paymentOption[].transfer[]."""
    if not isinstance(payment_options, list):
        return []

    remittance_values = []
    for payment_option in payment_options:
        if not isinstance(payment_option, dict):
            continue
        transfers = payment_option.get("transfer", [])
        if not isinstance(transfers, list):
            continue
        for transfer in transfers:
            if not isinstance(transfer, dict):
                continue
            remittance_information = transfer.get("remittanceInformation")
            if remittance_information:
                remittance_values.append(str(remittance_information))

    return remittance_values


def get_payment_option_descriptions(payment_options) -> list[str]:
    """Collect description values from paymentOption[]."""
    if not isinstance(payment_options, list):
        return []

    descriptions = []
    for payment_option in payment_options:
        if not isinstance(payment_option, dict):
            continue
        description = payment_option.get("description")
        if description:
            descriptions.append(str(description))

    return descriptions
