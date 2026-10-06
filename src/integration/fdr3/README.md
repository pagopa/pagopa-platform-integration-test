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
- `payloads.yaml`: template dei payload condivisi, indicizzati con il nome
  dichiarato nello step.
- `utils_fdr.py`: mappa tra nome funzionale della richiesta, metodo HTTP e
  endpoint, oltre alla costruzione e validazione delle richieste.

## Configurazione

L'ambiente viene selezionato tramite `TARGET_ENV` e caricato da un file
`yaml`, `yml` o `json` nella directory FdR3. Per usare i segreti del Key Vault:

```powershell
$env:AZURE_KEY_VAULT_URL = "https://pagopa-d-itn-qa-kv.vault.azure.net/"
```

I valori globali configurati vengono esposti agli scenari come placeholder
`#psp#`, `#organization#`, `#channel#`, `#channel_password#` e
`#broker_psp#`.

I client sono inizializzati dagli hook di `environment.py`. Il partner indicato
nello step determina il client usato: `PSP` seleziona il client PSP, mentre ogni
altro valore seleziona il client FdR.

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
Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
Quando il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
Quando il PSP invia la richiesta di "Pubblicazione" con il payload "None"
```

Per verificare gli scenari di autenticazione è disponibile anche la variante:

```gherkin
Quando il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "None" con subscription_key non valida
```

I payload di creazione usano `$tot_payments$` e `$sum_payments$`. Gli step
che impostano questi valori devono precedere lo step del payload.

Lo step `E un payload di creazione FdR create_payload`, senza blocco
`""" ... """`, carica il template `TEST_DATA.create_payload` da
`payloads.yaml`. I dieci payload originali delle nove feature sono identici
a meno dell'indentazione: `create_1_payload` e `create_2_payload` sono alias
YAML di `create_payload`, senza duplicare il contenuto.

La configurazione viene caricata una volta dagli hook; i placeholder sono
risolti quando viene eseguito lo step, con i valori dello scenario corrente.
Un blocco inline continua ad avere precedenza sulla configurazione, per
consentire payload specifici. Un nome non configurato senza blocco inline
genera un errore esplicito.

Per aggiungere una nuova richiesta, aggiungere direttamente la dicitura italiana
e il relativo metodo/path in `DEFAULT_ENDPOINTS` in `utils_fdr.py`; non
introdurre endpoint direttamente nei feature.

## Azioni ed endpoint

`DEFAULT_ENDPOINTS` è l'unica fonte della relazione tra dicitura Gherkin,
metodo HTTP e path:

| Dicitura | Metodo | Endpoint |
| --- | --- | --- |
| Creazione di una nuova struttura di flusso | POST | `/psps/#psp#/fdrs/$flow_name$` |
| Aggiunta pagamenti | PUT | `/psps/#psp#/fdrs/$flow_name$/payments/add` |
| Pubblicazione | POST | `/psps/#psp#/fdrs/$flow_name$/publish` |
| Cancellazione flusso | DELETE | `/psps/#psp#/fdrs/$flow_name$` |
| Recupero FdR pubblicato | GET | `/psps/#psp#/published/fdrs/$flow_name$/revisions/$revision$/organizations/#organization#` |
| Recupero pagamenti creati | GET | `/psps/#psp#/created/fdrs/$flow_name$/organizations/#organization#/payments` |
| Recupero FdR creato | GET | `/psps/#psp#/created/fdrs/$flow_name$/organizations/#organization#` |
| Cancellazione pagamenti | PUT | `/psps/#psp#/fdrs/$flow_name$/payments/del` |
| Recupero di tutti i FdR pubblicati dal PSP | GET | `/psps/#psp#/published` |

I placeholder nel path e nei payload vengono risolti dal contesto Behave. Per
la cancellazione pagamenti il body usa `indexList`, con gli indici da `1` a
`n`.

## Logging e troubleshooting

La suite usa il logger `fdr3`. Per ogni richiesta vengono registrati a livello
`INFO` azione, metodo, path, presenza del body, query parameter e presenza di
header sovrascritti; la risposta registra lo status HTTP. Non vengono
registrati body o valori degli header, così da non esporre dati di test o
segreti.

Per il dettaglio HTTP completo, inclusi request e response, usare
`DUMP_HTTP=1` come descritto nella sezione [Esecuzione](#esecuzione).

Gli errori di configurazione del client vengono riportati dagli hook di
`environment.py`; gli errori di azione, status atteso o asserzione JSON
vengono registrati da `utils_fdr.py` prima di essere rilanciati come errori
Behave.
