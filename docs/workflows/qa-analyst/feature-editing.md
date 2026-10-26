# Edit or correct existing Gherkin features (ADR-03)

Apply this procedure only in the edit activity selected by
[activity routing](activity-routing.md). A review-only request never authorizes
feature edits. The procedure is part of the analyst's core role, not a new skill.

## 1. Establish scope and baseline

- Identify the exact target files and requested corrections. An explicit request
  to correct those files authorizes that scope; ask only about missing targets,
  ambiguous decisions or expansion beyond the request.
- Read current contents and the applicable Gherkin instructions/profile. Preserve
  pre-existing changes, unrelated scenarios, comments, tags and data. If unexpected
  concurrent changes conflict with the request, stop and ask.
- Ask for a run registry if the request or feature provenance indicates UC output
  but its registry cannot be identified. Do not guess the most recent run.
  Read a supplied/identified registry to establish whether the target is registered.
  Do not silently treat known UC output as an untracked standalone feature.

## 2. Classify the correction

- **Syntax/style:** preserve functional meaning, action order, data and coverage.
  Grammar and outline refactoring can still alter step bindings: record the impact.
- **Functional:** changes to actions, setup, outcomes, required data, scenario
  boundaries or coverage require admitted evidence under the common source rules.
  A clear, explicit user requirement is evidence; ask only if the intended
  behaviour is ambiguous or conflicts with another requirement.
- Never infer correctness from the existing feature or Python alone. Do not
  weaken assertions, delete failing cases, replace data or add unsupported paths
  merely to make a correction look complete.

## 3. Reconcile registered UC output

For a registered feature, follow [UC resumption and invalidation](../../use-cases/uc-workflow.md#ripresa-invalidazione-e-controlli)
before overwriting it. Confirm continuity, preserve manual changes and respect
producer ownership. The analyst may apply the owning skill's procedure directly;
this is not delegation to another analyst.

- A feature-only correction requires reconciling that feature and the final
  report through `uc-to-feature`, updating real revisions, mapping, coverage,
  checks and the registry. Unchanged context/data need not be retrieved again.
- A change to requirements, oracle or data constraints returns first to context;
  a data-only change returns to data. Apply the existing downstream invalidation
  graph; never rewrite another stage's report as a shortcut.
- If prerequisites or permissions prevent reconciliation, do not overwrite a
  registered feature blindly. Report the blocker. If explicitly authorized edits
  are saved before reconciliation can finish, mark the feature and final report
  `stale` in the registry, move the run to `in_progress`, and report the incomplete
  reconciliation. Never leave the old `ready`/`complete` claim in effect.
- If the registry cannot be updated, report the actual failure and which files
  were saved; treat the result as blocked, not a completed/current UC stage.

## 4. Apply and check

- Make only the scoped edits at the agreed paths, integrating current contents.
  Do not create replacement feature files or split/rename files unless the request
  or a subsequent human decision authorizes those output paths.
- Check language, keyword roles, outline parameters/tables, tags, independence,
  data placeholders, source-supported outcomes and preservation of intended
  coverage. Reconcile TODO comments when the associated input is resolved.
- For outline normalization, preserve distinct rows/Examples tags and source
  coverage; consider table/docstring placeholders and changed binding text.
  Preserve stable identifiers on insertions/reordering. Renumbering/splitting
  needs authorized paths, an old/new identity mapping and workflow reconciliation.
- Distinguish intentional null cells from missing data and empty strings.
  Hand off the mandatory empty-cell-to-`None` conversion for new/changed bindings;
  feature syntax alone does not verify conversion.
- The analyst performs static inspection with read tools, not parser commands,
  tests, Git commands or environment queries. The only terminal exception remains
  `behave --lang-help <language code>`. Label externally supplied validation
  results as external; do not claim a parser/test was run by the analyst.
- Surface failed writes or partial completion explicitly. Do not report changes
  that exist only as proposals in chat as saved files.

## 5. Return the result

Use the activity result contract: changed paths, corrections and their evidence,
checks actually performed, unresolved issues, per-feature readiness and Python
implementation impact. Show old/new step wording or parameter changes where
bindings may be affected. Explain changed tags/outline expansion when test
selection or generated cases may change. Do not edit the Python or delegate
implementation; the orchestrator decides whether the development gate is met.
