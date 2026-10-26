# ADR-26: Route by requested activity independently from session mode

- Status: Accepted

## Decision

Keep ADR-01 branch/session routing, and use the
[operations workflow](../workflows/qa-orchestrator/operations.md#activity-routing-adr-26)
to select the first necessary specialist and requested stopping point. No
mandatory analyst-first sequence for technical review, existing defects,
execution or closure. Functional changes still require analyst ownership.

## Consequences

Partial activities do not accidentally launch the full pipeline. The concise
persona references operational contracts instead of retaining conflicting legacy
new-suite/fix sequences. Explicit end-to-end work still traverses applicable gates.
