---
description: 'Create a pull request for the current branch following project conventions'
argument-hint: "Optional: branch name, PR title override, or extra context"
---

Follow the **Pull request workflow** section in `AGENTS.md` to create a pull request for the current branch.

Steps:
1. Run `git log main..HEAD --oneline` and `git diff main...HEAD --stat` to gather the change summary.
2. Compose the PR body following the structure in `.github/PULL_REQUEST_TEMPLATE.md`. Do NOT pass the template file directly — compose the body as an inline string.
3. Run `gh pr create` with title, body, labels, reviewers (`aferracci`, `cristianosticca-pagopa`, `marcopiccoloalten-hash`, `marcods02`), and assignee (`daniele-quero`).

${input:Optional context — branch name, title override, or notes for the PR body}
