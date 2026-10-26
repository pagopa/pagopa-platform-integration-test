---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: "checkout-mail"
uc_id: "UC-CHECKOUT-002"
run_id: "20261016-01"
uc_input: "Allegato chat: UC-CHECKOUT-002 - Validazione sintattica dei campi mail.txt"
uc_revision: "1"
environment: uat
revision: 2
status: ready
updated_at: "2026-10-16T11:22:35+02:00"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | Allegato chat "UC-CHECKOUT-002 - Validazione sintattica dei campi mail.txt" | Intero documento | 2026-10-16 | Non indicato nello UC | provided | Utente, 2026-10-16 ~11:00 (allegato alla richiesta) |
| S-002 | Allegato chat "Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md" | Sezione "Pagina di inserimento Email" | 2026-10-16 | UAT, https://uat.checkout.pagopa.it/inserisci-email | provided | Utente, 2026-10-16 ~11:00 (allegato alla richiesta) |
| S-003 | Chiarimento umano in chat (orchestratore) | Precisazioni su EF-01/EF-03/EF-05 (messaggio durante la digitazione) e su AC-03 (click su Continua mostra un errore e impedisce l'avanzamento) | 2026-10-16 ~11:00 | Non applicabile | provided | Utente, 2026-10-16 ~11:00 |
| S-004 | Chiarimento umano in chat (risposta a domanda interattiva Q-001, orchestratore) | Domanda: "Per EF-01 ed EF-03, dopo la comparsa dell'errore durante la digitazione, cosa deve mostrare il click su «Continua»? [...] serve chiarire se l'errore e il warning possono coesistere." Risposta: "L'errore sotto il campo resta visibile; nei 2 casi documentati compare anche il warning" | 2026-10-16T11:22:35+02:00 | Non applicabile | provided | Utente, 2026-10-16T11:22:35+02:00 |

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | SC-001..SC-006 | Precondizioni | Dove si trova l'utente e quale lingua è impostata | L'utente si trova nella pagina di inserimento email; la lingua impostata è l'italiano | S-001, sezione "Precondizioni" | supported |
| F-002 | SC-001 | Flusso principale, passi 1-2 | Quali azioni compie l'utente nel flusso principale | Passo 1: l'utente inserisce un indirizzo email sintatticamente valido nel campo email; passo 2: l'utente ripete lo stesso indirizzo nel campo di conferma | S-001, sezione "Flusso principale" | supported |
| F-003 | SC-001..SC-006 | Struttura e validazione del campo email | Quali regole definiscono un indirizzo sintatticamente valido o non valido | Un indirizzo valido è "nome+@+dominio", con dominio = nome del sito (lettere, numeri, trattino) + punto + sigla finale di almeno 2 caratteri alfabetici; qualunque violazione evidenzia il campo in rosso e mostra sotto di esso "Inserisci un indirizzo email valido" | S-002, paragrafo "Pagina di inserimento Email" | supported |
| F-004 | SC-002, SC-003, SC-004, SC-005 | EF-01 (passo 1), EF-03 (passo 2), e i due pattern di EF-02/EF-04 (anch'essi sintassi non valida per F-003) | In quale momento compare il messaggio di errore sotto il campo | Il messaggio di errore compare durante la digitazione (in tempo reale), non solo alla perdita del focus o al click su Continua, per qualunque sintassi non valida, inclusi i due pattern nominati in EF-02/EF-04 | S-003 (chiarimento umano) in combinazione con S-001, EF-01/EF-03; S-004 (conferma esplicita che la regola si estende ai due pattern nominati) | supported |
| F-005 | SC-002, SC-003, SC-004, SC-005 | AC-03 applicato a EF-01/EF-02/EF-03/EF-04 | Cosa succede al click su Continua, dopo che l'errore è già comparso durante la digitazione | Il messaggio di errore generico sotto il campo resta visibile dopo il click, per qualunque sintassi non valida, inclusi i due pattern nominati in EF-02/EF-04; nei 2 casi documentati (assenza di "@"; assenza di parte dopo "@") compare anche il warning specifico, in coesistenza con l'errore e non in sua sostituzione | S-004 (chiarimento umano esplicito, risolve Q-001) | supported |
| F-006 | SC-003, SC-005 | EF-02 (passo 1), EF-04 (passo 2) | Cosa succede se l'utente tenta di proseguire con sintassi non valida in uno dei due pattern specifici | Al tentativo di proseguire, il sistema mostra un warning sul campo specifico, in aggiunta all'errore generico (vedi F-005): assenza del simbolo "@" → "Aggiungi un simbolo \"@\" nell'indirizzo email. Nel valore manca un simbolo \"@\""; assenza di caratteri dopo "@" → "Inserisci una parte dopo \"@\". Il valore è incompleto." | S-002, paragrafo "Pagina di inserimento Email"; S-004 (coesistenza con l'errore) | supported |
| F-007 | SC-006 | EF-05 | Cosa succede se l'utente inserisce al passo 2 un indirizzo valido ma diverso da quello del passo 1 | Il campo "Ripeti di nuovo" viene evidenziato in rosso e sotto di esso compare "Gli indirizzi email non coincidono"; per coerenza con F-004 anche qui il messaggio è mostrato in tempo reale (chiarimento EF-05 incluso) | S-002, paragrafo "Pagina di inserimento Email"; S-001, EF-05; S-003 (chiarimento su EF-01/03/05) | supported |
| F-008 | SC-006 | EF-06 / AC-04 | Cosa succede se, con indirizzi validi ma diversi, l'utente clicca su Continua | La pressione del tasto Continua non produce alcuna azione | S-001, EF-06; S-002 ("la pressione del tasto continua non produrrà alcuna azione") | supported |
| F-009 | SC-001 | Postcondizione / AC-01 | Quale pagina viene raggiunta in caso di successo | La pagina di scelta del metodo di pagamento (corrispondente, per conferma incrociata, a /scegli-metodo nell'ambiente UAT) | S-001, Postcondizioni/AC-01; S-002, paragrafo "Pagina di inserimento Email" | supported |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |
| SC-001 | Flusso principale 1; Flusso principale 2; Postcondizione/AC-01 | Inserire indirizzo valido nel campo email; ripetere lo stesso indirizzo nel campo di conferma; cliccare Continua; verificare avanzamento | F-001, F-002, F-003, F-009 | Due azioni distinte (campo email, campo conferma) perché la UC le numera come passi separati con possibili anomalie indipendenti (EF-01/02 vs EF-03/04/05/06) |
| SC-002 | Flusso principale 1 con anomalia (EF-01); AC-03 | Digitare sintassi non valida generica nel campo email; verificare errore in tempo reale; cliccare Continua; verificare persistenza errore e mancato avanzamento | F-003, F-004, F-005 | L'anomalia sostituisce il passo 1; la verifica del click è richiesta esplicitamente da AC-03 (chiarimento umano) |
| SC-003 | Flusso principale 1 con anomalia (EF-02); AC-02; AC-03 | Digitare uno dei due pattern di sintassi specifici nel campo email; verificare errore generico in tempo reale (F-004); cliccare Continua; verificare che l'errore generico resti visibile (F-005) e che compaia anche il warning specifico (F-006); verificare mancato avanzamento | F-003, F-004, F-005, F-006 | Due pattern distinti condividono lo stesso comportamento e le stesse verifiche: un solo Schema dello scenario con due righe di Esempi; l'errore generico e il warning coesistono (Q-001 risolta da S-004) |
| SC-004 | Flusso principale 1 (valido, di contesto); Flusso principale 2 con anomalia (EF-03); AC-03 | Inserire indirizzo valido nel campo email (passo 1 completato normalmente); digitare sintassi non valida generica nel campo di conferma; verificare errore in tempo reale; cliccare Continua; verificare persistenza errore e mancato avanzamento | F-002, F-003, F-004, F-005 | EF-03 presuppone un passo 1 già completato con dati validi: il passo 1 valido resta un'azione del flusso principale (When), non una precondizione |
| SC-005 | Flusso principale 1 (valido, di contesto); Flusso principale 2 con anomalia (EF-04); AC-02; AC-03 | Inserire indirizzo valido nel campo email; digitare uno dei due pattern specifici nel campo di conferma; verificare errore generico in tempo reale (F-004); cliccare Continua; verificare che l'errore generico resti visibile (F-005) e che compaia anche il warning specifico (F-006); verificare mancato avanzamento | F-002, F-003, F-004, F-005, F-006 | Stesso comportamento e stesse verifiche per i due pattern: un solo Schema dello scenario con due righe di Esempi; l'errore generico e il warning coesistono (Q-001 risolta da S-004) |
| SC-006 | Flusso principale 1 (valido, di contesto); Flusso principale 2 con anomalia (EF-05/EF-06); AC-03; AC-04 | Inserire indirizzo valido nel campo email; digitare un indirizzo valido ma diverso nel campo di conferma; verificare errore di mancata coincidenza in tempo reale; cliccare Continua; verificare che l'errore di mancata coincidenza resti visibile (AC-03) e che non si verifichi alcuna azione osservabile (AC-04); verificare mancato avanzamento | F-002, F-007, F-008 | EF-05 ed EF-06 descrivono la stessa anomalia da due osservazioni compatibili (errore in tempo reale, poi persistente al click; nessuna azione al click): un solo scenario con verifiche Then/And distinte per AC-03 (persistenza del messaggio) e AC-04 (assenza di azione) |

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |
| O-001 | SC-002, SC-003, SC-004, SC-005 | AC-03 (EF-01, EF-02, EF-03, EF-04) | Messaggio di errore sotto il campo: "Inserisci un indirizzo email valido", mostrato durante la digitazione e mantenuto visibile dopo il click su Continua, anche quando compare anche il warning specifico (O-003/O-004) | not-applicable | F-003, F-004, F-005 | supported |
| O-002 | SC-006 | AC-03 (EF-05) | Messaggio di errore sotto il campo "Ripeti di nuovo": "Gli indirizzi email non coincidono", mostrato durante la digitazione e mantenuto visibile dopo il click su Continua | not-applicable | F-007 | supported |
| O-003 | SC-003, SC-005 | AC-02 (EF-02, EF-04) | Warning sul campo per assenza di "@": "Aggiungi un simbolo \"@\" nell'indirizzo email. Nel valore manca un simbolo \"@\"", mostrato al click in aggiunta all'errore generico di O-001 (non in sua sostituzione) | not-applicable | F-005, F-006 | supported |
| O-004 | SC-003, SC-005 | AC-02 (EF-02, EF-04) | Warning sul campo per assenza di caratteri dopo "@": "Inserisci una parte dopo \"@\". Il valore è incompleto.", mostrato al click in aggiunta all'errore generico di O-001 (non in sua sostituzione) | not-applicable | F-005, F-006 | supported |
| O-005 | SC-006 | AC-04 (EF-06) | Nessuna azione osservabile al click su Continua, oltre alla persistenza del messaggio di errore già coperta da O-002 | not-applicable | F-008 | supported |
| O-006 | SC-001 | AC-01 / Postcondizione | Avanzamento alla pagina di scelta del metodo di pagamento | not-applicable | F-009 | supported |

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |
| D-001 | SC-001, SC-004, SC-005, SC-006 | Indirizzo email sintatticamente valido (valore di riferimento inserito al passo 1) | Deve rispettare la struttura locale+@+dominio+punto+sigla finale ≥2 lettere definita in F-003 | Nessuno stato pregresso richiesto | F-003 |
| D-002 | SC-002, SC-004 | Indirizzo email sintatticamente non valido, generico (non rientrante nei due pattern di D-003/D-004) | Deve violare la struttura di F-003 senza corrispondere esattamente a "assenza di @" o "assenza di parte dopo @" | Nessuno | F-003, F-005 |
| D-003 | SC-003, SC-005 | Indirizzo email privo del simbolo "@" | Stringa senza alcun carattere "@" | Nessuno | F-006 |
| D-004 | SC-003, SC-005 | Indirizzo email con "@" ma senza alcun carattere dopo di esso | Stringa terminante con "@" e parte di dominio vuota | Nessuno | F-006 |
| D-005 | SC-006 | Indirizzo email sintatticamente valido ma diverso dal valore D-001 inserito al passo 1 | Deve rispettare la struttura di F-003 ed essere diverso, carattere per carattere, dal valore scelto per D-001 nello stesso caso | Richiede che D-001 sia già stato inserito nello stesso scenario | F-003, F-007 |

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | SC-002, SC-003, SC-004, SC-005 | AC-03 (chiarita per il click su Continua) e EF-02/EF-04 (warning al click solo per due pattern nominati) si sovrappongono sul dominio degli indirizzi non validi: non era esplicitamente scritto se, per i pattern diversi da "assenza di @" e "assenza di parte dopo @", il click produca l'errore generico persistente (AC-03) oppure nessuna reazione aggiuntiva, né se errore e warning potessero coesistere nei due pattern nominati | Risposta esplicita dell'utente (S-004): "L'errore sotto il campo resta visibile; nei 2 casi documentati compare anche il warning". Non esiste quindi una ripartizione esclusiva tra EF-01/EF-03 (su altri pattern) ed EF-02/EF-04 (sui due pattern con "@"): l'errore generico persiste sempre al click, e nei due pattern nominati il warning si aggiunge, senza sostituirlo. Scopo: tutta la run 20261016-01, SC-002..SC-005 | answered |

## Readiness
Evidenza funzionale completa per tutti gli elementi dello UC (precondizioni, flusso
principale, EF-01..EF-06, postcondizione, AC-01..AC-04), ricavata dallo UC stesso,
dalla sezione "Pagina di inserimento Email" del documento Checkout fornito e da due
chiarimenti umani: uno sulla tempistica dei messaggi e sul significato di AC-03
(S-003), l'altro sulla coesistenza tra l'errore generico persistente e il warning
specifico nei due pattern nominati di EF-02/EF-04 (S-004, risolve Q-001).
Stato `ready`: nessuna questione aperta residua; nessun dato mancante o conflitto
bloccante. L'osservazione della postcondizione (avanzamento) avviene direttamente
tramite la navigazione alla pagina di scelta del metodo di pagamento, senza
richiedere uno stato interno non esposto dallo UC. Nessuna esecuzione di test o
verifica di ambiente è stata svolta; i controlli qui riportati sono analisi
statica manuale delle fonti ammesse.
