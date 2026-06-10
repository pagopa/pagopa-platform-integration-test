from __future__ import annotations

from typing import Any, Mapping, Optional

from src.utility.rest.oauth2_token_provider import (
    OAuth2TokenProvider,
    OAuth2TokenRequestConfig,
)
from src.utility.rest.rest_client import (
    AuthConfig,
    NoAuthConfig,
    OAuth2ClientCredentialsConfig,
    RestClient,
    RestClientConfig,
)


# ============================================================================
# Factory del client REST
# ============================================================================
# Questa factory NON legge variabili d'ambiente né file di configurazione.
# Riceve direttamente un nodo di configurazione già caricato tramite
# `src.utility.config.config_loader.load_json_config / load_test_config`.
#
# Struttura attesa di service_config:
# {
#     "url": "https://api.example.com",
#     "timeout": 30,           (opzionale, default 30)
#     "verify_ssl": true,      (opzionale, default true)
#     "default_headers": {}    (opzionale)
# }
#
# Se auth_config è di tipo OAuth2ClientCredentialsConfig, la factory crea
# automaticamente un OAuth2TokenProvider e lo inietta nel client.
# Il provider gestisce cache e rinnovo automatico del token.


def build_rest_client(
    service_config: Mapping[str, Any],
    auth_config: Optional[AuthConfig] = None,
) -> RestClient:
    """
    Crea un RestClient a partire dal nodo di configurazione del servizio
    e dall'eventuale configurazione di autenticazione.

    Se auth_config è OAuth2ClientCredentialsConfig, la factory crea
    automaticamente un OAuth2TokenProvider e lo inietta nel client.
    Il token viene recuperato al primo utilizzo e rinnovato automaticamente
    quando scade.

    Args:
        service_config: dict con "url" obbligatorio; "timeout", "verify_ssl" e
                        "default_headers" opzionali. Solitamente è il nodo
                        config["service"] caricato da load_test_config().
        auth_config: configurazione di autenticazione costruita tramite
                     rest_auth_factory. Se None, il client usa NoAuthConfig.

    Returns:
        RestClient pronto all'uso.

    Esempio senza autenticazione::

        from src.utility.rest.rest_client_factory import build_rest_client
        from src.utility.rest.rest_auth_factory import build_no_auth

        client = build_rest_client(config["service"], build_no_auth())
        response = client.get("/health")

    Esempio con Basic Auth::

        from src.utility.rest.rest_auth_factory import build_basic_auth_from_config

        client = build_rest_client(
            config["service"],
            build_basic_auth_from_config(config["auth"]["basic"]),
        )
        response = client.get("/private")

    Esempio con API Key::

        from src.utility.rest.rest_auth_factory import build_api_key_auth_from_config

        client = build_rest_client(
            config["service"],
            build_api_key_auth_from_config(config["auth"]["api_key"]),
        )

    Esempio con OAuth2 (token gestito automaticamente)::

        from src.utility.rest.rest_auth_factory import build_oauth2_client_credentials_from_config

        client = build_rest_client(
            config["service"],
            build_oauth2_client_credentials_from_config(config["auth"]["oauth2"]),
        )
        # Il token viene richiesto al primo utilizzo, poi è cached e rinnovato automaticamente
        response = client.get("/protected")

    Esempio completo in environment.py di Behave::

        from src.utility.config import load_test_config
        from src.utility.config.secrets import DictSecretResolver
        from src.utility.rest.rest_client_factory import build_rest_client
        from src.utility.rest.rest_auth_factory import build_oauth2_client_credentials_from_config

        def before_all(context):
            resolver = DictSecretResolver({"client_secret": "super-secret"})
            config = load_test_config(resolver)

            auth = build_oauth2_client_credentials_from_config(config["auth"]["oauth2"])
            context.rest_client = build_rest_client(config["service"], auth)
    """
    rest_config = RestClientConfig(
        base_url=service_config["url"],
        timeout=service_config.get("timeout", 30),
        verify_ssl=service_config.get("verify_ssl", True),
        default_headers=service_config.get("default_headers", {}),
    )

    # Se l'autenticazione è OAuth2, creiamo il token provider che gestirà
    # autonomamente il recupero e il rinnovo del token a ogni chiamata.
    token_provider: Optional[OAuth2TokenProvider] = None

    if isinstance(auth_config, OAuth2ClientCredentialsConfig):
        token_provider = OAuth2TokenProvider(
            config=OAuth2TokenRequestConfig(
                token_url=auth_config.token_url,
                client_id=auth_config.client_id,
                client_secret=auth_config.client_secret,
                scope=auth_config.scope,
                audience=auth_config.audience,
                extra_token_data=auth_config.extra_token_data,
            ),
            timeout=rest_config.timeout,
            verify_ssl=rest_config.verify_ssl,
        )

    return RestClient(
        config=rest_config,
        auth_config=auth_config or NoAuthConfig(),
        token_provider=token_provider,
    )
