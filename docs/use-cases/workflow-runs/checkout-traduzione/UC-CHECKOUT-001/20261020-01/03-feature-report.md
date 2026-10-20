---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
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
  - path: docs/use-cases/workflow-runs/checkout-traduzione/UC-CHECKOUT-001/20261020-01/02-test-data.md
    revision: 1
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |
| docs/use-cases/features/checkout/FEAT_001_Checkout_Attivazione_Pagamento.feature | uc-to-feature | written |
| docs/use-cases/features/checkout/FEAT_002_Checkout_Errori_Avviso.feature | uc-to-feature | written |

Per leggibilita, nelle tabelle seguenti F1 indica il primo percorso completo
della tabella Feature outputs, F2 il secondo. T1-T5 indicano i titoli esatti:

- T1: Avvio del pagamento con carta di credito e scelta del PSP
- T2: Avvio del pagamento con metodo alternativo e scelta del PSP
- T3: Avvio del pagamento con accesso diretto al riepilogo dopo la scelta del metodo
- T4: Visualizzazione del messaggio per avviso sconosciuto, scaduto o timeout
- T5: Visualizzazione del messaggio per avviso già pagato senza descrizione aggiuntiva

Sono 5 definizioni Gherkin, di cui 3 outline, per 14 casi: 10 positivi e
4 negativi. SC-015 non e scritto nelle feature, neppure come scenario saltato.
La creazione dei due file ha creato la directory di destinazione; nessuna
esplorazione o lettura della directory o dei suoi file e stata effettuata.

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |
| SC-001-SC-014 | Precondizioni | Contesto: homepage UAT aperta; lingua it | 01-context.md F-001 | Solo stati iniziali. Azioni di inserimento, navigazione e pagamento restano When/And. Ogni caso e indipendente |
| SC-001-SC-010 | FP 1 | Sceglie inserimento manuale; inserisce codice avviso e CF; preme Continua; preme Vai al pagamento nel riepilogo | 01-context.md F-002, F-003 | Split giustificato dalle pagine e CTA prescritte in S-002. I due campi sono un'unica compilazione funzionale |
| SC-001-SC-010 | FP 2 | Inserisce la stessa email nei due campi; preme Continua nella pagina email | 01-context.md F-003 | Inserimento coeso con vincolo di uguaglianza; invio separato per esplicitare la sequenza obbligatoria |
| SC-001 | FP 3-4 | Sceglie carta; compila i 4 dettagli con data table; preme Continua nella pagina carta | 01-context.md F-004 | La scelta del metodo determina il ramo; i dettagli non producono rami distinti nel caso positivo, nessuna frammentazione per singolo campo |
| SC-001 | FP 5 | Seleziona tramite radio button il PSP con nome Postepay; preme Continua nella lista PSP | 01-context.md F-004 | Nome commerciale documentato distinto dall'ID tecnico. Una sola carta/PSP candidata, senza moltiplicare casi per dimensione del catalogo |
| SC-002, SC-004, SC-005, SC-010 | AF-01, AF-03, AF-04, AF-09 | T2: sceglie metodo; seleziona PSP per identificativo; preme Continua nella lista PSP | 01-context.md F-005 | La fonte dichiara identici i quattro percorsi; un outline delle sole alternative con PSP, mai righe del flusso carta. Nessuno script nascosto nelle celle; la stessa sequenza e applicata a tutte |
| SC-003, SC-006-SC-009 | AF-02, AF-05-AF-08 | T3: sceglie metodo; preme Paga nel riepilogo | 01-context.md F-006, F-013 | Fonte dichiara identici i cinque percorsi senza selezione PSP iniziale. Outline separato da T2 per non nascondere azioni opzionali. GPay reso Google Pay; altre grafie funzionali conservate |
| SC-001-SC-010 | FP 6 e conclusione AF | Preme Paga relativo al totale visualizzato; Then reindirizzamento fuori da uat.checkout.pagopa.it | 01-context.md F-007; Q-003 | Riduzione esplicita del perimetro richiesta dall'umano. Non si equipara il redirect al successo; nessuna azione successiva eseguita dal test. Il totale e il riferimento documentato, non un importo inventato |
| SC-011-SC-013 | EF-01 al passo 1 | T4: sceglie manuale; inserisce avviso negativo e CF; Continua; Then messaggio entro limite dal clic; And titolo; And descrizione | 01-context.md F-002, F-009, F-010 | Medesimo percorso e medesime 3 verifiche per sconosciuto, scaduto e timeout; solo valori diversi, dunque un outline. Nessuna prosecuzione ai passi successivi del FP |
| SC-014 | EF-01 al passo 1 | T5: percorso fino a Continua; Then entro 5 secondi; And titolo; And assenza di descrizione | 01-context.md F-009, F-010 | Verifica diversa: assenza, non confronto con la parola Vuoto o una cella mancante. Scenario separato per non introdurre verifiche condizionali nell'outline |
| SC-015 | Variante EF-01 irraggiungibile | Nessuno step | 01-context.md F-011; Q-006 | Caso escluso dal test su istruzione umana; oracle mancanti non mascherati da placeholder |

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |
| UC-CHECKOUT-001; JTBD-001 | SC-001-SC-014 | F1, F2 | T1-T5 | Tutte | partial: capacita tracciata, fine pagamento fuori perimetro; JTBD solo riferimento, nessuna narrativa inventata |
| Attore principale Utente; attori secondari assenti | SC-001-SC-014 | F1, F2 | T1-T5 | Tutte | covered |
| Precondizione Checkout aperto | SC-001-SC-014 | F1, F2 | T1-T5 | Tutte | covered |
| Precondizione lingua italiana | SC-001-SC-014 | F1, F2 | T1-T5 | Tutte | covered |
| FP 1 | SC-001-SC-010 | F1 | T1-T3 | Tutte le righe positive e T1 not-applicable | covered |
| FP 2 | SC-001-SC-010 | F1 | T1-T3 | Tutte le righe positive e T1 not-applicable | covered |
| FP 3 | SC-001 | F1 | T1 | not-applicable | covered |
| FP 4 | SC-001 | F1 | T1 | not-applicable | covered |
| FP 5 | SC-001 | F1 | T1 | not-applicable | covered |
| FP 6 | SC-001 | F1 | T1 | not-applicable | partial: avvio e redirect, non conclusione esterna del pagamento |
| AF-01 | SC-002 | F1 | T2 | metodo=PayPal | partial: percorso interno coperto, conclusione esterna non testata |
| AF-02 | SC-003 | F1 | T3 | metodo=Google Pay | partial: percorso interno coperto, conclusione esterna non testata |
| AF-03 | SC-004 | F1 | T2 | metodo=Apple Pay | partial: percorso interno esplicito con PSP TODO, conclusione esterna non testata |
| AF-04 | SC-005 | F1 | T2 | metodo=BANCOMAT Pay | partial: percorso interno esplicito con PSP TODO, conclusione esterna non testata |
| AF-05 | SC-006 | F1 | T3 | metodo=Conto iCONTO | partial: percorso interno coperto, conclusione esterna non testata |
| AF-06 | SC-007 | F1 | T3 | metodo=Conto Intesa Sanpaolo | partial: percorso interno coperto, conclusione esterna non testata |
| AF-07 | SC-008 | F1 | T3 | metodo=Fabrick Pay By Bank | partial: percorso interno coperto, conclusione esterna non testata |
| AF-08 | SC-009 | F1 | T3 | metodo=Klarna | partial: percorso interno coperto, conclusione esterna non testata |
| AF-09 | SC-010 | F1 | T2 | metodo=MyBank | partial: percorso interno esplicito con PSP TODO, conclusione esterna non testata |
| EF-01 | SC-011-SC-014 | F2 | T4, T5 | avviso=302400000000000000, 302990000000000000, 302980000000000000; T5 not-applicable | partial: quattro varianti con tutti i controlli, irraggiungibile esclusa |
| EF-01 variante irraggiungibile | SC-015 | Nessun file | Nessuno scenario | not-applicable | uncovered: esclusa dall'umano, corpo e tempo non definiti |
| Postcondizione pagamento completato | SC-001-SC-010 | F1 | T1-T3 | Tutte le righe positive e T1 not-applicable | uncovered: il redirect non dimostra il completamento, nessuna interfaccia di osservazione entro il confine concordato |
| AC-01 (FP) | SC-001 | F1 | T1 | not-applicable | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-02 (AF-01) | SC-002 | F1 | T2 | metodo=PayPal | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-03 (AF-02) | SC-003 | F1 | T3 | metodo=Google Pay | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-04 (AF-03) | SC-004 | F1 | T2 | metodo=Apple Pay | partial: percorso in bozza con PSP TODO; messaggio di successo non verificato |
| AC-05 (AF-04) | SC-005 | F1 | T2 | metodo=BANCOMAT Pay | partial: percorso in bozza con PSP TODO; messaggio di successo non verificato |
| AC-06 (AF-05) | SC-006 | F1 | T3 | metodo=Conto iCONTO | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-07 (AF-06) | SC-007 | F1 | T3 | metodo=Conto Intesa Sanpaolo | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-08 (AF-07) | SC-008 | F1 | T3 | metodo=Fabrick Pay By Bank | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-09 (AF-08) | SC-009 | F1 | T3 | metodo=Klarna | partial: percorso fino al redirect; messaggio di successo non verificato |
| AC-10 (AF-09) | SC-010 | F1 | T2 | metodo=MyBank | partial: percorso in bozza con PSP TODO; messaggio di successo non verificato |
| AC-11 (EF-01) | SC-011 | F2 | T4 | avviso=302400000000000000 | covered |
| AC-12 (EF-01) | SC-011 | F2 | T4 | avviso=302400000000000000 | covered |
| AC-13 (EF-01) | SC-011 | F2 | T4 | avviso=302400000000000000 | covered |
| AC-11 (EF-01) | SC-012 | F2 | T4 | avviso=302990000000000000 | covered |
| AC-12 (EF-01) | SC-012 | F2 | T4 | avviso=302990000000000000 | covered |
| AC-13 (EF-01) | SC-012 | F2 | T4 | avviso=302990000000000000 | covered |
| AC-11 (EF-01) | SC-013 | F2 | T4 | avviso=302980000000000000 | covered |
| AC-12 (EF-01) | SC-013 | F2 | T4 | avviso=302980000000000000 | covered |
| AC-13 (EF-01) | SC-013 | F2 | T4 | avviso=302980000000000000 | covered |
| AC-11 (EF-01) | SC-014 | F2 | T5 | not-applicable | covered |
| AC-12 (EF-01) | SC-014 | F2 | T5 | not-applicable | covered |
| AC-13 (EF-01) | SC-014 | F2 | T5 | not-applicable | covered |
| AC-11 (EF-01, variante esclusa) | SC-015 | Nessun file | Nessuno scenario | not-applicable | uncovered: richiesta umana di esclusione dell'intero caso |
| AC-12 (EF-01, variante esclusa) | SC-015 | Nessun file | Nessuno scenario | not-applicable | uncovered: corpo esatto assente |
| AC-13 (EF-01, variante esclusa) | SC-015 | Nessun file | Nessuno scenario | not-applicable | uncovered: tempo massimo assente |

covered indica copertura nel disegno Gherkin, non esecuzione riuscita.
Per AC-01-AC-10 partial indica il solo percorso preparatorio: nessuna
asserzione soddisfa il messaggio di successo richiesto dall'AC originale.
Proposta al proprietario dello UC: separare l'accettazione dell'avvio fino al
redirect dalla conferma del completamento. Lo UC sorgente non e modificato.
Non sono emerse sezioni mancanti, identificativi duplicati o AC con target
inesistente; i riferimenti FP/AF/EF originali sono risolti nelle righe sopra.
Il titolo Attivazione pagamento e il flusso di completamento hanno ampiezze
diverse: il perimetro operativo e quello ristretto dal chiarimento umano.
Le validazioni di formato, gli annulli, i ritorni e gli ordinamenti descritti
nei documenti non diventano scenari aggiuntivi non richiesti dallo UC.

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |
| SC-001 | C-001 | D-001-D-006, D-008 | O-001 | Avviso 302042025112600001, CF 77777777777, email mail@pagopa.it, Mastercard 5255000260000014, 12/30, 123, Test test, Postepay; non verificati avviso/carta/PSP/metodo |
| SC-002 | C-002 | D-001, D-002, D-003, D-005, D-006, D-008 | O-001 | Valori comuni di C-002; PayPal, PSP identificato da BCITITMM, non nome UI; disponibilita non verificata |
| SC-003 | C-003 | D-001, D-002, D-003, D-006, D-008 | O-001 | Valori comuni di C-003; Google Pay; nessun PSP iniziale; disponibilita non verificata |
| SC-004 | C-004 | D-001, D-002, D-003, D-005, D-006, D-008 | O-001 | Apple Pay; __TODO_D005__ da reperire per questo caso, non valore condiviso con altri metodi |
| SC-005 | C-005 | D-001, D-002, D-003, D-005, D-006, D-008 | O-001 | BANCOMAT Pay; __TODO_D005__ da reperire per questo caso |
| SC-006 | C-006 | D-001, D-002, D-003, D-006, D-008 | O-001 | Conto iCONTO; nessun PSP iniziale; disponibilita non verificata |
| SC-007 | C-007 | D-001, D-002, D-003, D-006, D-008 | O-001 | Conto Intesa Sanpaolo; nessun PSP iniziale; disponibilita non verificata |
| SC-008 | C-008 | D-001, D-002, D-003, D-006, D-008 | O-001 | Fabrick Pay By Bank; nessun PSP iniziale; disponibilita non verificata |
| SC-009 | C-009 | D-001, D-002, D-003, D-006, D-008 | O-001 | Klarna; nessun PSP iniziale; disponibilita non verificata |
| SC-010 | C-010 | D-001, D-002, D-003, D-005, D-006, D-008 | O-001 | MyBank; __TODO_D005__ da reperire per questo caso |
| SC-011 | C-011 | D-002, D-007, D-008 | O-003, O-004, O-005 | Avviso 302400000000000000; titolo e corpo esatti del contesto; massimo 5 secondi da Continua |
| SC-012 | C-012 | D-002, D-007, D-008 | O-006, O-007, O-008 | Avviso 302990000000000000; titolo e corpo esatti del contesto; massimo 60 secondi da Continua |
| SC-013 | C-013 | D-002, D-007, D-008 | O-009, O-010, O-011 | Avviso 302980000000000000; titolo e corpo esatti del contesto; massimo 60 secondi da Continua |
| SC-014 | C-014 | D-002, D-007, D-008 | O-012, O-013, O-014 | Avviso 302950100443009424; titolo esatto del contesto, assenza di descrizione; massimo 5 secondi da Continua |
| SC-015 | not-applicable | Nessuno applicato | O-015 non applicato | Nessuno: caso escluso, nessun placeholder per oracle mancanti |

Le provenienze, caratteristiche, ammissioni, fitness e disponibilita per ogni
D/SC/C sono in 02-test-data.md, revision 1, Data resolution e Combinations.
Le fonti restano provided; Q-007 autorizza l'uso non verificato, non trasforma
i candidati in fit. Disponibilita documented-not-checked per i valori forniti;
unknown-to-prepare per i tre PSP mancanti. D-001 richiede stato non pagato da
predisporre indipendentemente; D-004/D-005/D-006 richiedono compatibilita e
abilitazione da verificare. Nessuna casella email consultata.
Per i valori attesi, O-003-O-014 provengono da 01-context.md#S-004,
Messaggi associati agli errori e Avvisi per prove di errore, con decisioni
01-context.md#S-005. O-001 proviene da 01-context.md#S-002, descrizione del
pulsante Paga xxxx nei tre flussi. O-002 e O-015 non sono applicati.
O-005/O-008/O-011/O-014 hanno semantica maximum, con origine al clic
confermata dall'umano; non sono tempi esatti o pause fisse.
Nessun catalogo opzionale salvato o modificato.

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |
| Q-003 | SC-001-SC-010 | Perimetro risolto: niente azioni dopo il redirect. Restano scoperti il messaggio di successo e lo stato completato degli AC/postcondizione originali | answered |
| Q-004 | SC-011-SC-014 | Attese indicative del catalogo interpretate come massimi su istruzione umana, solo per questa prova | answered |
| Q-005 | SC-011-SC-014 | Misura dal clic Continua confermata | answered |
| Q-006 | SC-011-SC-015 | Autorizzati i quattro casi con oracle documentati; escluso irraggiungibile | answered |
| Q-007 | SC-001-SC-014 | Dati non verificati autorizzati con warning, senza generazione | answered |
| Q-008 | SC-004, SC-005, SC-010 | D-005: PSP Apple Pay, BANCOMAT Pay e MyBank ancora da reperire | open |

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |
| Persistenza report a monte | Lettura dei file registrati con view dopo le scritture; confronto frontmatter, tabelle e registro | Coerenti: stesso UC/task/run/UAT/v1, produttori corretti, context=1 e test-data=1, stato incomplete consumabile per bozza | 01-context.md e 02-test-data.md effettivamente letti; registro revision 3 consumato |
| Persistenza feature | Esito apply_patch della creazione dei due percorsi | 2 file aggiunti; nessuna lettura successiva, come richiesto dall'umano | Risposta tool Added 2 file(s); questa tabella non rivendica parsing dei file |
| Copertura e cardinalita | Confronto statico manuale del contenuto composto con inventario e oracles | 10 casi positivi, 4 negativi, 1 escluso; tutti gli AF/EF/AC rendicontati; 1 sola attivazione o verifica avviso per caso | Coverage; Mapping; C-001-C-014 |
| Confine delle operazioni | Controllo statico manuale del contenuto inviato in scrittura | Nessuna azione dopo il redirect; nessun successo fittizio; EF termina al messaggio | T1-T5, O-001, O-003-O-014 |
| Semantica Given/When/Then | Controllo statico manuale prima della scrittura | Background solo homepage e lingua; Given solo disponibilita/configurazione; navigazione e input restano azioni; Then solo osservazioni | Mapping; nessun setup equivalente inventato per saltare la storia |
| Outline e tabelle | Controllo statico manuale del contenuto composto | T2: 2 parametri/2 colonne, 4 righe; T3: 1/1, 5 righe; T4: 4/4, 3 righe. Nessuna colonna costante, cella vuota o script opzionale | T2 metodo/psp; T3 metodo; T4 avviso/tempo_massimo/titolo/descrizione |
| Commenti di bozza | Controllo statico manuale prima delle tag | Tutte le 5 definizioni hanno warning; righe Apple Pay, BANCOMAT Pay, MyBank identificate per D-005; stati del Background inclusi nei warning | Scenario warnings del report dati applicati |
| Profilo | Confronto statico manuale con .github/profiles/gherkin.profile.yaml e gherkin.instructions.md | Nomi FEAT, italiano, commento #0123456789 prima della lingua, tag di suite/segno/regressione e identificativi per file/scenario, rientri conformi; 3 e 2 definizioni, entrambi <=12 | Payload di creazione; nessuna convenzione ricavata da feature esistenti |
| Dati e oracle | Riconciliazione manuale D/SC/C/O con i due report | Tutti i valori forniti hanno provenienza; candidati non verificati ammessi in Q-007; 3 TODO esclusivamente dati, nessun oracle inventato | Data and oracles; Q-007; Q-008 |
| Divieto anti-bias | Verifica delle operazioni svolte | Nessuna esplorazione/lettura di src o docs/use-cases/features, neppure delle nuove feature; solo scrittura nella destinazione autorizzata | Fonti e chiamate view limitate ad allegati, convenzioni, ACE, workflow, run e directory test-data |
| Parser, build, test e controlli live | Non eseguiti; ruolo QA-analyst non autorizzato a eseguirli | Non verificati: sintassi da parser, step implementati, abilitazioni, disponibilita e tempi effettivi | Nessun comando terminale o chiamata al sistema sotto test |

## Engineer handoff
Tutte le formulazioni sono nuove, derivate dallo UC e dalla documentazione:
non sono stati letti step o feature esistenti. Non si puo quindi affermare
che i testi siano gia implementati o indicare decorator da aggiornare.
Nessun Python scritto. Queste bozze non autorizzano implementazione o
esecuzione automatica prima della risoluzione dei prerequisiti.

- T1 / SC-001: ripetere il percorso manuale completo, confermare l'avviso,
  compilare entrambe le email, scegliere carta, inserire insieme i 4 dati,
  selezionare Postepay e avviare una sola volta il pagamento. La carta e
  quella sintetica gia documentata; data table a riga singola, non Examples.
  L'osservazione finale e il redirect esterno, non una ricevuta di pagamento.
- T2 / SC-002, SC-004, SC-005, SC-010: stesso percorso iniziale, poi metodo
  alternativo e PSP, senza carta. BCITITMM e un identificativo candidato
  per PayPal, non il nome visibile del PSP. Risolvere separatamente D-005
  per Apple Pay, BANCOMAT Pay e MyBank: tre token uguali non significano
  un PSP condiviso. Non saltare la selezione nelle righe TODO.
- T3 / SC-003, SC-006-SC-009: percorso iniziale identico, poi scelta del
  metodo e riepilogo diretto, senza compilazione carta o selezione PSP.
  Google Pay corrisponde a GPay nello UC; non e autorizzata l'invenzione
  di interazioni wallet esterne. iCONTO e Fabrick restano nomi funzionali,
  non selettori o etichette letterali imposti dalla bozza.
- T4 / SC-011-SC-013: preparare ogni errore tramite la configurazione mock
  gia prevista, non tramite una precedente esecuzione dello scenario.
  Registrare il riferimento temporale al clic Continua, osservare la
  comparsa entro il massimo inclusivo di 5/60/60 secondi, quindi controllare
  esattamente titolo e corpo della stessa risposta. Non aggiungere verifiche
  dei codici tecnici: sono provenance dei dati, non AC richiesti.
- T5 / SC-014: stessa singola verifica dell'avviso, massimo 5 secondi,
  titolo esatto e assenza di descrizione aggiuntiva. Non confrontare con
  la parola Vuoto e non introdurre un pagamento per generare il duplicato.

Ogni scenario deve stabilire indipendentemente avviso, metodo e
configurazione necessari. Il codice positivo e ripetuto come candidato
documentato, non come garanzia di riutilizzabilita o invito a eseguire i
casi in sequenza. Nessuna pulizia, configurazione di flag o transazione
preparatoria e stata eseguita. La verifica del redirect deve osservare
un'uscita reale dal dominio, non una mera differenza di stringa che
accetti URL relativi, sottodomini ingannevoli o redirect ancora interni.
I limiti temporali valgono per la comparsa del messaggio, non impongono che
il test consumi l'intero intervallo; nessuna ulteriore azione di business
deve essere nascosta nei Then.

## Readiness
bozza, status incomplete. I due report a monte sono revision 1/incomplete;
questa traduzione e revision 1/incomplete; il registro diventa draft.

Rimangono: PSP D-005 da reperire per Apple Pay, BANCOMAT Pay e MyBank,
stati e compatibilita non verificati in ambiente, successo e postcondizione
completamento non coperti per il confine richiesto. SC-015 e escluso come
richiesto. Non sono stati inventati valori funzionali o input sintetici.
I controlli sono statici manuali sul contenuto composto e sui report letti;
non attestano parsing o test eseguiti. Nessuna lezione ACE attiva da citare.

Friction effettiva: lo strumento domande dedicato non e disponibile e i
chiarimenti sono stati raccolti in chat; il divieto di lettura degli output
esclude una verifica filesystem post-scrittura delle feature. L'esito delle
scritture e disponibile nei tool; eventuale validazione sintattica esterna
richiede un'attivita successiva autorizzata. Nessuna traccia ACE scritta.
