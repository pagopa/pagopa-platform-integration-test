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
TEST_CONFIG_FILE_ENV_VAR = "TEST_CONFIG_FILE"


# ============================================================================
# Placeholder format
# ============================================================================
# I valori nel JSON possono essere scritti come:
#   "$var_name"
#
# Durante il caricamento, tali placeholder vengono sostituiti con il secret
# corrispondente recuperato tramite il resolver passato al loader.


SECRET_PLACEHOLDER_PATTERN = re.compile(r"^\$(?P<name>[A-Za-z0-9_]+)$")


class JsonConfigLoaderError(Exception):
    """Eccezione del loader di configurazione JSON."""
    pass


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


def _parse_key_value_config(raw_content: str) -> Dict[str, Any]:
    """Parse formato key:value o key=value, con supporto valori JSON/stringa."""
    parsed: Dict[str, Any] = {}

    lines = raw_content.splitlines()
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        line_number = i + 1
        line = raw_line.strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        idx_colon = raw_line.find(":")
        idx_equal = raw_line.find("=")
        if idx_colon == -1 and idx_equal == -1:
            raise JsonConfigLoaderError(
                f"Invalid config line at {line_number}: '{raw_line}'. Expected 'key:value' or 'key=value'."
            )

        if idx_equal != -1 and (idx_colon == -1 or idx_equal < idx_colon):
            key, raw_value = raw_line.split("=", 1)
        else:
            key, raw_value = raw_line.split(":", 1)

        key = key.strip()
        value_text = raw_value.strip()

        if not key:
            raise JsonConfigLoaderError(
                f"Invalid empty key at line {line_number}: '{raw_line}'."
            )

        if value_text.startswith(("'", '"')):
            quote = value_text[0]
            if len(value_text) >= 2 and value_text.endswith(quote):
                value_text = value_text[1:-1]
            else:
                buffer = [value_text[1:]]
                i += 1
                closed = False
                while i < len(lines):
                    current = lines[i]
                    if current.endswith(quote):
                        buffer.append(current[:-1])
                        closed = True
                        break
                    buffer.append(current)
                    i += 1

                if not closed:
                    raise JsonConfigLoaderError(
                        f"Unclosed multiline quoted value for key '{key}' at line {line_number}."
                    )
                value_text = "\n".join(buffer)

        # Se il valore e' JSON valido lo converte, altrimenti resta stringa raw.
        try:
            value = json.loads(value_text)
        except json.JSONDecodeError:
            value = value_text

        parsed[key] = value
        i += 1

    return parsed


def _parse_config_content(raw_content: str, file_path: Path) -> Dict[str, Any]:
    """Parse JSON object completo, altrimenti fallback a key:value."""
    try:
        parsed = json.loads(raw_content)
        if not isinstance(parsed, dict):
            raise JsonConfigLoaderError(
                f"JSON root must be an object in file {file_path}."
            )
        return parsed
    except json.JSONDecodeError:
        return _parse_key_value_config(raw_content)


def load_json_config(path: str | Path, secret_resolver: Any | list[Any]) -> Dict[str, Any]:
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
    # Notes:
    #     `secret_resolver` può essere un singolo resolver oppure una lista/tupla
    #     di resolver; in quest'ultimo caso vengono interrogati in ordine e la
    #     prima risoluzione non-`None` viene utilizzata.
    file_path = Path(path)

    if not file_path.exists():
        raise JsonConfigLoaderError(f"Config file not found: {file_path}")

    raw_content = file_path.read_text(encoding="utf-8")
    raw = _parse_config_content(raw_content, file_path)

    return _resolve_value(raw, secret_resolver)


def load_test_config(secret_resolver: Any | list[Any]) -> Dict[str, Any]:
    """
    Carica il file JSON di configurazione il cui percorso è definito
    nella variabile d'ambiente TEST_CONFIG_FILE.

    Permette di selezionare il file di test al momento del lancio senza
    modificare il codice, rendendo la stessa suite eseguibile con
    configurazioni diverse (es. ambienti dev/uat/prod).

    Args:
        secret_resolver: oggetto (o lista di oggetti) con metodo
            `resolve(secret_name: str) -> Any`. Se viene passata una lista, i
            resolver vengono interrogati in ordine.

    Returns:
        Dizionario Python con segreti già sostituiti.

    Raises:
        JsonConfigLoaderError: se TEST_CONFIG_FILE non è impostata o il file non esiste.

    Esempio di lancio (PowerShell)::

        $env:TEST_CONFIG_FILE = "config/tests/service_dev.json"
        behave src/api/my-service

    Esempio di lancio (bash)::

        TEST_CONFIG_FILE=config/tests/service_uat.json behave src/api/my-service

    Esempio in environment.py di Behave::

        from src.utility.config.config_loader import load_test_config
        from src.utility.config.secrets import DictSecretResolver, AzureKeyVaultSecretResolver

        def before_all(context):
            # In locale usa DictSecretResolver, in CI usa AzureKeyVaultSecretResolver
            if os.environ.get("CI"):
                resolver = AzureKeyVaultSecretResolver()
            else:
                resolver = DictSecretResolver({"client_secret": "local-secret"})

            context.test_config = load_test_config(resolver)
    """
    config_file = os.environ.get(TEST_CONFIG_FILE_ENV_VAR)
    if not config_file:
        raise JsonConfigLoaderError(
            f"Environment variable '{TEST_CONFIG_FILE_ENV_VAR}' is not set. "
            f"Set it to the path of the JSON config file to use for the tests."
        )
    return load_json_config(config_file, secret_resolver)
