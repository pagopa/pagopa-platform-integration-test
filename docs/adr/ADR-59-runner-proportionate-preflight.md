# ADR-59: Scoped prerequisite checks without implicit setup

- Status: Accepted

## Decision

Addition: use [preflight rules](../../.github/instructions/run-tests.instructions.md#proportionate-preflight-adr-59-addition)
for relevant interpreter/framework/formatter/config/browser prerequisites.
Prefer static evidence and explicitly approve executable diagnostics or setup.

## Consequences

Missing dependencies are blockers, not installation/service-start permission.
Credentials do not authorize probes. No universal mandatory preflight suite or
new launcher/profile is introduced.
