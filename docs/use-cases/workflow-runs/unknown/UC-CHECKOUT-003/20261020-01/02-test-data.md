---
schema: uc-workflow/v1
artifact: test-data
producer_skill: uc-test-data
task_id: unknown
uc_id: UC-CHECKOUT-003
run_id: 20261020-01
uc_input: 'C:\Users\dquero\Downloads\UC-CHECKOUT-003 - Back Navigation Control.txt'
uc_revision: "1"
environment: uat
revision: 1
status: incomplete
updated_at: "2026-10-20T13:26:52.455+02:00"
inputs:
  - path: docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/01-context.md
    revision: 2
---

# UC - Test data

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | C:\Users\dquero\Downloads\Note per gli sviluppatori.md | Codici Avviso; Codice Fiscale Ente Creditore | 2026-10-20 | uat nel contesto della richiesta; versione unknown | provided | Allegato iniziale |
| S-002 | docs/use-cases/test-data/checkout/checkout-test-data.md | Scopo e condizioni; Avviso completo disponibile; Carte di test; Dato complementare Email; Combinazioni candidate | 2026-10-20 | dev e uat dichiarati; versione unknown | approved | Q-007: risposta umana del 2026-10-20T13:26:52.455+02:00, punto 1; uso dei candidati come non verificati, incluso intestatario sintetico |
| S-003 | Messaggio umano del 2026-10-20T13:26:52.455+02:00 | Punto 1: autorizzazione dati e warning | 2026-10-20 | uat | provided | Conferma esplicita all'elenco di valori presentato |
| S-004 | C:\Users\dquero\Downloads\Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md | Formati avviso/CF; email; Flusso Carta; Flusso PayPal | 2026-10-20 | uat; versione unknown | provided | Allegato iniziale |

Letti i campi principali, le note, la tabella complementare con le email e le combinazioni candidate del catalogo. Tutti i 7 requisiti hanno valori: nessun campo dichiarato assente solo perche esterno alla tabella principale. Nessuna generazione di nuovi valori. Nessun utilizzo dei dati negativi o delle combinazioni PSP per aggiungere casi al requisito di navigazione. Nessuna esplorazione di src o docs/use-cases/features.

## Data resolution
| Data id | Scenario id | Parameter and constraints | Value or TODO token | Source id and passage | Admission | Fitness | Availability evidence | Unresolved reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | SC-002 | Avviso valido, 18 cifre, ente D-002, non pagato | C-002: 302042025112600001 | S-002, Avviso completo disponibile; S-001, famiglia 04 valida | approved | unverified | documented-not-checked: S-002, candidato per navigazione in uat, consultato 2026-10-20 | Formato compatibile; stato non pagato e disponibilita correnti da predisporre/verificare |
| D-001 | SC-003 | Stesso requisito avviso | C-003: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stesso stato corrente da verificare; nessun pagamento viene completato dal test |
| D-001 | SC-004 | Stesso requisito avviso | C-004: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e disponibilita correnti da verificare |
| D-001 | SC-005 | Stesso requisito avviso | C-005: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e compatibilita della combinazione con la carta da verificare |
| D-001 | SC-006 | Stesso requisito avviso | C-006: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e abilitazione percorso PayPal da verificare |
| D-001 | SC-007 | Stesso requisito avviso | C-007: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e abilitazione percorso Apple Pay da verificare |
| D-001 | SC-008 | Stesso requisito avviso | C-008: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e abilitazione percorso BANCOMAT Pay da verificare |
| D-001 | SC-009 | Stesso requisito avviso | C-009: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e abilitazione percorso MyBank da verificare |
| D-001 | SC-010 | Stesso requisito avviso | C-010: 302042025112600001 | S-002, Avviso completo disponibile | approved | unverified | documented-not-checked: S-002, uat | Stato e disponibilita correnti da verificare |
| D-002 | SC-002 | CF ente di 11 cifre associato all'avviso | C-002: 77777777777 | S-001, CF ente; S-002, coppia avviso completo/CF | provided | fit | documented-not-checked: S-001 e S-002, ente di test | Valore documentato; disponibilita corrente della coppia dipende da D-001 |
| D-002 | SC-003 | Stesso requisito CF | C-003: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-004 | Stesso requisito CF | C-004: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-005 | Stesso requisito CF | C-005: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-006 | Stesso requisito CF | C-006: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-007 | Stesso requisito CF | C-007: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-008 | Stesso requisito CF | C-008: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-009 | Stesso requisito CF | C-009: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-002 | SC-010 | Stesso requisito CF | C-010: 77777777777 | S-001, CF ente; S-002, coppia avviso/CF | provided | fit | documented-not-checked: S-001 e S-002 | Come D-001 della combinazione |
| D-003 | SC-004 | Email valida, uguale nella conferma | C-004: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione; casella non controllata | Nessuna verifica ricezione richiesta; intero percorso non verificato |
| D-003 | SC-005 | Stesso requisito email | C-005: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione | Intero percorso non verificato |
| D-003 | SC-006 | Stesso requisito email | C-006: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione | Intero percorso non verificato |
| D-003 | SC-007 | Stesso requisito email | C-007: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione | Intero percorso non verificato |
| D-003 | SC-008 | Stesso requisito email | C-008: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione | Intero percorso non verificato |
| D-003 | SC-009 | Stesso requisito email | C-009: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione | Intero percorso non verificato |
| D-003 | SC-010 | Stesso requisito email, conservare entrambi i valori | C-010: mail@pagopa.it in entrambi i campi | S-002, Dato complementare Email | approved | fit | documented-not-checked: S-002, compilazione | Percorso corrente non verificato; la conservazione e l'esito del test, non un dato gia accertato |
| D-004 | SC-005 | PAN esclusivamente di test | C-005: 5255000260000014 | S-002, Carte di test, riga Mastercard | approved | unverified | documented-not-checked: S-002, applicabile a dev e uat | Accettazione corrente per raggiungere lista PSP da verificare; autorizzato come non verificato da Q-007 |
| D-005 | SC-005 | Scadenza della stessa carta | C-005: 12/30 | S-002, stessa riga Mastercard | approved | fit | documented-not-checked: S-002, stessa carta | Futura rispetto al 2026-10-20; ricontrollare prima dell'esecuzione; accettazione della combinazione non verificata |
| D-006 | SC-005 | CVV della stessa carta di test | C-005: 123 | S-002, stessa riga Mastercard | approved | unverified | documented-not-checked: S-002, stessa carta | Coerenza documentata nella riga; accettazione corrente della carta da verificare |
| D-007 | SC-005 | Intestatario sintetico della stessa carta | C-005: Test test | S-002, stessa riga Mastercard e nota intestatario | approved | unverified | documented-not-checked: S-002, accettazione gateway da verificare | Nome sintetico esistente autorizzato da Q-007; non generato; accettazione non accertata |

## Combinations
| Combination id | Scenario id | Data ids and selected values | Relationship evidence | Fitness | Unresolved reason |
| --- | --- | --- | --- | --- | --- |
| C-001 | SC-001 | Nessuno | Nessun dato necessario per aprire inserimento avviso e tornare alla Home | fit | Nessuno |
| C-002 | SC-002 | D-001=302042025112600001; D-002=77777777777 | S-002, coppia Avviso completo disponibile; S-001, CF ente | unverified | Stato e disponibilita attuali dell'avviso da predisporre/verificare |
| C-003 | SC-003 | D-001=302042025112600001; D-002=77777777777 | Stessa coppia documentata; percorso email definito dal contesto | unverified | Stato e disponibilita attuali dell'avviso da predisporre/verificare |
| C-004 | SC-004 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi | Coppia documentata e email valida indipendente dall'avviso; nessun pagamento completato | unverified | Avviso e disponibilita metodo carta da verificare |
| C-005 | SC-005 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi; D-004=5255000260000014; D-005=12/30; D-006=123; D-007=Test test | S-002, coppia avviso/CF e unica riga Mastercard per tutti i dati carta; non si eredita la compatibilita di altre combinazioni PSP | unverified | Intera combinazione e accesso a lista PSP da verificare |
| C-006 | SC-006 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi; selezione funzionale PayPal | Stessi dati di ingresso; metodo da 01-context.md F-009 | unverified | Avviso, metodo e lista PSP disponibili da verificare |
| C-007 | SC-007 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi; selezione funzionale Apple Pay | Stessi dati di ingresso; metodo da 01-context.md F-009 | unverified | Avviso, metodo e lista PSP disponibili da verificare |
| C-008 | SC-008 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi; selezione funzionale BANCOMAT Pay | Stessi dati di ingresso; metodo da 01-context.md F-009 | unverified | Avviso, metodo e lista PSP disponibili da verificare |
| C-009 | SC-009 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi; selezione funzionale MyBank | Stessi dati di ingresso; metodo da 01-context.md F-009 | unverified | Avviso, metodo e lista PSP disponibili da verificare |
| C-010 | SC-010 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it nei 2 campi | Coppia documentata, uguaglianza email prescritta dal contesto; ritorno ammesso in Q-005 | unverified | Avviso e percorso correnti non verificati |

## Decisions
| Question id | Candidate or data ids | Human decision and date | Scope | State |
| --- | --- | --- | --- | --- |
| Q-007 | D-001..D-007; C-002..C-010 | Si, 2026-10-20T13:26:52.455+02:00, punto 1 | Includere i valori elencati come non verificati, mantenendo warning; nessun accesso alla casella o ricezione notifiche; nessuna generazione di ulteriori dati | answered |
| Q-008 | C-002..C-010 | Nessuna verifica corrente dichiarata dall'utente | Da predisporre/verificare avviso non pagato, carta accettata e metodi/lista PSP disponibili; l'approvazione non dimostra questi stati | open |

## Scenario warnings
| Scenario id | Affected combinations or all | Data ids | Required comment |
| --- | --- | --- | --- |
| SC-002 | C-002 | D-001, D-002 | Dati approvati ma non verificati in UAT: D-001, D-002; avviso valido e non pagato da verificare; scenario non pronto all'esecuzione |
| SC-003 | C-003 | D-001, D-002 | Dati approvati ma non verificati in UAT: D-001, D-002; avviso valido e non pagato da verificare; scenario non pronto all'esecuzione |
| SC-004 | C-004 | D-001, D-002, D-003 | Dati approvati ma percorso non verificato in UAT: D-001, D-002, D-003; avviso e metodo carta da verificare; scenario non pronto all'esecuzione |
| SC-005 | C-005 | D-001..D-007 | Dati approvati ma non verificati in UAT: D-001..D-007; avviso, accettazione carta e accesso lista PSP da verificare; scenario non pronto all'esecuzione |
| SC-006 | C-006 | D-001, D-002, D-003 | Tutte le righe dell'outline: dati approvati ma percorsi non verificati in UAT; D-001, D-002, D-003, avviso, metodi e lista PSP da verificare; scenario non pronto all'esecuzione |
| SC-007 | C-007 | D-001, D-002, D-003 | Stesso commento richiesto per tutte le righe dell'outline |
| SC-008 | C-008 | D-001, D-002, D-003 | Stesso commento richiesto per tutte le righe dell'outline |
| SC-009 | C-009 | D-001, D-002, D-003 | Stesso commento richiesto per tutte le righe dell'outline |
| SC-010 | C-010 | D-001, D-002, D-003 | Dati approvati ma percorso non verificato in UAT: D-001, D-002, D-003; avviso valido e non pagato da verificare; scenario non pronto all'esecuzione |

## Optional catalogue

not-requested

Nessun catalogo creato o modificato; il catalogo esistente e stato soltanto letto e i candidati sono stati ammessi per questa traduzione.

## Readiness

incomplete; bozza. Tutti i valori sono presenti e ammessi: nessun TODO necessario e nessun rifiuto umano da registrare. Restano Q-008 e gli stati richiesti da predisporre/verificare, non valori da inventare o dichiarare assenti. Conservare i commenti prescritti in ogni scenario interessato. SC-001 non richiede dati e non eredita dipendenze dai successivi scenari.

Controlli statici manuali: avviso di 18 cifre con prefisso 30204 nella famiglia valida; CF di 11 cifre; email conforme alla struttura documentata e uguale nei 2 campi; scadenza 12/30 futura alla data della traduzione; coerenza dei 4 dati carta come unica riga documentata; copertura di ogni D/SC nelle combinazioni e distinzione ammissione/idoneita/disponibilita. Identita e revisione 2 del contesto lette e compatibili col registro. Nessun test, accesso al gateway, query all'ambiente o completamento pagamento eseguito.
