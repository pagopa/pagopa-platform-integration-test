---
applyTo: "**/*.py"
---

# Python Scripts Guidelines

These instructions apply to new and modified Python files in the repository.

## Function docstrings (mandatory)

- Every Python function must include a clear and concise **English** docstring using triple quotes.
- Place the docstring immediately below the function definition.
- This rule applies to step functions, fixtures, helpers, and utility functions.

## General code quality

- Match the project's existing code style (imports, naming, indentation).
- Keep functions focused and easy to test.
- Use type hints when consistent with the surrounding module.
- Add inline comments only for non-obvious logic.

## Scope handoff

- When editing behave step definition files under `src/**/steps/**/*.py`, also follow [`.github/instructions/behave-steps.instructions.md`](behave-steps.instructions.md).

Example:

```python
def build_payload(amount):
    """Build the payment payload using the provided amount."""
```