"""Synchronize QA Hub PostgreSQL metrics tables into Azure Data Explorer (ADX).

Data is first ingested into ADX staging tables and verified, then published into the
target tables:

- ``QA_NRT_TEST_SUITES`` is always fully replaced (it has no time dimension).
- ``snapshot`` mode atomically replaces the extents of every target table.
- Windowed modes (``yesterday``, ``since``, ``range``) soft-delete the window from the
  target tables and move the staged extents in, so reruns are idempotent.

The time window is applied to ``test_runs.timestamp_start`` (UTC, start inclusive, end
exclusive); executions follow the runs of the window through ``run_id``.
"""

from __future__ import annotations

import argparse
import gzip
import json
import logging
import os
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Iterator
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

LOGGER = logging.getLogger("qa_hub_adx_sync")

MODES = ("yesterday", "snapshot", "since", "range")
DEFAULT_PG_SECRET_NAME = "qa-centralhub-database-url"
PG_SCHEMA = "qachub"
STAGING_SUFFIX = "_STAGING"
FETCH_BATCH_SIZE = 2_000
MAX_FILE_BYTES = 256 * 1024 * 1024
DELETE_ID_CHUNK_SIZE = 500
INGESTION_POLL_SECONDS = 15


@dataclass(frozen=True)
class SyncWindow:
    """UTC time window applied to ``test_runs.timestamp_start``; ``None`` bounds are open."""

    start: datetime | None = None
    end: datetime | None = None

    @property
    def is_snapshot(self) -> bool:
        """Return True when the window covers the whole table."""
        return self.start is None and self.end is None

    def describe(self) -> str:
        """Return a human readable description of the window."""
        if self.is_snapshot:
            return "full snapshot"
        start = self.start.isoformat() if self.start else "-inf"
        end = self.end.isoformat() if self.end else "+inf"
        return f"[{start}, {end})"


@dataclass(frozen=True)
class TableSpec:
    """Describe how a PostgreSQL table maps onto its ADX counterpart."""

    pg_table: str
    adx_table: str
    columns: tuple[tuple[str, str], ...]
    select_list: str
    windowed: bool

    @property
    def staging_table(self) -> str:
        """Return the name of the ADX staging table."""
        return f"{self.adx_table}{STAGING_SUFFIX}"


SUITES = TableSpec(
    pg_table="test_suites",
    adx_table="QA_NRT_TEST_SUITES",
    columns=(
        ("id", "guid"),
        ("test_object", "string"),
        ("test_type", "string"),
        ("suite_version", "string"),
        ("owner_team", "string"),
    ),
    select_list="s.id, s.test_object, s.test_type, s.suite_version, s.owner_team",
    windowed=False,
)

RUNS = TableSpec(
    pg_table="test_runs",
    adx_table="QA_NRT_TEST_RUNS",
    columns=(
        ("id", "guid"),
        ("suite_id", "guid"),
        ("scenario_qty", "int"),
        ("passed_scenario", "int"),
        ("failed_scenario", "int"),
        ("broken_scenario", "int"),
        ("skipped_scenario", "int"),
        ("timestamp_start", "datetime"),
        ("timestamp_end", "datetime"),
        ("duration_ms", "long"),
        ("env", "string"),
        ("trigger_type", "string"),
        ("test_version", "string"),
        ("test_origin", "string"),
    ),
    select_list=(
        "r.id, r.suite_id, r.scenario_qty, r.passed_scenario, r.failed_scenario, "
        "r.broken_scenario, r.skipped_scenario, r.timestamp_start, r.timestamp_end, "
        "r.duration_ms, r.env::text AS env, r.trigger_type::text AS trigger_type, "
        "r.test_version, r.test_origin"
    ),
    windowed=True,
)

EXECUTIONS = TableSpec(
    pg_table="test_executions",
    adx_table="QA_NRT_TEST_EXECUTIONS",
    columns=(
        ("id", "guid"),
        ("run_id", "guid"),
        ("allure_id", "string"),
        ("status", "string"),
        ("scenario_name", "string"),
        ("allure_report", "dynamic"),
        ("duration_ms", "long"),
        ("error_message", "string"),
        ("retries", "int"),
    ),
    select_list=(
        "e.id, e.run_id, e.allure_id, e.status::text AS status, e.scenario_name, "
        "e.allure_report, e.duration_ms, e.error_message, e.retries"
    ),
    windowed=True,
)

TABLES = (SUITES, RUNS, EXECUTIONS)


@dataclass
class ExportResult:
    """Files and row count produced by exporting one table."""

    spec: TableSpec
    files: list[Path] = field(default_factory=list)
    rows: int = 0


def parse_iso_date(value: str | None, option_name: str) -> date | None:
    """Parse an optional ``YYYY-MM-DD`` value, raising a clear error when invalid."""
    if value is None or not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError as error:
        raise ValueError(f"{option_name} must use the YYYY-MM-DD format, got {value!r}") from error


def _utc_midnight(day: date) -> datetime:
    """Return midnight UTC of the given day."""
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc)


def compute_window(mode: str, from_date: date | None, to_date: date | None, today: date) -> SyncWindow:
    """Translate the requested sync mode and dates into a UTC window."""
    if mode not in MODES:
        raise ValueError(f"Unsupported mode {mode!r}; expected one of {', '.join(MODES)}")
    if mode == "snapshot":
        return SyncWindow()
    if mode == "yesterday":
        return SyncWindow(_utc_midnight(today - timedelta(days=1)), _utc_midnight(today))
    if from_date is None:
        raise ValueError(f"from_date is required for mode {mode!r}")
    if from_date > today:
        raise ValueError("from_date cannot be in the future")
    if mode == "since":
        return SyncWindow(_utc_midnight(from_date), None)
    if to_date is None:
        raise ValueError("to_date is required for mode 'range'")
    if to_date < from_date:
        raise ValueError("to_date must be greater than or equal to from_date")
    return SyncWindow(_utc_midnight(from_date), _utc_midnight(to_date + timedelta(days=1)))


def to_libpq_url(database_url: str) -> str:
    """Convert a SQLAlchemy/asyncpg URL into a libpq URL usable by psycopg."""
    parts = urlsplit(database_url.strip())
    scheme = parts.scheme.split("+", 1)[0]
    if scheme not in ("postgresql", "postgres"):
        raise ValueError("The database URL must use the postgresql scheme")
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        query.append(("sslmode", value) if key == "ssl" else (key, value))
    return urlunsplit(("postgresql", parts.netloc, parts.path, urlencode(query), parts.fragment))


def build_select_query(spec: TableSpec, window: SyncWindow) -> tuple[str, dict[str, datetime]]:
    """Build the parametrized SELECT used to export one table for the given window."""
    if spec is SUITES:
        sql = f"SELECT {spec.select_list} FROM {PG_SCHEMA}.test_suites s"
    elif spec is RUNS:
        sql = f"SELECT {spec.select_list} FROM {PG_SCHEMA}.test_runs r"
    elif window.is_snapshot:
        sql = f"SELECT {spec.select_list} FROM {PG_SCHEMA}.test_executions e"
    else:
        sql = (
            f"SELECT {spec.select_list} FROM {PG_SCHEMA}.test_executions e "
            f"JOIN {PG_SCHEMA}.test_runs r ON r.id = e.run_id"
        )

    params: dict[str, datetime] = {}
    conditions = []
    if spec.windowed and window.start is not None:
        conditions.append("r.timestamp_start >= %(start)s")
        params["start"] = window.start
    if spec.windowed and window.end is not None:
        conditions.append("r.timestamp_start < %(end)s")
        params["end"] = window.end
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    return sql, params


def _json_default(value: Any) -> Any:
    """Serialize PostgreSQL driver values that json cannot encode natively."""
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    raise TypeError(f"Unsupported value type {type(value).__name__}")


def serialize_row(columns: Iterable[str], row: Iterable[Any]) -> str:
    """Serialize a database row as one JSON line keyed by ADX column name."""
    return json.dumps(dict(zip(columns, row)), default=_json_default, ensure_ascii=False)


def kusto_datetime(value: datetime) -> str:
    """Return a Kusto datetime literal for a timezone-aware datetime."""
    return f"datetime({value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')})"


def kusto_window_predicate(column: str, window: SyncWindow) -> str:
    """Return the Kusto predicate selecting the rows of the window."""
    conditions = []
    if window.start is not None:
        conditions.append(f"{column} >= {kusto_datetime(window.start)}")
    if window.end is not None:
        conditions.append(f"{column} < {kusto_datetime(window.end)}")
    if not conditions:
        raise ValueError("A window predicate requires at least one bound")
    return " and ".join(conditions)


def kusto_guid_list(ids: Iterable[str]) -> str:
    """Return a comma separated list of validated Kusto guid literals."""
    return ", ".join(f"guid({uuid.UUID(str(item))})" for item in ids)


def chunked(items: list[str], size: int) -> Iterator[list[str]]:
    """Yield consecutive chunks of at most ``size`` items."""
    for index in range(0, len(items), size):
        yield items[index:index + size]


def staging_create_command(spec: TableSpec) -> str:
    """Return the idempotent command creating the ADX staging table of a spec."""
    schema = ", ".join(f"{name}: {kusto_type}" for name, kusto_type in spec.columns)
    return f".create-merge table {spec.staging_table} ({schema})"


def _mask_secret(value: str) -> None:
    """Ask GitHub Actions to mask a secret value in the job logs."""
    if os.environ.get("GITHUB_ACTIONS") == "true" and value:
        print(f"::add-mask::{value}")


def _required_env(name: str) -> str:
    """Return a required environment variable or fail with a clear message."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


def resolve_database_url(secret_name: str) -> str:
    """Read the PostgreSQL connection URL from Azure Key Vault."""
    from src.conf.configuration import get_secrets_resolver

    resolver = get_secrets_resolver()
    try:
        database_url = resolver.resolve(secret_name)
    finally:
        close_client = getattr(resolver, "close_client", None)
        if close_client:
            close_client()
    if not database_url:
        raise RuntimeError(f"Key Vault secret {secret_name} is empty or unavailable")
    _mask_secret(database_url)
    password = urlsplit(database_url).password
    if password:
        _mask_secret(password)
    return database_url


def export_table(connection: Any, spec: TableSpec, window: SyncWindow, output_dir: Path) -> ExportResult:
    """Stream one PostgreSQL table into gzip JSON-lines files ready for ADX ingestion."""
    sql, params = build_select_query(spec, window)
    column_names = [name for name, _ in spec.columns]
    result = ExportResult(spec)
    handle = None
    written = 0
    try:
        with connection.cursor(name=f"export_{spec.pg_table}") as cursor:
            cursor.itersize = FETCH_BATCH_SIZE
            cursor.execute(sql, params)
            for row in cursor:
                if handle is None or written >= MAX_FILE_BYTES:
                    if handle is not None:
                        handle.close()
                    path = output_dir / f"{spec.adx_table}_{len(result.files):04d}.json.gz"
                    handle = gzip.open(path, "wt", encoding="utf-8")
                    result.files.append(path)
                    written = 0
                line = serialize_row(column_names, row) + "\n"
                handle.write(line)
                written += len(line.encode("utf-8"))
                result.rows += 1
    finally:
        if handle is not None:
            handle.close()
    LOGGER.info("Exported %d row(s) from %s.%s in %d file(s)", result.rows, PG_SCHEMA, spec.pg_table, len(result.files))
    return result


def export_all(database_url: str, window: SyncWindow, output_dir: Path) -> dict[str, ExportResult]:
    """Export every table within a single read-only, repeatable-read transaction."""
    import psycopg

    with psycopg.connect(to_libpq_url(database_url), application_name="qa-hub-adx-sync") as connection:
        connection.read_only = True
        connection.isolation_level = psycopg.IsolationLevel.REPEATABLE_READ
        with connection.transaction():
            return {spec.adx_table: export_table(connection, spec, window, output_dir) for spec in TABLES}


def read_exported_ids(result: ExportResult) -> list[str]:
    """Return the ``id`` values contained in exported files."""
    ids = []
    for path in result.files:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            ids.extend(json.loads(line)["id"] for line in handle)
    return ids


class AdxPublisher:
    """Wrap the ADX operations needed to stage, verify, and publish the exported data."""

    def __init__(self, cluster_uri: str, database: str, ingest_uri: str | None = None, credential: Any = None):
        """Create query and queued-ingestion clients authenticated with Entra ID."""
        from azure.identity import DefaultAzureCredential
        from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
        from azure.kusto.ingest import QueuedIngestClient

        credential = credential or DefaultAzureCredential()
        cluster_uri = cluster_uri.rstrip("/")
        if not ingest_uri:
            parts = urlsplit(cluster_uri)
            ingest_uri = urlunsplit((parts.scheme, f"ingest-{parts.netloc}", "", "", ""))
        self.database = database
        self.client = KustoClient(KustoConnectionStringBuilder.with_azure_token_credential(cluster_uri, credential))
        self.ingest_client = QueuedIngestClient(
            KustoConnectionStringBuilder.with_azure_token_credential(ingest_uri.rstrip("/"), credential)
        )

    def close(self) -> None:
        """Close the underlying Kusto clients."""
        self.client.close()
        self.ingest_client.close()

    def mgmt(self, command: str) -> Any:
        """Run a management command and return the primary result."""
        LOGGER.info("ADX command: %s", command if len(command) < 300 else command[:300] + " ...")
        return self.client.execute_mgmt(self.database, command).primary_results[0]

    def query_scalar(self, query: str) -> Any:
        """Run a query returning a single value."""
        rows = self.client.execute_query(self.database, query).primary_results[0]
        return rows[0][0]

    def query_column(self, query: str) -> list[Any]:
        """Run a query and return the values of its first column."""
        return [row[0] for row in self.client.execute_query(self.database, query).primary_results[0]]

    def ensure_tables(self) -> None:
        """Fail if a target table is missing and create the staging tables when needed."""
        existing = {row["TableName"] for row in self.mgmt(".show tables")}
        missing = [spec.adx_table for spec in TABLES if spec.adx_table not in existing]
        if missing:
            raise RuntimeError(f"Missing ADX target table(s): {', '.join(missing)}")
        for spec in TABLES:
            self.mgmt(staging_create_command(spec))

    def stage(self, export: ExportResult, timeout_seconds: int) -> None:
        """Ingest the exported files into the staging table and wait until all rows are visible."""
        from azure.kusto.data.data_format import DataFormat, IngestionMappingKind
        from azure.kusto.ingest import ColumnMapping, IngestionProperties

        spec = export.spec
        self.mgmt(f".clear table {spec.staging_table} data")
        if export.rows == 0:
            LOGGER.info("No rows to stage for %s", spec.adx_table)
            return

        started_at = datetime.now(timezone.utc)
        properties = IngestionProperties(
            database=self.database,
            table=spec.staging_table,
            data_format=DataFormat.JSON,
            ingestion_mapping_kind=IngestionMappingKind.JSON,
            column_mappings=[ColumnMapping(name, kusto_type, path=f"$.{name}") for name, kusto_type in spec.columns],
            flush_immediately=True,
        )
        for path in export.files:
            self.ingest_client.ingest_from_file(str(path), ingestion_properties=properties)
        self._wait_for_rows(spec, export.rows, started_at, timeout_seconds)

    def _wait_for_rows(self, spec: TableSpec, expected: int, started_at: datetime, timeout_seconds: int) -> None:
        """Poll the staging table until the expected row count is reached."""
        deadline = time.monotonic() + timeout_seconds
        while True:
            count = int(self.query_scalar(f"{spec.staging_table} | count"))
            if count == expected:
                LOGGER.info("Staged %d row(s) into %s", count, spec.staging_table)
                return
            if count > expected:
                raise RuntimeError(f"{spec.staging_table} contains {count} rows, expected {expected}")
            failures = self.mgmt(
                f".show ingestion failures | where Table == '{spec.staging_table}' "
                f"and FailedOn >= {kusto_datetime(started_at)} | project Details | take 3"
            )
            details = [row["Details"] for row in failures]
            if details:
                raise RuntimeError(f"Ingestion into {spec.staging_table} failed: {details}")
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Timed out waiting for {spec.staging_table}: {count}/{expected} rows ingested")
            time.sleep(INGESTION_POLL_SECONDS)

    def replace_all(self, spec: TableSpec) -> None:
        """Atomically replace every extent of the target table with the staged extents."""
        self.mgmt(
            f".replace extents in table {spec.adx_table} <| "
            f"{{ .show table {spec.adx_table} extents }}, {{ .show table {spec.staging_table} extents }}"
        )

    def move_staged(self, spec: TableSpec) -> None:
        """Append the staged extents to the target table."""
        self.mgmt(f".move extents all from table {spec.staging_table} to table {spec.adx_table}")

    def delete_window(self, window: SyncWindow, exported_run_ids: list[str]) -> None:
        """Soft-delete the runs of the window and their executions from the target tables."""
        predicate = kusto_window_predicate("timestamp_start", window)
        adx_run_ids = [str(value) for value in self.query_column(f"{RUNS.adx_table} | where {predicate} | project id")]
        run_ids = sorted(set(adx_run_ids) | set(exported_run_ids))
        for chunk in chunked(run_ids, DELETE_ID_CHUNK_SIZE):
            self.mgmt(
                f".delete table {EXECUTIONS.adx_table} records <| "
                f"{EXECUTIONS.adx_table} | where run_id in ({kusto_guid_list(chunk)})"
            )
        if adx_run_ids:
            self.mgmt(f".delete table {RUNS.adx_table} records <| {RUNS.adx_table} | where {predicate}")


def publish(publisher: AdxPublisher, exports: dict[str, ExportResult], window: SyncWindow, timeout_seconds: int) -> None:
    """Stage every table, then publish the staged data into the target tables."""
    publisher.ensure_tables()
    for spec in TABLES:
        publisher.stage(exports[spec.adx_table], timeout_seconds)

    publisher.replace_all(SUITES)
    if window.is_snapshot:
        publisher.replace_all(RUNS)
        publisher.replace_all(EXECUTIONS)
        return
    publisher.delete_window(window, read_exported_ids(exports[RUNS.adx_table]))
    publisher.move_staged(RUNS)
    publisher.move_staged(EXECUTIONS)


def write_summary(target_env: str, mode: str, window: SyncWindow, exports: dict[str, ExportResult], dry_run: bool) -> None:
    """Append the sync outcome to the GitHub job summary when available."""
    lines = [
        f"## QA Hub → ADX sync - {target_env}",
        "",
        f"- Mode: `{mode}`{' (dry run, nothing published)' if dry_run else ''}",
        f"- Window (`test_runs.timestamp_start`, UTC): `{window.describe()}`",
        "",
        "| ADX table | Rows |",
        "|---|---:|",
        *(f"| `{name}` | {result.rows} |" for name, result in exports.items()),
        "",
    ]
    text = "\n".join(lines)
    print(text)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write(text + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command line options."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mode", choices=MODES, default="yesterday", help="Synchronization mode")
    parser.add_argument("--from-date", default=None, help="First UTC day (YYYY-MM-DD) for since/range modes")
    parser.add_argument("--to-date", default=None, help="Last UTC day, inclusive (YYYY-MM-DD) for range mode")
    parser.add_argument("--dry-run", action="store_true", help="Export from PostgreSQL only, without writing to ADX")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the PostgreSQL to ADX synchronization."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("azure").setLevel(logging.WARNING)
    args = parse_args(argv)

    target_env = _required_env("TARGET_ENV").lower()
    window = compute_window(
        args.mode,
        parse_iso_date(args.from_date, "from_date"),
        parse_iso_date(args.to_date, "to_date"),
        datetime.now(timezone.utc).date(),
    )
    LOGGER.info("Syncing environment %s, mode %s, window %s", target_env, args.mode, window.describe())

    database_url = resolve_database_url(os.environ.get("PG_SECRET_NAME") or DEFAULT_PG_SECRET_NAME)
    with tempfile.TemporaryDirectory(prefix="qa-hub-adx-") as temp_dir:
        exports = export_all(database_url, window, Path(temp_dir))
        if not args.dry_run:
            publisher = AdxPublisher(
                _required_env("ADX_CLUSTER_URI"),
                _required_env("ADX_DATABASE"),
                os.environ.get("ADX_INGEST_URI"),
            )
            try:
                publish(publisher, exports, window, int(os.environ.get("ADX_INGESTION_TIMEOUT_SECONDS", "1800")))
            finally:
                publisher.close()
    write_summary(target_env, args.mode, window, exports, args.dry_run)


if __name__ == "__main__":
    main()
