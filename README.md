# pagopa-platform-integration-test

Repository di test di integrazione, API ed end-to-end per componenti della piattaforma pagoPA.
Le suite sono scritte principalmente in Python con Behave/Gherkin e producono report Allure;
alcune suite usano Playwright.

## Indice

- [Panoramica](#panoramica)
- [Struttura del repository](#struttura-del-repository)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Suite disponibili](#suite-disponibili)
- [Esecuzione locale](#esecuzione-locale)
- [Report Allure](#report-allure)
- [FDR api test](#fdr-api-test)
- [Esecuzione in CI](#esecuzione-in-ci)
- [Servizio di test riusabile](#servizio-di-test-riusabile)
- [Documentazione scenari](#documentazione-scenari)
- [Contribuire](#contribuire)
- [Release e versionamento](#release-e-versionamento)
- [Troubleshooting](#troubleshooting)
- [Tracciabilita delle fonti](#tracciabilita-delle-fonti)

## Panoramica

Il repository raccoglie scenari BDD e script di automazione per:

- Test API e servizi, sotto `src/api/<suite>/`.
- Test flussi di integrazione, sotto `src/integration/<suite>/`.
- Test flussi end-to-end , sotto `src/e2e/<suite>/`.

Ogni suite Behave va eseguita dalla root del repository, puntando alla cartella della singola
suite. 

Riferimenti: struttura `src/`, `behave.ini`, `requirements.txt`, regole operative di
progetto.

## Struttura del repository

```text
pagopa-platform-integration-test/
├── behave.ini                       # configurazione globale Behave
├── requirements.txt                 # dipendenze Python
├── config/
│   └── .secrets_template.yaml       # template segreti per suite di integrazione
├── scripts/
│   └── tas_orchestrator.py          # bridge CLI per avviare workflow di test
├── src/
│   ├── api/                         # suite API Behave
│   │   ├── auth-service/
│   │   ├── cart/
│   │   ├── checkout-npg/
│   │   ├── ecommerce-cdc/
│   │   ├── config/
│   │   │   ├── .env.dev             # variabili API test DEV
│   │   │   └── .env.uat             # variabili API test UAT
│   │   └── utility/                 # hook comuni e helpers
│   ├── integration/                 # suite integrazione Behave
│   │   ├── commondata.yaml          # dati condivisi per le suite che li usano
│   │   ├── wisp/
│   │   │   └── utility/             # helpers SOAP, request builder, routing
│   │   ├── fdr3/
│   │   ├── cup/
│   │   └── tas_{pass,mixed,fail}/   # suite dimostrative TAS
│   └── e2e/
│       └── checkout/                # Checkout E2E Behave/Playwright
├── reports/                         # output locali (allure-results/allure-html)
└── .github/
  ├── workflows/                   # workflow GitHub Actions
  ├── scripts/                     # script di pubblicazione report
  ├── templates/                   # template HTML storico report
  ├── gherkin-manifest.yml         # manifest dei feature file per QA Central Hub
  └── html/                        # dashboard GitHub Pages
```

Riferimenti: struttura workspace, `.gitignore`, `.github/workflows/*`, `.github/scripts/*`,
`.github/templates/history-index-template.html`, `.github/html/index.html`.

## Requisiti

| Requisito | Uso | Versione indicativa |
|---|---|---|
| Python | suite Behave, script di reportistica | 3.8+ |
| pip | installazione dipendenze Python | versione recente |
| Java | Allure CLI e workflow report | 17 consigliata |
| Allure CLI | generazione e apertura report | 2.x compatibile |
| Node.js + npm | Playwright JS | 18+ consigliata |
| jq | parsing JSON nei workflow Linux | richiesto in CI FdR e AI report analysis |

Dipendenze Python principali presenti nel progetto:

- `behave==1.2.6`
- `allure-behave==2.13.5`
- `allure-python-commons==2.13.5`
- `python-dotenv>=1.0.0`
- `requests==2.32.4`
- `dynaconf==3.2.13`
- `jinja2`
- `markdown==3.8.1`

Riferimenti: `requirements.txt`, `.github/workflows/nrt-run-suite.yml`,
`.github/workflows/deploy-test-report.yml`.

## Installazione

### Framework ACE (embedded)

Repository originale di ACE: [daniele-quero/ace](https://github.com/daniele-quero/ace).

Questo repository include un runtime ACE embedded per la raccolta delle trace di task e per il workflow di reflection del team. Per installare/configurare il framework, fare riferimento al README interno di ACE:

- [ace/README_EMBEDDED.md](./ace/README_EMBEDDED.md)
- [ace/README_EMBEDDED_IT.md](./ace/README_EMBEDDED_IT.md)

### Dipendenze Python del repository

Da PowerShell o Bash, entrare nella root del repository e installare le dipendenze Python:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Privacy delle trace ACE con Presidio

Il progetto include un addon project-owned per anonimizzare le trace ACE prima che vengano usate da contatori, threshold e reflector. La policy e il workflow sono documentati qui:

- [scripts/ace-addons/privacy/README.md](./scripts/ace-addons/privacy/README.md)

Per le suite Node.js opzionali:

```bash
cd src/e2e/checkout
npm install
npx playwright install
```

Per le suite Python che usano Playwright, se il pacchetto non e gia presente
nell'ambiente locale:

```bash
pip install playwright
playwright install chromium
```

Riferimenti: `requirements.txt`, `src/e2e/checkout/package.json`,
`src/e2e/checkout/environment.py`.

## Configurazione

### API test

Le suite in `src/api/<suite>/` caricano automaticamente il file:

```text
src/api/config/.env.<env>
```

L'ambiente si seleziona tramite la variabile d'ambiente `TARGET_ENV` (default: `dev`).

PowerShell:

```powershell
$env:TARGET_ENV = "uat"
```

Bash:

```bash
export TARGET_ENV=uat
```

Variabili comuni:

| Variabile | Descrizione |
|---|---|
| `CHECKOUT_HOST` | host API Checkout per DEV/UAT |
| `NOTICE_CODE_PREFIX` | prefisso per generare notice code casuali |
| `VALID_FISCAL_CODE_PA` | codice fiscale EC valido |
| `USE_BETA_BACKEND_HEADER` | header di routing blue/green globale |
| `DEPLOYMENT_*` | routing specifico per payment-methods, payment-requests, transactions |
| `NPG_*` | host e dati carta test NPG |

Riferimenti: `src/api/config/.env.dev`, `src/api/config/.env.uat`,
`src/api/utility/api_test_environment.py`.

### Integration test

WISP e FdR3 caricano `<TARGET_ENV>.yaml` dalla directory della suite. WISP usa
anche `src/integration/commondata.yaml`; FdR3 carica `payloads.yaml` dalla
propria directory. I segreti sono risolti secondo la configurazione locale o
Azure. Se `TARGET_ENV` non è impostata, il loader usa `uat` come default.

Preparare i segreti locali partendo dal template:

```bash
cp config/.secrets_template.yaml config/.secrets.yaml
```

Il file `config/.secrets.yaml` è ignorato da git e deve contenere le subscription key e le
password richieste dalle chiamate verso Nodo, Technical Support e canali WISP/Checkout.

PowerShell:

```powershell
$env:TARGET_ENV = "uat"
```

Bash:

```bash
export TARGET_ENV=uat
```

Riferimenti: `src/integration/wisp/environment.py`, `src/integration/fdr3/environment.py`,
`config/.secrets_template.yaml`, `src/conf/configuration.py`, `.gitignore`.

### E2E test

Checkout carica `<TARGET_ENV>.yaml` dalla directory della suite tramite
`load_configurations`; senza selettore usa UAT. Il loader corrente non legge
`ENV_FILE`. L'esempio seleziona UAT, ambiente registrato per Checkout NRT.
Nell'hook `HEADLESS` e `E2E_TIMEOUT_MS` vengono prima dalla configurazione:
le variabili omonime sono fallback, non override garantiti.

PowerShell:

```powershell
$env:TARGET_ENV = "uat"
$env:HEADLESS = "true"
$env:E2E_TIMEOUT_MS = "80000"
```

Bash:

```bash
export TARGET_ENV=uat
export HEADLESS=true
export E2E_TIMEOUT_MS=80000
```

Riferimenti: `src/e2e/checkout/environment.py`, `src/conf/configuration.py`,
`src/e2e/checkout/uat.yaml`, `.github/nrt-suites.json`.

### Gestione dei secret

L'applicazione fa uso di svariati secret per eseguire correttamente le suite di test.
I secret utilizzati dall'applicazione possono essere:
- risolti da un file di secret (per il testing in locale);
- risolti dal key vault Azure relativo all'ambiente di test (dev, uat).

Inoltre, è presente l'`ApimSubscriptionResolver`, utilizzato per risolvere le subscription key dei servizi, leggendole dal servizio APIM di Azure relativo all'ambiente di test (dev,uat), al momento però **non è impiegato**.


#### Requisiti comuni
Per entrambe le casistiche, è necessario che nel workspace sia presente:
- un file specifico per la singola suite, denominato "{target_env}.yaml" (es. uat.yaml), contenente sia i secrets della suite che le sue configurazioni (es. url di un servizio, timeout, ecc...)


L'applicazione risolverà poi i secret presenti nel file e li riassegnerà ai propri attributi all'interno dell'oggetto configuration ricavato dal file "{target_env}.yaml", per accedere al secret bisognerà richiamarlo utilizzando il nome ad esso associato nel file in cui è presente. 

Esempio:
```
 context.config.NOME_SECRET
```  

È necessario che il file sia inserito manualmente nel workspace, sotto la cartella root a cui appartengono i suoi secret e le sue config.

Esempio:
```
 file uat.yaml di wisp --> posizionare sotto src/integration/wisp
 ```

Il formato dei secret da risolvere all'interno dei file JSON **DEVE** essere il seguente:
` "NOME_NON_VINCOLANTE" : "$NOME_SECRET_VINCOLANTE" `.

Il nome dell'attributo non è vincolante in quanto rappresenta solo il nome che utilizzeremo all'interno del codice per accedere al secret, il valore dell'attributo invece è vincolante in quanto sarà utilizzato per individuare il secret da cui leggere il valore, che sarà poi settato come valore per quell'attributo.


```
FLUSSO D'ESEMPIO:
- Ho un attributo "API_KEY_TEST" : "$API_KEY_WISP"
- Il resolver cerca un secret denominato API_KEY_WISP
- Lo trova e lo sostituisce a "$API_KEY_WISP" nel file JSON 
- "API_KEY_TEST" : "XXXXXXXXX"
- Accedo all'attributo nel codice con "context.config.API_KEY_TEST"
```

Esempio di un file uat.yaml:

```
VALID_FISCAL_CODE: 77777777777
INVALID_FISCAL_CODE: 77777777776
EMAIL: example.email@domain.com
TEST_DATA:
    tests:
        - skipTest: true
          testingX: TEST_X
          testingY: TEST_Y
          secretX: $secret_placeholder
        - skipTest: false
          testingX: X_TEST
          testingY: Y_TEST
          secretX: $secret_placeholder_new
```

L'applicazione ha bisogno che sia settata la seguente variabile d'ambiente:
- `TARGET_ENV` -> Utilizzata per indicare quale file .yaml utilizzare per le config

Per utilizzare la logica di caricamento settings e risoluzione secrets, è necessario utilizzare il metodo `load_configuration` presente in `src/conf/configuration.py`, passando come parametro il path alla cartella dalla quale si vuole leggere il file {target_env}.yaml.

Esempio:
```
context.config = load_configurations(os.path.dirname(os.path.abspath(__file__)))
```

#### Risoluzione secret in locale
Per la risoluzione locale dei secret è necessario che sia presente un file `secrets.yaml` sotto `./config/`, affinchè il sistema possa utilizzarlo per risolvere i secret presenti nel file di config, e che il file in questione sia diviso per env.

Esempio:
```
uat:
  secret_1: XXX
  secret_2: YYY
dev:
  secret_1: XXX
  secret_2: YYY
```

#### Autenticazione Azure
L'autenticazione verso Azure avviene tramite `DefaultAzureCredential`, che prova in sequenza le credenziali disponibili nell'ambiente di esecuzione fino a trovare un'identità valida. Questo meccanismo viene usato sia per la risoluzione dei secret dal Key Vault Azure sia per il recupero delle subscription key da APIM, così da avere un unico modello di autenticazione per entrambi i resolver.
I principali metodi di autenticazione provati da Azure sono, in ordine:

- EnvironmentCredential -> Richiede le seguenti variabili d'ambiente:

  1.AZURE_TENANT_ID: L'ID Microsoft Entra tenant (directory).

  2.AZURE_CLIENT_ID: ID client (applicazione) di una registrazione dell'app nel tenant.

  3.AZURE_CLIENT_SECRET o AZURE_CLIENT_CERTIFICATE_PATH: Il primo è il segreto client generato per la registrazione dell'app, il secondo invece è il percorso di un certificato PEM da usare durante l'autenticazione, da usare come alternativa al client secret.


- WorkloadIdentityCredential -> Consente alle applicazioni in esecuzione su macchine virtuali (VM) di accedere ad altre risorse Azure senza la necessità di un principale di servizio o di un'identità gestita.

- ManagedIdentityCredential -> Tenta di eseguire l'autenticazione usando un'identità gestita disponibile nell'ambiente di distribuzione. Questo tipo di autenticazione funziona in VM Azure, istanze App Service, applicazioni Funzioni di Azure, Azure Kubernetes Services, istanze Azure Service Fabric e all'interno di Azure Cloud Shell.

- AzureCliCredential -> Tenta di eseguire l'autenticazione tramite lo strumento a linea di comando di Azure ("az"). Per farlo, leggerà il token di accesso utente e il tempo di scadenza con il comando interfaccia della riga di comando di Azure "az account get-access-token". Da usare in seguito ad un "az login".


#### Risoluzione secret dal Key Vault Azure
Per la risoluzione dei secret dal Key vault è necessario che sia presente la variabile d'ambiente `AZURE_KEY_VAULT_URL`, contenente l'url del Key Vault Azure; la sua presenza è necessaria anche per indicare al sistema di utilizzare il Key Vault e non il resolver locale.
 **Attenzione**: È presente un Key Vault per DEV ed uno per UAT, quindi è necessario fornire un URL differente in base all'ambiente;

#### Risoluzione secret da APIM
Per la risoluzione delle subscription key da APIM è necessario che siano presenti le variabili d'ambiente `AZURE_SUBSCRIPTION_ID`, `APIM_RESOURCE_GROUP` e `APIM_SERVICE_NAME`, così che il resolver possa creare il client di management e recuperare la subscription key corretta dal servizio APIM. Il nome del secret può essere un nome logico mappato tramite la variabile `APIM_SUBSCRIPTION_<NAME>` oppure direttamente l'identificativo della subscription APIM; inoltre, è possibile richiedere la chiave `primary` o `secondary` usando il suffisso `:primary` o `:secondary`.

## Suite disponibili

### API

| Suite | Percorso | Focus | Report locale |
|---|---|---|---|
| `auth-service` | `src/api/auth-service` | login, token, profilo utente, logout | `reports/allure-results/auth-service-<env>` |
| `cart` | `src/api/cart` | creazione carrello Checkout EC | `reports/allure-results/cart-<env>` |
| `checkout-npg` | `src/api/checkout-npg` | sessioni, transazioni, autorizzazioni e dati carta NPG | `reports/allure-results/checkout-npg-<env>` |
| `ecommerce-cdc` | `src/api/ecommerce-cdc` | flusso eCommerce CDC e stati transazione | `reports/allure-results/ecommerce-cdc-<env>` |

Tag ricorrenti: `@checkout`, `@positive`, `@negative`, `@npg`, `@cdc`,
`@authorization`, `@card`, `@payment-methods`, `@payment-verify`, `@session`,
`@transaction`.

Riferimenti: `src/api/*/features/*.feature`, `src/api/*/environment.py`.

### Integration

| Suite | Percorso | Runner | Note |
|---|---|---|---|
| `wisp` | `src/integration/wisp` | Behave | scenari `nodoInviaRPT` e `nodoInviaCarrelloRPT`, tag `@runnable` |
| `fdr3` | `src/integration/fdr3` | Behave | flussi di rendicontazione, tag `@runnable` |
| `cup` | `src/integration/cup` | Behave | scenari CUP |
| `tas_pass`, `tas_mixed`, `tas_fail` | `src/integration/tas_<esito>` | Behave | suite dimostrative TAS |

Report locali consigliati: `reports/allure-results/<suite>-<env>` per le suite Behave.
Per le suite e gli ambienti inclusi negli NRT consultare il [catalogo](.github/nrt-suites.json).

Riferimenti: `src/integration/**/features/**/*.feature`.

### End-to-end

| Suite | Percorso | Runner | Note |
|---|---|---|---|
| `checkout` | `src/e2e/checkout` | Behave + Playwright Python | feature UI Checkout sotto `features/` |

Riferimenti: `src/e2e/checkout/features/*.feature`,
`src/e2e/checkout/environment.py`, `src/e2e/checkout/tests/checkout-payment.spec.js`.

## Esecuzione locale

Tutti i comandi Behave vanno eseguiti dalla root del repository.
Gli esempi locali creano output separati per run e tentativo (`initial-00`);
per i fix usare `fix-01` fino a `fix-05`, conservando le evidenze precedenti.
Se una destinazione esiste gia, fermarsi senza sovrascriverla. Con il runner,
ambiente, selezione, effetti e politica dei tentativi richiedono un piano approvato.
Gli esempi Behave seguenti sono per una **shell dedicata**, con interprete Python
esplicitamente scelto al posto di `<approved-python-executable>` (per esempio il
percorso assoluto del virtualenv verificato). Propagano l'exit code al chiamante:
in uso interattivo conservare/riferire lo stato senza eseguire `exit`.
Non richiedono installazioni o probe live impliciti. Per suite NRT risolvere
ID, path, tag e ambienti dal [catalogo corrente](.github/nrt-suites.json);
per altre suite usare configurazione e documentazione effettive. I selettori
non provano da soli quale deployment venga usato.

Gli esempi acquisiscono stdout/stderr nel terminale/tool, non scrivono
automaticamente un log su disco: concordare una cattura conservata e riportarne
solo riferimenti reali. Tenere separati esito dei test e problemi di persistenza,
senza pubblicare output sensibili. Dettagli su interprete, configurazione,
preflight e stato remoto nelle [istruzioni di esecuzione](.github/instructions/run-tests.instructions.md).

### Singola suite API

PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
$python = (Get-Command "<approved-python-executable>" -CommandType Application -ErrorAction Stop).Source
$env:TARGET_ENV = "uat"
$suite = "cart"
$runId = [guid]::NewGuid().ToString("N")
$outDir = "reports\allure-results\$suite-$env:TARGET_ENV\$runId\initial-00"
New-Item $outDir -ItemType Directory -ErrorAction Stop | Out-Null

$LASTEXITCODE = $null
& $python -m behave "src\api\$suite" `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --summary --show-timings
$testExit = $LASTEXITCODE
if ($null -eq $testExit) { throw "Test process did not return an exit code" }
exit $testExit
```

Bash:

```bash
python="<approved-python-executable>"
command -v "$python" >/dev/null || { printf '%s\n' "Python executable unavailable" >&2; exit 1; }
export TARGET_ENV=uat
suite="cart"
run_id="$(date -u +%Y%m%dT%H%M%SZ)-${RANDOM}"
run_dir="reports/allure-results/${suite}-${TARGET_ENV}/${run_id}"
out_dir="${run_dir}/initial-00"
mkdir -p "$run_dir" || exit 1
mkdir "$out_dir" || exit 1

"$python" -m behave "src/api/${suite}" \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --summary --show-timings
test_exit=$?
exit "$test_exit"
```

Sostituire `cart` con `auth-service`, `checkout-npg` o `ecommerce-cdc`.

Riferimenti: regole operative di progetto, `src/api/utility/api_test_environment.py`,
`src/api/*/features/*.feature`.

### WISP e FdR3

L'esempio seleziona WISP. Per la suite NRT FdR3 usare `suite="fdr3"` e
confermare percorso, tag e ambiente nel catalogo. La suite legacy `fdr`
non è più presente nel repository.

PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
$python = (Get-Command "<approved-python-executable>" -CommandType Application -ErrorAction Stop).Source
$env:TARGET_ENV = "uat"
$suite = "wisp"
$env:suite = $suite
$tagArgs = @("--tags=@runnable")
$runId = [guid]::NewGuid().ToString("N")
$outDir = "reports\allure-results\$suite-uat\$runId\initial-00"
$junitDir = "reports\junit\$suite-uat\$runId\initial-00"
New-Item $outDir -ItemType Directory -ErrorAction Stop | Out-Null
New-Item $junitDir -ItemType Directory -ErrorAction Stop | Out-Null

$LASTEXITCODE = $null
& $python -m behave "src\integration\$suite" @tagArgs `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --junit-directory=$junitDir --junit --summary --show-timings -v
$testExit = $LASTEXITCODE
if ($null -eq $testExit) { throw "Test process did not return an exit code" }
exit $testExit
```

Bash:

```bash
python="<approved-python-executable>"
command -v "$python" >/dev/null || { printf '%s\n' "Python executable unavailable" >&2; exit 1; }
export TARGET_ENV=uat
export suite="wisp"
tag_args=("--tags=@runnable")
run_id="$(date -u +%Y%m%dT%H%M%SZ)-${RANDOM}"
run_dir="reports/allure-results/${suite}-uat/${run_id}"
junit_run_dir="reports/junit/${suite}-uat/${run_id}"
out_dir="${run_dir}/initial-00"
junit_dir="${junit_run_dir}/initial-00"
mkdir -p "$run_dir" "$junit_run_dir" || exit 1
mkdir "$out_dir" "$junit_dir" || exit 1

"$python" -m behave "src/integration/${suite}" "${tag_args[@]}" \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --junit-directory="$junit_dir" --junit --summary --show-timings -v
test_exit=$?
exit "$test_exit"
```

Riferimenti: `.github/workflows/nrt-run-suite.yml`, `.github/nrt-suites.json`,
`src/integration/wisp/features/`, `src/integration/fdr3/features/`.

### E2E 

L'esempio segue l'entry NRT `checkout` in UAT e i suoi due argomenti tag.
Il loader corrente legge `<TARGET_ENV>.yaml` dalla root della suite (default
UAT); non usa `ENV_FILE`. `HEADLESS` dal file di configurazione ha precedenza
sul fallback d'ambiente nell'hook. Confermare configurazione e disponibilita
del browser richiesto prima del run, senza installarlo implicitamente.

PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
$python = (Get-Command "<approved-python-executable>" -CommandType Application -ErrorAction Stop).Source
$env:TARGET_ENV = "uat"
$env:suite = "checkout"
$env:HEADLESS = "true"
$tagArgs = @("--tags=@e2e", "--tags=~@skip")
$runId = [guid]::NewGuid().ToString("N")
$outDir = "reports\allure-results\checkout-uat\$runId\initial-00"
New-Item $outDir -ItemType Directory -ErrorAction Stop | Out-Null

$LASTEXITCODE = $null
& $python -m behave "src\e2e\checkout" @tagArgs `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --summary --show-timings
$testExit = $LASTEXITCODE
if ($null -eq $testExit) { throw "Test process did not return an exit code" }
exit $testExit
```

Bash:

```bash
python="<approved-python-executable>"
command -v "$python" >/dev/null || { printf '%s\n' "Python executable unavailable" >&2; exit 1; }
export TARGET_ENV=uat
export suite=checkout
export HEADLESS=true
tag_args=("--tags=@e2e" "--tags=~@skip")
run_id="$(date -u +%Y%m%dT%H%M%SZ)-${RANDOM}"
run_dir="reports/allure-results/checkout-uat/${run_id}"
out_dir="${run_dir}/initial-00"
mkdir -p "$run_dir" || exit 1
mkdir "$out_dir" || exit 1

"$python" -m behave "src/e2e/checkout" "${tag_args[@]}" \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --summary --show-timings
test_exit=$?
exit "$test_exit"
```

Riferimenti: `src/e2e/checkout/environment.py`,
`src/conf/configuration.py`, `src/e2e/checkout/uat.yaml`.

## Report Allure

### Convenzioni output

In locale usare:

```text
reports/allure-results/<suite>-<env>/<run-id>/<attempt-id>
reports/junit/<suite>-<env>/<run-id>/<attempt-id>
```

Nel workflow NRT il runner produce `allure-results` nella working directory, poi il report
HTML viene pubblicato come artefatto e copiato su GitHub Pages.
Le convenzioni CI restano invariate; in locale non mescolare tentativi o cancellare
la directory condivisa per preparare una nuova esecuzione.

Riferimenti: regole operative di progetto, `.github/workflows/nrt-run-suite.yml`,
`.github/workflows/nrt-main-dispatch-tests.yml`.

### Aprire il report locale

Solo quando richiesto, aprire l'output di un tentativo preciso. PowerShell,
risolvendo dalla root del repository un percorso assoluto esistente:

```powershell
$results = (Resolve-Path -LiteralPath "reports\allure-results\cart-uat\<run-id>\initial-00" -ErrorAction Stop).Path
allure serve $results --port 5300
```

Bash:

```bash
allure serve "$PWD/reports/allure-results/cart-uat/<run-id>/initial-00" --port 5300
```

In alternativa, generare una directory HTML statica:

```bash
allure generate "reports/allure-results/cart-uat/<run-id>/initial-00" \
  -o "reports/allure-html/cart-uat/<run-id>/initial-00"
allure open "reports/allure-html/cart-uat/<run-id>/initial-00" --port 5300
```

Nota sul formatter Behave: `-o` si associa al primo formatter indicato. Mettere sempre
`allure_behave.formatter:AllureFormatter` prima di `-f progress`.

Riferimenti: regole operative di progetto, workflow NRT, cartelle `reports/`.

### Dashboard pubblicata

La dashboard GitHub Pages espone:

- una landing page da `.github/html/index.html`;
- storico WISP sotto `wisp-tests/`;
- storico FdR3 sotto `fdr3-tests/`;
- `last-history` per l'ultimo report processato dagli script di pubblicazione;
- statistiche lette da `widgets/summary.json` e `stats.json`.

Riferimenti: `.github/html/index.html`, `.github/scripts/process_reports.py`,
`.github/scripts/notify_slack.py`, `.github/templates/history-index-template.html`,
`.github/workflows/deploy-test-report.yml`.

### Pagina report su Confluence

Lo script `.github/scripts/create_report_page.py` legge i report disponibili
sotto `artifacts/` e crea pagine Confluence per le suite riconosciute.

La logica e orientata al reporting operativo:

- legge `widgets/summary.json` per recuperare data, durata e numero di failure;
- estrae i test falliti dai file case in `data/test-cases/`;
- compone la pagina usando template HTML sotto `.github/page_components/test_report_page/`;
- pubblica la pagina nella cartella Confluence configurata in `.github/dev.yaml` o `.github/uat.yaml`.

L'input `--run-type` (es. `NIGHTLY`, `NO-PROMO`) viene usato per valorizzare il contesto
della run nella pagina.

Esecuzione locale (con report compatibili in `artifacts/`): il comando crea
pagine Confluence, quindi va eseguito solo se la pubblicazione è autorizzata.

```bash
python .github/scripts/create_report_page.py --run-type NO-PROMO
```

Prerequisiti minimi:

- variabili d'ambiente `CONFLUENCE_KEY` e `CONFLUENCE_EMAIL` valorizzate;
- `.github/<TARGET_ENV>.yaml` con i metadati Confluence della suite.


Riferimenti: `.github/scripts/create_report_page.py`, `.github/workflows/create_report_page.yml`,
`.github/page_components/test_report_page/`, `src/utility/confluence_utils.py`.

## FDR api test

### Scope

La suite FDR api test verifica la conformità delle API REST di FdR (Flussi di Rendicontazione)
rispetto alle specifiche OpenAPI dichiarate. Diversamente dalle suite Behave, non richiede la
scrittura manuale di scenari: Schemathesis genera automaticamente i casi di test a partire dagli
schemi OpenAPI e valida ogni risposta contro i codici di stato e i modelli dichiarati nel
contratto.

Le API testate comprendono due profili:

| Profilo | File OpenAPI | Subscription key richiesta |
|---|---|---|
| `fdr_organization` | `fdr_organization.json` | `tas-fdr3-orgs-subscription-key` |
| `fdr_psp` | `fdr_psp.json` | `tas-fdr3-psp-subscription-key` |

Entrambi i profili vengono testati contro gli ambienti `dev` e `uat`.

### Script coinvolti

**`scripts/fetch_github_files.py`**

Scarica i file OpenAPI JSON dall'apposito repository GitHub usando un Personal Access Token
(PAT) letto dalla configurazione dei secret (`gh_token`). Il branch sorgente viene risolto
in base all'ambiente: `DEV` usa l'ultimo branch `SANPx.y.z`, `UAT` usa `develop`.
I file vengono salvati nella cartella temporanea `tmp_fetched/`.

**`scripts/schemathesis_runner.py`**

Scopre tutti i file `.json` in `tmp_fetched/`, risolve l'API key corrispondente dai secret
(la chiave del secret deve coincidere con lo stem del file, ad es. `fdr_organization`),
e lancia il comando `schemathesis run` per ciascun file. I risultati JUnit
vengono scritti in `junit/`; i risultati Allure sono abilitati da
`schemathesis.toml` e scritti in `allure-results/`.

**`.github/scripts/openApi_test.py`**

Orchestratore che esegue in sequenza: fetch dei file OpenAPI, esecuzione dei test Schemathesis,
rimozione della cartella temporanea `tmp_fetched/` e pulizia dei run più vecchi di 30 giorni.

### Esecuzione locale

Prerequisiti:

- Variabili d'ambiente `TARGET_ENV` (valori: `dev`, `uat`) e `suite` impostata a `fdr`.
- Configurazione `scripts/<TARGET_ENV>.yaml` con i placeholder del token GitHub e delle subscription key.
- Resolver dei segreti configurato, ad esempio `config/.secrets.yaml` compilato per l'ambiente scelto.

Il comando effettua richieste verso i servizi e rimuove `tmp_fetched/` al termine;
inoltre elimina le run scadute sotto `schemathesis-test-reports/`. Eseguirlo solo
con autorizzazione per l'ambiente e gli effetti previsti.

PowerShell:

```powershell
$env:TARGET_ENV = "dev"
$env:suite = "fdr"

python -u .github/scripts/openApi_test.py
```

Bash:

```bash
export TARGET_ENV=dev
export suite=fdr

python -u .github/scripts/openApi_test.py
```

Per aprire i risultati Allure prodotti localmente:

```bash
allure serve allure-results
```

Per eseguire solo uno specifico profilo OpenAPI senza l'orchestratore, il file
corrispondente deve essere già presente in `tmp_fetched/`:

```bash
export TARGET_ENV=dev
export suite=fdr
python scripts/schemathesis_runner.py fdr_organization
```

### Esecuzione tramite GitHub Actions

Il workflow riusabile `.github/workflows/openapi-fdr-tests.yml` viene invocato da
`.github/workflows/openapi-test-dispatch.yml`, avviabile manualmente.

**Flusso del job `fetch_and_test_openapi`:**

Il workflow usa una strategy matrix con `env: [dev, uat]`, quindi viene eseguito in parallelo
per entrambi gli ambienti. Per ogni ambiente:

1. Carica i secret da `FDR_INTEGRATION_TESTS_SECRETS`.
2. Esegue `openApi_test.py` con `TARGET_ENV` e `suite=fdr` impostati.
3. Costruisce il report con Allure CLI.
4. Carica l'artefatto `allure-report-openapi-<env>` (es. `allure-report-openapi-dev`).

Il job `deploy` in `openapi-test-dispatch.yml` scarica successivamente gli artefatti e pubblica
i report su GitHub Pages sotto `openapi-fdr-tests/`.

Riferimenti: `.github/workflows/openapi-fdr-tests.yml`, `.github/workflows/openapi-test-dispatch.yml`,
`scripts/fetch_github_files.py`, `scripts/schemathesis_runner.py`,
`.github/scripts/openApi_test.py`, `scripts/dev.yaml`, `scripts/uat.yaml`, `schemathesis.toml`.

## Esecuzione in CI

### Pull request

Il workflow `Check PR` gira sulle pull request verso `main` e applica automazioni di processo:

- assegna la PR all'autore;
- calcola la dimensione della PR;
- applica `size/small` sotto 200 righe modificate;
- applica `size/large` sopra 400 righe modificate;
- ignora nel conteggio alcuni file OpenAPI.

Riferimenti: `.github/workflows/check_pr.yml`, `.github/auto_assign.yml`.

### Suite NRT

Il workflow riusabile `nrt-run-suite.yml` installa Python, Java 17 e le
dipendenze, prepara i segreti dell'environment ed esegue Behave con percorso
e tag ricevuti dal catalogo. Per Checkout installa anche il browser richiesto.

Riferimenti: `.github/workflows/nrt-run-suite.yml`, `.github/nrt-suites.json`.

### Dispatch e pubblicazione report

- `nrt-main-dispatch-tests.yml` avvia ogni giorno alle `06:17 UTC` le suite registrate
  per UAT; consente anche l'avvio manuale per ambiente e selezione delle suite. Pubblica
  i report Allure e coordina ingestion, report Confluence e notifica Slack.
- `openapi-test-dispatch.yml` avvia manualmente i test OpenAPI FdR e richiama
  `deploy-test-report.yml` per processare e pubblicare i report.
- `create_report_page.yml` crea le pagine di riepilogo su Confluence dai report disponibili.
- `extract_allure_fail_rate.yml` legge `widgets/summary.json` da `gh-pages`, calcola fail
  rate e success rate, poi passa i dati al workflow di notifica.


### Manifest Gherkin

Il workflow `gherkin-manifest-sync.yml` mantiene `.github/gherkin-manifest.yml`,
destinato a QA Central Hub (Knowledge Base > Gherkin Feature Files).

- Trigger: una PR chiusa e unita su `main`, oppure l'avvio manuale
  (`workflow_dispatch`). La sincronizzazione parte se il manifest manca o se
  la PR modifica un `.feature` sotto `src/`, il manifest, il catalogo
  `.github/nrt-suites.json`, lo script di generazione o il workflow stesso. Il merge della PR
  generata dalla sincronizzazione non avvia un nuovo ciclo. Le esecuzioni sono
  serializzate: GitHub ne accoda fino a 100; quelle annullate per coda piena
  vanno rieseguite.
- Pubblicazione: il workflow propone il manifest in una PR cumulativa verso
  `main`, con etichetta `skip`; non scrive direttamente su `main`. Se esiste
  una PR di sincronizzazione aperta, aggiorna il suo branch dopo avervi
  integrato `main` senza force-push. Se non ci sono differenze, non apre una PR.
  La PR va revisionata e unita normalmente. Il repository deve consentire
  alle Actions di creare PR; il job usa i permessi `contents: write` e
  `pull-requests: write`.
- Manifest: `.github/scripts/gherkin_manifest_sync.py` lo rigenera dall'albero
  `src/<tipo>/<suite>/features/`, dove `<tipo>` è `api`, `integration` o
  `e2e`; sono ammesse sottocartelle sotto `features/`. L'ID deriva dall'header
  `# qa-hub:` alla prima riga quando presente; per le feature non ancora
  migrate usa il primo tag identificativo con progressivo a tre cifre oppure
  il nome del file. Lo script conserva le etichette delle suite, rimuove le
  voci dei file non più presenti, valida il risultato e lo scrive solo se
  cambia. Il controllo delle convenzioni rifiuta i `.feature` modificati
  fuori dal percorso canonico. Stato e stime appartengono a QA Central Hub e
  non sono campi del manifest.
- Metadati delle suite: `test_type` e `nrt` sono sempre presenti e ricalcolati
  a ogni rigenerazione. `test_type` deriva dal percorso `src/<tipo>/<suite>`:
  `api`, `integration` o `e2e`; le suite chiamate `tas` o con prefisso `tas_`
  hanno invece valore `tas`. `nrt` è un booleano YAML: `true` se il percorso
  della suite è censito come `behave_path` nel catalogo NRT, `false` altrimenti,
  indipendentemente dall'ID o dall'eseguibilità nel singolo ambiente.
  Per le voci manuali si usa la suite canonica che contiene i file; se non è
  identificabile o i file appartengono a suite diverse, la generazione si ferma.
  Anche un catalogo mancante, illeggibile o con dati di appartenenza invalidi
  ferma la generazione senza sovrascrivere il manifest. I manifest precedenti
  senza questi campi vengono aggiornati automaticamente.
- Correzioni: nel manifest si può cambiare `label` di una suite. L'ID non va
  modificato direttamente nel manifest: deriva dall'header QA Hub quando
  presente, altrimenti dal tag identificativo legacy o dal nome del file.
  Header e tag identificativi si aggiornano solo con la migrazione approvata
  per l'ambito, preservando i vecchi tag degli scenari come alias. Una
  modifica manuale al manifest sul branch cumulativo richiede revisione e
  merge della PR prima di rigenerare. Non modificare manualmente `test_type`
  o `nrt`: la sincronizzazione ripristina i valori derivati dalle fonti.
- Protezioni: se `main` avanza durante la generazione, se il branch riceve un
  push concorrente o se ci sono conflitti, il workflow si ferma senza
  sovrascrivere il branch remoto. Una PR cumulativa che contiene modifiche a
  file diversi dal manifest richiede revisione prima di riprendere.
- Esecuzione locale: `python .github/scripts/gherkin_manifest_sync.py --dry-run`
  mostra il riepilogo senza scrivere; `--check` esce con codice 1 se il
  manifest non è allineato.

Il workflow `syncFeatureFile.yaml`, che aggiornava le pagine Confluence dai
feature file, è stato rimosso; la relativa documentazione resta come riferimento
storico.

Riferimenti: `.github/workflows/gherkin-manifest-sync.yml`,
`.github/scripts/gherkin_manifest_sync.py`, `.github/scripts/gherkin-sync-pr.js`,
`.github/nrt-suites.json`.

### Documentazione GitHub Pages

Il workflow che generava e pubblicava automaticamente le pagine degli scenari è stato
rimosso. Lo script `scenario_parser.py` resta disponibile per la generazione locale:
vedere [Documentazione scenari](#documentazione-scenari).

## Servizio di test riusabile

Il workflow `test-automation-service.yml` espone una modalita riusabile tramite
`workflow_call` o `workflow_dispatch`.

Input:

| Input | Valori | Descrizione |
|---|---|---|
| `test_type` | `integration`, `e2e`, `api` | categoria di test (default `integration`, mappa su `src/<test_type>/<suite>`) |
| `test_suite` | `wisp`, `all` | suite da eseguire |
| `environment` | `dev`, `uat` | ambiente target |
| `caller_id` | stringa libera | sistema chiamante |
| `correlation_id` | stringa libera | identificativo per tracciare la run |
| `isQualityGateRun` | booleano opzionale | default `false`: origine `TAS`; `true`: origine `QG` |

Output:

| Output | Descrizione |
|---|---|
| `passed` | scenari passati |
| `failed` | scenari falliti |
| `skipped` | scenari saltati |
| `total` | totale scenari |
| `duration` | durata in secondi |
| `outcome` | `success` o `failure` |

Il workflow carica i segreti dall'environment `integration-tests`, produce `behave-results.json`,
`test-summary.json`, `junit/`, pubblica l'artefatto `test-results` e fallisce il job quando
uno o piu scenari falliscono.

Le run ordinarie pubblicano report e analisi AI sotto `TAS/<suite>/<timestamp>/` su
`gh-pages`; con `isQualityGateRun: true` usano
`QG/<suite>/<timestamp>/`, con lo stesso formato UTC.
`QG/index.html` elenca le suite, ciascuna con il proprio storico; le vecchie run
direttamente sotto `QG/<timestamp>/` restano accessibili senza essere spostate.
Origine e flag sono inclusi nei log, nel job
summary, in `test-summary.json` e nei metadati Allure. L'ingestion salva
`test_origin: QG` e URL Allure sotto `QG/<suite>/` per le run Quality Gate.
Il flag non modifica selezione dei test o criteri di successo.

Riferimenti: `.github/workflows/test-automation-service.yml`, `docs/tas/tas-developer-guide.md`,
`scripts/tas_orchestrator.py`.

### Bridge CLI

Il bridge Python permette di avviare il workflow riusabile via API GitHub.

Variabile obbligatoria:

```bash
export GITHUB_TOKEN=<token-con-permessi-actions>
```

Esecuzione asincrona:

```bash
python scripts/tas_orchestrator.py \
  --suite wisp \
  --env uat \
  --caller-id my-service
```

Per selezionare una categoria diversa da `integration` aggiungere `--type {integration|e2e|api}`
(default: `integration`, mappa su `src/<type>/<suite>`).

Per classificare una run come Quality Gate aggiungere `--is-quality-gate-run`.
I wrapper GitHub Actions e Azure DevOps espongono lo stesso input
`isQualityGateRun`, opzionale con default `false`; vale in tutte le modalita.
Contratto ed esempi: [guida TAS](docs/tas/tas-developer-guide.md).

Esecuzione sincrona:

```bash
python scripts/tas_orchestrator.py \
  --type integration \
  --suite wisp \
  --env uat \
  --caller-id my-service \
  --correlation-id my-run-001 \
  --sync
```

Exit code:

| Codice | Significato |
|---|---|
| `0` | test passati, oppure dispatch inviato in asincrono |
| `1` | uno o piu scenari falliti |
| `2` | errore di orchestrazione, configurazione, timeout o API |

Riferimenti: `scripts/tas_orchestrator.py`, `docs/tas/tas-developer-guide.md`.

## Ingestione dati test

Il flusso di *test data ingestion* raccoglie i risultati delle esecuzioni dei test per popolare il database del QA Hub e realizzare dashboard e metriche operative. Questa sezione descrive il comportamento operativo e la logica usata all'interno del flusso.

### Logica riassunta

- Il workflow `nrt-main-dispatch-tests.yml` esegue le suite programmate e pubblica un artefatto Allure per suite.
- Il workflow riusabile `test-automation-service.yml` pubblica, al termine di una run, l'artefatto `test-results` contenente i risultati dei test quando presenti.
- Entrambi i flussi richiamano `test-data-ingestion.yml`: NRT usa `artifact_pattern: allure-report-*`, mentre TAS usa `artifact_name: test-results`. Il default di `artifact_name` è `tmp_processed_reports`.
- Lo step di ingestion estrae JSON/JUnit/Allure dall'artefatto scaricato e popola le tabelle tramite lo script `.github/scripts/populate_tables.py`.
- La versione del test object associata alla suite non viene letta dal servizio live: `populate_tables.py` la richiede al QA Hub (`GET /api/v1/releases/versions`), che la mantiene aggiornata nella tabella `sp_version_state` della status page. La chiave di ricerca e la coppia ambiente + `product_key`, dove `product_key` e il campo omonimo della suite in [`.github/nrt-suites.json`](.github/nrt-suites.json) (es. `fdrfase3` per `fdr3`) e deve corrispondere alla chiave dell'applicazione censita nella status page. Se la versione non e disponibile (suite senza `product_key`, applicazione non censita, QA Hub non raggiungibile) lo script non usa piu una versione di default: riusa l'ultima suite salvata per quel test object, oppure crea una suite con versione `unknown` se non ne esiste nessuna, e segnala un warning nel log. La suite viene cercata per versione esatta, quindi anche un rollback dell'applicazione genera la propria suite.

### File di configurazione ambiente per le suite

- Ogni suite può includere file `dev.yaml` e `uat.yaml` sotto `src/<test_type>/<suite>/` (es. `src/integration/wisp/dev.yaml`).
- Questi file contengono metadati e mappe logiche (ad es. nomi delle API, nomi di secret come `NODO_SUBSCRIPTION_KEY`) che vengono poi risolti con `config/.secrets.yaml` o tramite Key Vault/APIM resolver.

### Esempio d'uso pratico

1. `nrt-main-dispatch-tests.yml` carica i report delle suite nightly come artefatti `allure-report-*`.
2. `nrt-main-dispatch-tests.yml` invoca `test-data-ingestion.yml` con `artifact_pattern: allure-report-*`.
3. `test-automation-service.yml` esegue una run on-demand e, alla fine, carica `test-results` invocando `test-data-ingestion.yml` con `artifact_name: test-results`.

Riferimenti: `.github/workflows/test-data-ingestion.yml`, `.github/workflows/nrt-main-dispatch-tests.yml`, `.github/workflows/test-automation-service.yml`.


## Documentazione scenari

La documentazione statica delle feature viene generata da `scenario_parser.py` leggendo
`src/integration`. Lo script:

- scansiona i file `.feature` sotto ogni componente di integrazione;
- esclude di default i tag `skip` e `need_fix`;
- scrive pagine Markdown sotto `docs/components`;
- genera `docs/index.md`, `docs/all_scenarios.txt` e `mkdocs.yml`;
- aggiunge link verso i report Allure del componente.

Generazione locale:

```bash
python3 scenario_parser.py \
  --repo-name pagopa-platform-integration-test \
  --page-name "PagoPA platform integration test"
mkdocs build
```

Il workflow di pubblicazione automatica delle pagine degli scenari è stato rimosso;
questi comandi non pubblicano il risultato.

Riferimenti: `scenario_parser.py`.

## Contribuire

Indici degli asset AI: [agenti](.github/agents/README.md),
[skill](.github/skills/README.md), [istruzioni](.github/instructions/README.md)
e [profili](.github/profiles/README.md), con scope, modalita d'uso ed esempi.

Per tradurre uno Use Case (UC) in feature, seguire il
[workflow UC](docs/use-cases/uc-workflow.md): esplicitare il focus funzionale,
riconciliare i percorsi documentati pertinenti e coprire flussi e criteri con
evidenze ammesse.

### Convenzioni Gherkin

- Usare un solo `Feature` per file.
- Salvare i file in `src/<api|integration|e2e>/<suite>/features/`; sono ammesse sottocartelle sotto `features/`.
- Per gli ambiti non ancora migrati da QA Central Hub, mantenere il sistema di identità e i tag già presenti; non anticipare l'aggiunta dell'header o la rinumerazione. La migrazione Hub scrive l'header `# qa-hub: FEAT_<NNN>_<Ambito>` e i nuovi tag per un ambito alla volta, preservando i vecchi tag come alias degli scenari.
- Dare al file un nome descrittivo.
- Mantenere gli step atomici e riusabili.
- Usare `Background` per precondizioni comuni.
- Conservare i tag esistenti.
- Aggiungere tag significativi, ad esempio `@smoke`, `@regression`, `@<suite>`.
- Scrivere nella lingua gia usata dalla suite.
- Tenere al massimo 12 scenari per feature file; se serve, dividere per area semantica.
- Usare la terza persona presente negli step.

Riferimenti: regole operative di progetto, feature file esistenti.

### Processo consigliato

1. Analizzare o creare prima i file `.feature`.
2. Implementare o aggiornare solo gli step necessari.
3. Riutilizzare helper, fixture e pattern gia presenti nella suite scelta come blueprint.
4. Eseguire la suite con Allure e JUnit quando disponibile.
5. Verificare che lo scope approvato sia stato realmente eseguito: exit code,
   conteggi, errori, esclusioni e artifact correnti; `0` falliti da solo non basta.
6. Se restano errori nella lavorazione di una suite, salvare o riusare in `reports/`
   il report Markdown del runner, in italiano, con scenari falliti, evidenze,
   causa probabile e azioni correttive. Nessun report autonomo di successo.
7. Non disabilitare scenari falliti per far passare la suite.

Riferimenti: regole operative di progetto, `reports/`, suite esistenti.

L'orchestratore separa il [routing di sessione e branch](docs/workflows/qa-orchestrator/session-routing.md)
dal [workflow operativo](docs/workflows/qa-orchestrator/operations.md): entra
dall'agente necessario e si ferma al risultato richiesto, senza imporre sempre
analista, esecuzione e closer. Le riprese conservano progressi e budget; vale
l'ultima autorizzazione esplicita applicabile, incluse revoche. Cambiamenti
rilevanti invalidano le evidenze dipendenti e le esecuzioni parallele richiedono
anche isolamento dei dati/risorse esterne. Esito QA e completamento ACE sono
distinti: un blocco del bookkeeping non autorizza a ripetere test o azioni Git.

Le [istruzioni Gherkin](.github/instructions/gherkin.instructions.md) e il
[profilo associato](.github/profiles/gherkin.profile.yaml) definiscono la fonte
autorevole e la forma degli identificativi e contano il limite di 12 sulle definizioni,
non sulle righe Examples espanse. Le celle Examples vuote significano null:
per i binding nuovi/modificati e obbligatoria la conversione esplicita a Python
`None`, poiche Behave fornisce testo vuoto. Non viene migrato automaticamente il
codice legacy. Gli outline si semplificano solo preservando copertura e selezione;
l'aggiunta ADR-48 richiede esiti osservabili supportati dalle fonti.

Il [workflow QA-engineer](docs/workflows/qa-engineer/implementation.md) distingue
review, implementazione e fix/refactor. L'ingegnere implementa binding e wiring
autorizzato della suite; i nuovi helper riusabili sono affidati allo specialista
utility, anche per API ed E2E. Gli agenti di implementazione non eseguono test:
restituiscono codice e verifiche statiche al runner, che esegue i comandi approvati.
Il parallelismo richiede file con ownership disgiunta, non solo feature diverse.
Le [istruzioni Python](.github/instructions/python-scripts.instructions.md)
definiscono docstring utili, tipi e compatibilita nello scope modificato.
Le aggiunte ADR-52, ADR-53 e ADR-54 richiedono errori espliciti, effetti/risorse
gestiti e verifiche proporzionate, senza introdurre nuovi tool o autorizzare
gli ingegneri a eseguire test. Nessun profilo YAML Python aggiuntivo e richiesto.

Le [istruzioni Behave](.github/instructions/behave-steps.instructions.md) e il
[profilo dei percorsi](.github/profiles/behave-steps.profile.yaml) precisano
organizzazione per responsabilita, compatibilita dei binding e lifecycle del
context, senza imporre frammentazione o migrazioni delle utility legacy.
Le aggiunte ADR-42 e ADR-43 coprono asserzioni complete, input strutturati,
attese finite e diagnostica sicura; non ampliano i permessi di esecuzione.

Il [workflow Python-utility-engineer](docs/workflows/python-utility-engineer/implementation.md)
copre review, implementazione e manutenzione delle utility condivise e di suite.
Richiede un contratto tecnico anche nell'uso diretto e verifica l'impatto sui
chiamanti, non solo le firme. Scrive unit test isolati senza eseguirli; migrazioni
di step/hook o modifiche fuori scope tornano al rispettivo owner. Non e un
partecipante ACE autonomo: restituisce lavoro e attriti al chiamante.

Il [workflow QA-runner](docs/workflows/qa-runner/execution.md) distingue esecuzione,
diagnosi e esecuzione con fix autorizzati. Dopo il primo fallimento (tentativo 0),
si puo andare direttamente al report oppure usare fino a **cinque tentativi bonus
di fix**, con piano approvato e artifact isolati. Non sono cinque esecuzioni totali:
il primo run non consuma il budget. Il runner distingue `passed`, `failed`,
`blocked` e `inconclusive`; non cancella la storia di errori intermittenti.
ADR-55--ADR-58 richiedono interprete/stato reale, selezione corrente, evidenze
effettivamente acquisite e provenienza della configurazione. Le aggiunte finali
ADR-59 e ADR-60 limitano il preflight e distinguono terminazione locale da
rollback remoto: dopo una mutazione interrotta verificare ripetibilita ed effetti
incerti prima di rilanciare, con osservazione/cleanup solo se autorizzati.

### Manutenzione README e chiusura QA

Dopo ogni insieme coerente di modifiche, usare
[`/ppa-readme`](.github/skills/ppa-readme/SKILL.md) per aggiornare le sezioni
coinvolte o motivare che non serve un aggiornamento. La valutazione si fa una
volta per lo scope corrente, prima dell'eventuale commit; non impone modifiche
cosmetiche o l'esecuzione dei comandi documentati.

Il [workflow QA-closer](docs/workflows/qa-closer/closure.md) usa le evidenze
del runner senza rieseguire test e mantiene separati scope e autorizzazioni
per commit, push e PR. I report di chiusura sono solo Markdown per errori
irrisolti nelle suite; non richiedono HTML o template Confluence. Questo limite
non modifica i report Allure e le pubblicazioni CI documentati nelle altre sezioni.

### Commit e PR

Usare uno dei prefissi seguenti nel messaggio di commit:

| Prefisso | Quando usarlo |
|---|---|
| `feat:` | nuovo scenario o nuova funzionalita di test |
| `fix:` | correzione di bug |
| `chore:` | manutenzione, dipendenze, tooling |
| `docs:` | modifiche solo documentali |
| `refactor:` | ristrutturazione senza cambio comportamento |
| `test:` | aggiunta o aggiornamento test |

La PR deve descrivere cambiamenti, motivazione, test eseguiti e tipo di modifica. Il workflow
di PR applica automaticamente label di dimensione in base alle righe modificate.

La skill [`/ppa-pr`](.github/skills/ppa-pr/SKILL.md) ricava la suite lavorata dal
diff e da [`.github/nrt-suites.json`](.github/nrt-suites.json): la label GitHub e
il campo `id`, non il nome descrittivo `label`, coerentemente con la CI.
Per una suite richiede il suo `id` e un solo incremento (`patch`, `minor` o `major`);
senza suite usa `skip`, senza incremento ne label di suite. Scope ambiguo,
multi-suite o suite non censita richiedono risoluzione, non un `skip` di ripiego.

Riferimenti: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/check_pr.yml`, regole operative di progetto.

## Release e versionamento

A ogni push su `main`, incluso il merge di una PR, il workflow `Release` crea automaticamente
un tag e una GitHub Release seguendo il [Semantic Versioning](https://semver.org/)
(`vMAJOR.MINOR.PATCH`).

Il workflow usa due action:

- `mathieudutour/github-tag-action` calcola la nuova versione a partire dai messaggi di commit
  ([Conventional Commits](https://www.conventionalcommits.org/)) e pubblica il tag;
- `ncipollo/release-action` crea la GitHub Release con note generate automaticamente, raggruppate
  secondo le categorie definite in `.github/release.yml`.

Non servono file di versione nel repository: la versione corrente e sempre l'ultimo tag SemVer
con prefisso `v`. I tag non SemVer esistenti (es. `WISP_v1.0`, `CHECKOUT_v1.0`) vengono ignorati.
La base di partenza e `1.0.0` (`initial_version`).

### Versioni delle suite di test

Le versioni delle singole suite sono indipendenti dal tag di release del repository e sono
registrate nel [catalogo NRT](.github/nrt-suites.json). Il loro aggiornamento e guidato dalle
**label della PR**, con una policy condivisa tra il check `Verify labels` e il workflow
`Bump test suite version`:

- Per versionare una suite, assegnare una label di incremento (`major`, `minor` o `patch`) e
  una sola label corrispondente a un ID del catalogo: attualmente `wisp`, `checkout` o `fdr3`.
  Il confronto non distingue maiuscole e minuscole.
- Usare `skip` per documentazione, configurazioni, tooling/AI o altre modifiche che non devono
  incrementare una versione di suite. **`skip` ha precedenza su tutte le altre label**:
  il check passa anche insieme a `major`, `minor`, `patch` o piu label di suite, senza bump.
- Le PR create da `dependabot[bot]` e `renovate[bot]` sono automaticamente esentate dal
  versionamento delle suite. Le loro label di incremento descrivono le dipendenze e possono
  rimanere sulla PR: non serve aggiungere `skip` o rimuovere `major`. L'esenzione usa l'autore
  della PR, non chi applica una label; non si estende ad altri bot o alla sola label `dependencies`.
- Senza `skip` o l'esenzione per i due bot, restano obbligatori incremento e singola suite.
  Gli errori sono riportati nel check, senza aggiungere commenti ripetuti alla PR.

Entrambi i workflow leggono le label correnti tramite API, non una copia potenzialmente
obsoleta nell'evento. Quando la PR viene mergiata, solo una combinazione valida di incremento
e suite avvia lo script di aggiornamento; il workflow crea quindi un commit del catalogo
aggiornato su `main`. Con `skip` o una PR dei due bot non viene modificata alcuna versione di
suite. Gli altri check e il versionamento della release del repository non sono esentati:
quest'ultimo dipende dai messaggi di commit, non dalle label.

La policy e implementata in [suite-version-labels.js](.github/scripts/suite-version-labels.js).
I test locali non richiedono dipendenze npm ne accesso a servizi esterni:

```powershell
node --test .github\scripts\suite-version-labels.test.js
```

Gli stessi test vengono eseguiti nel job `Verify labels` sulle PR.

### Regole di incremento

| Commit | Incremento | Esempio |
|---|---|---|
| `fix:`, `perf:` | patch | `v1.2.3` -> `v1.2.4` |
| `feat:` | minor | `v1.2.3` -> `v1.3.0` |
| `feat!:`, `fix!:` o footer `BREAKING CHANGE:` | major | `v1.2.3` -> `v2.0.0` |
| solo altri prefissi (`chore:`, `docs:`, `refactor:`, `test:`) o messaggi non convenzionali | patch (default) | `v1.2.3` -> `v1.2.4` |

Per non generare alcuna release, inserire `[no-release]` o `[skip-release]` nel messaggio di commit.

### Incremento unico per push

L'action analizza **tutti** i commit arrivati su `main` dall'ultimo tag, ma applica **un solo
incremento: quello di livello piu alto trovato**. Il numero di commit non conta, conta solo il
tipo piu "forte".

| Commit inclusi nel merge | Risultato |
|---|---|
| 10 `fix:` | `v1.2.3` -> `v1.2.4` |
| 8 `fix:` + 2 `feat:` | `v1.2.3` -> `v1.3.0` |
| 9 `feat:` + 1 `feat!:` | `v1.2.3` -> `v2.0.0` |

Quindi una PR con molti commit `feat:`/`fix:` produce comunque una sola release. Con il merge commit (strategia attuale) i singoli commit della PR restano nella storia di `main` e vengono letti correttamente; il commit `Merge pull request #...` non e convenzionale e viene ignorato.
In caso di squash merge, invece, il titolo della PR diventa l'unico commit analizzato e deve
quindi rispettare il formato convenzionale (es. `feat(PQ-123): descrizione`).

Attenzione: un solo `!` o `BREAKING CHANGE:` in un qualsiasi commit della PR porta a un
incremento major.

Riferimenti: `.github/workflows/release.yml`, `.github/release.yml`.

## Troubleshooting

| Problema | Causa probabile | Azione |
|---|---|---|
| `No steps directory` con `behave src/api` | Behave richiede una suite con `features/` e `steps/` | eseguire `behave src/api/<suite>` |
| `File di configurazione non trovato` nelle suite API | file per `TARGET_ENV` assente | verificare `src/api/config/.env.<env>` |
| Allure scrive errore su directory output | `-o` associato al formatter sbagliato | mettere AllureFormatter prima di `-f progress` |
| Report non trovato su Windows | path relativo risolto da cwd diverso | usare path assoluto con `allure serve` |
| Errori certificato nelle API suite | trust store locale non configurato | usare store OS o `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` |
| Segreti mancanti in integrazione | `config/.secrets.yaml` assente o incompleto | copiarlo dal template e compilare i valori reali |
| Browser Playwright non trovato | browser runtime non installato | eseguire `playwright install` o `npx playwright install` |
| Workflow riusabile non trova la suite | categoria o nome suite non corrispondono al percorso | verificare `src/<test_type>/<suite>` |

Riferimenti: `src/api/utility/http_client.py`, `src/api/utility/api_test_environment.py`,
`config/.secrets_template.yaml`, workflow CI, regole operative di progetto.

## Tracciabilita delle fonti

| Area documentata | Fonti |
|---|---|
| Dipendenze e setup Python | `requirements.txt`, workflow di setup Python |
| Configurazione API | `src/api/config/.env.dev`, `src/api/config/.env.uat`, `src/api/utility/api_test_environment.py` |
| Configurazione integrazione | `src/integration/<suite>/<env>.yaml`, `src/integration/commondata.yaml`, `config/.secrets_template.yaml`, `src/conf/configuration.py` |
| Comandi API Behave | suite `src/api/*`, feature file, hook `environment.py` |
| Comandi WISP/FdR3 | `.github/workflows/nrt-run-suite.yml`, `.github/nrt-suites.json` |
| Report Allure e dashboard | `.github/scripts/process_reports.py`, `.github/scripts/notify_slack.py`, `.github/scripts/create_report_page.py`, `.github/html/index.html`, `.github/templates/history-index-template.html`, `.github/workflows/create_report_page.yml` |
| CI e workflow riusabile | `.github/workflows/*.yml`, `scripts/tas_orchestrator.py`, `docs/tas/tas-developer-guide.md` |
| Manifest Gherkin | `.github/workflows/gherkin-manifest-sync.yml`, `.github/scripts/gherkin_manifest_sync.py`, `.github/scripts/gherkin-sync-pr.js`, `.github/nrt-suites.json` |
| Documentazione scenari | `scenario_parser.py` |
| Convenzioni di contributo | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/check_pr.yml`, regole operative di progetto |
