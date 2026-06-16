---
# No applyTo: loaded explicitly by /pr and QA-closer.
---

# Pull Request Guidelines

## Preconditions

1. Verify `gh` exists: `gh --version`
2. Verify auth: `gh auth status`
3. Stop if checks fail.

## PR data collection

- Run `git branch --show-current` to get the current branch name for PR head reference.
- Run `git log main..HEAD --oneline --no-merges -n 12` for concise commit context.
- Run `git diff main...HEAD --name-only` to list changed files.
- Run `git diff main...HEAD --shortstat` for compact change size.
- Compose PR body inline using [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md) sections (do not pass template file directly).
- Infer title: <branch codename> - <short semantic changes analysis>.

### Fallback for ambiguous scope

Use detailed per-file stats only when needed:

```bash
git diff main...HEAD --stat
```

## PR creation

Resolve assignee with:

```bash
gh api user --jq ".login"
```

Create PR with:

```bash
gh pr create \
  --base main \
  --head <current-branch> \
  --title "<human-readable title>" \
  --body "<filled PR body>" \
  --label <one or more: bug,documentation,size/large,size/small> \
  --reviewer aferracci,cristianosticca-pagopa,marcopiccoloalten-hash,marcods02,daniele-quero \
  --assignee <gh-user>
```
