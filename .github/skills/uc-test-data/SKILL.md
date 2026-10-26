---
name: uc-test-data
description: >-
  Use to find input test values for a UC-derived Gherkin scenario from supplied
  documentation or repository data records. Check fitness and provenance,
  obtain human approval for discovered candidates, and mark unresolved values
  with placeholders and per-scenario comments. Produce a fixed intermediate
  Markdown report. Runs only through QA-analyst; other agents delegate.
  Does not change functional rules, author UCs, run tests, or write Python.
---

# Resolve test data

Resolve concrete **input values** and entity states for scenarios, independently
of functional-document analysis. Use the existing
[QA-analyst](../../agents/QA-analyst.agent.md); any other agent delegates to it.
Read its persona and scoped ACE instructions. No new agent is needed.

## Persistent handoff

Read [uc-workflow.md](../../../docs/use-cases/uc-workflow.md) first. Read the
exact `00-run.md` and `01-context.md` registered for this run. Validate their
identity, revisions and states, and obtain the workflow's human continuity
confirmation on resumption, before resolving data; do not silently use chat
memory or a report from another run. If context is missing, stale or blocked,
report the prerequisite. In manual mode ask the user to run uc-scenario-context;
in automatic mode return the issue to uc-to-feature instead of recursively
invoking another skill.

Always write `02-test-data.md` from
[02-test-data.template.md](../../../docs/use-cases/workflow-templates/02-test-data.template.md),
even if no data is needed or all values remain TODO. Reuse the context's D-NNN
requirements and SC-NNN cases; record supported combinations as C-NNN and the
exact context revision in `inputs`. If new requirements emerge, record a
question and return for a context update; do not silently redefine constraints.
Only resolve requirements supported by admitted functional evidence.

After writing, update this output's row and pertinent Q decisions, append
History and update registry metadata under the workflow's ownership rules.
Invalidate both the feature report and existing feature rows when inputs or
resolutions change; do not edit their files, producers or revisions. Return the
actual path, revision and status. This skill does not edit features or invoke
translation: uc-to-feature consumes the report and applies values/comments.
An explicit read-only request returns a proposal, not a completed stage.

## Inputs and shared rules

- UC-derived feature draft or scenario inventory and data requirements:
  parameter meaning, constraints, required states, related values and scenario.
- Supplied data documentation: official URL/file or user-authored chat/file.
  It may differ from the functional documentation.
- Intended environment and relevant version/state, or explicit `unknown`.
- Optional request to retain data in Markdown.

Read [source-policy.md](../uc-scenario-context/source-policy.md) first.
It owns source admission, reading tools, human approval and provenance. Use
[uc-scenario-context](../uc-scenario-context/SKILL.md) for missing
field meanings, functional sequences, constraints or expected values; never
solve those questions by adapting the scenario to the data found.
For feature prescriptions read
[gherkin.instructions.md](../../instructions/gherkin.instructions.md) and its
profile. Do not duplicate their language, indentation, tag or outline rules.

## Procedure

1. Inventory each required value or state and its source requirement. Keep
   input data separate from expected texts, codes and times (the oracle).
   Check relationships as well as individual formats: an identifier may be
   well-formed but belong to the wrong entity, actor, configuration or state.
   If constraints are missing, hand that question to functional analysis.
   Keep data-fitness requirements distinct from guaranteed initial states.
   A requirement such as an unpaid, usable notice remains in Data resolution
   when no supported independent preparation or observation is documented;
   do not prescribe a Given that assumes it or a preliminary payment to
   establish it. Return any required context clarification to its owner.
2. Read supplied sources; map documented concrete values, ranges or generation
   rules to the requirements. Apply the resolution completeness gate below
   before declaring a value missing. A range is not a particular available entity.
   Generate values only when the source prescribes generation and the user
   authorizes it; record the rule and synthetic/generated status. Never
   fabricate identifiers or claim generated data exists in the environment.
   Derive relevant data sets for the context-supported flows and variation
   dimensions from admitted material; they need not be named by an AF.
   Record supported combinations as C-NNN with source/relationship evidence
   for registered SC-NNN cases. Propose additional cases under the UC skill's
   inventory rule, then return for a context update to register them and link
   evidence/oracles/requirements before including them in combinations.
   Preserve the context's AC applicability; do not invent checks from input
   values. New dimensions or constraints also require a context update.
   A D identifies the requirement, not each selected value. Keep distinct
   resolutions per D/SC and identify applicable C ids in the value cell when
   needed; Combinations selects the values. Each resolution retains its own
   provenance, admission and fitness. Do not overwrite one value with another
   or allocate a new D merely because a value varies.
3. For unresolved values, search repository documentation/data records as
   candidates under the shared policy, starting with the documented test-data
   directory when accessible. Do not skip this search just because generating
   new values is possible or authorized. Show matching candidates and ask the
   human for explicit approval **before** marking them usable in the report.
   Records approved in an older task still require approval for this task
   unless explicitly supplied now.
4. If there is no suitable candidate, candidates are rejected, or sources
   cannot be read, ask the user for values or a source. If the user cannot or
   declines to provide them, continue with the placeholder contract below.
   Do not loop on the same question or invent another candidate.
5. Apply only admitted values whose fitness is established. If fitness is
   unresolved, use a placeholder unless the human explicitly chooses to
   include the candidate as unverified; retain its status and record the
   affected scenarios in the report. Approval to try an unverified value is
   not a fitness finding. Concrete unverified values do not by themselves
   require feature comments.
   Preserve the constraints and rule-defined outcomes; do not change them to
   accommodate convenient data. Do not add variants, outlines or scenarios
   solely because the catalogue offers more data: such coverage decisions
   remain with UC translation under the documented evidence and human
   decisions. Neither catalogue size nor a Cartesian product establishes
   relevant combinations; same-flow data sets can become outline rows
   without creating UC AFs.
6. Report availability separately using the exact workflow values:
   `documented-not-checked`, `user-confirmed` (with scope/date), or
   `unknown-to-prepare`. Do not run
   tests, query test systems or mutate them. A consumable value may be stale
   even when once confirmed. Report warnings and `bozza` status remain when
   a required current state or combination is not established; this does not
   imply a feature comment without an unresolved placeholder.
7. Persist the mandatory intermediate report, including unavailable values,
   decisions and scenario warnings. Separately, if requested, persist useful
   admissible data under the optional catalogue contract below. Do not create
   a catalogue merely to report missing data, or overwrite an existing record.
8. Return the report to UC translation. Prescribe data substitutions and
   comments for unresolved placeholders, but do not apply them to feature
   files here. Other uncertainties stay in the report.
   Changed behaviour or constraints require a functional report update.

## Resolution completeness gate

Before reporting a requirement as missing or assigning a TODO, complete these
checks within the authorized source scope. This is a retrieval checklist, not
a new report schema or permission to inspect executable suites.

1. **Look for the complete set, not only the main table.** Map every existing
   D requirement to the relevant source sections. Read table explanations,
   notes, complementary-data tables and combination tables that may supply
   related fields; continue bounded reads when truncation hides them. Search
   by field meaning and documented aliases, not only literal field names.
   Combine values across sections only when their scope and relationships
   support the combination. Do not assume that all required fields share one
   table, or that the number of columns defines the number of requirements.
2. **Search before concluding absence.** For requirements still unresolved
   after supplied sources, discover relevant Markdown records under the
   authorized repository documentation, following the shared source policy.
   Record the files/sections inspected and any access limitation in the
   existing Sources and Data resolution sections. Distinguish no matching
   value found, unreadable source, candidate awaiting approval, unsuitable
   value and unresolved live state. An unperformed or failed search is not
   evidence that data does not exist.
3. **Keep admission and permission decisions exact.** A supplied document
   remains `provided`; permission to generate new values is a separate
   decision, not a reason to reject the entire document or its existing
   values. Observe the shared policy's synthetic-data permission requirement
   where applicable, asking only for the unresolved permission. A missing
   answer, unavailable question tool or agent instruction not to invent data
   is not a human refusal: keep the pertinent question `open` or
   `pending-approval`. Use `declined` or `rejected` only with an explicit
   human decision and its scope/reference; never attribute a parent agent's
   assumption to the user.
4. **Read environment scope before rejecting a candidate.** Record an
   explicit statement that values apply to multiple environments, and use
   it when assessing applicability; do not demand different values merely
   because the target environment differs. Do not extend that statement to
   other environments, current entity states, enabled methods or successful
   transactions. Documented applicability, fitness and live availability
   remain separate.
5. **Reconcile before handoff.** Account for every D/SC/C resolution and any
   cross-field relationship. A concrete documented value with uncertain
   availability is not a missing value; record the unresolved state and
   apply the existing fitness/availability and warning rules instead of
   claiming the source lacks the field. Confirm that each reported refusal
   has human evidence and that every TODO has a precise unresolved reason.
   If the search reveals a new required field, return to context for its D id
   rather than silently adding or dropping it.

Example (retrieval only, not an approved UC or test-data set): the functional
context requires card number, expiry, security code and holder name. A
catalogue lists the first three in its card table and a synthetic holder in
a complementary table. Read both, check whether the holder applies to that
card, and resolve all four requirements with their respective locators and
applicable permissions. Do not report the holder as absent because it is
outside the first table, and do not treat an unverified gateway association
as absence of the documented input values.

## Placeholder contract

Use this contract when input values are unavailable, declined, pending
approval, or still unsuitable:

- Reuse each unresolved requirement's `D-NNN` id from context; never allocate
  new D ids here. A missing or semantically different requirement returns to
  context before resolution.
  In the feature use a conspicuous string token `__TODO_D001__`, corresponding
  to `D-001`; never a plausible fake value. Reuse it only for the same
  requirement, including across its unresolved cases/combinations. Repeating
  the token does not assert equal concrete values. Distinct requirements get
  distinct tokens; different selected values alone do not create new D ids.
- A Gherkin outline parameter such as `<identifier>` is a variable, not an
  unresolved value. Keep it and put the TODO token in the appropriate
  `Examples` cell. For a constant value put the token in the step or step
  argument under the profile rules. Do not invent rows to simulate variation;
  if there is only one case and no meaningful variation, use a plain scenario.
- Do not use an empty cell for missing data: it means null under the project
  conventions. An intentional null from the requirements is not a TODO.
- Before the tags of **every Scenario or Scenario Outline with an unresolved
  placeholder**, add a
  comment using profile indentation that identifies the unresolved ids and
  says the scenario is not ready to execute. List the relevant rows when only
  some outline rows are affected. A TODO in Background affects every scenario
  using it, so each needs the comment.
- Concrete candidates intentionally included as unverified and unresolved
  required states belong in Data resolution, Scenario warnings and Readiness,
  not in feature comments. In the fixed Scenario warnings table, use
  `not-applicable` in Required comment when no placeholder comment is needed;
  put the uncertainty in Affected combinations or all and Data resolution.
  Do not change report columns or omit the warning.
- Reconcile annotations after filling values: remove resolved ids/row
  references and remove the data-warning comment when its last placeholder
  is resolved. Retain all unresolved report warnings and `bozza` reasons.
  Preserve unrelated comments, mandatory declarations and tags.
- Feature content must be syntactically valid Gherkin: matching outline
  parameters and columns, well-formed tables/doc strings, and profile rules.
  TODO tokens do not imply valid input types or executable steps; they are
  explicit markers for later substitution, not runtime defaults.

Illustration only (not an approved UC example or executable test data); the
indentation below assumes the current project profile:

```gherkin
  # Dati irrisolti: D-001; scenario non pronto all'esecuzione
  Scenario: Invio della richiesta con un identificativo da reperire
    Quando l'utente invia la richiesta con identificativo "__TODO_D001__"
    Allora il sistema mostra l'esito previsto dalla specifica
```

This fragment illustrates marker placement only; a real scenario must have
its source-supported outcome, profile tags and all required prerequisites.
Do not use data TODO markers to conceal missing functional behaviour or
oracles: those are functional gaps, not input data.

## Optional Markdown persistence

In addition to the mandatory run report and registry, the analyst may create
or update only a **human-confirmed** Markdown catalogue path under
`docs/use-cases/test-data/<scope>/`, and only when persistence is requested or
accepted. No permissions extend to arbitrary docs, UCs, code, ACE files or
skill files. This optional catalogue is not `02-test-data.md`. Use
[data-record-template.md](data-record-template.md); do not fill unknown fields
with invented metadata.

Read existing records before writing. If a suitable record is absent, propose
the scoped path and record, then obtain confirmation. If it exists, reuse it as
a candidate and propose a targeted addition or correction with approval;
preserve previous provenance/history and user-authored content. Ask before
changing conflicting entries. Admission for the current feature and permission
to persist are separate decisions. Do not claim a file was saved unless it
was actually written. When writing is unavailable, return the proposed record
in chat and explicitly say it has not been persisted.

Historical records never guarantee current availability or approval for a
future task. Do not manufacture a generic catalogue with live-looking values.

## Output (fixed Markdown report, Italian content)

Fill the fixed template sections with the information below. Chat summarizes
the actual report path, producer, revision, state and questions; it is not a
substitute for the persisted report.

- **Data matrix**: id, scenario and Examples row if applicable, parameter,
  required properties/relationships, value or placeholder, source locator,
  admission, fitness, availability evidence and unresolved reason.
- **Decisions**: candidates accepted/rejected/pending, with scope and date.
- **Feature prescriptions**: proposed values, markers and per-scenario report
  warnings; feature comments only for unresolved placeholders. No feature
  edit. Report checks actually performed, not assumed.
- **Persistence**: path actually saved and provenance retained, or explicitly
  `not-requested`, `not-saved` or `pending-confirmation`.
- **Readiness**: `bozza` when markers, unverified candidates or required states
  remain unresolved; source and approval alone are never proof of execution
  readiness. Return functional gaps to uc-scenario-context.
