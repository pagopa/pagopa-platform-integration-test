# ADR-57: Actual output capture and independent persistence status

- Status: Accepted

## Decision

The [evidence plan](../../.github/instructions/run-tests.instructions.md#evidence-acquisition-adr-57)
chooses retained session output, a real log or accessible artifacts, preserving
stdout/stderr/status and partial results. Log files specify encoding/destination;
conventional names alone do not prove persistence.

## Consequences

Capture/write failures are distinct from test outcomes. No lost pipeline status,
invented paths or automatic transfer of sensitive raw output to reports/Git/
external systems.
