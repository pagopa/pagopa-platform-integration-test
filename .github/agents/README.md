# Agenti

Gli agenti definiscono responsabilità, strumenti e limiti; persona e workflow
collegati nei rispettivi file sono il contratto operativo completo.
Selezionare un agente invocabile nel client e indicare attività, input, scope
e risultato atteso. Per runner e closer, non invocabili direttamente, passare
dall'orchestratore.

## Catalogo e uso

| Agente | Accesso | Responsabilità e limiti | Esempio di richiesta |
| --- | --- | --- | --- |
| [QA-orchestrator](QA-orchestrator.agent.md) | Diretto | Coordina il lavoro QA e le deleghe; distingue nuovo lavoro, ripresa ed esplorazione. Non scrive feature o Python. | «Esplora la copertura WISP: restituisci gap e piano, senza modifiche o esecuzioni.» |
| [QA-analyst](QA-analyst.agent.md) | Diretto | Review, modifica e creazione Gherkin da UC/documentazione. Non scrive Python e non esegue test. | «Analizza le feature allegate in sola lettura; segnala problemi con riferimenti di riga.» |
| [QA-engineer](QA-engineer.agent.md) | Diretto | Review e implementazione di binding Python e wiring autorizzato. Delega le utility; restituisce `implemented-not-run`, non esegue test. | «Implementa gli step della feature allegata nella suite WISP, senza cambiare la feature o eseguire test.» |
| [Python-utility-engineer](Python-utility-engineer.agent.md) | Diretto | Utility condivise/locali, export, test unitari e documentazione correlata. Non modifica step/hook e non esegue comandi. | «Rivedi l'utility allegata: verifica contratto e compatibilità dei chiamanti, senza modifiche.» |
| [QA-runner](QA-runner.agent.md) | Delega | Esegue/diagnostica su piano approvato; non modifica codice/configurazione. Dopo il fallimento iniziale consente fino a cinque fix bonus autorizzati, oppure report diretto. | All'orchestratore: «Fai eseguire WISP in UAT: prima mostrami il piano; nessun fix automatico.» |
| [Qa-closer](Qa-closer.agent.md) | Delega | Documentazione e pubblicazione con evidenze correnti e permessi separati per commit/push/PR; report-only per errori residui. Non esegue test. | All'orchestratore: «Con le evidenze runner correnti, delega la sola chiusura documentale; niente commit, push o PR.» |
| [gh/ace/reflector](ACE-reflector.agent.md) | Diretto / ciclo ACE | Analizza batch di tracce e produce proposte supportate da evidenze; non modifica playbook. | «Analizza il batch di tracce sanitizzate indicato e produci le proposte previste dal contratto.» |
| [gh/ace/curator](ACE-curator.agent.md) | Diretto / ciclo ACE | Converte proposte in decisioni tipizzate per il warden; non le applica. | «Valuta le proposte allegate con le relative evidenze; prepara le decisioni, senza applicarle.» |
| [gh/ace/warden](ACE-warden.agent.md) | Diretto / ciclo ACE | Esegue il gate e applica decisioni solo con le conferme umane richieste. Unico writer dei playbook. | «Esegui il gate sulle decisioni indicate; presenta l'esito e chiedi conferma prima di ogni applicazione.» |

## Tool nei due harness

I frontmatter usano gli alias condivisi da Local (chat classica di VS Code)
e Copilot (harness agentico), selezionati secondo le responsabilità del ruolo:

| Alias nel frontmatter | Local | Copilot |
| --- | --- | --- |
| `read` | Lettura, ad esempio `read/readFile` | Lettura con i tool del runtime, ad esempio `view` |
| `edit` | Creazione e modifica tramite i tool di editing | Editing del runtime, ad esempio `apply_patch` |
| `search` | Ricerca di file e testo | Ricerca del runtime, ad esempio `glob` e `rg` |
| `execute` | Comandi nel terminale integrato | Shell del runtime, ad esempio `powershell` su Windows |
| `agent` | Delega tramite `agent/runSubagent` | Delega tramite `task` |
| `web` | Tool web, ad esempio `web/fetch` | Ricerca e lettura web del runtime |

Per le domande, dichiarare `vscode/askQuestions` e `ask_user`: il primo è il
riferimento del client VS Code; il secondo è il tool nativo esposto dal runtime
Copilot in questa sessione. Non sono alias condivisi: la disponibilità dipende
dall'inventario della sessione. I nomi non riconosciuti vengono ignorati;
la dichiarazione non installa né abilita un tool assente. Il warden deve fermarsi
se manca un tool domande, come previsto dal suo contratto.

Gli alias selezionano gruppi di capacità, non impongono limiti su file o comandi.
Restano quindi validi i vincoli dei ruoli, inclusi il divieto di esecuzione per
gli implementatori e il solo comando linguistico consentito all'analista.
I modelli e gli altri campi del frontmatter non vengono uniformati da questi alias;
in particolare `agents` configura le deleghe in Local, non nel runtime Copilot.

Per cambiare i tool dei wrapper ACE, aggiornare
[`ace/config/project.json`](../../ace/config/project.json), poi rigenerare dalla
root con `node ace\scripts\generate_ace_agents.js`. Verificare con
`node ace\scripts\generate_ace_agents.js --check`.

Riferimenti: [frontmatter e compatibilità VS Code](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference#_tools),
[alias e nomi non riconosciuti](https://docs.github.com/en/copilot/reference/custom-agents-configuration#tools)
e [migrazione dei tool](https://code.visualstudio.com/docs/agent-customization/migrate-customizations#_why-does-an-agent-fail-with-a-tool-discovery-capability-error).
Per la verifica operativa, aprire una nuova sessione in ciascun harness e
controllare i tool effettivamente disponibili; il solo frontmatter non dimostra
che una capacità sia utilizzabile.

### Allowlist delle deleghe in Copilot

Copilot non legge `agents`. Per questo tutti gli agenti che delegano
(QA-orchestrator, QA-engineer, QA-runner, gh/ace/reflector e gh/ace/curator)
dichiarano anche un hook `preToolUse` a livello di agente che esegue
[`delegation-allowlist.js`](../hooks/scripts/delegation-allowlist.js) con gli
stessi nomi dell'allowlist Local. Lo script nega le chiamate a `task` (o `Agent`)
verso agenti non elencati, inclusi gli agenti built-in e gli id generati
`vscode-agent-*`. Il confronto dei nomi non distingue maiuscole e minuscole.
Se si cambia una delega, aggiornare insieme `agents` e gli argomenti dell'hook.

Limiti:

- GitHub documenta gli hook a livello di agente solo per Copilot CLI, quindi
  l'applicazione nel runtime Copilot di VS Code va verificata in una sessione reale.
- Un timeout dell'hook lascia proseguire la chiamata (fail-open); un errore la nega.
- Serve Node.js 18+ nel `PATH`. L'hook passa da un lanciatore,
  [`delegation-allowlist.ps1`](../hooks/scripts/delegation-allowlist.ps1) su Windows e
  [`delegation-allowlist.sh`](../hooks/scripts/delegation-allowlist.sh) altrove, che
  verifica Node prima di avviare lo script. Senza Node nega solo le deleghe, con un
  motivo esplicito, e lascia utilizzabili gli altri tool.
- Nei wrapper ACE l'hook è scritto da
  [`generate_ace_agents.js`](../../ace/scripts/generate_ace_agents.js) per la piattaforma
  Copilot, a partire dalle deleghe dei ruoli: non va modificato a mano. Il generatore
  è kit-owned; questa modifica locale ha aggiornato il suo hash in
  [`runtime-version.json`](../../ace/runtime-version.json) e va riapplicata se il kit
  ACE viene aggiornato.

Riferimento: [hook a livello di agente](https://docs.github.com/en/copilot/reference/hooks-reference#agent-scoped-hooks).

## Regole comuni

- Review non significa autorizzazione a modificare; implementazione non significa
  test superati o permesso di pubblicare.
- Dichiarare suite, ambiente, percorsi e autorizzazioni pertinenti. Gli agenti
  chiedono chiarimenti quando gli input non bastano.
- Orchestratore e analista seguono il
  [protocollo di interazione](../../docs/workflows/qa-orchestrator/operations.md#human-interaction-and-harness-compatibility):
  tool domande se disponibile, altrimenti chat con risposta umana esplicita;
  l'orchestratore media le domande dell'analista delegato. La delega deve usare
  il `QA-analyst` registrato, mai un agente inventato o generico rinominato.
- Le lezioni ACE restano scoped al ruolo. Non avviare il ciclo per aggirare
  approvazioni; le tracce vanno sanitizzate prima di essere consumate.
- I wrapper ACE sono generati: modifiche al loro contratto passano dai prompt
  sorgente collegati, non da questo indice.

Vedi anche [skill](../skills/README.md), [istruzioni](../instructions/README.md)
e [regole del repository](../../AGENTS.md).
