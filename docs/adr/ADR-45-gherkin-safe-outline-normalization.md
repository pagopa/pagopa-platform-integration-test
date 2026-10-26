# ADR-45: Normalize outlines only with preserved behaviour and coverage

- Status: Accepted

## Decision

Apply [safe normalization](../../.github/instructions/gherkin.instructions.md#safe-outline-normalization-adr-45):
constant columns are candidates, not mandatory removals. Inspect all Examples
blocks, tags, row/source coverage, table/docstring parameters and binding impact
before replacing placeholders or converting an outline to a scenario.

## Consequences

No silent collapse of distinct rows/tagged blocks or null meaning. Existing-file
refactors stay in authorized scope with wording/selection/expanded-case impact
reported. Retain the outline or ask when equivalence is not established.
