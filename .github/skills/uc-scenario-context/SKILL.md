---
name: uc-scenario-context
description: >-
  Use to supply missing functional detail for Gherkin scenarios from a
  human-authored UC: field meanings, user actions, sequences, rules and
  expected outcomes. Read official URLs, files or user-authored documentation;
  produce 01-context.md under uc-workflow/v1 and ask about functional gaps only.
  Implementation doubts (API, URL, configuration, UI components, technology,
  how to induce errors) are never asked: they are returned as findings.
  Runs only through QA-analyst; other agents
  must delegate. Does not author UCs, retrieve input test values, or write Python.
---

# Document scenario context

Recover the functional detail needed to express the scenarios of a
human-authored UC. This is not UC authoring from documentation, nor Python
implementation. Use the existing
[QA-analyst](../../agents/QA-analyst.agent.md); any other agent delegates to it.
Read its persona and scoped ACE instructions. Do not create a new agent.

## Persistent handoff

Read [uc-workflow.md](../../../docs/use-cases/uc-workflow.md) first. Confirm the
run directory and inputs; initialize `00-run.md` if this is the first manual
step, otherwise read the exact registered path. Reuse its scenario ids.
Always write `01-context.md` using
[01-context.template.md](../../../docs/use-cases/workflow-templates/01-context.template.md),
including when the UC already supplies all necessary detail or findings remain
unresolved. This intermediate evidence report is not a new authoritative
specification. A chat-only or explicit read-only request can return a proposal,
but cannot count as a completed persistent stage.

Check identity, producer, revision and state as defined by the workflow,
including its human continuity confirmation when resuming an existing run.
Use the registry ownership rules: update this output's row after writing,
register supported SC cases and pertinent Q decisions, append History and
update registry metadata. Invalidate downstream reports and feature rows
when content changes; never rewrite another skill's report or revision.
Do not invoke the next
skill or modify features: manual execution stops here; automatic execution
returns to uc-to-feature with the actual report path, revision and status.

## Inputs and shared rules

- UC and scenario inventory or feature draft, with the specific questions to
  resolve. If missing, ask for them; do not reconstruct a UC from a suite.
- Official documentation URLs or files, or user-authored documentation supplied
  in chat or files. Functional and data documentation may be separate.
- Target environment/version where it affects behaviour, when known.

Read [source-policy.md](source-policy.md) before retrieving anything. It owns
source admission, tool use, provenance and human approval for both retrieval
skills. The
[triage of doubts](../../../docs/use-cases/uc-workflow.md#triage-dei-dubbi-e-report-di-traduzione)
decides which doubts are asked, which block and which are only recorded; apply
it before every question. Gherkin conventions remain in
[gherkin.instructions.md](../../instructions/gherkin.instructions.md) and its
profile; granularity and UC mapping remain in
[uc-to-feature](../uc-to-feature/SKILL.md).

## Procedure

1. List the functional questions per UC step, AF, EF, postcondition or AC:
   which fields are used and what they mean; what action continues the flow;
   required ordering, branches, starting states and observable outcomes.
   Separate these questions from input values and their required properties.
   Do not list implementation questions: which API operation, method, path or
   request structure realizes a step, which URL or configuration applies,
   which UI components are used, which technology is involved, how to induce
   an error or prepare a state. They do not change what the feature says, so
   they are not asked, not searched and not blocking. When the sources
   happen to answer one, keep the answer out of the feature wording unless the
   behaviour needs it; when they do not, write the step in the UC's functional
   words and return the doubt as a `Rilievo implementativo:` line in
   Readiness (see Output). Never create a Q or a gap for it.
   Resolve AC flow references using
   [ac-flow-references.md](../uc-to-feature/ac-flow-references.md); retain
   target flow and applicability conditions in the oracle evidence.
   Read the authorized functional goal and boundaries recorded in Agreed inputs.
   Use the companion to identify every AC verification, including intermediate
   checks, and postconditions for all positive FP/AF scenarios.
   Distinguish deployment locators from functional requirements: keep source
   URLs and environment applicability in Sources, but propose environment-
   independent page/domain wording for steps under the Gherkin instructions.
   An example UAT hostname is not evidence that the behaviour requires UAT.
   Preserve a literal locator only when the requirement tests that locator.
2. Read the supplied sources with the tools defined by the shared policy.
   Extract only the relevant passages, with exact locators. Do not assume a
   source contains both functional instructions and test values.
3. Build the evidence matrix below. An instruction such as "enter the required
   data" is not evidence of particular fields, controls or request fields.
   Record what is actually stated; mark deductions as candidates, never facts.
   UI labels and API fields may belong in Gherkin when relevant to the
   behaviour, but selectors, automation mechanics and Python belong to the
   implementation. Apply the UC skill's granularity decision test; neither a
   screenshot nor a list of fields forces one Gherkin step per field.
   Identify relevant data-variation dimensions and constraints supported by
   admitted material, even when no AF mentions them. Distinguish data sets
   exercising the same flow/checks from actual changes of path or outcome.
   Record the evidence and applicable ACs, not an invented AF or an arbitrary
   number of cases.
   Map each UC precondition to an initial-state step as the UC states it. How
   the state is verified or established before the operation under test is an
   implementation doubt: do not require evidence for it, do not block the
   step, and return a `Rilievo implementativo:` line. Do not prescribe Python
   or search suite code to supply that evidence. If a property is known only
   through the tested operation, retain it as a data-fitness requirement or a
   supported observable outcome, not as an independently guaranteed Given, and
   never anticipate a business operation to establish it.
   Distinguish a missing setup/observation capability (an implementation
   finding) from an undefined functional rule (a gap). Preserve an explicit UC
   precondition in Mapping even when its preparation is unknown; do not
   silently drop it or label the functional document defective for that reason.
   In Mapping, distinguish initial state, incoming event, observable response,
   acceptance and completion; record relevant conditions, correlation, phase
   and timing formula. A documented path that the UC does not cover is not an
   SC: record it as a `Proposta di scenario:` line in Readiness with its
   anchor in a UC operation or step, source, trigger, required sequence and
   outcome, distinct from data sets. Keep these distinctions in the existing
   Functional evidence, Mapping, Oracles, Data requirements and Questions
   columns; add no schema, artifact, state or event dictionary.
4. Ask the user only about functional gaps: missing information, a source, or
   an unclear functionality or workflow step (request an explanation or
   additional or corrected documentation). For independently discovered
   information, get explicit approval before using it. When the UC and a
   source disagree, do not choose and do not ask which governs: apply the
   source policy by requesting a revision of both the documentation and the UC
   and repeating the task on the revised versions. When the documentation
   contradicts itself, request its resolution or a pointer to the documentation
   that resolves it. Do not rewrite the UC.
   Apply the shared source policy's distinctions among scope restrictions,
   requirement clarifications and conflict-resolving decisions; reuse only
   decisions that actually settle this conflict and its scope.
5. Classify exact expected texts, status/error codes and timing requirements
   as **oracle values**, not input data. Preserve whether a time is a maximum,
   a minimum or exact; ask if unspecified. Hand input data requirements to
   [uc-test-data](../uc-test-data/SKILL.md), with their constraints,
   field meanings, combinations and scenario links. The same source may
   contribute to both skills, without reading it twice unnecessarily.
   Before allocating D ids, justify each literal's functional role as a
   Gherkin parameter; requirements needed only for implementation remain in
   the report and engineer handoff. A fixed value on which the scenario does
   not depend, which the Python/Behave step can hard-code, is not a D and is
   never requested.
   Register newly supported data-variant cases of a flow the UC covers with
   stable SC-NNN ids under the UC skill's inventory rule; data resolution will
   establish their concrete combinations. Never register a path the UC does
   not cover.
   Define D ids for requirements, not every concrete value. Reuse a D across
   cases when meaning, role and constraints are unchanged; distinct roles or
   values that must differ within one case need distinct requirements and
   explicit relationships. Only context allocates new D ids.
   For a required intermediate check without an AC/postcondition id, record
   its actual FP/AF/EF element or admitted passage in `AC or postcondition`;
   do not invent an AC to fit the template.
6. Persist the resolved evidence and all gaps in the intermediate report and
   return it to UC translation. Do not edit features, create a new functional
   specification or an invented UC. Missing functional behaviour, ordering or
   oracles remains a blocking gap for the affected checks; lack of input data
   alone can use the data skill's placeholder contract.

## Output (fixed Markdown report, Italian content)

The following content fills the template's corresponding sections; do not
replace the fixed structure with a free-form chat answer. Chat summarizes
the saved path, producer, revision, status and questions only.

- **Functional evidence matrix**: UC element and scenario; question; supported
  action/field/operation/rule/outcome; source locator and environment/version;
  admission (`provided`, `approved`, `pending-approval`); unresolved conflict.
- **Mapping proposal**: resulting Gherkin actions/checks and the source for
  each refinement of a UC step. No source may introduce an unrelated path.
- **Oracle values**: value, meaning, AC/scenario and source; missing values.
- **Input data requirements**: field or parameter, constraints, related
  parameters, target environment and scenario, handed to uc-test-data.
- **Rilievi for the translation report**: in Readiness, one line per item, in
  the existing free text and without new columns or Q rows:
  `Rilievo implementativo:` (UC element or SC, doubt, source or `nessuna`,
  proposal) for implementation doubts and non-blocking frictions, and
  `Proposta di scenario:` for a documented path the UC does not cover.
  uc-to-feature collects them in `report_traduzione_<slug-uc>.md`; they never
  change the report status.
- **Open questions and readiness**: distinguish unsupported functional detail
  from unavailable data. If the user cannot supply functional detail, report
  the affected coverage as incomplete; do not invent actions or expected
  outcomes merely to finish the feature.

Source admission is not functional correctness or proof of current environment
state. An approved but contradictory or inapplicable passage is still a gap.
