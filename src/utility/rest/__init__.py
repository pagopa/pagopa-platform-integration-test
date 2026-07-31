"""REST utility package.

Espone:
- RestClient: client HTTP con autenticazione configurabile
- RestClientConfig: configurazione base del client
- AuthConfig, NoAuthConfig, BasicAuthConfig, ApiKeyAuthConfig, OAuth2ClientCredentialsConfig
- AuthType, ApiKeyLocation
- build_rest_client: factory per creare il client dal config loader
"""

from src.utility.rest.rest_client import (
    ApiKeyAuthConfig,
    ApiKeyLocation,
    AuthConfig,
    AuthType,
    BasicAuthConfig,
    NoAuthConfig,
    OAuth2ClientCredentialsConfig,
    RestClient,
    RestClientConfig,
    RestClientError,
)
from src.utility.rest.rest_client_factory import build_rest_client
from src.utility.rest.rest_auth_factory import build_api_key_auth_from_config

__all__ = [
    "RestClient",
    "RestClientConfig",
    "RestClientError",
    "AuthType",
    "ApiKeyLocation",
    "AuthConfig",
    "NoAuthConfig",
    "BasicAuthConfig",
    "ApiKeyAuthConfig",
    "OAuth2ClientCredentialsConfig",
    "build_rest_client",
    "build_api_key_auth_from_config"
]

