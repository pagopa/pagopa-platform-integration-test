---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: "back-navigation-control"
uc_id: "UC-CHECKOUT-003"
run_id: "20261020-01"
uc_input: "C:\\Users\\dquero\\Downloads\\UC-CHECKOUT-003 - Back Navigation Control.txt"
uc_revision: "1"
environment: uat
revision: 2
status: incomplete
updated_at: "2026-10-20T10:54:20+02:00"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | C:\Users\dquero\Downloads\UC-CHECKOUT-003 - Back Navigation Control.txt | Intero documento | 2026-10-20T10:54:20+02:00 | UAT (dichiarato nello UC) | provided | Confermato dall'orchestratore (task corrente) |
| S-002 | C:\Users\dquero\Downloads\Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md | Sezioni "Home Page", "Inserimento Dati Avviso", "Pagina Riepilogo Dati Pagamento", "Pagina di inserimento Email", "Pagina scelta Metodo di Pagamento" (Flusso Carta di Credito; Flusso PayPal/Apple Pay/BANCOMAT Pay/MyBank; Flusso Google Pay e equivalenti) | 2026-10-20T10:54:20+02:00 | UAT (dichiarato nel titolo del documento) | provided | Confermato dall'orchestratore (task corrente) |
| S-003 | C:\Users\dquero\Downloads\Note per gli sviluppatori.md | "Codici Avviso", "Codice Fiscale Ente Creditore (EC)" | 2026-10-20T10:54:20+02:00 | unknown | provided | Fornito dall'orchestratore; generazione sintetica per D-001 e D-003/D-004 AUTORIZZATA dall'umano in questa run (00-run.md Q-001, rettifica rispetto alla precedente registrazione erronea di rifiuto); D-002 (CF EC 77777777777) e' un valore direttamente fornito da questa fonte, non richiede tale autorizzazione |

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | SC-001..SC-006 | AC-01, Postcondizioni | Quale azione conclude il flusso oggetto dello UC e quale esito va verificato? | L'utente accede ad una pagina del flusso, preme una sola volta il pulsante "Indietro" e si ritrova nella pagina precedente del flusso | S-001, FP step 1-2, AC-01, Postcondizioni | supported |
| F-002 | SC-001 | Flusso principale, pulsanti "Home Page" / "Inserimento Dati Avviso" | Quale pagina precede `inserisci-dati-avviso` tramite il pulsante indietro? | "il tasto indietro che riporta nella pagina precedente del flusso (https://uat.checkout.pagopa.it/)" dalla pagina `inserisci-dati-avviso` | S-002, sezione "Inserimento Dati Avviso" | supported |
| F-003 | SC-002 | Pagina "Riepilogo Dati Pagamento" | Quale pagina precede `dati-pagamento` tramite il pulsante indietro? | "i due pulsanti di navigazione Indietro che riporterà alla pagina precedete ossia quella di inserimento dati avviso" | S-002, sezione "Pagina Riepilogo Dati Pagamento" | supported |
| F-004 | SC-003 | Pagina "inserimento Email" | Quale pagina precede `inserisci-email` tramite il pulsante indietro? | "il tasto indietro che riporta nella pagina precedente del flusso (.../dati-pagamento)" | S-002, sezione "Pagina di inserimento Email" | supported |
| F-005 | SC-004 | Flusso Carta di Credito, pagina "inserisci-carta" | Quale pagina precede `inserisci-carta` tramite il pulsante indietro? | "i pulsanti indietro che riporta l'utente alla pagina precedente del flusso (.../scegli-metodo)" | S-002, sezione "Flusso Carta di Credito" | supported |
| F-006 | SC-005 | Flusso Carta di Credito, pagina "lista-psp" (ramo carta) | Quale pagina precede `lista-psp` tramite il pulsante indietro quando si arriva dal ramo carta? | "i pulsanti indietro che riporta l'utente alla pagina di inserimento dati carta" | S-002, sezione "Flusso Carta di Credito" | supported |
| F-007 | SC-006 | Flusso PayPal (coincidente con Apple Pay, BANCOMAT Pay, MyBank), pagina "lista-psp" (ramo metodi alternativi) | Quale pagina precede `lista-psp` tramite il pulsante indietro quando si arriva da PayPal/Apple Pay/BANCOMAT Pay/MyBank? | "i pulsanti indietro che riporta l'utente alla pagina della scelta del metodo di pagamento"; "il flusso appena descritto e' identico per i metodi Apple Pay, BANCOMAT Pay, MyBank" | S-002, sezione "Flusso PayPal" | supported |
| F-008 | — | Pagina "scegli-metodo" | Esiste un pulsante indietro generico documentato sulla pagina di scelta metodo di pagamento? | Nessun pulsante indietro e' descritto per la pagina `scegli-metodo` stessa nel documento funzionale | S-002, sezione "Pagina scelta Metodo di Pagamento" (assenza di menzione) | unresolved |
| F-009 | — | Pagina "riepilogo-pagamento" | Esiste un pulsante indietro generico (analogo a quelli delle pagine precedenti) sulla pagina di riepilogo pagamento? | Sono documentati solo pulsanti "modifica" (per sezione "Paga con" e "Commissione") e il pulsante "Annulla" con popup dedicato; nessun pulsante "indietro" generico e' descritto | S-002, sezioni "Flusso Carta di Credito" e "Flusso PayPal" (parte finale) | unresolved |
| F-010 | — | Flusso Google Pay (coincidente con Conto iConto, Intesa Sanpaolo, Fabrik Pay By Bank, Klarna) | Esiste un pulsante indietro generico dalla pagina di riepilogo pagamento raggiunta da questo ramo? | Il documento descrive solo i pulsanti "modifica" (verso `scegli-metodo` e verso `lista-psp`) e "Annulla"; nessun pulsante "indietro" generico verso una pagina precedente e' descritto per questo ramo | S-002, sezione "Flusso Google Pay" | unresolved |
| F-011 | — | Ambito dello UC (pulsante UI vs comando "indietro" del browser) | Lo UC distingue la pressione del pulsante "Indietro" dell'interfaccia dalla funzione "indietro" nativa del browser? | Lo UC non distingue le due modalita'; solo i pulsanti "Indietro" di interfaccia documentati nel documento funzionale hanno evidenza di comportamento supportato. Nessuna copertura e' desumibile per il tasto "indietro" del browser | S-001, FP step 1-2; S-002 (nessuna menzione del comando browser) | unresolved |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |
| SC-001 | FP 1-2 | `Quando` l'utente accede a `inserisci-dati-avviso` (dalla home); `E` preme una sola volta "Indietro"; `Allora` si trova in `home` | F-001, F-002 | Azione unica di accesso + singola pressione back, nessuna sotto-azione produce un esito osservabile intermedio da verificare separatamente |
| SC-002 | FP 1-2 | `Dato` un avviso di pagamento valido inserito e confermato dalla pagina `inserisci-dati-avviso`; `Quando` l'utente accede a `dati-pagamento`; `E` preme una sola volta "Indietro"; `Allora` si trova in `inserisci-dati-avviso` | F-001, F-003 | La predisposizione dei dati avviso e' uno stato di partenza (Dato), non un comportamento sotto test di questo UC |
| SC-003 | FP 1-2 | `Dato` un avviso di pagamento valido confermato fino a `dati-pagamento`; `Quando` l'utente accede a `inserisci-email`; `E` preme "Indietro"; `Allora` si trova in `dati-pagamento` | F-001, F-004 | Idem SC-002, stato di partenza piu' avanzato nel flusso |
| SC-004 | FP 1-2 | `Dato` avviso ed email validi confermati fino a `scegli-metodo`; `Quando` l'utente accede a `inserisci-carta` selezionando "Carta di Credito"; `E` preme "Indietro"; `Allora` si trova in `scegli-metodo` | F-001, F-005 | Idem, stato di partenza con dati avviso+email gia' predisposti |
| SC-005 | FP 1-2 | `Dato` avviso, email e dati carta validi confermati fino a `inserisci-carta`; `Quando` l'utente accede a `lista-psp` (ramo carta); `E` preme "Indietro"; `Allora` si trova in `inserisci-carta` | F-001, F-006 | Idem, richiede anche dati carta per raggiungere `lista-psp` dal ramo carta |
| SC-006 | FP 1-2 | `Dato` avviso ed email validi confermati fino a `scegli-metodo` con il metodo "PayPal" selezionato, campione rappresentante nominato esplicitamente; `Quando` l'utente accede a `lista-psp` (ramo metodi alternativi); `E` preme "Indietro"; `Allora` si trova in `scegli-metodo` | F-001, F-007 | Il documento dichiara i 4 flussi identici (PayPal, Apple Pay, BANCOMAT Pay, MyBank): PayPal e' scelto come campione rappresentante nominato esplicitamente; Apple Pay, BANCOMAT Pay e MyBank restano documentati come equivalenti ma non campionati singolarmente, senza prodotto cartesiano per singolo metodo |

SC-001..SC-006 condividono lo stesso comportamento verificato (FP + AC-01): differiscono solo per pagina iniziale, pagina precedente e stato di predisposizione richiesto. In fase di progettazione scenario (uc-to-feature) questo giustifica un unico `Scenario Outline` con una riga per caso, secondo la regola delle varianti dati dello stesso flusso.

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |
| O-001 | SC-001 | AC-01 (FP); Postcondizioni | Pagina corrente dopo la singola pressione di "Indietro" = `home` | not-applicable | F-001, F-002 | supported |
| O-001 | SC-002 | AC-01 (FP); Postcondizioni | Pagina corrente dopo la singola pressione di "Indietro" = `inserisci-dati-avviso` | not-applicable | F-001, F-003 | supported |
| O-001 | SC-003 | AC-01 (FP); Postcondizioni | Pagina corrente dopo la singola pressione di "Indietro" = `dati-pagamento` | not-applicable | F-001, F-004 | supported |
| O-001 | SC-004 | AC-01 (FP); Postcondizioni | Pagina corrente dopo la singola pressione di "Indietro" = `scegli-metodo` | not-applicable | F-001, F-005 | supported |
| O-001 | SC-005 | AC-01 (FP); Postcondizioni | Pagina corrente dopo la singola pressione di "Indietro" = `inserisci-carta` | not-applicable | F-001, F-006 | supported |
| O-001 | SC-006 | AC-01 (FP); Postcondizioni | Pagina corrente dopo la singola pressione di "Indietro" = `scegli-metodo` | not-applicable | F-001, F-007 | supported |

Nessun riferimento temporale (massimo/minimo/esatto) e' presente nello UC o nel documento funzionale per questa verifica: `timing semantics` e' `not-applicable` perche' l'AC non definisce un vincolo di tempo, non perche' sia un'omissione da risolvere.

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |
| D-001 | SC-002, SC-003, SC-004, SC-005, SC-006 | Codice avviso di pagamento inserito in `inserisci-dati-avviso` | 18 caratteri numerici (S-002, "Struttura e Validazione del campo Codice Avviso"); deve corrispondere a un avviso valido recuperabile dal sistema per proseguire oltre `inserisci-dati-avviso` | Avviso di pagamento esistente e valido nell'ambiente di riferimento | F-003, F-004, F-005, F-006, F-007 |
| D-002 | SC-002, SC-003, SC-004, SC-005, SC-006 | Codice Fiscale Ente Creditore inserito in `inserisci-dati-avviso` | 11 caratteri numerici (S-002, "Struttura e Validazione del campo CF ente Creditore (EC)"); deve essere coerente con D-001 | EC esistente e coerente con l'avviso D-001 | F-003, F-004, F-005, F-006, F-007 |
| D-003 | SC-004, SC-005, SC-006 | Indirizzo email inserito in `inserisci-email` | Formato nome@dominio.tld secondo le regole descritte (S-002, "Pagina di inserimento Email"). Non e' un requisito di SC-003: accedere a `inserisci-email` precede l'inserimento dell'email stessa, nessuna email e' gia' richiesta per raggiungere quella pagina | Nessuno stato di entita' aggiuntivo oltre alla sintassi valida | F-005, F-006, F-007 |
| D-004 | SC-004, SC-005, SC-006 | Conferma indirizzo email (campo "Ripeti di nuovo") | Deve coincidere esattamente con D-003, altrimenti il campo viene evidenziato in rosso e il tasto continua non produce azione (S-002). Non e' un requisito di SC-003 per lo stesso motivo di D-003 | Uguale a D-003 | F-005, F-006, F-007 |
| D-005 | SC-005 | Numero carta inserito in `inserisci-carta` | Valore valido e coerente richiesto dal campo "numero carta" (S-002, "Flusso Carta di Credito"); il pulsante continua si attiva solo con tutti i campi carta validi e coerenti | Nessuno stato aggiuntivo documentato oltre alla validita' del valore | F-006 |
| D-006 | SC-005 | Scadenza carta inserita in `inserisci-carta` | Valore valido e coerente con D-005 (S-002) | Coerente con D-005 | F-006 |
| D-007 | SC-005 | CVV carta inserito in `inserisci-carta` | Valore valido richiesto dal campo "CVV" (S-002) | Coerente con D-005 | F-006 |
| D-008 | SC-005 | Intestatario carta ("Intestata a") inserito in `inserisci-carta` | Valore valido richiesto dal campo (S-002); nessun vincolo di formato ulteriore documentato | Nessuno stato aggiuntivo documentato | F-006 |

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | SC-002, SC-003, SC-004, SC-005, SC-006 | Uso dei valori sintetici di "Note per gli sviluppatori.md" per D-001/D-002 | Riportata in 00-run.md: dati sintetici NON autorizzati per questo UC; D-001/D-002 restano TODO. Ambito: questa run | answered |

## Readiness

Stato: `incomplete`. Sono supportati e pronti per la progettazione scenario i
sei casi SC-001..SC-006, ciascuno con evidenza funzionale (F-00X), oracle
(O-001) e requisiti dati (D-NNN) tracciati. Copertura parzialmente mancante,
riportata senza invenzione di comportamento:

- `scegli-metodo` (F-008): nessun pulsante "Indietro" generico e' documentato
  per questa pagina; nessuno scenario puo' coprirla con evidenza supportata.
- `riepilogo-pagamento` (F-009): sono documentati solo "modifica" (verso
  `inserisci-carta` o `scegli-metodo`/`lista-psp` a seconda del ramo) e
  "Annulla" con popup dedicato; nessun pulsante "Indietro" generico e'
  descritto, quindi non e' un caso di questo UC sulla sola base del
  documento ammesso.
- Ramo Google Pay (e flussi dichiarati identici: Conto iConto, Intesa
  Sanpaolo, Fabrik Pay By Bank, Klarna) (F-010): raggiunge direttamente
  `riepilogo-pagamento` senza passare da `lista-psp`; non e' documentato
  alcun pulsante "Indietro" generico da questa pagina, quindi nessuno
  scenario di back navigation e' supportabile per questo ramo.
- Flusso popup "Annulla" (Esci / "No, ho cambiato idea"): non e' un
  pulsante "Indietro" ne' un flusso alternativo/eccezione dello UC
  corrente; resta fuori ambito di questa run.
- Distinzione pulsante UI "Indietro" vs comando nativo "indietro" del
  browser (F-011): lo UC non la pone. Solo i pulsanti UI documentati hanno
  evidenza supportata; l'assenza di copertura per il comando browser e'
  un limite di copertura esplicito, non un'approvazione di ambito.
- Le sezioni "Flussi alternativi (AF)" ed "Eccezioni (EF)" dello UC sono
  vuote: nessuna AF/EF e' stata inventata per compensare l'assenza.

Nessun conflitto bloccante e' stato rilevato tra UC e documento funzionale per
i sei casi supportati.

Rettifica di questa revisione (rev 2): corretti i metadati `uc_revision`
("1", non "revisione1") e `environment` ("uat", non "UAT") secondo conferma
umana; rimosso SC-003 dallo scope di D-003/D-004 perche' in contraddizione
con il flusso documentato (accedere a `inserisci-email` precede l'inserimento
dell'email, non lo richiede come precondizione); esplicitato in Mapping che
SC-006 usa PayPal come campione rappresentante nominato, con Apple Pay,
BANCOMAT Pay e MyBank dichiarati equivalenti dalla fonte ma non campionati
singolarmente. Nessuna evidenza funzionale nuova e' stata introdotta da
questa rettifica.
