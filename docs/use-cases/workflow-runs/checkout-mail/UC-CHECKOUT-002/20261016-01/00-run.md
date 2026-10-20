---
schema: uc-workflow/v1
artifact: run
producer_skill: "uc-to-feature"
task_id: "checkout-mail"
uc_id: "UC-CHECKOUT-002"
run_id: "20261016-01"
uc_input: "Allegato chat: UC-CHECKOUT-002 - Validazione sintattica dei campi mail.txt"
uc_revision: "1"
environment: uat
revision: 6
status: complete
updated_at: "2026-10-16T11:50:00+02:00"
inputs: []
---

# UC - Run

## Agreed inputs
| Item | Value | Human confirmation |
| --- | --- | --- |
| Functional sources | Allegato "UC-CHECKOUT-002 - Validazione sintattica dei campi mail.txt"; allegato "Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md" (sezione "Pagina di inserimento Email") | Utente, 2026-10-16 ~11:00 |
| Data sources | Allegato "Note per gli sviluppatori.md" (non pertinente ai campi email di questo UC); dati email sintetici generati dall'analista secondo le regole documentate, con autorizzazione esplicita a usare indirizzi sintetici validi, malformati e differenti | Utente, 2026-10-16 ~11:00 |
| Feature paths | docs/use-cases/features/checkout/checkout-email-sintattica.feature (nome descrittivo scelto dall'analista in assenza di un nome imposto) | Utente, 2026-10-16 ~11:00 (directory confermata); nome file riportato per presa visione |
| Run directory | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01 | Utente, 2026-10-16 ~11:00 |
| Gherkin profile inputs | Commento di tracciamento `#0123456789` | Utente, 2026-10-16 ~11:00 |

## Scenario inventory
| Scenario id | UC elements | Behaviour to cover |
| --- | --- | --- |
| SC-001 | Flusso principale 1-2; Postcondizione; AC-01 | Inserimento di un indirizzo email sintatticamente valido e coincidente nei due campi; avanzamento alla pagina di scelta del metodo di pagamento |
| SC-002 | EF-01; AC-03 | Indirizzo email sintatticamente non valido (generico) al passo 1: errore in tempo reale sotto il campo; al tentativo di proseguire l'errore permane e non si avanza |
| SC-003 | EF-02; AC-02 | Al passo 1, indirizzo email malformato in uno dei due pattern specifici (assenza di "@"; assenza di caratteri dopo "@") e tentativo di proseguire: warning specifico sul campo, nessun avanzamento |
| SC-004 | EF-03; AC-03 | Indirizzo email sintatticamente non valido (generico) al passo 2, dopo un passo 1 valido: errore in tempo reale sotto il campo; al tentativo di proseguire l'errore permane e non si avanza |
| SC-005 | EF-04; AC-02 | Al passo 2, indirizzo email di conferma malformato in uno dei due pattern specifici e tentativo di proseguire: warning specifico sul campo, nessun avanzamento |
| SC-006 | EF-05; EF-06; AC-03; AC-04 | Al passo 2, indirizzo valido ma diverso da quello del passo 1: errore di mancata coincidenza in tempo reale; il tentativo di proseguire non produce alcuna azione |

## Artifacts
| Artifact | Producer skill | Path | Revision | State |
| --- | --- | --- | --- | --- |
| context | uc-scenario-context | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/01-context.md | 2 | ready |
| test-data | uc-test-data | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/02-test-data.md | 2 | ready |
| feature-report | uc-to-feature | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/03-feature-report.md | 3 | ready |
| feature | uc-to-feature | docs/use-cases/features/checkout/checkout-email-sintattica.feature | 2 | ready |

## Questions
| Question id | Stage | Question | Decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | context | AC-03 (chiarita dall'utente come "click su Continua mostra un errore e impedisce l'avanzamento") si applica a EF-01/EF-03/EF-05; EF-02/EF-04 documentano invece un warning specifico al click per due soli pattern di sintassi non valida (assenza di "@"; assenza di parte dopo "@"). Per i pattern diversi da questi due, il click su Continua con sintassi non valida genera l'errore generico persistente previsto da AC-03 (nessun'altra reazione documentata), mentre per i due pattern nominati vale la regola più specifica di EF-02/EF-04. E' la ripartizione corretta, o l'utente intende diversamente? | Risposta esplicita dell'utente (seconda domanda, rivolta specificamente a EF-01/EF-03): "L'errore sotto il campo resta visibile; nei 2 casi documentati compare anche il warning". Non esiste alcuna ripartizione esclusiva: l'errore generico resta sempre visibile al click (per qualunque sintassi non valida, inclusi i due pattern nominati); nei due pattern nominati il warning specifico compare in aggiunta, non in sostituzione. Riportata e applicata in 01-context.md (F-004, F-005, F-006, S-004) e 03-feature-report.md, revisione 2 di entrambi i report e della feature. | answered |

## History
| Timestamp | Skill or human | Action | Output path and revision | Invalidated outputs |
| --- | --- | --- | --- | --- |
| 2026-10-16T11:10:00+02:00 | uc-to-feature (QA-analyst) | Inizializzazione registro, conferma input concordati (riferimento umano 2026-10-16 ~11:00), allocazione inventario SC-001..SC-006 | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/00-run.md rev 1 | — |
| 2026-10-16T11:18:00+02:00 | uc-scenario-context | Analisi funzionale dello UC e delle fonti fornite; allocazione Q-001 | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/01-context.md rev 1 | — |
| 2026-10-16T11:25:00+02:00 | uc-test-data | Generazione dati sintetici autorizzati conformi ai vincoli documentati; nessun dato irrisolto | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/02-test-data.md rev 1 | — |
| 2026-10-16T11:35:00+02:00 | uc-to-feature | Assemblaggio scenari, scrittura feature e report finale | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/03-feature-report.md rev 1; docs/use-cases/features/checkout/checkout-email-sintattica.feature rev 1 | — |
| 2026-10-16T11:22:35+02:00 | uc-to-feature (QA-analyst) | Risoluzione di Q-001 tramite risposta umana esplicita ottenuta via domanda interattiva dell'orchestratore ("L'errore sotto il campo resta visibile; nei 2 casi documentati compare anche il warning"); rimossa l'interpretazione precedente che ripartiva esclusivamente EF-01/EF-03 sugli altri pattern ed EF-02/EF-04 sui due pattern con "@". Corretti di conseguenza 01-context.md (nuova fonte S-004, evidenze F-004/F-005/F-006, oracoli O-001/O-003/O-004, mapping SC-003/SC-005/SC-006, stato Q-001), 03-feature-report.md (mapping, coverage, dati e oracoli, checks, engineer handoff, readiness) e la feature (step espliciti "durante la digitazione", persistenza dell'errore e coesistenza con il warning negli Schemi SC-003/SC-005, asserzione esplicita di persistenza in SC-006, aggiunta del tag `Feature` mancante, tag di scenario riportati uno per riga). 02-test-data.md non è stato modificato: nessun dato richiede variazione per questa correzione. | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/01-context.md rev 2; docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/03-feature-report.md rev 2; docs/use-cases/features/checkout/checkout-email-sintattica.feature rev 2 | — |
| 2026-10-16T11:45:00+02:00 | uc-test-data (QA-analyst) | Rilevata dipendenza stale: `02-test-data.md` rev 1 dichiarava `inputs` con `01-context.md` revisione 1, mentre il contesto reale era già passato a revisione 2 (risoluzione Q-001). Per la regola del workflow, il cambiamento di contesto invalida i dati anche a valori invariati. Letto realmente `01-context.md` rev 2 (F-003, F-004, F-005, F-006, O-001, O-003, O-004): i vincoli strutturali dei requisiti D-001..D-005 non sono cambiati, nessun valore è stato modificato. Aggiunta la fonte locale S-005 (rivalidazione) e una riga Decisions per Q-001; aggiornata la relazione evidenza delle combinazioni C-003/C-004/C-006/C-007 per esplicitare che l'errore generico resta sempre visibile al click e il warning specifico compare in aggiunta, non in sostituzione, nei due pattern "assenza di @"/"assenza di parte dopo @". Readiness aggiornata con la nota di rivalidazione. | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/02-test-data.md rev 2 | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/03-feature-report.md (dipendeva da test-data rev 1) |
| 2026-10-16T11:50:00+02:00 | uc-to-feature (QA-analyst) | Letti realmente `02-test-data.md` rev 2 e `01-context.md` rev 2; confronto riga per riga con mapping, coverage, dati e oracoli già scritti nel report finale e con la feature pubblicata: nessuna discordanza, nessuna modifica di contenuto necessaria alla feature (resta rev 2). Aggiunta una riga Checks che documenta la rilettura e la riconferma; aggiornata la Readiness con la nota di rivalidazione dopo la correzione di `02-test-data.md`. Riscritto il report finale con `inputs` allineati a contesto rev 2 e dati rev 2. | docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/03-feature-report.md rev 3 | — |
