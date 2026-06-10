---
# No applyTo: loaded explicitly by /commit and QA-closer.
---

# Commit Guidelines

## Assess terminal

Determine which terminal is in use (e.g., bash, zsh, cmd, PowerShell) to ensure compatibility with git commands and input/output parsing.

## Allowed prefixes

Every commit message must start with one of:

- `feat` new feature or test scenario
- `fix` bug fix
- `chore` maintenance (deps/config/tooling)
- `docs` documentation-only changes
- `refactor` code restructuring without behavior change

## Message format

- Format: `<prefix>: <concise summary>`
- Keep summary specific and action-oriented.
- Infer the summary from staged changes (`git diff --cached --name-only` + `git diff --cached --shortstat`).

## Workflow

1. Read allowed prefixes.
2. Inspect staged changes with:

```bash
git diff --cached --name-only
git diff --cached --shortstat
```

3. If no files are staged, stage intended files (use user-provided paths when available, otherwise `git add -A`) and re-check.
4. If a valid override message is provided, use it; otherwise infer `<prefix>: <concise summary>` from staged changes.
5. Create commit:

```bash
git commit -m "<message>"
```

6. Push branch according to upstream status (see Push section).

## Output

Return only:

- commit message
- commit hash
- push result

## Fallback for unclear summary

Use detailed per-file stats only if needed to disambiguate the summary:

```bash
git diff --cached --stat
```

## Push

- If branch has no upstream: `git push --set-upstream origin <current-branch>`
- Otherwise: `git push`
