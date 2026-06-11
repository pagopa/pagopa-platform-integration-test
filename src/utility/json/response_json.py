from __future__ import annotations

import json
from typing import Any, Dict, List, Union


class JsonConversionError(ValueError):
    """Application error raised during JSON <-> dict conversion."""


class JsonAttributeError(ValueError):
    """Application error raised while reading attributes from a JSON payload."""


class JsonAttributeSetError(ValueError):
    """Application error raised while writing attributes into a JSON payload."""


JsonPathToken = Union[str, int]


def _parse_attr_path(attr_path: str) -> List[JsonPathToken]:
    """Converts a path like `key1.key2[0].key3` into navigable tokens."""
    if not isinstance(attr_path, str):
        raise JsonAttributeError(
            f"attr_path must be of type str, got {type(attr_path).__name__}"
        )

    if not attr_path.strip():
        raise JsonAttributeError("attr_path cannot be empty")

    tokens: List[JsonPathToken] = []
    current = ""
    index = 0

    while index < len(attr_path):
        char = attr_path[index]

        if char == ".":
            if current:
                tokens.append(current)
                current = ""
                index += 1
                continue

            if tokens and isinstance(tokens[-1], int):
                index += 1
                continue

            if not current:
                raise JsonAttributeError(
                    f"Invalid attr_path '{attr_path}'. Expected format 'key1.key2...'"
                )

        if char == "[":
            if current:
                tokens.append(current)
                current = ""

            close_idx = attr_path.find("]", index)
            if close_idx == -1:
                raise JsonAttributeError(
                    f"Invalid attr_path '{attr_path}'. Missing closing bracket ']'."
                )

            index_text = attr_path[index + 1:close_idx].strip()
            if not index_text.isdigit():
                raise JsonAttributeError(
                    f"Invalid list index '{index_text}' in attr_path '{attr_path}'"
                )

            tokens.append(int(index_text))
            index = close_idx + 1
            continue

        current += char
        index += 1

    if current:
        tokens.append(current)

    if not tokens:
        raise JsonAttributeError(
            f"Invalid attr_path '{attr_path}'. Expected format 'key1.key2...'"
        )

    return tokens


def json_to_dict(json_str: str) -> Dict[str, Any]:
    """Converts a JSON string into a Python dictionary.
    Args:
        json_str: JSON string to be converted.

    Returns:
        A Python dictionary representing the JSON data.

    Raises:
        JsonConversionError: if the input is empty, is not a valid string,
            contains malformed JSON, or the JSON root is not an object.
    """
    if not isinstance(json_str, str):
        raise JsonConversionError(
            f"json_str must be of type str, got {type(json_str).__name__}"
        )

    if not json_str.strip():
        raise JsonConversionError("json_str cannot be empty")

    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise JsonConversionError(f"Invalid JSON string: {exc}") from exc

    if not isinstance(parsed, dict):
        raise JsonConversionError(
            f"Expected JSON object at root, got {type(parsed).__name__}"
        )

    return parsed


def dict_to_json(data: Dict[str, Any]) -> str:
    """Converts a Python dictionary into a JSON string.
    Args:
        data: Python dictionary to be converted.
    Returns:
        A JSON string representing the JSON data.

    Raises:
        JsonConversionError: if the input is not a dict or is not serializable.
    """
    if not isinstance(data, dict):
        raise JsonConversionError(
            f"data must be of type dict, got {type(data).__name__}"
        )

    try:
        return json.dumps(data, sort_keys=True, indent=4)
    except (TypeError, ValueError) as exc:
        raise JsonConversionError(f"Unable to serialize dictionary to JSON: {exc}") from exc

def get_attr(
    data: Dict[str, Any],
    attr_path: str,
    default: Any = None,
    *,
    strict: bool = False,
) -> Any:
    """Returns the value identified by the path `key1.key2...`.

    Args:
        data: Python dictionary.
        attr_path: attribute path in the format `key1.key2...`.
            Also supports list access, for example `items[0].id`.
        default: value returned when the path is not found and strict is False.
        strict: when True, raises JsonAttributeError if the path does not exist.
            When False (default), returns `default` instead.

    Returns:
        The value associated with the requested path, or `default` if not found
        and strict is False.

    Raises:
        JsonAttributeError: if `data` is not a dictionary, the path is empty,
            an intermediate node is not navigable, or a key/index does not exist
            and strict is True.

    Example::

        payload = {
            "payment": {
                "amount": {
                    "currency": "EUR"
                }
            }
        }

        get_attr(payload, "payment.amount.currency")
        # -> "EUR"

        get_attr({"items": [{"id": "A1"}]}, "items[0].id")
        # -> "A1"

        get_attr(payload, "payment.missing.key", default="N/A")
        # -> "N/A"

        get_attr(payload, "payment.missing.key", strict=True)
        # -> raises JsonAttributeError
    """
    if not isinstance(data, dict):
        raise JsonAttributeError(
            f"data must be of type dict, got {type(data).__name__}"
        )

    current: Any = data
    traversed_tokens: List[str] = []

    for token in _parse_attr_path(attr_path):
        if isinstance(token, int):
            traversed_tokens.append(f"[{token}]")
            current_path = "".join(traversed_tokens)

            if not isinstance(current, list):
                if strict:
                    raise JsonAttributeError(
                        f"Path '{current_path}' is not available: parent node is {type(current).__name__}, expected list"
                    )
                return default

            if token >= len(current):
                if strict:
                    raise JsonAttributeError(
                        f"Index '{current_path}' not found in payload"
                    )
                return default

            current = current[token]
            continue

        traversed_tokens.append(token if not traversed_tokens else f".{token}")
        current_path = "".join(traversed_tokens)

        if not isinstance(current, dict):
            if strict:
                raise JsonAttributeError(
                    f"Path '{current_path}' is not available: parent node is {type(current).__name__}, expected dict"
                )
            return default

        if token not in current:
            if strict:
                raise JsonAttributeError(
                    f"Attribute '{current_path}' not found in payload"
                )
            return default

        current = current[token]

    return current


def set_attr(
    data: Dict[str, Any],
    attr_path: str,
    value: Any,
    create_missing: bool = False,
) -> Dict[str, Any]:
    """Sets the value identified by the path `key1.key2...`.

    Args:
        data: Python dictionary to mutate.
        attr_path: attribute path in the format `key1.key2...`.
            Also supports list access, for example `items[0].id`.
        value: value to assign at the requested path.
        create_missing: when True, missing nodes are created automatically.
            When False (default), a missing path raises an error.

    Returns:
        The mutated dictionary.

    Raises:
        JsonAttributeSetError: if `data` is not a dictionary, the path is empty,
            a path segment does not exist and `create_missing` is False,
            an intermediate node is not navigable, or an existing node is not
            compatible with the expected container type.

    Example::

        payload = {}
        set_attr(payload, "items[0].id", "A1", create_missing=True)
        # -> {"items": [{"id": "A1"}]}
    """
    if not isinstance(data, dict):
        raise JsonAttributeSetError(
            f"data must be of type dict, got {type(data).__name__}"
        )

    try:
        tokens = _parse_attr_path(attr_path)
    except JsonAttributeError as exc:
        raise JsonAttributeSetError(str(exc)) from exc

    current: Any = data
    traversed_tokens: List[str] = []

    for index, token in enumerate(tokens[:-1]):
        next_token = tokens[index + 1]

        if isinstance(token, int):
            traversed_tokens.append(f"[{token}]")
            current_path = "".join(traversed_tokens)

            if not isinstance(current, list):
                raise JsonAttributeSetError(
                    f"Path '{current_path}' is not writable: parent node is {type(current).__name__}, expected list"
                )

            if token >= len(current):
                if not create_missing:
                    raise JsonAttributeSetError(
                        f"Index '{current_path}' not found in payload"
                    )

                while len(current) <= token:
                    current.append(None)

            if current[token] is None:
                if not create_missing:
                    raise JsonAttributeSetError(
                        f"Path '{current_path}' not found in payload"
                    )
                current[token] = [] if isinstance(next_token, int) else {}
            elif isinstance(next_token, int) and not isinstance(current[token], list):
                raise JsonAttributeSetError(
                    f"Path '{current_path}' is not writable: expected list, got {type(current[token]).__name__}"
                )
            elif isinstance(next_token, str) and not isinstance(current[token], dict):
                raise JsonAttributeSetError(
                    f"Path '{current_path}' is not writable: expected dict, got {type(current[token]).__name__}"
                )

            current = current[token]
            continue

        traversed_tokens.append(token if not traversed_tokens else f".{token}")
        current_path = "".join(traversed_tokens)

        if not isinstance(current, dict):
            raise JsonAttributeSetError(
                f"Path '{current_path}' is not writable: parent node is {type(current).__name__}, expected dict"
            )

        if token not in current or current[token] is None:
            if not create_missing:
                raise JsonAttributeSetError(
                    f"Attribute '{current_path}' not found in payload"
                )
            current[token] = [] if isinstance(next_token, int) else {}
        elif isinstance(next_token, int) and not isinstance(current[token], list):
            raise JsonAttributeSetError(
                f"Path '{current_path}' is not writable: expected list, got {type(current[token]).__name__}"
            )
        elif isinstance(next_token, str) and not isinstance(current[token], dict):
            raise JsonAttributeSetError(
                f"Path '{current_path}' is not writable: expected dict, got {type(current[token]).__name__}"
            )

        current = current[token]

    last_token = tokens[-1]

    if isinstance(last_token, int):
        if not isinstance(current, list):
            raise JsonAttributeSetError(
                f"Path '{attr_path}' is not writable: parent node is {type(current).__name__}, expected list"
            )

        if last_token >= len(current):
            if not create_missing:
                raise JsonAttributeSetError(
                    f"Index '{attr_path}' not found in payload"
                )

            while len(current) <= last_token:
                current.append(None)

        current[last_token] = value
        return data

    if not isinstance(current, dict):
        raise JsonAttributeSetError(
            f"Path '{attr_path}' is not writable: parent node is {type(current).__name__}, expected dict"
        )

    if not create_missing and last_token not in current:
        raise JsonAttributeSetError(
            f"Attribute '{attr_path}' not found in payload"
        )

    current[last_token] = value
    return data


