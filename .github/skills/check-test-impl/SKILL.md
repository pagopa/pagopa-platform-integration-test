---
name: check-test-impl
description: >-
  Use for a read-only, feature-first review of Python Behave test implementation
  against attached or explicitly identified Gherkin features. Trigger on
  "check implementazione test", "confronta gli step con le feature", or requests
  to find missing, inconsistent, incorrect or potentially problematic test logic.
  Check bindings, implementation, assertions and directly relevant hooks,
  configuration and utility contracts through QA-engineer. Return evidenced
  findings and scenario coverage in chat; never fix files or execute tests.
---

# Check test implementation against Gherkin

## Purpose and boundaries

Determine whether the current Python implementation represents the actions,
inputs and observable outcomes described by the supplied features. Finding a
decorator is not proof that a scenario is implemented; an HTTP 200 is not proof
that its business assertions are satisfied.

This is a **static, read-only review**, not implementation, test execution,
functional certification or a development-readiness gate. Draft features and
partial implementations may be reviewed; report their gaps without inventing
requirements, expected results or test data.

Use [review-behave-steps](../review-behave-steps/SKILL.md) for a quick review
centred on Python files without a requested feature-to-implementation comparison.
Use [review-feature-files](../review-feature-files/SKILL.md) for a functional
Gherkin review. This skill does not start either workflow as an additional,
duplicate review.

## Inputs

- Required: one or more attached or explicitly identified `.feature` files,
  or an explicitly scoped suite whose features can be resolved.
- Implementation: attached/named Python bindings and implementation files.
  If omitted, resolve them from the selected suite's actual loading rules;
  do not assume a `steps_impl.py` filename or restrict bindings to one file.
- Optional: supplied API specifications, human-authored requirements,
  existing failure evidence, prior findings, exclusions and requested focus.
- Output: chat by default. Write a Markdown report only when explicitly
  requested, obtaining its exact destination if absent.

Ask with the dedicated question tool when the feature/suite scope or a material
requirement is ambiguous. If only Python files were supplied, ask for the
features needed for this comparison rather than silently reviewing another
suite. Do not require missing runtime data merely to review code; distinguish
unresolved data from missing functional rules.

## Review owner and permissions

1. Read [QA-engineer.agent.md](../../agents/QA-engineer.agent.md) afresh.
   When already QA-engineer, work directly and never self-delegate. Otherwise
   delegate one bounded review to the registered QA-engineer, listing all target
   features/Python files and the output requirements below. Use the configured
   agent/model selection; do not hard-code a model or substitute a generic agent.
   If unavailable, report the blocker.
2. The reviewer reads its linked persona,
   [activity workflow](../../../docs/workflows/qa-engineer/implementation.md),
   scoped ACE instructions, assigned family instructions,
   [Python guidelines](../../instructions/python-scripts.instructions.md),
   [Behave guidelines](../../instructions/behave-steps.instructions.md) and
   [Behave profile](../../profiles/behave-steps.profile.yaml).
   Load only the active role's assigned instructions.
3. Keep features, Python, hooks, configuration and utility files read-only.
   Do not create corrected copies, patches, tests or implementation plans as
   files. A report request permits only that report, not source changes.
4. Do not run shell/Git commands, tests, imports, compilation, parser scripts,
   Behave dry-runs, environment probes, package installation or live requests.
   Available read-only editor diagnostics may supplement file inspection.
   An unavailable diagnostic tool is a limitation, not permission to execute a
   substitute. Do not delegate prohibited execution to another agent.
5. Do not stage, commit, push, create a PR, modify external state, or launch
   QA-runner/closer. A later request to fix or execute is a separate authorized
   activity under the corresponding workflow.

## Procedure

### 1. Establish the current baseline

Read every requested feature and Python file, preserving their current contents
and line references in review context. Use the working files, including existing
uncommitted edits, not remembered contents or an assumed Git baseline.

Identify the suite type, language, framework, active matcher/converters and
binding-loading scope. Follow relevant imports and registrations. Read only
directly connected hooks, config/data sections and utility implementations needed
to verify an actual contract or producer/consumer relationship. Consult the
utility documentation required by the Behave profile before judging an API.

Keep the trace bounded to the requested scenarios; do not turn a dependency
check into a repository-wide audit. Record missing/unreadable dependencies and
their effect on the review. Do not dump secret files, full environments,
credentials or private request/response bodies into output.

### 2. Map features to executable intent

For each scenario:

- Include applicable Background steps, inherited tags and Examples blocks.
  Resolve the effective Given/When/Then kind of `And`/`But`.
- Compare complete step text against loaded decorators: quotes, case, literal
  suffixes, parameter names, matcher restrictions and conversions matter.
  Account for the framework's actual normalization before flagging whitespace.
- Follow each matching binding into its implementation and relevant helpers.
  Check callable existence, arguments, return values and context dependencies.
- Trace each scenario input to the request/setup that uses it and each expected
  result to an actual observation/assertion.
- For outlines, inspect every distinct row/variant, including positive/negative
  statuses and empty inputs. Count definitions and expanded execution cases
  separately, without claiming they ran.

Record binding status (`mapped`, `missing`, `overlap-risk` or `unresolved`) and
implementation status (`implemented`, `partial`, `stub` or `unresolved`) separately.
Here, `implemented` means statically traced, not runtime-verified or passed.
Shared mappings may be described once, but no requested scenario may disappear
from coverage. Do not call a scenario covered solely because its steps match.

### 3. Check implementation correctness

#### Bindings and parameter flow

- Missing/mismatched decorators, generic registrations, overlapping patterns,
  unsupported matcher types and incompatible wrapper/implementation signatures.
- Ignored or overwritten parameters, hard-coded replacements, incorrect config
  keys and values fetched from a different payload than the one sent.
- Identifier preservation: leading zeros, IUV/NoticeNumber distinctions,
  unjustified slicing/coercion, null versus absent/empty values.
  Apply the Behave guidelines' empty-Examples-cell contract when relevant.
- Do not equate duplicate Python function names with lost Behave registrations:
  verify how decorators register their callable before asserting an impact.

#### Client and configuration contracts

- Actual utility signatures and response types, not conventions from a different
  library: for example `json_body` versus `json`, and `status_code` versus a
  field in the response JSON.
- Path placeholder names/case, template substitutions, URL construction and
  required configuration values. Check the effective selected config when it
  can be established read-only; otherwise state which environments were read.
- Payload nesting, YAML indentation/types, discriminator/type values and
  consistency between feature parameters, configuration keys and submitted data.
- Missing callables/imports and wrongly assumed dict/object/list interfaces.
  Distinguish code reached by current scenarios from unused bindings/helpers:
  a latent defect must not be attributed to an unrelated active scenario.

#### Context, lifecycle and isolation

- Producers before consumers: clients, common data, responses, identifiers,
  correlation headers and session IDs must exist when accessed.
- Consistent dictionary, namespace or library-specific attribute access,
  including nested data and the loader's actual return type.
- Hook ordering and reset behaviour: values required by a scenario must not be
  erased before use; each scenario/Examples row must be independent.
- Mutable templates, request objects and shared containers must not leak
  generated identifiers or invalid-input mutations into later cases.
- Resource ownership and cleanup must match the objects actually created;
  setup/teardown errors must not be hidden or mask the original failure.

#### Assertions and observable results

- `pass`, logging-only bodies, unconditional success, unused responses and
  checks that merely restate locally prepared values.
- Every outcome required by the feature: status, response content, identifier
  correspondence, entity state, non-creation or interrupted flow as applicable.
  Do not invent extra business requirements to label a test incomplete.
- Response shape before indexing: missing/null properties, empty lists,
  wrong types, first-item-only checks and unsupported array cardinality.
- Negative cases must exercise the intended validation and distinguish an
  expected rejection from a technical failure. Do not assume every error
  response has a JSON body or that every 404 proves the intended non-creation.
- Retry/wait bounds, eventual consistency, external prerequisites and repeated
  mutations. Flag missing evidence instead of prescribing arbitrary sleeps,
  unconditional retries or live setup.
- Verify field paths against supplied contracts where available. If a business
  state might belong to an installment rather than the root object, report the
  uncertainty; do not declare a guessed path correct or incorrect.

### 4. Validate and classify findings

Use source excerpts, exact line references and read-only editor diagnostics
where available. A clean editor result is not proof of correct bindings,
runtime behaviour or passing tests. Static overlap analysis is not proof of a
runtime ambiguous-step error.

Before reporting each finding, verify its current source and consumer:

- **Evidence:** the concrete mismatch, relevant producer/contract and location.
- **Impact:** affected scenario(s), scope, and how execution or verification fails.
- **Action:** the smallest correction area or missing evidence needed; no edits.
- **Classification:** confirmed defect, potential risk, functional/contract gap,
  or guideline violation. Suggestions are not proven defects.

Order findings by demonstrated impact:

- **Critical:** a shared blocker prevents the reviewed suite from starting or
  reaching its scenarios.
- **High:** a scenario is blocked, an important outcome is untested, or a
  concrete defect permits false success.
- **Medium:** a conditional robustness, isolation or diagnostic problem with a
  stated trigger and impact.
- **Low:** a relevant maintainability/guideline issue without demonstrated
  execution impact. Avoid cosmetic noise.

Do not repeat a shared cause once per scenario or count its consequences as
independent root causes. Report existing issues without fixing them. If a
required contract is unavailable, state what cannot be concluded and continue
with unaffected checks.

### 5. Confirm read-only integrity

Compare the requested source files with the retained baseline using allowed
read tools. If another actor changed them, preserve those changes and identify
the affected findings/coverage as stale or recheck only the affected scope.
Do not overwrite, revert or claim an unchanged baseline without checking.

### 6. Return the review

Respond in Italian unless requested otherwise:

1. Result: `review-complete`, `partial` or `blocked`, with actual reviewed scope.
   `review-complete` means the agreed static review finished, not that tests pass.
2. Prioritized findings with file/line links, affected scenarios, evidence,
   impact, classification and suggested correction area. Group per file where
   useful and add cross-file relationships without duplicating findings.
3. Compact coverage matrix: feature/scenario identifier, binding status,
   implementation status and outstanding gap. Include definition/expanded-case
   counts where outlines exist.
4. Relevant strengths, actual checks performed, checks not run, assumptions,
   unread dependencies, unresolved contracts and any concurrent source changes.
5. Short conclusion identifying the first blockers to address. If no findings
   were established, say so within the inspected scope and retain the limits.

For an explicitly requested Markdown report, use the same structure, preserve
unrelated existing contents and return its actual saved path. A write failure
is explicit; never claim an unsaved report exists. Do not create a report for
a chat-only request or include secrets/personal payload data in excerpts.

## Repeat reviews and ACE

On "repeat the checks", reread the current scoped inputs and verify prior
findings against them. Separate resolved, remaining and newly observed issues;
do not repeat stale claims or widen scope without need. Rechecking does not
authorize fixes, runtime execution or a runner/closer handoff.

Follow the existing ACE lifecycle only for actual participating agents. The
engineer returns actual review actions, checks, applied lesson IDs and assessed
friction to the caller; it does not invent a task identity or write traces.
When an orchestrator captures traces, privacy finalization must precede
counters, thresholds and consumption/commit under the repository rules.
This skill grants no additional ACE write or execution permissions.

## Example invocation

Attach the target features, bindings and implementation files, then request:

> Usa check-test-impl: confronta questi Python con entrambe le feature e cerca
> incongruenze, parti mancanti, errori e rischi. Includi hook/config strettamente
> pertinenti, copertura per scenario e riferimenti alle righe. Solo review in
> chat, nessuna modifica o esecuzione.
