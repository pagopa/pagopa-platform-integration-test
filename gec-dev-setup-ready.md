# 🚀 GEC DEV Setup - COMPLETATO!

**Data:** 2026-11-20  
**Validazione:** ✅ 4/5 check passati

---

## ✅ Cosa è stata fatto

| Item | Stato | File |
|------|-------|------|
| **dev.yaml compilato** | ✅ PRONTO | `src/integration/gec/dev.yaml` |
| **Configurazione GEC** | ✅ CARICATA | URL v1/v2, timeout, auth |
| **Dati di test** | ✅ INCLUSI | PSP ID, CI ID, payment methods |
| **Environment hooks** | ✅ IMPORTABILI | `before_all`, `before_scenario` |
| **Step bindings** | ✅ COMPILATI | 31 binding in `feat_001_common_steps.py` |
| **Payload templates** | ✅ CARICABILI | 28.8 KB di test data |

---

## ⚠️ UNICO PASSO RIMANENTE: Popolare il Secret API Key

### 1. Modifica `config/.secrets.yaml`

Sostituisci `<SUBKEY_FROM_ENV>` con la **chiave API DEV reale**:

```yaml
dev:
  afm-subscription-key: "YOUR_ACTUAL_SUBKEY_HERE"
```

**Dove trovare la chiave:**
- Contatta DevOps per la chiave DEV di AFM/GEC
- Variabile d'ambiente: `SUBKEY` nella documentazione .env.dev

---

## 🧪 Comandi per Eseguire i Test

### A. Validazione Configurazione

```powershell
# Verifica che tutto sia configurato correttamente
$env:TARGET_ENV = "dev"
python gec-validate-dev-setup.py
```

**Risultato atteso:**
```
✅ PASS | dev.yaml
✅ PASS | .secrets.yaml                    # (dopo aver riempito la chiave)
✅ PASS | Configuration loader
✅ PASS | Environment hooks
✅ PASS | Step bindings

Result: 5/5 checks passed
```

---

### B. Dry-Run (verifica step binding senza eseguire)

```powershell
# Controlla che tutti gli step siano mappati
$env:TARGET_ENV = "dev"
python -m behave src/integration/gec --dry-run --no-color
```

**Output atteso:**
- 7 feature files trovati
- ~50 scenari @runnable
- 0 undefined steps
- 148~ steps riconosciuti

**Esempio output:**
```
7 features, 50 scenarios, 148 steps
```

---

### C. Esecuzione Suite Completa

```powershell
# Esegui tutti i test GEC con report Allure
$env:TARGET_ENV = "dev"
$suite = "gec"
$runId = "run-001"
$attemptId = "initial-00"
$outDir = "reports\allure-results\$suite-dev\$runId\$attemptId"

# Crea directory
New-Item -Path $outDir -ItemType Directory -Force | Out-Null

# Esegui
python -m behave "src\integration\$suite" `
    -f allure_behave.formatter:AllureFormatter -o $outDir `
    -f progress --summary --show-timings

# Visualizza report
allure serve $outDir --port 8080
```

---

## 📊 Validazione di Configurazione Dettagliata

| Componente | Test | Risultato |
|---|---|---|
| **dev.yaml** | File exists and populated | ✅ 1063 bytes |
| **Configuration loader** | Dynaconf carica dev.yaml | ✅ OK |
| **GEC config** | Attribute `gec` exists | ✅ Found |
| **GEC URL** | API endpoint resolvibile | ✅ `https://api.dev.platform.pagopa.it/afm/calculator-service/v1` |
| **GEC Auth** | Type is api-key | ✅ Configured |
| **Secret key** | Has placeholder | ⚠️ **POPULATE** |
| **Environment hooks** | before_all importabile | ✅ OK |
| **Step bindings** | feat_001_common_steps importabile | ✅ OK |
| **Global config** | Test data (PSP, CI) | ✅ Included |

---

## 🔧 Troubleshooting

### Errore: "config/.secrets.yaml not found"
**Causa:** Esegui da directory sbagliata.  
**Soluzione:** Assicurati di eseguire da **root del repository**.

```powershell
cd C:\Users\mpiccolo\git\pagopa\pagopa-platform-integration-test
# Poi esegui i comandi
```

---

### Errore: "TARGET_ENV not set"
**Causa:** Variabile d'ambiente non settata.  
**Soluzione:** 
```powershell
$env:TARGET_ENV = "dev"
# Oppure nel .env locale se usi bash
export TARGET_ENV=dev
```

---

### Errore: "API key not found" / "401 Unauthorized"
**Causa:** Secret key nel config/.secrets.yaml non popolo.  
**Soluzione:**
1. Verifica che `config/.secrets.yaml` contenga `dev:` section
2. Verifica che `afm-subscription-key` abbia valore reale (non placeholder)
3. Testa manualmente con curl:
```bash
curl -H "Ocp-Apim-Subscription-Key: <KEY>" \
     "https://api.dev.platform.pagopa.it/afm/calculator-service/v1"
```

---

### Errore: "Undefined step" nel dry-run
**Causa:** Step bindings non caricate.  
**Soluzione:**
1. Verifica che `src/integration/gec/steps/__init__.py` esista
2. Verifica che `feat_001_common_steps.py` sia leggibile
3. Esegui validazione:
```powershell
python -c "import src.integration.gec.steps.feat_001_common_steps; print('OK')"
```

---

## 📝 Configurazione Attuale (dev.yaml)

```yaml
gec:
  url: https://api.dev.platform.pagopa.it/afm/calculator-service/v1
  url_v2: https://api.dev.platform.pagopa.it/afm/calculator-service/v2
  extension: "?maxOccurrences=10"
  timeout: 5000
  auth:
    type: api-key
    key_name: Ocp-Apim-Subscription-Key
    key_value: $afm-subscription-key      # ← Risolto da .secrets.yaml
    location: header

global_configuration:
  psp_id: "BPPIITRRZZZ"                   # Poste Italiane
  channel_id: "17103880000_01"
  channel_payment_id: "17103880000_02"
  primary_creditor_institution: "77777777777"
  environment: "dev"
```

---

## 📚 File Principali

- **Config:** [`src/integration/gec/dev.yaml`](src/integration/gec/dev.yaml)
- **Secret key:** [`config/.secrets.yaml`](config/.secrets.yaml) (vedi template: [`config/.secrets_template.yaml`](config/.secrets_template.yaml))
- **Step definizioni:** [`src/integration/gec/steps/feat_001_common_steps.py`](src/integration/gec/steps/feat_001_common_steps.py)
- **Environment hooks:** [`src/integration/gec/environment.py`](src/integration/gec/environment.py)
- **Validatore:** [`gec-validate-dev-setup.py`](gec-validate-dev-setup.py)

---

## ✅ Checklist Finale

Dopo aver completato questi step, sei pronto per eseguire i test:

- [ ] Ho ricevuto la **chiave API DEV** per AFM/GEC da DevOps
- [ ] Ho popolo `config/.secrets.yaml` con `dev.afm-subscription-key: "<chiave>"`
- [ ] Ho eseguito `python gec-validate-dev-setup.py` → **5/5 check passati**
- [ ] Ho eseguito dry-run → **0 undefined steps**
- [ ] Ho eseguito la suite completa → **scenario passed/failed raccolti**

---

**Prossimi step dopo i test:**
1. Revisione risultati nel report Allure
2. Se test falliscono: Estendere step bindings in `feat_002-007_steps.py`
3. Se test passano: Aggiornare README e processare i risultati

---

**Generato da QA-orchestrator | 2026-11-20**
