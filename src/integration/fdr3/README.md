# Test di integrazione FdR3

La suite FdR3 si trova in questa directory e usa Behave per eseguire gli
scenari definiti in `feature/`.

## Struttura

- `feature/`: scenari Gherkin, un file per area funzionale.
- `steps/feat_001_common_steps.py`: step condivisi per creazione flussi,
  payload, pagamenti e richieste parametrizzate.
- `steps/feat_00x_steps.py`: step specifici di una singola feature.
- `environment.py`: caricamento configurazione e inizializzazione dei client
  PSP e FDR.
- `helper.py`: selezione client, gestione del contesto e sostituzione
  placeholder.
- `utils_fdr.py`: mappa tra nome funzionale della richiesta, metodo HTTP e
  endpoint.

## Configurazione

L'ambiente viene selezionato tramite `TARGET_ENV` e caricato da un file
`yaml`, `yml` o `json` nella directory FdR3. Per usare i segreti del Key Vault:

```powershell
$env:AZURE_KEY_VAULT_URL = "https://pagopa-d-itn-qa-kv.vault.azure.net/"
```

I valori globali configurati vengono esposti agli scenari come placeholder
`#psp#`, `#organization#`, `#channel#`, `#channel_password#` e
`#broker_psp#`.

## Esecuzione

Dal repository root:

```powershell
behave src\integration\fdr3 --dry-run --no-capture
behave src\integration\fdr3\feature\FEAT_001_FdR3_Aggiungi_pagamenti.feature --tags=@runnable --no-capture
```

Il dry-run deve terminare con `0 undefined`. Per stampare request e response:

```powershell
$env:DUMP_HTTP = "1"
```

## Regole principali

Le richieste usano il nome funzionale e un payload nominato:

```gherkin
Quando il PSP invia la richiesta "Create a new flow structure" con il payload "create_payload"
Quando il PSP invia la richiesta "Add payments" con il payload "payments_payload"
Quando il PSP invia la richiesta "Publish" con il payload "None"
```

I payload di creazione usano `$tot_payments$` e `$sum_payments$`. Gli step
che impostano questi valori devono precedere lo step del payload.

Il partner determina il client utilizzato: `PSP` usa `context.psp`, mentre
qualsiasi altro partner usa `context.fdr`.

Per aggiungere una nuova richiesta, aggiornare `REQUEST_ACTIONS` e
`DEFAULT_ENDPOINTS` in `utils_fdr.py`; non introdurre endpoint direttamente
nei feature.
