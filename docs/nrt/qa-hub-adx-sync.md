# QA Hub PostgreSQL to ADX sync

The [`qa-hub-adx-sync.yml`](../../.github/workflows/qa-hub-adx-sync.yml) workflow copies the
QA Hub PostgreSQL tables into their Azure Data Explorer (ADX) mirrors. The logic lives in
[`qa_hub_adx_sync.py`](../../.github/scripts/qa_hub_adx_sync.py).

| PostgreSQL | ADX |
|---|---|
| `qachub.test_suites` | `QA_NRT_TEST_SUITES` |
| `qachub.test_runs` | `QA_NRT_TEST_RUNS` |
| `qachub.test_executions` | `QA_NRT_TEST_EXECUTIONS` |

## Modes

All windows are UTC days and apply to `test_runs.timestamp_start`. Executions follow their
run. Suites are always reloaded in full because they are small and have no timestamp.

| Mode | Window | Trigger |
|---|---|---|
| `yesterday` | previous UTC day | default, nightly at 02:30 UTC on dev and UAT; manual on dev or UAT |
| `snapshot` | all rows, including runs without `timestamp_start` | manual |
| `since` | from `from_date` to now | manual, needs `from_date` |
| `range` | `from_date` to `to_date`, both inclusive | manual, needs `from_date` and `to_date` |

`dry_run` exports from PostgreSQL and writes the row counts to the job summary without
touching ADX.

Manual dispatch supports **dev** and **UAT**. The nightly schedule runs `yesterday`
on both environments; other modes are manual only. Prod is not enabled. Pushes and
pull requests do not trigger synchronization.

## How it works

1. Reads `qa-centralhub-database-url` from `pagopa-<d|u|p>-itn-qa-kv` with the runner's
   managed identity.
2. Exports the three tables in one read-only `REPEATABLE READ` transaction to gzip
   JSON-lines files.
3. Checks that all six target and staging tables already exist, then ingests each
   file with queued ingestion into its `<TABLE>_STAGING` table and waits until the
   staged row count matches. The script does not create or alter table schemas.
4. Publishes:
   - `snapshot` mode and suites use `.replace extents`, an atomic swap per table,
     not a transaction across the three tables.
   - The windowed modes soft-delete the rows in the window from the target tables
     (`.delete ... records`), then `.move extents` from staging. Rerunning the same
     window is idempotent.

## Prerequisites

- **ADX permissions**: grant **Database Admin** on the ADX database to the managed identity
  of the dedicated self-hosted runner. This grants access to the entire database,
  not just the QA tables. Table Ingestor alone is insufficient for this sync.
- **ADX authentication**: query and ingestion clients explicitly use
  `ManagedIdentityCredential()` with the Container Apps Job's system-assigned identity.
  They do not fall back to Azure CLI, OIDC deployment credentials, or client secrets.
  Key Vault authentication continues using the existing repository resolver.
- **Tables**: infrastructure must precreate the three target tables and their matching
  staging tables in each enabled environment, with identical columns, types, and order:
  - `QA_NRT_TEST_SUITES_STAGING`
  - `QA_NRT_TEST_RUNS_STAGING`
  - `QA_NRT_TEST_EXECUTIONS_STAGING`
  Missing tables cause an explicit failure before staging data is cleared.
- **GitHub Environment variables** (`dev`, `uat`):
  - `ADX_CLUSTER_URI`, e.g. `https://<cluster>.<region>.kusto.windows.net`.
  - `ADX_DATABASE`.
  - `ADX_INGEST_URI` is optional and defaults to `https://ingest-<cluster host>`.
- **Network**: the runner must reach the cluster, the ingestion endpoint, and the
  ingestion storage accounts/queues of the cluster (HTTPS 443), plus PostgreSQL (5432).
- **Key Vault**: `get` permission on the secret, as already used by `nrt-sync-secrets.yml`.

## Manual run

```bash
gh workflow run qa-hub-adx-sync.yml -f target_env=dev -f mode=range \
  -f from_date=2026-09-01 -f to_date=2026-09-30
```

## Temporary PostgreSQL connection diagnostics

Before connecting, `[DEBUG-adx-pg]` logs compare the libpq-parsed endpoint with the
expected PostgreSQL hostname for `TARGET_ENV`, port `5432`, database `qachub`, and
SSL mode `require`. They also report whether the configured Key Vault URL matches
the expected environment, and flag URL fragments and connection parameter overrides.
No connection URL, username, password, or arbitrary parsed parameter values are logged:
malformed URLs can cause password fragments to be interpreted as endpoint fields.

For UAT, `host_matches_expected=True` refers to
`pagopa-u-itn-qa-flexible-postgresql.postgres.database.azure.com`.
`host_is_qachub=True` instead indicates that libpq interpreted `qachub` as the host.
Check credential percent-encoding and the secret's URL structure in that case;
an unescaped `/` in a password can produce this result. These traces diagnose the
connection parameters; they do not prove DNS or network reachability.
Remove the tagged diagnostics after the UAT issue is resolved.

## Local validation

```bash
python -m pytest -q .github/scripts/tests/test_qa_hub_adx_sync.py
```

These tests mock Azure clients. A real full snapshot on dev was reported successful
on 2026-10-16, validating runner authentication and the snapshot publication path.
The windowed delete-and-reload path still needs verification with a real dev run.
