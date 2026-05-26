# Test Automation Service — Architettura

## Panoramica

Il **Test Automation Service (TAS)** è un'infrastruttura centralizzata di integration testing
ospitata nel repository GitHub `pagopa-platform-integration-test`.

Espone tre interfacce di integrazione in modo che qualsiasi sistema esterno — un workflow GitHub Actions,
una pipeline Azure DevOps o qualsiasi altro strumento CI/CD — possa lanciare suite di test BDD
(Behave + Playwright), attendere l'esito e prendere decisioni (ad esempio bloccare un deploy)
in base ai risultati.

---

## Diagramma dell'architettura

```
┌───────────────────────────────────────────────────────────────────────-─┐
│                        CHIAMANTI (sistemi esterni)                      │
│                                                                         │
│  ┌──────────────────┐   ┌──────────────────-┐   ┌─────────────────────┐ │
│  │  GitHub Actions  │   │  GitHub Actions   │   │    Azure DevOps /   │ │
│  │  (workflow_call) │   │ (test_orchestr.py)│   │  qualsiasi CI/CD    │ │
│  └────────┬─────────┘   └────────┬────────-─┘   └──────────┬──────────┘ │
└───────────┼──────────────────────┼──────────────────────-──┼────────────┘
            │ workflow_call        │ workflow_dispatch       │ workflow_dispatch
            │ (sincrono,           │ + polling + artifact    │ + polling + artifact
            │  output nativi)      │ download (sync/async)   │ download (sync/async)
            │                      │                         │
            ▼                      ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            pagopa-platform-integration-test  (GitHub repo)              │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │          test-automation-service.yml  (GHA Workflow)             │   │
│  │                                                                  │   │
│  │  Input: test_suite, environment, caller_id, correlation_id       │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌───────────────┐  ┌────────────┐  ┌──────────┐   │   │
│  │  │ Checkout │→ │ Esecuzione    │→ │  Parsing   │→ │ Upload   │   │   │
│  │  │ + Setup  │  │ Behave        │  │  risultati │  │ artifact │   │   │
│  │  └──────────┘  └───────────────┘  └────────────┘  └──────────┘   │   │
│  │                                          │                       │   │
│  │                                          ▼                       │   │
│  │                               test-summary.json                  │   │
│  │                               behave-results.json                │   │
│  │                               junit/*.xml                        │   │
│  │                                                                  │   │
│  │  Output (workflow_call): passed, failed, skipped, total,         │   │
│  │                          duration, outcome                       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌───────────────────────┐                                              │
│  │  tas_orchestrator.py │  Bridge CLI usato dai CI/CD esterni          │
│  │  (script Python)      │  per lanciare, fare polling e leggere esiti  │
│  └───────────────────────┘                                              │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Componenti

### 1. `test-automation-service.yml` — Workflow principale

Il workflow GHA centrale che esegue le suite di test. Supporta due meccanismi di attivazione:

| Trigger | Descrizione |
|---|---|
| `workflow_call` | Invocazione sincrona da un altro workflow GHA. Espone output tipizzati direttamente. |
| `workflow_dispatch` | Invocazione event-based tramite GitHub API. Per natura fire-and-forget; i risultati sono disponibili come artifact. |

**Input:**

| Nome | Tipo | Obbligatorio | Descrizione |
|---|---|---|---|
| `test_suite` | string | ✅ | Suite di test da eseguire (`wisp`, `all`) |
| `environment` | string | ✅ | Ambiente target (`dev`, `uat`) |
| `caller_id` | string | ❌ | Identificativo del sistema chiamante per la tracciabilità |
| `correlation_id` | string | ❌ | ID univoco per correlare la run con il chiamante |

**Output** (disponibili solo via `workflow_call`):

| Nome | Tipo | Descrizione |
|---|---|---|
| `passed` | string | Numero di scenari superati |
| `failed` | string | Numero di scenari falliti |
| `skipped` | string | Numero di scenari saltati |
| `total` | string | Numero totale di scenari |
| `duration` | string | Tempo totale di esecuzione in secondi |
| `outcome` | string | `success` oppure `failure` |

**Artifact prodotto:** `test-results` (zip), contenente:
- `test-summary.json` — riepilogo strutturato (vedi schema sotto)
- `behave-results.json` — output JSON grezzo di Behave
- `junit/*.xml` — report JUnit XML

### 2. `tas_orchestrator.py` — Bridge CLI

Script Python che racchiude la `workflow_dispatch` API con due modalità operative:

| Modalità | Flag | Comportamento |
|---|---|---|
| **Async** | _(default)_ | Invia il dispatch, stampa `CORRELATION_ID` e `RUN_NAME`, esce con `0` immediatamente |
| **Sync** | `--sync` | Invia il dispatch, fa polling fino al completamento, scarica l'artifact, analizza i risultati, stampa il riepilogo, esce con `0` (successo) o `1` (fallimento) |

Lo script utilizza il campo `run-name` (impostato a `tas-{correlation_id}`) per individuare
la run corretta tramite GitHub API, rendendolo robusto rispetto alle esecuzioni concorrenti.

**Dipendenze:** `requests` (già presente in `requirements.txt`)

**Variabile d'ambiente obbligatoria:** `GITHUB_TOKEN` — un PAT con scope `repo` e `actions:read`.

---

## Schema dell'artifact — `test-summary.json`

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "caller_id":      "pagopa-checkout",
  "suite":          "wisp",
  "environment":    "uat",
  "passed":         42,
  "failed":         0,
  "skipped":        3,
  "total":          45,
  "duration_seconds": 134.7,
  "outcome":        "success"
}
```

---

## Riepilogo delle interfacce di integrazione

| Interfaccia | Tipo di chiamante | Sincrono | Risultati accessibili | Infra richiesta |
|---|---|---|---|---|
| `workflow_call` | Solo GHA | ✅ | ✅ output nativi | Nessuna |
| `workflow_dispatch` (raw) | Qualsiasi | ❌ | ❌ | Nessuna |
| `tas_orchestrator.py --sync` | Qualsiasi CI/CD | ✅ | ✅ via stdout + exit code | Python + requests |
| `tas_orchestrator.py` (async) | Qualsiasi CI/CD | ❌ | ❌ (correlation_id stampato) | Python + requests |

---

## Sicurezza

- Tutti i segreti di test (credenziali d'ambiente, endpoint, ecc.) sono memorizzati nel secret `INTEGRATION_TESTS_SECRETS` nell'**environment `integration-tests`** del repository TAS centralizzato. I chiamanti non devono configurare né passare alcun segreto di test.
- Il job `run_tests` dichiara `environment: integration-tests`: questo garantisce che le environment-level secrets del repo TAS siano disponibili al workflow anche quando viene invocato via `workflow_call` da un repository esterno.
- Il PAT `GITHUB_TOKEN` usato da `tas_orchestrator.py` deve avere gli scope minimi necessari: `repo` (per leggere i dati della run) e `actions:read` (per elencare e scaricare gli artifact). Deve essere conservato come secret nel sistema CI/CD del chiamante e non va mai inserito in chiaro nel codice.
- Il `correlation_id` viene usato esclusivamente per individuare la run e non contiene informazioni sensibili.
