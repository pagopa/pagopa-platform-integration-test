from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Union

import requests
from requests import Response, Session
from requests.auth import HTTPBasicAuth

from src.utility.rest.oauth2_token_provider import OAuth2TokenProvider


# ============================================================================
# Enumerazioni di supporto
# ============================================================================


class AuthType(str, Enum):
    NONE = "none"
    BASIC = "basic"
    API_KEY = "api_key"
    OAUTH2_CLIENT_CREDENTIALS = "oauth2_client_credentials"


class ApiKeyLocation(str, Enum):
    HEADER = "header"
    QUERY = "query"


# ============================================================================
# Configurazioni di autenticazione
# ============================================================================
# Ogni dataclass descrive i parametri necessari per un tipo di autenticazione.
# Il tipo viene fissato alla costruzione del client, non per singola chiamata.


@dataclass
class NoAuthConfig:
    """
    Configurazione per richieste senza autenticazione.

    Esempio::

        from src.utility.rest.rest_auth_factory import build_no_auth
        auth = build_no_auth()
    """
    auth_type: AuthType = AuthType.NONE


@dataclass
class BasicAuthConfig:
    """
    Configurazione per autenticazione HTTP Basic.

    Esempio::

        from src.utility.rest.rest_auth_factory import build_basic_auth
        auth = build_basic_auth("user", "password")
    """
    username: str
    password: str
    auth_type: AuthType = AuthType.BASIC


@dataclass
class ApiKeyAuthConfig:
    """
    Configurazione per autenticazione tramite API Key.

    Esempio su header::

        from src.utility.rest.rest_auth_factory import build_api_key_auth
        auth = build_api_key_auth("x-api-key", "my-key")

    Esempio su query parameter::

        auth = build_api_key_auth("apikey", "my-key", location="query")
    """
    key_name: str
    key_value: str
    location: ApiKeyLocation = ApiKeyLocation.HEADER
    auth_type: AuthType = AuthType.API_KEY


@dataclass
class OAuth2ClientCredentialsConfig:
    """
    Configurazione per autenticazione OAuth2 client credentials.

    Il token viene gestito automaticamente dal RestClient tramite
    OAuth2TokenProvider: recupero, cache e rinnovo sono trasparenti.

    Esempio::

        from src.utility.rest.rest_auth_factory import build_oauth2_client_credentials
        auth = build_oauth2_client_credentials(
            token_url="https://auth.example.com/oauth/token",
            client_id="my-client",
            client_secret="my-secret",
            scope="read write",
        )
    """
    # Credenziali necessarie per richiedere un token al token endpoint.
    token_url: str
    client_id: str
    client_secret: str
    scope: Optional[str] = None
    audience: Optional[str] = None
    extra_token_data: Dict[str, Any] = field(default_factory=dict)
    auth_type: AuthType = AuthType.OAUTH2_CLIENT_CREDENTIALS


AuthConfig = Union[
    NoAuthConfig,
    BasicAuthConfig,
    ApiKeyAuthConfig,
    OAuth2ClientCredentialsConfig,
]


# ============================================================================
# Configurazione base del client
# ============================================================================


@dataclass
class RestClientConfig:
    """
    Configurazione infrastrutturale del client REST.

    Contiene solo parametri di connessione; l'autenticazione è separata.

    Esempio::

        config = RestClientConfig(
            base_url="https://api.example.com",
            timeout=30,
            verify_ssl=True,
            default_headers={"Content-Type": "application/json"},
        )
    """
    base_url: str
    timeout: int = 30
    verify_ssl: bool = True
    default_headers: Dict[str, str] = field(default_factory=dict)


class RestClientError(Exception):
    """Eccezione applicativa del client REST."""
    pass


# ============================================================================
# Client REST
# ============================================================================
# Il client viene istanziato con:
#   - RestClientConfig: base_url, timeout, ssl, header di default
#   - auth_config: tipo e parametri di autenticazione (fissi per l'istanza)
#   - token_provider: necessario solo per OAuth2, creato dalla factory
#
# Per OAuth2, ogni chiamata HTTP verifica la validità del token tramite
# il token_provider. Se il token è scaduto o prossimo alla scadenza,
# il provider ne richiede automaticamente uno nuovo.


class RestClient:
    """
    Client HTTP con supporto a Basic Auth, API Key e OAuth2 client credentials.

    Non deve essere istanziato direttamente: usa build_rest_client()
    per ottenere un'istanza correttamente configurata.

    Esempio base (nessuna auth)::

        from src.utility.rest import build_rest_client
        from src.utility.rest.rest_auth_factory import build_no_auth

        client = build_rest_client(config["service"], build_no_auth())
        response = client.get("/health")
        print(response.status_code)

    Esempio con Basic Auth::

        from src.utility.rest.rest_auth_factory import build_basic_auth

        client = build_rest_client(config["service"], build_basic_auth("user", "pass"))
        response = client.post("/resource", json_body={"name": "test"})

    Esempio con OAuth2 (token gestito automaticamente)::

        from src.utility.rest.rest_auth_factory import build_oauth2_client_credentials_from_config

        auth = build_oauth2_client_credentials_from_config(config["auth"]["oauth2"])
        client = build_rest_client(config["service"], auth)

        # Il token viene richiesto al primo utilizzo e rinnovato automaticamente
        response = client.get("/protected-resource")
        response = client.get("/another-resource")  # usa il token in cache

    Esempio in environment.py di Behave::

        def before_all(context):
            config = load_test_config(resolver)
            auth = build_oauth2_client_credentials_from_config(config["auth"]["oauth2"])
            context.rest_client = build_rest_client(config["service"], auth)

        def before_scenario(context, scenario):
            context.response = None
    """

    def __init__(
        self,
        config: RestClientConfig,
        auth_config: Optional[AuthConfig] = None,
        token_provider: Optional[OAuth2TokenProvider] = None,
    ):
        self.config = config
        self.auth_config = auth_config or NoAuthConfig()
        self.session: Session = requests.Session()
        self.session.headers.update(config.default_headers or {})

        # Il token_provider è richiesto solo quando auth_type è OAUTH2_CLIENT_CREDENTIALS.
        # La factory lo crea e lo inietta; il client non lo costruisce da solo.
        self._token_provider = token_provider

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _prepare_auth(
        self,
        headers: Dict[str, str],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Prepara i parametri di autenticazione per la singola request.

        - NONE: nessuna modifica
        - BASIC: aggiunge HTTPBasicAuth
        - API_KEY: aggiunge la chiave in header o query param
        - OAUTH2: ottiene il token valido dal provider (con rinnovo automatico)
        """
        request_kwargs: Dict[str, Any] = {}

        if self.auth_config.auth_type == AuthType.NONE:
            return request_kwargs

        if self.auth_config.auth_type == AuthType.BASIC:
            request_kwargs["auth"] = HTTPBasicAuth(
                self.auth_config.username,
                self.auth_config.password,
            )
            return request_kwargs

        if self.auth_config.auth_type == AuthType.API_KEY:
            if self.auth_config.location == ApiKeyLocation.HEADER:
                headers[self.auth_config.key_name] = self.auth_config.key_value
            else:
                params[self.auth_config.key_name] = self.auth_config.key_value
            return request_kwargs

        if self.auth_config.auth_type == AuthType.OAUTH2_CLIENT_CREDENTIALS:
            if self._token_provider is None:
                raise RestClientError(
                    "OAuth2 auth requires a token_provider. "
                    "Use build_rest_client() to instantiate the client correctly."
                )
            # get_token() gestisce internamente cache e rinnovo automatico.
            token = self._token_provider.get_token()
            headers["Authorization"] = f"Bearer {token}"
            return request_kwargs

        raise RestClientError(f"Unsupported auth type: {self.auth_config.auth_type}")

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Any] = None,
        form_data: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        """
        Esegue una richiesta HTTP con il metodo specificato.

        L'autenticazione viene applicata automaticamente a ogni chiamata.
        Per OAuth2, il token viene rinnovato se è scaduto o in scadenza.

        Args:
            method: verbo HTTP ("GET", "POST", "PUT", "PATCH", "DELETE").
            path: path relativo alla base_url, o URL assoluto.
            headers: header aggiuntivi per questa chiamata (si sommano ai default).
            params: query parameters.
            json_body: body serializzato come JSON.
            form_data: body come form data (application/x-www-form-urlencoded).
            data: body raw (stringa, bytes, ecc.).
            timeout: timeout in secondi (sovrascrive il default del client).

        Returns:
            requests.Response con il risultato della chiamata.

        Esempio::

            response = client.request(
                "POST",
                "/orders",
                json_body={"item": "book", "qty": 2},
                headers={"X-Request-Id": "abc-123"},
            )
            assert response.status_code == 201
            order_id = response.json()["id"]
        """
        final_headers: Dict[str, str] = dict(self.session.headers)  # type: ignore[arg-type]
        final_headers.update(headers or {})
        final_params: Dict[str, Any] = dict(params or {})

        # L'autenticazione viene applicata a ogni chiamata.
        # Per OAuth2 questo garantisce che il token sia sempre valido.
        auth_kwargs = self._prepare_auth(final_headers, final_params)

        return self.session.request(
            method=method.upper(),
            url=self._build_url(path),
            headers=final_headers,
            params=final_params,
            json=json_body,
            data=form_data if form_data is not None else data,
            timeout=timeout or self.config.timeout,
            verify=self.config.verify_ssl,
            **auth_kwargs,
        )

    # -------------------------------------------------------------------------
    # Convenience methods
    # -------------------------------------------------------------------------

    def get(self, path: str, **kwargs: Any) -> Response:
        """
        Esegue una GET.

        Esempio::

            response = client.get("/users", params={"page": 1})
            users = response.json()
        """
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        """
        Esegue una POST.

        Esempio::

            response = client.post("/users", json_body={"name": "Mario"})
            assert response.status_code == 201
        """
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        """
        Esegue una PUT.

        Esempio::

            response = client.put("/users/42", json_body={"name": "Luigi"})
            assert response.status_code == 200
        """
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        """
        Esegue una PATCH.

        Esempio::

            response = client.patch("/users/42", json_body={"email": "new@example.com"})
            assert response.status_code == 200
        """
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        """
        Esegue una DELETE.

        Esempio::

            response = client.delete("/users/42")
            assert response.status_code == 204
        """
        return self.request("DELETE", path, **kwargs)