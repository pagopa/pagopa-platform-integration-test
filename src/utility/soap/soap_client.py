from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Union


class SoapAuthType(str, Enum):
    NONE = "none"
    BASIC = "basic"
    WSSE = "wsse"


@dataclass
class SoapNoAuthConfig:
    """No authentication for SOAP calls."""
    auth_type: SoapAuthType = SoapAuthType.NONE


@dataclass
class SoapBasicAuthConfig:
    """HTTP Basic authentication for SOAP calls."""
    username: str
    password: str
    auth_type: SoapAuthType = SoapAuthType.BASIC


@dataclass
class SoapWsseAuthConfig:
    """WS-Security UsernameToken authentication for SOAP calls."""
    username: str
    password: str
    auth_type: SoapAuthType = SoapAuthType.WSSE


SoapAuthConfig = Union[SoapNoAuthConfig, SoapBasicAuthConfig, SoapWsseAuthConfig]


@dataclass
class SoapClientConfig:
    """Infrastructure configuration for the SOAP client.

    Args:
        wsdl_url: URL or local path of the WSDL file.
        timeout: request timeout in seconds (default 30).
        verify_ssl: whether to verify SSL certificates (default True).
        extra_headers: additional HTTP headers sent with every request.
        plugins: list of zeep plugins.

    Example::

        config = SoapClientConfig(
            wsdl_url="https://example.com/service?wsdl",
            timeout=30,
            verify_ssl=True,
        )
    """
    wsdl_url: str
    timeout: int = 30
    verify_ssl: bool = True
    extra_headers: Dict[str, str] = field(default_factory=dict)
    plugins: list = field(default_factory=list)


class SoapClientError(RuntimeError):
    """Application error raised by the SOAP client."""