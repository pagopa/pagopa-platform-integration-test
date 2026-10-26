# ADR-39: Evaluate bindings by loaded scope, kind and matcher

- Status: Accepted

## Decision

Follow [binding compatibility rules](../../.github/instructions/behave-steps.instructions.md#binding-compatibility-adr-39):
check imports/registrations, step kinds, matchers, parameter conversions, signatures
and feature consumers. Distinct patterns can overlap; equal text across kinds
is not automatically a duplicate. Generic step bindings need cross-kind checks.

## Consequences

No global matcher/converter changes for a local issue without scoped assessment.
Ownership covers shared registrations. Static inspection flags risks but cannot
certify runtime uniqueness; execution remains with the approved runner.
