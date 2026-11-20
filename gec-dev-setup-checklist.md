# GEC Integration Test - Setup per DEV

**Data:** 2026-11-20  
**Stato:** ⚠️ Implementation completato, **configurazione incompleta per esecuzione**

---

## 📋 Checklist Pre-Esecuzione

### ✅ COMPLETATO

| Item | File/Componente | Status |
|------|---|---|
| Step definitions (common) | `src/integration/gec/steps/feat_001_common_steps.py` | ✅ 31 binding |
| Step placeholders | `src/integration/gec/steps/feat_002-007_steps.py` | ✅ 7 file |
| Test data payloads | `src/integration/gec/payload.yaml` | ✅ 28.8 KB |
| Environment hooks | `src/integration/gec/environment.py` | ✅ before_all, before_scenario |
| Feature files | `src/integration/gec/feature/*.feature` | ✅ 7 file tradotti |
| Helper utilities | `src/integration/gec/helper.py` | ✅ Core logic |
| Python requirements | `requirements.txt` | ✅ behave, requests, dynaconf, etc. |

---

### ❌ MANCANTE - CRITICO

#### 1. **Configurazione dell'ambiente DEV (`dev.yaml`)**

📄 **File:** `src/integration/gec/dev.yaml`  
**Stato:** Vuoto (0 bytes)

**Cosa configurare:**

```yaml
# Endpoint GEC API
services:
  gec:
    url: https://api.dev.platform.pagopa.it/gec/service/v1  # ⚠️ Verificare URL reale
    timeout: 5000
    auth:
      type: api-key
      key_name: Ocp-Apim-Subscription-Key
      key_value: $tas-gec-subscription-key        # ⚠️ Variabile TAS/secret
      location: header

# Configurazioni globali
global_configuration:
  psp_id: "88888888888"                           # ⚠️ PSP ID di test
  primary_creditor_institution: "77777777777"     # ⚠️ CI ID di test
  broker_psp: "88888888888"
  environment: "dev"
```

**Domande chiave:**
- Qual è l'URL esatto dell'API GEC su DEV?
- Qual è il nome della chiave API (subscription key)?
- Come sono esposti i secret? (TAS, KeyVault, file locale?)
- Quali sono i dati di test per PSP e CI?

---

#### 2. **Secret Management (`.secrets.yaml`)**

📄 **File:** `config/.secrets.yaml` (configurato via `config/.secrets_template.yaml`)

**Stato:** Mancante

**Cosa fare:**

Creare `config/.secrets.yaml` a partire dal template:

```bash
cp config/.secrets_template.yaml config/.secrets.yaml
```

**Poi popolare con i secret DEV:**

```yaml
tas-gec-subscription-key: "<ACTUAL_API_KEY>"
# Eventuali altri secret per autenticazione
```

**⚠️ IMPORTANTE:** 
- Non committare `.secrets.yaml` su Git (è in `.gitignore`)
- Verificare che `configuration.py` risolva correttamente i placeholder `$tas-gec-*`

---

#### 3. **Risoluzione del Percorso di Configurazione**

**Problema individuato (segnalato da QA-engineer):**

Nel `environment.py` il client GEC è cercato con:

```python
gec_service_config = _config_value(context.config, "services", "gec")
```

Questo presuppone una struttura:

```
context.config["services"]["gec"] = { url, auth, ... }
```

**Verifica necessaria:**

Controllare come `load_configurations()` carica il YAML e se expone `services`:

```bash
python -c "
from src.conf.configuration import load_configurations
import os
os.chdir('src/integration/gec')
config = load_configurations('.')
print('Config keys:', list(config.keys()))
if 'services' in config:
    print('Services:', list(config['services'].keys()))
"
```

Se la struttura è diversa, aggiornare `environment.py` di conseguenza.

---

#### 4. **Variabili d'Ambiente per l'Esecuzione**

Quando esegui il test, assicurati di settare:

```bash
# PowerShell
$env:TARGET_ENV = "dev"

# Bash
export TARGET_ENV=dev
```

**Dove è usato:**
- Seleziona `dev.yaml` nella cartella della suite
- Popola placeholder variables nel contesto (vedi `_populate_placeholder_vars()`)

---

### ⚠️ VALIDAZIONI CONSIGLIATE PRIMA DELL'ESECUZIONE

#### 1. **Dry-run per verificare step binding**

```bash
cd C:\Users\mpiccolo\git\pagopa\pagopa-platform-integration-test

$env:TARGET_ENV = "dev"

python -m behave src/integration/gec --dry-run --no-color --format plain
```

**Output atteso:**
- 0 undefined steps
- Tutti i 148~ step lines mappati
- 50+ scenari riconosciuti

---

#### 2. **Test di configurazione**

Verifica che il client GEC sia inizializzato:

```bash
python -c "
from behave import configuration
from behave.runner import Runner
from src.integration.gec.environment import before_all
from types import SimpleNamespace

context = SimpleNamespace()
context.config = None

before_all(context)
print('GEC client:', context.gec.rest.client)
print('Config keys:', list(context.config.keys()))
"
```

**Risultato atteso:**
- GEC REST client inizializzato (non None)
- Config contiene `services.gec` oppure equivalente

---

#### 3. **Connettività API**

```bash
# Verifica che l'endpoint DEV sia raggiungibile
curl -I "https://api.dev.platform.pagopa.it/gec/service/v1"

# Se richiede chiave API:
curl -H "Ocp-Apim-Subscription-Key: <your-key>" \
     "https://api.dev.platform.pagopa.it/gec/service/v1"
```

---

### 📦 ESECUZIONE EFFETTIVA (Una volta risolti i blocchi sopra)

```powershell
# PowerShell from repo root

$env:TARGET_ENV = "dev"
$suite = "gec"
$runId = "run-001"
$attemptId = "initial-00"
$outDir = "reports\allure-results\$suite-$env:TARGET_ENV\$runId\$attemptId"

# Creare directory output
New-Item -Path $outDir -ItemType Directory -Force | Out-Null

# Eseguire i test
python -m behave "src\integration\$suite" `
    -f allure_behave.formatter:AllureFormatter -o $outDir `
    -f progress --summary --show-timings

# Output Allure report
allure serve $outDir --port 8080
```

---

## 🔧 Troubleshooting Comuni

### Problema: "GEC service configuration not found"

**Causa:** `dev.yaml` è vuoto o `load_configurations()` non lo carica.

**Soluzione:**
1. Compilare `dev.yaml` con la struttura corretta
2. Verificare che `load_configurations('src/integration/gec')` trovi il file
3. Debuggare `_config_value()` per verificare la navigazione della struttura

---

### Problema: "Undefined step" durante dry-run

**Causa:** Step bindings non caricate o mismatch di testo.

**Soluzione:**
1. Verificare che `src/integration/gec/steps/__init__.py` esista
2. Verificare imports in `feat_001_common_steps.py`
3. Eseguire `python -c "from src.integration.gec.steps.feat_001_common_steps import *"` per verificare imports

---

### Problema: "API key not found" o "401 Unauthorized"

**Causa:** Secret non risolto o chiave API errata.

**Soluzione:**
1. Verificare che `config/.secrets.yaml` contenga `tas-gec-subscription-key`
2. Verificare che `configuration.py` risolva correttamente i placeholder `$`
3. Testare manualmente curl con la chiave effettiva

---

### Problema: "Payload TEST_DATA not found"

**Causa:** `helper.py` non trova payload nel contesto.

**Soluzione:**
1. Verificare che `payload.yaml` contenga la chiave richiesta sotto `TEST_DATA`
2. Verificare che `load_commondata()` popoli `context.payload_templates` in `before_all()`
3. Debuggare `_load_payload()` per verificare l'estrazione

---

## 📝 Fasi di Setup Consigliate

| Fase | Azione | Responsabile | Tempo Est. |
|------|--------|---|---|
| 1 | Compilare `dev.yaml` con endpoint e auth | DevOps/QA | 15 min |
| 2 | Popolare `config/.secrets.yaml` | DevOps | 10 min |
| 3 | Verificare risoluzione config con `load_configurations()` | QA-engineer | 15 min |
| 4 | Eseguire dry-run behave | QA-runner | 5 min |
| 5 | Test di connettività API (curl) | QA-runner | 5 min |
| 6 | Esecuzione suite completa | QA-runner | 10-30 min |

**Tempo totale:** ~1 ora

---

## 📚 Referenze

- **GEC Helper:** [`src/integration/gec/helper.py`](src/integration/gec/helper.py)
- **GEC Environment:** [`src/integration/gec/environment.py`](src/integration/gec/environment.py)
- **FdR3 Baseline (config):** [`src/integration/fdr3/dev.yaml`](src/integration/fdr3/dev.yaml)
- **Configuration Loader:** [`src/conf/configuration.py`](src/conf/configuration.py)
- **Utility REST:** [`src/utility/rest/README.md`](src/utility/rest/README.md)

---

## 🎯 Prossimi Step

1. **Coinvolgere DevOps** per endpoint GEC API e credenziali DEV
2. **Compilare `dev.yaml`** con configurazione di staging
3. **Creare `config/.secrets.yaml`** con chiave API
4. **Validare configurazione** con dry-run
5. **Eseguire prima suite di test** e raccogliere feedback
6. **Estendere step files** (feat_002-007) se necessario post-esecuzione

---

**Generato da QA-orchestrator | 2026-11-20 | Commit: 339b6a813a**
