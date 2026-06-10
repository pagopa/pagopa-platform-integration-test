from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class SecretResolver(ABC):
    """
    Interfaccia astratta per il recupero dei secret.

    Tutte le implementazioni concrete devono implementare il metodo resolve().
    Il resolver viene passato a load_json_config / load_test_config per sostituire
    i placeholder "$nome_variabile" presenti nel file JSON di configurazione.

    Esempio di implementazione custom::

        class EnvSecretResolver(SecretResolver):
            def resolve(self, secret_name: str) -> Any:
                value = os.environ.get(secret_name)
                if value is None:
                    raise KeyError(f"Env var not set: {secret_name}")
                return value
    """

    @abstractmethod
    def resolve(self, secret_name: str) -> Any:
        """
        Restituisce il valore del secret identificato da secret_name.

        Args:
            secret_name: nome del secret (corrisponde alla parte dopo "$" nel JSON).

        Returns:
            Il valore del secret.

        Raises:
            KeyError: se il secret non esiste.
        """
        raise NotImplementedError


class DictSecretResolver(SecretResolver):
    """
    Implementazione semplice basata su un dizionario.
    Utile per test locali e per mocking nei test Behave.

    Esempio::

        resolver = DictSecretResolver({
            "db_password": "my-secret-password",
            "api_key": "my-api-key",
            "oauth_client_secret": "my-oauth-secret",
        })

        # Uso diretto
        value = resolver.resolve("db_password")  # → "my-secret-password"

        # Uso con il config loader
        config = load_json_config("config/tests/service.json", resolver)

    Esempio in environment.py di Behave::

        def before_all(context):
            context.secret_resolver = DictSecretResolver({
                "client_secret": "super-secret",
                "api_key": "test-key",
            })
            context.test_config = load_test_config(context.secret_resolver)
    """

    def __init__(self, secrets: Dict[str, Any]):
        self._secrets = secrets

    def resolve(self, secret_name: str) -> Any:
        """
        Restituisce il valore associato a secret_name nel dizionario.

        Args:
            secret_name: chiave del dizionario secrets.

        Returns:
            Il valore corrispondente.

        Raises:
            KeyError: se secret_name non è presente nel dizionario.

        Esempio::

            resolver = DictSecretResolver({"token": "abc123"})
            resolver.resolve("token")   # → "abc123"
            resolver.resolve("missing") # → KeyError: Secret not found: missing
        """
        if secret_name not in self._secrets:
            raise KeyError(f"Secret not found: {secret_name}")
        return self._secrets[secret_name]