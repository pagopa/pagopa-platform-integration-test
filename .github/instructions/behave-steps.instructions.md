---
applyTo: src/**/steps/**/*.py

---

# Behave Step Definitions Guidelines

These instructions apply to Python files containing behave step definitions.
Read [`.github/profiles/behave-steps.profile.yaml`](../../.github/profiles/behave-steps.profile.yaml) before editing. Use its paths for shared utility documentation and suite-specific utilities; ask the user only when the profile is absent or does not provide a required path.

## Step file organization (all suites)

- Do not place all step definitions in a single file.
- Split step definitions by scenario, or by clear subsets of scenarios.
- Use a shared file for global reusable steps: `common_steps.py`.
- Use scenario-focused files for specific logic, according to tags in feature files, for example:
  - `scenario_01.py`
  - `scenario_02_03_06.py`
- Keep decorators unique across files to avoid duplicate/matching collisions.
- Inspect the suite's actual loaded binding scope and matcher rules before adding
  a decorator; different patterns can still match the same step.
- Shared step files and hooks have one write owner during parallel work. Report
  new overlapping dependencies before editing; do not assume one feature means
  one independent file set.

## Step implementation

- Group steps by kind (`given`/`when`/`then`) within each file.
- Keep step functions focused; one assertion per step where practical.
- Use parametrized steps to reduce duplication.
- Store shared data in the `context` object for access across steps, e.g. `context.demand_status_code`, but avoid overcomplex data structures that hinder readability.
- Make sure that context is cleared or reset between scenarios to prevent state leakage.
- Use a failfast approach: use early assertions to prevent cascading failures, e.g. `check return status code before processing response body`.

## Shared utility reuse

- Search the codebase for existing test suites to understand project conventions: `environment.py`/`configuration.py`, existing step patterns and assertion styles.
- Inspect every path listed in the profile's `shared_utility_documentation` before coding, then reuse existing utility modules whenever they already cover the scenario needs.
- Store suite-specific utility using the profile's `suite_utility_path_template`.
- Substitute the actual suite type (`api`, `integration` or `e2e`); do not default
  API/E2E helpers to integration. Follow the active role's utility ownership rules.
