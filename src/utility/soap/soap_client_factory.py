from __future__ import annotations

from typing import Any, Mapping, Optional

import requests
from zeep import Client
from zeep.transports import Transport
from zeep.wsse import UsernameToken

from src.utility.soap.soap_client import (
    SoapAuthConfig,
    SoapBasicAuthConfig,
    SoapClientError,
    SoapWsseAuthConfig,
)


def build_soap_client(
        service_config: Mapping[str, Any],
        auth_config: Optional[SoapAuthConfig] = None,
) -> Client:
    """Creates a zeep SOAP Client from a service config node and optional auth.

    Args:
        service_config: dict with key "wsdl_url" (required) and optional
                        "timeout", "verify_ssl", "extra_headers", "plugins".
        auth_config: config built via soap_auth_factory. None = no auth.

    Returns:
        A configured zeep.Client ready to call SOAP operations.

    Raises:
        SoapClientError: if "wsdl_url" is missing or the client cannot be created.

    Example (no auth)::

        client = build_soap_client(config["service"], build_soap_no_auth())
        response = client.service.MyOperation(param="value")

    Example (WS-Security)::

        auth = build_soap_wsse_auth_from_config(config["auth"]["wsse"])
        client = build_soap_client(config["service"], auth)

    Example in environment.py::

        def before_all(context):
            config = load_test_config(resolver)
            auth = build_soap_wsse_auth_from_config(config["auth"]["wsse"])
            context.soap_client = build_soap_client(config["service"], auth)
    """
    def _get(key, default=None):
        if isinstance(service_config, Mapping):
            return service_config.get(key, default)
        return getattr(service_config, key, default)

    wsdl_url = _get("wsdl_url")
    if not wsdl_url:
        raise SoapClientError("Missing required 'wsdl_url' in service_config")

    session = requests.Session()
    session.verify = _get("verify_ssl", True)

    extra_headers = _get("extra_headers", {})
    if extra_headers:
        session.headers.update(extra_headers)

    if isinstance(auth_config, SoapBasicAuthConfig):
        session.auth = (auth_config.username, auth_config.password)

    transport = Transport(session=session, timeout=_get("timeout", 30))

    wsse = None
    if isinstance(auth_config, SoapWsseAuthConfig):
        wsse = UsernameToken(auth_config.username, auth_config.password)

    try:
        return Client(
            wsdl=wsdl_url,
            transport=transport,
            wsse=wsse,
            plugins=_get("plugins", []),
        )
    except Exception as exc:
        raise SoapClientError(
            f"Failed to create SOAP client for '{wsdl_url}': {exc}"
        ) from exc