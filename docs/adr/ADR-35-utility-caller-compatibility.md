# ADR-35: Preserve observable caller compatibility

- Status: Accepted

## Decision

Inspect relevant API/exports, call sites, contracts and tests under the
[compatibility workflow](../workflows/python-utility-engineer/implementation.md#compatibility-and-integration-adr-35).
Compatibility covers returns, errors, mutation, missing values, state, retries,
timeouts and effects, not just signatures. Explicitly disclose analysis limits.

## Consequences

Concrete breaking changes need approval and an identified migration/test plan.
Only owned utility consumers are migrated by this role; remaining incompatible
callers prevent integrated completion. Analysis remains proportional to impact.
