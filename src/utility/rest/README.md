# Utility REST (`src/utility/rest`)

Questa cartella contiene un client HTTP riusabile e le factory per configurare autenticazione e token OAuth2 nei test.

## File Python e utilizzo

- `__init__.py`
  - Espone classi/config principali e `build_rest_client`.

- `rest_client.py`
  - Implementa `RestClient` e i modelli di configurazione:
    - `RestClientConfig`
    - `NoAuthConfig`, `BasicAuthConfig`, `ApiKeyAuthConfig`, `OAuth2ClientCredentialsConfig`
    - enum `AuthType`, `ApiKeyLocation`
  - Metodi disponibili: `request`, `get`, `post`, `put`, `patch`, `delete`.

- `rest_client_factory.py`
  - Costruisce il client da nodo config servizio (`config["service"]`).
  - Se auth OAuth2, crea automaticamente `OAuth2TokenProvider`.

- `rest_auth_factory.py`
  - Helper per costruire auth config:
    - espliciti: `build_no_auth`, `build_basic_auth`, `build_api_key_auth`, `build_oauth2_client_credentials`
    - da config: `build_basic_auth_from_config`, `build_api_key_auth_from_config`, `build_oauth2_client_credentials_from_config`

- `oauth2_token_provider.py`
  - Gestisce richiesta token OAuth2 client-credentials.
  - Include cache in memoria, controllo validita e refresh automatico.

## Pattern consigliato negli step Behave

```python
from src.utility.config import load_test_config
from src.utility.config.secrets import DictSecretResolver
from src.utility.rest.rest_auth_factory import build_api_key_auth_from_config
from src.utility.rest.rest_client_factory import build_rest_client

resolver = DictSecretResolver({"api_key": "my-key"})
config = load_test_config(resolver)
auth = build_api_key_auth_from_config(config["auth"]["api_key"])
client = build_rest_client(config["service"], auth)

response = client.get("/resource")
assert response.status_code == 200
```

## Note operative

- Il campo `service.url` e obbligatorio per creare il client.
- `service.timeout`, `service.verify_ssl`, `service.default_headers` sono opzionali.
- Per OAuth2 il token viene richiesto al primo uso e rinnovato quando in scadenza.

