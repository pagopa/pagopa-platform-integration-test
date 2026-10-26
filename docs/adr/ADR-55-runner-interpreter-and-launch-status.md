# ADR-55: Explicit interpreter and genuine process status

- Status: Accepted

## Decision

Use [launch rules](../../.github/instructions/run-tests.instructions.md#interpreter-and-launch-outcome-adr-55)
to bind framework invocation to the approved interpreter. Distinguish failure
to start, running and completed states, clear stale exit state and capture the
actual process result. Unattended wrappers propagate its exit status.

## Consequences

Missing commands are blockers, not passing tests. Logging/report commands cannot
mask failures; dedicated-shell examples do not close an interactive user terminal.
