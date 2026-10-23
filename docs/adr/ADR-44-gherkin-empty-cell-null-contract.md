# ADR-44: Empty Examples cells mean null and Python None

- Status: Accepted

## Decision

Retain the mandatory [null convention](../../.github/instructions/gherkin.instructions.md#null-inputs-adr-44):
an empty Examples cell is intentional null, interpreted as Python None by
new/changed bindings. Behave supplies raw empty text, so the binding must accept
it and convert before typed processing, payload construction or assertions.
Intentional JSON null is neither an omitted field nor a string.

## Consequences

The analyst hands off affected parameters/rows and distinguishes absent/empty/
null inputs. Unresolved representation blocks readiness, not a missing Python
implementation alone. Engineer/runner checks cover acceptance, decoding and
serialization. No parser patch or migration of existing suites is authorized.
