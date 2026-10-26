# ADR-51: Reuse and observable compatibility within owned scope

- Status: Accepted

## Decision

Follow [reuse/compatibility rules](../../.github/instructions/python-scripts.instructions.md#reuse-compatibility-and-ownership-adr-51)
and existing role workflows. Inspect relevant exports/consumers before changes;
reuse existing APIs and preserve observable behaviour except the authorized
change, including bug corrections.

## Consequences

No speculative abstraction or duplicate helper layer. Breaking changes need
impact/migration decisions, not signature-only claims. General Python rules
do not widen ownership or override Behave's specialized input/null contract.
