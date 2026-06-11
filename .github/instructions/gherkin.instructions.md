---
applyTo: "src/**/*.feature"
---

# Gherkin Guidelines

- One `Feature` per file, named descriptively.
- Steps must be atomic and reusable.
- Use `Background` for shared preconditions.
- Low-case Tag scenarios with relevant labels (`@smoke`, `@regression`, `@<suite-name>`, `@positive`, `@negative`).
- Do not remove existing tags.
- Write in Italian Gherkin. Use correct Italian grammar and consistent terminology across files; mind accent marks; do NOT translate Gherkin keywords or acronyms. Technical terms may remain in English (login, token, API, etc.).
- Max 12 scenarios per file for readability; split into multiple files by semantic grouping if needed.
- Use consistent formatting and indentation.
- Use third-person singular present tense for steps (e.g. "l'utente effettua il login", not "io effettuo il login").
- Search the codebase for existing feature files to match style and language; ask the user which to follow as a blueprint.
- `Examples` should never have columns with only one value; if a column has only one value, it should be moved to the scenario outline as a *parameter*.


### Feature file style & indentation

- `Scenario` / `Scenario Outline`: indented by 2 spaces.
- Steps: indented by 4 spaces.
- `Examples`: indented by 4 spaces.
- Table rows: indented by 6 spaces (for example, six spaces before the `|`).
- Comments / separators: use `# ===...===` lines indented by 2 spaces.
- `Feature:` line placed at column 0 (no leading indent).
- Blank lines separate major sections.
- Tags are placed immediately above the `Scenario`, one per line, indented by 2 spaces.
- Gherkin keywords are capitalized
- Scenario titles and steps do not end with periods
- Numeric values are written as digits (for example `1`, `3`, `48`).
- No more than a single blank line between steps, scenarios, and sections.