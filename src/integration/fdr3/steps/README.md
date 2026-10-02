# Step FdR3

## Step condivisi

`feat_001_common_steps.py` contiene gli step riutilizzati dalle feature:

- inizializzazione dei sistemi;
- generazione di `flow_name` e `flow_date`;
- definizione dei payload di creazione;
- impostazione di numero e somma dei pagamenti;
- generazione di `payments_payload`;
- esecuzione di scenari precedenti tramite `context.execute_steps`;
- invio di richieste parametrizzate;
- asserzioni su status e stato del flusso.

Gli step comuni sono gli unici responsabili della sintassi generica:

```gherkin
Quando il PSP invia la richiesta "{request}" con il payload "{payload_name}"
```

Il parametro `partner` seleziona il client: `PSP` usa il client PSP, gli altri
partner usano il client FDR.

## Payload

Un payload di creazione viene memorizzato con il nome dichiarato nello step:

```gherkin
E un payload di creazione FdR create_payload
  """
  { ... }
  """
```

I placeholder numerici standard sono:

```text
$tot_payments$
$sum_payments$
```

Per l'aggiunta pagamenti, lo step dedicato genera record completi con IUV,
IUR, indice progressivo, importo, stato `EXECUTED` e data UTC:

```gherkin
Quando il PSP aggiunge 3 pagamenti la cui somme è 300 al flusso di rendicontazione flow_name come payments_payload
```

Le richieste senza body usano il payload `"None"`.

## Step specifici

Gli step non generici sono mantenuti nei moduli della feature:

- `feat_002_steps.py`: revisioni e `totPayments`;
- `feat_003_steps.py`: verifica della cancellazione del flusso;
- `feat_004_steps.py`: cancellazione e conteggio pagamenti;
- `feat_005_steps.py`: aggiunta pagamenti con subscription key non valida;
- `feat_006_steps.py`: cancellazione FdR con dati o subscription key non validi;
- `feat_007_steps.py`: cancellazione pagamenti con subscription key non valida;
- `feat_008_steps.py`: pubblicazione con subscription key non valida.

Gli endpoint non devono essere definiti negli step. Il nome funzionale della
richiesta viene risolto in `utils_fdr.py`, che contiene anche metodo HTTP e
path.
