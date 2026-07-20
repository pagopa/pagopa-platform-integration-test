"""Unit tests for the zeep-based raw SOAP common utility."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from src.utility.soap.soap_client import SoapClientError
from src.utility.soap.soap_raw_client import get_raw_soap_text, send_raw_soap_request


class FakeResponse:
    """Simple response object compatible with the raw SOAP utility expectations."""

    def __init__(self, status_code: int, text: str, headers: Dict[str, Any]):
        """Store status, text and headers used by tests."""
        self.status_code = status_code
        self.text = text
        self.headers = headers


class FakeTransport:
    """Captures zeep transport calls and returns a configurable fake response."""

    def __init__(self, response: FakeResponse, capture: Dict[str, Any]):
        """Build a fake transport with response and capture dictionary."""
        self._response = response
        self._capture = capture

    def post_xml(self, address: str, envelope: Any, headers: Dict[str, str]) -> FakeResponse:
        """Capture posted SOAP details and return the configured response."""
        self._capture["address"] = address
        self._capture["envelope_tag"] = getattr(envelope, "tag", "")
        self._capture["headers"] = headers
        return self._response


def test_get_raw_soap_text_returns_none_when_root_is_missing():
    """Return None if the XML root is missing."""
    assert get_raw_soap_text(None, "outcome") is None


def test_send_raw_soap_request_requires_url_in_service_config():
    """Raise SoapClientError when URL is missing from service configuration."""
    with pytest.raises(SoapClientError, match="Missing required configuration value: 'url'"):
        send_raw_soap_request(
            service_config={},
            soap_action="paDemandPaymentNotice",
            body="<Envelope />",
        )


def test_send_raw_soap_request_raises_for_invalid_xml_payload():
    """Raise SoapClientError when body is not valid XML."""
    with pytest.raises(SoapClientError, match="Invalid SOAP XML payload"):
        send_raw_soap_request(
            service_config={"url": "https://example.test/cup"},
            soap_action="paDemandPaymentNotice",
            body="<Envelope>",
        )


def test_send_raw_soap_request_posts_with_zeep_transport_and_parses_response(monkeypatch):
    """Send SOAP envelope via zeep transport and parse namespaced response tags."""
    capture: Dict[str, Any] = {}
    response_xml = (
        "<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'>"
        "  <soapenv:Body>"
        "    <ns2:paDemandPaymentNoticeRes xmlns:ns2='http://pagopa-api.pagopa.gov.it/pa/paForNode.xsd'>"
        "      <outcome>OK</outcome>"
        "    </ns2:paDemandPaymentNoticeRes>"
        "  </soapenv:Body>"
        "</soapenv:Envelope>"
    )
    fake_response = FakeResponse(status_code=200, text=response_xml, headers={"x-correlation-id": "abc"})
    fake_transport = FakeTransport(response=fake_response, capture=capture)

    def fake_build_transport(service_config, auth_config):
        """Return a fake transport and capture factory invocation arguments."""
        capture["service_config"] = service_config
        capture["auth_config"] = auth_config
        return fake_transport

    monkeypatch.setattr(
        "src.utility.soap.soap_raw_client._build_transport",
        fake_build_transport,
    )

    status_code, xml_root, headers = send_raw_soap_request(
        service_config={
            "url": "https://example.test/cup",
            "raw_headers": {"X-Test": "1"},
        },
        soap_action="paDemandPaymentNotice",
        body="<Envelope><Body /></Envelope>",
        auth_config=None,
    )

    assert status_code == 200
    assert capture["address"] == "https://example.test/cup"
    assert "Envelope" in capture["envelope_tag"]
    assert capture["headers"]["soapAction"] == "paDemandPaymentNotice"
    assert capture["headers"]["X-Test"] == "1"
    assert headers["x-correlation-id"] == "abc"
    assert get_raw_soap_text(xml_root, "outcome") == "OK"