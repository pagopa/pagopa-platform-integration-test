---
description: 'Fetch a remote branch and checkout only a specific folder into the current working tree'
argument-hint: "<source-branch> [target-folder=.github]"
model: "GPT-5 mini"
agent: agent
---

Fetch a remote branch and pull only a specific folder from it into the current working tree.

## Steps

1. Parse `${input:<source-branch> [target-folder=.github]}`:
   - Extract `branch` (required, first token).
   - Extract `folder` (optional, second token; default: `.github`).

2. Determine which terminal is in use (bash / PowerShell) to format commands correctly.

3. Verify current git context:
   ```
   git branch --show-current
   git status --short
   ```
   If there are uncommitted changes in `<folder>`, warn the user and stop.

4. Fetch the branch from the remote:
   ```
   git fetch origin <branch>
   ```
   If the fetch fails (branch not found, auth error), report the git error message and stop.

5. Checkout only the target folder from the fetched branch:
   ```
   git checkout origin/<branch> -- <folder>
   ```

6. Report the result:
   ```
   git status -- <folder>
   ```

## Representative cases

| Input | branch | folder |
|---|---|---|
| `PQ-523-ai-tool-implementation` | `PQ-523-ai-tool-implementation` | `.github` |
| `PQ-523-ai-tool-implementation .github/agents` | `PQ-523-ai-tool-implementation` | `.github/agents` |
| `main src/utility` | `main` | `src/utility` |

## Return

Return only:
- current branch
- branch fetched
- folder checked out
- list of modified/new files in `<folder>` (from `git status`)
- suggested next action: commit the changes or `git restore --staged <folder>` to undo
