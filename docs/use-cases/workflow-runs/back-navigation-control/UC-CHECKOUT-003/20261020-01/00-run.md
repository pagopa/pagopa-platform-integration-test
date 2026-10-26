---
schema: uc-workflow/v1
artifact: run
producer_skill: uc-to-feature
task_id: "back-navigation-control"
uc_id: "UC-CHECKOUT-003"
run_id: "20261020-01"
uc_input: "C:\\Users\\dquero\\Downloads\\UC-CHECKOUT-003 - Back Navigation Control.txt"
uc_revision: "1"
environment: uat
revision: 5
status: draft
updated_at: "2026-10-20T10:54:20+02:00"
inputs: []
---

# UC - Run

## Agreed inputs
| Item | Value | Human confirmation |
| --- | --- | --- |
| Functional sources | UC-CHECKOUT-003 - Back Navigation Control.txt (file fornito); Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md (file fornito) | Confermato dall'orchestratore nel prompt del task corrente |
| Data sources | Note per gli sviluppatori.md (file fornito; generazione sintetica di codice avviso ed email AUTORIZZATA dall'umano in questa run, vedi Q-001 rettificata; il CF EC 77777777777 e' un valore direttamente fornito dalla stessa fonte, non necessita di questa autorizzazione) | Confermato dall'orchestratore nel prompt del task corrente (nuova risposta umana via ask_user) |
| Feature paths | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | Confermato dall'orchestratore nel prompt del task corrente |
| Run directory | docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01 | Confermato dall'orchestratore nel prompt del task corrente (cartella gia' creata dal parent) |
| Gherkin profile inputs | Tracking comment `#0123456789` | Confermato dall'orchestratore nel prompt del task corrente |

## Scenario inventory
| Scenario id | UC elements | Behaviour to cover |
| --- | --- | --- |
| SC-001 | FP step 1-2, AC-01 | Back da `inserisci-dati-avviso` verso `home` |
| SC-002 | FP step 1-2, AC-01 | Back da `dati-pagamento` verso `inserisci-dati-avviso` |
| SC-003 | FP step 1-2, AC-01 | Back da `inserisci-email` verso `dati-pagamento` |
| SC-004 | FP step 1-2, AC-01 | Back da `inserisci-carta` verso `scegli-metodo` |
| SC-005 | FP step 1-2, AC-01 | Back da `lista-psp` (ramo carta) verso `inserisci-carta` |
| SC-006 | FP step 1-2, AC-01 | Back da `lista-psp` (ramo metodi alternativi; campione rappresentante PayPal, nominato esplicitamente) verso `scegli-metodo`. Apple Pay, BANCOMAT Pay e MyBank sono dichiarati equivalenti dalla fonte ma non campionati singolarmente in questa riga |

## Artifacts
| Artifact | Producer skill | Path | Revision | State |
| --- | --- | --- | --- | --- |
| context | uc-scenario-context | docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01/01-context.md | 2 | incomplete |
| test-data | uc-test-data | docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01/02-test-data.md | 2 | incomplete |
| feature-report | uc-to-feature | docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01/03-feature-report.md | 2 | incomplete |
| feature | uc-to-feature | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | 2 | incomplete |

## Questions
| Question id | Stage | Question | Decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | test-data | E' autorizzato l'uso dei valori sintetici documentati in "Note per gli sviluppatori.md" (pattern codice avviso 302YYXXXXXXXXXXXXX, CF EC 77777777777) per risolvere D-001/D-002 di questa run? | RETTIFICA: la voce precedente di questo registro riportava erroneamente "Rifiutato", come se un umano avesse negato esplicitamente l'autorizzazione; in realta' nessun rifiuto umano era mai stato espresso, c'era solo assenza di un'autorizzazione esplicita. Nuova decisione umana (via ask_user, riportata dall'orchestratore nel prompt del task corrente, 2026-10-20): autorizzata la generazione di un codice avviso sintetico (pattern 302YYXXXXXXXXXXXXX, YY 00-27, 13 cifre finali) e di un indirizzo email sintetico/di esempio secondo gli allegati; il CF EC 77777777777 resta un valore direttamente fornito dalla fonte, utilizzabile senza questa autorizzazione aggiuntiva. Ambito: questa run (UC-CHECKOUT-003, run 20261020-01); non approva altre fonti ne' rinnova la disponibilita' dell'ambiente live | answered |

## History
| Timestamp | Skill or human | Action | Output path and revision | Invalidated outputs |
| --- | --- | --- | --- | --- |
| 2026-10-20T10:54:20+02:00 | uc-to-feature (QA-analyst) | Inizializzazione registro; identita' e inventario SC-001..SC-006 confermati dall'orchestratore; timestamp osservato da Get-Date rilevato dal parent nel prompt del task | 00-run.md rev 1 | Nessuno |
| 2026-10-20T10:54:20+02:00 | uc-scenario-context (QA-analyst) | Analisi fonti S-001..S-003; evidenza funzionale, oracle e requisiti dati per SC-001..SC-006; copertura parziale esplicita per scegli-metodo, riepilogo-pagamento, ramo Google Pay/equivalenti e distinzione UI/browser back | 01-context.md rev 1 (incomplete) | Nessuno (prima scrittura) |
| 2026-10-20T10:54:20+02:00 | uc-test-data (QA-analyst) | Risoluzione dati per D-001..D-008; uso di S-003 rifiutato per decisione umana (Q-001); tutti i requisiti restano TODO con C-001..C-005 unverified e avvertenze di riga per SC-002..SC-006 | 02-test-data.md rev 1 (incomplete) | Nessuno (prima scrittura) |
| 2026-10-20T10:54:20+02:00 | uc-to-feature (QA-analyst) | Assemblaggio feature FEAT_003_Checkout_Back_Navigation.feature (1 Schema dello scenario, 6 righe Esempi per SC-001..SC-006); controlli statici (keyword `behave --lang-help it`, regex nome file, enum, TODO, Examples non costanti); report finale bozza per dati irrisolti e lacune esplicite (scegli-metodo, riepilogo-pagamento, ramo Google Pay/equivalenti, back UI vs browser) | 03-feature-report.md rev 1 (incomplete); feature rev 1 (incomplete) | Nessuno (prima scrittura) |
| 2026-10-20T10:54:20+02:00 | uc-to-feature (QA-analyst) | RETTIFICA Q-001: la precedente voce "Rifiutato" era un errore di registrazione, non un rifiuto umano reale (nessun umano aveva mai negato l'autorizzazione). Nuova decisione umana riportata dall'orchestratore via ask_user nel prompt del task corrente: autorizzata la generazione di D-001 (codice avviso sintetico) e D-003/D-004 (email sintetica/di esempio) secondo gli allegati; D-002 (CF EC 77777777777) riconosciuto come valore direttamente fornito, mai bisognoso di questa approvazione. Corretti anche `uc_revision` ("1", non "revisione1") e `environment` ("uat", non "UAT") secondo conferma umana. Invalidati context/test-data/feature-report/feature per rielaborazione | 00-run.md rev 5 | 01-context.md rev 1, 02-test-data.md rev 1, 03-feature-report.md rev 1, feature rev 1 (tutti da rielaborare) |
| 2026-10-20T10:54:20+02:00 | uc-scenario-context (QA-analyst) | Rielaborazione: corretto `uc_revision`/`environment` in frontmatter; rimosso SC-003 dallo scope di D-003/D-004 (contraddizione contesto/dati: accedere a `inserisci-email` non richiede l'email gia' inserita); esplicitato in Mapping il campione rappresentante PayPal per SC-006 (Apple Pay/BANCOMAT Pay/MyBank dichiarati equivalenti ma non campionati); nessuna evidenza funzionale nuova oltre a quanto gia' registrato | 01-context.md rev 2 (incomplete) | 02-test-data.md, 03-feature-report.md, feature (gia' marcati stale dalla rettifica precedente) |
| 2026-10-20T10:54:20+02:00 | uc-test-data (QA-analyst) | Rielaborazione: Q-001 ora `answered` (approvato); D-001 generato secondo il pattern autorizzato (YY=12, entro 00-27), D-002 usato come valore fornito, D-003/D-004 risolti con l'esempio fornito da 01-context.md#S-002 ("email@email.it"); disponibilita' live NON verificata per nessuno di questi (`documented-not-checked`), nessuna falsa disponibilita' dichiarata; D-003/D-004 rimossi dallo scope di SC-003; D-005..D-008 restano TODO (nessuna fonte ammessa, nessuna autorizzazione sintetica per i dati carta); corretto `uc_revision`/`environment` | 02-test-data.md rev 2 (incomplete) | 03-feature-report.md, feature (gia' marcati stale) |
| 2026-10-20T10:54:20+02:00 | uc-to-feature (QA-analyst) | Rielaborazione feature: sostituiti i valori concreti risolti per D-001..D-004 con avvertenza di riga su disponibilita' live non verificata; rimossa la precondizione non supportata "senza altri dati inseriti" dalla riga `inserisci-dati-avviso`; eliminato il nome di pagina pseudo-route "lista-psp (ramo carta)"/"lista-psp (ramo PayPal/...)" dalla colonna `pagina_iniziale`, ora `lista-psp` per entrambe le righe, disambiguate dal contesto; riga PayPal resa esplicita come campione rappresentante; D-005..D-008 restano TODO con avvertenza sulla sola riga `lista-psp`→`inserisci-carta`; corretto `uc_revision`/`environment` in tutti i report; controlli statici ripetuti (keyword italiane riutilizzate dall'esito gia' verificato, nessun nuovo comando terminale) | 03-feature-report.md rev 2 (incomplete); feature rev 2 (incomplete) | Nessuno |
