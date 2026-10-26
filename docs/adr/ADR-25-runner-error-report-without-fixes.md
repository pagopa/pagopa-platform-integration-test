# ADR-25: Error reports do not require a fix loop

- Status: Accepted

## Decision

Follow the [report policy](../workflows/qa-runner/execution.md#error-reporting-and-permissions-adr-25):
for unresolved suite errors, create/update a relevant Italian Markdown report
under `reports/`, whether fixes were skipped, declined, stopped or exhausted.
Reuse the report with preserved history and actual evidence, not duplicates.
The wrapper permits editing reports, never code/features/configuration or ACE.

## Consequences

No mandatory fixes just to obtain a report, standalone success report, HTML
narrative or Confluence template. Pure Git/tool/permission blockers without
suite-error evidence need chat status. Report persistence failures remain explicit.
Return trace elements to the orchestrator; no automatic closer/commit/push/PR.
