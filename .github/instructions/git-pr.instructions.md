---
# Catalog metadata anchors (do not edit manually)
source: pagopa-platform-mcp
source_version: 1.1.6
source_digest: sha256:a2ff30a10a0281d6276bfc8c051be4b7975609d5130fa7bcfa84ad7b92751ee0
source_id: git-pr-guidelines
---

# Pull Request Guidelines

## Preconditions

1. Verify `gh` exists: `gh --version`.
2. Verify auth: `gh auth status`.
3. Stop if checks fail.
4. Ensure all commit messages and PR descriptions are in English.

## PR data collection

1. Resolve assignee and reviewers:
  - Run `$ghUser = gh api user --jq ".login"`.
  - If a CSV of GitHub reviewer usernames was supplied as prompt input, store it verbatim in `$reviewers`; otherwise use `askQuestions` to request it.
  - Reject an empty or whitespace-only `$reviewers` value. Do not create a PR without at least one reviewer.
2. Assess current branch:
  - Run `git branch --show-current` to get the current branch name for PR head reference.
3. Collect changes info:
  - Run `git log main..HEAD --oneline --no-merges -n 12`, `git diff main...HEAD --name-only`, and `git diff main...HEAD --shortstat`.
4. Compose the body by reading [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md) and filling every section. Do not pass the template path directly to `gh pr create`.
5. Infer the title from the changes and branch codename, using the format `<type>: <branch codename> - <short semantic changes analysis>`.
6. Infer labels, including exactly one release label: `patch`, `minor`, or `major`. Additional labels may include `bug`, `documentation`, `size/large`, or `size/small`.
7. Create the PR with base `main`, the current branch as head, the filled title/body, labels, reviewers, and assignee.

### Fallback for ambiguous scope

Use `git diff main...HEAD --stat`.
