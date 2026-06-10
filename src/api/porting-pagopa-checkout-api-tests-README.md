# api-test — Test BDD con Python e Behave

Test BDD per le API del progetto PagoPA, implementati con **Python**, **Behave** e **Gherkin**.
Ogni sotto-cartella di `src/bdd/` raccoglie i test relativi a uno specifico modulo API.

---

## Struttura del progetto

```
pagopa-platform-integration-test/
├── requirements.txt                          ← dipendenze Python (inclusa allure-behave 2.x)
├── config/
│   └── api-test/
│       ├── .env.dev                          ← variabili d'ambiente DEV
│       └── .env.uat                          ← variabili d'ambiente UAT
└── src/
    ├── bdd/
    │   └── cart/                             ← scenari Gherkin e step definitions cart-test
    │       ├── environment.py                ← hooks Behave (delega a api_test_environment)
    │       ├── features/
    │       │   └── cart.feature              ← scenari Gherkin
    │       └── steps/
    │           └── cart_steps.py             ← step definitions
    └── utility/
        └── api_test/
            ├── api_test_environment.py       ← hooks comuni (carica .env, reset contesto)
            └── cart/
                └── cart_helpers.py           ← helper HTTP e data builder specifici cart
```

---

## Installazione

```bash
cd pagopa-platform-integration-test
pip install -r requirements.txt
```

---

## Variabili d'ambiente

Le variabili sono definite in `config/api-test/.env.<env>`.

| Variabile              | Descrizione                     | Esempio                              |
|------------------------|---------------------------------|--------------------------------------|
| `CHECKOUT_HOST`        | URL base delle API              | `https://api.dev.platform.pagopa.it` |
| `NOTICE_CODE_PREFIX`   | Prefisso del codice avviso      | `3020`                               |
| `VALID_FISCAL_CODE_PA` | Codice fiscale della PA di test | `77777777777`                        |

---

## Esecuzione dei test — cart-tests

I test si lanciano dalla **root del repository** (`pagopa-platform-integration-test/`).

### Solo output a terminale

```bash
behave src/bdd/cart -D env=<environment> -f allure_behave.formatter:AllureFormatter -o reports\allure-results\<suite>-tests-<environment> -f progress
```

### Con Allure (consigliata)

**Passo 1 — preparare la directory e produrre i risultati Allure**

```powershell
# Da pagopa-platform-integration-test/

# Pulire la directory di output (necessario su Windows con allure-behave 2.x)
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\cart-dev
New-Item reports\allure-results\cart-dev -ItemType Directory -Force | Out-Null

# Eseguire i test con formatter Allure
behave src/bdd/cart -D env=dev -f allure_behave.formatter:AllureFormatter -o reports/allure-results/cart-dev -f progress
```

> **Nota sull'ordine dei formatter**: `-o` si associa al **primo** `-f`.
> `AllureFormatter` deve venire **prima** di `-f progress`, altrimenti `progress` riceve
> il percorso della directory e genera un `PermissionError`.

**Passo 2 — visualizzare il report**

Il comando da usare dipende dalla versione di Allure CLI installata:

```powershell
allure --version   # verifica la versione
```

| Versione Allure CLI | Comando                                                                   |
|---------------------|---------------------------------------------------------------------------|
| **2.x** (legacy)    | `allure serve reports/allure-results/cart-dev --port 5300`                |
| **3.x** (corrente)  | `allure open reports/allure-results/cart-dev --port 5300`                 |

> In Allure 3.x i comandi `allure serve` e `allure open` sono equivalenti.
> Entrambi generano il report HTML in una directory temporanea, avviano un server locale
> e aprono il browser. La differenza rispetto a Allure 2.x è solo nel nome del comando
> (in 2.x esisteva solo `allure serve`; in 3.x è stato aggiunto `allure open` come alias).

Esempio completo (UAT):

```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue reports\allure-results\cart-uat
New-Item reports\allure-results\cart-uat -ItemType Directory -Force | Out-Null
behave src/bdd/cart -D env=uat -f allure_behave.formatter:AllureFormatter -o reports/allure-results/cart-uat -f progress
allure serve reports/allure-results/cart-uat --port 5300
```

---

## Architettura

### Separazione delle responsabilità

| File                                | Responsabilità                                              |
|-------------------------------------|-------------------------------------------------------------|
| `src/utility/api_test/api_test_environment.py` | Hook comuni: caricamento `.env`, reset `context.response` |
| `src/utility/api_test/cart/cart_helpers.py`    | Helper HTTP e data builder specifici dei cart-test        |
| `src/bdd/cart/environment.py`       | Delega a `api_test_environment` + reset stato cart         |
| `src/bdd/cart/steps/cart_steps.py`  | Step definitions Behave (importa da `cart_helpers`)        |

### Flusso di esecuzione

```
behave src/bdd/cart -D env=dev
    │
    ├─ cart/environment.py → before_all()
    │      └─ api_test_environment.before_all() → carica config/api-test/.env.dev
    │
    ├─ cart/environment.py → before_scenario()
    │      └─ api_test_environment.before_scenario() → reset context.response
    │      └─ reset context.notice_code, fiscal_code, cart_id
    │
    ├─ Per ogni Scenario:
    │   ├─ Given → configura host, genera noticeCode, legge fiscalCode da env
    │   ├─ When  → POST con requests (allow_redirects=False)
    │   └─ Then  → verifica status code, header, estrazione CART_ID
    │
    └─ Genera reports/allure-results/cart-{env}/
```
