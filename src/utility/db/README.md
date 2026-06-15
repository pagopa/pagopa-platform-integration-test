# Utility DB (`src/utility/db`)

This module provides a driver-agnostic DB-API 2.0 client for read operations and controlled DELETE statements for test scenarios.

## Public API

- `build_db_client(config_node)`
- `build_db_client_config(config_node)`
- `DbClient`
- `DbClientConfig`
- `DbClientError`

## Configuration node structure

```json
{
  "driver": "sqlite3",
  "connection_args": {
    "database": ":memory:"
  },
  "read_only": true
}
```

- `driver` (required): supported driver key/module from the allowlist (for example `sqlite`, `sqlite3`, `postgres`, `mysql`, `sqlserver`).
- `connection_args` (optional): keyword arguments forwarded to `driver.connect(...)`.
- `read_only` (optional, default `true`): blocks non read-only SQL statements, including `DELETE`.
  - Accepted values: boolean (`true`/`false`) or string aliases (`true/false`, `1/0`, `yes/no`, `on/off`).
  - Invalid values raise `DbClientError`.

### Supported driver mapping

- `sqlite` -> `sqlite3`
- `sqlite3` -> `sqlite3`
- `postgres` -> `psycopg`
- `psycopg` -> `psycopg`
- `psycopg2` -> `psycopg2`
- `mysql` -> `pymysql`
- `pymysql` -> `pymysql`
- `sqlserver` -> `pyodbc`
- `pyodbc` -> `pyodbc`

## Defensive query rules

- Query validation is intentionally conservative and **not** a complete SQL-injection defense across dialects.
- Semicolons (`;`) are rejected to enforce a single-statement policy.
- Placeholder queries require explicit parameters.
- Named placeholders use a conservative pattern and ignore PostgreSQL casts like `::text`.
- `execute_delete(...)` accepts only `DELETE ... WHERE ...` statements.

Primary protections expected by this utility:

- Use parameterized queries (`?`, `:name`, `%s`, `%(name)s`) instead of string interpolation.
- Keep statement-type restrictions enabled (`read_only=true` when write access is not needed).
- Use least-privilege DB credentials in test environments.

## Usage example

```python
from src.utility.db import build_db_client

client = build_db_client(
    {
        "driver": "sqlite3",
        "connection_args": {"database": ":memory:"},
        "read_only": True,
    }
)

rows = client.fetch_all("SELECT id, status FROM payments WHERE id = ?", (10,))
row = client.fetch_one("SELECT id, status FROM payments WHERE id = ?", (10,))
count = client.fetch_value("SELECT COUNT(*) FROM payments")

client.close()
```

## DELETE example

```python
from src.utility.db import build_db_client

client = build_db_client(
    {
        "driver": "sqlite3",
        "connection_args": {"database": ":memory:"},
        "read_only": False,
    }
)

deleted_rows = client.execute_delete("DELETE FROM payments WHERE status = ?", ("FAILED",))
print(deleted_rows)

client.close()
```

