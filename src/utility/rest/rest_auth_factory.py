from typing import Any, Mapping, Optional

from src.utility.rest.rest_client import (
    ApiKeyAuthConfig,
    ApiKeyLocation,
    BasicAuthConfig,
    NoAuthConfig,
    OAuth2ClientCredentialsConfig,
)


# ============================================================================
# Utility di supporto
# ============================================================================


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
        raise RuntimeError(f"Missing required configuration value: {key}")
    return value


# ============================================================================
# Auth builders espliciti
# ============================================================================
# Usati dagli step Behave quando i valori sono noti a compile-time
# o passati direttamente come parametri dello step.


def build_no_auth() -> NoAuthConfig:
    """
    Crea una configurazione senza autenticazione.

    Esempio::

        auth = build_no_auth()
        client = build_rest_client(config["service"], auth)
    """
    return NoAuthConfig()


def build_basic_auth(username: str, password: str) -> BasicAuthConfig:
    """
    Crea una configurazione Basic Auth con le credenziali specificate.

    Args:
        username: nome utente.
        password: password.

    Returns:
        BasicAuthConfig pronto da passare a build_rest_client.

    Esempio::

        auth = build_basic_auth("my-user", "my-password")
        client = build_rest_client(config["service"], auth)

    Esempio in uno step Behave::

        @given('la richiesta usa basic auth con username "{user}" e password "{pwd}"')
        def step_basic_auth(context, user, pwd):
            context.auth = build_basic_auth(user, pwd)
    """
    return BasicAuthConfig(username=username, password=password)


def build_api_key_auth(
        key_name: str,
        key_value: str,
        location: str = "header",
) -> ApiKeyAuthConfig:
    """
    Crea una configurazione API Key con nome, valore e posizione specificati.

    Args:
        key_name: nome dell'header o del query parameter.
        key_value: valore della chiave.
        location: "header" (default) o "query".

    Returns:
        ApiKeyAuthConfig pronto da passare a build_rest_client.

    Esempio su header::

        auth = build_api_key_auth("x-api-key", "secret-value")
        client = build_rest_client(config["service"], auth)

    Esempio su query parameter::

        auth = build_api_key_auth("apikey", "secret-value", location="query")
        # produce: GET /resource?apikey=secret-value
    """
    return ApiKeyAuthConfig(
        key_name=key_name,
        key_value=key_value,
        location=ApiKeyLocation(location),
    )


def build_oauth2_client_credentials(
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: Optional[str] = None,
        audience: Optional[str] = None,
) -> OAuth2ClientCredentialsConfig:
    """
    Crea una configurazione OAuth2 client credentials con parametri espliciti.

    Args:
        token_url: URL del token endpoint.
        client_id: client ID OAuth2.
        client_secret: client secret OAuth2.
        scope: scope opzionale.
        audience: audience opzionale.

    Returns:
        OAuth2ClientCredentialsConfig pronto da passare a build_rest_client.

    Esempio::

        auth = build_oauth2_client_credentials(
            token_url="https://auth.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scope="read write",
        )
        client = build_rest_client(config["service"], auth)
    """
    return OAuth2ClientCredentialsConfig(
        token_url=token_url,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        audience=audience,
    )


# ============================================================================
# Auth builders da configurazione JSON già caricata
# ============================================================================
# Questi helper ricevono un nodo del dizionario già caricato da config_loader,
# con i placeholder "$..." già sostituiti.
#
# Struttura attesa nel JSON di test:
#
#   "auth": {
#     "basic":   { "username": "...", "password": "..." },
#     "api_key": { "key_name": "...", "key_value": "...", "location": "header" },
#     "oauth2":  { "token_url": "...", "client_id": "...", "client_secret": "..." }
#   }


def build_basic_auth_from_config(config_node: Any) -> BasicAuthConfig:
    """
    Crea BasicAuthConfig da un nodo di configurazione già caricato.

    Args:
        config_node: dict o oggetto con chiavi "username" e "password".

    Returns:
        BasicAuthConfig pronto da passare a build_rest_client.

    Esempio::

        # JSON: { "username": "user", "password": "$api_password" }
        config = load_test_config(resolver)
        auth = build_basic_auth_from_config(config["auth"]["basic"])
        client = build_rest_client(config["service"], auth)
    """
    return BasicAuthConfig(
        username=_get_required_value(config_node, "username"),
        password=_get_required_value(config_node, "password"),
    )


def build_api_key_auth_from_config(config_node: Any) -> ApiKeyAuthConfig:
    """
    Crea ApiKeyAuthConfig da un nodo di configurazione già caricato.

    Args:
        config_node: dict o oggetto con chiavi "key_name", "key_value" e "location" (opzionale).

    Returns:
        ApiKeyAuthConfig pronto da passare a build_rest_client.

    Esempio::

        # JSON: { "key_name": "x-api-key", "key_value": "$api_key", "location": "header" }
        config = load_test_config(resolver)
        auth = build_api_key_auth_from_config(config["auth"]["api_key"])
        client = build_rest_client(config["service"], auth)
    """
    return ApiKeyAuthConfig(
        key_name=_get_required_value(config_node, "key_name"),
        key_value=_get_required_value(config_node, "key_value"),
        location=ApiKeyLocation(_get_value(config_node, "location", "header")),
    )


def build_oauth2_client_credentials_from_config(
        config_node: Any,
) -> OAuth2ClientCredentialsConfig:
    """
    Crea OAuth2ClientCredentialsConfig da un nodo di configurazione già caricato.

    Args:
        config_node: dict o oggetto con chiavi "token_url", "client_id", "client_secret"
                     e opzionalmente "scope" e "audience".

    Returns:
        OAuth2ClientCredentialsConfig pronto da passare a build_rest_client.

    Esempio::

        # JSON:
        # {
        #   "token_url": "https://auth.example.com/oauth/token",
        #   "client_id": "my-client",
        #   "client_secret": "$oauth_secret",
        #   "scope": "read write"
        # }
        config = load_test_config(resolver)
        auth = build_oauth2_client_credentials_from_config(config["auth"]["oauth2"])
        client = build_rest_client(config["service"], auth)
    """
    return OAuth2ClientCredentialsConfig(
        token_url=_get_required_value(config_node, "token_url"),
        client_id=_get_required_value(config_node, "client_id"),
        client_secret=_get_required_value(config_node, "client_secret"),
        scope=_get_value(config_node, "scope"),
        audience=_get_value(config_node, "audience"),
    )