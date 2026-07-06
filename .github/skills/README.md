# .github/skills

Questa cartella raccoglie le **skill** del repository: file `SKILL.md` che
descrivono procedure operative riusabili, consumate dagli agenti e dai prompt
custom.

Ogni skill vive in `<root>/.github/skills/<skill-name>/SKILL.md` e funge da
*single source of truth* tecnica per un dominio specifico.

## Contenuto attuale

| Skill | Scopo | Consumata da |
| --- | --- | --- |
| [mermaid-flow/SKILL.md](mermaid-flow/SKILL.md) | Generazione flow Mermaid Markdown (e SVG opzionale) per asset del repo | [Mermaid-flow-engineer.agent.md](../agents/Mermaid-flow-engineer.agent.md), [mermaid-flow.prompt.md](../prompts/mermaid-flow.prompt.md) |
| [marp-presentation/SKILL.md](marp-presentation/SKILL.md) | Autoring di deck Marp con interview su stile/tono e palette derivata per cromoarmonia | [Marp-presentation-engineer.agent.md](../agents/Marp-presentation-engineer.agent.md), [marp-presentation.prompt.md](../prompts/marp-presentation.prompt.md) |

## Convenzioni

- Una skill = una cartella = un file `SKILL.md`.
- Frontmatter YAML con `name`, `description`, opzionale `applyTo`.
- Il corpo della skill descrive: scopo, output contract, regole, prerequisiti,
  procedura, definition of done.
- La skill non esegue azioni: definisce solo il "come". Le azioni vengono
  eseguite dagli agenti o dai prompt che la richiamano.

## Relazione con agent e prompt

- Gli **agenti** (`.github/agents/*.agent.md`) leggono la skill all'inizio del
  workflow per applicarla con i propri tool.
- I **prompt** (`.github/prompts/*.prompt.md`) delegano agli agenti che
  conoscono la skill rilevante.
