# ADR-24: Current paths, isolated artifacts and tracked processes

- Status: Accepted

## Decision

Align [run instructions](../../.github/instructions/run-tests.instructions.md)
with actual README/configuration/CI: WISP/FdR use `src\integration`, with explicit
scope and suite environment. Use exclusive run/attempt subdirectories for local
Allure/JUnit/logs; preserve every execution instead of deleting shared evidence.
Track the original process through completion/cancellation, preserving partial
results and stopping only owned processes when authorized.

## Consequences

No stale/mixed artifacts or duplicate execution after a tool wait timeout.
Allure output formatter ordering remains explicit. Optional servers require a
separate request, real absolute selected-attempt path and lifecycle plan.
Valid CI artifact paths remain unchanged.
