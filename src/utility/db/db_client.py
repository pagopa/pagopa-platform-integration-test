from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any, Mapping

NAMED_PLACEHOLDER_PATTERN = re.compile(r"(?<!:):[A-Za-z_]\w*")


@dataclass
class DbClientConfig:
    """Infrastructure configuration for a DB-API client.

    Args:
        driver: Importable DB-API module name (for example ``sqlite3``).
        connection_args: Keyword arguments forwarded to ``driver.connect``.
        read_only: Whether to reject non read-only SQL statements.
    """

    driver: str
    connection_args: dict[str, Any] = field(default_factory=dict)
    read_only: bool = True


class DbClientError(RuntimeError):
    """Application error raised by DB utility operations."""


class DbClient:
    """Thin wrapper around a DB-API 2.0 connection for read and delete operations."""

    def __init__(self, config: DbClientConfig, driver_module: Any, connection: Any) -> None:
        """Initialize the DB client.

        Args:
            config: Parsed client configuration.
            driver_module: Imported DB-API module.
            connection: Open DB-API connection instance.
        """

        self.config = config
        self._driver_module = driver_module
        self._driver_error = getattr(driver_module, "Error", Exception)
        self._connection = connection

    def __enter__(self) -> "DbClient":
        """Return the active client for context-manager usage."""

        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        """Close the DB connection when leaving a context manager."""

        self.close()

    def fetch_all(self, query: str, params: Any = ()) -> list[dict[str, Any]]:
        """Execute a read query and return all rows as dictionaries.

        Args:
            query: SQL read statement.
            params: Bound SQL parameters (tuple, list, or mapping).

        Returns:
            List of rows where each row maps column names to values.

        Raises:
            DbClientError: If the query is not read-only or execution fails.
        """

        self._validate_query_security(query, params)
        self._ensure_read_only(query)

        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [column[0] for column in (cursor.description or [])]
            return [dict(zip(columns, row)) for row in rows]
        except self._driver_error as exc:
            raise DbClientError(f"DB query failed: {exc}") from exc
        finally:
            self._close_cursor(cursor)

    def fetch_one(self, query: str, params: Any = ()) -> dict[str, Any] | None:
        """Execute a read query and return the first row as a dictionary.

        Args:
            query: SQL read statement.
            params: Bound SQL parameters (tuple, list, or mapping).

        Returns:
            First row as a dictionary, or ``None`` when no rows are found.
        """
        rows = self.fetch_all(query, params)
        return rows[0] if rows else None

    def fetch_value(self, query: str, params: Any = ()) -> Any:
        """Execute a read query and return the first column of the first row.

        Args:
            query: SQL read statement.
            params: Bound SQL parameters (tuple, list, or mapping).

        Returns:
            Scalar value from the first column, or ``None`` when no rows are found.
        """

        row = self.fetch_one(query, params)
        if not row:
            return None
        return next(iter(row.values()))

    def execute_delete(self, query: str, params: Any = ()) -> int:
        """Execute a DELETE statement and return the number of affected rows.

        Args:
            query: SQL DELETE statement.
            params: Bound SQL parameters (tuple, list, or mapping).

        Returns:
            Number of rows deleted by the statement.

        Raises:
            DbClientError: If the statement is invalid, blocked by read-only mode, or execution fails.
        """

        self._validate_query_security(query, params)
        self._ensure_delete_allowed(query)

        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            deleted_rows = int(cursor.rowcount or 0)
            self._connection.commit()
            return deleted_rows
        except self._driver_error as exc:
            self._rollback_safely()
            raise DbClientError(f"DB delete failed: {exc}") from exc
        finally:
            self._close_cursor(cursor)

    def close(self) -> None:
        """Close the underlying database connection.

        Raises:
            DbClientError: If connection closing fails.
        """

        try:
            self._connection.close()
        except self._driver_error as exc:
            raise DbClientError(f"DB close failed: {exc}") from exc

    def _ensure_read_only(self, query: str) -> None:
        """Reject non read-only SQL statements when read-only mode is enabled."""

        if not self.config.read_only:
            return

        normalized_query = query.strip().lstrip("(").upper()
        allowed_prefixes = ("SELECT", "WITH", "PRAGMA", "EXPLAIN")
        if not normalized_query.startswith(allowed_prefixes):
            raise DbClientError(
                "Only read-only SQL statements are allowed when read_only is enabled"
            )

    def _ensure_delete_allowed(self, query: str) -> None:
        """Validate DELETE statement shape and enforce read-only restrictions."""

        normalized_query = query.strip().lstrip("(").upper()
        if not normalized_query.startswith("DELETE"):
            raise DbClientError("execute_delete only accepts SQL DELETE statements")

        where_match = re.search(r"\bWHERE\b", normalized_query)
        if not where_match:
            raise DbClientError("DELETE statements must include a WHERE clause")

        where_clause = normalized_query[where_match.end() :].strip().rstrip(";")
        if not where_clause:
            raise DbClientError("DELETE statements must include a non-empty WHERE clause")

        if self.config.read_only:
            raise DbClientError(
                "DELETE statements are not allowed when read_only is enabled"
            )

    def _validate_query_security(self, query: str, params: Any) -> None:
        """Apply conservative query validation for test safety.

        This validation is intentionally simple and does not provide complete
        SQL-injection protection across SQL dialects. The primary safety
        controls remain parameter binding and statement-type restrictions.
        """

        normalized_query = query.strip()
        if not normalized_query:
            raise DbClientError("SQL query cannot be empty")

        # Conservative allowlist: refuse ';' entirely to enforce single statement.
        if ";" in normalized_query:
            raise DbClientError("Semicolons are not allowed in SQL queries")

        if isinstance(params, (str, bytes, bytearray)):
            raise DbClientError("SQL parameters must be tuple, list, or mapping")

        has_placeholders = bool(
            re.search(r"\?", normalized_query)
            or NAMED_PLACEHOLDER_PATTERN.search(normalized_query)
            or re.search(r"%s", normalized_query)
            or re.search(r"%\(\w+\)s", normalized_query)
        )
        if has_placeholders and not params:
            raise DbClientError("SQL query contains placeholders but no parameters were provided")

    def _rollback_safely(self) -> None:
        """Try to rollback the current transaction without masking the root failure."""

        try:
            self._connection.rollback()
        except Exception:
            return

    def _close_cursor(self, cursor: Any) -> None:
        """Close a DB cursor if it is available and supports close."""

        if cursor is None:
            return

        close_method = getattr(cursor, "close", None)
        if callable(close_method):
            try:
                close_method()
            except Exception:
                return


def build_db_client_config(config_node: Mapping[str, Any]) -> DbClientConfig:
    """Build a typed DB client configuration from a generic config node.

    Args:
        config_node: Loaded configuration node.

    Returns:
        Parsed ``DbClientConfig`` instance.

    Raises:
        DbClientError: If mandatory configuration fields are missing.
    """

    driver = config_node.get("driver")
    if not driver:
        raise DbClientError("Missing required configuration field: driver")

    connection_args = config_node.get("connection_args", {})
    if not isinstance(connection_args, dict):
        raise DbClientError("connection_args must be a dictionary")

    read_only = _parse_read_only(config_node.get("read_only", True))

    return DbClientConfig(
        driver=str(driver),
        connection_args=connection_args,
        read_only=read_only,
    )


def _parse_read_only(value: Any) -> bool:
    """Parse the read_only flag from config using explicit and safe rules.

    Accepted values:
    - bool: returned as-is
    - str: one of true/false aliases (case-insensitive, trimmed)

    Raises:
        DbClientError: If value type/content is not supported.
    """

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y", "on"}:
            return True
        if normalized in {"false", "0", "no", "n", "off"}:
            return False
        raise DbClientError(
            "read_only must be a boolean or one of: true/false, 1/0, yes/no, on/off"
        )

    raise DbClientError(
        "read_only must be a boolean or a supported boolean string value"
    )

