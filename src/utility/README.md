# Utility (`src/utility`)

Questa cartella contiene componenti condivisi per i test di integrazione/API: caricamento configurazioni, gestione secret e client HTTP riusabile.

## Struttura (esclusa `ebollo`)

- `config/`: loader della configurazione test e risoluzione placeholder secret.
- `rest/`: client REST con supporto auth (none/basic/api key/oauth2).
- `json/`: utility per conversione JSON, lettura (`get_attr`) e scrittura (`set_attr`) di valori via path.
- `soap/`: client SOAP basato su `zeep` con supporto auth (none/basic/wsse), utility get/set su response e supporto a chiamate SOAP raw via zeep transport quando non e disponibile un WSDL.
- `data_generators.py`: generatori condivisi per stringhe casuali e identificativi applicativi (es. cart id).
- `datetime_utils.py`: helper condivisi per date e timestamp in formato stringa.
- `indexing.py`: mapping condiviso di cardinalita testuali verso indici numerici.
- `assertions.py`: assert helper con logging centralizzato del messaggio di errore.

## Flusso tipico di utilizzo

1. Carica la configurazione con `load_test_config(...)` o `load_json_config(...)`.
	Nota: è possibile passare a `load_test_config` un singolo resolver o una
	lista/tupla di resolver; in quest'ultimo caso vengono interrogati in
	ordine e la prima risoluzione non-`None` viene utilizzata.
2. Costruisci la strategia auth con funzioni in `rest_auth_factory.py`.
3. Crea il client con `build_rest_client(...)`.
4. Usa `client.get/post/put/patch/delete(...)` negli step Behave.

## Esempio rapido

```python
from src.utility.config import load_test_config
from src.utility.config.secrets import DictSecretResolver
from src.utility.rest.rest_auth_factory import build_oauth2_client_credentials_from_config
from src.utility.rest.rest_client_factory import build_rest_client

resolver = DictSecretResolver({"client_secret": "local-secret"})
config = load_test_config(resolver)
auth = build_oauth2_client_credentials_from_config(config["auth"]["oauth2"])
client = build_rest_client(config["service"], auth)

response = client.get("/health")
print(response.status_code)
```

## Documentazione di dettaglio

- `src/utility/config/README.md`
- `src/utility/rest/README.md`
- `src/utility/json/README.md`
- `src/utility/soap/README.md`

