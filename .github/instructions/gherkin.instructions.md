---
applyTo: "src/**/*.feature"
---

# Gherkin Guidelines

- One `Feature` per file, named descriptively.
- Steps must be atomic and reusable.
- Use `Background` for shared preconditions.
- Tag scenarios with relevant labels (`@smoke`, `@regression`, `@<suite-name>`).
- Do not remove existing tags.
- Write in Italian Gherkin. Use correct Italian grammar and consistent terminology across files; mind accent marks; do NOT translate Gherkin keywords or acronyms. Technical terms may remain in English (login, token, API, etc.).
- Max 12 scenarios per file for readability; split into multiple files by semantic grouping if needed.
- Use consistent formatting and indentation.
- Use third-person singular present tense for steps (e.g. "l'utente effettua il login", not "io effettuo il login").
- Search the codebase for existing feature files to match style and language; ask the user which to follow as a blueprint.
