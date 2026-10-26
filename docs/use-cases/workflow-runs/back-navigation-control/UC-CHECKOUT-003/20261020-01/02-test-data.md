---
schema: uc-workflow/v1
artifact: test-data
producer_skill: uc-test-data
task_id: "back-navigation-control"
uc_id: "UC-CHECKOUT-003"
run_id: "20261020-01"
uc_input: "C:\\Users\\dquero\\Downloads\\UC-CHECKOUT-003 - Back Navigation Control.txt"
uc_revision: "1"
environment: uat
revision: 2
status: incomplete
updated_at: "2026-10-20T10:54:20+02:00"
inputs:
  - path: "docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01/01-context.md"
    revision: 2
---

# UC - Test data

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-003 | C:\Users\dquero\Downloads\Note per gli sviluppatori.md | "Codici Avviso", "Codice Fiscale Ente Creditore (EC)" | 2026-10-20T10:54:20+02:00 | unknown | provided | RETTIFICA rispetto alla registrazione precedente (che riportava erroneamente un rifiuto umano, mai realmente espresso): generazione sintetica di D-001 (pattern codice avviso) e D-003/D-004 (email) AUTORIZZATA dall'umano (via ask_user, riportata dall'orchestratore nel prompt del task corrente, 00-run.md Q-001); D-002 (CF EC 77777777777) e' un valore direttamente fornito da questa fonte, non necessita di questa autorizzazione |

## Data resolution
| Data id | Scenario id | Parameter and constraints | Value or TODO token | Source id and passage | Admission | Fitness | Availability evidence | Unresolved reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | SC-002, SC-003, SC-004, SC-005, SC-006 | Codice avviso di pagamento, 18 cifre numeriche, deve corrispondere a un avviso valido recuperabile dal sistema | `302124502198375901` | S-003 fornisce il pattern di generazione (302YYXXXXXXXXXXXXX, YY tra 00 e 27 per un avviso di tipo pagamento valido, 13 cifre finali libere); valore generato secondo la regola, con YY=`12` (entro 00-27) e 13 cifre finali `4502198375901`, a seguito dell'autorizzazione umana (00-run.md Q-001, rettificata) | approved | fit | documented-not-checked | — |
| D-002 | SC-002, SC-003, SC-004, SC-005, SC-006 | CF Ente Creditore, 11 cifre numeriche, coerente con D-001 | `77777777777` | S-003 fornisce questo valore direttamente come CF EC valido per attivita' di test; non e' un valore generato, e' una fonte fornita e non richiedeva l'autorizzazione di Q-001 | provided | fit | documented-not-checked | — |
| D-003 | SC-004, SC-005, SC-006 | Indirizzo email inserito in `inserisci-email` | `email@email.it` | 01-context.md#S-002 fornisce questo valore come esempio nella sezione "Pagina di inserimento Email" ("Es. email@email.it"); uso come valore di input autorizzato dall'umano (00-run.md Q-001, rettificata). Non e' un requisito di SC-003 (01-context.md#D-003) | approved | fit | documented-not-checked | — |
| D-004 | SC-004, SC-005, SC-006 | Conferma email, deve coincidere con D-003 | `email@email.it` | Stesso riferimento di D-003; deve coincidere esattamente con D-003. Non e' un requisito di SC-003 (01-context.md#D-004) | approved | fit | documented-not-checked | — |
| D-005 | SC-005 | Numero carta valido e coerente | `__TODO_D005__` | Nessuna fonte ammessa fornisce un valore concreto | unknown | unverified | unknown-to-prepare | Nessun valore fornito ne' approvato |
| D-006 | SC-005 | Scadenza carta valida, coerente con D-005 | `__TODO_D006__` | Nessuna fonte ammessa fornisce un valore concreto | unknown | unverified | unknown-to-prepare | Nessun valore fornito ne' approvato |
| D-007 | SC-005 | CVV carta valido | `__TODO_D007__` | Nessuna fonte ammessa fornisce un valore concreto | unknown | unverified | unknown-to-prepare | Nessun valore fornito ne' approvato |
| D-008 | SC-005 | Intestatario carta valido | `__TODO_D008__` | Nessuna fonte ammessa fornisce un valore concreto | unknown | unverified | unknown-to-prepare | Nessun valore fornito ne' approvato |

## Combinations
| Combination id | Scenario id | Data ids and selected values | Relationship evidence | Fitness | Unresolved reason |
| --- | --- | --- | --- | --- | --- |
| C-001 | SC-002 | D-001=`302124502198375901`, D-002=`77777777777` | 01-context.md#D-001, #D-002 (avviso+EC coerenti, richiesti per raggiungere `dati-pagamento`) | fit | — |
| C-002 | SC-003 | D-001=`302124502198375901`, D-002=`77777777777` | 01-context.md#D-001, #D-002 (richiesti per raggiungere `dati-pagamento` prima di `inserisci-email`) | fit | — |
| C-003 | SC-004 | D-001=`302124502198375901`, D-002=`77777777777`, D-003=`email@email.it`, D-004=`email@email.it` | 01-context.md#D-001..#D-004 (richiesti per raggiungere `scegli-metodo` prima di `inserisci-carta`); D-004 coincide con D-003 | fit | — |
| C-004 | SC-005 | D-001=`302124502198375901`, D-002=`77777777777`, D-003=`email@email.it`, D-004=`email@email.it`, D-005=`__TODO_D005__`, D-006=`__TODO_D006__`, D-007=`__TODO_D007__`, D-008=`__TODO_D008__` | 01-context.md#D-001..#D-008 (richiesti per raggiungere `lista-psp` dal ramo carta dopo `inserisci-carta`) | unverified | D-005, D-006, D-007, D-008 non risolti (nessun valore ammesso fornito, nessuna generazione sintetica autorizzata per i dati carta); D-001..D-004 risolti ma disponibilita' live non verificata |
| C-005 | SC-006 | D-001=`302124502198375901`, D-002=`77777777777`, D-003=`email@email.it`, D-004=`email@email.it` | 01-context.md#D-001..#D-004 (richiesti per raggiungere `scegli-metodo` prima della selezione del metodo alternativo; riga campione rappresentante PayPal) | fit | — |

SC-001 non richiede alcun `D-NNN` (accesso diretto da `home` a
`inserisci-dati-avviso`, senza dati gia' inseriti): nessuna combinazione e'
definita per questo caso, coerentemente con 01-context.md.

## Decisions
| Question id | Candidate or data ids | Human decision and date | Scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | D-001, D-003, D-004 (D-002 riconosciuto come valore direttamente fornito, non necessitava approvazione) | RETTIFICA: la precedente voce "Rifiutato" era un errore di registrazione, nessun umano aveva effettivamente rifiutato, era solo assenza di autorizzazione esplicita. Nuova decisione (via ask_user, riportata dall'orchestratore nel prompt del task corrente, 2026-10-20): autorizzata la generazione/uso di D-001 (codice avviso sintetico, pattern 302YYXXXXXXXXXXXXX) e D-003/D-004 (email di esempio/sintetica) secondo gli allegati | Questa run (UC-CHECKOUT-003, run 20261020-01); non approva altre fonti ne' rinnova la disponibilita' dell'ambiente live | answered |

## Scenario warnings
| Scenario id | Affected combinations or all | Data ids | Required comment |
| --- | --- | --- | --- |
| SC-002 | C-001 | D-001, D-002 | D-001, D-002 risolti con valore concreto (D-001 sintetico autorizzato, D-002 fornito); disponibilita'/recuperabilita' in ambiente live NON verificata (`documented-not-checked`) |
| SC-003 | C-002 | D-001, D-002 | D-001, D-002 risolti con valore concreto (D-001 sintetico autorizzato, D-002 fornito); disponibilita'/recuperabilita' in ambiente live NON verificata (`documented-not-checked`) |
| SC-004 | C-003 | D-001, D-002, D-003, D-004 | D-001..D-004 risolti con valore concreto; disponibilita' live NON verificata per D-001/D-002 (`documented-not-checked`); D-003/D-004 richiedono solo validita' sintattica, nessuno stato di entita' aggiuntivo |
| SC-005 | C-004 | D-001, D-002, D-003, D-004, D-005, D-006, D-007, D-008 | D-001..D-004 risolti con valore concreto ma disponibilita' live NON verificata; D-005, D-006, D-007, D-008 non risolti (TODO): scenario non pronto all'esecuzione per questa riga |
| SC-006 | C-005 | D-001, D-002, D-003, D-004 | D-001..D-004 risolti con valore concreto; disponibilita' live NON verificata (`documented-not-checked`); riga campione rappresentante PayPal, Apple Pay/BANCOMAT Pay/MyBank dichiarati equivalenti ma non campionati singolarmente |

## Optional catalogue
not-requested

## Readiness

Stato: `incomplete`. D-001..D-004 sono stati risolti con valore concreto: D-001
generato secondo il pattern autorizzato 302YYXXXXXXXXXXXXX (YY=`12`, entro
l'intervallo valido 00-27, 13 cifre finali `4502198375901`), a seguito
dell'autorizzazione umana rettificata (00-run.md Q-001); D-002 (`77777777777`)
e' un valore direttamente fornito da S-003, non generato, e non necessitava di
questa autorizzazione; D-003/D-004 (`email@email.it`) usano l'esempio fornito
da 01-context.md#S-002, sintatticamente validi e coincidenti. Nessuno di questi
quattro valori e' stato verificato come effettivamente disponibile/recuperabile
in ambiente `uat`: disponibilita' `documented-not-checked` per tutti, con
avvertenza di riga su ogni scenario interessato, senza alcuna falsa
disponibilita' dichiarata. D-005..D-008 (dati carta) restano
`__TODO_Dxxx__`: nessuna fonte ammessa fornisce un valore concreto e nessuna
generazione sintetica per questi campi e' stata autorizzata. SC-001 non
richiede dati e resta privo di avvertenze. C-001, C-002, C-003 e C-005 sono
`fit` (con avvertenza di disponibilita' live); C-004 resta `unverified` per i
dati carta mancanti. Nessun controllo live e' stato eseguito, nessun comando
terminale e' stato lanciato per questa risoluzione.

Rettifica di questa revisione (rev 2): Q-001 e' passata da `declined` (voce
errata, nessun rifiuto umano reale) ad `answered` (approvazione esplicita);
D-003/D-004 non sono piu' associati a SC-003, coerentemente con la correzione
di 01-context.md rev 2.
