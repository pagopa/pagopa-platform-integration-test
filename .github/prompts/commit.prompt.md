---
description: 'Create a commit with a compliant message from staged changes and push the current branch'
argument-hint: "Optional: message override, scope hint, or extra context"
model: "GPT-5 mini"
agent: agent
---

Use [`.github/instructions/git-commit.instructions.md`](../../.github/instructions/git-commit.instructions.md) as the canonical source of truth for allowed commit prefixes and workflow conventions.

Follow that instruction file end-to-end.

If input provides a valid message override, use it.

Return only:
- commit message
- commit hash
- push result

${input:Optional context — message override, scope hint, or notes}
