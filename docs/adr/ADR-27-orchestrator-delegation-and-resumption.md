# ADR-27: Explicit delegation scope and evidence-based resumption

- Status: Accepted

## Decision

Every assignment uses the
[delegation contract](../workflows/qa-orchestrator/operations.md#delegation-and-recovery-contract-adr-27):
objective/stop, owned paths/resources, inputs/evidence, identities, decisions and
remaining budgets. Keep specialist labels and distinguish completed, partial,
blocked and failed/interrupted delegation.

## Consequences

An in-context checkpoint suffices; no mandatory new tracking file. Reconcile
partial outputs/active writers before recovery and resume from established
progress, preserving edits, budgets and completed publication.
