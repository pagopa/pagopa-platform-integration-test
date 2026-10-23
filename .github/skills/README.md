# Skill

Una skill e una procedura riusabile, non un agente. Richiederla per nome
(`Usa <nome> ...`) con file/input e risultato atteso; l'assistente legge il
relativo `SKILL.md` e rispetta i permessi del ruolo attivo.
Gli esempi seguenti sono richieste in chat, non comandi shell.

## Catalogo e uso

| Skill | Scopo e input principali | Esempio di richiesta |
| --- | --- | --- |
| [ppa-commit](ppa-commit/SKILL.md) | Commit conforme e push del branch corrente; scope e messaggio opzionali. Rispetta `commit-only`/`no-push`, staging e gate QA. | «Usa ppa-commit solo per le modifiche documentali indicate, senza push.» |
| [ppa-pr](ppa-pr/SKILL.md) | Crea PR con template, reviewer obbligatori e branch risolti. Per una suite usa il suo `id` NRT e una label release; senza suite usa `skip`, senza incremento. Non autorizza commit/push/merge. | «Usa ppa-pr dal branch corrente al default del repository; reviewer: `<login-github>`.» |
| [ppa-readme](ppa-readme/SKILL.md) | Valuta e aggiorna solo il README interessato dallo scope; nessun test o Git implicito. | «Usa ppa-readme per documentare le modifiche del workflow runner, senza eseguire i comandi descritti.» |
| [review-feature-files](review-feature-files/SKILL.md) | Review read-only delle feature allegate/indicate tramite QA-analyst; rilievi in chat o report esplicitamente richiesto. | «Usa review-feature-files sulle feature allegate; solo rilievi in chat, nessuna modifica.» |
| [review-behave-steps](review-behave-steps/SKILL.md) | Review read-only degli step Python allegati/indicati tramite QA-engineer; non implementa o esegue test. | «Usa review-behave-steps sugli step allegati; verifica binding e assertion senza modificare file.» |
| [uc-to-feature](uc-to-feature/SKILL.md) | Traduce un UC umano in Gherkin tramite QA-analyst; richiede UC, destinazioni e input di profilo. Coordina contesto, dati e report di copertura. | «Usa uc-to-feature con l'UC allegato per WISP; concordiamo prima percorsi di output e tracking.» |
| [uc-scenario-context](uc-scenario-context/SKILL.md) | Recupera dettaglio funzionale da fonti ammesse tramite QA-analyst; produce `01-context.md`, non valori di test o Python. | «Usa uc-scenario-context sull'UC e sulle specifiche allegate; chiarisci sequenze e risultati attesi.» |
| [uc-test-data](uc-test-data/SKILL.md) | Risolve valori/stati di input tramite QA-analyst da contesto corrente e fonti ammesse; produce `02-test-data.md`, con approvazione dei candidati e TODO per gap. | «Usa uc-test-data nella run UC indicata; proponi dati UAT con provenienza, senza eseguire chiamate.» |
| [add-catalog-asset](add-catalog-asset/SKILL.md) | Prepara manifest/body MCP da un vero Markdown sorgente. Richiede sorgente e metadati; applicabile dove e disponibile lo scaffold catalogo, non installa l'asset nel runtime. | «Usa add-catalog-asset sullo SKILL.md allegato; concordiamo ID, versione e destinazione nel catalogo.» |

## Vincoli operativi

- Le tre skill UC passano da QA-analyst. Il loro
  [workflow persistente](../../docs/use-cases/uc-workflow.md) gestisce registro,
  revisioni e ripresa: contesto, dati, poi feature/report; niente dati inventati.
- Le skill di review non producono copie corrette. Scrivere un report richiede
  richiesta esplicita e destinazione concordata.
- Per PR, [il catalogo NRT](../nrt-suites.json) usa `id`, non la `label`
  descrittiva. Scope multi-suite o irrisolto richiede chiarimento, non `skip`.
- Leggere i file companion quando richiesto dalla skill; questo indice non ne
  sostituisce procedure, prerequisiti o approvazioni.

Vedi anche [agenti](../agents/README.md), [istruzioni](../instructions/README.md)
e [profili](../profiles/README.md).
