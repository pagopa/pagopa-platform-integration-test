# QA analyst activity routing

Read this workflow before reviewing, editing, or creating features, whether the
request comes directly from the user or from the orchestrator. These activity
modes are independent of the orchestrator's branch/session modes.

## Select the activity (ADR-02)

Use the explicit intent; ask through the dedicated question tool only when the
action, files, or output scope is ambiguous. Supplied feature files alone do
not authorize editing. An explicit correction request authorizes its stated
scope without a second generic permission question.

| Activity | Procedure | Allowed output |
| --- | --- | --- |
| Review | Apply [review-feature-files](../../../.github/skills/review-feature-files/SKILL.md) directly when already QA-analyst; never delegate to yourself | Findings in chat; a Markdown review report only when requested at a human-confirmed path. No feature creation or modification |
| Edit or correct | Follow [feature-editing.md](feature-editing.md) | Scoped changes to authorized features, checks, explanations and implementation impact |
| Create from a team-template UC | Read [uc-workflow.md](../../use-cases/uc-workflow.md) and apply [uc-to-feature](../../../.github/skills/uc-to-feature/SKILL.md) | Agreed features and the fixed UC reports/registry |
| Create from other documentation or an explicitly supplied migration suite | Apply the common evidence rules below and the Gherkin conventions | Agreed features with evidence, coverage, gaps and readiness summarized in chat; no invented UC or mandatory UC registry |

An explanation-only request returns an explanation without editing features or
starting implementation. A request combining review and correction may use the
edit procedure for the explicitly authorized corrections; a review-only skill
invocation never escalates itself to editing. Ask for an explicit change of
activity before applying fixes proposed during a review.

Direct `/uc-scenario-context` and `/uc-test-data` requests stop after their own
report. `/uc-to-feature` in `assemble-only` consumes current existing reports;
it does not run retrieval stages to repair prerequisites.

## Common evidence rules (ADR-04)

Read the [shared source policy](../../../.github/skills/uc-scenario-context/source-policy.md)
for source admission, reading tools, approval, provenance, privacy and failures.
Apply these safeguards to creation and functional edits regardless of input
format; use them when judging functional correctness during review as well.

- Read the scoped Gherkin instructions and profile. A file under review/edit
  is an object of analysis, not proof of the correct product behaviour.
  Missing requirements do not prevent reporting an actual syntax/style defect;
  mark unsupported functional conclusions as questions, not proven defects.
- Preserve the distinction between functional requirements, expected values
  (oracles), input test data, and evidence of current environment availability.
  Never infer a missing rule, error path, value or live state to complete a file.
- For generic documentation, map each proposed behaviour/check to an admitted
  passage or explicit user requirement. Separate supported happy/alternative/
  error cases from uncovered requirements and unresolved questions. Ask about
  blocking ambiguity rather than manufacturing coverage.
- In non-UC migration only, an explicitly supplied executable suite may describe
  its current implementation under the source policy's migration exception.
  It is not automatically the target specification; seek explicit requirements
  or confirmation for intended behaviour. Do not autonomously mine other suites.
  The UC workflow's prohibition on executable-suite evidence remains unchanged.
- Use only admitted applicable data. Keep unresolved input values conspicuous;
  follow the existing data skill's TODO/comment convention, with stable local
  requirement IDs explained in the output. Do not create a UC registry merely
  to allocate those local IDs. Missing actions or oracles are functional gaps,
  never input-data placeholders.
- For non-UC work, include source locators, coverage, unresolved data/state,
  ambiguities and actual checks in chat. Persist an additional Markdown report
  only if requested at an agreed path; the four UC artifacts are not mandatory.
- Review/edit can read supplied features and relevant step definitions with read
  tools to assess implementation impact, not to establish missing requirements.
  Do not write Python. UC translation still excludes executable-suite sources
  and only reads registered feature outputs within its reconciliation rules.

## UC execution and resumption

The UC workflow remains the authority for schema, ownership and invalidation.
Confirm the run registry; context writes `01-context.md`, data consumes it and
writes `02-test-data.md`, then translation consumes both and writes features
and `03-feature-report.md`. Update `00-run.md` only for real outputs and changes.

Validate identity, producer, revisions and states before each stage. On
resumption obtain and persist the scoped human continuity confirmation for
inputs, reports and registered features; matching revisions do not establish
unchanged content. Historical records do not bypass source approval or renew
data availability. Support stages never call translation recursively. Explicit
read-only requests return proposals, not completed persistent stages.

Keep the stable UC workflow identity distinct from the Jira key and the current
request's ACE `task_id`, as defined in the UC workflow (ADR-07).

## Results and implementation boundary (ADR-05)

Always return the selected activity, actual file paths, checks actually
performed, unresolved issues and a result:

| Result | Meaning |
| --- | --- |
| `review-complete` | Review findings delivered; no feature edits or implicit approval to implement |
| `changes-complete` | Authorized edits saved; completion alone does not establish development readiness |
| `draft` | Supported output exists but functional gaps, unresolved data/state or ambiguities remain |
| `ready-for-development` | Agreed output is saved and current, supported coverage is reconciled, and no blocking requirement, oracle, data or preparation issue remains |
| `blocked` | Missing authorization/input, conflicting evidence or a tool/write failure prevents completion |

For creation/edit, report readiness and blockers **per feature**, even when the
overall activity is complete. A review-only result or `changes-complete` without
an explicit readiness assessment is not a development gate. For UC output,
derive readiness from the current registry, report and feature state:
`ready-for-development` corresponds to `pronta per lo sviluppo` with current
`ready` artifacts; never introduce these activity labels as new UC schema enums.

Explain each created/changed scenario and any step-text, parameter, outline or
tag change that may affect Python bindings or test selection. This is handoff
information, not an actual delegation. Only the orchestrator may delegate to
QA-engineer/runner after checking readiness and the authorized task scope.
When invoked directly, return the result to the user; do not start another agent.
Neither readiness nor a syntax check proves that Python exists, the environment
works, or tests have passed.

Apply [ADR-44 through ADR-48](../../../.github/instructions/gherkin.instructions.md#null-inputs-adr-44):
include intentional empty Examples cells and affected parameter/row locations
in implementation impact, requiring conversion to Python `None`. Distinguish
null, absent and explicitly empty-string inputs before readiness. State the
binding obligation without claiming Python conversion already exists or ran.
Preserve existing identifiers, report outline expansion separately from file
definition count, and return missing observable outcome criteria as functional
gaps in the existing report/chat contract, not invented defaults.

## Review reports and ACE (ADR-06)

During review, no feature may be created or modified, including alternative
"corrected" copies. A requested Markdown report may be written only to an
explicitly supplied or human-confirmed `.md` path. Read an existing report before
updating it and preserve unrelated/user-authored content. Do not use this
exception to write UCs, skill/instruction files, implementation code, ACE files,
or UC stage reports/registry. Those artifacts retain their own ownership rules.
If persistence fails, report the error and return the findings without claiming
the report was saved. Explicit chat-only requests create no review report.

The analyst returns trace elements (actions, outcome, checks, lessons and
friction), never trace files. The orchestrator owns ACE capture, privacy
finalization, counters and reflection under the current request's ACE `task_id`.
When invoked directly without an orchestrator, return those elements without
claiming that trace capture or finalization ran. Report permissions do not
disable ACE bookkeeping or authorize a second trace writer.
