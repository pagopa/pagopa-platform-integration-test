---
name: ppa-readme
description: >-
  Assess and maintain the project README after a coherent set of repository
  changes, or when asked to correct, extend, update or refactor a README.
  Use the supplied scope or an explicit Git comparison; update only affected
  documentation, or explain why no update is needed. No implicit tests,
  commit, push or PR.
---

# Maintain the project README

Apply once per coherent change set, before an eventual commit, not after every
individual edit. This skill is useful for suites, utilities, configuration,
workflows and agents; it is not restricted to QA-closer.

## Inputs and permissions

- The changed file scope, explicit Git comparison, or documentation request.
- The target README (default: the repository root README), relevant linked
  documentation, and any prior assessment covering the same change set.
- Applicable role permissions and user constraints.

Respect the calling role's write and terminal restrictions. If it cannot edit
the README, return the assessment and required changes to the orchestrator or
user for an authorized writer; do not self-delegate, broaden permissions or
start QA-closer automatically. Missing permission is not "no update needed".
Do not change source code, configuration, agent instructions or other documents
to make the README appear accurate. If their changes are needed, report them.

## Procedure

1. **Resolve the scope.** Reuse explicitly supplied paths or comparison refs.
   If neither is available, inspect repository state with allowed read-only tools
   and ask when intended changes cannot be distinguished from unrelated work.
   Account for staged, unstaged and intended untracked files without conflating
   them. Do not default to all changes or compare to an assumed branch.
2. **Read the current documentation.** Read the target README and only relevant
   linked sections. Locate the existing explanation before appending another.
   Preserve user-authored content and unrelated changes.
3. **Assess reader-visible impact.** Check purpose, layout, configuration,
   prerequisites, commands, output paths, workflows and role boundaries affected
   by the change. Distinguish actual repository behaviour from planned behaviour.
   An implementation-only refactor may correctly need no README change.
4. **Update only what is needed.** Correct obsolete content, extend incomplete
   instructions, remove superseded duplication and reorganize affected sections
   where necessary. Update the table of contents/anchors if headings change.
   Preserve valid material and the existing language/style. A broad restructuring
   beyond the change's impact requires explicit confirmation.
5. **Validate without executing documented workflows.** Check affected local
   paths, links/anchors, command syntax, examples and consistency against actual
   files or verified evidence. Do not run tests, transactions, deployments, Git
   writes or commands merely because they appear in documentation. Do not infer
   live environment availability from a working link or a command example.
   Report checks not performed and any blocked verification.
6. **Return an assessment.** State `updated`, `no-update-needed` or `blocked`;
   list the assessed scope, changed README sections, checks actually performed
   and unresolved issues. For `no-update-needed`, give a concise reason. A
   proposal that could not be saved is not an update.

An existing assessment may be reused only when it covers the current relevant
contents and scope, not merely the same filenames. If new reader-visible
changes occur, reassess the affected parts. Updating the README as the final
step does not recursively trigger another full assessment.

## Boundaries

No mandatory edits just to show activity. No automatic failure report, test
execution, commit, push, PR, package installation or external publication.
The closer's error-report policy does not prohibit normal README maintenance.

## Examples

> /ppa-readme Review the documentation impact of the new agent workflow files.

Link the new entry procedure from the relevant existing section; do not copy
the entire workflow into the README.

> /ppa-readme The helper implementation was refactored; its API and usage are unchanged.

Verify that claim against the scoped changes. If documentation remains accurate,
return `no-update-needed` with that reason rather than making cosmetic edits.
