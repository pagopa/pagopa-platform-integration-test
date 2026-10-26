# ADR-41: Explicit documentation paths and bounded profile authority

- Status: Accepted

## Decision

The [profile/reuse contract](../../.github/instructions/behave-steps.instructions.md#profile-resolution-and-shared-utility-reuse-adr-41)
uses explicit README paths resolved from the repository root. Resolve test type
and suite placeholders; report missing/unreadable configuration without guessed
paths. Material ambiguities still require clarification even with a valid profile.

## Consequences

The profile remains path configuration, not a second persona or permission grant.
New-helper templates do not mandate legacy migrations. Preserve role ownership
and current-suite conventions without importing another suite's requirements/data.
