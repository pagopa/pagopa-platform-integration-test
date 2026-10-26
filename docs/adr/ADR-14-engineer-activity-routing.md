# ADR-14: Distinguish engineer review, implementation and maintenance

- Status: Accepted
- Date: 2026-10-22

## Decision

Use the [engineer workflow](../workflows/qa-engineer/implementation.md) for review,
implementation/extension and fix/refactor. Apply review directly when already
QA-engineer, otherwise use the review skill's delegation.

## Consequences

Review writes no code/features, including corrected copies. Requested Markdown
reports at agreed paths are allowed. Explicit fixes authorize only their scope;
ambiguous intent requires a question, not an automatic edit.
