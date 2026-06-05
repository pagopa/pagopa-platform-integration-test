# AGENTS.md

Scope: pagopa-platform-integration-test root.
Canonical agent instructions for this repo (Copilot/Claude); use [README.md](README.md) for general project context and keep this file focused on operative rules.

## Repository quick map

- Test suites: `src/api/<suite>`, `src/integration/<suite>`, `src/e2e/<suite>`.
- Environment files: `config/<suite-type>/.env.<env>`.
- Run every command from the repository root.
- Detailed project structure and run conventions: [README.md](README.md) sections `Struttura del repository`, `Configurazione`, `Esecuzione locale`.

## Gherkin Guidelines

- One `Feature` per file, named descriptively.
- Keep steps atomic and reusable.
- Use `Background` for shared preconditions.
- Tag scenarios with relevant labels (`@smoke`, `@regression`, `@<suite-name>`).
- Don't remove existing tags.
- Write in the italian language version of Gherkin.
- Use proper italian grammar and consistent terminology across feature files, beware accent marks, DO NOT translate keywords or acronyms. Techical terms may remain in english (login, token, API, etc.).
- Max 12 scenarios per feature file to maintain readability: split into multiple files if needed, by semantic.
- Use consistent formatting and indentation.
- Use third person present tense for steps (e.g., "l'utente effettua il login", not "io effettuo il login").
- Search the codebase for existing feature files to match the style and language used in the project and ask the user which to follow as a blueprint.

## Run API suite

Placeholders: `<suite>` = `cart` | `auth-service` | `checkout-npg` | `ecommerce-cdc` (or other in future)— `<env>` = `dev` | `uat`

```powershell
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue "reports\allure-results\<suite>-<env>"
New-Item "reports\allure-results\<suite>-<env>" -ItemType Directory -Force | Out-Null
behave src\api\<suite> -D env=<env> `
    -f allure_behave.formatter:AllureFormatter -o reports\allure-results\<suite>-<env> `
    -f progress --summary --show-timings
```

## Run Integration tests in UAT

```text
# Set the environment to UAT
$env:TARGET_ENV="uat"

# Run the WISP test suite with Allure reporting
behave src/bdd/wisp --tags=@runnable `
    --format allure_behave.formatter:AllureFormatter -o allure-results `
    --junit-directory=junit --junit --summary --show-timings -v
```

## View the Allure report

Use **absolute paths** — the integrated terminal may start from a parent folder and relative paths can resolve incorrectly.

```text
# <port> = any free port, e.g. 5300
allure serve "\reports\allure-results\<suite>-<env>" --port <port>
```

## Validation rules

- All scenarios must pass (0 failures) before the task is considered done, unless otherwise specified.
- On certificate errors: keep `http_client.py` in place, diagnose the OS trust store — do **not** set `verify=False`.

## Commit message guidelines

Every commit message **must** start with one of the following prefixes:

| Prefix | When to use |
|--------|-------------|
| `feat:` | A new feature or test scenario |
| `fix:` | A bug fix |
| `chore:` | Maintenance tasks (deps, config, tooling) |
| `docs:` | Documentation-only changes |
| `refactor:` | Code restructuring without behaviour change |

**Examples**:
```
feat: add checkout-npg payment flow scenarios
fix: correct auth-service token refresh assertion
chore: update behave and allure-behave dependencies
docs: document run commands in AGENTS.md
refactor: extract common step definitions to shared module
```

## Pull request workflow

After task completion criteria are met or the user requests it, follow these steps to create a pull request for the current branch:

### 0. Ensure GitHub CLI is available (fail-fast)

Run this fail-fast check before any PR operation:

1. Verify that `gh` is available in PATH:
   - `gh --version`
2. Verify that GitHub authentication is valid:
   - `gh auth status`
3. If `gh` is missing, install GitHub CLI for your OS (package manager or installer from `https://cli.github.com/`) and rerun the checks.
4. If any check fails, stop and do not proceed with PR creation.

### 1. Determine metadata from git history

Run the following to inspect the branch commits since diverging from `main`:

```bash
git log main..HEAD --oneline
```

Use the output to fill the PR body template. Refer to the [PR template](.github/PULL_REQUEST_TEMPLATE.md) for the required structure.

### 2. Resolve assignee and create the pull request

Resolve the current GitHub user login first:

```text
gh api user --jq ".login"
```

Use the returned login value as `<gh-user>` and run:

```text
gh pr create --base main --head <current-branch> --title "<human-readable branch title, e.g. PQ-455 checkout npg api-test suite migration>" --body "<filled PR body — see [§3 PR body](#3-pr-body)>" --label <one or more: bug,documentation,size/large,size/small> --reviewer aferracci,cristianosticca-pagopa,marcopiccoloalten-hash,marcods02 --assignee <gh-user>
```

**Rules**:
- `--reviewer`: always include all four: `aferracci`, `cristianosticca-pagopa`, `marcopiccoloalten-hash`, `marcods02`.
- `--assignee`: resolve from the current GitHub user (`gh api user --jq ".login"`). Do not hardcode usernames.
- `--label`: pick ALWAYS one or more from `bug`, `documentation`, `size/large`, `size/small` based on the scope of changes.
- `--title`: derive from the branch name, making it human-readable (e.g. replace hyphens/underscores with spaces, expand ticket IDs).

### 3. PR body

Read [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) for the required sections and tone. **Do NOT edit or pass that file directly** — it must remain an unmodified template.

Instead, compose the body as an inline string:

1. Run `git log main..HEAD --oneline` and `git diff main...HEAD --stat` to gather the change summary.
2. Fill in each section of the template structure from the information above. Check boxes that apply. Keep it concise but informative, mention only major changes.
3. Pass the composed text as the `--body` argument to `gh pr create`.