# ADR-09: Publish only the confirmed closure scope

- Status: Accepted
- Date: 2026-10-22

## Context

The closer's unconditional staging of all changes conflicted with the commit
skill and could include unrelated work or publish from an unintended branch.

## Decision

Apply the [closure publication gates](../workflows/qa-closer/closure.md#actions-and-approval-gates-adr-09-and-adr-10).
Use the expected work branch and exact file scope. Preserve unrelated staging
and edits, and assess outgoing commits before pushing. Git procedures stay in
ppa-commit and ppa-pr, not duplicated in the persona.

## Consequences

Unexpected/default branches block publication without an automatic switch.
Unrelated index or outgoing-commit contents require scope resolution.
Local reports are not force-added, and closure does not authorize history edits.
