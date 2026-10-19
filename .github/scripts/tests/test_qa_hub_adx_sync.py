"""Unit tests for the QA Hub PostgreSQL to ADX synchronization script."""

import importlib.util
import json
import sys
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "qa_hub_adx_sync.py"
_SPEC = importlib.util.spec_from_file_location("qa_hub_adx_sync", _SCRIPT_PATH)
sync = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = sync
_SPEC.loader.exec_module(sync)

TODAY = date(2026, 10, 15)


def _utc(year, month, day):
    """Return midnight UTC for the given day."""
    return datetime(year, month, day, tzinfo=timezone.utc)


def test_yesterday_window_covers_previous_utc_day():
    """Default mode selects the whole previous UTC day."""
    window = sync.compute_window("yesterday", None, None, TODAY)
    assert window == sync.SyncWindow(_utc(2026, 10, 14), _utc(2026, 10, 15))


def test_snapshot_window_is_unbounded():
    """Snapshot mode has no bounds."""
    assert sync.compute_window("snapshot", None, None, TODAY).is_snapshot


def test_since_window_has_open_end():
    """Since mode starts at from_date and has no upper bound."""
    window = sync.compute_window("since", date(2026, 9, 1), None, TODAY)
    assert window == sync.SyncWindow(_utc(2026, 9, 1), None)


def test_range_window_includes_to_date():
    """Range mode includes the whole to_date day."""
    window = sync.compute_window("range", date(2026, 9, 1), date(2026, 9, 30), TODAY)
    assert window == sync.SyncWindow(_utc(2026, 9, 1), _utc(2026, 10, 1))


@pytest.mark.parametrize(
    ("mode", "from_date", "to_date"),
    [
        ("since", None, None),
        ("range", date(2026, 9, 1), None),
        ("range", date(2026, 9, 2), date(2026, 9, 1)),
        ("since", date(2026, 10, 16), None),
        ("weekly", None, None),
    ],
)
def test_invalid_window_inputs_are_rejected(mode, from_date, to_date):
    """Missing, inverted, future, or unknown inputs raise ValueError."""
    with pytest.raises(ValueError):
        sync.compute_window(mode, from_date, to_date, TODAY)


def test_parse_iso_date_handles_blank_and_invalid_values():
    """Blank values are ignored and malformed dates are rejected."""
    assert sync.parse_iso_date("  ", "from_date") is None
    assert sync.parse_iso_date("2026-10-01", "from_date") == date(2026, 10, 1)
    with pytest.raises(ValueError):
        sync.parse_iso_date("01/10/2026", "from_date")


def test_to_libpq_url_converts_asyncpg_url():
    """The asyncpg driver suffix is removed and ssl becomes sslmode."""
    url = sync.to_libpq_url("postgresql+asyncpg://user:pwd@host:5432/qachub?ssl=require")
    assert url == "postgresql://user:pwd@host:5432/qachub?sslmode=require"


def test_to_libpq_url_rejects_other_schemes():
    """Only PostgreSQL URLs are accepted."""
    with pytest.raises(ValueError):
        sync.to_libpq_url("mysql://user:pwd@host/db")


@pytest.mark.parametrize(
    ("password", "expected_host_match", "expected_host_is_qachub"),
    [
        ("synthetic-password", True, False),
        ("synthetic%2Fpassword", True, False),
        ("synthetic/password", False, True),
    ],
)
def test_connection_diagnostics_do_not_log_credentials(
    password, expected_host_match, expected_host_is_qachub, monkeypatch, caplog
):
    """Compare parsed endpoints without exposing even malformed credentials."""
    monkeypatch.setenv("TARGET_ENV", "uat")
    host = "pagopa-u-itn-qa-flexible-postgresql.postgres.database.azure.com"
    url = sync.to_libpq_url(f"postgresql+asyncpg://qachub:{password}@{host}:5432/qachub?ssl=require")
    with caplog.at_level("INFO", logger=sync.LOGGER.name):
        sync.log_database_connection_diagnostics(url)
    assert f"host_matches_expected={expected_host_match}" in caplog.text
    assert f"host_is_qachub={expected_host_is_qachub}" in caplog.text
    assert password not in caplog.text
    assert url not in caplog.text
    assert "synthetic" not in caplog.text


def test_connection_diagnostics_sanitize_parser_errors(monkeypatch, caplog):
    """Invalid URL options cannot expose their secret-bearing parser error."""
    monkeypatch.setenv("TARGET_ENV", "uat")
    url = "postgresql://qachub:synthetic-password@host/qachub?synthetic-secret-option=private"
    with caplog.at_level("INFO", logger=sync.LOGGER.name):
        with pytest.raises(ValueError, match="Invalid PostgreSQL connection URL") as error:
            sync.log_database_connection_diagnostics(url)
    assert "synthetic" not in caplog.text + str(error.value)
    assert "libpq_parse=failed" in caplog.text


def test_export_logs_connection_diagnostics_before_connecting(monkeypatch, caplog, tmp_path):
    """The real connection path emits diagnostics before a connection failure."""
    monkeypatch.setenv("TARGET_ENV", "uat")
    host = "pagopa-u-itn-qa-flexible-postgresql.postgres.database.azure.com"
    with patch("psycopg.connect", side_effect=RuntimeError("connection probe")) as connect:
        with caplog.at_level("INFO", logger=sync.LOGGER.name):
            with pytest.raises(RuntimeError, match="connection probe"):
                sync.export_all(
                    f"postgresql+asyncpg://qachub:synthetic-password@{host}:5432/qachub?ssl=require",
                    sync.SyncWindow(),
                    tmp_path,
                )
    connect.assert_called_once()
    assert "host_matches_expected=True" in caplog.text
    assert "synthetic-password" not in caplog.text


def test_runs_query_filters_on_timestamp_start():
    """Windowed runs export filters on timestamp_start with bound parameters."""
    window = sync.SyncWindow(_utc(2026, 10, 14), _utc(2026, 10, 15))
    sql, params = sync.build_select_query(sync.RUNS, window)
    assert "FROM qachub.test_runs r WHERE r.timestamp_start >= %(start)s AND r.timestamp_start < %(end)s" in sql
    assert params == {"start": window.start, "end": window.end}


def test_executions_query_joins_runs_only_when_windowed():
    """Executions follow the runs window through a join, but not in snapshot mode."""
    windowed_sql, _ = sync.build_select_query(sync.EXECUTIONS, sync.SyncWindow(_utc(2026, 9, 1), None))
    snapshot_sql, snapshot_params = sync.build_select_query(sync.EXECUTIONS, sync.SyncWindow())
    assert "JOIN qachub.test_runs r ON r.id = e.run_id WHERE r.timestamp_start >= %(start)s" in windowed_sql
    assert "JOIN" not in snapshot_sql and "WHERE" not in snapshot_sql
    assert snapshot_params == {}


def test_suites_query_is_never_windowed():
    """Suites are always exported in full."""
    sql, params = sync.build_select_query(sync.SUITES, sync.SyncWindow(_utc(2026, 9, 1), None))
    assert "WHERE" not in sql and params == {}


def test_select_lists_match_adx_columns():
    """Each exported column list matches the ADX table schema order."""
    for spec in sync.TABLES:
        selected = [item.strip().split(" AS ")[-1].split(".")[-1].split("::")[0] for item in spec.select_list.split(",")]
        assert selected == [name for name, _ in spec.columns]


def test_serialize_row_converts_driver_types():
    """UUIDs, datetimes, decimals, and JSON objects are serialized for ADX."""
    row_id = uuid.uuid4()
    line = sync.serialize_row(
        ["id", "ts", "qty", "report"],
        [row_id, datetime(2026, 10, 14, 12, 0, tzinfo=timezone.utc), Decimal("3"), {"a": [1]}],
    )
    assert json.loads(line) == {"id": str(row_id), "ts": "2026-10-14T12:00:00+00:00", "qty": 3, "report": {"a": [1]}}


def test_kusto_window_predicate_and_literals():
    """Kusto predicates use UTC datetime literals and validated guid literals."""
    predicate = sync.kusto_window_predicate("timestamp_start", sync.SyncWindow(_utc(2026, 10, 14), _utc(2026, 10, 15)))
    assert predicate == "timestamp_start >= datetime(2026-10-14T00:00:00Z) and timestamp_start < datetime(2026-10-15T00:00:00Z)"
    row_id = str(uuid.uuid4())
    assert sync.kusto_guid_list([row_id]) == f"guid({row_id})"
    with pytest.raises(ValueError):
        sync.kusto_guid_list(["1) | take 1"])


@pytest.mark.parametrize("missing_kind", [None, "target", "staging"])
def test_ensure_tables_only_checks_precreated_tables(missing_kind):
    """Check all six tables without creating or changing any table."""
    tables = [name for spec in sync.TABLES for name in (spec.adx_table, spec.staging_table)]
    missing = None
    if missing_kind is not None:
        missing = tables.pop(0 if missing_kind == "target" else 1)
    publisher = object.__new__(sync.AdxPublisher)
    publisher.mgmt = MagicMock(return_value=[{"TableName": name} for name in tables])
    if missing is None:
        publisher.ensure_tables()
    else:
        with pytest.raises(RuntimeError, match=missing):
            publisher.ensure_tables()
    publisher.mgmt.assert_called_once_with(".show tables")


def test_adx_clients_use_system_assigned_identity(monkeypatch):
    """Use an explicit managed identity for both clients, ignoring deployment credentials."""
    monkeypatch.setenv("AZURE_CLIENT_ID", "unrelated-deployment-identity")
    identity = MagicMock()
    data = MagicMock()
    ingest = MagicMock()
    with patch.dict(sys.modules, {
        "azure.identity": identity,
        "azure.kusto.data": data,
        "azure.kusto.ingest": ingest,
    }):
        sync.AdxPublisher("https://cluster.example/", "re")
    identity.ManagedIdentityCredential.assert_called_once_with()
    identity.DefaultAzureCredential.assert_not_called()
    builder = data.KustoConnectionStringBuilder.with_azure_token_credential
    assert builder.call_count == 2
    assert builder.call_args_list[0].args == (
        "https://cluster.example", identity.ManagedIdentityCredential.return_value,
    )
    assert builder.call_args_list[1].args == (
        "https://ingest-cluster.example", identity.ManagedIdentityCredential.return_value,
    )


def test_chunked_splits_items():
    """Items are split into chunks of the requested size."""
    assert list(sync.chunked(["a", "b", "c"], 2)) == [["a", "b"], ["c"]]
