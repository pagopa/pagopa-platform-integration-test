---
applyTo: "src/**/steps/**/*.py"
---

# Behave Step Definitions Guidelines

These instructions apply to Python files containing behave step definitions.

## Step file organization (all suites)

- Do not place all step definitions in a single file.
- Split step definitions by scenario, or by clear subsets of scenarios.
- Use a shared file for global reusable steps: `common_steps.py`.
- Use scenario-focused files for specific logic, according to tags in feature files, for example:
  - `scenario_01.py`
  - `scenario_02_03_06.py`
- Keep decorators unique across files to avoid duplicate/matching collisions.

## Step implementation

- Group steps by kind (`given`/`when`/`then`) within each file.
- Keep step functions focused; one assertion per step where practical.
- Use parametrized steps to reduce duplication.

## Shared utility reuse

- Search the codebase for existing test suites to understand project conventions: `environment.py`/`configuration.py`, existing step patterns and assertion styles.
- Inspect shared utility documentation before coding:
  - Read [`src/utility/README.md`](../../src/utility/README.md) and module README files in [`src/utility/config`](../../src/utility/config), [`src/utility/rest`](../../src/utility/rest), [`src/utility/json`](../../src/utility/json), [`src/utility/soap`](../../src/utility/soap).
  - Reuse existing utility modules whenever they already cover the scenario needs.
- Suite-specific utility must be stored in the suite folder, for example `src/integration/<suite>/utility`.
