---
name: ppa-commit
description: >-
  Commit project changes with a compliant English message and push the current
  branch. Use when asked to commit, save changes in Git, or when QA-closer reaches
  its commit gate. Accept an optional message override, file scope, and context;
  respect explicit commit-only or no-push requests.
---

# Commit project changes

This skill is the canonical commit and push workflow for this project.
Preserve the calling agent's approval and test gates. It does not authorize
creating a PR, merging, amending commits, or rewriting history.

## Inputs

- Optional complete commit message override.
- Optional paths or scope hint identifying the changes to commit.
- Optional context or restrictions, such as committing without pushing.

Use the available dedicated question tool for ambiguous scope or decisions.
Do not require a particular model or prompt-specific input placeholders.

## Allowed commit types

Every commit subject must use `<type>: <concise summary>`, with one of:

- `feat`: new feature or test scenario
- `fix`: bug fix
- `chore`: maintenance, dependencies, configuration, or tooling
- `docs`: documentation-only changes
- `refactor`: restructuring without behavior change
- `test`: new or updated test cases
- `style`: formatting, whitespace, or linting changes
- `perf`: performance improvements
- `ci`: continuous integration changes
- `build`: build system changes
- `BREAKING CHANGE`: backward-incompatible changes

Keep the summary specific, action-oriented, and in English.

## Procedure

1. **Check the terminal and repository state.**
   - Check the terminal type and run commands from the repository root.
     The examples below use PowerShell.
   - Run `git status --short` and `git branch --show-current`.
   - Preserve existing changes and staging. If the current branch cannot be
     determined reliably, ask before creating a commit or pushing.

2. **Inspect and resolve the staged scope.**

   ```powershell
   git diff --cached --name-only
   git diff --cached --shortstat
   ```

   - If files are already staged, use that selection unless explicit user paths
     require a different scope. If staged changes conflict with the requested
     scope, ask instead of silently including or unstaging them.
   - If nothing is staged, stage the intended files, using explicit user paths
     when supplied. Use `git add -A` only when all changes are in the authorized
     scope; otherwise stage specific paths or ask to resolve ambiguity.
   - Re-check staged names and stats after staging. If no changes remain, report
     that fact and stop without creating an empty commit.
   - Inspect the relevant staged content as needed to understand the changes and
     avoid committing secrets or unrelated work. Run `git diff --cached --check`
     and resolve or report failures before committing.

3. **Choose the message.**
   - Recognize a complete override by its allowed prefix, colon, and nonempty
     concise description. Use a valid English override rather than regenerating it.
   - Treat an invalid or incomplete override as context for a compliant message
     and honor any explicit restrictions on the actions to take.
   - Otherwise infer the message from the staged changes. If the summary is
     unclear, use `git diff --cached --stat` and inspect relevant staged hunks.
   - QA-closer must preserve the exact orchestrator-provided message. If it is
     incompatible with project requirements, report the conflict rather than
     silently rewriting it.
4. **Create and verify the commit.**
   - Use `git commit -m "<message>"`, passing the chosen subject/body
     without shell interpolation altering their contents.
   - Stop on a failed commit or hook; report the actual error. Do not bypass hooks,
     create a success-shaped fallback, or push after a failed commit.
   - Retrieve the resulting hash with `git rev-parse HEAD`. If Git reports no
     commit was created, do not claim that an existing hash is a new commit.

5. **Push unless explicitly excluded.**
   - Respect a commit-only or no-push instruction.
   - Determine whether an upstream exists, for example with
     `git for-each-ref --format='%(upstream:short)' "refs/heads/$branch"`,
     where `$branch` is the resolved current branch.
   - With an existing upstream, run `git push`.
   - Without an upstream, verify that `origin` exists and run
     `git push --set-upstream origin $branch`.
   - Never force-push or silently change a configured destination. If the
     destination is missing or ambiguous, ask before proceeding.
   - Check the command's exit status. On failure, preserve the local commit and
     report the push error; do not report the branch as published.

## Output

Return only:
- Commit message, using the message already chosen
- Commit hash
- Push result, including an explicit skipped or failed status when applicable

If blocked before creating a commit, report the blocker rather than inventing
commit metadata.

## Examples

> /ppa-commit the documentation changes with "docs: clarify local test execution".

Use the supplied message, commit only the intended documentation changes, and
push according to upstream status.

> /ppa-commit the staged changes without pushing.

Infer a compliant message from the staged selection and report the push as
skipped.
