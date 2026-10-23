# ADR-43: Bounded observation waits and reproducible safe diagnostics

- Status: Accepted

## Decision

Addition: follow [wait/diagnostic rules](../../.github/instructions/behave-steps.instructions.md#bounded-waits-repeatability-and-diagnostics-adr-43-addition).
Use finite condition-based waits and appropriate observation polling, not repeated
mutating operations. Random inputs need requirements support and safe correlation.
Errors retain meaningful expected/actual evidence without secrets/payload dumps.

## Consequences

No implicit idempotency assumptions, global timeout changes or retry-until-green
layers. Preserve failure propagation and active-role permissions; no newly granted
execution, probe or installation authority.
