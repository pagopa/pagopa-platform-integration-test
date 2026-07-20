from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict


# ============================================================================
# Variabile d'ambiente per la selezione del file di configurazione
# ============================================================================
# Il percorso del file JSON da caricare viene passato tramite la variabile
# d'ambiente TEST_CONFIG_FILE, così è possibile selezionarlo a runtime
# senza modificare il codice.
#
# Esempio:
#   TEST_CONFIG_FILE=config/tests/my_service.json behave src/...
#
# ============================================================================
TARGET_ENV_VAR = "TARGET_ENV"
SUITE_ENV_VAR = "suite"
SUITE_FILE_PATH_PREFIX = "config/suites/{suite}_config.json"

# ============================================================================
# Placeholder format
# ============================================================================
# I valori nel JSON possono essere scritti come:
#   "$var_name"
#
# Durante il caricamento, tali placeholder vengono sostituiti con il secret
# corrispondente recuperato tramite il resolver passato al loader.


SECRET_PLACEHOLDER_PATTERN = re.compile(r"^\$(?P<name>[A-Za-z0-9_-]+)$")


class JsonConfigLoaderError(Exception):
    """Eccezione del loader di configurazione JSON."""
    pass


class AttributeDict(dict):
    """Dictionary with recursive attribute-style access support."""

    def __getattr__(self, item: str) -> Any:
        """Return dictionary items using attribute access."""
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc

    def __setattr__(self, key: str, value: Any) -> None:
        """Allow assigning dictionary items via attributes."""
        self[key] = value

    def __delattr__(self, item: str) -> None:
        """Allow deleting dictionary items via attributes."""
        try:
            del self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc


def _to_attribute_dict(value: Any) -> Any:
    """Recursively convert dict and list nodes to AttributeDict."""
    if isinstance(value, dict):
        return AttributeDict({k: _to_attribute_dict(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_to_attribute_dict(item) for item in value]
    return value


def _resolve_value(value: Any, secret_resolver: Any) -> Any:
    # Se il valore è una stringa del tipo "$nome_secret", lo sostituiamo.
    if isinstance(value, str):
        match = SECRET_PLACEHOLDER_PATTERN.match(value)
        if match:
            secret_name = match.group("name")

            # Support both a single resolver and a list/tuple of resolvers.
            resolvers = (
                list(secret_resolver)
                if isinstance(secret_resolver, (list, tuple))
                else [secret_resolver]
            )

            last_exc: Exception | None = None
            for resolver in resolvers:
                if resolver is None:
                    continue
                try:
                    resolve_fn = getattr(resolver, "resolve", None)
                    if not callable(resolve_fn):
                        continue
                    secret_value = resolve_fn(secret_name)
                except Exception as exc:  # defensive: skip resolver on error
                    last_exc = exc
                    continue

                # Treat any non-None return as a successful resolution.
                if secret_value is not None:
                    return secret_value

            # If none of the resolvers returned a value, raise an informative error.
            if last_exc:
                raise JsonConfigLoaderError(
                    f"Secret '{secret_name}' not resolved by any resolver (last error: {last_exc})."
                )
            raise JsonConfigLoaderError(
                f"Secret '{secret_name}' not found in any provided resolver."
            )
        return value

    # Ricorsione su oggetti JSON annidati.
    if isinstance(value, dict):
        return {k: _resolve_value(v, secret_resolver) for k, v in value.items()}

    if isinstance(value, list):
        return [_resolve_value(item, secret_resolver) for item in value]

    # Numeri, booleani, null ecc. restano invariati.
    return value

    
def _coerce_scalar_or_json(text: str) -> Any:
    """Return the parsed value if it is a JSON object/array, else the raw string.

    Bare scalars (URLs, numbers, fiscal/notice codes) are intentionally kept as
    strings so callers relying on their string form are not affected; structured
    values (JSON objects/arrays) are parsed so they can be consumed directly.
    """
    try:
        parsed = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return text
    if isinstance(parsed, (dict, list)):
        return parsed
    return text


def _parse_key_value_content(raw_content: str, file_path: Path) -> Dict[str, Any]:
    """Parse a ``KEY=VALUE`` / ``KEY:VALUE`` configuration file.

    Supports comments (``#``), blank lines, and single- or double-quoted values
    that may span multiple lines (e.g. an embedded JSON blob). Values are kept as
    strings unless they are valid JSON objects/arrays (see ``_coerce_scalar_or_json``).
    """
    result: Dict[str, Any] = {}
    lines = raw_content.splitlines()
    index = 0
    total = len(lines)

    while index < total:
        raw_line = lines[index]
        index += 1
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        eq_pos = raw_line.find("=")
        colon_pos = raw_line.find(":")
        separators = [pos for pos in (eq_pos, colon_pos) if pos != -1]
        if not separators:
            raise JsonConfigLoaderError(
                f"Invalid configuration line (missing '=' or ':' separator) "
                f"in file {file_path}: {stripped!r}"
            )

        sep = min(separators)
        key = raw_line[:sep].strip()
        value = raw_line[sep + 1:].strip()

        if value[:1] in ("'", '"'):
            quote = value[0]
            body = value[1:]
            close = body.find(quote)
            if close != -1:
                value = body[:close]
            else:
                parts = [body]
                closed = False
                while index < total:
                    next_line = lines[index]
                    index += 1
                    close = next_line.find(quote)
                    if close != -1:
                        parts.append(next_line[:close])
                        closed = True
                        break
                    parts.append(next_line)
                if not closed:
                    raise JsonConfigLoaderError(
                        f"Unterminated quoted value for key '{key}' in file {file_path}."
                    )
                value = "\n".join(parts)

        result[key] = _coerce_scalar_or_json(value)

    return result


def _parse_config_content(raw_content: str, file_path: Path) -> Dict[str, Any]:
    """Parse a full JSON object, falling back to ``KEY=VALUE`` / ``KEY:VALUE``."""
    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        return _parse_key_value_content(raw_content, file_path)

    if not isinstance(parsed, dict):
        raise JsonConfigLoaderError(
            f"JSON root must be an object in file {file_path}."
        )
    return parsed


def load_json_config(secret_resolver: Any | list[Any]) -> Dict[str, Any]:
    """
    Legge un file di configurazione e risolve i placeholder "$var_name".

    Formati supportati:
    - JSON object completo
    - key:value (una coppia per riga)

    Nel formato key:value il valore puo' essere stringa o JSON valido.
    Esempio key:value:
        service_url:https://api.example.com
        timeout:30
        verify_ssl:true
        default_headers:{"Content-Type":"application/json"}
        oauth2:{"client_id":"my-client","client_secret":"$oauth_client_secret"}
    """
   
    if(os.getenv(TARGET_ENV_VAR) is None or os.getenv(TARGET_ENV_VAR) == "") or (os.getenv(SUITE_ENV_VAR) is None or os.getenv(SUITE_ENV_VAR) == ""):
        raise JsonConfigLoaderError(f"Environment variable '{TARGET_ENV_VAR}' or '{SUITE_ENV_VAR}' is not set. Set them to the target environment (e.g., 'uat', 'dev') and suite (e.g., 'wisp', 'cup').")

    suite_file_path = Path(SUITE_FILE_PATH_PREFIX.replace("{suite}", os.getenv(SUITE_ENV_VAR)))
    if not suite_file_path.exists():
        raise JsonConfigLoaderError(f"Config file not found: {suite_file_path}")

    suite_content = suite_file_path.read_text(encoding="utf-8")
   
    parsed_content = _parse_config_content(suite_content, suite_file_path).get(str(os.getenv(TARGET_ENV_VAR)).lower(), {})

    if not parsed_content:
        raise JsonConfigLoaderError(
            f"Impossible to find or parse configuration for environment '{os.getenv(TARGET_ENV_VAR)}' and suite '{os.getenv(SUITE_ENV_VAR)}' in file {suite_file_path}."
        )

    resolved = _resolve_value(parsed_content, secret_resolver)
    return _to_attribute_dict(resolved)
    
