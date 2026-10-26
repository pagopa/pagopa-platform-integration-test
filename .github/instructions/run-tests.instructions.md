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

## Interpreter and launch outcome (ADR-55)

Resolve the approved Python executable explicitly. Prefer that interpreter's
`-m behave` (or the selected framework's supported module entrypoint) rather
than an unrelated `behave`/`pytest` on PATH. Record its resolved path/version
and framework/formatter provenance using available evidence or approved checks.
Do not substitute another interpreter on failure.

Distinguish not started, still running and completed. A missing executable or
startup error is not a passing run or a test exit code. Clear stale native exit
state before launch and read the actual completed process status immediately;
never reuse an earlier Git/other command's `$LASTEXITCODE`. In an unattended
script/wrapper, propagate the test exit status explicitly to its caller.

The PowerShell examples below run in a dedicated approved shell, with setup and
execution together. `$ErrorActionPreference = "Stop"` stops preparation/launch
errors; disabling native-error promotion keeps a nonzero test result available
for explicit capture instead of mistaking it for failure to start. `exit` ends
that dedicated shell, not an instruction to close the user's interactive terminal.
For interactive use retain/report the captured status without `exit`; for Bash,
capture `$?` immediately and propagate it from the actual wrapper. Never hide a
test failure behind a successful logging/report command.

## Suite and selection resolution (ADR-56)

For registered suites read [the NRT catalog](../nrt-suites.json): exact `id`,
`behave_path`, each `tags` argument, `envs` and relevant prerequisites such as
`needs_playwright`, dependencies and shared resources. Compare with current
suite configuration and applicable CI; contradictions require resolution.
`fdr` and `fdr3` are distinct suites, not interchangeable aliases.

The catalog describes NRT configuration, not a ban on local unregistered suites
or unit checks. For those resolve their real paths/framework/configuration from
relevant documentation. Do not copy registered-suite assumptions into them.
Keep paths/tag expressions as separate CLI arguments (PowerShell arrays/splatting
or Bash arrays); do not use `Invoke-Expression`/`eval` or build an interpreted
command string. Record deliberate partial selection; never change exclusions,
tags or paths merely to obtain green results.

## Evidence acquisition (ADR-57)

The execution plan specifies the actual capture method: retained tool/session
stdout/stderr, a run-local log file, or an accessible runner artifact. The console
log naming above is a destination convention, not proof that a file was written.
The examples below use retained terminal/tool output, not an implicit log file.
Record its actual reference only once it is available; if the tool cannot retain
it, establish an approved capture method before starting.

Capture process output/status without losing the native exit code in a pipeline.
If writing a log, specify encoding/path and preserve partial output. Distinguish
test outcome from capture/artifact-write/report failures; do not claim a saved
log or complete verification when required evidence is unavailable.
Use only actual paths/references. Summaries must not expose credentials, tokens,
personal data or private payloads. Do not automatically copy raw output into
reports, Git or external systems; handle sensitive output only in an authorized
protected location with an explicit retention/access plan.

## Effective configuration (ADR-58)

Identify selectors actually used by the suite (`TARGET_ENV`, `suite`, `ENV_FILE`,
CLI/config values or applicable alternatives), their precedence and resolved
configuration file/deployment. Consider framework defaults and hooks, not only
what was assigned in the shell. Record safe selectors/paths/provenance, not secret
values or a whole environment dump.

Do not assume `TARGET_ENV` alone proves the tested deployment. Resolve uncertainty
before an environment-specific run; return a blocker rather than silently using
defaults. Change only the needed approved selectors in the execution session;
do not clear the user's entire environment or rewrite configuration to simplify
a run. Recheck effective configuration when materially relevant inputs change.

## Run an API suite (PowerShell)

`<suite>` is the requested API suite, e.g. `cart`, `auth-service`, `checkout-npg`
or `ecommerce-cdc`; `<env>` is an explicitly confirmed supported environment.
Resolve placeholders, interpreter and output scheme before approval.

```powershell
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
$python = (Get-Command "<approved-python-executable>" -CommandType Application -ErrorAction Stop).Source
$env:TARGET_ENV = "<env>"
$suite = "<suite>"
$runId = "<unique-run-id>"
$attemptId = "initial-00"
$outDir = "reports\allure-results\$suite-$env:TARGET_ENV\$runId\$attemptId"
if (Test-Path -LiteralPath $outDir) { throw "Output already exists: $outDir" }
New-Item -Path $outDir -ItemType Directory -ErrorAction Stop | Out-Null
$LASTEXITCODE = $null
& $python -m behave "src\api\$suite" `
    -f allure_behave.formatter:AllureFormatter -o $outDir `
    -f progress --summary --show-timings
$testExit = $LASTEXITCODE
if ($null -eq $testExit) { throw "Test process did not return an exit code" }
exit $testExit
```

Record `$testExit` immediately, before another command overwrites it. The runner
also retains actual console output; the variable alone is not a passing result.

## Run WISP or registered FdR3 in UAT (PowerShell)

Use `src\integration`, consistent with the README, actual suites and CI.
Set `$env:suite` only where the selected suite's configuration requires it.

```powershell
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
$python = (Get-Command "<approved-python-executable>" -CommandType Application -ErrorAction Stop).Source
$env:TARGET_ENV = "uat"
$suite = "wisp"
$env:suite = $suite
$tagArgs = @("--tags=@runnable")
$runId = "<unique-run-id>"
$attemptId = "initial-00"
$outDir = "reports\allure-results\$suite-uat\$runId\$attemptId"
$junitDir = "reports\junit\$suite-uat\$runId\$attemptId"
foreach ($path in @($outDir, $junitDir)) {
    if (Test-Path -LiteralPath $path) { throw "Output already exists: $path" }
    New-Item -Path $path -ItemType Directory -ErrorAction Stop | Out-Null
}
$LASTEXITCODE = $null
& $python -m behave "src\integration\$suite" @tagArgs `
    -f allure_behave.formatter:AllureFormatter -o $outDir `
    -f progress --junit-directory=$junitDir --junit --summary --show-timings -v
$testExit = $LASTEXITCODE
if ($null -eq $testExit) { throw "Test process did not return an exit code" }
exit $testExit
```

For the currently registered FdR3 entry resolve `$suite = "fdr3"` and confirm its
path/tags/environment in the current catalog. Legacy `fdr` needs its own explicit
selection and documentation; do not replace one with the other. The WISP tags
above are an example to confirm, not a hardcoded catalog replacement.
Do not extrapolate these selectors/environment rules to eBollo, E2E, unit tests
or another framework. Use actual documented configuration and confirmed commands.
Unit checks use the existing test runner/interpreter; no automatic installation.

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

## Proportionate preflight (ADR-59, addition)

Before execution check only relevant prerequisites: interpreter, framework/
formatter, selected configuration and required browser/service setup as applicable.
Prefer read-based evidence. Include executable diagnostics in the approved plan;
imports, version checks and credential probes are not automatically harmless.
A missing package/browser is a blocker with a proposed setup step, not permission
to install it, substitute a framework or launch a service.
Possessing credentials does not authorize live validation calls. No universal
preflight suite is required for every targeted unit check; do not duplicate
readiness probes or broaden scope without need and consent.

## Interrupted mutations and remote cleanup (ADR-60, addition)

Stopping a local test process does not roll back a request already sent to a
remote system. After timeout/cancellation of a mutating test, retain operation
correlation and report unknown remote outcomes or residual resources explicitly.
Before retry, establish completion/idempotency/repeatability within approved
scope; if uncertain, stop for an orchestrator/user decision rather than repeat a
payment, create/delete or consume the same data again.
Remote observation and cleanup need authorization and precise run-owned resource
scope. No automatic rollback, broad deletion or new business operation to "reset"
the run. Return actual cleanup results/failures and remaining uncertainty separately
from process termination and test status. This does not reset the bonus budget.
