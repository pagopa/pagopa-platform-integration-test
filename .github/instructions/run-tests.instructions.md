# Running Tests

Use [the runner workflow](../../docs/workflows/qa-runner/execution.md) for mode,
plan approval, failure policies, five bonus fix attempts and result classification.
Commands below are examples to resolve and present, not authorization to execute.
Run from the repository root after checking the terminal type.
Consult only relevant [README](../../README.md) and CI sections; verify actual
suite paths/configuration and interpreter before running. Do not run bare
`behave`: the repository default paths can select a wider integration scope.

## Output isolation

Allocate a new run ID and a fresh directory per initial/bonus/diagnostic execution.
Never delete or reuse a shared result directory. Naming examples:

- Allure: `reports\allure-results\<suite>-<env>\<run-id>\<attempt-id>`
- JUnit: `reports\junit\<suite>-<env>\<run-id>\<attempt-id>`
- Console logs: `reports\run-logs\<run-id>\<attempt-id>.log`

The approved plan defines the request/run identity and attempt naming scheme;
use `initial-00`, `fix-01` through `fix-05`, or a separately approved diagnostic ID.
Use an exclusive directory creation check: a collision is an error, not permission
to overwrite evidence. Keep each execution's exit status and artifact provenance.
Environment setup and test execution must occur in the same shell process.

## Run an API suite (PowerShell)

`<suite>` is the requested API suite, e.g. `cart`, `auth-service`, `checkout-npg`
or `ecommerce-cdc`; `<env>` is an explicitly confirmed supported environment.
Resolve placeholders, interpreter and output scheme before approval.

```powershell
$env:TARGET_ENV = "<env>"
$suite = "<suite>"
$runId = "<unique-run-id>"
$attemptId = "initial-00"
$outDir = "reports\allure-results\$suite-$env:TARGET_ENV\$runId\$attemptId"
if (Test-Path -LiteralPath $outDir) { throw "Output already exists: $outDir" }
New-Item -Path $outDir -ItemType Directory -ErrorAction Stop | Out-Null
behave "src\api\$suite" `
    -f allure_behave.formatter:AllureFormatter -o $outDir `
    -f progress --summary --show-timings
$testExit = $LASTEXITCODE
```

Record `$testExit` immediately, before another command overwrites it. The runner
also retains actual console output; the variable alone is not a passing result.

## Run WISP or FdR in UAT (PowerShell)

Use `src\integration`, consistent with the README, actual suites and CI.
Set `$env:suite` only where the selected suite's configuration requires it.

```powershell
$env:TARGET_ENV = "uat"
$suite = "wisp"
$env:suite = $suite
$runId = "<unique-run-id>"
$attemptId = "initial-00"
$outDir = "reports\allure-results\$suite-uat\$runId\$attemptId"
$junitDir = "reports\junit\$suite-uat\$runId\$attemptId"
foreach ($path in @($outDir, $junitDir)) {
    if (Test-Path -LiteralPath $path) { throw "Output already exists: $path" }
    New-Item -Path $path -ItemType Directory -ErrorAction Stop | Out-Null
}
behave "src\integration\$suite" --tags=@runnable `
    -f allure_behave.formatter:AllureFormatter -o $outDir `
    -f progress --junit-directory=$junitDir --junit --summary --show-timings -v
$testExit = $LASTEXITCODE
```

For FdR set `$suite = "fdr"`. Do not extrapolate these selectors/environment rules
to eBollo, E2E, unit tests or another framework. Use their actual documented
configuration and confirmed targeted command. Unit checks use the repository's
existing test runner/interpreter; no automatic dependency installation.

## View an existing Allure report

Only on a separate explicit request to open a server, resolve the exact selected
attempt to an absolute existing path from the repository root:

```powershell
$results = (Resolve-Path -LiteralPath "<exact-attempt-results-path>" -ErrorAction Stop).Path
allure serve $results --port <approved-free-port>
```

Specify server lifetime and cleanup; do not open an unrelated attempt or start a
server as part of normal test execution. Allure/JUnit artifacts remain supported;
standalone narrative error reports are Markdown, not HTML.

## Validation and safety rules

- Check approved selection, actual counts, exit code, hook/step errors, skips,
  undefined/pending cases and fresh artifacts. Zero failures or exit code zero
  alone does not prove success; zero executed tests are inconclusive.
- Preserve the initial failure and all later outcomes; the bonus budget starts
  after the first failure and permits at most five authorized fix attempts.
  Skipping/stopping the loop goes directly to the unresolved-suite-error report.
- Do not skip failing tests, invent counts, merge attempts, use stale artifact
  success, or claim a partial/running/cancelled execution passed.
- On certificate errors, diagnose the trust/configuration issue; do not disable
  verification, delete client modules or silently change endpoints/protocols.
- Installation, external-state setup, expanded scope or changed environment
  require appropriate approval. Report actual failures explicitly.
