# ADR-16: Resolve blueprint and utility location from the actual suite

- Status: Accepted
- Date: 2026-10-22

## Decision

Use [suite context and reuse](../workflows/qa-engineer/implementation.md#suite-context-and-reuse-adr-16).
Existing suites supply their technical conventions; new suites need a question
only for material ambiguity. Resolve helpers under the actual suite type.

## Consequences

The profile uses `src/<test-type>/<suite>/utility`, not integration for all suites.
Blueprints do not establish requirements, expected data or environment state.
Behave, pytest-bdd and Playwright are handled according to their actual roles.
