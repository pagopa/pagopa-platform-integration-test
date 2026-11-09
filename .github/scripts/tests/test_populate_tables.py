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
