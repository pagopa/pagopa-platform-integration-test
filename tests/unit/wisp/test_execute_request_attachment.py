"""Unit tests for the response attachments written by the WISP `execute_request` helper."""

import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".github" / "scripts"))

from build_ai_prompt import parse_response_attachment
from src.integration.wisp.utility import constants, utils

URL = "https://api.uat.platform.pagopa.it/nodo/node-for-psp/v1"


class _FakeResponse:
    """Minimal stand-in for `requests.Response` used by `execute_request`."""

    def __init__(self, status_code: int, text: str, json_body=None) -> None:
        """Store the status, the raw text and an optional JSON payload."""
        self.status_code = status_code
        self.text = text
        self.headers = {}
        self._json_body = json_body

    def json(self):
        """Return the JSON payload or fail like `requests` does for a non-JSON body."""
        if self._json_body is None:
            raise ValueError("not json")
        return self._json_body


@pytest.fixture
def attachments(monkeypatch):
    """Capture Allure attachments created by `execute_request`."""
    captured = []
    monkeypatch.setattr(utils, "attach", lambda body, name=None, attachment_type=None: captured.append((name, body)))
    return captured


def _respond_with(monkeypatch, response: _FakeResponse) -> None:
    """Make every HTTP call of `execute_request` return `response`."""
    monkeypatch.setattr(utils.requests, "request", lambda **kwargs: response)


def test_xml_response_attachment_carries_the_http_status(monkeypatch, attachments) -> None:
    """A SOAP answer is attached with URL and HTTP status and parsed as before."""
    soap_ko = "<Envelope><Body><r><outcome>KO</outcome><fault><faultCode>PPT_X</faultCode></fault></r></Body></Envelope>"
    _respond_with(monkeypatch, _FakeResponse(200, soap_ko))

    status, body, _ = utils.execute_request(URL, "post", {}, "<req/>", constants.ResponseType.XML, description="step")

    assert status == 200
    assert isinstance(body, ElementTree.Element)
    received = [text for name, text in attachments if name == "step - Received response"]
    assert received == [f"URL: {URL}\nHTTP status: 200\nResponse:\n{soap_ko}"]
    evidence = parse_response_attachment(received[0])
    assert evidence["http_status"] == 200
    assert "faultCode=PPT_X" in evidence["detail"]


def test_non_xml_error_body_is_attached_before_the_parser_fails(monkeypatch, attachments) -> None:
    """An APIM JSON 500 for a SOAP call keeps its body and status in the report despite the ParseError."""
    apim = '{ "statusCode": 500, "message": "Internal server error", "activityId": "c42b" }'
    _respond_with(monkeypatch, _FakeResponse(500, apim))

    with pytest.raises(AssertionError, match="HTTP status: 500.*activityId"):
        utils.execute_request(URL, "post", {}, "<req/>", constants.ResponseType.XML, description="step")

    received = [text for name, text in attachments if name == "step - Received response"]
    assert received and "HTTP status: 500" in received[0]
    evidence = parse_response_attachment(received[0])
    assert evidence["http_status"] == 500
    assert "activityId" in evidence["detail"]


def test_empty_error_body_is_attached_but_empty_success_is_not(monkeypatch, attachments) -> None:
    """An empty 5xx body is evidence; an empty 2xx body and health checks stay unattached."""
    _respond_with(monkeypatch, _FakeResponse(502, ""))
    status, body, _ = utils.execute_request(URL, "get", {}, None, constants.ResponseType.JSON, description="step")
    assert (status, body) == (502, None)
    assert attachments == [("step - Received response", f"URL: {URL}\nHTTP status: 502\nResponse:\n<empty body>")]
    assert parse_response_attachment(attachments[0][1])["http_status"] == 502

    attachments.clear()
    _respond_with(monkeypatch, _FakeResponse(200, ""))
    utils.execute_request(URL, "get", {}, None, constants.ResponseType.JSON, description="step")
    _respond_with(monkeypatch, _FakeResponse(503, ""))
    utils.execute_request(URL + "/info", "get", {}, None, constants.ResponseType.JSON, description="step")
    assert attachments == []


def test_secrets_are_still_obfuscated_with_the_new_header(monkeypatch, attachments) -> None:
    """The status header does not bypass the password obfuscation applied to attachments."""
    _respond_with(monkeypatch, _FakeResponse(200, "<r><password>topsecret</password></r>"))

    utils.execute_request(URL, "post", {}, None, constants.ResponseType.XML, description="step")

    assert "topsecret" not in attachments[0][1]
    assert "<password>***</password>" in attachments[0][1]
