# Handoff: modalità advisory per Test Automation Service

## Destinatario

Agente che opera sul repository `pagopa/pagopa-platform-integration-test`.

## Obiettivo

Estendere il workflow riusabile TAS per supportare due politiche d'esito:

- `blocking`: un risultato test non positivo rende failed il job chiamato. È la policy richiesta per il gate Prod e deve restare il default retrocompatibile.
- `advisory`: i fallimenti o la copertura insufficiente degli scenari vengono restituiti come dati e report, ma non falliscono il reusable workflow. È la policy richiesta dopo i deploy DEV/UAT.

Il chiamante GitHub Actions non può applicare `continue-on-error` a una chiamata di reusable workflow per neutralizzarne il fallimento. La distinzione deve essere implementata nel workflow TAS, che conosce sia i risultati dei test sia il job che li finalizza.

## Ambito

Workflow principale da modificare:

- `.github/workflows/test-automation-service.yml`

Individuare inoltre gli script, i reusable workflow interni e i test che contribuiscono a parsing, summary, pubblicazione dei report, analisi AI e ingestion dei dati. Non assumere che il solo step finale sia l'unico punto in cui un fallimento possa propagarsi alla conclusione del workflow TAS.

## Contratto proposto

### Input

Aggiungere `failure_mode` a `on.workflow_call.inputs`:

- Tipo: `string`.
- Valori ammessi: `blocking`, `advisory`.
- Default: `blocking`.
- Validare a runtime i valori ricevuti da `workflow_call`, perché il tipo string non applica un'enumerazione.

Aggiungere lo stesso input a `on.workflow_dispatch.inputs` come `choice`, con le stesse opzioni e default `blocking`. I chiamanti esistenti che non passano il nuovo input devono mantenere il comportamento blocking.

### Output

Conservare i nomi e la compatibilità degli output esistenti:

- `outcome`: esito funzionale dei test, indipendente da `failure_mode` (`success` o `failure`).
- `passed`, `failed`, `skipped`, `total`, `duration`: conteggi e durata, quando disponibili.

Aggiungere, se necessario, un output esplicito come `execution_status` per distinguere l'esecuzione completata dai problemi operativi. Usare valori documentati, per esempio `completed` e `error`; non codificare un errore infrastrutturale come normale fallimento di scenario.

La policy governa la conclusione del workflow, non il valore di `outcome`: in modalità advisory, un job chiamante può risultare `success` mentre l'output `outcome` è `failure` e i conteggi documentano gli scenari falliti.

## Regole funzionali

| Situazione | `outcome` / copertura | Modalità `blocking` | Modalità `advisory` |
| --- | --- | --- | --- |
| Report valido, almeno uno scenario, nessun fallimento | `success`; riportare i conteggi | Workflow success | Workflow success, nessun warning |
| Uno o più scenari falliti | `failure`, conteggi disponibili | Workflow/job TAS failure | Workflow/job TAS success; output conservati per il warning del chiamante |
| Alcuni scenari skipped | Registrare `skipped` e indicare copertura parziale | Preservare la semantica blocking esistente; non introdurre un nuovo blocco solo per gli skipped senza esplicita decisione di prodotto | Workflow/job TAS success; output conservati; il chiamante advisory deve segnalare warning |
| Report valido ma zero scenari eseguiti | `failure`, `total: 0`, copertura `empty` o equivalente | Workflow/job TAS failure, evitando un falso successo vacuo | Workflow/job TAS success; output indicano copertura assente per il warning del chiamante |
| Report assente, malformato o non interpretabile | `execution_status: error` o equivalente | Workflow/job TAS failure | Workflow/job TAS failure: è un errore operativo, non un risultato test advisory |
| Errore di setup, dipendenze, autenticazione o configurazione TAS | Stato operativo errore | Workflow/job TAS failure | Workflow/job TAS failure; non mascherarlo come warning di scenario |

Un report valido con zero scenari non equivale a un report mancante: il primo è un esito advisory di copertura assente; il secondo è un errore operativo. Se l'implementazione attuale non permette di distinguerli, correggere il parsing e aggiungere un output esplicito.

## Modifiche richieste

1. Aggiungere e validare `failure_mode` su `workflow_call` e `workflow_dispatch`; default `blocking`.
2. Rendere robusto il parser dei risultati. In particolare, non impostare `outcome: success` quando il report non esiste, non è JSON valido o contiene zero scenari.
3. Separare il risultato funzionale degli scenari dallo stato operativo dell'esecuzione. Mantenere conteggi e output disponibili per i risultati advisory validi.
4. Condizionare allo `failure_mode` lo step che attualmente fallisce il job per scenari non riusciti: deve bloccare in `blocking` e non bloccare per il solo esito degli scenari in `advisory`.
5. Garantire che lo stato complessivo del reusable workflow sia success in modalità advisory quando l'unica causa non positiva sono i risultati degli scenari. Verificare anche i job downstream (analisi AI, pubblicazione report e ingestion): una loro gestione dei test falliti non deve reintrodurre il fallimento della run advisory. Gli errori operativi di tali job devono avere una policy esplicita e non essere confusi con l'esito dei test.
6. Mantenere upload e pubblicazione dei risultati per scenari falliti o zero scenari, così il chiamante e gli operatori possono consultare report e conteggi.
7. Riportare `failure_mode`, `outcome`, conteggi e stato di copertura nel GitHub step summary e nei report già prodotti dal TAS.
8. Aggiornare documentazione e changelog del repository TAS e comunicare il nuovo ref immutabile ai repository chiamanti.

## Criteri di accettazione

- Input omesso da un chiamante esistente: comportamento blocking invariato.
- Input non riconosciuto a `workflow_call`: errore di validazione chiaro e fail-closed.
- `blocking` + almeno uno scenario fallito: reusable workflow failed; output e report dei test restano disponibili.
- `advisory` + almeno uno scenario fallito: reusable workflow success; `outcome: failure`, conteggi corretti e report disponibili.
- `advisory` + report valido senza scenari: reusable workflow success; `total: 0`, outcome non positivo e copertura assente segnalata.
- `advisory` + scenari skipped: workflow success; conteggi e stato di copertura parziale sono visibili.
- `advisory` + report assente/non valido o errore di setup: workflow failed come errore operativo; non deve apparire come suite passata.
- Entrambe le modalità producono il risultato coerente nel summary e negli artifact.
- Un test di regressione verifica che la modalità blocking usata dai chiamanti Prod continui a bloccare la promozione dopo test non superati.

## Verifiche da aggiungere/eseguire

- Unit test del parser per report valido con tutti passati, fallimenti, skipped, zero scenari, file assente e JSON malformato.
- Test del contratto reusable per input default, valori ammessi e output.
- Verifica del risultato finale del workflow nelle combinazioni blocking/advisory, includendo i job accessori che possono influenzare la conclusione.
- Verifica che il comportamento manuale `workflow_dispatch` mantenga `blocking` come default.
- Controllo statico del workflow e test esistenti del repository TAS.

## Integrazione prevista nel chiamante FDR

Dopo il merge e il rilascio del contratto TAS:

- La chiamata Prod in `pagopa-fdr` passa esplicitamente `failure_mode: blocking` e mantiene il gate Prod.
- Le chiamate dopo un deploy DEV/UAT passano `failure_mode: advisory`, attendono l'esito, quindi scrivono un warning nel riepilogo quando `outcome` non è positivo, `failed > 0`, `skipped > 0`, `total == 0` o la copertura non è completa.
- I fallimenti del deploy DEV/UAT restano errori del deploy e non avviano TAS.
- Il workflow TAS va referenziato dal chiamante tramite SHA/tag stabile aggiornato dopo il rilascio.

## Fuori ambito

- Non modificare la policy del gate Prod senza una decisione separata.
- Non cambiare per default i chiamanti TAS esistenti da blocking ad advisory.
- Non mascherare errori operativi, report mancanti o configurazioni non valide come test superati.
- Non richiedere al chiamante di usare `continue-on-error` sul job reusable: la policy advisory appartiene al contratto TAS.
