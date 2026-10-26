---
schema: uc-workflow/v1
artifact: run
producer_skill: uc-to-feature
task_id: unknown
uc_id: UC-CHECKOUT-003
run_id: 20261020-01
uc_input: 'C:\Users\dquero\Downloads\UC-CHECKOUT-003 - Back Navigation Control.txt'
uc_revision: "1"
environment: uat
revision: 5
status: draft
updated_at: "2026-10-20T13:26:52.455+02:00"
inputs: []
---

# UC - Run

## Agreed inputs
| Item | Value | Human confirmation |
| --- | --- | --- |
| Functional sources | UC allegato; `C:\Users\dquero\Downloads\Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md`; risposte umane; catalogo Markdown, solo ritorno scelta metodo verso email | Allegati iniziali; conferma punti 1, 3, 4 del 2026-10-20T13:20:40.119+02:00; conferma punti 2 e 3 del 2026-10-20T13:26:52.455+02:00 |
| Data sources | `C:\Users\dquero\Downloads\Note per gli sviluppatori.md`; docs/use-cases/test-data/checkout/checkout-test-data.md, solo avviso completo, CF, carta Mastercard ed email mail@pagopa.it | Risposta del 2026-10-20T13:26:52.455+02:00, punto 1: autorizzati come dati non verificati; incluso intestatario sintetico gia documentato |
| Feature paths | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Punto 1 confermato il 2026-10-20T13:20:40.119+02:00 |
| Run directory | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/ | Punto 1 confermato, salvo task da ignorare; unknown rappresenta l'assenza del task, non un ticket |
| Gherkin profile inputs | Profilo .github/profiles/gherkin.profile.yaml; italiano; progressivo 004; commento mock #1234567890 | Punti 1 e 2 confermati il 2026-10-20T13:20:40.119+02:00 |
| UC identity and revision | UC-CHECKOUT-003; revisione 1; ambiente uat; nessun task associato | Punto 1: tutto confermato tranne id task, da ignorare |
| Source boundaries | Non esplorare src o docs/use-cases/features; scrivere soltanto il nuovo output concordato nella destinazione feature | Richiesta iniziale |
| Workflow mode | Automatico, nuova run; nessun output preesistente riutilizzato | Richiesta di traduzione e conferma della nuova run |

## Scenario inventory
| Scenario id | UC elements | Behaviour to cover |
| --- | --- | --- |
| SC-001 | FP 1-2; postcondizione destinazione; AC-01 secondo Q-006 | Inserimento dati avviso verso Home con 1 pressione di Indietro; verifica dati non applicabile |
| SC-002 | FP 1-2; entrambe le postcondizioni; AC-01 | Riepilogo dati pagamento verso inserimento avviso; conservazione codice avviso e CF ente |
| SC-003 | FP 1-2; entrambe le postcondizioni; AC-01 | Inserimento email verso riepilogo dati pagamento; codice avviso e CF ente precedenti ancora visibili nel riepilogo |
| SC-004 | FP 1-2; postcondizione destinazione; AC-01 secondo Q-006 | Inserimento carta verso scelta metodo; verifica dati non applicabile |
| SC-005 | FP 1-2; entrambe le postcondizioni; AC-01 | Lista PSP del percorso carta verso inserimento carta; conservazione dei 4 campi, CVV incluso |
| SC-006 | FP 1-2; postcondizione destinazione; AC-01 secondo Q-006 | Lista PSP del percorso PayPal verso scelta metodo; verifica dati non applicabile |
| SC-007 | FP 1-2; postcondizione destinazione; AC-01 secondo Q-006 | Lista PSP del percorso Apple Pay verso scelta metodo; stesse azioni e verifiche di SC-006 |
| SC-008 | FP 1-2; postcondizione destinazione; AC-01 secondo Q-006 | Lista PSP del percorso BANCOMAT Pay verso scelta metodo; stesse azioni e verifiche di SC-006 |
| SC-009 | FP 1-2; postcondizione destinazione; AC-01 secondo Q-006 | Lista PSP del percorso MyBank verso scelta metodo; stesse azioni e verifiche di SC-006 |
| SC-010 | FP 1-2; entrambe le postcondizioni; AC-01 | Scelta metodo verso email con Indietro; conservazione di indirizzo email e Ripeti di nuovo, secondo Q-005 |

## Artifacts
| Artifact | Producer skill | Path | Revision | State |
| --- | --- | --- | --- | --- |
| context | uc-scenario-context | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/01-context.md | 2 | ready |
| test-data | uc-test-data | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/02-test-data.md | 1 | incomplete |
| feature-report | uc-to-feature | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/03-feature-report.md | 1 | incomplete |
| feature | uc-to-feature | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | 1 | incomplete |

## Questions
| Question id | Stage | Question | Decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | initialization | Identita, revisione, ambiente, destinazione e nuova run? | Conferma umana del 2026-10-20T13:20:40.119+02:00; task ignorato e rappresentato da unknown; nessuna associazione Jira | answered |
| Q-002 | translation | Numero di tracking richiesto dal profilo? | Stessa risposta, punto 2: usare #1234567890 come mock, non identificativo reale | answered |
| Q-003 | context | Controllo, cardinalita e campi conservati? | Stessa risposta, punto 3: Indietro dell'applicazione; 1 ritorno per scenario; tutti i campi avviso, email e carta, CVV incluso, quando presenti nella pagina di destinazione | answered |
| Q-004 | context | AF ed EF vuoti significano assenza? | Stessa risposta, punto 4: nessun AF/EF previsto; nessuna variante negativa inventata | answered |
| Q-005 | context | Come si torna dalla scelta metodo alla pagina email? | Risposta del 2026-10-20T13:26:52.455+02:00, punto 2: Indietro verso email, conservazione di entrambi i campi. Ammessa la relativa coppia del catalogo | answered |
| Q-006 | context | Come applicare la conservazione dati ai ritorni verso Home e scelta metodo, senza input documentati? | Stessa risposta, punto 3: verificare solo la destinazione; conservazione dati dove sono presenti i campi | answered |
| Q-007 | data | Approvare i candidati del catalogo Markdown per questa traduzione? | Stessa risposta, punto 1: avviso 302042025112600001, CF 77777777777, Mastercard 5255000260000014 / 12/30 / 123 / Test test ed email mail@pagopa.it autorizzati come non verificati con warning; nessuna verifica notifiche | answered |
| Q-008 | data | Stato e disponibilita correnti dei dati e percorsi richiesti? | Nessuna disponibilita corrente confermata: avviso valido e non pagato, accettazione carta, metodi e lista PSP da predisporre/verificare. Nessuna esecuzione autorizzata o svolta dall'analista; bozza | open |

## History
| Timestamp | Skill or human | Action | Output path and revision | Invalidated outputs |
| --- | --- | --- | --- | --- |
| 2026-10-20T13:20:40.119+02:00 | human | Conferma inizializzazione, commento mock, controllo applicativo, 1 ritorno, conservazione campi e assenza AF/EF | Decisioni Q-001..Q-004 | Nessuno |
| 2026-10-20T13:20:40.119+02:00 | uc-to-feature | Inizializzazione nuova run e inventario dai soli input ammessi; task non associato | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/00-run.md revision 1 | Nessuno |
| 2026-10-20T13:20:40.119+02:00 | uc-scenario-context | Persistenza evidenza funzionale, estensione inventario ai percorsi documentati e registrazione lacune; aggiornamento registro | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/01-context.md revision 1; 00-run.md revision 2 | Nessuno; output a valle non creati |
| 2026-10-20T13:26:52.455+02:00 | human | Risoluzione Q-005..Q-007; proseguimento della stessa traduzione senza riuso di feature preesistenti | Messaggio di conferma punti 1-3 | Nessuno |
| 2026-10-20T13:26:52.455+02:00 | uc-scenario-context | Contesto aggiornato con ritorno verso email e applicabilita del confronto dati; inventario corrente | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/01-context.md revision 2; 00-run.md revision 3 | Nessuno; output a valle non creati |
| 2026-10-20T13:26:52.455+02:00 | uc-test-data | Letti registro e contesto revision 2; valori ammessi con warning e combinazioni per tutti i casi; disponibilita non accertata Q-008 | docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/02-test-data.md revision 1; 00-run.md revision 4 | Nessuno; feature e report finale non creati |
| 2026-10-20T13:26:52.455+02:00 | uc-to-feature | Letti entrambi i report persistiti e registro; verificati identita, revisioni, fonti, decisioni e SC/D/C/O; scritti nuovo file feature e report finale con esito positivo del tool | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature revision 1; docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/03-feature-report.md revision 1 | Nessuno |
| 2026-10-20T13:26:52.455+02:00 | uc-to-feature | Registrati soltanto output realmente scritti; chiusura in draft per Q-008. Verificati staticamente 7 definizioni, 10 casi, 1 ritorno per caso, confronti dati e warning; nessun test o parser eseguito | 00-run.md revision 5; context revision 2 ready; test-data revision 1 incomplete; feature-report e feature revision 1 incomplete | Nessuno |
