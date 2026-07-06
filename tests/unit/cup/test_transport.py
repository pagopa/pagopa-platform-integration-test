"""Unit tests for CUP SOAP transport delegation."""

from src.integration.cup.utility.transport import send_soap_request


def test_send_soap_request_delegates_to_common_raw_helper(monkeypatch):
    """Ensure CUP transport delegates SOAP raw calls to the shared utility."""
    captured = {}
    expected_response = (200, object(), {"x-trace": "abc"})

    def fake_send_raw_soap_request(service_config, soap_action, body, auth_config=None):
        """Capture invocation arguments and return a canned response."""
        captured["service_config"] = service_config
        captured["soap_action"] = soap_action
        captured["body"] = body
        captured["auth_config"] = auth_config
        return expected_response

    monkeypatch.setattr(
        "src.integration.cup.utility.transport.send_raw_soap_request",
        fake_send_raw_soap_request,
    )

    result = send_soap_request(
        url="https://example.test/cup",
        soap_action="paDemandPaymentNotice",
        body="<Envelope />",
        description="ignored",
    )

    assert result == expected_response
    assert captured["service_config"] == {
        "url": "https://example.test/cup",
        "verify_ssl": False,
    }
    assert captured["soap_action"] == "paDemandPaymentNotice"
    assert captured["body"] == "<Envelope />"
    assert captured["auth_config"] is None