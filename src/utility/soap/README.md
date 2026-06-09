# SOAP Utility (`src/utility/soap`)

Utilities for building a `zeep`-based SOAP client, managing authentication and reading/writing values from SOAP responses.

## Python files

- `__init__.py`
  - Centralised export of all public APIs.

- `soap_client.py`
  - Config dataclasses: `SoapClientConfig`, `SoapNoAuthConfig`, `SoapBasicAuthConfig`, `SoapWsseAuthConfig`.
  - `SoapAuthType` enum (`none`, `basic`, `wsse`).
  - `SoapClientError`: application error raised by the client.

- `soap_auth_factory.py`
  - Explicit builders: `build_soap_no_auth()`, `build_soap_basic_auth()`, `build_soap_wsse_auth()`.
  - Config-based builders: `build_soap_basic_auth_from_config()`, `build_soap_wsse_auth_from_config()`.

- `soap_client_factory.py`
  - `build_soap_client(service_config, auth_config)`: creates a `zeep.Client` with transport and optional WS-Security.

- `soap_response.py`
  - `serialize_response(response)`: converts a zeep response object into a plain Python `dict`/`list`.
  - `get_soap_attr(response, path, default, strict)`: reads a value from a SOAP response via dot path (e.g. `payment.amount[0].currency`).
  - `set_soap_attr(response, path, value, create_missing)`: writes a value into the serialized SOAP response via dot path.
  - `SoapResponseError`: application error raised on read/write failures.

## Configuration node structure

```json
{
  "service": {
    "wsdl_url": "https://example.com/service?wsdl",
    "timeout": 30,
    "verify_ssl": true,
    "extra_headers": {}
  },
  "auth": {
    "basic": { "username": "user", "password": "$soap_password" },
    "wsse":  { "username": "user", "password": "$wsse_password" }
  }
}
```

## Quick example

```python
from src.utility.config import load_test_config
from src.utility.config.secrets import DictSecretResolver
from src.utility.soap import (
    build_soap_client,
    build_soap_wsse_auth_from_config,
    get_soap_attr,
    set_soap_attr,
)

resolver = DictSecretResolver({"wsse_password": "secret"})
config = load_test_config(resolver)

auth = build_soap_wsse_auth_from_config(config["auth"]["wsse"])
client = build_soap_client(config["service"], auth)

# Call a SOAP operation
raw = client.service.GetPayment(paymentId="123")

# Read a value
currency = get_soap_attr(raw, "payment.amount.currency")
item_id  = get_soap_attr(raw, "items[0].id", default="N/A")

# Write a value (fails if path missing)
set_soap_attr(raw, "payment.amount.currency", "USD")

# Write a value (creates missing nodes)
set_soap_attr(raw, "payment.extra[0].note", "test", create_missing=True)
```

## Usage in Behave `environment.py`

```python
from src.utility.config import load_test_config
from src.utility.config.secrets import AzureKeyVaultSecretResolver
from src.utility.soap import build_soap_client, build_soap_wsse_auth_from_config

def before_all(context):
    config = load_test_config(AzureKeyVaultSecretResolver())
    auth = build_soap_wsse_auth_from_config(config["auth"]["wsse"])
    context.soap_client = build_soap_client(config["service"], auth)
```

## API summary

| Function / Class | Description |
|---|---|
| `build_soap_client(service_config, auth_config)` | Creates the `zeep.Client` |
| `build_soap_no_auth()` | No-auth config |
| `build_soap_basic_auth(user, pwd)` | HTTP Basic config |
| `build_soap_wsse_auth(user, pwd)` | WS-Security UsernameToken config |
| `build_soap_basic_auth_from_config(node)` | Basic config from loaded JSON node |
| `build_soap_wsse_auth_from_config(node)` | WSSE config from loaded JSON node |
| `serialize_response(response)` | zeep response → plain Python dict |
| `get_soap_attr(response, path, default, strict)` | Read value from SOAP response |
| `set_soap_attr(response, path, value, create_missing)` | Write value into SOAP response |

## Notes

- `get_soap_attr` and `set_soap_attr` delegate path navigation to `src.utility.json` (`get_attr` / `set_attr`).
- `create_missing=False` (default on `set_soap_attr`): raises `SoapResponseError` if a node in the path is missing.
- `strict=False` (default on `get_soap_attr`): returns `default` if path not found.
- Requires `zeep>=4.2.1` (see `requirements.txt`).

