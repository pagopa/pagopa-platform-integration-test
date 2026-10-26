---
schema: uc-workflow/v1
artifact: test-data
producer_skill: uc-test-data
task_id: checkout-traduzione
uc_id: UC-CHECKOUT-001
run_id: 20261020-01
uc_input: 'C:\Users\dquero\Downloads\UC-CHECKOUT-001 - Attivazione pagamento Checkout.txt'
uc_revision: v1
environment: uat
revision: 1
status: incomplete
updated_at: "2026-10-20T16:41:36.150+02:00"
inputs:
  - path: docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/01-context.md
    revision: 1
---

# UC - Test data

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | docs/use-cases/test-data/checkout/checkout-test-data.md | Letto integralmente, righe 1-223; inclusi Scopo, avviso completo, carte, dati complementari, PSP, combinazioni e avvisi negativi | 2026-10-20 | dev e uat espliciti; disponibilita dipendente dalla configurazione; versione unknown | provided | Allegato umano; autorizzazione ai dati non verificati e sintetici gia presenti, punto 3 risposta 2026-10-20T16:41:36.150+02:00 |
| S-002 | C:/Users/dquero/Downloads/Note per gli sviluppatori.md | Codici Avviso; CF Ente Creditore | 2026-10-20 | Ambiente test, versione unknown | provided | Allegato iniziale; nessuna autorizzazione a generare nuovi avvisi |
| S-003 | C:/Users/dquero/Downloads/Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md | Campi avviso, email, carta; famiglie di metodi | 2026-10-20 | uat, versione unknown | provided | Allegato iniziale |
| S-004 | Chat della presente sessione | Risposta 2026-10-20T16:41:36.150+02:00, punto 3 | 2026-10-20 | uat, solo questa prova | provided | Si all'uso dei dati gia documentati non verificati, senza generazione aggiuntiva |
| S-005 | docs/use-cases/test-data/ e docs/use-cases/test-data/checkout/ | Elenchi directory mediante view: solo checkout e checkout-test-data.md | 2026-10-20 | Ricerca locale, non ambiente applicativo | provided | Directory autorizzata dall'umano; nessun altro candidato trovato qui. Non ricercate cartelle vietate o fonti eseguibili |

## Data resolution
| Data id | Scenario id | Parameter and constraints | Value or TODO token | Source id and passage | Admission | Fitness | Availability evidence | Unresolved reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | SC-001-SC-010 | Avviso 18 cifre associato al CF D-002, utilizzabile e non pagato | 302042025112600001 | S-001 Avviso completo disponibile; candidato per inserimento, riepilogo e navigazione | provided | unverified | documented-not-checked: catalogo dev/uat; verifica stato pagamento richiesta | Codice concreto presente, non mancante; stato corrente e utilizzabilita con ogni metodo non provati. Non generati suffissi nuovi |
| D-002 | SC-001-SC-014 | CF EC 11 cifre associato agli avvisi | 77777777777 | S-001 Ente creditore e lingua, avvisi positivi e negativi; S-002 CF EC | provided | fit | documented-not-checked: ente di test documentato per dev/uat | Nessuna verifica live della configurazione |
| D-003 | SC-001-SC-010 | Email valida uguale nei due campi | mail@pagopa.it | S-001 Dato complementare Email, candidato per compilazione e conferma | provided | fit | documented-not-checked: documentata per compilazione, uso autorizzato in Q-007 | Non verificata ricezione, fuori scope; nessun accesso alla casella presunto |
| D-004 | SC-001 | PAN, scadenza futura, CVV, intestatario e compatibilita PSP | PAN 5255000260000014; scadenza 12/30; CVV 123; intestatario sintetico Test test | S-001 Carte di test, riga Mastercard, e spiegazioni adiacenti | provided | unverified | documented-not-checked: carta di test; scadenza futura rispetto al 2026-10-20 | Accettazione nome e gateway non provata. Tutti e 4 i campi presenti, nessun dato personale reale |
| D-005 | SC-001 | PSP carta coerente con Mastercard | Postepay | S-001 Carte di test cita Postepay compatibile; Metodi di pagamento e PSP | provided | unverified | documented-not-checked: associazione PSP/carta candidata | Associazione al metodo e avviso attuale da verificare. Non si dichiara che l'avviso 30204 appartenga alle combinazioni 30200/30201 |
| D-005 | SC-002 | PSP selezionabile per PayPal, identificativo distinto da nome | BCITITMM | S-001 ID PSP per PayPal | provided | unverified | documented-not-checked: ID candidato per PayPal | Nome commerciale e disponibilita non confermati; usare l'ID come identificativo, non come testo UI |
| D-005 | SC-004 | PSP selezionabile per Apple Pay | __TODO_D005__ | S-001 sezione PSP; S-003 Flusso PayPal; S-005 ricerca locale | unknown | unverified | unknown-to-prepare: PSP Apple Pay da reperire | Il flusso e documentato, ma non un PSP applicabile; non estendere BCITITMM da PayPal ad Apple Pay |
| D-005 | SC-005 | PSP selezionabile per BANCOMAT Pay | __TODO_D005__ | S-001 sezione PSP; S-003 Flusso PayPal; S-005 ricerca locale | unknown | unverified | unknown-to-prepare: PSP BANCOMAT Pay da reperire | Nessun valore specifico nel materiale letto |
| D-005 | SC-010 | PSP selezionabile per MyBank | __TODO_D005__ | S-001 sezione PSP; S-003 Flusso PayPal; S-005 ricerca locale | unknown | unverified | unknown-to-prepare: PSP MyBank da reperire | Nessun valore specifico nel materiale letto |
| D-006 | SC-001-SC-010 | Metodo corrente abilitato e selezionabile | C-001 Carta di credito; C-002 PayPal; C-003 Google Pay; C-004 Apple Pay; C-005 BANCOMAT Pay; C-006 Conto iCONTO; C-007 Conto Intesa Sanpaolo; C-008 Fabrick Pay By Bank; C-009 Klarna; C-010 MyBank | S-003 famiglie funzionali; S-001 Scopo e condizioni | provided | unverified | documented-not-checked: metodi documentati, abilitazione dipendente dalla configurazione | Nomi funzionali del contesto, non etichette esatte o codici tecnici garantiti |
| D-007 | SC-011 | Avviso sconosciuto, 18 cifre | 302400000000000000 | S-001 Avvisi per prove di errore, estremo iniziale sconosciuto | provided | unverified | documented-not-checked: associazione mock da verificare | Valore completo gia documentato, non generato; corrispondenza errore non provata |
| D-007 | SC-012 | Avviso scaduto, 18 cifre | 302990000000000000 | S-001 Avvisi per prove di errore, estremo iniziale scaduto | provided | unverified | documented-not-checked: associazione mock da verificare | Valore completo gia documentato, non generato; corrispondenza errore non provata |
| D-007 | SC-013 | Avviso per timeout, 18 cifre | 302980000000000000 | S-001 Avvisi per prove di errore, estremo iniziale timeout | provided | unverified | documented-not-checked: associazione mock da verificare | Valore completo gia documentato, non generato; corrispondenza errore non provata |
| D-007 | SC-014 | Avviso duplicato, singolo valore documentato | 302950100443009424 | S-001 Avvisi per prove di errore, riga duplicato | provided | unverified | documented-not-checked: associazione mock da verificare | Nessun pagamento preparatorio nel test; configurazione simulata da verificare |
| D-008 | SC-001-SC-014 | Lingua italiana collegata agli oracle testuali | it | S-001 Ente creditore e lingua; 01-context.md F-001 | provided | fit | documented-not-checked: precondizione richiesta dallo UC, da stabilire nella sessione | Nessuna sessione aperta o interrogata dall'analista |

## Combinations
| Combination id | Scenario id | Data ids and selected values | Relationship evidence | Fitness | Unresolved reason |
| --- | --- | --- | --- | --- | --- |
| C-001 | SC-001 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-004={PAN:5255000260000014, scadenza:12/30, CVV:123, intestatario:Test test}; D-005=Postepay; D-006=Carta di credito; D-008=it | S-001 avviso completo con CF, Mastercard per Postepay, email per conferma. Questi valori permettono un candidato di navigazione, non una combinazione avviso/carta/PSP garantita | unverified | Stato avviso, metodo e compatibilita effettiva da verificare; nessun nuovo valore sintetico generato |
| C-002 | SC-002 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-005=BCITITMM; D-006=PayPal; D-008=it | S-001 ID esplicitamente candidato per PayPal; stesso avviso candidato alla navigazione | unverified | Avviso e metodo/PSP da verificare |
| C-003 | SC-003 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-006=Google Pay; D-008=it | 01-context.md F-006; nessuna scelta PSP iniziale | unverified | Avviso e metodo da verificare |
| C-004 | SC-004 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-005=__TODO_D005__; D-006=Apple Pay; D-008=it | 01-context.md F-005; PSP specifico assente | unverified | PSP da reperire; avviso e metodo da verificare |
| C-005 | SC-005 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-005=__TODO_D005__; D-006=BANCOMAT Pay; D-008=it | 01-context.md F-005; PSP specifico assente | unverified | PSP da reperire; avviso e metodo da verificare |
| C-006 | SC-006 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-006=Conto iCONTO; D-008=it | 01-context.md F-006; nessuna scelta PSP iniziale | unverified | Avviso e metodo da verificare |
| C-007 | SC-007 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-006=Conto Intesa Sanpaolo; D-008=it | 01-context.md F-006; nessuna scelta PSP iniziale | unverified | Avviso e metodo da verificare |
| C-008 | SC-008 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-006=Fabrick Pay By Bank; D-008=it | 01-context.md F-006 e F-013; nessuna scelta PSP iniziale | unverified | Avviso e metodo da verificare |
| C-009 | SC-009 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-006=Klarna; D-008=it | 01-context.md F-006; nessuna scelta PSP iniziale | unverified | Avviso e metodo da verificare |
| C-010 | SC-010 | D-001=302042025112600001; D-002=77777777777; D-003=mail@pagopa.it in entrambi i campi; D-005=__TODO_D005__; D-006=MyBank; D-008=it | 01-context.md F-005; PSP specifico assente | unverified | PSP da reperire; avviso e metodo da verificare |
| C-011 | SC-011 | D-007=302400000000000000; D-002=77777777777; D-008=it | S-001 riga sconosciuto e CF EC prescritto per gli errori | unverified | Mock da verificare |
| C-012 | SC-012 | D-007=302990000000000000; D-002=77777777777; D-008=it | S-001 riga scaduto e CF EC prescritto per gli errori | unverified | Mock da verificare |
| C-013 | SC-013 | D-007=302980000000000000; D-002=77777777777; D-008=it | S-001 riga timeout e CF EC prescritto per gli errori | unverified | Mock da verificare |
| C-014 | SC-014 | D-007=302950100443009424; D-002=77777777777; D-008=it | S-001 riga duplicato e CF EC prescritto per gli errori | unverified | Mock da verificare |

## Decisions
| Question id | Candidate or data ids | Human decision and date | Scope | State |
| --- | --- | --- | --- | --- |
| Q-007 | D-001-D-008; C-001-C-014 | Si, punto 3 risposta 2026-10-20T16:41:36.150+02:00 | Usare dati gia documentati, anche sintetici, con warning e senza generarne altri; resta distinta la fitness dalla disponibilita | answered |
| Q-008 | D-005 in C-004, C-005, C-010 | Nessuna scelta concreta disponibile nel materiale letto; 2026-10-20 | PSP Apple Pay, BANCOMAT Pay e MyBank da reperire; mantenuti TODO distinti per caso dello stesso requisito, non assunzione di uguale PSP | open |

## Scenario warnings
| Scenario id | Affected combinations or all | Data ids | Required comment |
| --- | --- | --- | --- |
| SC-001 | C-001 | D-001, D-002, D-004, D-005, D-006, D-008 | Dati e stati non verificati nell'ambiente: avviso, carta/PSP, metodo, ente e lingua; scenario non pronto all'esecuzione |
| SC-002, SC-004, SC-005, SC-010 | C-002, C-004, C-005, C-010 | D-001, D-002, D-005, D-006, D-008 | Tutte le righe non verificate nell'ambiente; D-005 irrisolto nelle righe Apple Pay, BANCOMAT Pay e MyBank; scenario non pronto all'esecuzione |
| SC-003, SC-006-SC-009 | C-003, C-006-C-009 | D-001, D-002, D-006, D-008 | Tutte le righe: avviso, metodo, ente e lingua non verificati nell'ambiente; scenario non pronto all'esecuzione |
| SC-011-SC-013 | C-011-C-013 | D-002, D-007, D-008 | Tutte le righe: associazione mock/errore e stati non verificati nell'ambiente; scenario non pronto all'esecuzione |
| SC-014 | C-014 | D-002, D-007, D-008 | Associazione mock/duplicato e stati non verificati nell'ambiente; scenario non pronto all'esecuzione |

## Optional catalogue
not-requested

Il catalogo allegato e stato letto e non modificato; nessun nuovo record salvato.

## Readiness
incomplete, bozza: dati non verificati ammessi esplicitamente ma non provati,
D-005 da reperire per SC-004, SC-005 e SC-010 (Q-008). Gli altri valori esistono
nelle fonti: non sono dichiarati mancanti per la sola incertezza live.
L'unico catalogo scoperto nella directory autorizzata coincide con quello
fornito; nessuna fonte aggiuntiva adottata. Gli intervalli sono stati risolti
usando esclusivamente gli estremi completi gia scritti nel documento.
Nessun prodotto cartesiano, nessun nuovo codice o intestatario generato.
Le 3 combinazioni prefisso/carta/PSP del catalogo non vengono spacciate per
combinazioni valide con il diverso avviso completo: C-001 resta candidata
non verificata, coerentemente con l'ammissione umana. Gli altri PSP della
tabella non costituiscono automaticamente ulteriori casi del requisito.
SC-015 non ha combinazione: escluso dal test. Ogni caso positivo richiede
uno stato indipendente dell'avviso; il riuso della stringa non impone ordine
di esecuzione e non autorizza pulizia automatica dell'ambiente.
Nessun test o controllo live eseguito.
