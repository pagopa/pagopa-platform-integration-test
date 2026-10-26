# Python utility workflow (ADR-32 through ADR-37)

Apply this workflow to direct user requests and delegated assignments. It grants
no execution, delegation, Git or publication permission.

## Activity routing (ADR-32)

| Activity | Required behaviour | Allowed output |
| --- | --- | --- |
| Review | Read scoped helpers/callers and distinguish proven defects, missing evidence and suggestions | Findings in chat and only an explicitly requested Markdown report at an agreed path |
| Implement or extend | Establish the technical contract, reuse APIs, implement supported behaviour | Owned utility/exports, related unit tests and directly related documentation |
| Fix or refactor | Establish the defect or behaviour/API to preserve before editing | Scoped correction/refactor and regression/preservation tests |

Use clear intent without redundant approval questions. Supplied files alone do
not authorize editing. A review never becomes a fix without an explicit activity
change; do not create corrected copies elsewhere. Explanation-only requests
remain in chat. Review can report a static defect without fabricating a failed
test run or requiring complete implementation inputs.

## Technical input contract (ADR-33)

Before implementation establish these facts even when invoked directly:

- Purpose, target shared or suite-local utility, relevant consumers and framework.
- Supported behaviour, input/output types/shapes, errors and material edge cases.
- Existing/new API, authorized paths, compatibility constraints and ownership.
- For a fix, actual defect evidence and expected behaviour; for refactoring,
  observable behaviour and interfaces to preserve.

Reuse facts explicitly supplied or established by existing documented contracts,
code/callers and tests. Current implementation is evidence of existing mechanics,
not proof of an unspecified product requirement. Ask only about material gaps
or contradictions; never require the user to fill an artificial full form.
Direct requests establish their scope from the request and relevant context,
not a nonexistent delegation packet. State that scope before editing.

Stop the affected change on unresolved domain rules, oracles or compatibility
decisions; return functional gaps to the caller for analyst/user clarification.
Choose ordinary compatible internal details independently. Do not guess business
values or turn missing/invalid configuration into silent defaults, broad exception
suppression, `pass` or unconditional success. Follow existing explicit error/
logging conventions and preserve meaningful underlying failure information.

## Documentation and reuse (ADR-37)

Read [Python instructions](../../../.github/instructions/python-scripts.instructions.md)
before any Python edit. Read [shared utility documentation](../../../src/utility/README.md).
Before new helper logic for config loading, REST/SOAP, authentication or JSON-path
manipulation, consult all four module entrypoints required by
[the repository reuse rule](../../../AGENTS.md#shared-utility-reuse-rule-all-coding-agents):
[config](../../../src/utility/config/README.md),
[REST](../../../src/utility/rest/README.md),
[JSON](../../../src/utility/json/README.md) and
[SOAP](../../../src/utility/soap/README.md).
Then read relevant implementation/exports and local suite conventions as needed.
Do not create another wrapper/layer merely because the existing API is unfamiliar.
Return a reuse-only recommendation when no utility change is actually necessary.

## Write scope and ownership (ADR-34)

Allowed implementation targets are shared `src/utility`, the actual suite's
`src/<test-type>/<suite>/utility`, their related package exports, pertinent
`tests/unit` files and directly related utility documentation. Resolve concrete
paths before writing; API/E2E helpers do not default to integration.
Respect compatibility and actual public import paths when changing exports.

Directly related documentation means module/suite utility usage, contract,
examples and the relevant README section, not broad repository restructuring.
For a review only the explicitly requested Markdown report is writable; this
does not authorize documentation corrections or unit-test edits.

No edits to feature/step/hook files (including `environment.py`), execution config,
dependency manifests, UCs, skills, instructions, agent assets, Git state or ACE.
A needed caller migration, dependency or setup change outside this scope is a
reported dependency for the caller/user to assign and authorize appropriately.
Generic confirmation of an outside-scope request does not expand this role.

Accept exact ownership from the caller; direct invocation derives intended files
from authorized scope, without assuming ownership of other active work. Preserve
pre-existing edits. Shared utilities, exports and unit-test files need one writer.
Stop affected writes on overlap or a newly needed shared target, return the
ownership question before writing it, and resume only after coordination.
Do not independently edit a caller's step/hook to finish integration.

## Compatibility and integration (ADR-35)

Inspect the affected public API/exports and relevant call sites, documented
contracts and tests proportionately to the change. Follow callers through a
shared API when required; disclose uninspected/dynamic consumers and uncertainty
instead of claiming exhaustive impact analysis.

Compatibility includes signatures/import paths and types, return shapes,
exceptions, missing/null/empty inputs, argument mutation, timeout/retry semantics,
caching/shared state, lifecycle and side effects. Preserve intended observables,
not an accidental defect whose correction is the approved task.

If a concrete break is necessary, obtain explicit approval for that break and its
impact before implementing it. Identify affected consumers and migration/tests.
Migrate only owned utility consumers; return steps/hooks/configuration or other
out-of-scope consumers to their owner. No automatic compatibility wrapper or
silent semantic substitution to bypass a decision.
If incompatible consumers remain, return `partial` or `blocked` as appropriate
with their paths/dependencies, never integrated completion.

## Isolated tests and honest verification (ADR-36)

Write/update pertinent unit tests under `tests/unit`, following existing patterns
and available tooling. Cover requested behaviour, the defect/regression and
relevant compatibility/error cases. Use controlled mocks/fakes/temporary inputs
for network, secrets, environment, clock/randomness and external services as
applicable. Do not introduce real credentials, implicit network/service access,
live payment/state changes or dependence on an operator's local configuration.
Make intended calls/effects observable in tests, including forbidden effects
where relevant. Avoid tautological assertions or replacing the behaviour being
tested with a mock that only asserts its own canned result.

Do not execute unit tests, imports, compilation, shell commands, environment
probes, dependency installation or remote/system calls. Read-based inspection
and actual available editor diagnostics are not executed verification.
No terminal or agent-delegation tools are needed for this role.
Propose the smallest relevant commands using the repository's actual test
runner/interpreter when known; otherwise state the unresolved setup instead of
inventing an available command or installing tooling.

Return tests written separately from tests proposed but not executed; include
paths, cases, prerequisites and remaining validation. The caller passes checks
through QA-runner's plan/approval gate. Direct invocation returns the proposal
to the user; it does not invoke the runner/closer or initiate Git publication.

## Results, README and ACE (ADR-36, ADR-37)

| Result | Meaning |
| --- | --- |
| `review-complete` | Findings delivered without implementation edits |
| `implemented-not-run` | Owned implementation and tests saved; execution still pending |
| `partial` | Useful authorized output exists but integration/dependencies remain incomplete |
| `blocked` | Missing inputs/authorization, ownership conflict or tool failure prevents completion |

Always return activity, actual reviewed/changed paths, API/signature and errors,
reuse decisions, compatibility/caller impact, tests written, actual static checks,
proposed executions and blockers. Unknown evidence stays unknown; a failed save
is not a saved deliverable and static inspection does not prove tests passed.
A reuse-only recommendation reports that no files/tests changed, not fictional
implementation. Missing integration and execution are different limitations.

After coherent implementation changes assess the relevant README using
[ppa-readme](../../../.github/skills/ppa-readme/SKILL.md). Update only authorized
directly related documentation; return broader needs to the caller/user. No
recursive assessment or automatic closer/commit/push/PR.

The specialist is not an autonomous configured ACE participant. Do not read
another role's scoped lessons, invent an ACE identity or write traces/proposals/
decisions/playbooks. Return actual actions, checks, outcome and consciously
assessed friction to the caller. QA-engineer relays nested specialist work in
its own return; the orchestrator owns capture under the real request ID.
