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
Quando il PSP invia la richiesta di "{request}" con il payload "{payload_name}"
```

La variante per testare l'autenticazione mantiene la stessa logica e forza
`Ocp-Apim-Subscription-Key` a `invalid-key`:

```gherkin
Quando il PSP invia la richiesta di "{request}" con il payload "{payload_name}" con subscription_key non valida
```

Il parametro `partner` seleziona il client: `PSP` usa il client PSP, gli altri
partner usano il client FDR.

## Payload

Un payload di creazione viene caricato da `../payloads.yaml` e memorizzato
con il nome dichiarato nello step:

```gherkin
E un payload di creazione FdR create_payload
```

Il nome deve corrispondere a una chiave sotto `TEST_DATA`. Gli alias
`create_1_payload` e `create_2_payload` condividono il template
`create_payload`. I placeholder vengono risolti a ogni esecuzione dello step.

Per un payload specifico, un blocco inline ha precedenza sul template:

```gherkin
E un payload di creazione FdR custom_payload
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
- `feat_006_steps.py`: impostazione di dati non validi per la cancellazione FdR.
- `feat_009_steps.py`: configurazione query, revisioni e asserzioni di
  paginazione condivise dalle feature organizzazione (009) e PSP (010).

La paginazione di flussi e pagamenti usa un unico step per tutti i partner:

```gherkin
E il PSP riceve pagina 1 con 99 elementi come risposta
E l'organizzazione riceve pagina 1 con 1 elementi come risposta
```

La richiesta con subscription key non valida è gestita dallo step comune:

```gherkin
Quando il PSP invia la richiesta di "{request}" con il payload "{payload_name}" con subscription_key non valida
```

Gli endpoint non devono essere definiti negli step. Il nome funzionale della
richiesta viene risolto in `utils_fdr.py`, che contiene anche metodo HTTP e
path. `perform_fdr_action` registra metadati non sensibili della richiesta e
lo status della risposta; per i dettagli completi usare `DUMP_HTTP=1`.
