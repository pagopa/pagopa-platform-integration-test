# Gherkin Conventions — pagopa-platform-integration-test

## Indentation

- `Feature:` / `Funzionalità:` at column 0.
- `Background:`, `Scenario:`, `Schema dello scenario:` and tags indented by 2 spaces.
- Steps indented by 4 spaces.
- `Esempi:` / `Examples:` indented by 4 spaces.
- Table rows indented by 6 spaces.
- Comment separators indented by 2 spaces.

## Tag layout

- Put all tags for a scenario on a single line.
- Keep tags directly above the scenario they belong to.

## Italian feature files

- If the file starts with `# language: it`, use Italian keywords consistently: `Funzionalità`, `Dato`, `Quando`, `Allora`, `E`, `Scenario`, `Schema dello scenario`, `Esempi`.
- Use `Schema dello scenario:` instead of `Scenario Outline:`.
- Preserve the wisp-style section separators:
  - `  # ===============================================================================================`
  - repeated between logical groups

## Scenario Outline placeholders

- Use `<placeholder>` syntax inside step text and examples tables.
- Empty example cells are valid and should be preserved.