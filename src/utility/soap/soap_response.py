from __future__ import annotations

from typing import Any

from zeep.helpers import serialize_object


class SoapResponseError(ValueError):
    """Application error raised while reading or writing attributes from a SOAP response."""


def serialize_response(response: Any) -> Any:
    """Converts a zeep SOAP response into a plain Python dict/list.

    After serialization the result is compatible with get_attr/set_attr
    from the json utility package.

    Args:
        response: zeep response object returned by client.service.Operation().

    Raises:
        SoapResponseError: if the response is None.

    Example::

        raw = client.service.GetPayment(paymentId="123")
        payload = serialize_response(raw)

        from src.utility.json import get_attr
        amount = get_attr(payload, "payment.amount.value")
    """
    if response is None:
        raise SoapResponseError("SOAP response is None")

    return serialize_object(response, target_cls=dict)


def get_soap_attr(
        response: Any,
        attr_path: str,
        default: Any = None,
        *,
        strict: bool = False,
) -> Any:
    """Serializes a zeep SOAP response and retrieves a value by path.

    Path format: `key1.key2[0].key3` (same as JSON get_attr).

    Args:
        response: zeep response object.
        attr_path: dot-separated path with optional list indexes.
        default: returned when path is not found and strict is False.
        strict: when True, raises SoapResponseError if the path does not exist.

    Example::

        raw = client.service.GetPayment(paymentId="123")
        currency = get_soap_attr(raw, "payment.amount.currency")
        item_id  = get_soap_attr(raw, "items[0].id", default="N/A")
    """
    from src.utility.json import JsonAttributeError, get_attr

    payload = serialize_response(response)

    try:
        return get_attr(payload, attr_path)
    except JsonAttributeError as exc:
        if strict:
            raise SoapResponseError(str(exc)) from exc
        return default


def set_soap_attr(
        response: Any,
        attr_path: str,
        value: Any,
        create_missing: bool = False,
) -> Any:
    """Serializes a zeep SOAP response and sets a value by path.

    Path format: `key1.key2[0].key3` (same as JSON set_attr).

    Args:
        response: zeep response object.
        attr_path: dot-separated path with optional list indexes.
        value: value to assign at the requested path.
        create_missing: when True, missing nodes are created automatically.
            When False (default), raises SoapResponseError if the path does not exist.

    Returns:
        The mutated plain Python dict produced by serialize_response().

    Raises:
        SoapResponseError: if the response is None, or the path is not writable
            and create_missing is False.

    Example::

        raw = client.service.GetPayment(paymentId="123")
        payload = set_soap_attr(raw, "payment.amount.currency", "USD")

        # With auto-creation of missing nodes:
        payload = set_soap_attr(raw, "payment.extra[0].note", "test", create_missing=True)
    """
    from src.utility.json import JsonAttributeSetError, set_attr

    payload = serialize_response(response)

    try:
        return set_attr(payload, attr_path, value, create_missing)
    except JsonAttributeSetError as exc:
        raise SoapResponseError(str(exc)) from exc