# ADR-04: Apply evidence safeguards beyond template UCs

- Status: Accepted
- Date: 2026-10-22

## Context

Generic documentation and migration requests lacked the explicit evidence,
oracle and data safeguards of UC translation.

## Decision

Apply the [common evidence rules](../workflows/qa-analyst/activity-routing.md#common-evidence-rules-adr-04)
and the existing shared source policy to creation and functional corrections.
For review, distinguish actual defects from unproven functional assumptions.
Non-UC migration may inspect explicitly supplied executable suites as current
implementation, not automatically as intended requirements.

## Consequences

Do not invent requirements, values or live state. Do not fabricate a UC or
require the four UC reports for simple non-UC work. Preserve the UC workflow's
strict prohibition on executable-suite evidence and its existing stage contracts.
