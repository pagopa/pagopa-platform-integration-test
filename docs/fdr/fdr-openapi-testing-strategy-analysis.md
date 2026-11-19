# Analisi comparata strategie test REST da OpenAPI FDR

## Obiettivo
Valutare due approcci per sfruttare i file OpenAPI fetchati (`tmp_fetched/fdr_psp.json` e `tmp_fetched/fdr_organization.json`) al fine di riconoscere le interfacce REST ed eseguire test API, privilegiando efficacia, semplicita e coerenza con il progetto.

Approcci confrontati:
1. Script Python (preparazione request, chiamata, asserzioni risposta).
2. Suite Newman (pre/post scripts + assertions in collection Postman).

## Baseline tecnica osservata

### OpenAPI disponibili
- `fdr_psp.json`
  - `server`: `https://api.platform.pagopa.it/fdr-psp/service/v1`
  - `operations`: 11
  - sicurezza: `apiKeyHeader` (`Ocp-Apim-Subscription-Key`) e `apiKeyQuery` (`subscription-key`)
- `fdr_organization.json`
  - `server`: `https://api.platform.pagopa.it/fdr-org/service/v1`
  - `operations`: 3
  - stessa sicurezza API key

Totale endpoint operativi rilevati: 14.

### Stato attuale repository
- Stack primario: Python + Behave + Allure (vedi `README.md`).
- Utility condivise pronte per riuso in `src/utility`:
  - config/secret resolution (`src/utility/config`)
  - REST client e auth strategies (`src/utility/rest`)
  - JSON path helpers (`src/utility/json`)
- Presenza storica di Newman/Postman documentata (`src/api/analisi-tecnica-api-tests-checkout.md`) e guida di migrazione verso Behave (`src/api/porting-api-tests-guide.md`).
- Suite `src/integration/fdr` attualmente minimale (hello world), quindi esiste spazio per introdurre test FDR reali.

## Criteri di valutazione
- **Efficacia**: copertura endpoint, robustezza asserzioni, validazione schema OpenAPI, gestione test negativi.
- **Semplicita**: velocita di bootstrap, curva di apprendimento, costo manutenzione.
- **Coerenza con progetto**: allineamento con stack corrente, riuso utility, integrazione report/CI.
- **Estendibilita**: facilita nel passare da smoke a regression suite.

Scala punteggio: 1 (basso) - 5 (alto).

## Analisi alternativa 1: Script Python

### Come funzionerebbe
- Parsing OpenAPI per estrarre operation map (`method`, `path`, `params`, `responses`).
- Builder richieste in Python con parametrizzazione ambiente.
- Invocazione REST via utility interne (`src/utility/rest`) o `requests`.
- Asserzioni su:
  - status code atteso
  - header principali
  - schema risposta (allineato a component schemas)
  - campi semantici chiave
- Integrazione naturale in Behave/pytest + Allure/JUnit.

### Pro
- Massima coerenza con ecosistema attuale (Python-first).
- Riuso diretto di utility config/secret/auth gia in repo.
- Miglior controllo su logiche complesse (chaining chiamate, fixture, retry, data generation).
- Manutenzione centralizzata nel linguaggio dominante del progetto.
- Facile convergenza verso le suite BDD gia esistenti.

### Contro
- Richiede setup iniziale maggiore rispetto a importare una collection pronta.
- Serve definire convenzioni di generazione casi da OpenAPI (naming, dataset, negative cases).

### Valutazione
- Efficacia: **5/5**
- Semplicita: **3/5**
- Coerenza col progetto: **5/5**
- Estendibilita: **5/5**

## Analisi alternativa 2: Suite Newman

### Come funzionerebbe
- Conversione OpenAPI -> Postman Collection (manuale o tool-assisted).
- Definizione pre-request scripts per variabili/autenticazione.
- Definizione test scripts (`pm.test`, `pm.expect`) per status e payload.
- Esecuzione via Newman CLI con reporter (CLI/JUnit).

### Pro
- Avvio rapido per smoke test endpoint-oriented.
- Buona accessibilita per QA non Python-centric.
- Ecosistema Postman utile per esplorazione manuale + automatica.

### Contro
- Minore coerenza con direzione attuale del repository (evidenziata anche dalla guida interna di porting Newman -> Gherkin).
- Duplica logiche gia coperte in Python utility (config, auth, parsing).
- Gestione strutturata di test complessi/riuso codice meno elegante rispetto a Python.
- Rischio frammentazione toolchain (Node/Newman + Python/Behave).

### Valutazione
- Efficacia: **4/5**
- Semplicita: **4/5** (alta all'inizio, media sul lungo periodo)
- Coerenza col progetto: **2/5**
- Estendibilita: **3/5**

## Confronto sintetico

| Criterio | Script Python | Newman |
|---|---:|---:|
| Efficacia | 5 | 4 |
| Semplicita | 3 | 4 |
| Coerenza col progetto | 5 | 2 |
| Estendibilita | 5 | 3 |
| **Totale** | **18/20** | **13/20** |

## Raccomandazione
Raccomandazione principale: **Alternativa 1 (Script Python)**.

Motivazione:
- E il percorso piu coerente con l'architettura test del repository.
- Consente il massimo riuso delle utility interne gia standardizzate.
- Riduce il debito tecnico da doppia toolchain e favorisce integrazione con Behave/Allure.
- Offre maggiore controllo per validazioni OpenAPI robuste e test evolutivi (smoke -> regression).

## Strategia pratica consigliata (senza implementazione, per prossimi passi)
1. Definire un documento di test matrix OpenAPI (14 operation) con priorita smoke/critical.
2. Stabilire convenzioni Python per operation mapping e naming test-case.
3. Introdurre un primo smoke pack FDR (read-only GET) e poi scenari write con cleanup.
4. Integrare schema validation e reporting nel flusso CI gia esistente.
5. Mantenere Newman solo come supporto opzionale per esplorazione/manual QA, non come percorso primario.

## Rischi e mitigazioni
- **Rischio**: aumento effort iniziale Python.
  - **Mitigazione**: partire da smoke GET + scaffolding minimo.
- **Rischio**: dati test non stabili in ambienti condivisi.
  - **Mitigazione**: dataset dedicato e cleanup deterministico.
- **Rischio**: mismatch tra examples OpenAPI e vincoli runtime.
  - **Mitigazione**: distinguere test di contratto (schema) da test di comportamento (business).

## Conclusione
Entrambe le strade sono fattibili. In questo repository, la soluzione Python e la piu efficace nel medio-lungo periodo e la piu coerente con stack, processi e asset gia presenti. Newman resta valida per prototipazione rapida, ma non come backbone della nuova suite FDR.
