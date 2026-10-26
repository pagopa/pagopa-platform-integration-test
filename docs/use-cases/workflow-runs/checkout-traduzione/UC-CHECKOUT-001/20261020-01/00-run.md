---
schema: uc-workflow/v1
artifact: run
producer_skill: uc-to-feature
task_id: checkout-traduzione
uc_id: UC-CHECKOUT-001
run_id: 20261020-01
uc_input: 'C:\Users\dquero\Downloads\UC-CHECKOUT-001 - Attivazione pagamento Checkout.txt'
uc_revision: v1
environment: uat
revision: 4
status: draft
updated_at: "2026-10-20T16:41:36.150+02:00"
inputs: []
---

# UC - Run

## Agreed inputs
| Item | Value | Human confirmation |
| --- | --- | --- |
| Functional sources | UC allegato; C:/Users/dquero/Downloads/Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md; docs/use-cases/test-data/checkout/checkout-test-data.md; chiarimenti umani in chat | Richiesta iniziale e risposta del 2026-10-20T16:06:16.298+02:00 |
| Data sources | C:/Users/dquero/Downloads/Note per gli sviluppatori.md; docs/use-cases/test-data/checkout/checkout-test-data.md | Allegati esplicitamente forniti nella stessa conversazione |
| Feature paths | docs/use-cases/features/checkout/FEAT_001_Checkout_Attivazione_Pagamento.feature; docs/use-cases/features/checkout/FEAT_002_Checkout_Errori_Avviso.feature | Cartella confermata nella richiesta iniziale; nomi descrittivi scelti secondo il profilo |
| Run directory | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/ | Punto 1 della risposta umana del 2026-10-20T16:06:16.298+02:00: ok; comprende UAT e revisione v1 |
| Gherkin profile inputs | .github/profiles/gherkin.profile.yaml; tracking 0123456789; suite checkout | Punto 2 della risposta umana del 2026-10-20T16:06:16.298+02:00 |
| Source exclusions | Nessuna esplorazione o lettura di src o docs/use-cases/features, incluse le nuove feature; nessun contenuto eseguibile come evidenza | Divieto esplicito nella richiesta iniziale |
| Functional boundary | Non testare azioni successive all'uscita da pagoPA; tempi degli errori interpretati come massimi | Punto 3 della risposta umana del 2026-10-20T16:06:16.298+02:00 |

## Scenario inventory
| Scenario id | UC elements | Behaviour to cover |
| --- | --- | --- |
| SC-001 | FP 1-6; AC-01; postcondizione | Percorso carta, dettagli carta, scelta PSP e avvio del pagamento; successo fuori perimetro |
| SC-002 | AF-01; AC-02; FP 1-2, 5-6; postcondizione | PayPal con scelta PSP e avvio del pagamento; successo fuori perimetro |
| SC-003 | AF-02; AC-03; FP 1-2, 6; postcondizione | Google Pay senza scelta iniziale PSP e avvio del pagamento; successo fuori perimetro |
| SC-004 | AF-03; AC-04; FP 1-2, 5-6; postcondizione | Apple Pay con scelta PSP e avvio del pagamento; successo fuori perimetro |
| SC-005 | AF-04; AC-05; FP 1-2, 5-6; postcondizione | BANCOMAT Pay con scelta PSP e avvio del pagamento; successo fuori perimetro |
| SC-006 | AF-05; AC-06; FP 1-2, 6; postcondizione | Conto iCONTO senza scelta iniziale PSP e avvio del pagamento; successo fuori perimetro |
| SC-007 | AF-06; AC-07; FP 1-2, 6; postcondizione | Conto Intesa Sanpaolo senza scelta iniziale PSP e avvio del pagamento; successo fuori perimetro |
| SC-008 | AF-07; AC-08; FP 1-2, 6; postcondizione | Fabrick Pay By Bank senza scelta iniziale PSP e avvio del pagamento; successo fuori perimetro |
| SC-009 | AF-08; AC-09; FP 1-2, 6; postcondizione | Klarna senza scelta iniziale PSP e avvio del pagamento; successo fuori perimetro |
| SC-010 | AF-09; AC-10; FP 1-2, 5-6; postcondizione | MyBank con scelta PSP e avvio del pagamento; successo fuori perimetro |
| SC-011 | EF-01; AC-11; AC-12; AC-13 | Avviso sconosciuto: titolo e corpo documentati, entro 5 secondi da Continua |
| SC-012 | EF-01; AC-11; AC-12; AC-13 | Avviso scaduto: titolo e corpo documentati, entro 60 secondi; variante sostenuta dal catalogo allegato, stesse verifiche di EF-01 |
| SC-013 | EF-01; AC-11; AC-12; AC-13 | Timeout stazione: titolo e corpo documentati, entro 60 secondi; variante sostenuta dal catalogo allegato, stesse verifiche di EF-01 |
| SC-014 | EF-01; AC-11; AC-12; AC-13 | Avviso duplicato: titolo documentato, assenza di corpo, entro 5 secondi; variante sostenuta dal catalogo allegato, verifica di assenza distinta |
| SC-015 | EF-01; AC-11; AC-12; AC-13 | Ente irraggiungibile: variante documentale esclusa dal test su richiesta umana, tempo e corpo esatto mancanti |

## Artifacts
| Artifact | Producer skill | Path | Revision | State |
| --- | --- | --- | --- | --- |
| context | uc-scenario-context | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/01-context.md | 1 | incomplete |
| test-data | uc-test-data | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/02-test-data.md | 1 | incomplete |
| feature-report | uc-to-feature | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/03-feature-report.md | 1 | incomplete |
| feature | uc-to-feature | docs/use-cases/features/checkout/FEAT_001_Checkout_Attivazione_Pagamento.feature | 1 | incomplete |
| feature | uc-to-feature | docs/use-cases/features/checkout/FEAT_002_Checkout_Errori_Avviso.feature | 1 | incomplete |

## Questions
| Question id | Stage | Question | Decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | initialization | Identita, revisione, ambiente e directory della nuova run? | Confermati punto 1 della risposta umana del 2026-10-20T16:06:16.298+02:00 | answered |
| Q-002 | translation | Numero di tracciamento obbligatorio? | 0123456789, punto 2 della stessa risposta | answered |
| Q-003 | context | Perimetro dopo l'uscita da pagoPA? | Le azioni successive non vanno testate; non equiparare il reindirizzamento al pagamento completato o al messaggio di successo, punto 3 della stessa risposta | answered |
| Q-004 | context | Semantica dei tempi degli errori? | Tempo massimo, punto 3 della stessa risposta; istante iniziale ancora da confermare in Q-005 | answered |
| Q-005 | context | Il massimo decorre dalla pressione di Continua dopo l'inserimento dell'avviso? | Si, punto 1 risposta umana del 2026-10-20T16:41:36.150+02:00 | answered |
| Q-006 | context | I testi candidati sono autorizzati come valori attesi per questa bozza? Come trattare irraggiungibile? | Confermata proposta dei quattro errori; quello con copertura mancante non va incluso nel test, punto 2 stessa risposta. Valori non verificati sulla versione applicativa | answered |
| Q-007 | test-data | Usare i valori documentati ma non verificati con warning, oppure TODO? | Si ai dati documentati, compresi sintetici, come non verificati con warning e senza generarne altri, punto 3 stessa risposta | answered |
| Q-008 | test-data | Quale PSP selezionare per Apple Pay, BANCOMAT Pay e MyBank? | Nessun candidato specifico nel catalogo fornito, unico record presente nella directory dati; D-005 resta TODO nei tre casi, non si estende l'ID PayPal ad altri metodi | open |

## History
| Timestamp | Skill or human | Action | Output path and revision | Invalidated outputs |
| --- | --- | --- | --- | --- |
| 2026-10-20T16:06:16.298+02:00 | human | Confermati nuova run, revisione v1, UAT, tracking, semantica massima dei tempi e confine prima delle azioni esterne; fornito catalogo checkout | Input della run | Nessuno |
| 2026-10-20T16:06:16.298+02:00 | uc-to-feature | Inizializzazione del registro e inventario da UC; letti allegati, policy, profilo e template; nessuna lettura dei percorsi vietati; nessun test eseguito; domande dedicate non disponibili nell'harness, chiarimenti richiesti in chat | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/00-run.md revision 1 | Nessuno |
| 2026-10-20T16:41:36.150+02:00 | human | Confermati origine dei massimi, quattro errori e dati candidati con warning; escluso ente irraggiungibile | Q-005, Q-006, Q-007 | Nessuno |
| 2026-10-20T16:41:36.150+02:00 | uc-scenario-context | Salvato contesto, definiti F/O/D, registrate varianti SC-012-SC-015. Nessun report o feature preesistente da riprendere; le risposte completano l'inizializzazione della stessa run | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/01-context.md revision 1; 00-run.md revision 2 | Nessuno |
| 2026-10-20T16:41:36.150+02:00 | uc-test-data | Consumato contesto revision 1; completata ricerca locale nei soli dati autorizzati; salvate 14 combinazioni, ammissione e warning; tre PSP irrisolti in Q-008. Nessun catalogo modificato, nessun nuovo valore generato | docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/02-test-data.md revision 1; 00-run.md revision 3 | Nessuno |
| 2026-10-20T16:41:36.150+02:00 | uc-to-feature | Validati gli input reali e i report revision 1; scritte due feature con 5 definizioni/14 casi e warning. Escluso SC-015. Salvato report finale incompleto con copertura e controlli statici; nessuna lettura delle feature, nessun test. Registro draft | docs/use-cases/features/checkout/FEAT_001_Checkout_Attivazione_Pagamento.feature revision 1; docs/use-cases/features/checkout/FEAT_002_Checkout_Errori_Avviso.feature revision 1; docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/03-feature-report.md revision 1; 00-run.md revision 4 | Nessuno |
