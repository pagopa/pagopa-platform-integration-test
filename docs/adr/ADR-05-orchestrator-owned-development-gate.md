# ADR-05: Keep implementation delegation with the orchestrator

- Status: Accepted
- Date: 2026-10-22

## Context

The analyst prohibited draft handoffs, but its frontmatter offered an
unconditional implementation handoff and the orchestrator's sequence did not
explicitly check analyst readiness.

## Decision

Remove the analyst's frontmatter handoff. Return a uniform
[activity result and per-feature readiness](../workflows/qa-analyst/activity-routing.md#results-and-implementation-boundary-adr-05).
The [orchestrator](../agent-personas/qa-orchestrator.md#analyst-result-gate-adr-05)
checks scope, actual outputs, blockers and current UC artifacts before delegation.

## Consequences

Review or edit completion does not trigger implementation. Drafts do not proceed
automatically. Partial implementation requires explicit authorization. Development
readiness does not prove Python availability, environment state or test success.
