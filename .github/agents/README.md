# .github/agents

Questa cartella contiene le definizioni operative degli agenti custom del repository.
Ogni file `.agent.md` descrive uno specifico ruolo, i tool consentiti, i vincoli, e
gli eventuali handoff verso altri agenti.

## Obiettivo della cartella

- Standardizzare i comportamenti degli agenti QA e utility.
- Ridurre ambiguita su responsabilita, limiti, e workflow.
- Rendere ripetibile il passaggio tra analisi, implementazione, esecuzione e chiusura.

## Contenuto attuale

| File | Ruolo principale | Quando usarlo |
| --- | --- | --- |
| [Python-utility-engineer.agent.md](Python-utility-engineer.agent.md) | Sviluppo/refactor utility Python | Quando serve creare o aggiornare helper in `src/utility` o utility di suite |
| [QA-analyst.agent.md](QA-analyst.agent.md) | Analisi e scrittura file Gherkin | Quando si deve creare/rivedere una `.feature` |
| [QA-engineer.agent.md](QA-engineer.agent.md) | Implementazione step Python | Quando occorre tradurre scenari Gherkin in step definitions |
| [QA-runner.agent.md](QA-runner.agent.md) | Esecuzione test e diagnosi failure | Quando bisogna eseguire suite, analizzare errori e aprire loop di fix |
| [QA-closer.agent.md](QA-closer.agent.md) | Chiusura task QA | Quando serve aggiornare docs/report e completare git commit/PR |
| [QA-orchestrator.agent.md](QA-orchestrator.agent.md) | Coordinamento end-to-end | Quando si vuole orchestrare il ciclo completo QA |

## Flusso di lavoro consigliato

1. `QA-orchestrator` raccoglie input (task id, suite, obiettivo).
2. `QA-analyst` valida o produce i file feature.
3. `QA-engineer` implementa gli step (e delega utility complesse a `Python-utility-engineer` se necessario).
4. `QA-runner` esegue i test e gestisce il fix loop (max 5 iterazioni).
5. `QA-closer` finalizza documentazione, commit, push e PR (quando previsto).

## Schema handoff (dove e quando)

### Percorso autonomo (orchestratore)

```text
Utente -> QA-orchestrator
		   |- -> QA-analyst (subagent)   [handoff invisibile]
		   |- -> QA-engineer (subagent)  [handoff invisibile]
		   |- -> QA-runner (subagent)    [handoff invisibile]
		   `- -> QA-closer (subagent)    [handoff invisibile, solo se suite verde]
										   |
										   v
								 Fine workflow (autonomo)
```

### Percorso manuale (agent usato standalone)

```text
Utente -> QA-analyst
		   `- -> risposta all'utente + [Implement step definitions] [bottone visibile]
										   |
										   v
								 Utente clicca (oppure no)
```

Nota: nel percorso orchestrato gli handoff avvengono tra subagent senza interazione manuale.
Nel percorso manuale l'handoff compare come azione suggerita/bottone e richiede click dell'utente.

### Matrice handoff

| Da | A | Visibilita | Quando avviene |
| --- | --- | --- | --- |
| `QA-orchestrator` | `QA-analyst` | Invisibile | Inizio workflow QA (nuova suite e fix) |
| `QA-orchestrator` | `QA-engineer` | Invisibile | Dopo analisi, quando bisogna implementare/modificare step |
| `QA-orchestrator` | `QA-runner` | Invisibile | Quando bisogna eseguire test, diagnosticare failure o fare retest |
| `QA-orchestrator` | `QA-closer` | Invisibile | Solo dopo esito positivo della suite (e policy di chiusura) |
| `QA-analyst` | `QA-engineer` | Visibile (bottone) | Se `QA-analyst` e invocato standalone e propone implementazione step |
| `Python-utility-engineer` | `QA-engineer` | Visibile (bottone) | Se utility completata e serve integrazione negli step |
| `QA-engineer` | `QA-orchestrator` | Visibile (bottone) | Se `QA-engineer` e invocato standalone e suggerisce run/finalizzazione |

## Convenzioni dei file `.agent.md`

Ogni file usa frontmatter YAML con campi tipici:

- `description`: scopo dell'agente.
- `model`: modello consigliato.
- `tools`: set strumenti consentiti.
- `agents`: eventuali subagent invocabili.
- `user-invocable`: se invocabile direttamente dall'utente.
- `argument-hint`: suggerimento per input utente.
- `handoffs`: passaggi standard verso altri agenti.

Segue una sezione istruttiva in Markdown con:

- workflow passo-passo,
- vincoli (cosa non fare),
- dipendenze da instruction file in `.github/instructions`.

## Relazione con le instruction

Questi agenti fanno riferimento soprattutto a:

- [../instructions/python-scripts.instructions.md](../instructions/python-scripts.instructions.md)
- [../instructions/behave-steps.instructions.md](../instructions/behave-steps.instructions.md)
- [../instructions/gherkin.instructions.md](../instructions/gherkin.instructions.md)
- [../instructions/run-tests.instructions.md](../instructions/run-tests.instructions.md)
- [../instructions/git-commit.instructions.md](../instructions/git-commit.instructions.md)
- [../instructions/git-pr.instructions.md](../instructions/git-pr.instructions.md)

Aggiornare un agente senza verificare le instruction correlate puo introdurre conflitti di comportamento.

## Linee guida di manutenzione

- Mantenere una singola responsabilita per agente.
- Evitare sovrapposizioni tra ruoli (es. runner non modifica codice).
- Esplicitare sempre limiti e condizioni di stop.
- Definire handoff chiari con prompt sintetici e contestuali.
- Tenere allineate descrizione, tools e workflow reale.

## Esempi pratici

### Esempio 1: nuova suite QA

- Input al coordinatore: task id + suite name + obiettivo.
- Routing atteso: orchestrator -> analyst -> engineer -> runner -> closer.

### Esempio 2: fix su test fallito

- Input al coordinatore: errore test + suite + scenario.
- Routing atteso: orchestrator -> analyst (contesto) -> runner (diagnosi) -> engineer (fix) -> runner (retest).

## Checklist pre-PR (cartella agenti)

- [ ] Ogni agente dichiara strumenti minimi necessari.
- [ ] Workflow coerente con il ruolo dichiarato.
- [ ] Vincoli espliciti e non ambigui.
- [ ] Riferimenti a instruction file aggiornati.
- [ ] Handoff validi e non circolari.
