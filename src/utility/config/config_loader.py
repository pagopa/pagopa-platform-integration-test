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
            secret_value = secret_resolver.resolve(secret_name)
            return secret_value
        return value

    # Ricorsione su oggetti JSON annidati.
    if isinstance(value, dict):
        return {k: _resolve_value(v, secret_resolver) for k, v in value.items()}

    if isinstance(value, list):
        return [_resolve_value(item, secret_resolver) for item in value]

    # Numeri, booleani, null ecc. restano invariati.
    return value


def load_json_config(path: str | Path, secret_resolver: Any) -> Dict[str, Any]:
    """
    Legge un file JSON e risolve i placeholder segreti del tipo "$var_name".

    I valori nel JSON scritti come "$nome_variabile" vengono sostituiti
    con il valore reale restituito da secret_resolver.resolve("nome_variabile").
    La sostituzione è ricorsiva su tutto il documento (dict, list, valori).
    Valori non stringa (numeri, booleani, null) restano invariati.

    Args:
        path: percorso del file JSON (assoluto o relativo alla CWD).
        secret_resolver: oggetto con metodo resolve(secret_name: str) -> Any.

    Returns:
        Dizionario Python con segreti già sostituiti.

    Raises:
        JsonConfigLoaderError: se il file non esiste o contiene JSON non valido.

    Esempio di file JSON::

        {
            "service": {
                "url": "https://api.example.com",
                "timeout": 30
            },
            "auth": {
                "type": "oauth2",
                "client_id": "my-client",
                "client_secret": "$oauth_client_secret"
            }
        }

    Esempio d'uso::

        from src.utility.config.config_loader import load_json_config
        from src.utility.config.secrets import DictSecretResolver

        resolver = DictSecretResolver({"oauth_client_secret": "super-secret"})
        config = load_json_config("config/tests/service.json", resolver)

        # config["auth"]["client_secret"] → "super-secret"
        # config["service"]["url"] → "https://api.example.com"
    """
    file_path = Path(path)

    if not file_path.exists():
        raise JsonConfigLoaderError(f"JSON config file not found: {file_path}")

    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise JsonConfigLoaderError(
            f"Invalid JSON in file {file_path}: {exc}"
        ) from exc

    return _resolve_value(raw, secret_resolver)


def load_test_config(secret_resolver: Any) -> Dict[str, Any]:
    """
    Carica il file JSON di configurazione il cui percorso è definito
    nella variabile d'ambiente TEST_CONFIG_FILE.

    Permette di selezionare il file di test al momento del lancio senza
    modificare il codice, rendendo la stessa suite eseguibile con
    configurazioni diverse (es. ambienti dev/uat/prod).

    Args:
        secret_resolver: oggetto con metodo resolve(secret_name: str) -> Any.

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
