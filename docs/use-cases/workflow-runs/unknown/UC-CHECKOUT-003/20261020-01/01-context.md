---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: unknown
uc_id: UC-CHECKOUT-003
run_id: 20261020-01
uc_input: 'C:\Users\dquero\Downloads\UC-CHECKOUT-003 - Back Navigation Control.txt'
uc_revision: "1"
environment: uat
revision: 2
status: ready
updated_at: "2026-10-20T13:26:52.455+02:00"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | C:\Users\dquero\Downloads\UC-CHECKOUT-003 - Back Navigation Control.txt | Precondizioni; FP 1-2; postcondizioni; AC-01 | 2026-10-20 | uat confermato; revisione 1 confermata | provided | Allegato iniziale e conferma punto 1 |
| S-002 | C:\Users\dquero\Downloads\Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md | Home Page; Inserimento Dati Avviso; Riepilogo Dati Pagamento; inserimento Email; scelta Metodo; flussi Carta e PayPal | 2026-10-20 | uat; versione unknown | provided | Allegato iniziale |
| S-003 | Messaggio umano del 2026-10-20T13:20:40.119+02:00 | Risposte 1-4 alle domande di inizializzazione | 2026-10-20 | uat; revisione UC 1 | provided | Conferma esplicita; Q-001..Q-004 nel registro |
| S-004 | C:\Users\dquero\Downloads\Note per gli sviluppatori.md | Codici Avviso; Codice Fiscale Ente Creditore | 2026-10-20 | uat nel contesto della richiesta; versione unknown | provided | Allegato iniziale |
| S-005 | docs/use-cases/test-data/checkout/checkout-test-data.md | Coppie per prove di navigazione indietro, riga /scegli-metodo verso /inserisci-email; Etichette e opzioni, Indietro | 2026-10-20 | dev e uat dichiarati; versione unknown | approved | Risposta umana del 2026-10-20T13:26:52.455+02:00, punto 2; solo questa transizione per il dettaglio funzionale mancante |
| S-006 | Messaggio umano del 2026-10-20T13:26:52.455+02:00 | Risposte 2 e 3 ai chiarimenti funzionali | 2026-10-20 | uat | provided | Conferma ritorno scelta metodo verso email; sola destinazione per Home e scelta metodo |

I link SANP e Jira presenti nello UC non sono stati consultati: non e disponibile un tool di lettura web. Nessun contenuto attribuito a tali pagine e usato come evidenza. Le fonti locali bastano per i percorsi indicati come supported; gli altri restano lacune esplicite. Nessuna esplorazione di src o della destinazione feature.

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | SC-001..SC-010 | Precondizioni; FP 1-2; postcondizioni; AC-01 | Che operazione si verifica? | Checkout aperto, lingua italiana; accedere a una pagina del flusso e tornare indietro 1 sola volta; pagina precedente e dati gia inseriti visibili. FP nel testo di AC-01 risolve il riferimento al flusso principale | S-001, sezioni indicate; S-003, punto 3 | supported |
| F-002 | SC-001 | FP 1-2; postcondizione destinazione | Percorso fino all'inserimento avviso e ritorno? | Dalla Home https://uat.checkout.pagopa.it/ la CTA di inserimento manuale apre /inserisci-dati-avviso; Indietro riporta alla Home | S-002, Home Page e Inserimento Dati Avviso | supported |
| F-003 | SC-002..SC-010 | FP 1; dati di partenza | Come si accede al riepilogo? | Compilare codice avviso di 18 cifre e CF ente di 11 cifre; Continua apre /dati-pagamento. Non introdurre validazioni negative, fuori UC | S-002, Inserimento Dati Avviso; S-004, Codici Avviso e CF ente | supported |
| F-004 | SC-002 | FP 2; entrambe le postcondizioni; AC-01 | Dove torna il riepilogo e quali campi si confrontano? | Indietro da /dati-pagamento torna a /inserisci-dati-avviso; i 2 campi restano visibili con i valori inseriti nello stesso scenario | S-002, Riepilogo Dati Pagamento; S-001, postcondizioni; S-003, punto 3 | supported |
| F-005 | SC-003 | FP 1-2; postcondizioni; AC-01 | Percorso email e ritorno? | Vai al pagamento dal riepilogo apre /inserisci-email; Indietro torna a /dati-pagamento. Il riepilogo espone codice avviso e CF ente: confrontarli con gli input precedenti, non con valori inventati di importo o oggetto | S-002, Riepilogo Dati Pagamento e inserimento Email; S-001, postcondizioni | supported |
| F-006 | SC-004..SC-010 | FP 1; percorso verso scelta metodo | Come si raggiunge la scelta del metodo? | Inserire email valida e uguale nei campi indirizzo email e Ripeti di nuovo; Continua apre /scegli-metodo | S-002, inserimento Email | supported |
| F-007 | SC-004..SC-005 | FP 1-2 | Percorso carta? | Selezionare Carta di Credito apre /inserisci-carta; Indietro torna a /scegli-metodo. Compilare numero, scadenza, CVV e Intestata a con dati validi e coerenti abilita Continua verso /lista-psp | S-002, Flusso Carta di Credito | supported |
| F-008 | SC-005 | FP 2; postcondizioni; AC-01 | Quali dati devono restare nella carta? | Indietro da /lista-psp del percorso carta torna a /inserisci-carta; tutti i 4 campi conservano i valori inseriti prima di Continua, CVV incluso. Il PAN deve essere confrontabile con quello inserito, senza assumere mascheramenti non specificati | S-002, Flusso Carta di Credito; S-001, postcondizioni; S-003, punto 3 | supported |
| F-009 | SC-006..SC-009 | FP 1-2; postcondizione destinazione | Quali varianti hanno lo stesso percorso? | Da /scegli-metodo selezionare PayPal, Apple Pay, BANCOMAT Pay o MyBank apre /lista-psp; Indietro torna a /scegli-metodo. Nessuna selezione PSP e richiesta per tornare indietro | S-002, Flusso PayPal e frase di equivalenza dei 4 metodi | supported |
| F-010 | SC-001, SC-004, SC-006..SC-009 | Postcondizione dati; AC-01 | Quali dati risultano visibili nella destinazione? | Home e scelta metodo non hanno input compilati documentati; per questi ritorni l'utente conferma la sola verifica della destinazione. Non verificare una selezione persistente non specificata | S-002, Home Page e scelta Metodo; S-006, punto 3 | supported |
| F-011 | SC-010 | FP 2; postcondizioni; AC-01 | Ritorno dalla scelta metodo? | Indietro da /scegli-metodo torna a /inserisci-email; indirizzo email e Ripeti di nuovo conservano il valore inserito nello stesso scenario | S-005, coppia scelta metodo verso email; S-003, conservazione campi; S-006, punto 2 | supported |
| F-012 | SC-001..SC-010 | AF; EF | Sezioni vuote? | Nessun AF/EF previsto. I diversi metodi sono varianti del percorso documentato, non nuovi AF o casi negativi | S-003, punto 4 | supported |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |
| SC-001 | Precondizioni; FP 1-2 | Given Checkout aperto in italiano sulla Home; When apertura inserimento manuale; And pressione Indietro 1 sola volta; Then Home | F-001, F-002, F-010 | Home e setup indipendente; accesso alla pagina sotto test resta un'azione. La verifica dati non si applica alla Home secondo conferma umana |
| SC-002 | FP 1 | Apertura inserimento manuale; compilazione congiunta codice avviso e CF; Continua | F-002, F-003 | Esplicitare il percorso che crea i dati e la storia di navigazione da conservare. I 2 input sono un'unica azione funzionale; Continua e il cambio pagina richiesto |
| SC-002 | FP 2; postcondizioni | Indietro 1 sola volta; verifica pagina inserimento e confronto dei 2 valori con quelli inseriti nello scenario | F-001, F-004 | Destinazione e conservazione sono verifiche compatibili della stessa operazione; non concatenare altri ritorni |
| SC-003 | FP 1 | Percorso esplicito Home, inserimento avviso, Continua, Vai al pagamento | F-002, F-003, F-005 | Non simulare l'apertura diretta dell'email perdendo storia e avviso precedente; non compilare email inutilmente per verificare i dati della pagina precedente |
| SC-003 | FP 2; postcondizioni | Indietro 1 sola volta; verifica riepilogo e codice avviso/CF uguali agli input precedenti | F-001, F-005 | Non introdurre importi o nomi non definiti; i valori derivati del riepilogo non sono dati inseriti dall'utente |
| SC-004..SC-009 | FP 1 | Percorso Home, avviso, Continua, Vai al pagamento, compilazione congiunta delle 2 email uguali, Continua | F-002, F-003, F-005, F-006 | La storia resta esplicita nei When; Background contiene solo Checkout aperto in italiano sulla Home |
| SC-004 | FP 1-2 | Selezione Carta di Credito; Indietro 1 sola volta; verifica scelta metodo | F-007, F-010 | Percorso distinto da SC-005; non compilare carta se la destinazione non e una pagina carta; sola destinazione come confermato dall'utente |
| SC-005 | FP 1 | Selezione Carta di Credito; compilazione congiunta dei 4 dati carta; Continua | F-007 | La compilazione carta e coesa; separare Continua per rendere esplicito l'avanzamento richiesto prima del ritorno |
| SC-005 | FP 2; postcondizioni | Indietro 1 sola volta; pagina inserimento carta e confronto di numero, scadenza, CVV e intestatario | F-001, F-008 | Una sola operazione e 4 verifiche compatibili; il CVV non viene omesso; nessuna selezione PSP necessaria |
| SC-006..SC-009 | FP 1-2 | Selezione del metodo variabile; Indietro 1 sola volta; verifica scelta metodo | F-009, F-010 | Proposto un outline con 4 righe: stesso percorso e stessi controlli, nessuno script nascosto nelle celle |
| SC-010 | FP 1-2; postcondizioni | Percorso esplicito Home, avviso, riepilogo, compilazione delle 2 email, Continua; Indietro 1 sola volta; verifica pagina email e confronto dei 2 campi | F-002, F-003, F-005, F-006, F-011 | Conservare l'intera sequenza che crea i dati da verificare; 1 ritorno, 2 verifiche compatibili. Destinazione ora confermata, non inferita dalla URL |

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |
| O-001 | SC-001 | Postcondizione destinazione; AC-01 parziale | Home https://uat.checkout.pagopa.it/ dopo 1 Indietro dall'inserimento avviso | not-applicable | F-001, F-002 | supported |
| O-002 | SC-002 | Entrambe le postcondizioni; AC-01 (FP) | /inserisci-dati-avviso; codice avviso e CF ente visibili e uguali ai valori inseriti nel medesimo scenario | not-applicable | F-001, F-004 | supported |
| O-003 | SC-003 | Entrambe le postcondizioni; AC-01 (FP) | /dati-pagamento; codice avviso e CF ente ancora visibili e uguali agli input precedenti | not-applicable | F-001, F-005 | supported |
| O-004 | SC-004, SC-006..SC-009 | Postcondizione destinazione; AC-01 parziale | /scegli-metodo, dopo 1 Indietro dalla pagina del percorso effettivamente visitato | not-applicable | F-007, F-009 | supported |
| O-005 | SC-005 | Entrambe le postcondizioni; AC-01 (FP) | /inserisci-carta; numero, scadenza, CVV e Intestata a visibili e uguali agli input precedenti | not-applicable | F-001, F-008 | supported |
| O-006 | SC-010 | Entrambe le postcondizioni; AC-01 (FP) | /inserisci-email; indirizzo email e Ripeti di nuovo visibili e uguali al valore inserito prima di Continua | not-applicable | F-011 | supported |
| O-007 | SC-001, SC-004, SC-006..SC-009 | Postcondizione dati; AC-01 (FP) | Controllo dati non applicabile ai ritorni verso Home e scelta metodo; verificare soltanto la destinazione, come confermato dall'utente | not-applicable | F-010 | supported |

Nessuna soglia temporale, codice tecnico o messaggio di errore e richiesto. I nomi dei pulsanti e le destinazioni derivano da S-002; la cardinalita 1 da S-001 e S-003.

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |
| D-001 | SC-002..SC-010 | Codice avviso per il percorso | Stringa di 18 cifre; famiglia valida 302 + YY tra 00 e 27 + 13 cifre; usare lo stesso valore nel confronto dopo il ritorno | Avviso valido e non gia pagato, associato all'ente di D-002; disponibile in uat | F-003, F-004, F-005 |
| D-002 | SC-002..SC-010 | CF ente creditore | Stringa di 11 cifre; abbinata a D-001; confronto con l'input precedente, non CF personale | Ente di test compatibile con l'avviso | F-003, F-004, F-005 |
| D-003 | SC-004..SC-010 | Indirizzo email e ripetizione | Indirizzo valido con nome, @, dominio e suffisso alfabetico di almeno 2 caratteri; stesso valore nei 2 campi; non verificare ricezione notifiche | Email utilizzabile per compilazione nel test, non richiede accesso alla casella per questo UC | F-006 |
| D-004 | SC-005 | Numero carta | PAN di test valido e coerente con D-005..D-007; non usare carta reale | Carta di test accettata per raggiungere lista PSP in uat | F-007, F-008 |
| D-005 | SC-005 | Scadenza carta | Valida e futura alla data di esecuzione; parte della stessa carta D-004 | Consente avanzamento dalla pagina carta | F-007, F-008 |
| D-006 | SC-005 | CVV | Valido per la stessa carta di D-004; deve restare visibile e uguale dopo il ritorno secondo conferma umana | Dato esclusivamente di carta di test | F-007, F-008 |
| D-007 | SC-005 | Intestata a | Intestatario sintetico valido, coerente con i dati carta | Accettato nel contesto di test | F-007, F-008 |

Le varianti PayPal, Apple Pay, BANCOMAT Pay e MyBank sono selezioni funzionali enumerate da S-002, non valori arbitrari. Non occorre scegliere un PSP, inviare un pagamento o conoscere commissioni per verificare questi ritorni. La disponibilita corrente di metodi, avviso e carta non e provata dalla documentazione.

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-003 | SC-001..SC-010 | Distinguere Indietro applicativo da browser; cardinalita; conservazione CVV | Conferma umana del 2026-10-20T13:20:40.119+02:00, punto 3: Indietro applicativo, 1 ritorno, tutti i campi inclusi quelli carta e CVV | answered |
| Q-004 | SC-001..SC-010 | Sezioni AF/EF vuote | Stessa risposta, punto 4: nessun AF/EF previsto | answered |
| Q-005 | SC-010 | Controllo Indietro e destinazione dalla scelta metodo non specificati negli allegati | Risposta umana del 2026-10-20T13:26:52.455+02:00, punto 2: conferma Indietro verso email e conservazione dei 2 campi; ammessa la coppia del catalogo | answered |
| Q-006 | SC-001, SC-004, SC-006..SC-009 | Conservazione dati non osservabile nelle destinazioni senza input documentati | Stessa risposta, punto 3: verificare solo la destinazione in questi casi; conservazione dove sono presenti i campi | answered |

## Readiness

ready per il dettaglio funzionale, non per l'esecuzione. Sono supportati 10 casi di navigazione con 1 ritorno ciascuno, di cui SC-002, SC-003, SC-005 e SC-010 hanno anche confronti dei dati osservabili e definiti. Negli altri casi il controllo dati non si applica secondo Q-006. Nessuna lacuna funzionale resta aperta per questo perimetro.

Il catalogo contiene anche una coppia generica /lista-psp verso /scegli-metodo: non viene applicata al percorso carta, per il quale l'allegato funzionale prescrive esplicitamente /inserisci-carta. La conferma Q-005 ammette soltanto il dettaglio mancante scelta metodo verso email. Nessuna sequenza di ritorni, modifica dal riepilogo o verifica di assenza loop viene aggiunta a questo UC.

Lo UC non viene modificato: si segnala l'ambiguita di "pagina iniziale del flusso" nell'AC rispetto a "una pagina del flusso" del FP; i percorsi effettivamente documentati definiscono i casi proposti senza trasformare la Home in una pagina con precedente non specificata. AF/EF vuoti sono risolti dalla conferma umana, non considerati lacune. JTBD-001 resta sola tracciabilita, non una narrativa inventata.

Handoff a uc-test-data: D-001..D-007, vincoli e casi sopra elencati. Nessun test, parser o comando terminale eseguito. Controllo statico manuale di fonti, cardinalita, distinzione azioni/prerequisiti/esiti e assenza di dipendenze tra scenari. Nessuna lezione ACE attiva; nessuna traccia ACE scritta.
