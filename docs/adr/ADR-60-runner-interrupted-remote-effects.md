# ADR-60: Local termination does not undo remote effects

- Status: Accepted

## Decision

Addition: follow [interrupted mutation rules](../../.github/instructions/run-tests.instructions.md#interrupted-mutations-and-remote-cleanup-adr-60-addition).
After a mutating run is interrupted, preserve correlation and distinguish local
termination from remote completion. Establish safe repetition before retrying.

## Consequences

Unknown outcomes/residual resources stay explicit. Remote observation/cleanup
requires authorized run-owned scope; no automatic rollback/deletion/new payment
to reset the run. Preserve actual cleanup status and the existing fix budget.
