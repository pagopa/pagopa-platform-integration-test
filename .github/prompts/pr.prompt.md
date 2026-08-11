---
description: Create a pull request for the current branch following project conventions
argument-hint: 'Optional: branch name, PR title override, or extra context'
model: GPT-5 mini
agent: agent

# Catalog metadata anchors (do not edit manually)
source: pagopa-platform-mcp
source_version: 1.1.0
source_digest: sha256:a27bc895ba3be37762f5ba6962e04fa3396b3a74d66ab85370acc541e3be44c3
source_id: pr
---

Use [`.github/instructions/git-pr.instructions.md`](../../.github/instructions/git-pr.instructions.md) as the canonical source of truth for pull request rules and metadata, **WITH NO DEVIATIONS**.

Follow that instruction file end-to-end.

If input provides a valid title override, use it.


Return only:
- PR title
- labels
- assignee
- PR URL

${input:Optional context — branch name, title override, or notes for the PR body}
