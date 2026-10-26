# ADR-03: Make feature editing a core analyst workflow

- Status: Accepted
- Date: 2026-10-22

## Context

The analyst could ask to edit features but lacked a scoped correction procedure
and a required bridge to UC registry/report reconciliation.

## Decision

Use [feature-editing.md](../workflows/qa-analyst/feature-editing.md), referenced by
the persona and activity routing, rather than adding a new skill. Explicit
correction requests authorize their scope. Separate syntax/style preservation
from evidence-backed functional changes. Respect UC producer ownership and
invalidation for registered outputs.

## Consequences

Preserve unrelated edits, behaviour and coverage. Report implementation impact
without editing Python. Partial or failed UC reconciliation cannot retain an
old readiness claim or be reported as completed.
