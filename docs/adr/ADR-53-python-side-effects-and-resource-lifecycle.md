# ADR-53: Explicit effects, import boundaries and resource cleanup

- Status: Accepted

## Decision

Addition: apply [side-effect/resource rules](../../.github/instructions/python-scripts.instructions.md#side-effects-resources-and-executable-scripts-adr-53-addition).
Separate executable entry logic behind a main guard, avoid accidental operational
effects at import, and manage resources across partial setup/failure paths.
Text encoding and path resolution follow explicit contracts.

## Consequences

Preserve intended bootstrap behaviour unless a scoped impact assessment supports
change. No incidental global mutation, hidden cleanup/persistence errors or newly
authorized network/probe operations.
