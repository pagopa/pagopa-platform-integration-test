from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Any, Mapping, MutableMapping, Optional

import requests
from lxml import etree
from zeep.transports import Transport
from zeep.wsse import UsernameToken

from src.utility.soap.soap_client import (
    SoapAuthConfig,
    SoapBasicAuthConfig,
    SoapClientError,
    SoapWsseAuthConfig,
)


def _get_value(source: Any, key: str, default: Optional[Any] = None) -> Any:
    """Reads a value from a mapping or object-like configuration node."""
    if source is None:
        return default
    if isinstance(source, Mapping):
        return source.get(key, default)
    if hasattr(source, key):
        return getattr(source, key)
    return default


def _get_required_value(source: Any, key: str) -> Any:
    """Reads a required value and raises SoapClientError when missing."""
    value = _get_value(source, key)
    if value is None or value == "":
        raise SoapClientError(f"Missing required configuration value: '{key}'")
    return value


def _remove_namespace(content: str) -> str:
    """Removes XML namespace prefixes for namespace-agnostic tag lookups."""
    content_without_ns = re.sub(r'(<\/?)(\w+:)', r'\1', content)
    content_without_ns = re.sub(r'\sxmlns[^"]+"[^"]+"', '', content_without_ns)
    content_without_ns = re.sub(r'\sxsi[^"]+"[^"]+"', '', content_without_ns)
    return content_without_ns


def _build_transport(
        service_config: Mapping[str, Any],
        auth_config: Optional[SoapAuthConfig],
) -> Transport:
    """Creates a zeep Transport configured from service and auth settings."""
    session = requests.Session()
    session.verify = _get_value(service_config, "verify_ssl", True)

    extra_headers = _get_value(service_config, "extra_headers", {})
    if extra_headers:
        session.headers.update(extra_headers)

    if isinstance(auth_config, SoapBasicAuthConfig):
        session.auth = (auth_config.username, auth_config.password)

    timeout = _get_value(service_config, "timeout", 30)
    return Transport(session=session, timeout=timeout)


def send_raw_soap_request(
        service_config: Mapping[str, Any],
        soap_action: str,
        body: str,
        auth_config: Optional[SoapAuthConfig] = None,
) -> tuple[int, Optional[ET.Element], Mapping[str, Any]]:
    """Sends a raw SOAP envelope through zeep transport and parses the XML response.

    Args:
        service_config: dict-like node with required key ``url`` and optional
            ``timeout``, ``verify_ssl``, ``extra_headers`` and ``raw_headers``.
        soap_action: SOAP action value sent as ``soapAction`` header.
        body: full SOAP XML envelope to send.
        auth_config: optional SOAP auth config (none/basic/wsse).

    Returns:
        Tuple ``(status_code, xml_root_or_none, response_headers)``.

    Raises:
        SoapClientError: when request payload is invalid or the request fails.
    """
    url = _get_required_value(service_config, "url")
    transport = _build_transport(service_config, auth_config)

    headers: MutableMapping[str, str] = {
        "Content-Type": "application/xml",
        "soapAction": soap_action,
    }
    raw_headers = _get_value(service_config, "raw_headers", {})
    if raw_headers:
        headers.update(raw_headers)

    try:
        envelope = etree.fromstring(body.encode("utf-8"))
    except etree.XMLSyntaxError as exc:
        raise SoapClientError(f"Invalid SOAP XML payload: {exc}") from exc

    if isinstance(auth_config, SoapWsseAuthConfig):
        username_token = UsernameToken(auth_config.username, auth_config.password)
        envelope, headers = username_token.apply(envelope, headers)

    try:
        response = transport.post_xml(address=url, envelope=envelope, headers=dict(headers))
    except Exception as exc:
        raise SoapClientError(f"Failed to send raw SOAP request to '{url}': {exc}") from exc

    xml_root = None
    response_text = getattr(response, "text", "")
    if response_text:
        cleaned = _remove_namespace(response_text)
        try:
            xml_root = ET.fromstring(cleaned)
        except ET.ParseError:
            xml_root = None

    return response.status_code, xml_root, getattr(response, "headers", {})


def get_raw_soap_text(xml_root: Optional[ET.Element], tag_path: str) -> Optional[str]:
    """Extracts a text value from a namespace-stripped SOAP XML tree.

    Args:
        xml_root: parsed XML root returned by ``send_raw_soap_request``.
        tag_path: ElementTree path relative to any nested node.

    Returns:
        The matched element text, or ``None`` when missing.
    """
    if xml_root is None:
        return None

    lookup_path = tag_path if tag_path.startswith(".") else f".//{tag_path}"
    element = xml_root.find(lookup_path)
    if element is None:
        return None
    return element.text