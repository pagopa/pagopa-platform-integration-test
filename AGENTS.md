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

## Python script instruction rule (all coding agents)

Applies to custom agents and non-custom coding agents working in this repository.

1. Before creating or editing any `.py` file, read [`.github/instructions/python-scripts.instructions.md`](.github/instructions/python-scripts.instructions.md).
2. When editing behave step files (`src/**/steps/**/*.py`), also read [`.github/instructions/behave-steps.instructions.md`](.github/instructions/behave-steps.instructions.md).

## Agent instruction loading policy

Each agent loads **only** the instruction and skill files explicitly referenced in its own `.agent.md` via `read_file`. The `applyTo` patterns in `.instructions.md` files apply to non-agent contexts (inline Copilot, default mode); they do not restrict or extend what an agent reads. For the exact list of files each agent consumes, see [`.github/agents/`](.github/agents/).