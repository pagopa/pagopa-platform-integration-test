# ADR-56: Resolve actual suites and preserve argument boundaries

- Status: Accepted

## Decision

Follow [selection rules](../../.github/instructions/run-tests.instructions.md#suite-and-selection-resolution-adr-56):
use current NRT IDs/paths/tags/environments/prerequisites for registered suites,
and actual local documentation/configuration for others. FdR and FdR3 are distinct.
Pass paths/selectors as separate arguments, not evaluated command strings.

## Consequences

No duplicate catalog/profile or ban on unregistered local/unit tests. Preserve
partial scope and exclusions; resolve catalog/runtime contradictions explicitly.
