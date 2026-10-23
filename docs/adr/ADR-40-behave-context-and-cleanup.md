# ADR-40: Scoped context state and failure-safe cleanup

- Status: Accepted

## Decision

Apply [context lifecycle rules](../../.github/instructions/behave-steps.instructions.md#context-lifecycle-and-cleanup-adr-40):
identify produced/consumed state and its scope, preserve framework attributes and
existing hooks, and isolate scenarios including outline rows. Distinguish data
reset from resource release, including partial setup and failed tests.

## Consequences

No blanket context clearing, module-level scenario state or order dependencies.
Cleanup failures remain visible without hiding original failures. Hook/lifecycle
changes require the existing write ownership and authorization.
