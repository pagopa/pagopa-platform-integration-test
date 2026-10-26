# ADR-50: Meaningful types and explicit value semantics

- Status: Accepted

## Decision

Use [type/value rules](../../.github/instructions/python-scripts.instructions.md#types-and-value-semantics-adr-50):
annotate new public APIs/modified signatures where types are known, preserve
compatible style and validate external input at the appropriate boundary.
Annotations/casts are not runtime validation.

## Consequences

No Any/cast shortcuts, bulk annotation churn or truthiness-based loss of valid
zero/false/empty values. Resolve runtime compatibility without inventing a
minimum Python version from CI's 3.x or introducing incidental version pins.
