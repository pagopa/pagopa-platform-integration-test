# QA engineer activity and implementation workflow

This is the mandatory entry for direct user requests, orchestrator assignments
and runner fixes. It implements ADR-14 through ADR-19. Branch routing remains
the orchestrator's responsibility; this workflow authorizes no Git operations.

## Activity routing (ADR-14)

| Activity | Behavior | Allowed output |
| --- | --- | --- |
| Review | Apply review-behave-steps directly when already QA-engineer; never self-delegate | Findings in chat and an explicitly requested Markdown report at an agreed path; no code or feature writes |
| Implement or extend | Require the implementation input contract, reuse existing bindings, implement authorized behaviour | Scoped step/binding and necessary suite-hook edits |
| Fix or refactor | Establish the defect or preservation goal and authorized files before editing | Scoped corrections preserving unrelated behaviour and coverage |

Use explicit intent without redundant permission questions. Ask if the activity,
files, expected behaviour or scope is ambiguous. Supplied files alone do not
authorize editing. A review never becomes a fix without an explicit activity
change. Explanation-only requests remain in chat.

Review can examine incomplete code or draft features without passing the
implementation readiness gate. Findings must distinguish proven code defects,
missing functional evidence and suggestions. No corrected copies of code may be
created during review. Report permission is not permission to write UCs, skills,
instructions, execution config, ACE files or implementation code.

## Input and functional boundary (ADR-15)

For implementation receive the current feature paths/contents, analyst explanation,
per-feature readiness, suite type/framework, target files, approved scope and
ownership. Check these even when invoked directly, not only through an orchestrator.
For UC features, consume current registry/report readiness; do not reconstruct
requirements from Python or silently use stale/draft artifacts.

Stop affected implementation on unresolved functional requirements, oracles,
required setup/data, TODO placeholders or contradictory inputs. Ask the user or
return the gap to the orchestrator for QA-analyst; do not edit the feature,
choose an expected result, substitute plausible data, or turn placeholders into
runtime defaults. A ready subset requires explicit scope authorization.

For a fix, obtain the failing scenario, actual error/traceback when available,
expected behaviour and target scope. A clearly described static defect does not
require fabricating a failed run. For a refactor, identify behaviour and public
bindings to preserve. Existing-test maintenance does not require a new UC run,
but unresolved requirements remain blockers. Never use `pass`, unconditional
success, skipped assertions, broad exception suppression, weakened checks or
disabled scenarios as a completion shortcut.

## Suite context and reuse (ADR-16)

Read the Python instructions and, for step/binding/hook work, the Behave
instructions and profile. Confirm the actual framework: Behave bindings,
pytest-bdd fixtures and Playwright automation are not interchangeable.
Playwright can be used inside Behave without changing its binding framework.

For an existing suite, use its own loading rules, hooks, matcher, context lifecycle
and conventions; do not require a second blueprint choice merely because none
was passed. For a new suite, find compatible technical references and ask only
if the choice or missing conventions materially affects implementation.
Blueprints supply technical patterns, not product requirements or expected values.
Do not copy another suite's environment assumptions or data.

Inspect the shared utility documentation listed in the profile and applicable
module APIs before adding logic. Resolve local utility paths with the actual
`<test-type>` and `<suite>`; never place API/E2E helpers under integration by default.
Inspect the full relevant loaded step scope for reusable definitions and matcher
collisions, not only the feature's proposed new file.
Apply [Behave coding conventions](../../../.github/instructions/behave-steps.instructions.md)
(ADR-38 through ADR-43): organization follows cohesive suite responsibilities,
binding checks include kind/matcher/conversions, and context/reset/cleanup respect
actual lifecycle scopes. Profile paths guide reuse/new helpers, not automatic
legacy migrations. Preserve full logical assertions and structured input
semantics, with bounded observation waits and safe diagnostics. These conventions
do not expand writing or execution permissions.

## File and utility ownership (ADR-17)

QA-engineer owns authorized step definitions, bindings, assertions and necessary
suite wiring in `environment.py` or equivalent hooks. Hook edits must be within
scope and respect existing cleanup/context lifecycle; new targets require scope
confirmation. Do not turn hooks or step files into a reusable utility layer.

Python-utility-engineer owns new reusable helpers and changes to existing utility
modules, both suite-local and shared `src/utility`. Call existing documented APIs
directly when sufficient. Delegate only a concrete missing utility change, with:

- Exact owned paths and requested API/signature.
- Supported behaviour, inputs, expected outputs/errors and compatibility needs.
- Existing helpers considered and why they do not suffice.
- Relevant unit-test cases and integration expectations.

The specialist returns API, files, compatibility impact, tests written and checks
actually performed. Integrate its result only after reading the changed API.
Use its [utility workflow](../python-utility-engineer/implementation.md) contract:
include relevant consumers and error/compatibility expectations, preserve exact
ownership including exports/tests, and resolve any breaking-change migration.
An incompatible remaining caller is an integration blocker, not a completed fix.
Do not independently change the same utility files, duplicate a helper inside
steps, or broaden a specialist assignment to avoid ownership rules.
If delegation is unavailable, report the dependency instead of silently taking over.
New dependencies or execution/configuration changes outside approved wiring are
returned to the orchestrator for authorization.

## Collision-free scheduling (ADR-18)

Before parallel assignments, the orchestrator establishes exact write ownership
for step files, `common_steps.py`, hooks, utility files and related tests.
One worker per feature is allowed only when write sets are disjoint.
Group overlapping work under one owner or serialize it; shared files have one
writer. Include shared context attribute names, lifecycle/reset rules and
binding/matcher conventions in each assignment so file-disjoint edits do not
introduce semantic collisions.

An engineer receiving overlapping ownership or discovering a new common-file
dependency returns it before editing that file. The orchestrator resolves it
and collects the integrated result before asking the runner to execute.
Perform a final read-based check across the loaded suite for duplicate/overlapping
decorators, parameter conversions, shared context leakage and hook integration.
Matching patterns may overlap even when decorator text is not identical.
Do not claim that static inspection proves runtime binding uniqueness.

## Validation and return (ADR-19)

QA-engineer does not execute tests, shell commands, system/API probes or package
installation. Use read-based static inspection and actual editor diagnostics;
do not claim compilation, imports or a parser ran when they did not.
Python-utility-engineer writes relevant unit tests but does not run them.
The runner receives the proposed targeted unit/application checks and executes
only after the existing command-approval gate. A broader/different command needs
the corresponding approval; no indirect test execution through delegation.

Return:

- Activity result: `review-complete`, `implemented-not-run`, `partial` or `blocked`.
- Actual changed/reviewed paths, step-to-binding coverage, reused APIs, hook/context
  impact, utility dependencies and compatibility concerns.
- Checks actually performed, tests proposed but not executed, unresolved issues
  and the exact verification scope for the runner.
- Actions, outcome, lessons and friction for the current ACE request, separately
  from Jira and any persistent UC identity.

Only the orchestrator chooses downstream QA execution/closure, apart from the
runner's existing authorized fix-loop resumption. A direct invocation returns
to the user without starting runner/closer. No commit, push, PR or implementation
success is inferred from static inspection. The engineer and utility specialist
do not write ACE trace files; the engineer relays actual specialist work without
inventing a participating ACE identity for an unconfigured agent.
