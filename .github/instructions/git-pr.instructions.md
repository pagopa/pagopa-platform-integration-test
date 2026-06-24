---
# No applyTo: loaded explicitly by /pr and QA-closer.
---

# Pull Request Guidelines

## Preconditions

1. Verify `gh` exists: `gh --version`
2. Verify auth: `gh auth status`
3. Stop if checks fail.
4. Ensure all commit messages and PR descriptions are in English.

## PR data collection

- Run `git branch --show-current` to get the current branch name for PR head reference.
- Run `git log main..HEAD --oneline --no-merges -n 12` for concise commit context.
- Run `git diff main...HEAD --name-only` to list changed files.
- Run `git diff main...HEAD --shortstat` for compact change size.
- Compose PR body inline using [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md) sections (do not pass template file directly).
- Infer title: <branch codename> - <short semantic changes analysis>.
- Infer labels based on commit prefixes and changed files (e.g., `docs` prefix -> `documentation` label). Available labels:       
  - `bug`, 
  - `documentation`, 
  - `size/large`, 
  - `size/small`.

### Fallback for ambiguous scope

Use detailed per-file stats only when needed:

```bash
git diff main...HEAD --stat
```

## PR creation

1. Resolve assignee and reviewers with:

  ```bash
  $ghUser = gh api user --jq ".login"
  $reviewers = "aferracci,cristianosticca-pagopa,marcopiccoloalten-hash,marcods02,daniele-quero"
  ```

2. Store title and body in variables for later use:

  ```bash
  $title = "<inferred human-readable title>"
  $body = "<filled PR template body>"
  ```

3. Store labels and current branch in a variable for later use:

  ```bash
  $labels = "<comma-separated list of inferred labels>"
  $branch =  `git branch --show-current`
  ```

4. Create PR with:

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
