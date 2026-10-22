# ADR-15: Validate implementation inputs without inventing requirements

- Status: Accepted
- Date: 2026-10-22

## Decision

Apply the [input contract](../workflows/qa-engineer/implementation.md#input-and-functional-boundary-adr-15)
even for direct engineer invocation. Implementation needs current features and
readiness; fixes need defect/expected-behaviour context, not a mandatory new UC.

## Consequences

Draft requirements, missing oracle/data/setup and stale UC artifacts block affected
implementation. Review can still examine incomplete input. No fake data, default
TODO resolution, disabled tests or weakened assertions may conceal incompleteness.
