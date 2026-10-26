---
applyTo: src/**/*.feature

---

# Gherkin Guidelines

Read [the Gherkin profile](../../.github/profiles/gherkin.profile.yaml) before
editing and resolve it from the repository root. Apply its language, structure,
indentation, naming and tags. Report missing, malformed, unreadable or
contradictory settings explicitly; stop dependent changes rather than inventing
values. Ask about material functional, compatibility, ownership or profile
ambiguities, reusing answers already established.

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
- Apply the profile maximum to Scenario/Scenario Outline definitions, not expanded
  Examples rows. Report expanded execution counts separately. Group new files
  semantically; splitting existing files needs authorized output paths and
  preserved identity/coverage, not automatic renaming or scope expansion.
- Use consistent formatting and indentation.
- Use third-person singular present tense for steps (e.g. "l'utente effettua il login", not "io effettuo il login", nor "come utente voglio").
- Where the active workflow permits, consult existing feature files only for conventions not already defined here or in the profile; ask the user which to follow as a blueprint when needed.

## Null inputs (ADR-44)

An empty `Examples` cell (`| |`) MUST mean intentional `null`, represented as
Python `None` at the binding's input interpretation boundary. It is never an
unresolved data placeholder or an intentional empty string. Keep this project
convention even though Behave's parser/substitution returns raw empty text:
the parser does not perform the required conversion automatically.

For new/changed features, identify affected parameters/rows in the implementation
handoff. New/changed bindings MUST accept their empty outline values and convert
them to `None` before type conversion, request construction or assertions; a
matcher rejecting empty input does not satisfy the contract. JSON serialization
must preserve intentional `None` as `null`, not silently omit the field, stringify
it as `"None"`/`"null"`, or substitute a default. For other transports, explicit
null representation follows the supported API contract, not a guessed encoding.

An absent field and an intentional empty string remain distinct. When those
values must coexist with null, establish an explicit, unambiguous representation
and decoding contract from requirements/user clarification; do not invent a
universal sentinel or reinterpret literal text such as `null`. Preserve numeric
zero, false, leading-zero identifiers and literal nonempty values. Do not use
truthiness (`value or None`) as a generic conversion rule.

Analyst readiness requires a clear supported data meaning and a stated conversion
obligation, not already implemented or executed Python. Engineer/runner checks
must cover matcher acceptance and actual converted values, not just feature
syntax. If the representation is unresolved, keep the affected output draft.
This is mandatory for new/modified scope, not an automatic migration of all
legacy features/bindings. Do not globally patch the Behave parser.

## Safe outline normalization (ADR-45)

A constant Examples column is a candidate for simplification, not an unconditional
edit. Before replacing its placeholders with a literal, inspect all relevant
Examples blocks, tags, coverage/source associations and placeholder uses in steps,
data tables and docstrings. Preserve lexical values and the null contract.

Normalize only when behaviour, case coverage, selection and binding impact are
established equivalent within the authorized scope. Preserve remaining variations;
do not silently collapse distinct rows or tagged Examples blocks. If no variable
parameters remain, conversion to an ordinary scenario is allowed only when those
same conditions hold; otherwise retain the outline or ask for a scoped decision.
For existing features, report old/new wording, generated-case and tag changes.
An apparent formatting optimization is not authority to alter binding consumers.

## Stable identity and tracking (ADR-46)

At initial creation allocate unique feature progressives within the target suite
and scenario progressives from `01` in each file. During maintenance retain
existing identifiers even when scenario order changes; allocate an unused
progressive to additions, without renumbering existing scenarios or recycling
identifiers known to be referenced. Never silently renumber on insertion/deletion.

Check relevant suite/file allocations only within the active workflow's admitted
reading scope. When UC source rules prevent reading executable suites, obtain
an authoritative allocation/confirmation from the user or admitted registry;
do not bypass those rules, guess uniqueness or claim it was checked globally.
Missing allocation evidence is a question, not permission to scan excluded paths.
Report exhausted numeric ranges rather than widening the profile silently.

Renumbering, file splitting/moving or identifier changes need explicit scope
approval, an old-to-new identity mapping and impact on selectors/reports/UC
registries. Follow the owning workflow's reconciliation rules.
Reuse an existing valid tracking comment; if a required value is absent/invalid,
ask for the authoritative ten-digit value. Do not derive it from Jira, a timestamp
or another technical ID. Tracking is distinct from dynamic feature/scenario tags.

## Profile interpretation and validation (ADR-47)

The profile's regex dialect is Python `re`, including `(?P<name>...)` groups.
Apply full-string matching and the declared case/word-limit rules together:
matching a lexical regex alone does not establish semantic profile compliance.
Use the canonical suite token with preserved acronym casing in filenames and
its lowercase form in identifier tags. Slugs start uppercase and preserve
established spelling/acronyms; underscore-separated words need not all start
uppercase. Do not silently rename legacy files to enforce a new convention.

Feature progressives match across filename and identifier tags. Scenario IDs
are unique within the file but remain stable rather than positional. Match tag
suite tokens to the filename's suite token after lowercase conversion.
The profile limits definitions per file; also report actual expanded rows/cases
without claiming they ran. An outline contributes one definition and one
execution case per Examples row.

Distinguish valid YAML, profile conformity and Gherkin grammar; none proves
runtime bindings, environment readiness or passing tests. Use syntax supported
by the actual suite/parser, not unsupported newer Gherkin constructs. The
analyst performs read-based checks and only its permitted language-help command;
external parser/test results stay attributed to their actual producer.
No profile value grants editing, execution or source-reading permission.

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
- Feature and scenario identifier tags are mandatory; use the profile formats.
  Each feature progressive is unique within its suite and matches its filename
  and tags. Initially number scenarios from `01` in each file; on maintenance,
  preserve stable identifiers under ADR-46 rather than renumbering by position.
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

## Observable completion criteria (ADR-48, addition)

- Then states the source-supported observable outcome, not merely "correct",
  "valid" or "fast" without criteria. Identify the affected entity/correlation,
  state, properties and applicable cardinality when needed to remove ambiguity.
- Distinguish asynchronous request acceptance from completed business processing.
  State the required observation; a technical wait cannot invent a deadline or
  replace proof of the final result.
- Negative cases verify the specified rejection/error and any required preserved
  state, not just that some exception or failure occurs. Do not add unsupported
  error codes, text or absence-of-side-effect assertions.
- Thresholds, time limits, numeric tolerances/units, ordering and normalization
  rules come from admitted requirements or an explicit decision, never guessed
  defaults or the current observed implementation.
- Missing criteria are functional gaps in the active workflow's existing report
  or non-UC chat summary. Return questions/draft readiness, not invented checks.
  No new mandatory matrix or additional reporting artifact is introduced.
