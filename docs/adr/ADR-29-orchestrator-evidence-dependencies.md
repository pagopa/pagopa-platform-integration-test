# ADR-29: Evidence dependencies and resource-safe parallel work

- Status: Accepted

## Decision

Follow [dependency reassessment](../workflows/qa-orchestrator/operations.md#evidence-dependencies-and-safe-parallelism-adr-29):
requirements/scenarios affect readiness and bindings; executable/configuration/
shared helper changes affect relevant verification. Descriptive documentation
alone does not invalidate tests. Evidence certifies its actual contents/scope.

## Consequences

Use targeted fresh checks where needed; do not infer total success from a partial
selection. Parallel execution needs safe data/accounts/service-state isolation,
not merely disjoint files. Serialize unsafe or uncertain shared-resource use.
