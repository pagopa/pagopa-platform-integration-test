---
applyTo: src/**/steps/**/*.py

---

# Behave Step Definitions Guidelines

These instructions apply to Python files containing behave step definitions.
Read [the Behave profile](../../.github/profiles/behave-steps.profile.yaml) before
editing and follow [Python instructions](python-scripts.instructions.md).
These are coding conventions, not permission to edit, execute tests, change
requirements or exceed the active role's ownership.

## Step file organization (ADR-38)

- Organize bindings by coherent responsibility/capability and existing suite
  conventions. A small cohesive suite may use one step file; split when size,
  cohesion or maintenance warrants it, not to satisfy a file-count rule.
- `common_steps.py` and scenario-numbered files are optional conventions.
  A filename or scenario tag does not restrict the binding's loaded visibility.
- Prefer grouping Given/When/Then where readable; do not sacrifice cohesion or
  refactor unrelated files merely to reorder functions.
- Preserve public step text and consumers during file moves/refactors unless
  the concrete change is authorized. Do not rename/reorganize unrelated files.

## Binding compatibility (ADR-39)

- Inspect the actual loaded binding scope, imports/shared registrations and
  existing consumers before adding or changing a decorator.
- Check step kind (`given`, `when`, `then`, or generic `step`), active matcher,
  parameter names/conversions and function signature together. Different
  patterns can match the same step; identical text under Given and When can be
  intentional. Consider generic `step` registrations across kinds.
- Preserve the suite's matcher/converter conventions. Do not globally change
  `use_step_matcher` or type registrations to solve a local binding problem;
  changes affecting other bindings need explicit scope and impact assessment.
- Parameterize only when behaviour and conversions remain compatible; inspect
  affected feature usage, including outlines, rather than generalizing blindly.
- Static inspection can identify collision risks, not prove runtime uniqueness.
  Return proposed runtime checks through the active role's runner approval gate.
- Shared bindings, hooks and registrations have one write owner. Report new
  overlapping dependencies before editing; one feature is not one isolated scope.

## Context lifecycle and cleanup (ADR-40)

- Identify context attributes produced/consumed by the changed bindings and their
  intended scenario/feature/run lifetime. Respect Behave's context scopes and
  the suite's existing hook lifecycle; do not indiscriminately clear `context`
  or overwrite framework-managed attributes.
- Keep scenario state on its intended context layer, not module globals, mutable
  class state or default arguments shared across scenarios. Treat each Scenario
  Outline row as an independent scenario; never rely on scenario execution order.
- Distinguish resetting data from releasing browser/session/file/external
  resources. Use the suite's supported cleanup mechanisms within authorized
  hooks/ownership, including failure paths and partial initialization.
- Preserve the original test failure when cleanup also fails, but report the
  cleanup error explicitly; do not swallow either or fabricate successful cleanup.
- Do not move lifecycle management into arbitrary steps. Required hook or shared
  lifecycle changes must follow the engineer's authorization/ownership contract.

## Profile resolution and shared utility reuse (ADR-41)

- Resolve profile paths from the repository root, not the instruction directory
  or an assumed terminal working directory. Read each explicit README listed in
  `shared_utility_documentation` before coding; reuse documented utility APIs.
- A missing, malformed or unreadable profile/required document is an explicit
  blocker for dependent changes. Report the actual path/error and ask for
  resolution rather than inventing paths, silently skipping reading or scaffolding
  replacement documentation. Unaffected read-only findings can still be returned.
- Resolve `suite_utility_path_template` with the actual test type (`api`,
  `integration` or `e2e`) and suite. No unresolved placeholders or defaulting
  API/E2E helpers to integration. Validate the resolved target is the intended
  suite before writing; a new authorized utility directory need not already exist.
- The template guides new helpers; it does not require migrating existing legacy
  utility locations. Read and preserve actual existing public imports/conventions;
  a migration is a separate scoped decision.
- Use the current suite's hooks, configuration, binding and assertion conventions
  as the primary reference. Other suites are technical examples, not product
  requirements, oracles or evidence that their data/environment applies here.
- Ask about material behaviour, compatibility, ownership or path ambiguity even
  with a complete profile. Reuse established answers without redundant questions.
- New reusable helpers or utility changes follow active-role ownership; profile
  paths do not authorize the step engineer to edit utility modules directly.

## Assertions and structured inputs (ADR-42, addition)

- Keep each step focused on its described logical outcome, with all necessary
  assertions. Assertion count is not a target: do not weaken a multi-property
  requirement to obtain one assertion per step.
- Distinguish prerequisites, action and expected result. A Then must observe the
  relevant system outcome, not merely reassert a value the test itself prepared.
- Fail early on genuine prerequisites or unexpected response shape/status before
  dependent processing. Do not reject intentionally invalid input locally when
  the scenario requires sending it to exercise system validation.
- Handle decorator parameters, `context.table` and `context.text` according to
  the agreed contract. Validate required table headers/cells, all relevant rows
  and document formats; do not silently ignore input, replace missing data with
  guessed values, or confuse missing, null, empty and intentionally invalid data.
- Under [the Gherkin null contract](gherkin.instructions.md#null-inputs-adr-44),
  an empty Examples cell MUST become Python `None` in new/changed bindings.
  Behave substitutes raw empty text: ensure the matcher accepts it, then decode
  only the intended outline inputs before numeric/type conversion, request
  construction or assertions. Do not globally convert every empty string in
  context/tables/docstrings or use `value or None` (which also loses zero/false).
  JSON encoding preserves intentional `None` as `null`, not an omitted key or
  string. Keep explicit empty strings and absent fields distinct under the agreed
  representation; literal `null`/`None` text is not a universal sentinel.
  Propose targeted matcher/decoding/serialization regression checks, including
  a genuine empty cell and non-null controls. No bulk migration/parser patch.
- Preserve lexical values such as leading-zero identifiers unless the contract
  requires conversion. Missing actions/oracles are requirements gaps, not helper
  defaults. Do not edit Gherkin just to fit an implementation.

## Bounded waits, repeatability and diagnostics (ADR-43, addition)

- Prefer condition-based waits with finite timeouts over fixed sleeps. Reuse the
  suite's automation/assertion APIs and existing wait conventions; avoid global
  timeout changes or extra retry layers without an explicit scoped reason.
- Poll only suitable observations. Never repeat a payment/create/delete or other
  mutating action merely to wait for its outcome. Required repeatability,
  idempotency and shared-resource isolation are explicit execution-plan concerns.
- Generate random data only where requirements permit and through existing
  helpers; preserve enough safe correlation information to reconstruct the case.
  Do not substitute random values for specified input or assumed live state.
- Failure diagnostics include useful expected/actual values, operation and safe
  correlation identifiers. Redact credentials, tokens and personal data; do not
  dump whole payloads/responses/context or secrets into logs, reports or messages.
- Do not turn errors/timeouts into success with broad catches, missing-value
  defaults, skipped checks or retry-until-green. Propagate meaningful failures
  using existing logging/assertion conventions without adding duplicate layers.
- These rules govern authored bindings; they do not grant test execution,
  environment probes or package installation to implementation agents.
