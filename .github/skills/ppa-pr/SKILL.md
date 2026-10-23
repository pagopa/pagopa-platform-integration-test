---
name: ppa-pr
description: >-
  Create a GitHub pull request for this project using the repository template,
  mandatory reviewers, CI suite/skip labels, release labels, and explicit branch routing.
  Use when asked to open or create a PR, or when QA-closer reaches its PR creation
  gate. Accept optional branches, title override, reviewer usernames, and context.
---

# Create a project pull request

This skill is the canonical workflow for creating pull requests in this project.
It does not authorize committing, pushing, or merging changes on its own.
Preserve the calling agent's approval and test gates.

## Inputs

- Optional source and target branches.
- Optional English PR title override.
- Optional comma-separated GitHub reviewer usernames.
- Optional notes for the PR body.

Ask for missing decisions through the available dedicated question tool.
Do not use prompt-specific input placeholders or require a particular model.

## Preconditions

1. Check the terminal type and run commands from the repository root.
   The examples below use PowerShell.
2. Run `gh --version` and `gh auth status`. Stop and report the error if either
   check fails.
3. Keep commit messages and PR titles/descriptions in English. Do not rewrite
   existing commits as part of this workflow.

## Procedure

1. **Resolve the repository and branches.**
   - Run `gh repo view --json nameWithOwner,defaultBranchRef` and
     `git branch --show-current`.
   - Use an explicitly requested source branch; otherwise use the current
     branch. If the source cannot be determined reliably, including a detached
     HEAD without an explicit source, ask for confirmation.
   - Use an explicitly requested target; otherwise use the repository's actual
     default branch. Never assume `main`, `production`, or another release branch.
   - Store the resolved names in `$head` and `$base`. Confirm that both refs are
     available locally for comparison and that the source is published on GitHub.
     If refs are missing, resolve them without changing the working tree; if a
     push is needed and is not already authorized, ask before pushing.
   - Reject identical source and target branches. Check for an existing open PR
     for that source/target pair; if present, retain its metadata for label
     verification below rather than creating a duplicate. Do not modify an
     existing PR without authorization.

2. **Resolve assignee and reviewers.**
   - Run `$ghUser = gh api user --jq ".login"` and use that login as assignee.
   - If reviewer CSV was supplied, store it verbatim in `$reviewers`; otherwise
     request it through the dedicated question tool.
   - Reject empty or whitespace-only input. Split the CSV into trimmed,
     nonempty usernames for the CLI. At least one reviewer is mandatory.
   - Do not silently discard rejected reviewers or create a PR without them.

3. **Collect the changes against the resolved target.**

   ```powershell
   git log "${base}..${head}" --oneline --no-merges -n 12
   git diff "${base}...${head}" --name-only
   git diff "${base}...${head}" --shortstat
   ```

   If the scope is unclear, use `git diff "${base}...${head}" --stat` and inspect
   the relevant changes. Stop on comparison errors; do not infer a summary from
   an unavailable diff. Do not describe uncommitted changes as part of the PR.

4. **Compose the body from the repository template.**
   - Inspect [the default template](../../PULL_REQUEST_TEMPLATE.md), also checking
     `.github/pull_request_template.md` and `.github/PULL_REQUEST_TEMPLATE/`.
     If multiple applicable templates exist and the choice is ambiguous, ask.
   - Preserve the selected template's headings, comments, checklist items, and
     ordering. Replace placeholders with accurate content and fill every section.
   - If validation evidence is requested, inspect the documented test commands
     and use actual results. Run relevant checks when feasible and permitted by
     the calling agent; QA-closer uses QA-runner's evidence without running tests.
     Include each exact command and its result, or clearly state what was not run.
     Never claim an unchecked result or mark an incomplete checklist item done.
   - Pass the completed body to `gh pr create`; do not pass the unchanged
     template file as `--body-file`. If no template exists, report that fact and
     compose an accurate summary and validation section.

5. **Resolve title and labels.**
   - Use a valid user-supplied English title override when present.
   - Otherwise infer `<type>: <branch codename> - <short semantic changes analysis>`.
   - Follow the **Suite and skip label policy** below. Available policy labels
     include `patch`, `minor`, `major`, `skip`, and the suite IDs from the catalog.
     Additional labels may include `bug`, `documentation`, `size/large` or
     `size/small`; they never replace required policy labels.
   - Verify availability with `gh label list --limit 200`; if the result is
     truncated, retrieve the remaining labels before deciding that one is absent.
     A missing required label is a blocker, not permission to omit it, substitute
     the catalog's descriptive label or create repository labels without approval.

6. **Create and verify the PR.**
   - If an open PR for the resolved source/target already exists, check its
     current labels against the same policy. Return its actual metadata/URL
     when compliant; report a mismatch and obtain authorization before changing
     labels. Do not return an existing noncompliant PR as a successful result.
   - Use `gh pr create` with explicit `--base`, `--head`, `--title`, completed
     `--body` or `--body-file`, labels, all reviewers, and `$ghUser` as assignee.
   - On failure, report the actual error. Do not retry by weakening requirements.
   - Retrieve the created PR with `gh pr view` and verify its URL, title, base,
     head, labels, assignee, and requested reviewers. Report any mismatch
     explicitly instead of claiming success.
   - Remove only temporary body files created by this invocation.

## Suite and skip label policy

Read [the NRT suite catalog](../../nrt-suites.json) and the relevant label checks
in [CI](../../workflows/check_pr.yml). For the resolved published source, inspect
its catalog with `git show "${head}:.github/nrt-suites.json"` rather than assuming
the current working-tree file belongs to that branch. Missing/unreadable/malformed
catalog data or comparison errors are blockers, never a reason to choose `skip`.
If source catalog changes disagree with the catalog used by the applicable CI
check, report the conflict before creating the PR.

Use each entry's **`id` as the GitHub suite label**, exactly as stored. The `label`
field is a human-readable display name, not the PR label accepted by CI.
Use `behave_path` to associate changed paths with the suite, normalizing path
separators and matching directory boundaries, not arbitrary name substrings.
Do not hardcode a duplicate suite list or infer labels from a Jira/branch name.

Read the actual `${base}...${head}` change scope and relevant hunks/context to
identify the suite worked on. The supplied task context can explain suite-specific
documentation, configuration or shared-helper changes outside `behave_path`,
but does not override the actual diff. For renames/deletions inspect
`git diff "${base}...${head}" --name-status --find-renames` and the relevant prior
catalog/path when needed. Do not ignore a deleted or renamed suite.
Read tools and reasoning suffice for this bounded classification; no new script
or live test execution is required to determine labels.

| Established PR scope | Required policy labels |
| --- | --- |
| Exactly one catalog suite worked on | Its exact `id`, plus exactly one of `patch`, `minor` or `major`; no `skip` |
| No test suite involved | `skip`, with no suite label and no `patch`, `minor` or `major` |
| Multiple suites worked on | Stop: CI accepts at most one suite label; ask to split the PR scope, never silently pick one |
| Ambiguous suite impact or a worked-on suite absent from the catalog | Ask for clarification/catalog resolution; do not treat unknown as no suite |

Shared utilities can affect several suites: inspect the relevant consumers/task
scope and distinguish incidental potential impact from actual suite work. If
the classification remains uncertain, ask rather than defaulting to `skip` or
adding all suite labels. General tooling/agent maintenance with no suite work
uses `skip`. An unregistered suite is still suite work, not a skip case.

`skip` replaces increment labels only for no-suite work: mixing it with an
increment still triggers the CI suite-label check. Preserve unrelated optional
labels, but conflicting user-supplied/existing policy labels require resolution,
not silent omission or creation with a known invalid combination.
Verify the final labels on GitHub, including the required suite ID or `skip`
and the absence of conflicting policy labels.

## Output

On success, return only:
- PR title
- Labels
- Assignee
- PR URL

On a blocker or failed verification, report the error instead of a success-shaped
response.

## Example

> /ppa-pr from PQ-714-reforge-ai-assets, reviewer octocat, with title
> "refactor: PQ-714 - consolidate PR workflow".

Use that source and title, obtain the target from the repository's default branch
because none was supplied, and apply the full workflow above. If the actual diff
only changes general agent assets and involves no suite, use `skip` without
`patch`, `minor` or `major`.

For a diff confined to the checkout suite, read its catalog entry and use
`checkout` (the `id`), not `Checkout E2E` (the display `label`), together with the
appropriate increment label. Always re-read the catalog rather than relying on
this example as a maintained suite list.
