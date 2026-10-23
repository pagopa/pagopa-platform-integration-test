# ADR-30: Complete the activity without implicit publication

- Status: Accepted

## Decision

The [completion contract](../workflows/qa-orchestrator/operations.md#completion-and-closure-handoff-adr-30-adr-08-through-adr-13)
returns actual results/checks/limits/next steps at the requested boundary.
Assess README after coherent changes even without publication. Invoke closer for
an actual assigned documentation/report or authorized publication task, not
simply because another agent succeeded.

## Consequences

Restricted roles return README needs to an authorized writer. Reuse runner error
reports, avoid standalone success reports and preserve independent Git gates.
No fabricated runtime evidence for documentation-only closure.
