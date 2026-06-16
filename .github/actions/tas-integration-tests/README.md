# TAS — GitHub Actions composite action

Official GitHub Actions reusable component published by the Test Automation
Service (TAS) team for external consumers.

| Path | Purpose |
|---|---|
| [`action.yml`](./action.yml) | All-in-one entry point to run TAS integration tests from any GitHub Actions workflow. Supports the `sync`, `async` and `raw` invocation modes behind a single composite action with normalised outputs. |

---

## Why use this action

Without the action, a GHA consumer that wants to use the `tas_orchestrator.py`
flow (Options 2 and 3) has to maintain ~40 lines of YAML per workflow:
Python setup, orchestrator download, integrity verification, secret wiring
and stdout parsing for `CORRELATION_ID` / `RUN_ID` / `RUN_URL`. With this
action the same integration boils down to a single step and the boilerplate
is owned by the TAS team.

The action also normalises a few things that real consumers tend to get
wrong:

- Forgetting the SHA-256 verification of `tas_orchestrator.py` after the
  download (silent supply-chain drift).
- Re-implementing the stdout parsing for `CORRELATION_ID` / `RUN_ID` with
  fragile `cut`/`awk` pipelines that break when the script's log format
  changes.
- Switching the output paths (`steps.trigger.*` vs `steps.dispatch.*`)
  every time the invocation mode is changed (`sync` ↔ `async` ↔ `raw`).

The action exposes the same output names regardless of `mode`, so the
caller's `steps.<id>.outputs.*` paths stay identical.

---

## When NOT to use this action

If your tests are already merged on `main` of the TAS repo and you do not
need to target a feature branch dynamically, prefer the native
`workflow_call` integration (Option 1 in the developer guide). It does not
need a PAT, and it exposes the same numeric outputs (`passed`, `failed`,
…) without any extra boilerplate:

```yaml
jobs:
  integration-tests:
    uses: pagopa/pagopa-platform-integration-test/.github/workflows/test-automation-service.yml@main
    with:
      test_suite: wisp
      environment: uat
```

Use the composite action when:

- You need to choose the TAS repo `ref` at runtime (parallel development
  on a feature branch).
- You need async / fire-and-forget behaviour (Option 3).
- You want a single switchable entry point that can run in `sync`,
  `async`, or `raw` mode depending on a workflow input.

---

## Quick start

```yaml
# .github/workflows/deploy.yml  (in your repository)
name: Build, Integration Test & Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run TAS integration tests
        id: tas
        uses: pagopa/pagopa-platform-integration-test/.github/actions/tas-integration-tests@main
        with:
          suite: wisp
          environment: uat
          mode: sync                       # sync | async | raw
          github_token: ${{ secrets.INTEGRATION_TEST_PAT }}
      # That's it — the action automatically logs the run summary (sync)
      # or dispatch info (async/raw) at the end. Consume `steps.tas.outputs.*`
      # directly when you need numeric counters in downstream steps.
```

A complete consumer example (including the `Deploy` job gated by test
results) is available at
[`../../../docs/tas/examples/tas-example-gha-using-template.yml`](../../../docs/tas/examples/tas-example-gha-using-template.yml).

The full integration guide, including prerequisites (PAT scope), the
flowchart that helps you pick the right option, and the rationale for each
invocation mode, lives in
[`../../../docs/tas/tas-developer-guide.md`](../../../docs/tas/tas-developer-guide.md)
— see the "**Option 6 — Official GitHub Actions composite action**" section.

---

## Public contract

Anything documented in this section is part of the action's stable API.
Changes to these identifiers are released under a new major tag (e.g.
`v1` → `v2`); internal refactors that preserve the contract ship on the
same tag.

### Inputs

| Name | Default | Required | Description |
|---|---|:---:|---|
| `suite` | `wisp` | — | Test suite: `wisp` or `all` |
| `environment` | `uat` | — | Target environment: `dev` or `uat` |
| `mode` | `sync` | — | Invocation mode: `sync`, `async` or `raw` |
| `ref` | `main` | — | TAS repo branch/tag to run the tests from |
| `github_token` | — | ✅ | GitHub PAT (scopes `public_repo` + `actions:read`). Must be passed explicitly (composite actions cannot read caller secrets). |
| `caller_id` | `${{ github.repository }}/${{ github.run_id }}` | — | Identifier of the calling system (traceability) |
| `correlation_id` | `${{ github.run_id }}-${{ github.run_attempt }}` | — | Unique ID to correlate the run with the caller |
| `tas_repo` | `pagopa/pagopa-platform-integration-test` | — | TAS repository (rarely overridden) |
| `workflow_file` | `test-automation-service.yml` | — | TAS workflow file (rarely overridden) |
| `python_version` | `3.11` | — | Python version (orchestrator-based modes only) |
| `verify_orchestrator` | `true` | — | Verify SHA-256 of `tas_orchestrator.py` after download |
| `orchestrator_sha256` | `""` | — | Pinned SHA-256 hex digest (true SRI). When set, the sidecar is ignored. |
| `print_summary` | `true` | — | Print a human-readable summary after the dispatch (counters in sync, dispatch info in async/raw). Set to `"false"` to opt out. |

### Outputs

| Name | `sync` | `async` | `raw` | Description |
|---|:---:|:---:|:---:|---|
| `correlation_id` | ✅ | ✅ | ✅ | Identifier used to locate the run (`run-name: tas-<id>`) |
| `run_id` | ✅ | — | — | GHA workflow run numeric ID |
| `run_url` | ✅ | — | — | Direct URL to the GHA run |
| `outcome` | ✅ | — | — | `success` or `failure` |
| `passed` | ✅ | — | — | Number of passed scenarios |
| `failed` | ✅ | — | — | Number of failed scenarios |
| `skipped` | ✅ | — | — | Number of skipped scenarios |
| `total` | ✅ | — | — | Total scenarios |
| `duration` | ✅ | — | — | Total test duration in seconds |

In modes where an output is not produced, the value is an **empty string**.
Downstream steps can branch on it with `if: steps.tas.outputs.run_id != ''`.

> **The action prints a post-step summary automatically** (sync: full
> counters; async/raw: dispatch info with `correlation_id`, `run-name`
> and Actions URL). Set `print_summary: "false"` to suppress it and
> handle the outputs yourself.
>
> **In async/raw mode the action returns as soon as the dispatch is
> accepted, while the tests are still running on the TAS repository.**
> The numeric counters (`passed`, `failed`, …) and `outcome` are therefore
> not yet knowable and are emitted as empty strings — they are not "zero
> failures". If you build custom logic on top of the outputs, branch on
> the presence of `outcome`:
>
> ```yaml
> - if: always() && steps.tas.outputs.outcome != ''
>   run: echo "Passed=${{ steps.tas.outputs.passed }} / ${{ steps.tas.outputs.total }}"
>
> - if: always() && steps.tas.outputs.outcome == '' && steps.tas.outputs.correlation_id != ''
>   run: echo "Dispatched — track at run-name 'tas-${{ steps.tas.outputs.correlation_id }}'"
> ```

### Exit code (sync mode)

The composite action propagates the orchestrator exit code:

| Exit | Meaning | Effect on the calling job |
|:---:|---|---|
| `0` | All scenarios passed | Step succeeds → job continues |
| `1` | One or more scenarios failed | Step fails → job fails (subsequent `if: success()` steps are skipped) |
| `2` | Orchestration error (missing token, timeout, API error) | Step fails |

`async` and `raw` modes exit `0` as long as the dispatch is accepted; the
test outcome is not knowable in those modes.

---

## Prerequisites for consumers

1. A **GitHub PAT** stored as a secret in the caller's repository (commonly
   `INTEGRATION_TEST_PAT`), with the minimum scopes:
   - `public_repo`
   - `actions:read`

   The PAT is required because all three modes trigger the TAS workflow
   via the GitHub API.

2. **No test secrets to configure**: test secrets live in the
   `integration-tests` environment of the TAS repository and are loaded
   automatically by `test-automation-service.yml`.

---

## Versioning policy

| Change type | Example | Released as |
|---|---|---|
| Contract-preserving fix or internal refactor | Better error message, faster bootstrap, new optional input with a default | Same major tag (e.g. `v1`) |
| Breaking change to inputs/outputs/names | Removed input, renamed output, removed mode | New major tag (`v2`) |

Consumers that prioritise stability **pin a tag**:

```yaml
uses: pagopa/pagopa-platform-integration-test/.github/actions/tas-integration-tests@v1
```

Consumers that prioritise always running the latest fixes track `main`.

---

## Supply-chain integrity

`tas_orchestrator.py` is fetched at job time from `raw.githubusercontent.com`.
To detect tampering or partial downloads the action verifies its SHA-256
before executing it. Two modes are supported, identical to the ADO template
behaviour:

### Sidecar mode (default)

The action downloads `scripts/tas_orchestrator.py.sha256` from the **same**
`ref` and runs `sha256sum -c`. The guarantee is "the script I just
downloaded matches the digest the TAS team published on this ref" — its
strength is therefore tied to how trusted the ref is. Pin a tag
(`@v1`) rather than a moving branch for maximum value.

### Pinned mode (recommended for strict supply-chain requirements)

Set `orchestrator_sha256` to the expected hex digest. The action verifies
the download against that value and **ignores the sidecar**. Survives even
tampering of the ref tip, at the cost of an explicit upgrade step whenever
the orchestrator changes.

```bash
curl -sSfL https://raw.githubusercontent.com/pagopa/pagopa-platform-integration-test/refs/tags/v1/scripts/tas_orchestrator.py \
  | sha256sum
```

```yaml
- uses: pagopa/pagopa-platform-integration-test/.github/actions/tas-integration-tests@v1
  with:
    # ...
    orchestrator_sha256: "a68b6c43c98517352c6d182df4a97b67e33a94ed79ae56949b1f6e6a179b5fe1"
```

### Opting out

Set `verify_orchestrator: "false"` to skip verification entirely. Not
recommended — keep the default on unless you have a specific reason.

---

## Where to ask for help

- Open an issue on
  [`pagopa/pagopa-platform-integration-test`](https://github.com/pagopa/pagopa-platform-integration-test/issues).
- For integration questions not specific to GitHub Actions, see the general
  [TAS developer guide](../../../docs/tas/tas-developer-guide.md).

