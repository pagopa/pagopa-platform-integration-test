# .github/instructions

Questa cartella contiene le regole operative e di stile che guidano agenti e workflow.
I file `.instructions.md` sono la fonte canonica per convenzioni di test, coding Python,
Gherkin, commit e pull request.

## Obiettivo della cartella

- Rendere esplicite le policy del repository.
- Ridurre incoerenze tra suite e contributori.
- Fornire regole verificabili e riusabili dagli agenti.

## Contenuto attuale

| File | Ambito | Pattern/uso principale |
| --- | --- | --- |
| [python-scripts.instructions.md](python-scripts.instructions.md) | Script Python | `applyTo: **/*.py` |
| [behave-steps.instructions.md](behave-steps.instructions.md) | Step behave | `applyTo: src/**/steps/**/*.py` |
| [gherkin.instructions.md](gherkin.instructions.md) | Feature Gherkin | `applyTo: src/**/*.feature` |
| [gherkin-confluence-sync.instructions.md](gherkin-confluence-sync.instructions.md) | Sincronizzazione Confluence dei feature file | `applyTo: src/**/*.feature` |
| [run-tests.instructions.md](run-tests.instructions.md) | Esecuzione test | Caricato esplicitamente da QA Runner |
| [git-commit.instructions.md](git-commit.instructions.md) | Commit policy | Caricato esplicitamente da `/commit` e QA Closer |
| [git-pr.instructions.md](git-pr.instructions.md) | PR policy | Caricato esplicitamente da `/pr` e QA Closer |

## Dipendenze e precedenze

Le regole sono cumulative quando gli scope si sovrappongono.

Esempio tipico:

1. File step Python in `src/**/steps/**/*.py`:
   - prima si applica [python-scripts.instructions.md](python-scripts.instructions.md),
   - poi si applica [behave-steps.instructions.md](behave-steps.instructions.md).
2. File `.feature`:
   - si applica [gherkin.instructions.md](gherkin.instructions.md);
   - si applica anche [gherkin-confluence-sync.instructions.md](gherkin-confluence-sync.instructions.md) per i metadati Confluence.

Per workflow git/test:

- `QA-runner` usa [run-tests.instructions.md](run-tests.instructions.md).
- `QA-closer` e prompt `/commit` usano [git-commit.instructions.md](git-commit.instructions.md).
- `QA-closer` e prompt `/pr` usano [git-pr.instructions.md](git-pr.instructions.md).

## Regole principali per area

### Python

- Docstring in inglese obbligatorie per ogni funzione.
- Stile coerente con il modulo circostante.
- Commenti inline solo per logica non ovvia.

### Behave steps

- Organizzazione step in file per scenario o gruppi omogenei (no file monolitico).
- Riuso utility condivise (`src/utility`) prima di introdurre nuovo codice.
- Fail-fast e gestione stato `context` senza leakage tra scenari.

### Gherkin

- Testi in italiano (keyword Gherkin non tradotte).
- Formattazione e indentazione coerenti.
- Tag e naming mantenuti, con attenzione alla riusabilita degli step.

### Commit/PR

- Commit prefix consentiti e formato messaggio vincolato.
- PR create seguendo template e metadata richiesti (label/reviewer/assignee).

## Come aggiornare una instruction

1. Identificare gli agenti/prompt che dipendono dal file.
2. Applicare modifiche minime e atomiche.
3. Verificare che `applyTo` resti corretto.
4. Aggiornare documentazione correlata in:
   - [../agents/README.md](../agents/README.md)
   - [../prompts/README.md](../prompts/README.md)
5. Includere motivazione chiara nel commit.

## Esempi pratici

### Esempio 1: nuova regola per step behave

- Modifica [behave-steps.instructions.md](behave-steps.instructions.md).
- Verifica impatto su `QA-engineer` e `Python-utility-engineer`.

### Esempio 2: nuova policy commit

- Modifica [git-commit.instructions.md](git-commit.instructions.md).
- Verifica allineamento con [../prompts/commit.prompt.md](../prompts/commit.prompt.md) e `QA-closer`.

## Checklist pre-PR (cartella instruction)

- [ ] Scope `applyTo` corretto e non ambiguo.
- [ ] Regole testabili e non contraddittorie.
- [ ] Coerenza con agenti e prompt dipendenti.
- [ ] Esempi e comandi ancora validi.
- [ ] Nessuna duplicazione inutile tra file instruction.
