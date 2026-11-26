# Blob Storage Utilities (`src/utility/blob`)

Modulo centralizzato per gestione Azure Storage (Blob e Table Storage).

## Componenti

### 1. AzureBlobService (azure_blob.py)
Client per Azure Blob Storage.

**Uso**:
```python
from src.utility.blob import AzureBlobService

service = AzureBlobService(context)
blobs = service.list_blobs("container-name")
blob = service.find_blob("container-name", "blob-name")
service.close()
```

### 2. IssuerTableClient (azure_table.py)
Client per Azure Table Storage con focus su issuer/BIN range management.

**Caratteristiche**:
- Connessione via connection string **oppure** endpoint URL (`https://<account>.table.core.windows.net`)
- Endpoint URL autenticato con `DefaultAzureCredential` (es. `az login`, Managed Identity)
- Creazione/aggiornamento/cancellazione entità
- Query con filtri opzionali
- Setup idempotente (delete-then-create)
- Error handling con logging

**Uso**:
```python
from src.utility.blob import IssuerTableClient, build_issuer_table_client

# Factory con error handling (connection string o endpoint URL)
client = build_issuer_table_client(connection_string)
if client:
    # Setup issuer entities
    entities = [
        {
            "PartitionKey": "300000",
            "RowKey": "visa-300000",
            "issuer_name": "VISA Test",
            "bin_start": "300000",
            "bin_end": "399999"
        }
    ]
    client.setup_issuer_ranges(entities)
    client.close()
```

### 3. build_issuer_table_client() (azure_table.py)
Factory function con error handling per IssuerTableClient.

**Ritorna**: IssuerTableClient o None se fails

**Gestisce**:
- Missing connection string/endpoint URL
- Missing azure-data-tables package
- Connection errors

**Input supportati**:
- Connection string classica (invariata): `DefaultEndpointsProtocol=...;AccountKey=...`
- Endpoint URL senza key/SAS: `https://<storage-account>.table.core.windows.net`

## Architettura

```
src/utility/blob/
├── __init__.py                  # Export pubblici
├── azure_blob.py               # Blob Storage (pre-esistente)
└── azure_table.py              # Table Storage (nuovo)

src/integration/gec/
├── azure_table_client.py        # GEC-specific ISSUER_ENTITIES
└── environment.py               # Uses utility/blob.build_issuer_table_client()
```

## Pattern di Utilizzo

### Nel before_all hook (Behave)
```python
from src.utility.blob import build_issuer_table_client
from src.integration.gec.azure_table_client import ISSUER_ENTITIES

def _setup_azure_storage(context):
    """Setup Azure Table Storage (optional)."""
    gec_config = getattr(context.config, "gec", None)
    if not gec_config:
        return
    
    azure_conn_str = _config_value(gec_config, "azure_connection_string")
    if not azure_conn_str:
        LOGGER.info("No Azure Storage connection string - skipping setup")
        return
    
    table_client = build_issuer_table_client(azure_conn_str)
    if table_client:
        table_client.setup_issuer_ranges(ISSUER_ENTITIES)
        context.gec.azure_table_client = table_client
```

## Requisiti

`azure-data-tables` è dichiarato in `requirements.txt` (`pip install -r requirements.txt`).

Il supporto Table è opzionale a import time: `src.utility.blob` e `AzureBlobService` restano
importabili anche senza `azure-data-tables`. Senza il pacchetto, `IssuerTableClient(...)` solleva
`ImportError` e `build_issuer_table_client()` restituisce `None`.

Con un endpoint URL l'identità di `DefaultAzureCredential` deve avere almeno il ruolo
**Storage Table Data Contributor** sullo Storage Account.

## Coerenza Architetturale

Segue il pattern stabilito da:
- `src/utility/rest/` - REST client utilities
- `src/utility/config/` - Configuration loading
- `src/utility/soap/` - SOAP client utilities

**Principi**:
1. Utility centralizzate in src/utility/
2. Separazione concerns (utility = logica, integration = data)
3. Factory functions con error handling
4. Logging strutturato
5. Importazioni esplicite nel __init__.py

## Manutenzione

Modifiche a:
- Autenticazione Azure
- Format tabelle
- Strategie di setup

Vanno fatte **UNA SOLA VOLTA** in `src/utility/blob/azure_table.py`.

Progetti che usano IssuerTableClient automaticamente beneficiano della fix.
