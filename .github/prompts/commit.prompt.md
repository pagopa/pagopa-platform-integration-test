---
description: 'Create a commit with a compliant message from staged changes and push the current branch'
argument-hint: "Optional: message override, scope hint, or extra context"
model: "GPT-5 mini"
agent: agent
---

Use [`.github/instructions/git-commit.instructions.md`](../../.github/instructions/git-commit.instructions.md) as the canonical source of truth for allowed commit prefixes and workflow conventions.

Steps:
1. Read [`.github/instructions/git-commit.instructions.md`](../../.github/instructions/git-commit.instructions.md) and derive the allowed commit prefixes.
2. Inspect staged changes with `git diff --cached --name-only` and `git diff --cached --stat`.
3. If no files are staged, stage the intended changes first (use user-provided paths when available; otherwise use `git add -A`) and re-check staged changes.
4. If input includes a valid commit message, use it; otherwise infer a message from staged changes using `<prefix> <concise summary>`.
5. Create the commit with `git commit -m "<message>"`.
6. Push the current branch: if no upstream exists, run `git push --set-upstream origin <current-branch>`; otherwise run `git push`.
7. Return a concise output with only: commit message, commit hash, and push result.

${input:Optional context — message override, scope hint, or notes}
