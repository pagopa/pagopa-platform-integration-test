# ADR-36: Isolated unit tests and implemented-not-run results

- Status: Accepted

## Decision

Follow [test and validation rules](../workflows/python-utility-engineer/implementation.md#isolated-tests-and-honest-verification-adr-36):
write pertinent behaviour/error/regression/compatibility tests using controlled
external dependencies, but do not execute tests, imports, commands or probes.
Return review-complete, implemented-not-run, partial or blocked with actual facts.

## Consequences

No real secrets, implicit network/live-state access or tautological tests.
Return tests written separately from proposed unexecuted checks/setup. The caller
uses the runner's approval gate; direct invocation returns to the user without
delegation, terminal privileges or publication.
