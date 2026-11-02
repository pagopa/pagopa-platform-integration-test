"""Unit tests for the XML value comparison of the WISP `check_field` step helper."""

from types import SimpleNamespace
from xml.etree import ElementTree

import pytest

from src.integration.wisp.utility import constants, steps_utils


@pytest.fixture
def attachments(monkeypatch):
    """Capture Allure attachments created by `check_field` and disable test skipping."""
    captured = []
    monkeypatch.setattr(steps_utils, "attach", lambda body, name=None, attachment_type=None: captured.append((name, body)))
    monkeypatch.setattr(steps_utils.session, "skip_tests", lambda context: False)
    monkeypatch.delenv(steps_utils.CHECK_FIELD_ENFORCE_ENV, raising=False)
    return captured


def _context(xml: str) -> SimpleNamespace:
    """Build a behave-like context holding a parsed XML response."""
    body = ElementTree.fromstring(xml)
    response = {"body": body, "content_type": constants.ResponseType.XML}
    return SimpleNamespace(flow_data={"action": {"response": response}})


def test_matching_value_does_not_attach(attachments) -> None:
    """An equal XML value passes silently."""
    steps_utils.check_field(_context("<r><outcome>OK</outcome></r>"), "outcome", "'OK'")
    assert attachments == []


def test_mismatch_is_only_attached_by_default(attachments) -> None:
    """Observation mode: a different value is attached but the step does not fail."""
    steps_utils.check_field(_context("<r><outcome>KO</outcome></r>"), "outcome", "'OK'")
    assert len(attachments) == 1
    assert "Current value: KO" in attachments[0][1]


def test_mismatch_fails_when_enforced(attachments, monkeypatch) -> None:
    """With the env switch on, the mismatch raises an AssertionError."""
    monkeypatch.setenv(steps_utils.CHECK_FIELD_ENFORCE_ENV, "true")
    with pytest.raises(AssertionError, match="Current value: KO"):
        steps_utils.check_field(_context("<r><outcome>KO</outcome></r>"), "outcome", "'OK'")


def test_missing_field_still_fails(attachments) -> None:
    """A missing XML field keeps failing regardless of the mode."""
    with pytest.raises(AssertionError):
        steps_utils.check_field(_context("<r/>"), "outcome", "'OK'")
