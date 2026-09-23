---
# Catalog metadata anchors (do not edit manually)
source: pagopa-platform-mcp
source_version: 1.1.0
source_digest: sha256:803b32b852d72e67d3fe173c24ffca848d237f0be99c75b5f0626fe72be44eeb
source_id: git-commit-guidelines
---

# Commit Guidelines

## Assess terminal

Determine which terminal is in use (e.g., bash, zsh, cmd, PowerShell) to ensure compatibility with git commands and input/output parsing.

## Allowed commit types

Every commit message must start with one of:

- `feat` new feature or test scenario
- `fix` bug fix
- `chore` maintenance (deps/config/tooling)
- `docs` documentation-only changes
- `refactor` code restructuring without behavior change
- `test` new or updated test cases
- `style` formatting, whitespace, or linting changes
- `perf` performance improvements
- `ci` continuous integration or build system changes
- `build` build system changes (e.g., Gradle, Maven, Make)
- `BREAKING CHANGE` for commits that introduce backward-incompatible changes

## Message format

- Format: `<type>: <concise summary>`
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
4. If a valid override message is provided, use it; otherwise infer `<type>: <concise summary>` from staged changes.
5. Create commit:

    ```bash
    git commit -m "<message>"
    ```

6. Push branch according to upstream status (see Push section).
    - If branch has no upstream:
        ```bash
        git push --set-upstream origin <current-branch>
        ```
    - Otherwise:
        ```bash
        git push
        ```

## Output

Return only:

- commit message (do not run commands, use the message already inferred in the workflow)
- commit hash
- push result

## Fallback for unclear summary

Use detailed per-file stats only if needed to disambiguate the summary:

```bash
git diff --cached --stat
```
