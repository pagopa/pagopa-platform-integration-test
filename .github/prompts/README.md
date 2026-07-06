# .github/prompts

Questa cartella contiene prompt riusabili che incapsulano task operativi ricorrenti
per il team QA e per il workflow git.

Ogni file `.prompt.md` definisce:

- descrizione del comando,
- agente target,
- eventuale modello,
- template di input con placeholder `${input:...}`.

## Obiettivo della cartella

- Uniformare i comandi frequenti (`/qa`, `/commit`, `/pr`, `/promptize`).
- Ridurre errori manuali su convenzioni di commit e PR.
- Rendere ripetibile la trasformazione di richieste libere in istruzioni operative.

## Contenuto attuale

| File | Scopo | Agente target |
| --- | --- | --- |
| [qa.prompt.md](qa.prompt.md) | Avvia il processo QA iterativo tramite orchestrazione | `QA-orchestrator` |
| [commit.prompt.md](commit.prompt.md) | Guida commit e push conformi alle linee guida | `agent` |
| [pr.prompt.md](pr.prompt.md) | Guida creazione PR conforme a template e policy | `agent` |
| [promptize.prompt.md](promptize.prompt.md) | Converte una richiesta libera in template operativo completo | `Ask` |
| [sync-folder.prompt.md](sync-folder.prompt.md) | Fetch branch remoto e checkout selettivo di una cartella nel working tree | `agent` |
| [mermaid-flow.prompt.md](mermaid-flow.prompt.md) | Genera/aggiorna flow diagram Mermaid (Markdown sempre, SVG opzionale) | `Mermaid-flow-engineer` |
| [marp-presentation.prompt.md](marp-presentation.prompt.md) | Crea/aggiorna deck Marp con interview su stile, tono e palette | `Marp-presentation-engineer` |

## Come usare i prompt

L'invocazione dipende dalla configurazione locale dei prompt custom.
In una configurazione slash tipica, l'uso e:

```text
/qa <task-id, suite, obiettivo>
/commit <eventuale override del messaggio>
/pr <eventuale titolo o note PR>
/promptize <richiesta da strutturare>
/sync-folder <branch> [folder]
/mermaid-flow <source files or categories> [orientation=TD|LR] [svg=yes|no]
/marp-presentation <topic> [audience] [duration] [style] [tone] [colors]
```

Se il prompt non riceve input esplicito, alcuni file sono progettati per usare il contesto chat corrente.

## Convenzioni di scrittura dei prompt

- Usare frontmatter YAML minimo e chiaro.
- Mantenere una responsabilita singola per file prompt.
- Inserire `argument-hint` quando l'input utente puo essere ambiguo.
- Specificare output atteso in modo restrittivo quando serve automazione affidabile.
- Evitare logica procedurale complessa nel prompt quando puo vivere nelle instruction o negli agent.

## Relazione con altri asset `.github`

- Prompt git devono allinearsi a:
  - [../instructions/git-commit.instructions.md](../instructions/git-commit.instructions.md)
  - [../instructions/git-pr.instructions.md](../instructions/git-pr.instructions.md)
- Prompt QA deve allinearsi a:
  - [../agents/QA-orchestrator.agent.md](../agents/QA-orchestrator.agent.md)
- Prompt di formattazione richieste (`promptize`) e indipendente dal codice ma deve rispettare il template dichiarato nel file.

## Esempi pratici

### Esempio 1: commit guidato

Input utente:

```text
/commit docs: aggiorna README suite cart
```

Comportamento atteso:

- Applica le regole in [../instructions/git-commit.instructions.md](../instructions/git-commit.instructions.md).
- Restituisce solo messaggio, hash commit, risultato push.

### Esempio 2: richiesta QA completa

Input utente:

```text
/qa FEAT-123 cart validare scenari checkout con env dev
```

Comportamento atteso:

- Delega ai sub-agent secondo workflow definito in [../agents/QA-orchestrator.agent.md](../agents/QA-orchestrator.agent.md).

## Checklist pre-PR (cartella prompt)

- [ ] Ogni prompt ha frontmatter valido.
- [ ] `description` e coerente con il comportamento reale.
- [ ] Placeholder `${input:...}` presenti quando necessari.
- [ ] Riferimenti a instruction/agent aggiornati.
- [ ] Output richiesto chiaramente vincolato nei prompt operativi.
