---
# No applyTo: loaded explicitly by /commit and Qa-closer.
---

# Commit Guidelines

## Allowed prefixes

Every commit message must start with one of:

- `feat:` new feature or test scenario
- `fix:` bug fix
- `chore:` maintenance (deps/config/tooling)
- `docs:` documentation-only changes
- `refactor:` code restructuring without behavior change

## Message format

- Format: `<prefix> <concise summary>`
- Keep summary specific and action-oriented.
- Infer the summary from staged changes (`git diff --cached --name-only` + `git diff --cached --stat`).

## Push

- If branch has no upstream: `git push --set-upstream origin <current-branch>`
- Otherwise: `git push`
