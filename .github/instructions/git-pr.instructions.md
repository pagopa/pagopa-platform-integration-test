---
# Catalog metadata anchors (do not edit manually)
source: pagopa-platform-mcp
source_version: 1.1.5
source_digest: sha256:5273f891bd620751e488c7533f18abaeed4941c979c4ddbaad219d8a8017d7a8
source_id: git-pr-guidelines
---

# Pull Request Guidelines

## Preconditions

1. Verify `gh` exists: `gh --version`
2. Verify auth: `gh auth status`
3. Stop if checks fail.
4. Ensure all commit messages and PR descriptions are in English.

## PR data collection

1. Resolve assignee and reviewers:
  - Run `$ghUser = gh api user --jq ".login"`.
  - Use the `askQuestions` for every PR to ask the user for the CSV of GitHub usernames to request as reviewers. Store the answer verbatim in `$reviewers`; accept an empty CSV when no reviewer is required.
2. Assess current branch:
  - Run `git branch --show-current` to get the current branch name for PR head reference,
  - store the result verbatim as the `$branch` variable.
3. Collect changes info:
  - Run `$commits = git log main..HEAD --oneline --no-merges -n 12` for concise commit context,
  - Run `$files = git diff main...HEAD --name-only` to list changed files,
  - Run `$stats = git diff main...HEAD --shortstat` for compact change size.
  - store the results verbatim as the `$commits`, `$files`, and `$stats` variables.
4. Compose the body:
  - Call read_file on [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md), 
  - fill **every section** with content inferred from the `$commits`, `$files`, and `$stats` variables (replacing all HTML comments with actual text, do not pass template file directly),
  - store the result verbatim as the `$body` variable. Do not pass the template path to `gh pr create`; the filled text must be embedded inline.
5. Infer title:
  - use content inferred from the `$commits`, `$files`, and `$stats` variables,
  - use the branch name to extract a codename in the form `XY-123`,
  - format title as `<branch codename> - <short semantic changes analysis>`,
  - store the result verbatim as the `$title` variable.
6. Infer labels:
  - use content from the `$commits`, `$files`, and `$stats` variables,
  - store the result verbatim as the `$labels` variable, 
  - Available labels (e.g., `docs` prefix -> `documentation` label):       
    - `bug`, 
    - `documentation`, 
    - `size/large`, 
    - `size/small`.
7. Create PR with:

  ```bash
  gh pr create \
    --base main \
    --head $branch \
    --title "$title" \
    --body "$body" \
    --label "$labels" \
    --reviewer $reviewers \
    --assignee $ghUser
  ```

### Fallback for ambiguous scope

Use detailed per-file stats only when needed:

```bash
git diff main...HEAD --stat
```
