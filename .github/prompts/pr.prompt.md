---
description: 'Create a pull request for the current branch following project conventions'
argument-hint: "Optional: branch name, PR title override, or extra context"
model: "GPT-5 mini"
---

Use `.github/instructions/git-pr.instructions.md` as the canonical source of truth for pull request rules and metadata.

Steps:
1. Read and follow `.github/instructions/git-pr.instructions.md`.
2. Run `git log main..HEAD --oneline -n 40` and `git diff main...HEAD --stat` to gather the change summary.
3. Compose the PR body following `.github/PULL_REQUEST_TEMPLATE.md` sections as an inline string.
4. Resolve assignee with `gh api user --jq ".login"`, then run `gh pr create` using labels/reviewers/rules from `.github/instructions/git-pr.instructions.md`.
5. Return a concise output with only: PR title, labels, assignee, and PR URL.

${input:Optional context — branch name, title override, or notes for the PR body}
