# ADR-52: Explicit failures and meaningful recovery

- Status: Accepted

## Decision

Addition: use [error rules](../../.github/instructions/python-scripts.instructions.md#explicit-errors-and-recovery-adr-52-addition)
to distinguish invalid input, expected negative results and technical failures.
Recover/translate intentionally; broad boundary catches may support controlled
failure/cleanup, not silent success.

## Consequences

No success-shaped None/empty/false fallbacks without contractual meaning.
Preserve useful safe error context and existing logging conventions without
duplicate tracebacks or sensitive payload dumps. Operational validation cannot
depend solely on assertions removed by Python optimization.
