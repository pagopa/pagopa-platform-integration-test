from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.utility.db import DbClientError, build_db_client


def seed_database(db_path: str) -> None:
    """Create test schema and seed sample rows for smoke validation."""

    connection = sqlite3.connect(db_path)
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE payments (id INTEGER PRIMARY KEY, status TEXT)")
        cursor.execute("INSERT INTO payments (id, status) VALUES (?, ?)", (1, "FAILED"))
        cursor.execute("INSERT INTO payments (id, status) VALUES (?, ?)", (2, "PAID"))
        connection.commit()
    finally:
        connection.close()


def assert_delete_works(db_path: str) -> None:
    """Verify DELETE execution and rowcount with write-enabled client."""

    client = build_db_client(
        {
            "driver": "sqlite3",
            "connection_args": {"database": db_path},
            "read_only": False,
        }
    )

    try:
        deleted_rows = client.execute_delete(
            "DELETE FROM payments WHERE status = ?", ("FAILED",)
        )
        if deleted_rows != 1:
            raise AssertionError(f"Expected 1 deleted row, got {deleted_rows}")

        remaining_rows = client.fetch_value("SELECT COUNT(*) FROM payments")
        if remaining_rows != 1:
            raise AssertionError(f"Expected 1 remaining row, got {remaining_rows}")
    finally:
        client.close()


def assert_read_only_blocks_delete(db_path: str) -> None:
    """Verify that read-only clients reject DELETE statements."""

    client = build_db_client(
        {
            "driver": "sqlite3",
            "connection_args": {"database": db_path},
            "read_only": True,
        }
    )

    try:
        try:
            client.execute_delete("DELETE FROM payments WHERE id = ?", (2,))
            raise AssertionError("Expected DbClientError for read-only DELETE")
        except DbClientError:
            return
    finally:
        client.close()


def assert_delete_requires_where(db_path: str) -> None:
    """Verify that DELETE statements without WHERE are rejected."""

    client = build_db_client(
        {
            "driver": "sqlite3",
            "connection_args": {"database": db_path},
            "read_only": False,
        }
    )

    try:
        try:
            client.execute_delete("DELETE FROM payments")
            raise AssertionError("Expected DbClientError for DELETE without WHERE")
        except DbClientError:
            return
    finally:
        client.close()


def assert_sql_injection_guards(db_path: str) -> None:
    """Verify that basic SQL injection patterns are blocked."""

    client = build_db_client(
        {
            "driver": "sqlite3",
            "connection_args": {"database": db_path},
            "read_only": False,
        }
    )

    try:
        try:
            client.fetch_all("SELECT id FROM payments; DELETE FROM payments")
            raise AssertionError("Expected DbClientError for multi-statement query")
        except DbClientError:
            pass

        try:
            client.fetch_all("SELECT id FROM payments WHERE id = ?")
            raise AssertionError("Expected DbClientError for missing placeholder parameters")
        except DbClientError:
            return
    finally:
        client.close()


def assert_unsupported_driver_is_rejected(db_path: str) -> None:
    """Verify that driver imports are restricted to the supported allowlist."""

    try:
        build_db_client(
            {
                "driver": "os",
                "connection_args": {"database": db_path},
                "read_only": True,
            }
        )
        raise AssertionError("Expected DbClientError for unsupported DB driver")
    except DbClientError:
        return


def assert_named_placeholder_detection_is_precise(db_path: str) -> None:
    """Verify named-placeholder detection ignores PostgreSQL casts and catches real params."""

    client = build_db_client(
        {
            "driver": "sqlite3",
            "connection_args": {"database": db_path},
            "read_only": True,
        }
    )

    try:
        client._validate_query_security("SELECT '2026-01-01'::TEXT", ())

        try:
            client._validate_query_security("SELECT :real_param", ())
            raise AssertionError("Expected DbClientError for missing named placeholder values")
        except DbClientError:
            return
    finally:
        client.close()


def assert_read_only_parsing_is_explicit(db_path: str) -> None:
    """Verify read_only accepts supported values and rejects invalid ones."""

    for value, expected in (("false", False), ("TRUE", True), (True, True), (False, False)):
        client = build_db_client(
            {
                "driver": "sqlite3",
                "connection_args": {"database": db_path},
                "read_only": value,
            }
        )
        try:
            if client.config.read_only != expected:
                raise AssertionError(f"Expected read_only={expected}, got {client.config.read_only}")
        finally:
            client.close()

    try:
        build_db_client(
            {
                "driver": "sqlite3",
                "connection_args": {"database": db_path},
                "read_only": "maybe",
            }
        )
        raise AssertionError("Expected DbClientError for invalid read_only value")
    except DbClientError:
        return


def main() -> None:
    """Run DB utility smoke checks for DELETE support."""

    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = temp_db.name
    temp_db.close()

    try:
        seed_database(db_path)
        assert_delete_works(db_path)
        assert_read_only_blocks_delete(db_path)
        assert_delete_requires_where(db_path)
        assert_sql_injection_guards(db_path)
        assert_unsupported_driver_is_rejected(db_path)
        assert_named_placeholder_detection_is_precise(db_path)
        assert_read_only_parsing_is_explicit(db_path)
        print("DB utility smoke test: OK")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == "__main__":
    main()


