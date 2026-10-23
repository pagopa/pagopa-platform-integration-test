# ADR-28: Latest explicit applicable authorization wins

- Status: Accepted

## Decision

Apply [authorization precedence](../workflows/qa-orchestrator/operations.md#authorization-precedence-adr-28):
the latest explicit decision for an action/scope supersedes earlier permission.
Execution, fixes, commit, push and PR remain independent. Pass revocations and
restrictions to active/future delegates; establish already completed effects.

## Consequences

An initial automatic-PR request no longer overrides a later refusal. Valid
same-scope consent can be reused, not expanded to another environment/destination.
No claim that a revocation undoes already completed external actions.
