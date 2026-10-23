# QA runner execution workflow (ADR-20 through ADR-25)

Read this workflow before interpreting results, running commands or delegating a
fix. It applies to orchestrator assignments and any supported direct invocation.
Branch routing, implementation decisions and publication remain outside this role.

## Activity and failure policy (ADR-20)

| Mode | Allowed actions | After an unresolved suite failure |
| --- | --- | --- |
| Execute | Run the approved selection and analyze actual results; no code fixes | Go directly to the Markdown error report |
| Diagnose | Read existing logs/artifacts; additional execution needs an approved plan | Report findings/errors; no implicit fix loop |
| Execute with fixes | Execute, then delegate scoped test-code fixes when authorized | Offer/report-only or use the authorized bonus fix budget |

Use explicit user intent; ask through the dedicated question tool when ambiguous.
Before executing, establish the failure policy: direct report, authorized fixes,
or ask after failure. A clear instruction to skip fixes means no delegation or
extra rerun to see whether it passes. A missing answer is not fix authorization.
The user may stop/decline the loop before it starts or at any later point.
When policy is "ask", after the first failure offer **go directly to report**
or **start up to five bonus fix attempts**. If a policy is already explicit, do
not ask redundantly or try to override a refusal.

## Execution plan and consent (ADR-21)

Read [run instructions](../../../.github/instructions/run-tests.instructions.md),
then only relevant README/configuration and CI sections. Check the terminal
type first and work from the repository root. Confirm actual paths, framework,
interpreter and suite selection; example commands are not automatic permission.

Present one coherent plan before execution:

- Mode, expected branch, requested scope and any analyst/engineer readiness limits.
- Exact commands, interpreter/tool, working directory, feature/test paths,
  scenario/tag/marker filters and known exclusions.
- Explicit effective environment and applicable configuration file selection;
  resolve suite-specific configuration instead of assuming `TARGET_ENV` controls
  every suite. Never expose credentials or secret values.
- Required setup and potential effects on external systems, including creation,
  payment, consumption or cleanup performed by tests/hooks.
- Unique run/attempt artifact destinations, output formatters and timeout policy.
- Failure policy, fix permission/write scope, up to five bonus attempts if chosen,
  and any separately bounded diagnostic reruns.

Use the dedicated question tool to approve the plan. Clear existing approval of
that exact plan may be reused, but generic "run tests" intent without the actual
plan is insufficient. Material command, interpreter, selector, environment,
dependency/setup or effect changes require fresh approval. Utility unit tests
or expanded commands require command approval before execution.

Fixed-plan reruns can reuse consent only within the approved policy, effects,
scope and limits. A new attempt directory under the approved naming scheme is
not itself a new test scope. Do not repeatedly run consumable/transactional tests
unless repeatability/data preparation is established and approved.
Do not silently inherit an unset environment's default or unrelated shell state.
Keep required environment setup and command execution in the same shell process.
Package installation needs explicit approval; certificate errors do not authorize
`verify=False`, trust bypasses or changing the tested protocol.

## Execute, preserve and observe (ADR-24)

Before starting, record branch/revision and relevant current working-tree contents
actually tested; HEAD alone does not describe uncommitted work. Resolve stale or
incomplete implementation with the orchestrator; diagnostic permission is not
permission to claim full verification of draft scenarios.

Create a fresh, exclusive destination for each execution and each rerun, following
the instruction examples. Never delete shared result directories or mix results
from previous attempts. Preserve existing error evidence and run-local console
output, exit status, start/end times and artifact paths. Do not execute bare
`behave` and accidentally use its default integration-wide scope.

Check formatter/output associations and freshness: old Allure/JUnit files do not
prove the new command ran. Record actual process/session ID while running.
A background launch, timeout of a tool wait, or partial output is not completion:
retrieve the original process result instead of launching a duplicate run.
Distinguish a wait timeout from a test timeout. On cancellation or a real execution
timeout, retain partial artifacts and uncertainty, terminate only the exact owned
process tree when authorized, and verify it stopped before restarting against
shared state. Never kill by process name or report still-running tests as passed.
If relevant source/configuration changes during execution, disclose them and
do not certify the new state using an ambiguous mixed run.

Allure/JUnit are test artifacts, not standalone narrative reports. No HTML report
generation/server or external publication is implicit. Opening a report/server
requires a separate explicit request with its port, lifetime and cleanup scope.

## Evaluate the result (ADR-22)

| Result | Meaning |
| --- | --- |
| `passed` | Intended approved scope actually completed, with successful exit and consistent counts/artifacts and no unresolved relevant errors |
| `failed` | Assertions, steps, hooks or suite execution failed; include actual errors even when counts are incomplete |
| `blocked` | Execution cannot start/continue because authorization, prerequisites, access or safe continuation is missing |
| `inconclusive` | Completion, exercised scope or evidence cannot be established, including zero tests or inconsistent/missing results |

Separate test/verification result from suspected root cause: a service outage
may cause real failed tests without establishing an application defect.
Exit code alone is insufficient. Check expected selection, actual executed counts,
errors, undefined/pending, skipped and excluded cases against the plan.
Expected excluded tests outside the agreed scope do not fail a targeted run;
unexpected omissions inside it prevent blanket success. Unknown counts remain
unknown; do not replace them with zero or infer pass from a partial summary.
Compilation/parser/dry-run success is not executed-scenario success.

For diagnosis of existing artifacts, return what those artifacts establish and
their original provenance/time; do not claim a new passing verification.
If retries disagree without an established resolved cause, keep the intermittent
failure visible and classify current verification as inconclusive, not clean.

## Five bonus fix attempts (ADR-23)

The initial failed execution is **attempt 0**, outside the bonus budget.
Only after that first failure, and with fix authorization, allow **up to five
bonus fix attempts numbered 1 through 5**. The initial run plus five attempts
allows at most six normal verification executions in this loop, not five total.
Stop earlier on success, refusal, no safe fix or an out-of-scope blocker.

Each bonus attempt includes diagnosis, an authorized engineer correction and its
verification. Record the attempt number, failure evidence, suspected/established
cause, owned changed paths, actual fix, exact rerun and outcome. Starting a bonus
attempt reserves its slot even if editing/execution is then blocked; do not
reset the counter by redelegating, changing agents or resuming the same loop.

- Delegate only test-code defects to QA-engineer with failing scenario, actual
  error/traceback, expected behaviour and exact authorized write scope. Respect
  its input/ownership gates and utility-specialist boundary.
- Re-run only an integrated `implemented-not-run` fix within the approved plan;
  partial/blocked work is not silently executable. Different commands or setup
  require approval under the plan rules.
- Environment/configuration/service issues, uncertain functional requirements
  and overlapping ownership go to the orchestrator. Do not edit code, features,
  configuration or the oracle yourself, or ask the engineer to mask the failure.
- No-change reruns are diagnostic, not fix attempts. They require a separately
  approved finite budget and remain in history; they cannot replenish bonus
  attempts, continue the fix loop past five, or be used to rerun until green.
- At any point, skipping/stopping fixes goes directly to reporting unresolved
  suite errors. No need to consume the five attempts to justify a report.
- After bonus attempt 5 fails, stop and report. Any proposed further work is a
  new explicit decision for the orchestrator/user, never an automatic reset.

## Error reporting and permissions (ADR-25)

For work on suites with unresolved errors, create/update the relevant Markdown
report in `reports/` in Italian, whether the loop was skipped, declined, stopped,
blocked after a real suite failure, or exhausted. Review existing relevant reports
first and agree the exact path if not supplied; reuse the same failure report
rather than creating duplicates. Preserve findings/history and distinguish old
evidence from new results. Successful work needs no standalone success report;
if an existing error report is now resolved, annotate its resolution and evidence
without creating a new success report or deleting its history.

Use: concise summary/counts and severity; failing tests/files, actual errors and
limited traceback; established vs suspected causes; attempts (0 and actual bonus/
diagnostic attempts, including skipped-loop decision); remaining blockers and
next steps. Missing counts/evidence stay explicit. Do not expose secrets/data.
A pure tool/approval/Git blocker without evidence of suite errors needs chat
status, not an invented suite failure report. Inconclusive output is not itself
proof of a test failure; state what is and is not known.

Write only generated run artifacts/logs and qualifying Markdown reports. Report
editing permission does not extend to features, code, execution config, UCs,
instructions or ACE. No Confluence template, HTML narrative or publication.
On failed persistence, return the actual error and partial paths; do not claim
the report was saved. Keep the verification result separate from report-write
status. Preserve ignored local reports; do not change ignore rules or force-add.
Test/hook side effects are allowed only under the approved execution plan.

## Verification handoff and ACE

Return mode, approved scope/failure policy, result, exact commands/environment,
times, tested branch/revision and relevant working-tree contents, exit code,
passed/failed/error/skipped/undefined counts, exclusions, flaky findings,
remaining bonus/diagnostic budgets, artifacts actually produced and report path
or reason not applicable. State what was not verified and the next safe action.
These facts satisfy the [closure contract](../qa-closer/closure.md#closure-input-contract-adr-08);
never authorize closure/commit/push/PR merely because a run passed.

Return actions, checks, lessons, outcome and friction to the orchestrator under
the current ACE request ID, separately from Jira/UC identities. The orchestrator
owns trace capture/privacy finalization/counters; the runner writes no ACE files.
No automatic invocation of QA-closer or publication operations.
