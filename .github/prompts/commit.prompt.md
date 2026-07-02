---
description: 'Create a commit with a compliant message from staged changes and push the current branch'
argument-hint: "Optional: message override, scope hint, or extra context"
model: "GPT-5 mini"
agent: agent
---

Call `read_file` on [`.github/instructions/git-commit.instructions.md`](../../.github/instructions/git-commit.instructions.md) as the canonical source of truth for allowed commit prefixes and workflow conventions.

Follow that instruction file end-to-end.

If input provides a valid message override, use it. A valid message should be recognized as a complete commit message, including a prefix and a short description. If the message is not valid, use it as context to generate a compliant commit message or to modify the actions to be taken.

Return only:
- commit message
- commit hash
- push result

${input:Optional context — message override, scope hint, or notes}
