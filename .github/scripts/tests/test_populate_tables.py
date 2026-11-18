"""Unit tests for the run-URL helper of populate_tables.py."""
import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "populate_tables.py"


@pytest.fixture(scope="module")
def populate_tables():
    """Load populate_tables.py as a module without executing its main()."""
    spec = importlib.util.spec_from_file_location("populate_tables", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["populate_tables"] = module
    spec.loader.exec_module(module)
    return module


def test_gha_run_url_is_built_from_github_variables(populate_tables, monkeypatch):
    """The run URL combines server, repository and run id."""
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    monkeypatch.setenv("GITHUB_REPOSITORY", "pagopa/pagopa-platform-integration-test")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    assert (
        populate_tables.get_gha_run_url()
        == "https://github.com/pagopa/pagopa-platform-integration-test/actions/runs/123"
    )


@pytest.mark.parametrize("missing", ["GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"])
def test_gha_run_url_is_none_when_a_variable_is_missing(populate_tables, monkeypatch, missing):
    """Outside GitHub Actions no URL is produced."""
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    monkeypatch.setenv("GITHUB_REPOSITORY", "org/repo")
    monkeypatch.setenv("GITHUB_RUN_ID", "1")
    monkeypatch.delenv(missing)
    assert populate_tables.get_gha_run_url() is None


# ---------------------------------------------------------------- product version lookup


class _Response:
    """Minimal stand-in for requests.Response."""

    def __init__(self, status_code=200, payload=None, text=""):
        """Store the status code, JSON payload and raw text."""
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        """Return the configured JSON payload."""
        return self._payload


CONFIG = {
    "qa_hub_apis": {
        "product_version": {
            "url": "https://hub.example/releases/versions",
            "method": "GET",
            "api_key": "k",
        },
        "latest_suite_version": {"url": "https://hub.example/latest", "method": "GET"},
        "save_test_suite": {"url": "https://hub.example/suites", "method": "POST"},
    }
}


@pytest.mark.parametrize(
    "raw, expected",
    [("1.2.3", "1.2.3"), ("v1.2.3", "1.2.3"), ("V1.2.3", "1.2.3"), ("Release 1.2.3", "1.2.3"),
     ("  Release v1.2.3 ", "1.2.3")],
)
def test_normalize_product_version(populate_tables, raw, expected):
    """Prefixes and whitespace are removed so versions compare consistently."""
    assert populate_tables.normalize_product_version(raw) == expected


def test_current_version_is_read_from_the_hub(populate_tables, monkeypatch):
    """The version is requested by product key and uppercase environment, then normalized."""
    calls = []

    def fake_request(**kwargs):
        calls.append(kwargs)
        return _Response(200, {"version": "v0.11.3", "read_status": "OK"})

    monkeypatch.setattr(populate_tables.requests, "request", fake_request)
    assert populate_tables.get_current_product_version("fdrfase3", "uat", CONFIG) == "0.11.3"
    assert calls[0]["params"] == {"product_key": "fdrfase3", "env": "UAT"}
    assert calls[0]["headers"] == {"Ocp-Apim-Subscription-Key": "k"}
    assert calls[0]["timeout"]


def test_current_version_keeps_last_good_value_when_the_last_read_failed(
    populate_tables, monkeypatch
):
    """An ERROR read still carries the last good version, which is used."""
    monkeypatch.setattr(
        populate_tables.requests, "request",
        lambda **_: _Response(200, {"version": "1.0.0", "read_status": "ERROR"}),
    )
    assert populate_tables.get_current_product_version("a", "DEV", CONFIG) == "1.0.0"


def test_current_version_is_none_without_product_key(populate_tables, monkeypatch):
    """No key means unknown, without calling the hub."""
    monkeypatch.setattr(
        populate_tables.requests, "request",
        lambda **_: pytest.fail("the hub must not be called"),
    )
    assert populate_tables.get_current_product_version(None, "DEV", CONFIG) is None


@pytest.mark.parametrize(
    "response",
    [_Response(404, text="nope"), _Response(500, text="boom"),
     _Response(200, {"version": None, "read_status": "NO_VERSION"}),
     _Response(200, ["not", "a", "dict"])],
)
def test_current_version_is_none_when_the_hub_has_no_usable_version(
    populate_tables, monkeypatch, response
):
    """Missing app, hub errors and empty readings are reported as unknown, never as a default."""
    monkeypatch.setattr(populate_tables.requests, "request", lambda **_: response)
    assert populate_tables.get_current_product_version("a", "DEV", CONFIG) is None


def test_current_version_is_none_on_network_error(populate_tables, monkeypatch):
    """A transport failure does not break the ingestion: the version is unknown."""
    def boom(**_):
        raise populate_tables.requests.exceptions.ConnectionError("down")

    monkeypatch.setattr(populate_tables.requests, "request", boom)
    assert populate_tables.get_current_product_version("a", "DEV", CONFIG) is None


def test_current_version_requires_the_endpoint_configuration(populate_tables):
    """A missing endpoint is a configuration error, not an unknown version."""
    with pytest.raises(ValueError, match="product_version"):
        populate_tables.get_current_product_version("a", "DEV", {"qa_hub_apis": {}})


def test_latest_suite_lookup_sends_optional_filters_only_when_given(populate_tables, monkeypatch):
    """Exact lookups add version and type; the legacy call keeps only the test object."""
    calls = []

    def fake_request(**kwargs):
        calls.append(kwargs["params"])
        return _Response(404)

    monkeypatch.setattr(populate_tables.requests, "request", fake_request)
    assert populate_tables.get_latest_saved_suite_version("x", CONFIG) is None
    assert populate_tables.get_latest_saved_suite_version("x", CONFIG, "1.0.0", "e2e") is None
    assert calls == [
        {"test_object": "x"},
        {"test_object": "x", "test_object_version": "1.0.0", "test_type": "e2e"},
    ]


def test_latest_suite_lookup_fails_on_unexpected_status(populate_tables, monkeypatch):
    """A server error is raised instead of being parsed as a suite."""
    monkeypatch.setattr(
        populate_tables.requests, "request", lambda **_: _Response(500, text="boom")
    )
    with pytest.raises(Exception, match="500"):
        populate_tables.get_latest_saved_suite_version("x", CONFIG)


def _suite(populate_tables, version="", test_type="integration"):
    """Build a Test_suites object for the decision tests."""
    return populate_tables.Test_suites(
        test_object="x", test_type=test_type, test_object_version=version
    )


def test_known_version_reuses_the_exact_suite(populate_tables, monkeypatch):
    """When the exact version is already saved no suite is created."""
    saved = _suite(populate_tables, "0.10.0")
    monkeypatch.setattr(
        populate_tables, "get_latest_saved_suite_version", lambda *a, **k: saved
    )
    monkeypatch.setattr(
        populate_tables, "save_test_suite", lambda *a, **k: pytest.fail("must not save")
    )
    result = populate_tables.ensure_suite_version(_suite(populate_tables), "0.10.0", CONFIG)
    assert result is saved


def test_known_version_looks_up_exactly_and_creates_when_missing(populate_tables, monkeypatch):
    """A version not saved yet creates a suite; the lookup is exact on version and type."""
    lookups = []

    def fake_lookup(test_object, config, version=None, test_type=None):
        lookups.append((test_object, version, test_type))
        return None

    saved = []
    monkeypatch.setattr(populate_tables, "get_latest_saved_suite_version", fake_lookup)
    monkeypatch.setattr(
        populate_tables, "save_test_suite", lambda suite, config: saved.append(suite) or suite
    )
    populate_tables.ensure_suite_version(_suite(populate_tables), "0.9.0", CONFIG)
    assert lookups == [("x", "0.9.0", "integration")]
    assert [s.test_object_version for s in saved] == ["0.9.0"]


def test_unknown_version_reuses_the_latest_saved_suite(populate_tables, monkeypatch):
    """Without a version the latest saved suite is reused, so nothing is created."""
    saved = _suite(populate_tables, "1.4.0")
    monkeypatch.setattr(
        populate_tables, "get_latest_saved_suite_version", lambda *a, **k: saved
    )
    monkeypatch.setattr(
        populate_tables, "save_test_suite", lambda *a, **k: pytest.fail("must not save")
    )
    assert populate_tables.ensure_suite_version(_suite(populate_tables), None, CONFIG) is saved


def test_unknown_version_without_saved_suite_creates_an_unknown_one(populate_tables, monkeypatch):
    """With no version and no suite a placeholder suite is created."""
    created = []
    monkeypatch.setattr(populate_tables, "get_latest_saved_suite_version", lambda *a, **k: None)
    monkeypatch.setattr(
        populate_tables, "save_test_suite", lambda suite, config: created.append(suite) or suite
    )
    populate_tables.ensure_suite_version(_suite(populate_tables), None, CONFIG)
    assert [s.test_object_version for s in created] == [populate_tables.UNKNOWN_SUITE_VERSION]
