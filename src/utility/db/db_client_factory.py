from __future__ import annotations

from importlib import import_module
from typing import Any, Mapping

from src.utility.db.db_client import DbClient, DbClientError, build_db_client_config


SUPPORTED_DB_DRIVERS: dict[str, str] = {
    "sqlite": "sqlite3",
    "sqlite3": "sqlite3",
    "postgres": "psycopg",
    "mysql": "pymysql",
    "pymysql": "pymysql",
    "sqlserver": "pyodbc",
    "pyodbc": "pyodbc",
}


def _resolve_driver_module_name(configured_driver: str) -> str:
    """Resolve and validate the configured driver against the supported allowlist."""

    normalized_driver = configured_driver.strip().lower()
    if normalized_driver not in SUPPORTED_DB_DRIVERS:
        supported = ", ".join(sorted(SUPPORTED_DB_DRIVERS))
        raise DbClientError(
            f"Unsupported DB driver '{configured_driver}'. Supported values: {supported}"
        )

    return SUPPORTED_DB_DRIVERS[normalized_driver]


def build_db_client(config_node: Mapping[str, Any]) -> DbClient:
    """Create a ``DbClient`` from a loaded configuration node.

    Args:
        config_node: Configuration node that contains ``driver`` and ``connection_args``.

    Returns:
        Ready-to-use ``DbClient`` instance.

    Raises:
        DbClientError: If module import or DB connection creation fails.
    """

    client_config = build_db_client_config(config_node)
    driver_module_name = _resolve_driver_module_name(client_config.driver)

    try:
        driver_module = import_module(driver_module_name)
    except ImportError as exc:
        raise DbClientError(f"Cannot import DB driver '{driver_module_name}': {exc}") from exc

    try:
        connection = driver_module.connect(**client_config.connection_args)
    except Exception as exc:
        raise DbClientError(f"Cannot create DB connection: {exc}") from exc

    return DbClient(client_config, driver_module, connection)

