# Test Automation Service — Developer Guide

This guide is intended for external teams who want to integrate the **Test Automation Service (TAS)**
into their CI/CD pipelines. Before choosing an integration option, read the
[Which option should I choose?](#which-option-should-i-choose) section, which will guide you
through the decision using a flowchart.

---

## Prerequisites

### For all callers

- No test-related secrets to configure: test secrets are managed centrally in the
  `integration-tests` environment of the TAS repository, regardless of the integration
  mode used.
- The `pagopa/pagopa-platform-integration-test` repository is **public**: no special
  access is required to read it.

### For GitHub Actions callers (`workflow_call`)

- **No PAT required** to trigger the workflow and read its outputs: GitHub Actions orchestrates
  the call natively via the `uses:` directive, without going through external APIs.
- A PAT is only needed if you want to download the full report artifact from the TAS repo
  (see [Downloading the full report artifact](#downloading-the-full-report-artifact)).
  In that case the minimum required scopes are **`public_repo`** and **`actions:read`**.

### For callers using the official ADO template or GHA composite action

- A GitHub Personal Access Token (PAT) with scopes **`public_repo`** and **`actions:read`**,
  stored as a secret in the calling system (`INTEGRATION_TEST_PAT` in the examples below).
  A PAT is required because both wrappers trigger the workflow via the GitHub API, which
  requires authentication even on public repositories. The template/action forward it to
  their internal engine as `TAS_GITHUB_TOKEN`.
- No Python setup on your side: the wrappers bootstrap Python and download their internal
  engine (`tas_orchestrator.py`) automatically.

---

## Which option should I choose?

Use the following flowchart to identify the option that best fits your situation.

```mermaid
flowchart TD
    A([Start]) --> B{Is your CI/CD\nAzure DevOps?}

    B -- Yes --> G([Option 1\nOfficial ADO template\nany ref supported])
    B -- No --> C{Is your CI/CD\nGitHub Actions?}

    C -- No --> X([TAS is called only from GHA or ADO\nadd a small GHA/ADO pipeline\nthat invokes Option 1 or 2])
    C -- Yes --> D{Need a switchable\nsync/async/raw entry point?}

    D -- Yes --> H([Option 2\nOfficial GHA composite action])
    D -- No --> E{Prefer a native call\nor a packaged wrapper?}

    E -- "native and minimal, no PAT" --> F([Option 3\nworkflow_call])
    E -- "packaged wrapper, richer outputs" --> H
```

> **Notes on the GitHub Actions branch:** `workflow_call` (Option 3) is **synchronous** and
> runs the TAS code from a **fixed** ref baked into `uses: …@<ref>`. If you need `async`/`raw`
> modes **or** a dynamic ref chosen at runtime (e.g. a feature branch), use **Option 2**.
> Both **Option 1 (ADO)** and **Option 2 (GHA action)** support any `ref` and all three modes.

### Quick reference

| #     | Option | Mode | Target branch | Caller | Results |
|-------|---|---|---|---|---|
| **1** | Official ADO template | sync / async / raw (parameter) | Any branch ✅ | Azure DevOps only | ✅ Normalised output variables |
| **2** | Official GHA composite action | sync / async / raw (parameter) | Any branch ✅ | GitHub Actions only | ✅ Normalised step outputs |
| **3** | `workflow_call` | Synchronous | `main` only (fixed) | GitHub Actions only | ✅ Native GHA outputs |

---

## The target branch question

A crucial aspect to consider when choosing an integration option is the ability to specify
**which branch of the TAS repository** the tests should run from.

This becomes relevant when the team developing the product under test and the team writing
the tests are working **in parallel on separate feature branches**. At this stage, the new
tests are not yet available on `main` of the TAS repo: the calling team needs to be able to
point to the test feature branch — otherwise the pipeline would run outdated scenarios, or
worse, scenarios that do not yet cover the new functionality under development.

| Option | Target branch | Notes |
|---|---|---|
| `workflow_call` | **Fixed** — hardcoded in the `uses: ...@<ref>` directive in the caller's YAML | Cannot be made dynamic: **GitHub Actions limitation** |
| Official ADO template | **Dynamic** — `ref` template parameter at runtime | Recommended for ADO callers |
| Official GHA composite action | **Dynamic** — `ref` action input at runtime | Recommended for GHA callers that need a dynamic ref |

> **Recommendation for parallel development:** on Azure DevOps use Option 1 (the ADO
> template) and on GitHub Actions use Option 2 (the GHA composite action), passing
> `ref: <feature-branch>`. Once the feature branch is merged into `main`, simply remove
> the override (the default is already `main`) — no other changes to the pipeline needed.

---
## Option 1 — Official Azure DevOps template (recommended for ADO callers)

**When to use it:** your CI/CD is **Azure DevOps** and you want the simplest,
most maintainable integration. The TAS team publishes an official ADO template
that encapsulates the boilerplate (Python setup,
orchestrator download, secret handling, JSON dispatch, output normalisation)
behind a single, parameterised entry point. Your pipeline only declares
parameters and consumes the standardised outputs.

**How it works:** your pipeline references the template as a remote resource
via `resources.repositories`, then injects it into a job **you** own via
`steps: - template:`, choosing the desired `mode` parameter (`sync`, `async`,
or `raw`). Because it is a steps template, you control the wrapping stage/job
(name, `dependsOn`, `condition`) and can invoke it multiple times in one
pipeline. Internally the template selects between the three invocation modes
using compile-time conditionals, but publishes the **same** output variable
names on the **same** step name (`tas`, configurable via `stepName`), so the
output paths are stable regardless of the mode selected.

### Prerequisites

In addition to the standard prerequisites for `tas_orchestrator.py` callers
(PAT, variable group), Azure DevOps needs to be able to fetch the template
from the TAS GitHub repository:

1. **Variable group `tas-integration-secrets`** containing
   `INTEGRATION_TEST_PAT` (secret). Authorise the pipeline:
   *Library → Variable group → Pipeline permissions → +*.
2. **GitHub service connection** in the ADO project:
   *Project settings → Service connections → New service connection → GitHub*.
   Note the connection name (e.g. `pagoPA-projects`) — it goes into the
   `endpoint:` field below. If your project already exposes a shared
   GitHub connection (it typically does), reuse it instead of creating
   a new one.

### Caller pipeline

```yaml
# azure-pipelines-integration-tests.yml  (in your ADO repository)
trigger: none
pr: none

parameters:
  - name: suite
    type: string
    default: wisp
    values: [wisp, all]
  - name: environment
    type: string
    default: uat
    values: [dev, uat]
  - name: mode
    type: string
    default: sync
    values: [sync, async, raw]
  - name: ref
    type: string
    default: main
  - name: tags
    type: string
    default: "@runnable"

resources:
  repositories:
    - repository: tas
      type: github
      name: pagopa/pagopa-platform-integration-test
      ref: refs/heads/main          # or refs/tags/v1 for a pinned version
      endpoint: pagoPA-projects     # GitHub service connection name

stages:
  - stage: IntegrationTests
    displayName: "TAS integration tests"
    jobs:
      - job: RunTAS
        pool: { vmImage: ubuntu-latest }
        steps:
          - template: .azuredevops/templates/tas-integration-tests.yml@tas
            parameters:
              suite:       ${{ parameters.suite }}
              environment: ${{ parameters.environment }}
              mode:        ${{ parameters.mode }}
              ref:         ${{ parameters.ref }}
              tags:        ${{ parameters.tags }}
              githubToken: $(INTEGRATION_TEST_PAT)   # secret pipeline variable / KV-linked group

  - stage: Deploy
    dependsOn: IntegrationTests
    condition: succeeded()
    jobs:
      - job: DeployApp
        pool: { vmImage: ubuntu-latest }
        variables:
          # Output variables published by the template step 'tas' in the RunTAS job above:
          CORRELATION_ID: $[ stageDependencies.IntegrationTests.RunTAS.outputs['tas.CORRELATION_ID'] ]
          RUN_ID:         $[ stageDependencies.IntegrationTests.RunTAS.outputs['tas.RUN_ID'] ]
          RUN_URL:        $[ stageDependencies.IntegrationTests.RunTAS.outputs['tas.RUN_URL'] ]
        steps:
          - script: |
              echo "Correlation ID : $(CORRELATION_ID)"
              echo "Run ID         : $(RUN_ID)"
              echo "Run URL        : $(RUN_URL)"
              ./deploy.sh
            displayName: "Deploy"
```

A ready-to-copy version is available at
[`docs/tas/examples/tas-example-ado-using-template.yml`](examples/tas-example-ado-using-template.yml).
The template itself, its public contract and the versioning policy are
documented in
[`.azuredevops/templates/README.md`](../../.azuredevops/templates/README.md).

### Template parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `testType` | string | `integration` | Test category: `integration`, `e2e`, or `api` (maps to `src/<testType>/<suite>` on the TAS workflow) |
| `suite` | string | `wisp` | Test suite: `wisp` or `all` |
| `environment` | string | `uat` | Target environment: `dev` or `uat` |
| `mode` | string | `sync` | Invocation mode: `sync`, `async`, or `raw` |
| `ref` | string | `main` | TAS repo branch/tag to run the tests from |
| `tags` | string | `""` | Behave tag expression to filter scenarios (e.g. `@runnable`, `@e2e`, `@a,@b`). Empty = workflow default (`@runnable`) |
| `allure` | boolean | `false` | Also produce an Allure results directory (`allure-results/`) inside the artifact (extracted under `ARTIFACT_DIR` in sync mode) |
| `githubToken` | string | — | GitHub PAT (`public_repo` + `actions:read`) forwarded to the orchestrator as `TAS_GITHUB_TOKEN`. Source it from a secret pipeline variable / Key Vault–linked group |
| `pythonVersion` | string | `3.11` | Python version used for orchestrator-based modes |
| `tasRepo` | string | `pagopa/pagopa-platform-integration-test` | TAS repository (rarely overridden) |
| `workflowFile` | string | `test-automation-service.yml` | TAS workflow file (rarely overridden) |
| `stepName` | string | `tas` | Publishing step name; prefix used to read the output variables. Override when invoking the template multiple times in one job |
| `publishTests` | boolean | `true` | Publish JUnit results to the ADO **Tests** tab via `PublishTestResults@2` (sync only — silently ignored in async/raw) |
| `testRunTitle` | string | `""` | Title of the published test run. Empty = `TAS — <suite> / <env> (<ref>)` |

### Public contract (output variables)

The template publishes its outputs from the step named `tas` (configurable
via `stepName`). Read them from a downstream stage, substituting your own
stage/job names:

```
stageDependencies.<yourStage>.<yourJob>.outputs['tas.<NAME>']
```

| Variable | `sync` | `async` | `raw` | Description |
|---|:---:|:---:|:---:|---|
| `CORRELATION_ID` | ✅ | ✅ | ✅ | Identifier used to locate the run (`run-name: tas-<id>`) |
| `RUN_ID` | ✅ | — | — | GHA workflow run numeric ID (useful to fetch artifacts) |
| `RUN_URL` | ✅ | — | — | Direct URL to the GHA run |
| `ARTIFACT_DIR` | ✅ | — | — | On-agent path where the TAS artifact (`test-summary.json`, `behave-results.json`, `junit/*.xml`) is extracted |

In modes where a variable is not produced, the value is an **empty string**:
downstream jobs can branch on it with `condition: ne(variables.RUN_ID, '')`.

### Mode-specific behaviour

| Aspect | `sync` | `async` | `raw` |
|---|:---:|:---:|:---:|
| Bootstraps Python + downloads `tas_orchestrator.py` | ✅ | ✅ | — (uses `curl` only) |
| Test outcome propagates to the stage exit code | ✅ | ❌ (dispatch-only) | ❌ (dispatch-only) |
| `Deploy` stage gated by test results via `succeeded()` | ✅ | ❌ (gated by dispatch only) | ❌ (gated by dispatch only) |
| Suitable when test results must block downstream stages | ✅ | ❌ | ❌ |
| Suitable for fire-and-forget / observability runs | ❌ | ✅ | ✅ |
| Requires Python on the agent | ✅ | ✅ | ❌ |

### Versioning

Pin the template to a tag for reproducible builds:

```yaml
resources:
  repositories:
    - repository: tas
      type: github
      name: pagopa/pagopa-platform-integration-test
      ref: refs/tags/v1
      endpoint: pagoPA-projects
```

Breaking changes to the template's public contract (step name, output step
name, parameter names, output variables) are released under a new major tag
(`v1` → `v2`). Internal refactors that preserve the contract are released
on the same tag.

### Why use the template

Compared with hand-rolling the GitHub API dispatch in your own pipeline, the
template:

- collapses ~80 lines of caller YAML down to ~15;
- removes the `variables:` mapping/sequence pitfall that caused `HTTP 401` in
  practice, and the PAT-leak risk of using `$(VAR)` instead of `$VAR` in the
  rendered shell script;
- keeps the output-variable path stable (`tas.*`) regardless of the `mode`
  chosen;
- upgrades its internal engine centrally, so every caller benefits without
  editing its YAML;
- populates the native ADO **Tests** tab automatically in sync mode
  (`PublishTestResults@2` wired for you).

### Test reporting (ADO "Tests" tab)

In `mode: sync` the template enables the Azure DevOps **Tests** tab on the
build summary out of the box:

1. The orchestrator step downloads the TAS artifact and extracts it under
   `$(Agent.TempDirectory)/tas-artifact` (`test-summary.json`,
   `behave-results.json`, `junit/*.xml`). The path is also exposed as the
   output variable `ARTIFACT_DIR`.
2. A `PublishTestResults@2` task runs with `condition: always()` against
   `junit/*.xml`, so the tab is populated even when the orchestrator step
   exits 1 on test failure — that is exactly the case the developer wants
   to inspect from the portal.

Customise the title shown on the portal with the `testRunTitle` parameter
(empty = `TAS — <suite> / <env> (<ref>)`). Opt out entirely with
`publishTests: false` (the artifact is still extracted, so `ARTIFACT_DIR`
remains usable for custom downstream logic).

> The publish step is added at compile time only when both `mode == 'sync'`
> and `publishTests == true`. In `async` / `raw` the dispatch returns before
> the artifact exists, so there is nothing to publish — the parameter is
> silently ignored in those modes.

---

## Option 2 — Official GitHub Actions composite action (recommended for advanced GHA callers)

**When to use it:** your CI/CD is **GitHub Actions** and Option 3
(`workflow_call`) is not enough — typically because you need to target a
feature branch of the TAS repo at runtime (parallel development), or
because you want a single switchable entry point that can run in `sync`,
`async`, or `raw` mode depending on a workflow input. The TAS team
publishes an official GHA composite action that encapsulates the same
boilerplate (Python setup, orchestrator download,
supply-chain verification, secret wiring and stdout parsing) behind a
single step.

> **Reminder:** if your tests are already merged on `main` of the TAS
> repo and you do not need a dynamic `ref`, prefer **Option 3**: it is
> lighter, does not require a PAT, and natively exposes the same numeric
> outputs (`passed`, `failed`, …).

**How it works:** the action is referenced via `uses:` from any step in
your job. Internally it picks between the three invocation strategies
based on the `mode` input, but exposes the **same** output names
(`correlation_id`, `run_id`, `run_url`, `outcome`, `passed`, `failed`,
`skipped`, `total`, `duration`) on the same step ID, so the caller's
`steps.<id>.outputs.*` paths stay identical regardless of the mode. In
`sync` mode the action propagates the orchestrator's exit code, so the
job fails on test failure exactly like Option 1.

### Prerequisites

- **`INTEGRATION_TEST_PAT`** secret in the caller's repository, with
  scopes `public_repo` + `actions:read`. The PAT is required because all
  three modes trigger the TAS workflow via the GitHub API. Composite
  actions cannot read caller secrets implicitly, so the token must be
  passed via the `github_token` input.

### Caller workflow

```yaml
# .github/workflows/deploy.yml  (in your repository)
name: Build, Integration Test & Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      mode:
        type: choice
        options: [sync, async, raw]
        default: sync
      ref:
        type: string
        default: main

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run TAS
        id: tas
        # Pin to a tag (e.g. @v1) for reproducible builds, or track @main
        # to always get the latest version of the action.
        uses: pagopa/pagopa-platform-integration-test/.github/actions/tas-integration-tests@main
        with:
          suite:        wisp
          environment:  uat
          mode:         ${{ inputs.mode || 'sync' }}
          ref:          ${{ inputs.ref  || 'main' }}
          tags:         "@runnable"          # e.g. @e2e (with test_type: e2e); empty = workflow default
          github_token: ${{ secrets.INTEGRATION_TEST_PAT }}
        # The action automatically logs a run summary (sync) or dispatch
        # info (async/raw) at the end. Set `print_summary: "false"` to
        # opt out and consume `steps.tas.outputs.*` yourself.

  deploy:
    needs: integration-tests
    # In sync mode the action fails the step on test failure, so `needs:`
    # already gates the deploy. In async/raw modes only the dispatch
    # outcome is gated.
    if: needs.integration-tests.result == 'success'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
```

A ready-to-copy version is available at
[`docs/tas/examples/tas-example-gha-using-template.yml`](examples/tas-example-gha-using-template.yml).
The action itself, its public contract and the versioning policy are
documented in
[`.github/actions/tas-integration-tests/README.md`](../../.github/actions/tas-integration-tests/README.md).

### Action inputs

| Input | Default | Required | Description |
|---|---|:---:|---|
| `test_type` | `integration` | — | Test category: `integration`, `e2e`, or `api` (maps to `src/<test_type>/<suite>` on the TAS workflow) |
| `suite` | `wisp` | — | Test suite: `wisp` or `all` |
| `environment` | `uat` | — | Target environment: `dev` or `uat` |
| `mode` | `sync` | — | Invocation mode: `sync`, `async`, or `raw` |
| `ref` | `main` | — | TAS repo branch/tag to run the tests from |
| `tags` | `""` | — | Behave tag expression (e.g. `@runnable`, `@e2e`, `@a,@b`). Empty = workflow default (`@runnable`) |
| `allure` | `"false"` | — | Also produce an Allure results directory (`allure-results/`) inside the `test-results` artifact |
| `github_token` | — | ✅ | GitHub PAT (`public_repo` + `actions:read`) |
| `caller_id` | `${{ github.repository }}/${{ github.run_id }}` | — | Identifier of the calling system |
| `correlation_id` | `${{ github.run_id }}-${{ github.run_attempt }}` | — | Unique ID to correlate the run |
| `tas_repo` | `pagopa/pagopa-platform-integration-test` | — | TAS repository (rarely overridden) |
| `workflow_file` | `test-automation-service.yml` | — | TAS workflow file (rarely overridden) |
| `python_version` | `3.11` | — | Python version (orchestrator-based modes only) |
| `verify_orchestrator` | `true` | — | Verify SHA-256 of `tas_orchestrator.py` after download |
| `orchestrator_sha256` | `""` | — | Pinned SHA-256 hex digest (true SRI) |
| `print_summary` | `true` | — | Log the run summary (sync) or dispatch info (async/raw) automatically — set to `"false"` to opt out |

### Public contract (step outputs)

The action exposes the following outputs, read from the step ID:

```
steps.<id>.outputs.<NAME>
```

| Output | `sync` | `async` | `raw` | Description |
|---|:---:|:---:|:---:|---|
| `correlation_id` | ✅ | ✅ | ✅ | Identifier used to locate the run (`run-name: tas-<id>`) |
| `run_id` | ✅ | — | — | GHA workflow run numeric ID (useful to fetch artifacts) |
| `run_url` | ✅ | — | — | Direct URL to the GHA run |
| `outcome` | ✅ | — | — | `success` or `failure` |
| `passed` / `failed` / `skipped` / `total` / `duration` | ✅ | — | — | Numeric counters parsed from the TAS artifact |

In modes where an output is not produced, the value is an **empty string**:
downstream steps can branch on it with `if: steps.tas.outputs.run_id != ''`.

### Mode-specific behaviour

| Aspect | `sync` | `async` | `raw` |
|---|:---:|:---:|:---:|
| Bootstraps Python + downloads `tas_orchestrator.py` | ✅ | ✅ | — (uses `curl` only) |
| Test outcome propagates to the step exit code | ✅ | ❌ (dispatch-only) | ❌ (dispatch-only) |
| Downstream jobs gated by test results via `needs.*.result` | ✅ | ❌ (gated by dispatch only) | ❌ (gated by dispatch only) |
| Suitable when test results must block deployment | ✅ | ❌ | ❌ |
| Suitable for fire-and-forget / observability runs | ❌ | ✅ | ✅ |
| Requires Python on the runner | ✅ | ✅ | ❌ |

### Versioning

Pin the action to a tag for reproducible builds:

```yaml
uses: pagopa/pagopa-platform-integration-test/.github/actions/tas-integration-tests@v1
```

Breaking changes to the action's public contract (input/output names,
removal of modes) are released under a new major tag (`v1` → `v2`).
Internal refactors that preserve the contract are released on the same tag.
---
## Option 3 — `workflow_call` from GitHub Actions (synchronous)

**When to use it:** your pipeline is GitHub Actions, you want to block execution and read the
results as native job outputs, and the tests you want to run are already available on `main`
of the TAS repository.

**How it works:** the calling job waits until `test-automation-service.yml` completes. If one
or more scenarios fail, the called workflow exits with code 1, which automatically fails the
calling job — exactly as if the test were part of your own pipeline. Results (passed, failed,
duration, outcome…) are available as named outputs in the `needs` context, ready to use in
downstream jobs without any additional logic.

**Main limitation:** the TAS repo branch on which the tests run is hardcoded in the `uses:`
directive. GitHub Actions does not support dynamic expressions in that field, so it is not
possible to choose at runtime which branch to run the tests on. If your team and the TAS team
are developing in parallel on separate feature branches, this option is not suitable until
that branch has been merged into `main`.

```yaml
# .github/workflows/deploy.yml  (in your repository)
name: Build, Test & Deploy

on:
  push:
    branches: [main]

jobs:

  # ── Step 1: run integration tests ─────────────────────────────────────────
  integration-tests:
    uses: pagopa/pagopa-platform-integration-test/.github/workflows/test-automation-service.yml@main
    with:
      test_type: integration     # integration | e2e | api
      test_suite: wisp           # wisp | all
      environment: uat           # dev | uat
      caller_id: ${{ github.repository }}
    # No secrets: to pass — test secrets live in the centralised TAS repository

  # ── Step 2: deploy only if tests passed ───────────────────────────────────
  deploy:
    needs: integration-tests
    runs-on: ubuntu-latest
    steps:
      - name: Show test results
        run: |
          echo "Passed   : ${{ needs.integration-tests.outputs.passed }}"
          echo "Failed   : ${{ needs.integration-tests.outputs.failed }}"
          echo "Skipped  : ${{ needs.integration-tests.outputs.skipped }}"
          echo "Total    : ${{ needs.integration-tests.outputs.total }}"
          echo "Duration : ${{ needs.integration-tests.outputs.duration }}s"
          echo "Outcome  : ${{ needs.integration-tests.outputs.outcome }}"

      - name: Deploy application
        run: ./deploy.sh
```

**Available outputs on `needs.integration-tests.outputs`:**

| Output | Example value | Description |
|---|---|---|
| `passed` | `42` | Passed scenarios |
| `failed` | `0` | Failed scenarios |
| `skipped` | `3` | Skipped scenarios |
| `total` | `45` | Total scenarios |
| `duration` | `134.7` | Execution time (seconds) |
| `outcome` | `success` | `success` or `failure` |

> **No PAT required** for `workflow_call` invocations — **even when your caller lives in a
> different repository**. GitHub resolves the `uses: …@<ref>` call natively (it does not go
> through the REST API, so there is no token to supply), and because
> `test-automation-service.yml` reads its test secrets from its **own** `integration-tests`
> environment, those secrets are used regardless of the caller. Per GitHub's reusable-workflow
> rules, environment secrets come from the repository that **defines** the workflow (the TAS
> repo), not from the caller — so you do not pass, inherit, or configure any secret. A PAT is
> only needed if you later want to download the run's artifact (see
> [Downloading the full report artifact](#downloading-the-full-report-artifact)).

### Choosing between Option 2 and Option 3

Both are GitHub-Actions-native and run the same suites, so the choice is mostly a
**preference between a native call and a packaged wrapper** — with one hard constraint:

- **You need a dynamic `ref` (feature branch) or a switchable `sync`/`async`/`raw`
  entry point** → you must use **Option 2**. `workflow_call` hardcodes the ref in
  `uses: …@<ref>` and cannot vary it at runtime, which rules Option 3 out.
- **Otherwise (tests on `main`, synchronous is fine)** → it is a genuine preference.
  **Option 3** (`workflow_call`) is the most native and minimal: no PAT, native job
  outputs, nothing to wrap. **Option 2** (composite action) wraps the same run but
  additionally:
  - keeps the caller to a single step (~10 lines);
  - performs the SHA-256 verification of its internal engine for you (built-in, toggleable);
  - keeps the step-output path stable regardless of the `mode` chosen;
  - upgrades its internal engine centrally, so every caller benefits without editing its YAML;
  - parses the numeric outputs (`passed`, `failed`, …) and exposes them as step outputs.

> Trade-off: Option 2 requires a PAT (`github_token`) because it triggers the run via the
> GitHub API, whereas Option 3 needs none.

---

## Downloading the full report artifact

The TAS workflow always uploads a `test-results` artifact to the GHA run that executed it.
The zip contains `test-summary.json`, `behave-results.json`, and the `junit/` folder with
XML reports. When the caller enables the `allure` input/parameter, it also contains an
`allure-results/` folder that can be rendered to a browsable HTML report with the Allure
CLI (`allure generate allure-results -o allure-report`, or `allure serve allure-results`);
Java + Allure CLI 2.x are required.

Two API calls are needed:
1. List the run's artifacts → `GET /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts`
2. Download the zip → `GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/zip`

> **Options 1 & 2 do this for you.** In `sync` mode the ADO template extracts the artifact
> under `ARTIFACT_DIR` (and publishes JUnit to the Tests tab), and the GHA composite action
> exposes `run_id` / `run_url` as step outputs. The manual lookup below is only relevant for
> **Option 3 (`workflow_call`)**, which does not expose the `run_id`.

---

### Downloading once you have the `run_id`

With a `RUN_ID` in hand, download the artifact:

```bash
# Download the artifact
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

### From `workflow_call`

`workflow_call` does not expose the TAS run's `run_id` among the native outputs.
Here too you need to search for the run by name; the `correlation_id` passed as an input
to the workflow becomes the `run-name: tas-{correlation_id}`.

```yaml
- name: Retrieve TAS artifact (optional)
  run: |
    CORRELATION_ID="${{ inputs.correlation_id }}"
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
    # Then proceed with the artifact download as shown above
```

> **Note:** always pass an explicit `correlation_id` (e.g.
> `${{ github.run_id }}-${{ github.run_attempt }}`) to have a unique identifier
> with which to locate the TAS run.

---

## CLI reference — `tas_orchestrator.py`

> `tas_orchestrator.py` is the **internal engine** wrapped by Option 1 (the ADO
> template) and Option 2 (the GHA composite action). It is documented here for
> reference and troubleshooting; invoking it directly is not a supported
> integration option — use Option 1 or 2 instead.

```
usage: tas_orchestrator.py [-h]
                               [--type {integration,e2e,api}]
                               --suite {wisp,all}
                               --env {dev,uat}
                               --caller-id CALLER_ID
                               [--correlation-id CORRELATION_ID]
                               [--tags TAGS]
                               [--allure]
                               [--sync]
                               [--repo REPO]
                               [--workflow WORKFLOW]
                               [--ref REF]
                               [--artifact-dir ARTIFACT_DIR]

arguments:
  --type            Test category to run: integration | e2e | api
                    (default: integration). Maps to src/<type>/<suite>
                    on the TAS workflow.
  --suite           Test suite to run: wisp | all
  --env             Target environment: dev | uat
  --caller-id       Identifier of the calling system (e.g. repository name)
  --correlation-id  Custom correlation ID (auto-generated UUID if omitted)
  --tags            Behave tag expression to filter scenarios (e.g. '@runnable',
                    '@e2e', '@a,@b' for OR, '~@wip' to exclude). Omitted =
                    the workflow keeps its own default (@runnable).
  --allure          Ask the TAS workflow to also produce an Allure results
                    directory (allure-results/) inside the test-results artifact.
  --sync            Wait for completion and exit with the test outcome
  --repo            GitHub repo in owner/repo format (default: pagopa/pagopa-platform-integration-test)
  --workflow        Workflow filename to trigger (default: test-automation-service.yml)
  --ref             Branch or tag of the TAS repo to run the tests from (default: main).
                    Useful during parallel development to point to a feature branch
                    not yet merged into main.
  --artifact-dir    Sync mode only: directory where the 'test-results' artifact is
                    extracted (test-summary.json, behave-results.json, junit/*.xml).
                    Feed it to PublishTestResults@2 on Azure DevOps or to
                    actions/upload-artifact on GitHub Actions. Skipped when empty.

environment variables:
  TAS_GITHUB_TOKEN  Required. PAT with scopes repo + actions:read. Falls back
                    to GITHUB_TOKEN when unset (backward compatibility).
  GITHUB_TOKEN      Legacy name for the PAT, used only if TAS_GITHUB_TOKEN is unset.
  GITHUB_REPO       Optional. Overrides --repo.
  WORKFLOW_FILE     Optional. Overrides --workflow.

exit codes:
  0   Tests passed (or dispatch sent in async mode)
  1   One or more scenarios failed
  2   Orchestration error (missing token, timeout, API error)
```

---

## Troubleshooting

| Symptom | Likely cause | Solution |
|---|---|---|
| `GITHUB_TOKEN environment variable is not set` | PAT not configured | Set the `GITHUB_TOKEN` environment variable in your pipeline |
| `Dispatch failed: HTTP 404` | Wrong repo or workflow name | Check the values of `--repo` and `--workflow` |
| `Dispatch failed: HTTP 403` | PAT lacks required permissions | Verify the PAT has scopes `repo` + `actions:read` |
| `Run not found after 20 attempts` | GitHub latency / wrong correlation_id | Retry; verify the `run-name` matches `tas-{correlation_id}` |
| `Artifact 'test-results' not found` | Workflow failed before the upload step | Check the GHA run logs directly |
| `Timeout: run did not complete within 1800s` | Tests are taking too long | Increase `POLL_TIMEOUT_SECONDS` in the script |
| All scenarios fail with `health-check systems or subscription-key errors` | The branch in `--ref` does not have updated tests, or the secret is not configured in the `integration-tests` environment | Verify the target branch and check `INTEGRATION_TESTS_SECRETS` in the `integration-tests` environment of the TAS repo |
| Calling GHA job fails despite `outcome=success` | `outputs:` at job level not propagated | Verify the TAS workflow has `outputs:` defined at the `run_tests` job level |
| TAS job fails immediately with `TARGET_ENV is empty — workflow input 'environment' did not propagate` | The caller did not pass `environment` to `test-automation-service.yml`, or a wrapper stripped it | Pass `environment` explicitly via `workflow_call` `with:` / `workflow_dispatch` inputs / `tas_orchestrator.py --env`; do not override `TARGET_ENV` in the step `env:` |
| GHA composite action: numeric outputs (`passed`, `failed`, …) are empty even though tests ran | The action was invoked with `mode: async` or `mode: raw` — those modes only know the dispatch outcome | Switch to `mode: sync` (Option 2 default) to get the parsed counters; use `correlation_id` + run-name `tas-<id>` to download the artifact later in async/raw |
| GHA composite action manifest error `Unrecognized named-value: 'secrets'` | Action `description:` fields cannot contain `${{ … }}` expressions — only the action body can | Keep `${{ … }}` template expressions out of `inputs.*.description` and `outputs.*.description` (already handled in v1+ of the action) |
