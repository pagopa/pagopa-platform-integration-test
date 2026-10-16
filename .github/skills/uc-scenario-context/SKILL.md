---
name: uc-scenario-context
description: >-
  Use to supply missing functional detail for Gherkin scenarios from a
  human-authored UC: fields, UI actions, API operations, sequences, rules and
  expected outcomes. Read official URLs, files or user-authored documentation;
  produce 01-context.md under uc-workflow/v1 and ask about gaps.
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
skills. Gherkin conventions remain in
[gherkin.instructions.md](../../instructions/gherkin.instructions.md) and its
profile; granularity and UC mapping remain in
[uc-to-feature](../uc-to-feature/SKILL.md).

## Procedure

1. List the functional questions per UC step, AF, EF, postcondition or AC:
   which fields are used and what they mean; what action continues the flow;
   which API operation, method, path and request structure are prescribed;
   required ordering, branches, starting states and observable outcomes.
   Separate these questions from input values and their required properties.
   Resolve AC flow references using
   [ac-flow-references.md](../uc-to-feature/ac-flow-references.md); retain
   target flow and applicability conditions in the oracle evidence.
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
4. Ask the user for missing information or a source. For independently
   discovered information, get explicit approval before using it. When the UC
   and a source disagree, expose the conflict and ask which requirement
   governs; do not rewrite the UC or silently choose a source.
5. Classify exact expected texts, status/error codes and timing requirements
   as **oracle values**, not input data. Preserve whether a time is a maximum,
   a minimum or exact; ask if unspecified. Hand input data requirements to
   [uc-test-data](../uc-test-data/SKILL.md), with their constraints,
   field meanings, combinations and scenario links. The same source may
   contribute to both skills, without reading it twice unnecessarily.
   Register newly supported cases with stable SC-NNN ids under the UC skill's
   inventory rule; data resolution will establish their concrete combinations.
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
- **Open questions and readiness**: distinguish unsupported functional detail
  from unavailable data. If the user cannot supply functional detail, report
  the affected coverage as incomplete; do not invent actions or expected
  outcomes merely to finish the feature.

Source admission is not functional correctness or proof of current environment
state. An approved but contradictory or inapplicable passage is still a gap.
