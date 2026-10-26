---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
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
  - path: docs/use-cases/workflow-runs/unknown/UC-CHECKOUT-003/20261020-01/02-test-data.md
    revision: 1
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |
| docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | uc-to-feature | written |

Una feature, 6 scenari semplici e 1 outline con 4 righe: 7 definizioni, 10 casi indipendenti. La cartella di destinazione viene creata dalla scrittura del nuovo file, senza elencare o leggere la cartella o altre feature.

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |
| SC-001..SC-010 | Precondizioni | Contesto: Home del Checkout UAT aperta; lingua italiana | 01-context.md F-001, F-002 | Stato iniziale comune, preparabile indipendentemente; nessuna azione del flusso nascosta nel Contesto. L'apertura della Home non elimina la storia rilevante, che comincia e resta esplicita con l'accesso all'inserimento avviso |
| SC-001 | FP 1 | Quando sceglie inserimento manuale; Allora visualizza inserimento avviso | F-001, F-002 | L'osservazione intermedia verifica la pagina di partenza del singolo ritorno, requisito FP 1; non aggiunge una validazione di campo o un obiettivo autonomo |
| SC-002 | FP 1 | Scelta inserimento manuale; compilazione congiunta codice avviso e CF; Continua; osservazione riepilogo | F-002, F-003 | Scomposizione giustificata dalla sequenza funzionale del documento: accesso, dati, avanzamento; non un passo per ciascun campo. Il valore da conservare viene creato nel medesimo scenario |
| SC-003 | FP 1 | Stessa sequenza fino al riepilogo; Vai al pagamento; osservazione inserimento email | F-002, F-003, F-005 | Percorso storico rilevante esplicito; nessuna compilazione email superflua o preparazione via URL della pagina finale |
| SC-010 | FP 1 | Percorso avviso e riepilogo; Vai al pagamento; compilazione email e conferma insieme; Continua; osservazione scelta metodo | F-002, F-003, F-005, F-006, F-011 | Compilazione coesa dei 2 campi correlati; avanzamento separato per preservare l'ordine. Il ritorno verso email proviene dal chiarimento ammesso, non da deduzione |
| SC-004 | FP 1 | Percorso fino a scelta metodo; selezione Carta di Credito; osservazione inserimento carta | F-002, F-003, F-005, F-006, F-007 | Caso distinto dal ritorno verso carta: si verifica un'altra singola transizione. Non compilare dati carta inutili al ritorno verso scelta metodo |
| SC-005 | FP 1 | Percorso fino a carta; inserimento coeso di numero, scadenza, CVV e intestatario tramite tabella; Continua; osservazione lista PSP | F-002, F-003, F-005, F-006, F-007 | La tabella e l'argomento di un'azione di compilazione, non un elenco di script. Continua e l'avanzamento prima del ritorno; nessun PSP selezionato |
| SC-006..SC-009 | FP 1 | Percorso fino a scelta metodo; selezione di <metodo>; osservazione lista PSP | F-002, F-003, F-005, F-006, F-009 | Un solo outline: stessi passi e stessi controlli per i 4 metodi esplicitamente equiparati dalla fonte. Il parametro e solo il metodo, non un percorso operativo |
| SC-001..SC-010 | FP 2 | Quando preme 1 sola volta Indietro del Checkout | F-001, F-002, F-004, F-005, F-007, F-008, F-009, F-011 | Esattamente 1 ritorno per caso, mai browser back, catena di ritorni o loop. L'osservazione della pagina di partenza precede questa azione |
| SC-001, SC-004, SC-006..SC-009 | Postcondizioni; AC-01 | Allora destinazione Home o scelta metodo | F-002, F-007, F-009, F-010; O-001, O-004, O-007 | Sola destinazione secondo Q-006: non inventare dati o stato selezionato dove non sono previsti input |
| SC-002 | Postcondizioni; AC-01 | Allora inserimento avviso; codice e CF ancora visibili con i medesimi valori | F-004; O-002 | 2 verifiche compatibili dell'esito della stessa operazione; nessun nuovo ritorno |
| SC-003 | Postcondizioni; AC-01 | Allora riepilogo; codice e CF ancora visibili | F-005; O-003 | Verificare gli input esposti dal riepilogo; nessun importo, nome o oggetto atteso inventato |
| SC-010 | Postcondizioni; AC-01 | Allora inserimento email; entrambi i campi ancora visibili e uguali al valore precedente | F-011; O-006 | Uguaglianza rispetto agli input dello stesso scenario; non confrontare solo i 2 campi tra loro |
| SC-005 | Postcondizioni; AC-01 | Allora inserimento carta; numero, scadenza, CVV e intestatario ancora visibili e uguali agli input | F-008; O-005 | 4 controlli della stessa operazione; conservazione CVV richiesta dall'utente, non omessa o sostituita da un generico controllo pagina |

F/O citati senza prefisso nella tabella sono definiti in `01-context.md`. Ogni accesso sotto test termina con una verifica intermedia della pagina raggiunta, supportata da FP 1 e dal percorso documentato; poi un nuovo Quando introduce l'unico ritorno. Non vengono aggiunti controlli intermedi di formato, abilitazione pulsante o successo del pagamento.

JTBD-001 resta tracciabilita e non viene trasformato in una narrativa inventata. Nessun UC/AC tag o commento aggiuntivo e stato introdotto senza formato concordato: la matrice sottostante conserva il collegamento. Il commento tracking #1234567890 e esclusivamente mock. Il titolo inglese dello UC e reso funzionalmente in italiano, senza modificarne il contenuto.

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |
| UC-CHECKOUT-003; JTBD-001 | SC-001..SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Tutti gli scenari della feature | not-applicable | covered; tracciabilita al caso d'uso e al riferimento JTBD, non obiettivo aggiuntivo |
| Precondizioni: Checkout aperto e lingua italiana | SC-001..SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Tutti gli scenari della feature | not-applicable | covered; Contesto condiviso, privo di azioni del flusso |
| FP 1: accesso a una pagina | SC-001..SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Tutti gli scenari della feature | not-applicable | covered; percorso esplicito e osservazione della pagina di partenza prima del ritorno |
| FP 2: tornare indietro 1 sola volta | SC-001..SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Tutti gli scenari della feature | not-applicable | covered; una pressione applicativa per ogni caso |
| Postcondizione: pagina precedente | SC-001..SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Tutti gli scenari della feature | not-applicable | covered; Then di destinazione in tutti i casi |
| Postcondizione: dati inseriti ancora visibili | SC-002, SC-003, SC-005, SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Scenari con confronto dati avviso, riepilogo, carta ed email | not-applicable | covered; confronto esplicito con gli input dello stesso scenario; per le altre destinazioni controllo non applicabile secondo Q-006 |
| AC-01 (FP) | SC-001 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dall'inserimento dati avviso alla Home | not-applicable | covered; sola destinazione secondo Q-006 |
| AC-01 (FP) | SC-002 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dal riepilogo ai dati avviso conservando i valori inseriti | not-applicable | covered; destinazione e conservazione codice avviso/CF |
| AC-01 (FP) | SC-003 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dall'inserimento email al riepilogo con i dati avviso ancora visibili | not-applicable | covered; destinazione e visibilita degli input nel riepilogo |
| AC-01 (FP) | SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dalla scelta metodo ai dati email conservando entrambi i campi | not-applicable | covered; destinazione confermata Q-005 e conservazione dei 2 campi |
| AC-01 (FP) | SC-004 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dall'inserimento carta alla scelta metodo di pagamento | not-applicable | covered; sola destinazione secondo Q-006 |
| AC-01 (FP) | SC-005 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dalla lista PSP ai dati carta conservando tutti i campi | not-applicable | covered; destinazione e tutti i 4 campi, CVV incluso |
| AC-01 (FP) | SC-006 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dalla lista PSP alla scelta del metodo di pagamento | metodo=PayPal | covered; sola destinazione secondo Q-006 |
| AC-01 (FP) | SC-007 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dalla lista PSP alla scelta del metodo di pagamento | metodo=Apple Pay | covered; sola destinazione secondo Q-006 |
| AC-01 (FP) | SC-008 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dalla lista PSP alla scelta del metodo di pagamento | metodo=BANCOMAT Pay | covered; sola destinazione secondo Q-006 |
| AC-01 (FP) | SC-009 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Ritorno dalla lista PSP alla scelta del metodo di pagamento | metodo=MyBank | covered; sola destinazione secondo Q-006 |
| AF; EF | SC-001..SC-010 | docs/use-cases/features/checkout/FEAT_004_Checkout_Back_Navigation_Control.feature | Tutti gli scenari della feature | not-applicable | covered; sezioni esplicitamente prive di casi secondo Q-004, nessun negativo inventato |

Coverage indica copertura del requisito nel testo Gherkin, non test superati. Nessun controllo dati su Home/scelta metodo viene presentato come eseguito o coperto: e escluso dall'applicabilita tramite conferma umana Q-006. Le pagine di riepilogo finale documentano Annulla e Modifica, non un ulteriore Indietro: quei controlli e le sequenze anti-loop non sono aggiunti al perimetro.

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |
| SC-001 | C-001 | Nessuno | O-001, O-007 | Origine /inserisci-dati-avviso; destinazione /; dati non applicabili |
| SC-002 | C-002 | D-001, D-002 | O-002 | Avviso 302042025112600001; CF 77777777777; destinazione /inserisci-dati-avviso; Q-008 |
| SC-003 | C-003 | D-001, D-002 | O-003 | Stessa coppia; destinazione /dati-pagamento e confronto degli input; Q-008 |
| SC-004 | C-004 | D-001, D-002, D-003 | O-004, O-007 | Stessa coppia; email mail@pagopa.it nei 2 campi; metodo Carta di Credito; destinazione /scegli-metodo; Q-008 |
| SC-005 | C-005 | D-001..D-007 | O-005 | Stessa coppia ed email; PAN 5255000260000014, scadenza 12/30, CVV 123, intestatario Test test; destinazione /inserisci-carta; Q-008 |
| SC-006 | C-006 | D-001, D-002, D-003 | O-004, O-007 | Stessa coppia ed email; PayPal; destinazione /scegli-metodo; Q-008 |
| SC-007 | C-007 | D-001, D-002, D-003 | O-004, O-007 | Stessa coppia ed email; Apple Pay; destinazione /scegli-metodo; Q-008 |
| SC-008 | C-008 | D-001, D-002, D-003 | O-004, O-007 | Stessa coppia ed email; BANCOMAT Pay; destinazione /scegli-metodo; Q-008 |
| SC-009 | C-009 | D-001, D-002, D-003 | O-004, O-007 | Stessa coppia ed email; MyBank; destinazione /scegli-metodo; Q-008 |
| SC-010 | C-010 | D-001, D-002, D-003 | O-006 | Stessa coppia ed email; destinazione /inserisci-email; entrambi i campi uguali all'email inserita; Q-008 |

D/O sono definiti in `01-context.md`; C e risoluzioni per ciascun D/SC in `02-test-data.md`.

Input: D-001..D-007 hanno valori documentati e ammessi, nessun TODO. Il CF e provided da `02-test-data.md#S-001`; avviso, email e carta provengono da `02-test-data.md#S-002`, approved con Q-007. La riga Mastercard documenta insieme i 4 campi e il carattere sintetico dell'intestatario: non sono stati generati o mescolati dati di carte diverse. Formati e scadenza controllati staticamente; fitness ancora unverified per D-001, D-004, D-006, D-007 e combinazioni dipendenti. Availability evidence e documented-not-checked, mai user-confirmed per stati correnti. Restano da predisporre/verificare avviso valido/non pagato, accettazione carta e disponibilita dei metodi/lista PSP. Nessun valore aggiuntivo da reperire e nessun catalogo Markdown salvato o modificato: Optional catalogue not-requested.

Oracle: le destinazioni O-001..O-005 e i pulsanti provengono da `01-context.md#S-002`; O-006 da `01-context.md#S-005` con conferma `01-context.md#S-006`. Le uguaglianze con gli input sono prescritte da AC-01/postcondizioni e conferma `01-context.md#S-003`; O-007 e l'eccezione di applicabilita confermata in `01-context.md#S-006`. Nessun testo di errore, importo o tempo viene ricavato dai dati o dall'ambiente osservato.

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |
| Q-001 | SC-001..SC-010 | Identita e percorsi confermati; task ignorato e rappresentato da unknown, senza associazione Jira | answered |
| Q-002 | SC-001..SC-010 | Commento tracking mock #1234567890 confermato | answered |
| Q-003 | SC-001..SC-010 | Indietro applicativo, 1 ritorno e conservazione campi, CVV incluso, confermati | answered |
| Q-004 | SC-001..SC-010 | Nessun AF/EF previsto, confermato | answered |
| Q-005 | SC-010 | Ritorno scelta metodo verso email e conservazione entrambi i campi, confermati | answered |
| Q-006 | SC-001, SC-004, SC-006..SC-009 | Sola destinazione per Home/scelta metodo, confermata | answered |
| Q-007 | SC-002..SC-010 | Candidati approvati come non verificati con warning | answered |
| Q-008 | SC-002..SC-010 | Da predisporre/verificare stati e disponibilita correnti di avviso, carta, metodi e lista PSP | open |

Nessuna lacuna funzionale bloccante resta nel perimetro concordato. L'espressione "pagina iniziale" dell'AC viene letta insieme a FP 1 e ai chiarimenti sulle singole pagine, non come richiesta di tornare indietro dalla Home. Il contrasto apparente tra coppia PSP generica del catalogo e percorso carta e delimitato dall'ammissione: per la carta si applica la destinazione specifica del documento funzionale, non quella generica.

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |
| Identita e provenienza handoff | Lettura effettiva del registro e dei 2 report ai percorsi registrati; confronto frontmatter, Artifacts, History, fonti e decisioni | Conforme: contesto revision 2 ready; dati revision 1 incomplete, consumabili per una bozza; UC/run/task/ambiente concordanti | 00-run.md revision 4 prima dell'assemblaggio; inputs del report dati e di questo report |
| Struttura semantica | Revisione manuale del contenuto composto: prerequisiti, azioni, osservazioni prima/dopo ritorno e origine di ogni confronto | Conforme: nessuna azione del viaggio nascosta nel Contesto; nessuna azione business nei Then; And mantiene il ruolo del blocco precedente | Mapping; sequenza Quando/Allora/Quando/Allora in ogni definizione |
| Cardinalita e autonomia | Conteggio manuale delle azioni Indietro nel contenuto da scrivere; verifica dei percorsi indipendenti | 1 pressione per ciascuna delle 7 definizioni, quindi 1 per ciascuno dei 10 casi; nessuna dipendenza da altri scenari | 6 scenari semplici e outline di 4 righe |
| Conformita al profilo | Controllo statico manuale di lingua, nome file, indentazione, commento, tag e tabelle | Conforme: 004; italiano; 2/4/6 spazi; 7 definizioni e 10 casi, entrambi entro il massimo 12; tracking mock; un solo parametro variabile metodo con 4 valori distinti | .github/profiles/gherkin.profile.yaml e .github/instructions/gherkin.instructions.md |
| Completezza campi e confronti | Confronto manuale con F/O/D/C, valori ammessi e specifiche dei 4 campi carta/2 email | Conforme: PAN, scadenza, CVV, intestatario, codice avviso, CF e 2 email espliciti nei casi applicabili; nessun confronto basato su un token irrisolto | Data and oracles; 01-context.md; 02-test-data.md |
| Warning | Confronto manuale con Scenario warnings del report dati | Presenti prima dei tag di ogni definizione interessata, incluse tutte le 4 righe dell'outline; nessuna disponibilita corrente dichiarata verificata | Q-007 e Q-008; 02-test-data.md |
| Copertura e tracciabilita | Riconciliazione manuale SC-001..SC-010 e unico AC-01 con righe outline, postcondizioni e chiarimenti | Completa nel perimetro concordato; nessun AF/EF o variante negativa inventato | Coverage; Q-004..Q-006 |
| Limiti di lettura | Uso esclusivo di allegati, istruzioni/profilo, report correnti e catalogo Markdown ammesso; nessuna lettura della cartella feature | Rispettati; nessuna esplorazione di src o docs/use-cases/features | Fonti registrate; scrittura del solo nuovo file feature concordato |
| Sintassi automatica, build e test | Non eseguiti: il ruolo analista non esegue parser o test | Non verificati automaticamente; controllo soltanto manuale, nessuna dichiarazione di test superati | Nessun comando terminale eseguito |
| ACE | Letti persona, istruzioni ACE scoped e configurazione famiglie | Nessuna lezione attiva da applicare/citare; nessuna famiglia assegnata; nessuna traccia scritta dall'analista | .github/instructions/ace-qa-analyst.instructions.md; ace/config/project.json |

## Engineer handoff

Questa e una traduzione nuova, senza lettura di step o feature esistenti. Non viene dichiarata compatibilita con decorator gia implementati; nessun testo preesistente e stato modificato. I nuovi testi dovranno essere considerati esplicitamente nell'eventuale fase di implementazione, dopo la risoluzione della bozza, non riadattati a step scoperti in suite.

- **SC-001, tag finale 01:** dalla Home apre l'inserimento manuale, verifica di trovarsi nella pagina avviso, preme Indietro 1 volta e verifica la Home. Nessun input o controllo di conservazione per la destinazione priva di campi.
- **SC-002, tag finale 02:** inserisce la coppia avviso/ente, avanza al riepilogo e torna 1 volta alla compilazione. Entrambi i campi devono mostrare esattamente gli input del caso, senza reinserirli nei Then.
- **SC-003, tag finale 03:** raggiunge l'email passando dal riepilogo dell'avviso, poi torna 1 volta. Il riepilogo deve esporre codice avviso e CF gia inseriti. Non verifica dati email, non ancora compilati, o valori derivati non richiesti.
- **SC-010, tag finale 04:** compila email e conferma con lo stesso indirizzo, avanza alla scelta metodo e torna 1 volta. Verifica i 2 campi separatamente rispetto al valore originario, non semplicemente la loro uguaglianza reciproca.
- **SC-004, tag finale 05:** sceglie Carta di Credito e torna dall'inserimento carta alla scelta metodo. Non compila dati carta e non pretende una selezione persistente non richiesta.
- **SC-005, tag finale 06:** compila tutti i dati della carta della stessa riga approvata, raggiunge la lista PSP e torna 1 volta alla carta. Non seleziona un PSP, non paga. Verifica visibilita e conservazione di numero, scadenza, CVV e intestatario. Non omettere o correggere il CVV per aspettative di implementazione diverse: eventuali discrepanze richiedono un chiarimento del requisito.
- **SC-006..SC-009, tag finale 07:** una riga indipendente per PayPal, Apple Pay, BANCOMAT Pay e MyBank. Stesso percorso avviso/email, selezione del metodo, lista PSP, 1 ritorno alla scelta metodo. Nessun ramo o passo opzionale nascosto nel parametro; nessun PSP scelto.

Ogni caso parte da una Home preparata indipendentemente; i dati e la storia di navigazione da conservare nascono nei suoi When. Le osservazioni intermedie verificano il punto di partenza del ritorno, non causano ulteriori avanzamenti. Il pulsante Continua e qualificato dalla pagina per evitare ambiguita di azione, non prescrive selettori tecnici. L'ambiente, i metodi, lo stato dell'avviso e l'accettazione della carta restano prerequisiti da predisporre/verificare separatamente. Non consultare caselle email, completare pagamenti o introdurre accessi autenticati per questo UC.

Friction rilevata per l'orchestratore: dettagli mancanti risolti con 2 gruppi di conferme umane; tool domande e lettura web non disponibili, chiarimenti ottenuti in chat; nessun accesso terminale o tentativo di aggiramento. Conferme registrate nelle Q pertinenti. Nessuna lezione ACE attiva, nessuna traccia o playbook scritto.

## Readiness

**bozza**. Feature/report revision 1 prodotti da uc-to-feature; contesto revision 2 ready di uc-scenario-context; dati revision 1 incomplete di uc-test-data. Nessun valore mancante e nessuna lacuna funzionale aperta nel perimetro confermato; resta Q-008: disponibilita e idoneita correnti non accertate. L'approvazione Q-007 permette l'inclusione dei candidati, non li trasforma in dati verificati.

La matrice copre AC-01, FP, precondizioni e postcondizioni nel perimetro concordato, senza rivendicare esecuzione. Il controllo statico manuale non equivale a validazione automatica della sintassi, implementazione degli step o test applicativi superati. Non e pronta per lo sviluppo/esecuzione automatici finche i prerequisiti irrisolti restano tali. Il numero di tracking e mock e nessun task Jira e associato.
