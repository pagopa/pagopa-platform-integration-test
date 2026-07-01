# pagopa-platform-integration-test

Repository di test di integrazione, API ed end-to-end per componenti della piattaforma pagoPA.
Le suite sono scritte principalmente in Python con Behave/Gherkin e producono report Allure;
alcune suite storiche usano Cucumber.js o Playwright.

## Indice

- [Panoramica](#panoramica)
- [Struttura del repository](#struttura-del-repository)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Suite disponibili](#suite-disponibili)
- [Esecuzione locale](#esecuzione-locale)
- [Report Allure](#report-allure)
- [Esecuzione in CI](#esecuzione-in-ci)
- [Servizio di test riusabile](#servizio-di-test-riusabile)
- [Documentazione scenari](#documentazione-scenari)
- [Contribuire](#contribuire)
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
├── config.yaml                      # servizi DEV/UAT per suite di integrazione
├── commondata.yaml                  # dati condivisi per test di integrazione
├── config/
│   ├── .secrets_template.yaml       # template segreti per suite di integrazione
│   └── api-tests/
│       ├── .env.dev                 # variabili API test DEV
│       └── .env.uat                 # variabili API test UAT
├── scripts/
│   └── tas_orchestrator.py          # bridge CLI per avviare workflow di test
├── src/
│   ├── api/                         # suite API Behave
│   │   ├── auth-service/
│   │   ├── cart/
│   │   ├── checkout-npg/
│   │   └── ecommerce-cdc/
│   ├── integration/                 # suite integrazione Behave/Cucumber
│   │   ├── wisp/
│   │   ├── fdr/
│   │   ├── ebollo/
│   │   └── gpd/
│   └── e2e/
│       └── checkout/                # Checkout E2E Behave/Playwright
├── reports/                         # output locali (allure-results/allure-html)
└── .github/
  ├── workflows/                   # workflow GitHub Actions
  ├── scripts/                     # script di pubblicazione report
  ├── templates/                   # template HTML storico report
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
| Node.js + npm/yarn | GPD Cucumber.js e Playwright JS | 18+ consigliata |
| jq | parsing JSON nei workflow Linux | richiesto in CI WISP/FdR |

Dipendenze Python principali presenti nel progetto:

- `behave==1.2.6`
- `allure-behave==2.13.5`
- `allure-python-commons==2.13.5`
- `python-dotenv>=1.0.0`
- `requests==2.32.4`
- `dynaconf==3.2.13`
- `jinja2`
- `markdown==3.8.1`

Riferimenti: `requirements.txt`, `.github/workflows/wisp-tests.yml`,
`.github/workflows/fdr-tests.yml`, `.github/workflows/deploy-test-report.yml`.

## Installazione

Da PowerShell o Bash, entrare nella root del repository e installare le dipendenze Python:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Per le suite Node.js opzionali:

```bash
cd src/integration/gpd
yarn install
```

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

Riferimenti: `requirements.txt`, `src/integration/gpd/package.json`,
`src/integration/gpd/README.md`, `src/e2e/checkout/package.json`,
`src/e2e/checkout/environment.py`, `src/integration/ebollo/environment.py`.

## Configurazione

### API test

Le suite in `src/api/<suite>/` caricano automaticamente il file:

```text
config/api-tests/.env.<env>
```

L'ambiente si seleziona con `-D env=dev` o `-D env=uat`. Se il parametro non viene passato,
gli hook comuni leggono `TARGET_ENV`; in assenza anche di questa variabile, usano `dev`.

Variabili comuni:

| Variabile | Descrizione |
|---|---|
| `CHECKOUT_HOST` | host API Checkout per DEV/UAT |
| `NOTICE_CODE_PREFIX` | prefisso per generare notice code casuali |
| `VALID_FISCAL_CODE_PA` | codice fiscale EC valido |
| `USE_BETA_BACKEND_HEADER` | header di routing blue/green globale |
| `DEPLOYMENT_*` | routing specifico per payment-methods, payment-requests, transactions |
| `NPG_*` | host e dati carta test NPG |

Riferimenti: `config/api-tests/.env.dev`, `config/api-tests/.env.uat`,
`src/api/utility/api_test_environment.py`.

### Integration test

Le suite sotto `src/integration/` usano `config.yaml`, `commondata.yaml` e, quando necessario,
`config/.secrets.yaml`. Se `TARGET_ENV` non e impostata, la configurazione Python seleziona
`uat` come default.

Preparare i segreti locali partendo dal template:

```bash
cp config/.secrets_template.yaml -> config/.secrets.yaml
```

Il file `config/.secrets.yaml` è ignorato da git e deve contenere le subscription key e le
password richieste dalle chiamate verso Nodo, GPD, Technical Support e canali WISP/Checkout.

PowerShell:

```powershell
$env:TARGET_ENV = "uat"
```

Bash:

```bash
export TARGET_ENV=uat
```

Riferimenti: `config.yaml`, `config/.secrets_template.yaml`,
`src/conf/configuration.py`, `.gitignore`.

### E2E test

Le suite Behave sotto `src/e2e/` caricano ognuna un file env locale tramite variabile `ENV_FILE`.
Es. `dev.env` in checkout.

PowerShell:

```powershell
$env:ENV_FILE = "dev.env"
$env:HEADLESS = "true"
$env:E2E_TIMEOUT_MS = "80000"
```

Bash:

```bash
export ENV_FILE=dev.env
export HEADLESS=true
export E2E_TIMEOUT_MS=80000
```

Riferimenti: `src/e2e/checkout/environment.py`, `src/e2e/checkout/dev.env`.

### Gestione dei secret

L'applicazione fa uso di svariati secret per eseguire correttamente le suite di test.
I secret utilizzati dall'applicazione possono essere:
- risolti da un file di secret (per il testing in locale);
- risolti dal key vault Azure relativo all'ambiente di test (dev, uat).

Inoltre, è presente l'`ApimSubscriptionResolver`, utilizzato per risolvere le subscription key dei servizi, leggendole dal servizio APIM di Azure relativo all'ambiente di test (dev,uat), al momento però **non è impiegato**.


#### Requisiti comuni
Per entrambe le casistiche, è necessario che nel workspace sia presente:
- un file specifico per la singola suite, denominato "{suite}_config.json" (es. wisp_config.json), contenente sia i secrets della suite che le sue configurazioni (es. url di un servizio, timeout, ecc...)

L'applicazione risolverà poi i secret presenti nel file e li assegnerà nell'attributo secret presente nell'oggetto context, per accedere al secret bisognerà richiamarlo utilizzando il nome ad esso associato nel file in cui è presente. es. `context.secret.NOME_SECRET` 

È necessario che il file sia inserito manualmente nel workspace, sotto la cartelle `./config/suites_config/`.


Il formato dei secret da risolvere all'interno dei file JSON **DEVE** essere il seguente:
` "NOME_NON_VINCOLANTE" : "$NOME_SECRET_VINCOLANTE" `.

Il nome dell'attributo JSON non è vincolante in quanto rappresenta solo il nome che utilizzeremo all'interno del codice per accedere al secret, il valore dell'attributo invece è vincolante in quanto sarà utilizzato per individuare il secret da cui leggere il valore, che sarà poi settato come valore per quell'attributo.


```
FLUSSO D'ESEMPIO:
- Ho un attributo "API_KEY_TEST" : "$API_KEY_WISP"
- Il resolver cerca un secret denominato API_KEY_WISP
- Lo trova e lo sostituisce a "$API_KEY_WISP" nel file JSON 
- "API_KEY_TEST" : "XXXXXXXXX"
- Accedo all'attributo nel codice con "context.secret.API_KEY_TEST"
```
Tutti i placeholder all'interno dei JSON **devono** essere suddivisi per ambiente, inserendoli dentro un oggetto avente come nome la denominazione dell'ambiente di riferimento, così che l'applicazione possa risolvere i secret corretti per l'ambiente d'esecuzione.
Esempio:
```
{
  "uat":{
    "EXAMPLE_SECRET": "$EXAMPLE_SECRET",
    "EXAMPLE_CONFIG": "CONFIG"
  },
  "dev":{
    "EXAMPLE_SECRET": "$EXAMPLE_SECRET",
    "EXAMPLE_CONFIG": "CONFIG"
  }
}
```

L'applicazione ha bisogno che siano settate le seguenti variabili d'ambiente:
-  `suite` -> Utilizzata per individuare il file di placeholders specifico per la suite;
- `TARGET_ENV` -> Utilizzata per indicare l'env da cui leggere i placeholders, sia per i secret   comuni che per quelli specifici per la suite;

#### Risoluzione secret in locale
Per la risoluzione locale dei secret è necessario che sia presente un file `secrets.yaml` sotto `./config/`, affinchè il sistema possa utilizzarlo per risolvere i secret presenti nel file di config.

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
| `fdr` | `src/integration/fdr` | Behave | smoke/example suite con tag `@runnable` |
| `ebollo` | `src/integration/ebollo` | Behave + Playwright Python | scenari eBollo e broadcast station |
| `gpd` | `src/integration/gpd` | Cucumber.js | suite Node.js con script `yarn test:<env>` |

Report locali consigliati: `reports/allure-results/<suite>-<env>` per le suite Behave.
La suite GPD usa la reportistica Cucumber configurata dal runner JS.

Riferimenti: `src/integration/**/features/**/*.feature`,
`src/integration/gpd/package.json`, `src/integration/gpd/README.md`.

### End-to-end

| Suite | Percorso | Runner | Note |
|---|---|---|---|
| `checkout` | `src/e2e/checkout` | Behave + Playwright Python | feature UI Checkout sotto `features/` |

Riferimenti: `src/e2e/checkout/features/*.feature`,
`src/e2e/checkout/environment.py`, `src/e2e/checkout/tests/checkout-payment.spec.js`.

## Esecuzione locale

Tutti i comandi Behave vanno eseguiti dalla root del repository.

### Singola suite API

PowerShell:

```powershell
$suite = "cart"
$targetEnv = "uat"
$outDir = "reports\allure-results\$suite-$targetEnv"

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $outDir
New-Item $outDir -ItemType Directory -Force | Out-Null

behave "src\api\$suite" -D env=$targetEnv `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --summary --show-timings
```

Bash:

```bash
suite="cart"
target_env="uat"
out_dir="reports/allure-results/${suite}-${target_env}"

rm -rf "$out_dir"
mkdir -p "$out_dir"

behave "src/api/${suite}" -D env="$target_env" \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --summary --show-timings
```

Sostituire `cart` con `auth-service`, `checkout-npg` o `ecommerce-cdc`.

Riferimenti: regole operative di progetto, `src/api/utility/api_test_environment.py`,
`src/api/*/features/*.feature`.

### WISP e FdR

PowerShell:

```powershell
$env:TARGET_ENV = "uat"
$suite = "wisp"
$outDir = "reports\allure-results\$suite-uat"

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $outDir
New-Item $outDir -ItemType Directory -Force | Out-Null

behave "src\integration\$suite" --tags=@runnable `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --junit-directory=junit --junit --summary --show-timings -v
```

Bash:

```bash
export TARGET_ENV=uat
suite="wisp"
out_dir="reports/allure-results/${suite}-uat"

rm -rf "$out_dir"
mkdir -p "$out_dir"

behave "src/integration/${suite}" --tags=@runnable \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --junit-directory=junit --junit --summary --show-timings -v
```

Per FdR usare `suite="fdr"`.

Riferimenti: `.github/workflows/wisp-tests.yml`, `.github/workflows/fdr-tests.yml`,
`.github/workflows/run_behave_tests.yml`, `src/integration/wisp/features/**`,
`src/integration/fdr/features/**`.

### eBollo

PowerShell:

```powershell
$env:TARGET_ENV = "uat"
$outDir = "reports\allure-results\ebollo-uat"

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $outDir
New-Item $outDir -ItemType Directory -Force | Out-Null

behave "src\integration\ebollo" `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --summary --show-timings
```

Bash:

```bash
export TARGET_ENV=uat
out_dir="reports/allure-results/ebollo-uat"

rm -rf "$out_dir"
mkdir -p "$out_dir"

behave "src/integration/ebollo" \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --summary --show-timings
```

Riferimenti: `src/integration/ebollo/environment.py`,
`src/integration/ebollo/features/*.feature`.

### E2E 

PowerShell:

```powershell
$env:ENV_FILE = "dev.env"
$env:HEADLESS = "true"
$outDir = "reports\allure-results\checkout-dev"

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $outDir
New-Item $outDir -ItemType Directory -Force | Out-Null

behave "src\e2e\checkout" `
  -f allure_behave.formatter:AllureFormatter -o $outDir `
  -f progress --summary --show-timings
```

Bash:

```bash
export ENV_FILE=dev.env
export HEADLESS=true
out_dir="reports/allure-results/checkout-dev"

rm -rf "$out_dir"
mkdir -p "$out_dir"

behave "src/e2e/checkout" \
  -f allure_behave.formatter:AllureFormatter -o "$out_dir" \
  -f progress --summary --show-timings
```

Riferimenti: `src/e2e/checkout/environment.py`,
`src/e2e/checkout/dev.env`.

### GPD Cucumber.js

```bash
cd src/integration/gpd
yarn install
yarn test:uat
```

Script disponibili: `test`, `test:local`, `test:dev`, `test:uat`, `test:prod`.

Riferimenti: `src/integration/gpd/package.json`, `src/integration/gpd/README.md`.


## Report Allure

### Convenzioni output

In locale usare:

```text
reports/allure-results/<suite>-<env>
```

Nei workflow WISP/FdR il runner produce `allure-results` nella working directory, poi il report
HTML viene pubblicato come artefatto e copiato su GitHub Pages.

Riferimenti: regole operative di progetto, `.github/workflows/wisp-tests.yml`,
`.github/workflows/fdr-tests.yml`, `.github/workflows/run_behave_tests.yml`.

### Aprire il report locale

PowerShell, usando un percorso assoluto su Windows:

```powershell
allure serve `
  "...\pagopa-platform-integration-test\reports\allure-results\cart-uat" `
  --port 5300
```

Bash:

```bash
allure serve "$PWD/reports/allure-results/cart-uat" --port 5300
```

In alternativa, generare una directory HTML statica:

```bash
allure generate reports/allure-results/cart-uat \
  -o reports/allure-html/cart-uat --clean
allure open reports/allure-html/cart-uat --port 5300
```

Nota sul formatter Behave: `-o` si associa al primo formatter indicato. Mettere sempre
`allure_behave.formatter:AllureFormatter` prima di `-f progress`.

Riferimenti: regole operative di progetto, workflow WISP/FdR, cartelle `reports/`.

### Dashboard pubblicata

La dashboard GitHub Pages espone:

- una landing page da `.github/html/index.html`;
- storico WISP sotto `wisp-tests/`;
- storico FdR nei workflow legacy sotto `fdr-tests/`;
- `last-history` per l'ultimo report processato dagli script di pubblicazione;
- statistiche lette da `widgets/summary.json` e `stats.json`.

Riferimenti: `.github/html/index.html`, `.github/scripts/process_reports.py`,
`.github/scripts/notify_slack.py`, `.github/templates/history-index-template.html`,
`.github/workflows/deploy-test-report.yml`.

## Esecuzione in CI

### Pull request

Il workflow `Check PR` gira sulle pull request verso `main` e applica automazioni di processo:

- assegna la PR all'autore;
- calcola la dimensione della PR;
- applica `size/small` sotto 200 righe modificate;
- applica `size/large` sopra 400 righe modificate;
- ignora nel conteggio alcuni file OpenAPI.

Riferimenti: `.github/workflows/check_pr.yml`, `.github/auto_assign.yml`.

### WISP e FdR

I workflow dedicati installano Python, Java 17, dipendenze Python e `jq`, poi eseguono:

```bash
behave src/integration/wisp --tags=@runnable \
  --format allure_behave.formatter:AllureFormatter -o allure-results \
  --junit-directory=junit --junit --summary --show-timings -v
```

```bash
behave src/integration/fdr --tags=@runnable \
  --format allure_behave.formatter:AllureFormatter -o allure-results \
  --junit-directory=junit --junit --summary --show-timings -v
```

WISP carica `config/.secrets.yaml` dal secret `INTEGRATION_TESTS_SECRETS`.

Riferimenti: `.github/workflows/wisp-tests.yml`, `.github/workflows/fdr-tests.yml`,
`.github/workflows/run_behave_tests.yml`.

### Dispatch e pubblicazione report

- `main-dispatch-tests.yml` esegue WISP ogni giorno alle `06:17 UTC` e permette l'avvio
  manuale per `wisp` o `all`.
- `run_behave_tests.yml` permette l'avvio manuale di WISP e FdR e copia i report su
  `gh-pages` con timestamp.
- `deploy-test-report.yml` scarica gli artefatti, processa i report, aggiorna dashboard e
  invia la notifica Slack se configurata.
- `extract_allure_fail_rate.yml` legge `widgets/summary.json` da `gh-pages`, calcola fail
  rate e success rate, poi passa i dati al workflow di notifica.

Riferimenti: `.github/workflows/main-dispatch-tests.yml`, `.github/workflows/run_behave_tests.yml`, `.github/workflows/deploy-test-report.yml`,
`.github/workflows/extract_allure_fail_rate.yml`, `.github/workflows/send_notification.yml`.

### Documentazione GitHub Pages

Al push su `main`, `landing_pages.yaml` esegue `scenario_parser.py`, genera pagine MkDocs a
partire dalle feature sotto `src/integration` e pubblica `site/` su `gh-pages` mantenendo i
file gia presenti.

Riferimenti: `.github/workflows/landing_pages.yaml`, `scenario_parser.py`.

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

Nota di allineamento: il workflow riusabile storico risolve il path `src/bdd/<suite>` per
wisp e `all`. Prima di usarlo come gate per la struttura attuale del repository, verificare
che il path sia coerente con `src/integration/<suite>`.

Riferimenti: `.github/workflows/test-automation-service.yml`, `docs/examples/*`,
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

Riferimenti: `scripts/tas_orchestrator.py`, `docs/examples/tas-example-*.yml`.

## Documentazione scenari

La documentazione statica delle feature viene generata da `scenario_parser.py` leggendo
`src/integration`. Lo script:

- scansiona i file `.feature` sotto ogni componente di integrazione;
- esclude di default i tag `skip` e `need_fix`;
- scrive pagine Markdown sotto `docs/components`;
- genera `docs/index.md`, `docs/all_scenarios.txt` e `mkdocs.yml`;
- aggiunge link verso i report Allure del componente.

Comando equivalente al workflow:

```bash
python3 scenario_parser.py \
  --repo-name pagopa-platform-integration-test \
  --page-name "PagoPA platform integration test"
mkdocs build
```

Riferimenti: `scenario_parser.py`, `.github/workflows/landing_pages.yaml`.

## Contribuire

### Convenzioni Gherkin

- Usare un solo `Feature` per file.
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
5. Considerare completata la modifica solo con `0` scenari falliti.
6. Se una run fallisce, salvare in `reports/` un report sintetico in italiano con scenari
   falliti, causa probabile e azioni correttive.
7. Non disabilitare scenari falliti per far passare la suite.

Riferimenti: regole operative di progetto, `reports/`, suite esistenti.

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

Riferimenti: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/check_pr.yml`, regole operative di progetto.

## Troubleshooting

| Problema | Causa probabile | Azione |
|---|---|---|
| `No steps directory` con `behave src/api` | Behave richiede una suite con `features/` e `steps/` | eseguire `behave src/api/<suite>` |
| `File di configurazione non trovato` | `-D env=<env>` punta a un file assente | verificare `config/api-tests/.env.<env>` |
| Allure scrive errore su directory output | `-o` associato al formatter sbagliato | mettere AllureFormatter prima di `-f progress` |
| Report non trovato su Windows | path relativo risolto da cwd diverso | usare path assoluto con `allure serve` |
| Errori certificato nelle API suite | trust store locale non configurato | usare store OS o `REQUESTS_CA_BUNDLE` / `SSL_CERT_FILE` |
| Segreti mancanti in integrazione | `config/.secrets.yaml` assente o incompleto | copiarlo dal template e compilare i valori reali |
| Browser Playwright non trovato | browser runtime non installato | eseguire `playwright install` o `npx playwright install` |
| Workflow riusabile non trova WISP | path storico non allineato alla struttura attuale | verificare `src/bdd` vs `src/integration` nel workflow |

Riferimenti: `src/api/utility/http_client.py`, `src/api/utility/api_test_environment.py`,
`config/.secrets_template.yaml`, workflow CI, regole operative di progetto.

## Tracciabilita delle fonti

| Area documentata | Fonti |
|---|---|
| Dipendenze e setup Python | `requirements.txt`, workflow di setup Python |
| Configurazione API | `config/api-tests/.env.dev`, `config/api-tests/.env.uat`, `src/api/utility/api_test_environment.py` |
| Configurazione integrazione | `config.yaml`, `commondata.yaml`, `config/.secrets_template.yaml`, `src/conf/configuration.py` |
| Comandi API Behave | suite `src/api/*`, feature file, hook `environment.py` |
| Comandi WISP/FdR | `.github/workflows/wisp-tests.yml`, `.github/workflows/fdr-tests.yml`, `.github/workflows/run_behave_tests.yml` |
| Report Allure e dashboard | `.github/scripts/process_reports.py`, `.github/scripts/notify_slack.py`, `.github/html/index.html`, `.github/templates/history-index-template.html` |
| CI e workflow riusabile | `.github/workflows/*.yml`, `scripts/tas_orchestrator.py`, `docs/examples/*` |
| Documentazione scenari | `scenario_parser.py`, `.github/workflows/landing_pages.yaml` |
| Convenzioni di contributo | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/check_pr.yml`, regole operative di progetto |
