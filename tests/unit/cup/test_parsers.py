"""Unit tests for CUP SOAP response parsers."""

import xml.etree.ElementTree as ET

from src.integration.cup.utility.parsers import (
    get_pa_demand_payment_notice_fault_code,
    get_pa_demand_payment_notice_outcome,
    get_pa_demand_payment_notice_payment_option_description,
    get_pa_demand_payment_notice_remittance_information,
)


def _xml_root(xml_payload: str):
    """Parse an XML payload into an ElementTree root."""
    return ET.fromstring(xml_payload)


def test_get_fault_code_reads_value():
    """Return the faultCode value when present in the response payload."""
    xml_root = _xml_root("<Envelope><Body><faultCode>PAA_SYSTEM_ERROR</faultCode></Body></Envelope>")
    assert get_pa_demand_payment_notice_fault_code(xml_root) == "PAA_SYSTEM_ERROR"


def test_get_outcome_reads_value():
    """Return the outcome value when present in the response payload."""
    xml_root = _xml_root("<Envelope><Body><outcome>OK</outcome></Body></Envelope>")
    assert get_pa_demand_payment_notice_outcome(xml_root) == "OK"


def test_get_remittance_information_reads_value():
    """Return remittanceInformation from the SOAP response body."""
    xml_root = _xml_root("<Envelope><Body><remittanceInformation>REM-123</remittanceInformation></Body></Envelope>")
    assert get_pa_demand_payment_notice_remittance_information(xml_root) == "REM-123"


def test_get_payment_option_description_prefers_nested_option_value():
    """Prefer option/description over a generic top-level description."""
    xml_root = _xml_root(
        ""
        "<Envelope>"
        "  <Body>"
        "    <description>fallback</description>"
        "    <option><description>preferred</description></option>"
        "  </Body>"
        "</Envelope>"
    )
    assert get_pa_demand_payment_notice_payment_option_description(xml_root) == "preferred"


def test_get_payment_option_description_falls_back_to_generic_description():
    """Read a generic description when option/description is not available."""
    xml_root = _xml_root("<Envelope><Body><description>fallback</description></Body></Envelope>")
    assert get_pa_demand_payment_notice_payment_option_description(xml_root) == "fallback"


def test_parsers_return_none_on_missing_xml_root():
    """Return None when no SOAP XML root is provided."""
    assert get_pa_demand_payment_notice_fault_code(None) is None
    assert get_pa_demand_payment_notice_outcome(None) is None
    assert get_pa_demand_payment_notice_remittance_information(None) is None
    assert get_pa_demand_payment_notice_payment_option_description(None) is None