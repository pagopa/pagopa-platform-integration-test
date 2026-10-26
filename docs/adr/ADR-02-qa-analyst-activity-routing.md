# ADR-02: Route QA analyst activities explicitly

- Status: Accepted
- Date: 2026-10-22

## Context

Feature input alone did not distinguish reviewing from correcting, and the
generic output procedure always implied feature production and engineer output.
The review skill also required delegation even when already run by QA-analyst.

## Decision

Use [activity routing](../workflows/qa-analyst/activity-routing.md) as the mandatory
entry for direct and orchestrated requests. Explicit intent selects review,
editing, UC creation, other-document creation or explanation. Ask only when
ambiguous. QA-analyst applies its own skills directly without self-delegation.

## Consequences

Review does not silently become editing. Explanation does not imply file
production. Activity modes are independent of the orchestrator's session modes.
Keep role constraints in the persona and procedures in the linked workflow.
