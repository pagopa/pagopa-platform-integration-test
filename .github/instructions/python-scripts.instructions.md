---
applyTo: '**/*.py'

---

# Python Scripts Guidelines

These instructions apply to new and modified Python code throughout the
repository, including scripts, tests, bindings, fixtures and utilities. They
are coding rules, not permission to edit outside the task/role, execute code,
install tooling or change publication/ownership decisions.

## Function docstrings and scoped maintenance (ADR-49)

- Every new or modified function must include a concise **English** docstring
  using triple quotes immediately below its definition. This includes methods,
  step functions, fixtures, helpers and unit-test functions.
- Describe purpose and relevant behaviour, including non-obvious errors or side
  effects. Do not merely repeat the function name. A simple function needs only
  a useful sentence, not mandatory empty Args/Returns/Raises sections.
- Update documentation when the actual contract changes. Limit compliance edits
  to the requested change and touched functions; do not launch a legacy docstring
  cleanup or rewrite unrelated user-authored content.
- Match existing naming, imports and formatting, keeping functions cohesive and
  testable. Comment only non-obvious logic rather than narrating the code.

## Types and value semantics (ADR-50)

- Annotate parameters and returns of new public APIs and modified signatures
  where types can be established. Preserve the module's compatible annotation
  style; do not bulk-convert legacy annotations or invent types for unresolved
  domain contracts.
- Prefer meaningful types/guards over `Any` or casts that hide incompatibility.
  An annotation or `cast` is not runtime validation of external input.
- Validate inputs at the appropriate boundary according to the actual contract;
  do not indiscriminately coerce strings/numbers, erase leading-zero identifiers
  or confuse absent, null, empty, zero and false values.
- For example, `value or fallback` loses valid `0`, `False` and `""`; when only
  null needs a default, use an explicit `is None` decision if that default is
  authorized. Intentional null is not automatically a missing value.
- Use syntax/library APIs supported by the actual targeted Python runtime.
  A CI value of `3.x` does not establish a minimum Python version. Inspect the
  relevant runtime/configuration and clarify material uncertainty; do not invent
  a repository-wide minimum or add a version pin as an incidental cleanup.

## Reuse, compatibility and ownership (ADR-51)

- Follow the [repository reuse rule](../../AGENTS.md#shared-utility-reuse-rule-all-coding-agents)
  before new helper logic. Read the relevant APIs/callers and exports; reuse
  existing capabilities before adding wrappers, abstractions or dependencies.
- Preserve observable compatibility unless the concrete change is authorized:
  signatures/imports, result shapes, exceptions, input mutation, state/lifecycle
  and side effects all matter. A requested bug fix may change the defective
  behaviour; distinguish it from unintended changes to other callers.
- Inspect affected consumers proportionately and report unexamined/dynamic caller
  uncertainty. Breaking changes require explicit impact/migration decisions,
  not a nominally unchanged signature or an unverified compatibility claim.
- Respect role ownership and pre-existing edits. Use the
  [QA-engineer workflow](../../docs/workflows/qa-engineer/implementation.md) for
  bindings/hooks and the [utility workflow](../../docs/workflows/python-utility-engineer/implementation.md)
  for reusable utility changes. These rules do not authorize step engineers to
  edit utility modules or specialists to edit out-of-scope callers.
- When editing `src/**/steps/**/*.py`, also follow the
  [Behave instructions](behave-steps.instructions.md), including their structured
  input/null contract. Do not duplicate or override it here.

## Explicit errors and recovery (ADR-52, addition)

- Distinguish invalid input, an expected negative result and a technical failure.
  Use explicit validation/exceptions at operational boundaries; test assertions
  do not replace runtime input validation that must remain effective under
  Python optimization.
- Catch specific exceptions when meaningful recovery/translation is defined.
  Do not suppress failures with bare catches, `pass`, unconditional success or
  return values that look like valid empty/negative results.
- `None`, `[]` or `False` may be legitimate contractual outcomes, but must not
  silently stand in for a failed operation. A fallback requires a supported
  semantic reason, not convenience or an attempt to make checks pass.
- Broad boundary catches may serve cleanup or a controlled application/CLI error
  result; they must not conceal failure or continue as though the action worked.
  Preserve useful exception context/chaining where safe, without exposing secret
  values in translated errors or diagnostics.
- Follow existing logging/error conventions; avoid logging the same traceback
  at every layer, changing global logging for a local fix, or dumping credentials,
  tokens, personal data and full payloads into logs/messages.

## Side effects, resources and executable scripts (ADR-53, addition)

- Identify filesystem/network/environment access and other external effects.
  Importing a reusable module must not accidentally run operational requests,
  parse CLI arguments, write files or execute tests.
- Put executable script entry logic behind `if __name__ == "__main__":` and keep
  reusable logic separate. Preserve intentional documented bootstrap behaviour;
  assess callers before moving/removing initialization or changing global state.
- Use appropriate resource management for files, sessions and other owned
  resources, including partial initialization and failure paths. Cleanup must
  not hide the primary failure or silently claim resources were released.
- Specify text encoding and resolve paths according to the module/script's
  documented contract; do not assume an arbitrary current directory. Respect the
  repository-root command convention without changing the process directory to
  fix local path handling.
- Avoid incidental mutation of global logging, environment, process directory
  or shared state. Necessary global/bootstrap changes require explicit scope
  and compatibility assessment, not an automatic ban or a silent relocation.
- Preserve safe write/cleanup boundaries and report persistence failures.
  Network operations use existing client timeout/trust/error conventions;
  these instructions do not authorize live calls or environment probes.

## Proportionate verification and honest results (ADR-54, addition)

- Add/update pertinent behaviour/regression tests when the change requires them,
  using existing patterns/tooling. Unit tests isolate network, secrets,
  environment, clock/randomness and external state where relevant; do not
  introduce implicit live-service access or real credentials.
- Select the smallest checks that cover the changed behaviour, errors and
  compatibility. Expand only for relevant uncovered dependencies or failures.
  Do not invent unavailable checks or infer runtime success from static reading.
- Do not introduce or install formatters, linters, type checkers or packages
  merely to standardize style. Dependency/tooling changes need their appropriate
  task scope and authorization; preserve existing supported tooling.
- Execution remains subject to the active role and
  [runner approval workflow](../../docs/workflows/qa-runner/execution.md).
  QA-engineer and Python-utility-engineer write/propose checks but do not execute
  tests, imports, compilation, shell commands, probes or package installation.
  No indirect execution through another unauthorized agent is permitted.
- Return actual static/editor checks separately from executed commands/results,
  tests written, proposed checks and unverified limitations. Record unknown or
  blocked verification explicitly; saved code is not proof of passing tests.
