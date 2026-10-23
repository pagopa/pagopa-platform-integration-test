# Agenti

Gli agenti definiscono responsabilita, strumenti e limiti; persona e workflow
collegati nei rispettivi file sono il contratto operativo completo.
Selezionare un agente invocabile nel client e indicare attivita, input, scope
e risultato atteso. Per runner e closer, non invocabili direttamente, passare
dall'orchestratore.

## Catalogo e uso

| Agente | Accesso | Responsabilita e limiti | Esempio di richiesta |
| --- | --- | --- | --- |
| [QA-orchestrator](QA-orchestrator.agent.md) | Diretto | Coordina il lavoro QA e le deleghe; distingue nuovo lavoro, ripresa ed esplorazione. Non scrive feature o Python. | «Esplora la copertura WISP: restituisci gap e piano, senza modifiche o esecuzioni.» |
| [QA-analyst](QA-analyst.agent.md) | Diretto | Review, modifica e creazione Gherkin da UC/documentazione. Non scrive Python e non esegue test. | «Analizza le feature allegate in sola lettura; segnala problemi con riferimenti di riga.» |
| [QA-engineer](QA-engineer.agent.md) | Diretto | Review e implementazione di binding Python e wiring autorizzato. Delega le utility; restituisce `implemented-not-run`, non esegue test. | «Implementa gli step della feature allegata nella suite WISP, senza cambiare la feature o eseguire test.» |
| [Python-utility-engineer](Python-utility-engineer.agent.md) | Diretto | Utility condivise/locali, export, test unitari e documentazione correlata. Non modifica step/hook e non esegue comandi. | «Rivedi l'utility allegata: verifica contratto e compatibilita dei chiamanti, senza modifiche.» |
| [QA-runner](QA-runner.agent.md) | Delega | Esegue/diagnostica su piano approvato; non modifica codice/configurazione. Dopo il fallimento iniziale consente fino a cinque fix bonus autorizzati, oppure report diretto. | All'orchestratore: «Fai eseguire WISP in UAT: prima mostrami il piano; nessun fix automatico.» |
| [Qa-closer](Qa-closer.agent.md) | Delega | Documentazione e pubblicazione con evidenze correnti e permessi separati per commit/push/PR; report-only per errori residui. Non esegue test. | All'orchestratore: «Con le evidenze runner correnti, delega la sola chiusura documentale; niente commit, push o PR.» |
| [gh/ace/reflector](ACE-reflector.agent.md) | Diretto / ciclo ACE | Analizza batch di tracce e produce proposte supportate da evidenze; non modifica playbook. | «Analizza il batch di tracce sanitizzate indicato e produci le proposte previste dal contratto.» |
| [gh/ace/curator](ACE-curator.agent.md) | Diretto / ciclo ACE | Converte proposte in decisioni tipizzate per il warden; non le applica. | «Valuta le proposte allegate con le relative evidenze; prepara le decisioni, senza applicarle.» |
| [gh/ace/warden](ACE-warden.agent.md) | Diretto / ciclo ACE | Esegue il gate e applica decisioni solo con le conferme umane richieste. Unico writer dei playbook. | «Esegui il gate sulle decisioni indicate; presenta l'esito e chiedi conferma prima di ogni applicazione.» |

## Regole comuni

- Review non significa autorizzazione a modificare; implementazione non significa
  test superati o permesso di pubblicare.
- Dichiarare suite, ambiente, percorsi e autorizzazioni pertinenti. Gli agenti
  chiedono chiarimenti quando gli input non bastano.
- Le lezioni ACE restano scoped al ruolo. Non avviare il ciclo per aggirare
  approvazioni; le tracce vanno sanitizzate prima di essere consumate.
- I wrapper ACE sono generati: modifiche al loro contratto passano dai prompt
  sorgente collegati, non da questo indice.

Vedi anche [skill](../skills/README.md), [istruzioni](../instructions/README.md)
e [regole del repository](../../AGENTS.md).
