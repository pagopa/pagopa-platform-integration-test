# Utility Config (`src/utility/config`)

Questa cartella gestisce il caricamento configurazioni test e la risoluzione dei secret referenziati nei file di config.

## File Python e utilizzo

- `__init__.py`
  - Espone API pubbliche: `load_json_config`, `load_test_config`.

- `config_loader.py`
  - Carica configurazione da file (`JSON object` completo o formato `key:value`).
  - Sostituisce placeholder nel formato `$NOME_SECRET` usando un resolver.
  - Funzioni principali:
    - `load_json_config(path, secret_resolver)`
    - `load_test_config(secret_resolver)` (usa env var `TEST_CONFIG_FILE`)

      Nota: `secret_resolver` può essere un singolo oggetto con metodo
      `resolve(name)` oppure una lista/tupla di resolver. Se è una lista,
      i resolver verranno interrogati in ordine e la prima risoluzione
      non-`None` sarà utilizzata.

- `secrets/__init__.py`
  - Re-export dei resolver disponibili.

- `secrets/secret_resolver.py`
  - Definisce l'interfaccia astratta `SecretResolver`.
  - Include `DictSecretResolver` per test locali/mock.

- `secrets/azure_secret_resolver.py`
  - Implementa `AzureKeyVaultSecretResolver` basato su `DefaultAzureCredential` + `SecretClient`.
  - Richiede env var `AZURE_KEY_VAULT_URL`.

## Variabili ambiente usate

- `TEST_CONFIG_FILE`: percorso del file di configurazione da caricare.
- `AZURE_KEY_VAULT_URL`: URL del vault Azure (solo con resolver Azure).

## Esempio locale (dict resolver)

```python
from src.utility.config import load_test_config
from src.utility.config.secrets import DictSecretResolver

resolver = DictSecretResolver({
    "client_secret": "super-secret",
    "api_key": "test-key",
})
config = load_test_config(resolver)
print(config["service"]["url"])

## Esempio con più resolver

```python
# prova prima il resolver locale, poi il KeyVault se non presente
resolver_list = [
  DictSecretResolver({"client_secret": "local-secret"}),
  AzureKeyVaultSecretResolver(),
]

config = load_test_config(resolver_list)
```
```

## Esempio CI/cloud (Azure Key Vault)

```python
from src.utility.config import load_test_config
from src.utility.config.secrets import AzureKeyVaultSecretResolver

resolver = AzureKeyVaultSecretResolver()
config = load_test_config(resolver)
```

