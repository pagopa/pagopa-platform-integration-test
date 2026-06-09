---
# No applyTo: loaded explicitly by /pr and QA-closer.
---

# Pull Request Guidelines

## Preconditions

1. Verify `gh` exists: `gh --version`
2. Verify auth: `gh auth status`
3. Stop if checks fail.

## PR data collection

- Run `git log main..HEAD --oneline -n 40`
- Run `git diff main...HEAD --stat`
- Compose PR body inline using `.github/PULL_REQUEST_TEMPLATE.md` sections (do not pass template file directly).

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
