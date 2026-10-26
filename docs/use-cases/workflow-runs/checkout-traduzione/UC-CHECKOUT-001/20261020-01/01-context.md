---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: checkout-traduzione
uc_id: UC-CHECKOUT-001
run_id: 20261020-01
uc_input: 'C:\Users\dquero\Downloads\UC-CHECKOUT-001 - Attivazione pagamento Checkout.txt'
uc_revision: v1
environment: uat
revision: 1
status: incomplete
updated_at: "2026-10-20T16:41:36.150+02:00"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | C:/Users/dquero/Downloads/UC-CHECKOUT-001 - Attivazione pagamento Checkout.txt | UC completo, 53 righe | 2026-10-20 | uat, revisione v1 confermata | provided | Richiesta iniziale; conferma run del 2026-10-20T16:06:16.298+02:00 |
| S-002 | C:/Users/dquero/Downloads/Checkout PagoPA - Interfaccia Utente e Comportamento Funzionale.md | Home Page; Inserimento Dati Avviso; Pagina Riepilogo Dati Pagamento; Pagina di inserimento Email; tre famiglie di flussi | 2026-10-20 | uat, versione applicativa unknown | provided | Allegato iniziale |
| S-003 | C:/Users/dquero/Downloads/Note per gli sviluppatori.md | Codici Avviso; CF Ente Creditore | 2026-10-20 | Ambiente test, versione unknown | provided | Allegato iniziale |
| S-004 | docs/use-cases/test-data/checkout/checkout-test-data.md | Scopo; Avvisi per prove di errore; Messaggi associati agli errori; dati e percorsi | 2026-10-20 | dev e uat; configurazione e corrispondenza alla versione da verificare | provided | Allegato del 2026-10-20T16:06:16.298+02:00; valori candidati autorizzati il 2026-10-20T16:41:36.150+02:00 |
| S-005 | Chat della presente sessione, risposte del 2026-10-20T16:06:16.298+02:00 e 2026-10-20T16:41:36.150+02:00 | Punti 1-3 delle risposte ai chiarimenti | 2026-10-20 | uat, scope di questa prova | provided | Non testare azioni esterne; tempi massimi dal clic Continua; escludere irraggiungibile; usare dati documentati non verificati con warning, senza generare altri dati |

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | SC-001-SC-014 | Precondizioni | Da dove parte il percorso? | Checkout aperto in italiano; homepage UAT https://uat.checkout.pagopa.it/; ogni caso riparte autonomamente dalla homepage | S-001 Precondizioni; S-002 Home Page | supported |
| F-002 | SC-001-SC-014 | FP 1; EF-01 | Come si invia un avviso? | Scegliere inserimento manuale, compilare codice avviso di 18 cifre e CF EC di 11 cifre, premere Continua; per dati validi segue il riepilogo dell'avviso | S-002 Inserimento Dati Avviso; S-003 CF EC | supported |
| F-003 | SC-001-SC-010 | FP 1-2 | Come si prosegue ai metodi? | Dal riepilogo premere Vai al pagamento; inserire lo stesso indirizzo valido in Indirizzo email e Ripeti di nuovo; premere Continua | S-002 Pagina Riepilogo Dati Pagamento; Pagina di inserimento Email | supported |
| F-004 | SC-001 | FP 3-5 | Quale percorso distingue la carta? | Scegliere carta; compilare numero, scadenza, CVV e Intestata a; Continua; scegliere PSP con radio button; Continua | S-001 FP 3-5; S-002 Flusso Carta di Credito | supported |
| F-005 | SC-002, SC-004, SC-005, SC-010 | AF-01, AF-03, AF-04, AF-09 | Quali alternative richiedono PSP? | PayPal, Apple Pay, BANCOMAT Pay e MyBank saltano i dettagli carta e raggiungono lista PSP; selezione radio button e Continua portano al riepilogo | S-001 AF indicati; S-002 Flusso PayPal e coincidenze dichiarate | supported |
| F-006 | SC-003, SC-006-SC-009 | AF-02, AF-05-AF-08 | Quali alternative saltano la lista PSP iniziale? | Google Pay, Conto iCONTO, Conto Intesa Sanpaolo, Fabrick Pay By Bank e Klarna portano direttamente al riepilogo | S-001 AF indicati; S-002 Flusso Google Pay e coincidenze dichiarate | supported |
| F-007 | SC-001-SC-010 | FP 6; conclusione AF | Quale azione e quale esito sono nel perimetro? | Premere il pulsante Paga con il totale visualizzato; il browser esce dal dominio Checkout. Fermare il test al reindirizzamento, senza interazioni con siti esterni | S-002 pulsante Paga xxxx nei tre flussi; S-005 punto 3 prima risposta | supported |
| F-008 | SC-001-SC-010 | AC-01-AC-10; postcondizione | Il redirect dimostra pagamento completato? | No: non e documentato ne verificato il messaggio di successo entro il confine concordato. Conservare gli AC come parziali e la postcondizione come non coperta; nessuna asserzione di successo inventata | S-001 AC e postcondizione; S-005 esclusione delle azioni esterne | unresolved |
| F-009 | SC-011-SC-014 | EF-01; AC-11-AC-13 | Quali varianti negative sono documentate? | Sconosciuto, scaduto, timeout e duplicato hanno avvisi documentati, titolo, corpo o sua assenza e tempi numerici. Sono varianti dello stesso EF, non nuove AF | S-004 Avvisi per prove di errore; Messaggi associati agli errori; S-005 conferma punto 2 ultima risposta | supported |
| F-010 | SC-011-SC-014 | AC-13 | Come interpretare e misurare il tempo? | Massimo inclusivo di 5 o 60 secondi dalla pressione di Continua dopo compilazione avviso e CF; verificare comparsa del messaggio entro il limite, senza sleep fisso e senza considerarlo SLA di produzione | S-004 tempi indicativi; S-005 massimi e origine temporale confermati ai punti 1-2 ultima risposta | supported |
| F-011 | SC-015 | EF-01; AC-11-AC-13 | Includere ente irraggiungibile? | Escluso dal test su istruzione umana: mancano tempo massimo e corpo esatto, il testo Codice di errore per l'assistenza non definisce il codice concreto | S-004 riga ente irraggiungibile; S-005 punto 2 ultima risposta | unresolved |
| F-012 | SC-001-SC-014 | Dati e prerequisiti | Quali dati possono essere usati? | Ammessi i dati gia documentati, anche sintetici, come non verificati con warning. Nessuna generazione aggiuntiva; ammissione non prova disponibilita di avvisi, metodi, carte o PSP | S-004 Scopo e condizioni; S-005 punto 3 ultima risposta | supported |
| F-013 | SC-001-SC-010 | FP 3; AF-02; AF-05; AF-07 | Come gestire i nomi? | GPay e Google Pay indicano il medesimo percorso citato; iCONTO/iConto e Fabrick/Fabrik sono grafie nelle fonti per i flussi esplicitamente associati. Si mantiene il nome UC, salvo Google Pay per esteso; non si pretende corrispondenza letterale di etichette UI | S-001 nomi dei metodi; S-002 intestazioni e liste delle coincidenze | supported |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |
| SC-001-SC-014 | Precondizioni | Background con homepage UAT aperta e lingua italiana | F-001 | Solo stato iniziale; nessun percorso operativo trasferito in Given |
| SC-001-SC-010 | FP 1 | When sceglie inserimento manuale; And compila avviso e CF; And preme Continua; And preme Vai al pagamento nel riepilogo | F-002, F-003 | La sequenza pagina input, invio e prosecuzione da riepilogo e prescritta dalla documentazione; i due campi dell'avviso restano un inserimento coeso |
| SC-001-SC-010 | FP 2 | And compila i due campi email con lo stesso valore; And preme Continua nella pagina email | F-003 | I due indirizzi devono coincidere; il click e il trigger separato per accedere ai metodi, non una verifica nascosta |
| SC-001 | FP 3-4 | And sceglie carta; And compila i 4 dettagli in una data table; And preme Continua nella pagina carta | F-004 | La scelta cambia percorso; i 4 campi non hanno rami indipendenti nel caso di pagamento e restano coesi |
| SC-001, SC-002, SC-004, SC-005, SC-010 | FP 5 e AF con PSP | And seleziona il PSP con radio button; And preme Continua nella lista PSP | F-004, F-005 | Selezione necessaria per abilitare la prosecuzione; nessuna chiamata tecnica o codice PSP confuso col nome |
| SC-003, SC-006-SC-009 | AF senza PSP iniziale | And sceglie il metodo; And preme Paga nel riepilogo | F-006, F-007 | Nessuna selezione PSP o compilazione carta inventata |
| SC-001-SC-010 | FP 6 e AF | And preme il pulsante Paga relativo al totale; Then browser fuori dal dominio del Checkout | F-007, F-008 | Una sola attivazione per caso; il percorso completo in When mantiene la storia rilevante. Nessun successo implicito |
| SC-011-SC-014 | EF-01 al passo 1 | When inserimento manuale; And avviso negativo e CF; And Continua; Then messaggio entro limite; And titolo; And corpo o assenza di descrizione | F-002, F-009, F-010 | Termina all'errore senza email o metodi. I 3 AC compatibili sono verifiche dello stesso esito; duplicato separato per il controllo di assenza del corpo |
| SC-015 | EF-01 variante documentale | Nessuno step generato | F-011 | Esclusione richiesta, senza sostituire oracle mancanti con TODO dati |

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |
| O-001 | SC-001-SC-010 | FP 6 e AF; S-002 pulsante Paga xxxx | Reindirizzamento al di fuori del dominio uat.checkout.pagopa.it, senza ulteriori azioni del test | not-applicable | F-007 | supported |
| O-002 | SC-001-SC-010 | AC-01-AC-10; postcondizione | Messaggio di successo e pagamento completato: non verificabili con il perimetro adottato; non applicati nelle feature | not-applicable | F-008 | unresolved |
| O-003 | SC-011 | AC-11 (EF-01) | Titolo: Non riusciamo a trovare l’avviso | not-applicable | F-009 | supported |
| O-004 | SC-011 | AC-12 (EF-01) | Corpo: L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore. | not-applicable | F-009 | supported |
| O-005 | SC-011 | AC-13 (EF-01) | Comparsa entro 5 secondi dal clic Continua | maximum | F-010 | supported |
| O-006 | SC-012 | AC-11 (EF-01) | Titolo: L’avviso è scaduto e non è più possibile pagarlo | not-applicable | F-009 | supported |
| O-007 | SC-012 | AC-12 (EF-01) | Corpo: Contatta l’Ente per maggiori informazioni. | not-applicable | F-009 | supported |
| O-008 | SC-012 | AC-13 (EF-01) | Comparsa entro 60 secondi dal clic Continua | maximum | F-010 | supported |
| O-009 | SC-013 | AC-11 (EF-01) | Titolo: Si è verificato un errore imprevisto | not-applicable | F-009 | supported |
| O-010 | SC-013 | AC-12 (EF-01) | Corpo: Riprova, oppure contatta l’assistenza | not-applicable | F-009 | supported |
| O-011 | SC-013 | AC-13 (EF-01) | Comparsa entro 60 secondi dal clic Continua | maximum | F-010 | supported |
| O-012 | SC-014 | AC-11 (EF-01) | Titolo: Questo avviso è stato già pagato! | not-applicable | F-009 | supported |
| O-013 | SC-014 | AC-12 (EF-01) | Assenza di testo descrittivo aggiuntivo, non stringa letterale Vuoto | not-applicable | F-009 | supported |
| O-014 | SC-014 | AC-13 (EF-01) | Comparsa entro 5 secondi dal clic Continua | maximum | F-010 | supported |
| O-015 | SC-015 | AC-11-AC-13 (EF-01) | Variante irraggiungibile esclusa: tempo e corpo esatto mancanti; titolo documentato ma non testato isolatamente | unknown | F-011 | unresolved |

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |
| D-001 | SC-001-SC-010 | Codice avviso valido | Stringa di 18 cifre, associata al CF D-002; nessuna generazione autonoma | Disponibile, non gia pagato, utilizzabile per il percorso scelto; preparazione indipendente per ciascun caso | F-002, F-012 |
| D-002 | SC-001-SC-014 | CF ente creditore di test | Stringa di 11 cifre; non CF personale; abbinato agli avvisi | Ente di test configurato in UAT | F-002, F-009, F-012 |
| D-003 | SC-001-SC-010 | Email e conferma | Un valore valido copiato nei due campi; non si testa ricezione email | Utilizzo autorizzato per compilazione; nessun accesso alla casella richiesto | F-003, F-012 |
| D-004 | SC-001 | Carta di test, oggetto con PAN, scadenza, CVV e intestatario | Tutti e 4 i campi, PAN senza spazi, scadenza futura, carta coerente con PSP D-005 | Accettata dal gateway in UAT; non carta reale | F-004, F-012 |
| D-005 | SC-001, SC-002, SC-004, SC-005, SC-010 | PSP selezionabile per il metodo corrente | Nome o identificativo documentato, radio button corrispondente; non confondere nome e ID; compatibilita con D-004 per carta | PSP abilitato nella lista per il metodo e l'avviso | F-004, F-005, F-012 |
| D-006 | SC-001-SC-010 | Disponibilita del metodo di pagamento | Metodo indicato nello SC; nomi funzionali, non codici tecnici inventati | Metodo abilitato e selezionabile in UAT | F-004, F-005, F-006, F-012, F-013 |
| D-007 | SC-011-SC-014 | Avviso negativo per il tipo di errore | 18 cifre; SC-011 sconosciuto, SC-012 scaduto, SC-013 timeout, SC-014 duplicato; CF D-002 | Mock configurato per l'errore corrispondente; non richiede un pagamento precedente eseguito dal test | F-009, F-012 |
| D-008 | SC-001-SC-014 | Lingua della sessione | Italiano, valore it; determina gli oracle testuali | Configurazione italiana prima del flusso | F-001, F-009 |

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-003 | SC-001-SC-010 | Successo richiesto dagli AC ma azioni esterne fuori perimetro | Escluse le azioni dopo l'uscita; copertura positiva solo fino al redirect, senza assumere successo; risposta 2026-10-20T16:06:16.298+02:00 | answered |
| Q-004 | SC-011-SC-014 | Fonte indica attese indicative, non limiti | L'umano richiede massimi per questa prova; non e modifica dello SLA del prodotto | answered |
| Q-005 | SC-011-SC-014 | Origine della misura temporale | Dal clic Continua dopo compilazione avviso e CF, punto 1 risposta 2026-10-20T16:41:36.150+02:00 | answered |
| Q-006 | SC-011-SC-015 | Testi candidati e variante priva di oracle completi | Confermata proposta dei 4 errori documentati; variante irraggiungibile non inclusa nel test, punto 2 stessa risposta | answered |
| Q-007 | SC-001-SC-014 | Idoneita e disponibilita dei dati | Dati documentati autorizzati come non verificati con warning, nessuna generazione; punto 3 stessa risposta. Non e conferma live | answered |

## Readiness
incomplete: i percorsi fino al redirect e i quattro errori hanno evidenza ammessa.
Gli AC-01-AC-10 restano parziali e la postcondizione pagamento completato non
coperta per il confine richiesto. SC-015 e escluso dal test per decisione umana.
Il contesto definisce i nuovi SC-012-SC-015 come varianti documentali di EF-01,
senza modificare lo UC. Gli oracle dei quattro errori sono valori attesi della
bozza autorizzati, non osservazioni dell'applicazione. I dettagli carta restano
un inserimento coeso; nessuna variante aggiunta solo per enumerare un catalogo.
Nessun test, parser o verifica dell'ambiente eseguito. Nessuna fonte da src
o dalla cartella features letta o esplorata. Nessuna lezione ACE attiva.
