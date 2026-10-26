# ADR-48: Source-supported observable completion criteria

- Status: Accepted

## Decision

Addition: follow [observable outcome rules](../../.github/instructions/gherkin.instructions.md#observable-completion-criteria-adr-48-addition).
Expected entity/state/properties/cardinality and asynchronous acceptance versus
completion must be sufficiently precise and supported. Negative cases verify
the specified rejection, not just any failure.

## Consequences

Do not invent deadlines, tolerances/units, ordering, normalization, codes or
side-effect checks. Missing criteria remain functional gaps/draft questions in
the existing workflow report or non-UC chat, without a new mandatory matrix.
