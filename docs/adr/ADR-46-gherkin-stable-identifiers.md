# ADR-46: Stable feature/scenario identity during maintenance

- Status: Accepted

## Decision

Use [stable identity rules](../../.github/instructions/gherkin.instructions.md#stable-identity-and-tracking-adr-46):
initial progressives are ordered; existing IDs remain stable on reorder/insertion.
Allocate unused IDs without silently recycling referenced ones. Check allocation
only through sources admitted by the active workflow.

## Consequences

UC source exclusions remain intact; ask for authoritative allocation when needed.
Renumbering/splits/moves require scope approval, mapping and reconciliation.
Reuse valid tracking values or ask for their authoritative ten digits; never
derive them from Jira/time/other technical identifiers.
