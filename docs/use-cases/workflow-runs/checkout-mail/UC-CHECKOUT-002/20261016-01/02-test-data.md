---
schema: uc-workflow/v1
artifact: test-data
producer_skill: uc-test-data
task_id: "checkout-mail"
uc_id: "UC-CHECKOUT-002"
run_id: "20261016-01"
uc_input: "Allegato chat: UC-CHECKOUT-002 - Validazione sintattica dei campi mail.txt"
uc_revision: "1"
environment: uat
revision: 2
status: ready
updated_at: "2026-10-16T11:45:00+02:00"
inputs:
  - path: "docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/01-context.md"
    revision: 2
---

# UC - Test data

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-002 | Allegato chat "Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md" | Sezione "Pagina di inserimento Email" (vincoli di struttura dell'indirizzo) | 2026-10-16 | UAT | provided | Utente, 2026-10-16 ~11:00 |
| S-004 | Autorizzazione esplicita dell'utente a generare indirizzi email sintetici validi, malformati e differenti, coerenti con le regole documentate | Richiesta orchestratore/utente | 2026-10-16 ~11:00 | Non applicabile | provided | Utente, 2026-10-16 ~11:00 |
| S-005 | Rivalidazione contro `01-context.md` revisione 2 (F-004, F-005, F-006, Q-001): l'errore generico resta sempre visibile dopo il click, per qualunque sintassi non valida; nei due pattern nominati (assenza di "@"; assenza di parte dopo "@") compare anche il warning specifico, in aggiunta e non in sostituzione | 01-context.md#Q-001, 01-context.md#F-004, 01-context.md#F-005, 01-context.md#F-006 | 2026-10-16T11:45:00+02:00 | Non applicabile | provided | Utente, 2026-10-16T11:22:35+02:00 (risposta a Q-001, riportata in 01-context.md rev 2) |

Nota: nel repository esiste un catalogo candidato (`docs/use-cases/test-data/checkout/checkout-test-data.md`)
con valori di email sia validi sia malformati. Non è stato usato: essendo un
reperto scoperto autonomamente avrebbe richiesto approvazione esplicita, mentre
l'utente ha già autorizzato la generazione sintetica diretta (S-004), che evita
la richiesta di approvazione aggiuntiva. Non ammesso né respinto: resta un
candidato non utilizzato in questa run.

## Data resolution
| Data id | Scenario id | Parameter and constraints | Value or TODO token | Source id and passage | Admission | Fitness | Availability evidence | Unresolved reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | SC-001, SC-004, SC-005, SC-006 | Indirizzo email sintatticamente valido (vedi F-003 in 01-context.md) | `mario.rossi@esempio-test.it` (sintetico) | S-002 (regola di struttura); S-004 (autorizzazione sintetica) | provided | fit | documented-not-checked | — |
| D-002 | SC-002, SC-004 | Indirizzo email sintatticamente non valido, generico (non "assenza di @" né "assenza di parte dopo @") | `mario.rossi@esempiotest` (sintetico; dominio privo di punto e sigla finale) | S-002; S-004 | provided | fit | documented-not-checked | — |
| D-003 | SC-003, SC-005 | Indirizzo email privo del simbolo "@" | `mariorossiesempiotest.it` (sintetico) | S-002; S-004 | provided | fit | documented-not-checked | — |
| D-004 | SC-003, SC-005 | Indirizzo email con "@" ma senza caratteri dopo di esso | `mario.rossi@` (sintetico) | S-002; S-004 | provided | fit | documented-not-checked | — |
| D-005 | SC-006 | Indirizzo email sintatticamente valido, diverso da D-001 | `luigi.verdi@esempio-test.it` (sintetico; diverso carattere per carattere da D-001) | S-002; S-004 | provided | fit | documented-not-checked | — |

## Combinations
| Combination id | Scenario id | Data ids and selected values | Relationship evidence | Fitness | Unresolved reason |
| --- | --- | --- | --- | --- | --- |
| C-001 | SC-001 | D-001 = `mario.rossi@esempio-test.it` nel campo email e nel campo di conferma (stesso valore) | I due campi devono coincidere per AC-01 | fit | — |
| C-002 | SC-002 | D-002 = `mario.rossi@esempiotest` nel campo email | Valore non valido generico per EF-01 | fit | — |
| C-003 | SC-003 (riga 1) | D-003 = `mariorossiesempiotest.it` nel campo email | Pattern "assenza di @" per EF-02; rivalidato contro 01-context.md rev 2 (F-004/F-005/O-001, F-006/O-003): l'errore generico resta visibile al click e il warning specifico per "assenza di @" compare in aggiunta, non in sostituzione (Q-001) | fit | — |
| C-004 | SC-003 (riga 2) | D-004 = `mario.rossi@` nel campo email | Pattern "assenza di parte dopo @" per EF-02; rivalidato contro 01-context.md rev 2 (F-004/F-005/O-001, F-006/O-004): l'errore generico resta visibile al click e il warning specifico compare in aggiunta, non in sostituzione (Q-001) | fit | — |
| C-005 | SC-004 | D-001 nel campo email (passo 1 valido) + D-002 = `mario.rossi@esempiotest` nel campo di conferma | Passo 1 valido richiesto prima dell'anomalia EF-03 al passo 2 | fit | — |
| C-006 | SC-005 (riga 1) | D-001 nel campo email + D-003 nel campo di conferma | Passo 1 valido richiesto; pattern "assenza di @" per EF-04; rivalidato contro 01-context.md rev 2 (F-004/F-005/O-001, F-006/O-003): errore generico persistente e warning specifico in aggiunta (Q-001) | fit | — |
| C-007 | SC-005 (riga 2) | D-001 nel campo email + D-004 nel campo di conferma | Passo 1 valido richiesto; pattern "assenza di parte dopo @" per EF-04; rivalidato contro 01-context.md rev 2 (F-004/F-005/O-001, F-006/O-004): errore generico persistente e warning specifico in aggiunta (Q-001) | fit | — |
| C-008 | SC-006 | D-001 nel campo email + D-005 = `luigi.verdi@esempio-test.it` nel campo di conferma | D-005 deve differire da D-001 per EF-05/EF-06 | fit | — |

## Decisions
| Question id | Candidate or data ids | Human decision and date | Scope | State |
| --- | --- | --- | --- | --- |
| — | D-001..D-005 (generazione sintetica) | L'utente ha autorizzato esplicitamente indirizzi email sintetici validi, malformati e differenti coerenti con le regole documentate | Intera run 20261016-01, tutti gli scenari SC-001..SC-006 | answered |
| — | Catalogo `docs/use-cases/test-data/checkout/checkout-test-data.md` | Non utilizzato: nessuna richiesta di approvazione necessaria poiché la generazione sintetica autorizzata copre il fabbisogno | Non applicabile (candidato non consumato) | declined |
| Q-001 | C-003, C-004, C-006, C-007 | Risposta esplicita dell'utente, riportata in 01-context.md rev 2 (F-004, F-005, F-006): "L'errore sotto il campo resta visibile; nei 2 casi documentati compare anche il warning". Nessuna ripartizione esclusiva tra errore generico e warning specifico: l'errore persiste sempre al click, il warning si aggiunge nei due pattern nominati | Combinazioni C-003/C-004/C-006/C-007 (comportamento atteso al click per i pattern "assenza di @" e "assenza di parte dopo @"); i valori D-003/D-004 restano invariati | answered |

## Scenario warnings
Nessuno: tutti i requisiti D-001..D-005 sono risolti con valori ammessi e idonei;
nessun token TODO residuo nella feature.

## Optional catalogue
not-requested

## Readiness
`ready`: tutti i dati richiesti dal contesto sono risolti con valori sintetici
ammessi (autorizzazione esplicita dell'utente) e idonei rispetto ai vincoli
documentati in F-003/01-context.md. L'evidenza di disponibilità è
`documented-not-checked` per ciascun valore: trattandosi di dati sintetici di
solo inserimento campo (nessuna verifica di invio email o di stato di sistema
richiesta dallo UC), non è necessaria una verifica di ambiente live. Nessun
test è stato eseguito per produrre o confermare questi valori.

Rivalidazione (revisione 2): `01-context.md` è passato da revisione 1 a
revisione 2 (risposta umana a Q-001, 2026-10-16T11:22:35+02:00), invalidando
questo report anche a valori di D-001..D-005 invariati. Letto realmente il
contenuto di `01-context.md` revisione 2 (F-003, F-004, F-005, F-006, O-001,
O-003, O-004): i vincoli strutturali dei requisiti dati non sono cambiati, i
valori D-001..D-005 restano idonei senza modifiche. Il cambiamento riguarda
esclusivamente il comportamento atteso al click per i pattern "assenza di @"
e "assenza di parte dopo @" (combinazioni C-003/C-004/C-006/C-007): l'errore
generico resta sempre visibile e il warning specifico compare in aggiunta, non
in sostituzione. Relazione evidenza aggiornata in Combinations e decisione
Q-001 registrata in Decisions. Nessun dato è stato rigenerato o ereditato da
un contesto superato; questa è la prima riscrittura del report dopo
l'allocazione di Q-001 in 00-run.md.
