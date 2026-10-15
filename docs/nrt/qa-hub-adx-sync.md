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
| `yesterday` | previous UTC day | default, nightly at 02:30 UTC on every environment |
| `snapshot` | all rows, including runs without `timestamp_start` | manual |
| `since` | from `from_date` to now | manual, needs `from_date` |
| `range` | `from_date` to `to_date`, both inclusive | manual, needs `from_date` and `to_date` |

`dry_run` exports from PostgreSQL and writes the row counts to the job summary without
touching ADX.

## How it works

1. Reads `qa-centralhub-database-url` from `pagopa-<d|u|p>-itn-qa-kv` with the runner's
   managed identity.
2. Exports the three tables in one read-only `REPEATABLE READ` transaction to gzip
   JSON-lines files.
3. Ingests each file with queued ingestion into a `<TABLE>_STAGING` table, which the
   script creates automatically, then waits until the staged row count matches.
4. Publishes:
   - `snapshot` mode and suites use `.replace extents`, an atomic swap.
   - The windowed modes soft-delete the rows in the window from the target tables
     (`.delete ... records`), then `.move extents` from staging. Rerunning the same
     window is idempotent.

## Prerequisites

- **ADX permissions**: grant **Database Admin** on the ADX database to the managed identity
  of each environment's self-hosted runner. Soft delete, extent operations, and ingestion
  failure checks require this role.
- **Target tables**: the `QA_NRT_*` tables must already exist (`.create-merge table ...`).
- **GitHub Environment variables** (`dev`, `uat`, `prod`):
  - `ADX_CLUSTER_URI`, e.g. `https://<cluster>.<region>.kusto.windows.net`.
  - `ADX_DATABASE`.
  - `ADX_INGEST_URI` is optional and defaults to `https://ingest-<cluster host>`.
- **Network**: the runner must reach the cluster, the ingestion endpoint, and the
  ingestion storage accounts/queues of the cluster (HTTPS 443), plus PostgreSQL (5432).
- **Key Vault**: `get` permission on the secret, as already used by `nrt-sync-secrets.yml`.

## Manual run

```bash
gh workflow run qa-hub-adx-sync.yml -f target_env=uat -f mode=range \
  -f from_date=2026-09-01 -f to_date=2026-09-30
```
