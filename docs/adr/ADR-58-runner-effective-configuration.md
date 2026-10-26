# ADR-58: Record effective configuration rather than assumed selectors

- Status: Accepted

## Decision

Apply [configuration rules](../../.github/instructions/run-tests.instructions.md#effective-configuration-adr-58):
resolve actual selectors, CLI/environment/configuration precedence and hook
behaviour. Record safe paths/provenance and intended effective deployment.

## Consequences

TARGET_ENV alone does not prove environment selection. Unresolved configuration
blocks environment-specific claims; no secret dumps, blanket environment clearing
or incidental config rewrites to make execution easier.
