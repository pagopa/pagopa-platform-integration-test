# ADR-47: Explicit regex dialect and scenario-count semantics

- Status: Accepted

## Decision

The [profile contract](../../.github/instructions/gherkin.instructions.md#profile-interpretation-and-validation-adr-47)
uses Python re named groups, canonical suite/acronym spelling and explicit
definition counting. The limit of twelve counts Scenario/Outline definitions;
expanded Examples cases are reported separately.

## Consequences

Profile examples and regexes are mechanically checkable; semantic case/identity
relations still require validation. No silent legacy renames or out-of-scope
file splitting. YAML validity, profile conformity and Gherkin syntax remain
distinct from runtime binding/test success. Invalid configuration is explicit.
