---
applyTo: src/**/*.feature

# Catalog metadata anchors (do not edit manually)
source: pagopa-platform-mcp
source_version: 1.1.2
source_digest: sha256:cc85cac3e13a4517b037a8561c0543cdfeade5eebe5960f33cfb14772cebee5d
source_id: gherkin-guidelines
---

# Gherkin Guidelines

Read [`.github/profiles/gherkin.profile.yaml`](../../.github/profiles/gherkin.profile.yaml) before editing a feature file and apply its language, structure, indentation, and tag values. Ask the user for a profile value only when the profile is absent or does not define the required setting.

- One `Feature` per file, named descriptively.
- Steps must be atomic and reusable.
- Use `Background` for shared preconditions.
- Write Gherkin using the profile language. Use correct grammar and consistent terminology; mind accent marks; do NOT translate Gherkin keywords or acronyms. Technical terms may remain in English (login, token, API, etc.).
- Use the profile language with `behave --lang-help <language>` when a keyword dictionary is needed.
- Apply the profile maximum number of scenarios per file; split files by semantic grouping when needed.
- Use consistent formatting and indentation.
- Use third-person singular present tense for steps (e.g. "l'utente effettua il login", not "io effettuo il login", nor "come utente voglio").
- Search the codebase for existing feature files to match style and language; ask the user which to follow as a blueprint.
- `Examples` should never have columns with only one value; if a column has only one value, it should be moved to the scenario outline as a *parameter*.
- Empty cells in `Examples` tables (i.e. `| |`) represent a `null` (`None`) value for that parameter.
- The SUITE and FEATURE groups in the file name regex are to be filled with Capitalized_Snake_Case strings.
- The SUITE group in the file name regex is to be inferred from the suite you're working on, ask if in doubt.
- The FEATURE group in the file name regex is to be inferred from the feature you're working on in the scenario, in synthetic form, ask if in doubt.


## Feature file style & indentation

- Apply all indentation and separator values from the profile.
- Place the `Feature:` line at the profile-defined feature indentation.
- Blank lines separate major sections.
- Gherkin keywords are capitalized
- Scenario titles and steps do not end with periods
- Numeric values are written as digits (for example `1`, `3`, `48`).
- No more than a single blank line between steps, scenarios, and sections.
- Before the language declaration line, apply the profile tracking-comment policy; if it requires a value and it is missing, **ask the user to provide it**.

## Tags
- Tag scenarios with the profile-defined relevant labels.
- Do not remove existing tags.
- Place tags immediately above the `Scenario`, one per line, using the profile indentation.
- Apply feature and scenario tag formats from the profile.

## Learnings

### Alternating actions and intermediate assertions

Alternating `When` / `Then` blocks within one scenario is valid and appropriate when a specified observable result must be verified before the next action (for example, an error appears during typing and remains visible after clicking Continue).
Keep that intermediate assertion before the next action: moving all assertions to the end would no longer express the required observation before that action.
Review repeated action/assertion blocks when they concatenate independently meaningful behaviours or an entire application journey: split them into separate scenarios when they have distinct goals or independently verifiable outcomes, keeping each scenario self-contained without dependencies on another scenario's execution.
Do not split mechanically at every `Then`, impose a single `When` / `Then` block, or treat scenario length alone as a defect; keep the sequence together when its order and intermediate observations are necessary to verify one cohesive behaviour supported by the requirements.

Example of a justified intermediate assertion (step text follows the profile language):

```gherkin
    Quando l'utente digita un indirizzo email non valido
    Allora il sistema mostra un messaggio di errore durante la digitazione
    Quando l'utente clicca sul pulsante "Continua"
    Allora il messaggio di errore rimane visibile
    E l'utente rimane nella pagina di inserimento email
```
