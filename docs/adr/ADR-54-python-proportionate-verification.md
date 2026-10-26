# ADR-54: Proportionate checks and honest verification boundaries

- Status: Accepted

## Decision

Addition: follow [verification rules](../../.github/instructions/python-scripts.instructions.md#proportionate-verification-and-honest-results-adr-54-addition):
write relevant isolated tests, select targeted existing checks, and distinguish
static inspection, saved tests, executed results and remaining uncertainty.

## Consequences

No style-driven tooling/dependency installation or unsupported success claims.
Execution remains subject to role/runner approval; implementation engineers gain
no terminal, import, compilation, test or installation permissions.
