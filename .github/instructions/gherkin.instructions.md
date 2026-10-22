---
applyTo: src/**/*.feature

---

# Gherkin Guidelines

Read [`.github/profiles/gherkin.profile.yaml`](../../.github/profiles/gherkin.profile.yaml) before editing a feature file and apply its language, structure, indentation, file naming conventions, and tag values. Ask the user for a profile value only when the profile is absent or does not define the required setting.

The profile governs configurable values; these instructions govern semantics
and scenario design. Existing features may serve as style references only
where the active workflow permits, and never override explicit conventions.
In the UC workflow, do not use executable suite content as a source.
Ask for clarification on unresolved conflicts rather than choosing silently.

- One `Feature` per file, named descriptively.
- Steps must be atomic and reusable.
- Use `Background` for shared preconditions.
- Write Gherkin using the profile language and its official Gherkin keywords; do not invent keyword translations. Use correct grammar and consistent terminology; mind accent marks; do NOT translate acronyms. Technical terms may remain in English (login, token, API, etc.).
- Use the profile language with `behave --lang-help <language>` when a keyword dictionary is needed.
- Apply the profile maximum number of scenarios per file; split files by semantic grouping when needed.
- Use consistent formatting and indentation.
- Use third-person singular present tense for steps (e.g. "l'utente effettua il login", not "io effettuo il login", nor "come utente voglio").
- Where the active workflow permits, consult existing feature files only for conventions not already defined here or in the profile; ask the user which to follow as a blueprint when needed.
- If an `Examples` column has the same value in every row, replace its placeholders in the outline with that literal value and remove the column. Preserve variations in the remaining columns. If no variable parameters remain, convert the outline to a regular scenario without an `Examples` table.
- Empty cells in `Examples` tables (i.e. `| |`) represent a `null` (`None`) value for that parameter.

## Project operational context

Consult only the relevant sections of the repository
[README](../../README.md), such as configuration and local execution, when
operational context affects scenario design. Use them to distinguish run
configuration and implementation responsibilities from functional behaviour;
they do not override these instructions or the profile. Apply documented
mechanisms only to the suite type they describe, without extending API
defaults or capabilities to integration or E2E suites.

Reading the README does not authorize executing its commands or following
links into excluded paths. It does not prove data fitness, live availability
or a way to prepare a Given. Functional rules, expected values and test data
found there remain subject to the active workflow's source-admission policy.
If relevant operational documentation is missing or conflicting, record the
uncertainty and clarify it when it affects the design; do not invent a
configuration mechanism or read the entire repository as a fallback.

## Preserve keyword semantics

Choose keywords from the functional role of each step, not from the
structure, brevity or reuse desired for the scenario.

- Given describes the initial context: entity states, actor configuration,
  permissions and other prerequisites relevant to the behaviour.
  It must not conceal the actions or interaction history that the scenario
  needs to exercise and demonstrate. Rewriting actions in the past tense
  does not turn them into valid preconditions.
- When describes an actor action or other functional trigger of the
  behaviour. Preserve relevant actions and their order instead of hiding
  them in initial-state descriptions or generic navigation steps.
- Then describes an observable expected result. It must not silently
  perform further business actions to obtain that result. Technical
  observation, including bounded waiting for an asynchronous result, does
  not itself constitute a new business action.
- And and But continue the semantic role of the preceding Given, When or
  Then block. Use an explicit keyword when that role changes.
- Background follows the same rules as Given and applies to every scenario
  in its scope. It is not a container for an operational journey merely
  because that journey is repeated.
- Examples supplies values to a stable scenario structure. It must not
  encode different operational scripts, optional steps or instructions
  that change the functional sequence between rows.

A Given may require technical preparation to establish its declared state.
This is legitimate only when that preparation does not replace behaviour
or history that the scenario must verify. Each scenario must establish its
own prerequisites without depending on another scenario's execution.

Every Given must have a supported way to verify or establish its state before
the operation under test. It need not perform an assertion if supported
preparation establishes that state. A data-fitness requirement is not a
guaranteed initial state: do not assert it in Given when it can only be
determined by the operation being tested. Keep the requirement and any
unresolved preparation in the active workflow's report; do not discard an
explicit UC precondition or invent a preliminary business operation to
validate it. Missing preparation evidence is not automatically a missing
functional rule.

Before accepting an initial-state step, ask:
"If this state were prepared independently, without replaying the preceding
journey, would the scenario still demonstrate the same requirement?"

If not, keep the relevant journey explicit as actions. If equivalence is
unknown, clarify it rather than assuming that direct setup is sufficient.
Do not choose keyword semantics or scenario boundaries merely to reduce
duplication, execution time or scenario count.

## Environment-independent scenarios

Keep deployment configuration out of steps and Examples. Environment names,
hostnames and base URLs used only to select a deployment are resolved by the
Python/Behave implementation from the run configuration; use the repository
[README](../../README.md) for the supported selection mechanism. Describe
pages and domains functionally, for example "the Checkout homepage" and
"outside the Checkout domain", rather than fixing a UAT URL in Given or Then.
Keep the intended environment in workflow metadata and source-applicability
reports. Preserve a literal URL, domain or environment only when it is itself
an explicit functional requirement, and record that justification in Mapping.
Environment-independent wording must preserve the required observation, not
weaken an external-domain check into a generic change of page.

## Feature file style & indentation

- Apply all indentation and separator values from the profile.
- Place the `Feature:` line at the profile-defined feature indentation.
- Blank lines separate major sections.
- Gherkin keywords are capitalized
- Scenario titles and steps do not end with periods
- Numeric values are written as digits (for example `1`, `3`, `48`).
- No more than a single blank line between steps, scenarios, and sections.
- Before the language declaration line, apply the profile tracking-comment policy; if it requires a value and it is missing, **ask the user to provide it**. The tracking comment and language declaration are unindented; the profile comment indentation applies to internal comments.
- Keep data provenance, approval, fitness and availability warnings in the active workflow's reports, not in feature comments. Data-warning comments are only for unresolved placeholders: identify the affected requirements and outline rows. Remove the corresponding comment when its last placeholder is resolved, without treating remaining report uncertainties as resolved. Preserve the mandatory tracking and language declarations and any separately required traceability.

## Tags
- Feature and scenario identifier tags are mandatory; use the profile formats. Each feature file has its own progressive number within its suite, matching the filename and all identifier tags in that file. Scenario numbering restarts from `01` in each file.
- Other profile labels are optional. `@positive` and `@negative` are mutually exclusive; neither is mandatory.
- Preserve existing tags unless they conflict with these rules; ask for clarification before changing conflicting tags.
- Place the feature identifier immediately above the feature and scenario tags immediately above their scenario, one per line, at the corresponding feature or scenario indentation.

Minimal illustrative example only, not an approved functional requirement:

```gherkin
#1234567890
# language: it

@fdr3_002_Crea_revisione
Funzionalità: Creazione revisione

  @fdr3_002_01
  @positive
  Scenario: Creazione consentita
    Dato che esiste un flusso modificabile
    Quando l'operatore crea una revisione
    Allora la revisione risulta creata
```

## Learnings

### Choosing scenario boundaries

Use the following strategies according to the behaviour being verified.
These are decision patterns, not mandatory labels or a requirement to
minimize the number of scenarios.

**A. Independent transitions with an explicit journey**

Use separate, self-contained scenarios for independently meaningful
transitions or paths. Keep the documented actions needed to exercise each
path explicit when the journey or interaction history matters.
Repeated actions are preferable to concealed operational steps.

A mandatory application path does not imply dependent scenarios or require
a single scenario: autonomous scenarios may repeat the actions needed to
reach their respective verification points.
Conversely, scenario autonomy does not authorize hiding a relevant journey
in Given steps.
Choose boundaries from the requirement and its continuity needs, not merely
from dependencies between application steps or the cost of repeating them.

**B. Independently prepared initial state**

Use Given for a state that is sufficient for the test, when the way that
state was reached is outside the behaviour being verified.
The setup must preserve all relevant properties and must not depend on
a previous scenario. If preparation is unavailable or its equivalence is
not established, report the prerequisite rather than assuming it.

**C. One cohesive sequence with intermediate observations**

Keep multiple When/Then blocks in one scenario when continuity, ordering
or correlation is part of one functional requirement.
Place required intermediate assertions before the next action.
Do not split mechanically at every Then, but do not concatenate unrelated
goals merely because they occur in the same application journey.
Do not impose a single When/Then block or treat scenario length alone as
a defect.

**D. Data variants of a stable behaviour**

After choosing scenario boundaries, use Scenario Outline only for cases
with the same functional action structure and applicable checks.
Different values may select different expected results, but must not
conceal different action sequences or conditionally skipped assertions.
An outline is not a remedy for duplication between different paths.

Do not chain scenarios by execution order or retained mutable context.
If continuity between actions is essential, represent it within a cohesive
scenario; otherwise prepare each scenario's prerequisites independently.

The following fragments illustrate the patterns only: they are not approved
UC examples or complete feature files. Their assumed behaviours must be
supported by the requirements in a real scenario.

**A. Explicit journey and independent transition**

```gherkin
    Dato che l'utente si trova nella pagina A
    Quando l'utente apre la pagina B dalla pagina A
    E l'utente apre la pagina C dalla pagina B
    E l'utente preme una sola volta il pulsante "Indietro"
    Allora l'utente si trova nella pagina B
```

**B. Independently prepared state**

```gherkin
    Dato che esiste un ordine pagato e rimborsabile
    Quando l'operatore richiede il rimborso dell'ordine
    Allora l'ordine risulta rimborsato
```

**C. Cohesive sequence and intermediate observation**

```gherkin
    Dato che l'utente si trova nella pagina di inserimento email
    Quando l'utente inserisce un indirizzo email non valido
    Allora il sistema mostra un errore di formato
    Quando l'utente corregge l'indirizzo email con uno valido
    Allora il sistema non mostra più l'errore di formato
```

**D. Data variation without operational variation**

```gherkin
  Schema dello scenario: Accesso a un documento in base al ruolo
    Dato che l'utente ha il ruolo "<ruolo>"
    Quando l'utente richiede l'apertura del documento
    Allora il sistema mostra "<esito>"

    Esempi:
      | ruolo          | esito               |
      | amministratore | contenuto documento |
      | lettore        | contenuto documento |
      | ospite         | accesso negato      |
```
