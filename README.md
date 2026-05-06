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
│   ├── .secrets_template.yaml             ← template variabili segrete (non committare .secrets.yaml)
│   └── api-test/
│       ├── .env.dev                        ← variabili d'ambiente DEV (escluse da git)
│       └── .env.uat                        ← variabili d'ambiente UAT (escluse da git)
└── src/
    ├── bdd/                                ← suite BDD (Python + Behave)
    │   ├── ebollo/                         ← test eBollettino
    │   ├── fdr/                            ← test Flussi di Rendicontazione
    │   ├── gpd/                            ← test GPD (JavaScript + Cucumber)
    │   └── wisp/                           ← test WISP Converter
    ├── utility/
    │   └── api_test/                       ← helper condivisi per le suite api-test
    │       ├── api_test_environment.py     ← hook Behave comuni (carica .env, reset context)
    │       ├── auth_service/               ← helper auth-service
    │       ├── cart/                       ← helper cart
    │       └── checkout/                   ← helper checkout NPG
    ├── conf/
    │   └── configuration.py               ← loader Dynaconf per config.yaml e .secrets.yaml
    ├── automation-test/                    ← test di automazione UI (Playwright)
    └── e2e-test/
        └── checkout/                       ← test E2E checkout (Playwright)
```

---

## Suite di test disponibili

### Suite BDD — Python + Behave

| Suite | Cartella | Descrizione |
|-------|----------|-------------|
| **eBolletto** | `src/bdd/ebollo/` | Acquisto marca da bollo digitale, rendicontazione via API e broadcast |
| **FdR** | `src/bdd/fdr/` | Flussi di Rendicontazione (smoke test) |
| **WISP** | `src/bdd/wisp/` | WISP Converter — invio RPT singolo e carrello, casi con/senza marca da bollo |
| **Cart** | `src/bdd/cart/` | API cart — creazione carrello, redirect PSP |
| **Auth Service** | `src/bdd/auth-service/` | Autenticazione e autorizzazione |
| **Checkout NPG** | `src/bdd/checkout/` | Checkout eCommerce via gateway NPG — verifica pagamento, metodi, sessioni, transazioni, dati carta, autorizzazione |

#### File `.feature` per suite Checkout NPG

| File | Scenari coperti |
|------|-----------------|
| `checkout_npg_payment_verification.feature` | Verifica avviso di pagamento (positivi e negativi) |
| `checkout_npg_payment_methods.feature` | Recupero metodi di pagamento v1/v2, dettagli carta, calcolo fee |
| `checkout_npg_session.feature` | Creazione sessione NPG per le 5 lingue supportate |
| `checkout_npg_transactions.feature` | Ciclo di vita transazione: creazione, stato, cancellazione |
| `checkout_npg_card_data.feature` | Lettura dati carta, casi di errore 401 |
| `checkout_npg_authorization.feature` | Richiesta autorizzazione con/senza JWT token |

### Suite GPD — JavaScript + Cucumber

| Suite | Cartella | Descrizione |
|-------|----------|-------------|
| **GPD** | `src/bdd/gpd/` | Gestione Posizioni Debitorie — creazione, pubblicazione, pagamento, recupero, aggiornamento |

> La suite GPD utilizza **Node.js** con **Cucumber** anziché Python/Behave. Consultare `src/bdd/gpd/README.md` per le istruzioni specifiche.

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

### 3. Installare Playwright (solo test E2E)

```bash
pip install playwright pytest-playwright
playwright install-deps
playwright install
```

### 4. Installare le dipendenze Node.js (solo suite GPD)

```bash
cd src/bdd/gpd
npm install
```

### 5. Installare Allure CLI

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

### Suite API Test (cart, auth-service, checkout)

La configurazione avviene tramite file `.env` nella cartella `config/api-test/`.

Creare `config/api-test/.env.dev` e/o `config/api-test/.env.uat` con le variabili necessarie. Esempio:

```dotenv
CHECKOUT_HOST=https://api.dev.platform.pagopa.it
NOTICE_CODE_PREFIX=3020
VALID_FISCAL_CODE_PA=77777777777
UNKNOWN_FISCAL_CODE_PA=00000000000
UNKNOWN_NOTICE_CODE=302000000000000000
UNKNOWN_STAZIONE_FISCAL_CODE_PA=11111111111
UNKNOWN_STAZIONE_NOTICE_CODE=302000000000000001
PSP_ID=BCITITMM
NPG_TEST_CARD_PAN=4111111111111111
NPG_TEST_EXPIRATION_DATE=12/30
NPG_TEST_SECURITY_CODE=123
NPG_TEST_CARDHOLDER_NAME=Test User
NPG_TEST_CARD_BRAND=VISA
```

> I file `.env` e `config/.secrets.yaml` sono esclusi da git (`.gitignore`).

---

## Esecuzione dei test

Tutti i comandi vanno eseguiti dalla **root del repository** (`pagopa-platform-integration-test/`).

### Suite BDD legacy (ebollo, fdr, wisp)

```bash
behave src/bdd/<suite> -D env=<environment> -f allure_behave.formatter:AllureFormatter -o reports/allure-results/<suite>-<environment> -f progress
```

Esempio per WISP in DEV:

```bash
behave src/bdd/wisp -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/wisp-dev -f progress
```

### Suite API Test (cart, auth-service, checkout)

```powershell
# Pulire la directory di output (necessario su Windows con allure-behave 2.x)
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\<suite>-<env>
New-Item reports\allure-results\<suite>-<env> -ItemType Directory -Force | Out-Null

# Eseguire i test
behave src/bdd/<suite> -D env=<env> -f allure_behave.formatter:AllureFormatter -o reports/allure-results/<suite>-<env> -f progress
```

Esempio completo per Checkout NPG in DEV:

```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\checkout-dev
New-Item reports\allure-results\checkout-dev -ItemType Directory -Force | Out-Null
behave src/bdd/checkout -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/checkout-dev -f progress
```

### Eseguire solo scenari con tag specifici

```bash
behave src/bdd/checkout --tags=@npg,@payment-verify -D env=dev -f progress
```

### Eseguire un singolo file `.feature`

```bash
behave src/bdd/checkout/features/checkout_npg_transactions.feature -D env=dev -f progress
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
| `src/utility/api_test/api_test_environment.py` | Hook Behave comuni: caricamento `.env`, reset `context.response` prima di ogni scenario |
| `src/utility/api_test/<suite>/<suite>_helpers.py` | Helper HTTP, costruttori di request e logica di verifica specifica per suite |
| `src/bdd/<suite>/environment.py` | Delega a `api_test_environment` + reset dello stato locale della suite |
| `src/bdd/<suite>/steps/<suite>_steps.py` | Step definitions Behave — traduzione Gherkin → chiamate helper |
| `src/conf/configuration.py` | Loader Dynaconf per `config.yaml` e `config/.secrets.yaml` |
| `config.yaml` | URL dei servizi per ambiente (dev/uat) |
| `config/.secrets.yaml` | Credenziali e subscription key (escluso da git) |
| `commondata.yaml` | Dati di test condivisi (codici fiscali, broker, canali, dati pagatore) |

### Flusso di esecuzione (suite api_test)

```
behave src/bdd/<suite> -D env=dev
    │
    ├─ environment.py → before_all()
    │      └─ api_test_environment.before_all() → carica config/api-test/.env.dev
    │
    ├─ environment.py → before_scenario()
    │      └─ api_test_environment.before_scenario() → reset context.response
    │      └─ reset stato locale della suite
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

### Installazione pre-commit

```bash
pip install pre-commit
pre-commit install
```

### Hook attivi

- Validazione sintassi YAML, JSON, XML
- Rilevamento chiavi private
- Normalizzazione fine-riga (LF)
- Formattazione JSON automatica
- Rimozione spazi finali
- Controllo AST Python
- Uniformità delle virgolette (`double-quote-string-fixer`)
