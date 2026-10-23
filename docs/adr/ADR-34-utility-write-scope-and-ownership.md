# ADR-34: Explicit utility, export, test and documentation ownership

- Status: Accepted

## Decision

Apply [write-scope boundaries](../workflows/python-utility-engineer/implementation.md#write-scope-and-ownership-adr-34)
to shared/suite-local utilities, their exports, pertinent unit tests and directly
related documentation. Review report permission is narrower than implementation.
Resolve overlapping writers and new shared targets before writing.

## Consequences

No step/hook/feature/configuration/dependency/agent/skill/instruction edits.
Outside-scope needs return for appropriate assignment, not generic confirmation
to widen the role. Preserve pre-existing work and concrete local suite paths.
