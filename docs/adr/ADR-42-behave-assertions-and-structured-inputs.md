# ADR-42: Complete logical assertions and explicit structured inputs

- Status: Accepted

## Decision

Addition: apply [assertion/input rules](../../.github/instructions/behave-steps.instructions.md#assertions-and-structured-inputs-adr-42-addition).
Cover the step's full logical outcome, not an assertion quota. Observe actual
system results, fail early only on genuine prerequisites, and preserve negative
tests that intentionally submit invalid inputs.

## Consequences

Parameters, tables and docstrings retain their agreed meaning, relevant rows,
missing/null/empty distinctions and lexical identifiers. No guessed defaults,
ignored input or Gherkin rewrites to fit an incomplete implementation.
