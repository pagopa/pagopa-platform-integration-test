from __future__ import annotations

from typing import Any, Mapping, Optional

from src.utility.soap.soap_client import (
    SoapBasicAuthConfig,
    SoapNoAuthConfig,
    SoapWsseAuthConfig,
)


def _get_value(source: Any, key: str, default: Optional[Any] = None) -> Any:
    if source is None:
        return default
    if isinstance(source, Mapping):
        return source.get(key, default)
    if hasattr(source, key):
        return getattr(source, key)
    return default


def _get_required_value(source: Any, key: str) -> Any:
    value = _get_value(source, key)
    if value is None:
        raise RuntimeError(f"Missing required configuration value: '{key}'")
    return value


def build_soap_no_auth() -> SoapNoAuthConfig:
    """Returns a no-authentication config.

    Example::

        auth = build_soap_no_auth()
        client = build_soap_client(config["service"], auth)
    """
    return SoapNoAuthConfig()


def build_soap_basic_auth(username: str, password: str) -> SoapBasicAuthConfig:
    """Returns a Basic Auth config.

    Example::

        auth = build_soap_basic_auth("user", "secret")
    """
    return SoapBasicAuthConfig(username=username, password=password)


def build_soap_wsse_auth(username: str, password: str) -> SoapWsseAuthConfig:
    """Returns a WS-Security UsernameToken config.

    Example::

        auth = build_soap_wsse_auth("user", "secret")
    """
    return SoapWsseAuthConfig(username=username, password=password)


def build_soap_basic_auth_from_config(config_node: Any) -> SoapBasicAuthConfig:
    """Builds BasicAuthConfig from an already-loaded config node.

    Example::

        # JSON: { "username": "user", "password": "$soap_password" }
        auth = build_soap_basic_auth_from_config(config["auth"]["basic"])
    """
    return SoapBasicAuthConfig(
        username=_get_required_value(config_node, "username"),
        password=_get_required_value(config_node, "password"),
    )


def build_soap_wsse_auth_from_config(config_node: Any) -> SoapWsseAuthConfig:
    """Builds WsseAuthConfig from an already-loaded config node.

    Example::

        # JSON: { "username": "user", "password": "$wsse_password" }
        auth = build_soap_wsse_auth_from_config(config["auth"]["wsse"])
    """
    return SoapWsseAuthConfig(
        username=_get_required_value(config_node, "username"),
        password=_get_required_value(config_node, "password"),
    )