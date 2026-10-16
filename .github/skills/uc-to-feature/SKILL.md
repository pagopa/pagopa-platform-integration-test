---
name: uc-to-feature
description: >-
  Use when a Use Case (UC) written with the team UC template must be translated
  into one or more Gherkin .feature files. Trigger on "UC → feature", "traduci
  lo UC", "da use case a feature", or "genera la feature dallo UC". Maps the UC
  onto Gherkin concepts, designs scenarios under the project Gherkin
  conventions, and reports coverage, data requirements, and functional gaps.
  Runs only through the QA-analyst agent: any other agent must delegate to it.
  Uses uc-scenario-context and uc-test-data for missing details and
  values; never invents them. Does not author UCs or write Python.
---

# UC → feature

Scope: step 1 of the QA process (UC → feature). The UC is human-authored and is
an input, never an output. Functional-document analysis and test-data retrieval
are separate activities, performed through
[uc-scenario-context](../uc-scenario-context/SKILL.md) and
[uc-test-data](../uc-test-data/SKILL.md). This skill owns the scenario
design and assembles their results; it does not invent missing information.
Python implementation (step 3) is out of scope.

This skill is used by `QA-analyst`. If you are not running as `QA-analyst`,
delegate to [QA-analyst.agent.md](../../agents/QA-analyst.agent.md) with this
skill and the inputs below; do not translate the UC directly.

## Inputs

- The UC, attached or explicitly referenced. If missing, ask for it; never
  reconstruct a UC from existing features.
- Specifications referenced by the UC and any further documentation provided
  with the request (by the user or by a documentation-analysis activity), when
  available. Functional and data sources may be separate. Use the retrieval
  skills and their shared
  [source policy](../uc-scenario-context/source-policy.md) for additional
  sources and approval; never use an independently discovered finding without
  explicit human approval.
- Target suite and feature path, and the profile values that the
  conventions require from the user (for example the tracking comment). When
  the path is not given, ask for it; do not derive it from existing files.

## Automatic workflow and report inputs

Read [uc-workflow.md](../../../docs/use-cases/uc-workflow.md) before translating.
It defines the fixed report schemas, paths, ids, producer ownership and gates.
Confirm or read `00-run.md`, validate the UC and establish the SC-NNN inventory.
In automatic mode, execute in this order:

1. `uc-scenario-context` writes `01-context.md`, including UC-only evidence
   when no external detail is needed.
2. Read and validate that report, then `uc-test-data` writes `02-test-data.md`,
   including TODO values or an explicit no-data result when appropriate.
3. Read both actual files at the registered paths; validate their schema,
   identities, producers, revisions and states. Only then assemble features
   at the agreed paths and persist
   [03-feature-report.template.md](../../../docs/use-cases/workflow-templates/03-feature-report.template.md)
   as `03-feature-report.md`. Record actual feature paths in `00-run.md`.

When the reports already exist and are current, consume them without repeating
the retrieval activities, after the workflow's human continuity confirmation
on resumption. This includes the registered feature outputs before reuse or
overwrite; matching revision numbers alone do not prove unchanged content.
Record the scoped confirmation in registry Questions/History, not new schema
fields. Missing confirmation blocks resumption even in assemble-only.
Never infer completeness from chat summaries or a
filename. `assemble-only` mode consumes existing reports and stops on missing,
stale, incompatible or blocked prerequisites, specifying the manual step to
run; it does not invoke support skills.

The following interpretive procedure determines report inventory and final
scenario design; it does not override the stage order above. Missing functional
details or newly found constraints return automatic control to context, then
data, before reassembly. Support skills return reports without calling this
skill, preventing recursion. Do not retake unchanged decisions unnecessarily.
If a file cannot be persisted, report the failure and do not declare the stage
complete or advance. Follow the workflow's partial-coverage and blocked rules.
Use its registry ownership rules for Q decisions, History, metadata and
invalidation. Only context extends the inventory after initialization or
defines new D requirements; translation owns scenario grouping and feature
rows. Do not rewrite support reports to repair them.

Gherkin style, structure, language, indentation, tags, `Background`,
`Scenario Outline`/`Examples` rules, and file splitting are defined only in
[gherkin.instructions.md](../../instructions/gherkin.instructions.md) and the
profile it references. Read them first and apply them; this skill does not
restate or override them.

The UC may target a new or an existing suite, but existing feature files, step
definitions, and other executable suite content are never a source: not for
step wording, interaction steps, data placeholders, expected values, or
conventions. Repository documentation and Markdown data records are candidates
under the shared source policy, not executable-suite evidence. For this reason
the blueprint search of existing feature files suggested by the Gherkin
instructions does not apply to this skill. Whatever the UC lacks comes from
admitted documentation or from the user.

## UC template

The UC must follow the agreed template in
[UC-template.md](UC-template.md). Read it before step 0;
it is the single source of the UC structure and is not restated here.

## What to expect from a UC

### Nature

A UC states, at functional level, the actor's goal, the interactions between
actors and system, the conditions, and the expected outcomes. It is neither an
implementation description nor an inventory of the test environment: do not
expect ready-to-use test data. Rules, constraints, and expected outcomes,
instead, must be stated in the UC or in admitted documentation; when they
are missing, they are functional gaps, not something to infer. Technical
details (payloads, operation names, status codes) may appear: handle them as in
step 0.

### Content per section

Report these findings; do not fix them in the UC.

- **Precondizioni**: each one states something already true before the flow
  starts. An action performed during the flow is misplaced.
- **Flusso principale**: numbered steps of the actor or the system. A step
  whose actor, action, or outcome is unclear is an ambiguity.
- **Flussi alternativi (AF)**: the condition and the alternative behaviour. An
  AF stated on a step ("al passo X") or on a range of steps ("nei passi X-Y")
  replaces those steps with its own prescription: the rest of the main flow is
  unchanged and resumes after the replaced steps. Any other AF must state its
  return step or the end of the flow; otherwise it is an ambiguity. An AF must
  change the path (actions or system responses) or the outcome: an AF that
  changes only values, with the same steps and outcome, is a data variation.
  AFs do not specify data variants. Derive those from admitted documentation
  and material through the support skills, even when the UC has no AF for
  them. For a legacy AF containing only values, report misclassification
  without blocking the feature; preserve its traceability as a data variant.
- **Eccezioni (EF)**: anomalous situation and expected system behaviour. An EF
  without expected behaviour is a functional gap. An EF may name the step where
  it occurs (for example "Al passo 3, …"): the anomaly is introduced at that
  step and the stated reaction follows; the flow ends there unless the EF
  states a return. Each EF needs its own verifiable outcome: do not extend to
  an EF the verifications that an AC defines for another EF; report the EF
  instead.
- **Postcondizioni**: the template covers the state after success. A UC may
  also state postconditions for failure outcomes: use them as the oracle of
  the matching AF/EF scenarios, and report a conflict with the AF/EF expected
  behaviour.
- **Acceptance Criteria**: each AC is verifiable yes/no without
  interpretation. Vague qualifiers (for example "correttamente", "in tempi
  brevi") or an unstated outcome are ambiguities; an AC contradicting the
  flows or postconditions is a conflict. An AC may leave expected values
  (texts, times, codes) to a referenced document, but it must state which
  properties are verified and where they are defined: a property without value
  or source (for example "un titolo specifico") is an ambiguity. When a source
  gives a time without saying whether it is exact or a limit, ask.
  A verbal flow reference is recommended, not mandatory: for example
  `AC01 - {criterion} (FP)` or `AC03 - {criterion} (AF02)`. Read
  [ac-flow-references.md](ac-flow-references.md) for accepted aliases,
  normalization, scope across data variants and ambiguity checks.

### Form

No UC style guide exists beyond the template. Variations that do not change
the meaning are not findings: spacing around `:`, identifier padding or case
(`AF-1`, `AF-01`, `Ac-01`), recognizable abbreviated section names, heading
levels, list markers, section order, wording. Do not rewrite the UC for style.

Report only deviations that change or hide the meaning: a missing section, a
missing or duplicated `AF`/`EF`/`AC` identifier, an empty item, content placed
in the wrong section (for example an alternative written inside the main flow;
cover it anyway and report it), or an item abbreviated by reference to the
previous one (for example "… {other value}"; interpret it only when the
meaning is unambiguous, and report it anyway). `—` means "explicitly none" and
is not a gap.

## Procedure

### 0. Interpretive mapping UC → Gherkin

Build the mapping before writing any step. It is interpretive, not mechanical:
a UC step is not a Gherkin step, and an AC is not a scenario. Use the table as
the default reading of each section; record every deviation and its reason.

One functional UC step may correspond to one or more Gherkin steps. Choose
the granularity primarily from the UC and the referenced or provided functional
specifications, considering the actions, rules, and outcomes that the scenario
must make explicit. Split a UC step when those sources justify distinct
functional actions or verifications; otherwise keep a cohesive functional
step, even when its implementation performs several UI operations or enters
several fields. Atomicity is functional, not necessarily one field or click
per step.

Data variation and step granularity are independent: different values may be
parameters of a single step, and several steps may use constant values. Neither
the number of `Examples` columns nor repeated or varying values alone justifies
splitting a UC step. Apply the instructions' rules on constant columns
separately. Do not derive the granularity from existing suite content or invent
interactions to expand the UC. Missing functional details must be clarified
with the user or supplied through documentation.

For each proposed split, apply this decision test to the current scenario:

- Does the sub-action produce an observable response that must be verified
  before continuing? Make the action and its required verification explicit.
- Can the sub-action cause a branch or stop the flow? Make it explicit in the
  scenario exercising that condition; do not introduce an unspecified branch.
- Is its order relative to other actions a functional requirement that this
  scenario must expose? Make the required sequence explicit.
- Is it only part of data entry, with no independent behaviour relevant to
  this scenario? Keep it within the cohesive functional step.

The deciding question is: "Would grouping these sub-actions hide a functional
distinction necessary to understand or verify this scenario?" If yes, split
and cite the supporting UC content or documentation. If no, prefer the
cohesive step. These are decision criteria, not a mechanical rule yielding a
unique decomposition. Implementation convenience alone is not a reason to
split. Granularity may differ between scenarios: a field can be explicit in
its validation scenario and grouped in a completion scenario. Add intermediate
assertions only when required by the specified behaviour, consistently with
the mapping below.

| UC element | Gherkin concept | Interpretation rule |
|---|---|---|
| `UC-…` id and title | `Feature` title and traceability | The title describes the capability; the id is traced as described in step 4. |
| `JTBD di riferimento` | Traceability only | It is a reference, not a goal statement: do not derive a narrative ("in order to…") from it. Add a `Feature` description only with content stated in the UC. |
| Attore principale | Subject of actor steps | Use the role named by the UC, in the grammatical form required by the instructions. |
| Attori secondari | Subject of system responses | Typically the subject of `Then` steps. A secondary actor is never an extra test precondition by itself. |
| Precondizioni | `Given` (or `Background` when shared by every scenario of the file) | Classify each one: system/environment availability, state of a business entity, or actor configuration/authorization. Entity states and configurations also become data requirements. Preconditions set the starting state of the scenario that needs it: they do not become scenarios with their own `When`/`Then`, nor dependencies on the execution of other scenarios. A configuration precondition that determines expected values (for example the language of displayed texts) is linked to the oracles that depend on it. A precondition does not define the behaviour when it is not satisfied: derive no negative scenario from it unless an AF, EF, or AC defines that behaviour. |
| Flusso principale — actor actions | `When` / `And` | All actions of the actor in the main flow, data entry included, up to the action that produces the verified outcome. `Given` is reserved for the state before the flow. Add an intermediate `Then` when the scenario's specified behaviour requires verifying an observable intermediate response, supported by the UC or admitted documentation, including ACs and postconditions. Cite the evidence; implementation convenience or an internal check alone never justifies it. |
| Interaction steps not stated in the UC | No step | Do not add actions the UC does not state (confirmations, intermediate controls, navigation). If an outcome cannot be reached without them, take them from referenced or provided documentation or from the user; otherwise report a gap. |
| Flusso principale — internal system checks | No dedicated step | Verification performed internally by the system is observed through its outcome, not described as a step. |
| Flusso principale — system response | `Then` | Only observable outcomes. |
| AF-NN | Distinct scenario, never an `Examples` row of the main flow | The main-flow steps up to the divergence, the AF prescription replacing the steps it names, then the remaining main-flow steps if the AF rejoins. Verify the AF-specific outcome and, after a rejoin, the final outcome; if the AF ends the flow, only its outcome. The AF scenario may be an outline for data variants derived from admitted material, not specified as further AFs. A legacy AF that changes only values is a misclassified data variant: preserve its coverage reference and apply the row on variations, without inventing an alternative path. |
| EF-NN | Negative scenario | The main flow up to the step where the anomaly occurs, with the anomaly in that step; `Then` verifies the stated reaction; the scenario ends there unless the EF states a return. Apply the profile label for negative scenarios. |
| Postcondizioni | `Then` checks of final state | Verify them when observable through an interface named by the UC or by referenced or provided documentation. When observable only indirectly (for example through a displayed message), mark the coverage as partial. Otherwise report them as a verification requirement instead of inventing a check. |
| AC-NN | Oracle of one or more scenarios | Resolve verbal flow references under ac-flow-references.md. Many ACs may target one flow and one Gherkin scenario, for FP, AF and EF/negative cases alike. Collect all applicable compatible criteria as `Then`/`And` checks in that scenario; never create one scenario per AC or keep only one AC per flow. An AC scoped to a flow applies to its supported data variants unless the criterion restricts applicability; the reference alone defines no values or variants. Every AC must be satisfied by at least one `Then` (with its `Given`/`When` context), and one AC may require several scenarios. Preserve each AC separately in Coverage even when scenario and Examples row are shared. |
| Cases that differ only in values | `Scenario Outline` + `Examples` | Derive relevant data sets through the support skills from admitted documentation and material; no AF is required to specify them. Main flow, AF, or EF cases with the same behaviour and the same verifications become one outline with one row per supported case. Cases with different behaviour, or with different or additional verifications, get separate scenarios/outlines even if their steps look similar. A catalogue size or range alone does not determine the rows; do not invent a Cartesian product. Apply the instructions' rules on outlines. |
| Values fixed by the UC (quantities, outcomes, status codes, enumerations) | Literal step parameters or `Examples` values | When the behaviour or an outcome depends on them, they are functional rules: keep them unchanged. A value on which nothing depends (changing it would change no outcome) is probably test data written in the UC: ask whether it is a rule or data, keep it unchanged meanwhile, and keep the feature a `bozza`. |
| Expected values defined outside the UC (texts, times, codes) | `Then` parameters or `Examples` columns | Oracle values, not input data: take them only from referenced or provided documentation, never from the suite or the observed system. A technical code is verified only when the UC or the source states that it is part of the outcome. When missing, they are a functional gap. |
| Values that the UC only qualifies (for example "a unique name", "a valid key", "an existing entity") | Data requirement | Do not invent a concrete value. State the characteristic in the step as the UC does and hand the requirement to uc-test-data. If unresolved, use that skill's placeholder contract. |
| Technical details in the UC (payloads, operation names, field names) | Step argument (doc string / data table) only when needed to state the behaviour | Keep them verbatim if they define the expected behaviour; otherwise leave them to the implementation and mention them for `QA-engineer`. |

### 1. Validate the input

Check the UC against [What to expect from a UC](#what-to-expect-from-a-uc) and
the consistency between sections. Classify each finding:

- **Functional gaps**: undefined rules, expected outcomes, or behaviours
  (for example an AC whose outcome is not stated, or an AF needing a state
  that no precondition or rule defines). They block the affected scenarios.
- **Ambiguities and conflicts**: between sections, with referenced
  specifications, or with the conventions.
- **Data requirements**: concrete input values or states needed to run a
  scenario that the UC only characterizes. They do not block the feature
  design, but they block readiness for execution. Expected values are not data
  requirements: they belong to the oracle (see step 0).

Ask the user about blocking gaps and ambiguities through the question tool.
When questions cannot be asked, list them as open items in the output and keep
the feature a `bozza`. Never fill them with assumptions, executable suite
content, or domain knowledge not stated in the UC or in admitted documentation.
Before writing detailed steps, require the current report from
[uc-scenario-context](../uc-scenario-context/SKILL.md) for missing
fields, UI/API actions, sequence requirements or oracle values. If the UC
already supplies sufficient detail, do not require additional documents merely
as a formality. Missing input values go to uc-test-data, not this
functional-gap decision.

### 2. Inventory the behaviours

List the behaviours to cover. Each entry cites its sources (`Flusso principale`
step numbers, `AF-NN`, `EF-NN`, postconditions, `AC-NN`). Each AC and each
AF/EF must appear in at least one entry, or be listed as not coverable with the
reason.

The initial inventory is not a fixed count of data variants. When support
reports establish additional relevant data sets for an existing flow, allocate
new stable SC-NNN ids through context in the registry before using them in
reports; do not create or edit UC AFs. Record the supporting evidence,
applicable ACs and reason for each case. Context registers these supported
cases, but final grouping into scenarios/outlines belongs here.
If data resolution discovers an additional case, return to context to
register it and link the applicable evidence, oracles and requirements before
using it in data combinations. Reuse existing F/O/D ids when their meaning is
unchanged; new constraints or a different oracle need functional evidence.
Apply normal revisions and downstream invalidation.

Intermediate checks need not have an invented AC: cite the actual FP/AF/EF
element or admitted passage. In the context template's `AC or postcondition`
cell, record that functional reference explicitly when no AC/postcondition
names it; keep the fixed column and do not fabricate a criterion id.

### 3. Design the scenarios

Group behaviours into scenarios under the mapping of step 0 and the
conventions: shared preconditions, outlines, tags, file splitting. Write the
steps from the UC and admitted details in `01-context.md` under the instructions.
Do not independently retrieve missing detail while assembling. Setup is preparation, not a behaviour
of the UC: it belongs to the `Given` of the scenario that needs it, and no
scenario depends on the execution of another.

Use the current `02-test-data.md` from
[uc-test-data](../uc-test-data/SKILL.md) for input values, combinations,
admission, fitness, availability and warnings. It may cite a different source
from functional analysis. Integrate only admitted applicable findings; report
conflicts instead of changing the intended behaviour. Treat pending or rejected
values in reports as candidates, not accepted data.

If the user cannot or declines to supply missing data, still produce the agreed
feature with the data skill's TODO tokens and comments on every affected
scenario, including Background and partially populated outline cases. Follow
its contract for valid tables and resolved parameters. Syntactically valid
Gherkin is not evidence of executable steps, valid input types or available
environment states. Do not use input placeholders to invent missing functional
behaviour or oracle values; report those coverage gaps separately.

### 4. Preserve traceability

Every scenario must be traceable to its UC elements. No in-file traceability
format is agreed yet: report traceability in the output matrix, and add UC/AC
references inside the feature (comments or tags) only in a form the user
confirms or that the conventions define.

### 5. Produce the output

Write the feature at the agreed path and persist `03-feature-report.md` using
the fixed template. Populate its sections with the information below, update
the registry only after successful writes, and answer in Italian with actual
output paths, producer, revisions and states. The final report is obligatory
even when generation is blocked; never claim an unwritten feature as output.

1. **Mapping**: the deviations from the default reading of step 0, with reasons;
   for each UC step split into several Gherkin steps, identify the resulting
   steps, the functional reason for the split, and the supporting UC content or
   documentation reference.
2. **Coverage matrix**: UC element (`AC-NN`, `AF-NN`, `EF-NN`, postcondition,
   main flow) → scenario(s), down to the `Examples` row when an element is
   covered by a single row; partial coverage marked as such; uncovered
   elements with reason.
3. **Data requirements**: for each item, the scenario, the UC source, the
   required characteristics, value or TODO id, source and human admission,
   fitness and availability evidence from uc-test-data. List remaining
   requirements as `da reperire` or `da predisporre`; report any Markdown record
   actually saved, or explicitly that it was not saved.
4. **Expected values from documentation**: for each value, the scenario, the
   AC, and the source; missing values are listed as functional gaps.
5. **Functional gaps, ambiguities, and conflicts** still open.
6. **Readiness**: `pronta per lo sviluppo` only when no gap, no blocking
   ambiguity, no missing expected value, and no data requirement remains open;
   otherwise `bozza`, with the reasons. Never present a feature with
   unresolved prerequisites or data as ready to run. Report syntactic checks
   actually performed separately; a valid draft with placeholders is not an
   executable test or permission for automatic implementation/execution.
7. The scenario explanation for `QA-engineer` required by the analyst persona.

## Guardrails

- Do not invent rules, outcomes, negative paths, concrete data, or
  environment availability.
- Do not change UC rules to fit existing steps or available data.
- Do not edit the UC. Propose UC corrections in chat for the UC owner.
- Approved UC → feature examples are not available yet. Do not present any
  generated feature as an approved example; add examples to this skill only
  after explicit team approval, keeping refinement cases separate from
  independent evaluation cases.
