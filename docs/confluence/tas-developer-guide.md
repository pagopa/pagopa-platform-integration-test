# Test Automation Service — Guida per lo sviluppatore

## Prerequisiti

### Per tutti i chiamanti

- Nessun segreto legato ai test da configurare: i segreti di test sono gestiti centralmente nell'environment `integration-tests` del repository TAS, indipendentemente dalla modalità di integrazione usata.
- Il repository `pagopa/pagopa-platform-integration-test` è **pubblico**: non è richiesto alcun accesso speciale per leggerlo.

### Per i chiamanti GitHub Actions (`workflow_call`)

- **Nessun PAT richiesto** per avviare il workflow e leggere gli output: GitHub Actions orchestra la chiamata nativamente tramite la direttiva `uses:`, senza passare da API esterne.
- Un PAT è necessario solo se si vuole scaricare gli artifact del report dal repo TAS (vedi sezione [Recupero del report completo](#recupero-del-report-completo-artifact)). In quel caso gli scope minimi sono **`public_repo`** e **`actions:read`**.

### Per i chiamanti con `tas_orchestrator.py` o raw `workflow_dispatch` (GitHub Actions / Azure DevOps / qualsiasi sistema)

- Python 3.9+ e `pip install requests` (solo per `tas_orchestrator.py`).
- Un GitHub Personal Access Token (PAT) con scope **`public_repo`** e **`actions:read`**, salvato come secret nel sistema chiamante (`INTEGRATION_TEST_PAT` negli esempi seguenti).
  Il PAT è necessario perché queste modalità triggerano il workflow tramite API GitHub, operazione che richiede autenticazione anche su repo pubblici.

---

## Opzioni di integrazione

| # | Opzione | Chiamante | Modalità | Risultati |
|---|---|---|---|---|
| 1 | `workflow_call` | GitHub Actions | Sincrona | ✅ Output nativi |
| 2 | `tas_orchestrator.py --sync` | GHA / Azure DevOps / any | Sincrona | ✅ stdout + exit code |
| 3 | `tas_orchestrator.py` (async) | GHA / Azure DevOps / any | Asincrona | ❌ (solo correlation_id) |
| 4 | `workflow_dispatch` (raw) | Qualsiasi | Asincrona | ❌ |

---

## Opzione 1 — `workflow_call` da GitHub Actions (sincrona)

**Quando usarla:** la tua pipeline è GitHub Actions e vuoi bloccare l'esecuzione leggendo i risultati
come output nativi del job GHA.

**Come funziona:** il job chiamante resta in attesa finché `test-automation-service.yml` non termina.
Se uno scenario fallisce, il workflow chiamato esce con codice 1, il che fa fallire automaticamente
il job chiamante. I risultati sono disponibili come output nominati nel contesto `needs`.

```yaml
# .github/workflows/deploy.yml  (in your repo)
name: Build, Test & Deploy

on:
  push:
    branches: [main]

jobs:

  # ── Step 1: run integration tests ────────────────────────────────────────
  integration-tests:
    uses: pagopa/pagopa-platform-integration-test/.github/workflows/test-automation-service.yml@main
    with:
      test_suite: wisp           # wisp | all
      environment: uat           # dev | uat
      caller_id: ${{ github.repository }}
    # Nessun secrets: da passare — i segreti di test vivono nel repo TAS centralizzato

  # ── Step 2: deploy only if tests passed ───────────────────────────────────
  deploy:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - name: Show test results
        run: |
          echo "Suite    : ${{ needs.integration-tests.outputs.suite }}"  # not an output, FYI
          echo "Passed   : ${{ needs.integration-tests.outputs.passed }}"
          echo "Failed   : ${{ needs.integration-tests.outputs.failed }}"
          echo "Skipped  : ${{ needs.integration-tests.outputs.skipped }}"
          echo "Total    : ${{ needs.integration-tests.outputs.total }}"
          echo "Duration : ${{ needs.integration-tests.outputs.duration }}s"
          echo "Outcome  : ${{ needs.integration-tests.outputs.outcome }}"

      - name: Deploy application
        run: ./deploy.sh
```

**Output disponibili su `needs.integration-tests.outputs`:**

| Output | Valore di esempio | Descrizione |
|---|---|---|
| `passed` | `42` | Scenari superati |
| `failed` | `0` | Scenari falliti |
| `skipped` | `3` | Scenari saltati |
| `total` | `45` | Scenari totali |
| `duration` | `134.7` | Tempo di esecuzione (secondi) |
| `outcome` | `success` | `success` oppure `failure` |

> **Nota:** non è necessario alcun PAT per l'invocazione via `workflow_call`: GitHub Actions gestisce la chiamata nativamente.
> Un PAT è richiesto solo per il download degli artifact dal repo TAS (vedi sezione dedicata).
> I segreti di test sono gestiti centralmente nell'environment `integration-tests` del repository TAS.

---

## Opzione 2 — `tas_orchestrator.py --sync` (sincrona)

**Quando usarla:** vuoi un comportamento sincrono e vuoi il riepilogo completo visibile nel log dello step, oppure la tua pipeline non è GitHub Actions.

### Da GitHub Actions

### Da GitHub Actions

```yaml
# .github/workflows/deploy.yml  (nel tuo repository)
name: Build, Test & Deploy

on:
  push:
    branches: [main]

jobs:

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Installa le dipendenze dell'orchestratore
        run: pip install requests

      - name: Scarica tas_orchestrator.py
        run: |
          curl -sSfL \
            "https://raw.githubusercontent.com/pagopa/pagopa-platform-integration-test/main/scripts/tas_orchestrator.py" \
            -o tas_orchestrator.py

      # Exit 0 = tutti i test passati  → job OK   → deploy eseguito
      # Exit 1 = scenari falliti       → job KO   → deploy saltato
      # Exit 2 = errore orchestrazione (config / timeout)
      - name: Esegui integration test (sync)
        run: |
          python tas_orchestrator.py \
            --suite wisp \
            --env uat \
            --caller-id "${{ github.repository }}" \
            --sync
        env:
          GITHUB_TOKEN: ${{ secrets.INTEGRATION_TEST_PAT }}

  deploy:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - name: Deploya l'applicazione
        run: ./deploy.sh
```

**Esempio di output stampato nel log dello step:**

```
======================================================
   TEST AUTOMATION SERVICE — RESULTS SUMMARY
======================================================
   Correlation ID  : 3f2a1b4c-...
   Caller          : pagopa/pagopa-checkout
   Suite           : wisp
   Environment     : uat
------------------------------------------------------
   Passed          : 42
   Failed          : 0
   Skipped         : 3
   Total           : 45
   Duration        : 134.7s
------------------------------------------------------
   Outcome         : PASSED
======================================================
```

### Da Azure DevOps

**Configurazione del secret in Azure DevOps:**

1. Vai su **Pipelines → Library → Variable Groups** (oppure direttamente nelle variabili della pipeline).
2. Aggiungi una variabile chiamata `INTEGRATION_TEST_PAT` e contrassegnala come **secret**.
3. Valore: il GitHub PAT con scope `public_repo` + `actions:read`.

```yaml
# azure-pipelines.yml  (nel tuo repository ADO)
trigger: none

parameters:
  - name: suite
    type: string
    default: wisp
    values: [wisp, all]
  - name: environment
    type: string
    default: uat
    values: [dev, uat]

variables:
  PYTHON_VERSION: "3.11"
  TAS_REPO: "pagopa/pagopa-platform-integration-test"
  TAS_REF: "main"

stages:

  # ── Stage 1: Integration test ─────────────────────────────────────────────
  - stage: IntegrationTests
    displayName: "Integration Tests"
    jobs:
      - job: RunTests
        displayName: "Avvia e attendi i risultati"
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(PYTHON_VERSION)"

          - script: pip install requests
            displayName: "Installa dipendenze"

          - script: |
              curl -sSfL \
                "https://raw.githubusercontent.com/$(TAS_REPO)/$(TAS_REF)/scripts/tas_orchestrator.py" \
                -o tas_orchestrator.py
            displayName: "Scarica tas_orchestrator.py"

          - script: |
              python tas_orchestrator.py \
                --suite "${{ parameters.suite }}" \
                --env "${{ parameters.environment }}" \
                --caller-id "$(Build.Repository.Name)/$(Build.BuildId)" \
                --sync
            displayName: "Esegui integration test (sync)"
            env:
              # Salva INTEGRATION_TEST_PAT come variabile secret in ADO
              GITHUB_TOKEN: $(INTEGRATION_TEST_PAT)

  # ── Stage 2: Deploy (si esegue solo se IntegrationTests ha avuto successo) ──
  - stage: Deploy
    displayName: "Deploy"
    dependsOn: IntegrationTests
    condition: succeeded()
    jobs:
      - job: DeployApp
        pool:
          vmImage: ubuntu-latest
        steps:
          - script: echo "Deploying..."
            displayName: "Deploy"
```

---

## Opzione 3 — `tas_orchestrator.py` (async)

**Quando usarla:** vuoi lanciare i test senza attenderne l'esito — ad esempio per eseguirli
in parallelo con altri job, o a scopo puramente osservativo.

### Da GitHub Actions

```yaml
jobs:
  trigger-tests:
    runs-on: ubuntu-latest
    outputs:
      correlation_id: ${{ steps.trigger.outputs.correlation_id }}
    steps:
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }

      - run: pip install requests

      - run: |
          curl -sSfL \
            "https://raw.githubusercontent.com/pagopa/pagopa-platform-integration-test/main/scripts/tas_orchestrator.py" \
            -o tas_orchestrator.py

      - name: Avvia i test (fire-and-forget)
        id: trigger
        run: |
          # Lo script stampa CORRELATION_ID=<uuid> e RUN_NAME=<name> su stdout
          python tas_orchestrator.py \
            --suite wisp \
            --env uat \
            --caller-id "${{ github.repository }}"
          # Cattura CORRELATION_ID per uso downstream se necessario
          echo "correlation_id=$(python tas_orchestrator.py ... 2>/dev/null | grep CORRELATION_ID | cut -d= -f2)" >> $GITHUB_OUTPUT
        env:
          GITHUB_TOKEN: ${{ secrets.INTEGRATION_TEST_PAT }}

      - name: Continua senza attendere
        run: echo "Test avviati. Monitora su https://github.com/pagopa/pagopa-platform-integration-test/actions"
```

> **Nota:** in modalità async lo script esce sempre con `0`. Il chiamante non si blocca e
> non può determinare l'esito dei test dall'exit code.

### Da Azure DevOps

```yaml
stages:
  - stage: TriggerTests
    jobs:
      - job: FireAndForget
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: UsePythonVersion@0
            inputs: { versionSpec: "3.11" }

          - script: pip install requests
            displayName: "Installa dipendenze"

          - script: |
              curl -sSfL \
                "https://raw.githubusercontent.com/pagopa/pagopa-platform-integration-test/main/scripts/tas_orchestrator.py" \
                -o tas_orchestrator.py
            displayName: "Scarica tas_orchestrator.py"

          - script: |
              python tas_orchestrator.py \
                --suite wisp \
                --env uat \
                --caller-id "$(Build.Repository.Name)"
              # Stampa CORRELATION_ID=<uuid> — salvalo se vuoi tracciare la run in seguito
            displayName: "Avvia i test (async)"
            env:
              GITHUB_TOKEN: $(INTEGRATION_TEST_PAT)

  - stage: ContinueImmediately
    dependsOn: TriggerTests
    jobs:
      - job: NextStep
        pool: { vmImage: ubuntu-latest }
        steps:
          - script: echo "Test avviati in background, la pipeline continua."
```

---

## Opzione 4 — Raw `workflow_dispatch` (fire-and-forget, senza script)

**Quando usarla:** massima semplicità, nessun risultato necessario, solo avvio.

### Da GitHub Actions

```yaml
steps:
  - name: Avvia gli integration test
    run: |
      gh api repos/pagopa/pagopa-platform-integration-test/actions/workflows/test-automation-service.yml/dispatches \
        -X POST \
        -f ref=main \
        -f "inputs[test_suite]=wisp" \
        -f "inputs[environment]=uat" \
        -f "inputs[caller_id]=${{ github.repository }}"
    env:
      GH_TOKEN: ${{ secrets.INTEGRATION_TEST_PAT }}
```

### Da Azure DevOps (curl)

```yaml
- script: |
    curl -X POST \
      -H "Authorization: Bearer $(INTEGRATION_TEST_PAT)" \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      -d '{"ref":"main","inputs":{"test_suite":"wisp","environment":"uat","caller_id":"my-ado-pipeline"}}' \
      https://api.github.com/repos/pagopa/pagopa-platform-integration-test/actions/workflows/test-automation-service.yml/dispatches
  displayName: "Avvia integration test (fire-and-forget)"
```

> L'API restituisce `HTTP 204 No Content` in caso di successo. Non viene restituito alcun run_id.
> Monitora la run avviata su:
> `https://github.com/pagopa/pagopa-platform-integration-test/actions`

---

## Recupero del report completo (artifact)

Il workflow TAS carica sempre l'artifact `test-results` sulla run GHA che lo esegue.
Lo zip contiene `test-summary.json`, `behave-results.json` e la cartella `junit/` con i report XML.

Le API necessarie sono due:
1. Ottenere la lista degli artifact della run → `GET /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts`
2. Scaricare lo zip → `GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip`

La disponibilità del `run_id` varia in base alla modalità di integrazione usata.

---

### Da `tas_orchestrator.py --sync`

Lo script stampa `RUN_ID=<id>` su stdout prima del riepilogo. Il `run_id` è quindi
disponibile direttamente, senza chiamate API aggiuntive.

```bash
# Cattura RUN_ID dall'output dello script
RUN_ID=$(python tas_orchestrator.py --suite wisp --env uat --caller-id myapp --sync \
  | grep '^RUN_ID=' | cut -d= -f2)

# Scarica l'artifact
curl -sSfL \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/pagopa/pagopa-platform-integration-test/actions/runs/${RUN_ID}/artifacts" \
  | python -c "import sys,json; print(next(a['id'] for a in json.load(sys.stdin)['artifacts'] if a['name']=='test-results'))" \
  | xargs -I{} curl -sSfL \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      -L "https://api.github.com/repos/pagopa/pagopa-platform-integration-test/actions/artifacts/{}/zip" \
      -o test-results.zip

unzip test-results.zip -d test-results/
```

---

### Da `tas_orchestrator.py` (async)

In modalità async lo script esce prima che la run sia visibile su GitHub, quindi non può
fornire il `run_id`. Lo script stampa però `CORRELATION_ID` e `RUN_NAME` (`tas-{correlation_id}`),
che permettono di ritrovare la run con una ricerca per nome.

```bash
# Recupera il run_id cercando per nome (eseguire dopo che i test sono terminati)
CORRELATION_ID="<uuid-ricevuto-dallo-script>"
RUN_NAME="tas-${CORRELATION_ID}"

RUN_ID=$(curl -sSfL \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/pagopa/pagopa-platform-integration-test/actions/runs?event=workflow_dispatch&per_page=50" \
  | python -c "
import sys, json
runs = json.load(sys.stdin)['workflow_runs']
match = next((r for r in runs if r['name'] == '${RUN_NAME}'), None)
print(match['id'] if match else '')
")

# Poi proseguire con il download come mostrato nella sezione --sync sopra
```

---

### Da `workflow_call`

La `workflow_call` non espone il `run_id` della run TAS tra gli output nativi.
Anche in questo caso occorre cercare la run per nome; il `correlation_id` passato
come input al workflow diventa il `run-name: tas-{correlation_id}`.

```yaml
# Nel job chiamante, dopo aver ricevuto gli output
- name: Recupera artifact TAS (opzionale)
  run: |
    CORRELATION_ID="${{ inputs.correlation_id }}"  # o il valore passato al workflow
    RUN_NAME="tas-${CORRELATION_ID}"

    RUN_ID=$(curl -sSfL \
      -H "Authorization: Bearer ${{ secrets.INTEGRATION_TEST_PAT }}" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/pagopa/pagopa-platform-integration-test/actions/runs?event=workflow_call&per_page=50" \
      | python3 -c "
    import sys, json
    runs = json.load(sys.stdin)['workflow_runs']
    match = next((r for r in runs if r['name'] == '${RUN_NAME}'), None)
    print(match['id'] if match else '')
    ")

    echo "RUN_ID=$RUN_ID"
    # Proseguire con il download dell'artifact come mostrato sopra
```

> **Nota:** per la modalità `workflow_call` conviene sempre passare un `correlation_id`
> esplicito (es. `${{ github.run_id }}-${{ github.run_attempt }}`) in modo da avere
> un identificatore univoco con cui ritrovare la run TAS.

---

### Da `workflow_dispatch` raw / Opzione 4

Non è disponibile alcun identificatore della run all'atto del dispatch (l'API restituisce
solo `HTTP 204`). L'unico modo per ritrovare la run è passare un `caller_id` o
`correlation_id` nei parametri del dispatch e cercare per run-name come mostrato
nella sezione async sopra.

---

## Riferimento CLI — `tas_orchestrator.py`

```
uso: tas_orchestrator.py [-h]
                             --suite {wisp,all}
                             --env {dev,uat}
                             --caller-id CALLER_ID
                             [--correlation-id CORRELATION_ID]
                             [--sync]
                             [--repo REPO]
                             [--workflow WORKFLOW]
                             [--ref REF]

argomenti:
  --suite           Suite di test da eseguire: wisp | all
  --env             Ambiente target: dev | uat
  --caller-id       Identificativo del sistema chiamante (es. nome del repo)
  --correlation-id  Correlation ID personalizzato (UUID auto-generato se omesso)
  --sync            Attende il completamento ed esce con l'esito dei test
  --repo            Repo GitHub in formato owner/repo (default: pagopa/pagopa-platform-integration-test)
  --workflow        Nome del file workflow (default: test-automation-service.yml)
  --ref             Git ref su cui eseguire il workflow (default: main)

variabili d'ambiente:
  GITHUB_TOKEN      Obbligatoria. PAT con scope repo + actions:read.
  GITHUB_REPO       Opzionale. Sovrascrive --repo.
  WORKFLOW_FILE     Opzionale. Sovrascrive --workflow.

exit code:
  0   Test superati (oppure dispatch inviato in modalità async)
  1   Uno o più scenari falliti
  2   Errore di orchestrazione (token mancante, timeout, errore API)
```

---

## Risoluzione dei problemi

| Sintomo | Causa | Soluzione |
|---|---|---|
| `GITHUB_TOKEN environment variable is not set` | PAT non configurato | Imposta la variabile d'ambiente `GITHUB_TOKEN` nella tua pipeline |
| `Dispatch failed: HTTP 404` | Repo o nome del workflow errati | Controlla i valori di `--repo` e `--workflow` |
| `Dispatch failed: HTTP 403` | Il PAT non ha i permessi necessari | Verifica che il PAT abbia gli scope `repo` + `actions:read` |
| `Run not found after 20 attempts` | Latenza GitHub / correlation_id errato | Riprova; verifica che il `run-name` corrisponda a `tas-{correlation_id}` |
| `Artifact 'test-results' not found` | Il workflow è fallito prima dello step di upload | Controlla i log della run GHA direttamente |
| `Timeout: run did not complete within 1800s` | I test impiegano troppo tempo | Aumenta `POLL_TIMEOUT_SECONDS` nello script |
| Il job GHA chiamante fallisce nonostante `outcome=success` | `outputs:` a livello di job non propagati | Verifica che il workflow TAS abbia `outputs:` definiti a livello del job `run_tests` |
