# QA orchestrator operations (ADR-26 through ADR-31)

Read this complete workflow before operational delegation or substantive planning.
Use [session routing](session-routing.md) for branch choices and Git transitions;
session mode and requested activity are independent. This workflow does not
authorize execution, editing or publication merely because a branch was selected.

## Activity routing (ADR-26)

Determine intent, scope and requested stopping point from the user. Ask through
the dedicated question tool only where ambiguous; show a concise plan before
delegation. Collect a suite name only where needed for the actual work. Keep the
selected branch; new-suite work does not independently require a second branch.

| Requested activity | Entry and route | Stop boundary |
| --- | --- | --- |
| Explain or explore | Answer directly; use a bounded specialist only when necessary | Requested answer/plan, no automatic implementation |
| Review features | QA-analyst in review mode | Findings and only a requested report, no corrections |
| Review Python steps | QA-engineer in review mode | Findings and only a requested report, no corrections |
| Create or edit features | QA-analyst with applicable sources/skills | Authorized feature output and per-feature readiness |
| Implement or fix test code | QA-engineer with current readiness or concrete existing-defect evidence | Integrated implementation and actual static checks, not inferred test success |
| Diagnose or execute tests | QA-runner in the requested mode | Actual evidence/report, no implicit implementation or closure |
| Documentation or publication closure | QA-closer for the exact authorized task and its applicable evidence gates | Requested documentation/publication result |
| Complete suite work | Analyst when requirements/features need work, engineer when implementation needs work, runner for approved verification; closer only if needed | Agreed end-to-end result within current authorizations |

Do not always start with the analyst: a concrete technical defect, Python review,
existing-suite execution or closure-only request can enter its actual owner.
Functional requirements/scenario changes or uncertainty return to the analyst.
Providing documentation for discussion alone does not start feature creation.
A combined review/correction request authorizes only its explicit correction scope.
If a request expands beyond exploration, reapply session routing before changes.

## Delegation and recovery contract (ADR-27)

Give each delegated task:

- Objective, activity mode, deliverable and explicit stopping point.
- Exact read/write scope, owned files, shared-file/resource owner, baseline and
  pre-existing edits to preserve; read-only means no corrected copies.
- Current inputs/evidence and their provenance, requirements/readiness or existing
  defect evidence, suite/framework/environment where relevant.
- Distinct Jira association, stable UC identity when applicable and current ACE
  request ID. No fabricated participation for an unconfigured specialist.
- Current approvals/refusals and constraints, permitted effects, dependencies,
  remaining bonus/diagnostic budgets and prior completed actions.

Validate the return against that assignment. Retain specialist-specific result
labels; summarize coordination as completed, partial, blocked or delegation
failed/interrupted. A successful tool/agent return alone proves no artifact,
execution or publication. Use actual returned evidence; resolve missing scope,
contradictory output or unverifiable claims without repeating successful work.

An interrupted delegate may have saved partial changes: do not blindly relaunch
against its files or give a second agent the same ownership. Establish whether
the original writer/process is still active, reconcile actual artifacts and
release/transfer ownership before resuming. Preserve user/unrelated edits.
Never reset/stash/discard changes to recover a delegation.

Maintain a concise in-context checkpoint: current branch/activity/scope, completed
outputs, remaining work, blockers, approvals, budgets, active writers/processes
and prior publication/ACE stage. No mandatory new tracking file. When context is
missing, reconstruct from available evidence and ask only about unresolved facts.
On resume recheck relevant current branch, contents, evidence and permission;
restart at the last established step, not automatically at the first agent.
Independent chat requests get a new ACE ID; continuation keeps its existing ID.

## Authorization precedence (ADR-28)

The latest explicit applicable decision supersedes an earlier one for the same
action/scope. An earlier PR request does not survive a later "do not open a PR".
Preserve independent `commit`, `push`, `create_pr`, execution and fix decisions,
including unresolved values. No success condition sets `create_pr: true` implicitly.

Pass the updated decisions to every affected delegate. If a decision changes
while work is active, stop future affected actions, notify the delegate and
establish what already happened; do not claim a completed push/PR was undone.
Ambiguous revisions require clarification, not silently treating them as consent.
Never ask again merely to overturn an explicit refusal.
Reusing consent requires the same still-valid scope/environment/effects and
destination; a broader or changed plan needs its own decision. Generic approval
does not waive runner command approval, specialist readiness or Git safety gates.

## Analyst-result gate (ADR-05)

Use the [analyst activity/result contract](../qa-analyst/activity-routing.md#results-and-implementation-boundary-adr-05).
Only the orchestrator chooses downstream work; review/edit-only requests end at
their requested boundary. Do not start another stage simply because files exist.

- Require explicit `ready-for-development` for new/changed feature implementation.
  `changes-complete` or `review-complete` is not readiness.
- For UC output require current registry/reports/feature rows in `ready` state;
  the final report says `pronta per lo sviluppo`. Filenames, old summaries or
  missing TODO tokens do not prove readiness.
- For mixed output, the user explicitly
  authorizes that partial implementation scope before a ready subset proceeds.
- Preserve runner approvals; diagnostic
  permission for existing tests is not permission to execute draft scenarios.
- Existing test-code maintenance can use concrete defect evidence under the
  engineer's gate without manufacturing a new UC or analyst stage.

## Engineer ownership and result gate (ADR-14 through ADR-19)

Use the [engineer workflow](../qa-engineer/implementation.md). Assign exact write
sets and current functional/defect evidence, not just a feature filename.
Parallelize only disjoint ownership; group or serialize overlapping work,
including shared steps/hooks/utilities/unit tests and nested utility assignments.
One shared file has one writer. After integration assign the suite-wide
binding/context collision check; static inspection is not runtime verification.

Keep `review-complete`, `implemented-not-run`, `partial` and `blocked` distinct.
Resolve incomplete dependencies before normal verification; limited diagnostics
need explicit scope/approval. Pass actual changed paths, binding/utility impact,
known issues and proposed checks to the runner. Utility-specialist unit tests
are executed by the approved runner, not by implementation agents indirectly.
Direct or scoped implementation is not automatic permission for execution.

## Runner activity and plan gate (ADR-20 through ADR-25)

Use the [runner workflow](../qa-runner/execution.md). Pass requested mode, current
integrated contents, suite/framework/environment, verification scope and failure
policy. The runner obtains approval for exact commands, selection, setup/effects,
unique artifacts and rerun limits; orchestrator intent is not that approval.
Same-plan reruns may reuse consent, material changes need fresh approval.

The first failure is attempt 0, followed only when authorized by up to five bonus
fix attempts. Keep its counter across delegations and resumptions; separately
approved finite diagnostic reruns do not reset/extend it. Allow direct reporting
without fixes or stopping early; never restart the loop automatically.
Test-code defects go through engineer ownership, functional changes through the
analyst, environment/configuration/service issues through an explicit scoped
orchestrator decision. Do not authorize a test-code workaround for an unclear oracle.

Consume `passed`, `failed`, `blocked` and `inconclusive` as defined by the runner.
Zero failures alone, zero executed cases or unexplained flaky retries do not
establish blanket success. Execution-only/diagnosis requests do not auto-start
implementation/closure. Reuse the relevant unresolved-suite-error report even
when the fix loop never started.

## Evidence dependencies and safe parallelism (ADR-29)

Associate evidence with the inputs/contents and selection it actually covers;
matching HEAD alone is insufficient. Before each dependent stage, compare current
relevant artifacts/changes to that baseline. If relevance is uncertain, resolve
it rather than presuming everything stale or everything valid.

| Change or dependency | Required reassessment |
| --- | --- |
| Requirements, oracles or scenarios | Analyst readiness and affected coverage/bindings; apply UC invalidation rules when applicable |
| Steps, hooks, helpers, dependencies or execution configuration | Affected implementation and runner verification; shared changes may affect multiple features/suites |
| Descriptive documentation only | Assess README/documentation impact; do not indiscriminately invalidate tests |
| Partial selection, unknown baseline or missing artifacts | Explicit coverage limitation; no whole-task passing claim |
| Shared external test data, accounts, service state or consumable resources | Establish isolation/repeatability and effects before concurrent execution; serialize if unsafe or uncertain |

No downstream gate may reuse evidence invalidated by a relevant change. Assign
targeted fresh checks to the owner/runner; do not demand full-repository execution
when scoped checks suffice. Do not run verification concurrently with relevant
writers unless the approved isolated snapshot is explicit and reported.
File-disjoint engineers do not imply safe parallel suite execution.

## Completion and closure handoff (ADR-30, ADR-08 through ADR-13)

End every requested activity with actual results, changed/produced paths, checks
performed, unexecuted checks, coverage limits/blockers and next safe actions.
Activity completion is not publication. Stop at the requested boundary.

After a coherent repository change set, apply the
[README gate](../../../AGENTS.md#readme-maintenance-gate-adr-11) and
[ppa-readme](../../../.github/skills/ppa-readme/SKILL.md), even without a commit.
Reuse a current assessment; restricted agents return requirements for an
authorized writer. The orchestrator may make explicitly authorized planning/
README edits, not test code/features. Do not expand another role's permissions
or run tests because README assessment occurred.

Invoke QA-closer only for an actual assigned documentation/report-completion or
authorized publication task, not merely because another agent succeeded.

## Closure handoff (ADR-08 through ADR-13)

Pass
the [closure input contract](../qa-closer/closure.md#closure-input-contract-adr-08):
expected branch and file scope/work type, current verification including tested
working-tree contents, artifacts/limits, current independent `commit`, `push`
and `create_pr` decisions, README assessment and prior publication state.
Use explicit unknown/not-applicable rather than inventing evidence.

For publication supply an exact English message from current scope/user intent;
for full suite work `test: <suite-name> tests complete` or
`test: <suite-name> tests updated <fix semantic>` are examples, not substitutes
for an explicit user message or factual scope. Preserve skill/trailer rules.
No merge/force push/amend or implicit Git action.

With unresolved suite errors, reuse the runner's report; request report-only
closer work only for a real missing/incomplete report, never to bypass evidence
gates. Non-suite/tool/Git blockers do not invent a suite error report. Successful
work needs no standalone success report. Documentation-only closer work does not
authorize publication and must not require invented executed-test evidence.

## QA result and ACE lifecycle (ADR-31)

The orchestrator owns capture; specialists return trace elements, not trace files.
Before capture read the schema and capture guide listed in the persona. Capture
only actual configured participants under the same request ID, plus the
orchestrator's substantive work. Assess friction and evidence deliberately.

Track QA result separately from ACE completion: pending capture, captured,
privacy-finalized, counters/threshold checked and reflection delegated when due,
or blocked at the actual failed stage. These are coordination notes, not new ACE
schema enums. A privacy failure does not turn a genuinely passed run into a test
failure, but the overall lifecycle is not complete; return both statuses honestly.

After all traces (including closer's) are captured, run the project privacy addon
before counters, thresholds, reflection or trace publication. Stop ACE processing
on failure; never consume/commit raw traces or call the core finalizer directly.
Report the failed command/stage without exposing private trace content.

Recovery uses the original request ID and established stage, not a new QA loop.
Inspect actual persisted state and applicable addon/script recovery guidance
before retrying; do not blindly repeat a possibly completed counter/reflection
action or overwrite finalized traces. If safe replay cannot be established,
report the blocker and obtain a recovery decision. Amend later assessments only
through the capture guide's separate correction-trace procedure.
Do not change runtime/scripts/playbooks or install addon dependencies implicitly.

The closer's trace is captured after its result: privacy-finalize
those through the existing ACE lifecycle afterward. Never require it inside the
commit it describes, initiate a recursive commit, or automatically
publish newly captured traces. Only sanitized, explicitly scoped traces can be
included in an authorized later publication.

Before final response verify claimed persistence/command results and distinguish
actual outputs from proposals. On ACE failure preserve QA results and recover
only the blocked lifecycle stage; do not rerun tests, commits, pushes or PRs.
Only gh/ace/warden applies playbook changes after explicit human sign-off.
