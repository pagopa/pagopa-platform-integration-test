# ADR-07: Separate Jira, ACE request and UC workflow identities

- Status: Accepted
- Date: 2026-10-22

## Context

Jira identifies the human's issue, ACE traces identify individual chat requests,
and UC reports already use a historical `task_id` field for resumable work.
Equating them would rename runs or conflate independent requests.

## Decision

Document the [distinct UC identities](../use-cases/uc-workflow.md#identita-distinte-adr-07)
without changing `uc-workflow/v1` fields or migrating historical reports.
Keep a UC run's identity stable across requests. A new independent request
receives a new ACE task ID, not a new identity for the existing UC run.

## Consequences

Distinguish all applicable identities in analyst/orchestrator exchanges.
Optional persistent associations use administrative History events, not schema
extensions, path renames or content invalidation.
