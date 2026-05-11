# pagopa-platform-integration-test

Suite di test di integrazione per le API della piattaforma **PagoPA**, implementata con **Python**, **Behave** e **Gherkin**. Il repository raccoglie scenari BDD (Behavior-Driven Development) end-to-end e test API, organizzati per modulo funzionale, con supporto alla reportistica tramite **Allure**.

---

## Indice

- [Panoramica del progetto](#panoramica-del-progetto)
- [Struttura del repository](#struttura-del-repository)
- [Suite di test disponibili](#suite-di-test-disponibili)
- [Requisiti di sistema](#requisiti-di-sistema)
- [Installazione](#installazione)
- [Configurazione degli ambienti](#configurazione-degli-ambienti)
- [Esecuzione dei test](#esecuzione-dei-test)
- [Report Allure](#report-allure)
- [Architettura interna](#architettura-interna)
- [Qualità del codice](#qualità-del-codice)

---

## Panoramica del progetto

Il repository centralizza i test di integrazione della piattaforma PagoPA. Ogni sotto-cartella di `src/bdd/` corrisponde a un modulo applicativo e contiene:

- **File `.feature`** — scenari scritti in Gherkin (Given/When/Then).
- **Step definitions** — implementazione Python degli step Gherkin (framework `behave`).
- **Helper** — moduli Python riutilizzabili per le chiamate HTTP e la costruzione dei dati di test.

Il progetto supporta gli ambienti **DEV** e **UAT**, configurabili tramite variabili d'ambiente e file `.env`.

---

## Struttura del repository

```
pagopa-platform-integration-test/
├── requirements.txt                        ← dipendenze Python
├── behave.ini                              ← configurazione globale Behave
├── config.yaml                             ← URL dei servizi per ambiente (dev/uat)
├── commondata.yaml                         ← dati di test condivisi tra suite
├── config/
│   └── .secrets_template.yaml             ← template variabili segrete (non committare .secrets.yaml)
└── src/
    ├── bdd/                                ← suite BDD (Python + Behave)
    │   ├── ebollo/                         ← test eBollettino
    │   ├── fdr/                            ← test Flussi di Rendicontazione
    │   ├── gpd/                            ← test GPD (Node.js + Cucumber)
    │   └── wisp/                           ← test WISP Converter
    ├── utility/
    │   ├── ebollo/                         ← helper per eBollo
    │   └── wisp/                           ← helper per WISP
    ├── conf/
    │   └── configuration.py               ← loader Dynaconf per config.yaml e .secrets.yaml
    ├── automation-test/                    ← test di automazione UI (Playwright)
    │   └── features/                       ← scenari Gherkin per automazione UI
    └── e2e-test/
        └── checkout/                       ← test E2E checkout (Node.js + Playwright)
```

---

## Suite di test disponibili

### Suite BDD — Python + Behave

| Suite | Cartella | Descrizione |
|-------|----------|-------------|
| **eBolletto** | `src/bdd/ebollo/` | Acquisto marca da bollo digitale, rendicontazione via API e broadcast |
| **FdR** | `src/bdd/fdr/` | Flussi di Rendicontazione (smoke test) |
| **WISP** | `src/bdd/wisp/` | WISP Converter — invio RPT singolo e carrello, casi con/senza marca da bollo |

### Suite GPD — Node.js + Cucumber

| Suite | Cartella | Descrizione |
|-------|----------|-------------|
| **GPD** | `src/bdd/gpd/` | Gestione Posizioni Debitorie — creazione, pubblicazione, pagamento, recupero, aggiornamento |

> La suite GPD utilizza **Node.js** con **Cucumber** anziché Python/Behave. Consultare `src/bdd/gpd/README.md` per le istruzioni specifiche.

### Suite E2E — Node.js + Playwright

| Suite | Cartella | Descrizione |
|-------|----------|-------------|
| **Checkout E2E** | `src/e2e-test/checkout/` | Test end-to-end del processo di checkout utilizzando Playwright |

---

## Requisiti di sistema

| Requisito | Versione minima |
|-----------|-----------------|
| Python | 3.10+ |
| pip | 22+ |
| Node.js (solo GPD) | 18+ |
| Allure CLI | 2.x o 3.x |
| Java (per Allure) | 11+ |

---

## Installazione

### 1. Clonare il repository

```bash
git clone https://github.com/pagopa/pagopa-platform-integration-test.git
cd pagopa-platform-integration-test
```

### 2. Installare le dipendenze Python

```bash
pip install -r requirements.txt
```

### 3. Installare le dipendenze Node.js (solo suite GPD e E2E Checkout)

Per GPD:
```bash
cd src/bdd/gpd
npm install
```

Per E2E Checkout:
```bash
cd src/e2e-test/checkout
npm install
npx playwright install
```

### 4. Installare Allure CLI

Seguire le istruzioni ufficiali per il proprio OS: [https://allurereport.org/docs/install/](https://allurereport.org/docs/install/)

---

## Configurazione degli ambienti

### Suite BDD (ebollo, fdr, wisp)

La configurazione avviene tramite `config.yaml` (URL dei servizi) e `config/.secrets.yaml` (credenziali).

1. Copiare il template dei segreti:
   ```bash
   cp config/.secrets_template.yaml config/.secrets.yaml
   ```
2. Compilare `config/.secrets.yaml` con le chiavi di sottoscrizione e le password.
3. Impostare la variabile d'ambiente `TARGET_ENV`:
   ```bash
   export TARGET_ENV=dev   # oppure: uat
   ```

> Il file `config/.secrets.yaml` è escluso da git (`.gitignore`).

---

## Esecuzione dei test

Tutti i comandi vanno eseguiti dalla **root del repository** (`pagopa-platform-integration-test/`).

### Suite BDD (ebollo, fdr, wisp)

```bash
behave src/bdd/<suite> -D env=<environment> -f allure_behave.formatter:AllureFormatter -o reports/allure-results/<suite>-<environment> -f progress
```

Esempio per WISP in DEV:

```bash
behave src/bdd/wisp -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/wisp-dev -f progress
```

### Eseguire solo scenari con tag specifici

```bash
behave src/bdd/wisp --tags=@v1 -D env=dev -f progress
```

### Eseguire un singolo file `.feature`

```bash
behave src/bdd/ebollo/features/citizen_buys_ebollo.feature -D env=dev -f progress
```

### Suite E2E Checkout (Playwright)

```bash
cd src/e2e-test/checkout
npx playwright test
```

---

## Report Allure

Dopo l'esecuzione dei test, visualizzare il report con Allure CLI.

Verificare prima la versione installata:

```powershell
allure --version
```

| Versione Allure CLI | Comando |
|---------------------|---------|
| **2.x** (legacy) | `allure serve reports/allure-results/<suite>-<env> --port <porta>` |
| **3.x** (corrente) | `allure open reports/allure-results/<suite>-<env> --port <porta>` |

Esempio per Checkout DEV con Allure 3.x:

```powershell
allure open reports/allure-results/checkout-dev --port 5302
```

> **Nota sull'ordine dei formatter**: il flag `-o` si associa al **primo** `-f`. `AllureFormatter` deve sempre precedere `-f progress`, altrimenti `progress` riceve il percorso della directory e genera un `PermissionError`.

---

## Architettura interna

### Separazione delle responsabilità

| File / Modulo | Responsabilità |
|---------------|----------------|
| `src/utility/<suite>/<suite>_helpers.py` | Helper HTTP, costruttori di request e logica di verifica specifica per suite |
| `src/bdd/<suite>/environment.py` | Hook Behave specifici per la suite |
| `src/bdd/<suite>/steps/<suite>_steps.py` | Step definitions Behave — traduzione Gherkin → chiamate helper |
| `src/conf/configuration.py` | Loader Dynaconf per `config.yaml` e `config/.secrets.yaml` |
| `config.yaml` | URL dei servizi per ambiente (dev/uat) |
| `config/.secrets.yaml` | Credenziali e subscription key (escluso da git) |
| `commondata.yaml` | Dati di test condivisi (codici fiscali, broker, canali, dati pagatore) |

### Flusso di esecuzione (suite Python/Behave)

```
behave src/bdd/<suite> -D env=dev
    │
    ├─ environment.py → before_scenario()
    │      └─ reset dello stato locale della suite
    │
    ├─ Per ogni Scenario:
    │   ├─ Given → configura pre-condizioni, genera dati di test
    │   ├─ When  → esegue chiamate HTTP tramite helpers (requests)
    │   └─ Then  → verifica status code, payload, asserzioni di business
    │
    └─ Genera reports/allure-results/<suite>-dev/
```

---

## Qualità del codice

Il repository utilizza **pre-commit** per garantire la qualità del codice prima di ogni commit.