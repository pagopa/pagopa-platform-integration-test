# ADR-49: Useful English docstrings without unrelated legacy cleanup

- Status: Accepted

## Decision

Apply [docstring rules](../../.github/instructions/python-scripts.instructions.md#function-docstrings-and-scoped-maintenance-adr-49)
to every new/modified function, including steps, methods, fixtures and tests.
Describe actual purpose/behaviour and relevant non-obvious errors/effects;
update the docstring when its contract changes.

## Consequences

Simple functions need concise useful prose, not empty template sections.
Preserve style and unrelated edits; no repository-wide legacy documentation
cleanup as an incidental change.
