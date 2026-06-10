# AGENTS.md

Scope: pagopa-platform-integration-test root.
Canonical agent instructions for this repo (Copilot/Claude); use [README.md](README.md) for general project context and keep this file focused on operative rules.

## Repository quick map

- Test suites: `src/api/<suite>`, `src/integration/<suite>`, `src/e2e/<suite>`.
- Environment files: `config/<suite-type>/.env.<env>`.
- Shared utilities: `src/utility` (entrypoint README + module README files).
- Run every command from the repository root.
- Detailed project structure and run conventions: [README.md](README.md) sections `Struttura del repository`, `Configurazione`, `Esecuzione locale`.

## Shared utility reuse rule (all coding agents)

Applies to custom agents and non-custom coding agents working in this repository.

1. Before writing new helper code for config loading, REST/SOAP calls, auth, or JSON-path manipulation, check:
   - [src/utility/README.md](src/utility/README.md) 
   - [src/utility/config/README.md](src/utility/config/README.md)
   - [src/utility/rest/README.md](src/utility/rest/README.md)
   - [src/utility/json/README.md](src/utility/json/README.md)
   - [src/utility/soap/README.md](src/utility/soap/README.md)
2. Reuse existing utility APIs from [src/utility](src/utility) whenever they satisfy the scenario.
3. Add new helper layers only when no existing utility fits; keep additions minimal and consistent with the existing utility style.

## Agent-to-Instructions mapping

Each agent reads **only** the instruction files listed for its role. Instructions not listed are out of scope for that agent.

| Agent | Instruction files |
|-------|-------------------|
| `QA-analyst` | [`gherkin.instructions.md`](.github/instructions/gherkin.instructions.md) |
| `QA-engineer` | *(repo map above — no dedicated instruction file)* |
| `QA-runner` | [`run-tests.instructions.md`](.github/instructions/run-tests.instructions.md) |
| `QA-closer` | [`git-commit.instructions.md`](.github/instructions/git-commit.instructions.md), [`git-pr.instructions.md`](.github/instructions/git-pr.instructions.md) |
| `QA-orchestrator` | all of the above (delegates to sub-agents) |

> **Detailed instructions** live in `.github/instructions/`. Do not duplicate content here.