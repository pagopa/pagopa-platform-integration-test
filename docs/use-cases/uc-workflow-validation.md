# Verifica del contratto UC

Questa matrice verifica [uc-workflow/v1](uc-workflow.md), non specifica
comportamenti di prodotto. Gli identificativi sono astratti: nessun UC,
dato reale, feature della suite o esempio UC-to-feature approvato viene
introdotto. Le tre skill restano responsabili degli output del contratto.

## Livelli di verifica

1. **Asset statici**: metadata, link, colonne e sezioni dei template, permessi,
   invalidazione, enum e presenza delle regole operative concordate.
2. **Sintassi isolata**: il parser Behave legge frammenti artificiali in memoria
   con TODO, outline parziali, Background e piu verifiche nello stesso scenario.
   Non esegue step, transazioni o test della suite; non dimostra idoneita dei dati.
3. **Comportamento dell'agente**: una prova richiede un UC umano, fonti ammesse,
   percorsi/input e run confermati. Confrontare gli artefatti effettivi con la
   matrice, registrando risultati, metodo, revisioni ed evidenza. Non dedurre
   il comportamento dell'agente dalla presenza di una frase nella skill.

I test di sviluppo, esterni al QA-analyst, sono in
[test_uc_workflow_contract.py](../../tests/unit/qa_workflow/test_uc_workflow_contract.py).
Usano il runner dei test unitari e il parser Behave gia adottati dal progetto:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\unit\qa_workflow\test_uc_workflow_contract.py -q
```

Eseguire dalla root con pytest e le dipendenze del progetto disponibili nel
virtualenv di sviluppo. I tool di sviluppo mancanti non sono capacita
operative aggiuntive dell'analista.

L'analista non esegue questo comando: i suoi permessi terminale non cambiano.
Nessun verificatore o matcher runtime viene installato nel workflow.
Gli assert sulle clausole e sulle tabelle sono regressioni del contratto
documentale, non un motore sostitutivo che simula l'agente.

## Matrice di accettazione

| Caso | Preparazione astratta | Risultato atteso | Evidenza da controllare nella prova agente |
| --- | --- | --- | --- |
| V-01 | Il contesto scopre un caso supportato dello stesso flusso | Registra un nuovo SC, collega F/O/D e AC, senza creare AF o rinumerare id | Scenario inventory, contesto e History |
| V-02 | I dati scoprono un caso non registrato | Propongono il caso con Q; ritorno al contesto prima delle nuove C; in manuale nessuna chiamata automatica | Questions, report dati e successiva revisione del contesto |
| V-03 | Una decisione modifica il report di un'altra skill | Aggiorna Q e invalida i dipendenti, senza riscrivere report o revisioni altrui | Questions, Artifacts e History |
| V-04 | D-001 ha valori diversi in due SC/C | Un solo requisito D; risoluzioni distinte con provenienza e fitness per ogni valore | Data requirements, Data resolution e Combinations |
| V-05 | Due valori nello stesso caso devono essere diversi per ruolo o vincolo | Il contesto definisce D distinti e la relazione; i dati non fondono i requisiti | Contesto e relazione della C |
| V-06 | D-001 resta irrisolto in due casi | Stesso token __TODO_D001__; nessuna uguaglianza concreta dedotta; entrambi i casi restano bozza | Valori e warning per ogni SC/C |
| V-07 | Due AC compatibili riferiti a FP | Stesso scenario con tutte le verifiche Then/And e voci Coverage distinte | Oracles, feature e Coverage |
| V-08 | Due AC compatibili riferiti ad AF02 | Stesso scenario alternativo con entrambe le verifiche; nessuna estensione automatica a FP | Oracles e Coverage per AF02 |
| V-09 | Due AC compatibili riferiti ad EF01 | Stesso caso negativo con entrambe le verifiche; nessuna estensione ad altre EF | Oracles e Coverage per EF01 |
| V-10 | Due casi richiedono insiemi di verifiche diversi | Scenari/outline separati; non uno scenario per singolo AC compatibile | Mapping e Coverage |
| V-11 | Alias equivalenti per un flusso presente, con case/spazi/punti diversi | Risoluzione allo stesso id originale; tutti gli AC conservati | Oracles e riferimenti della Coverage |
| V-12 | Riferimento inesistente, ambiguo, assente o usato come esclusione | Q quando necessario; nessun FP di default, nessun flusso inventato, esclusione non positiva | Questions e copertura affected |
| V-13 | Una risposta intermedia necessaria e documentata non ha un AC dedicato | Verifica intermedia con riferimento funzionale reale, senza inventare AC | Mapping, evidenza e Oracles |
| V-14 | Un controllo interno o click implementativo non richiede un esito osservabile | Nessun Then o scomposizione aggiunto per comodita | Mapping e motivazione della granularita |
| V-15 | Ripresa con revisioni uguali, contenuti confermati invariati e struttura valida | Q/History della conferma con scopo esatto; riuso senza retrieval superfluo | Inventario presentato, risposta umana e inputs |
| V-16 | Modifica manuale dichiarata con revisioni numeriche invariate | Artefatto e dipendenti stale; report rivalidato dal proprietario; nessuna adozione cieca dei metadati | Artifacts, provenienza e nuova revisione |
| V-17 | Continuita non confermata oppure file mancante/illeggibile | Ripresa blocked con Q; nessun riuso presunto; una conferma non supera l'errore di lettura | Questions, errore e status della run |
| V-18 | Solo History o conferma amministrativa cambiano | Nessuna invalidazione dei report/feature; revisione del registro non entra negli inputs | Artifacts e inputs immutati |
| V-19 | Cambia il contesto di una run prima complete | Dati, finale e tutte le feature dipendenti stale; run in_progress, non complete | Artifacts e status prima della rielaborazione |
| V-20 | Cambiano solo dati o una feature manuale | Dati cambiati invalidano finale/feature; feature manuale invalida se stessa/finale, non il contesto | Propagazione circoscritta e nessuna sovrascrittura non confermata |
| V-21 | Report precedente con enum non canonici | Rivalidazione del produttore, non conversione silenziosa nel consumatore | Report corretto e History |
| V-22 | assemble-only con prerequisiti mancanti, stale, blocked o continuita non confermata | Stop con passaggio necessario; nessuna skill di retrieval eseguita | Questions, report finale quando persistibile e assenza di feature inventate |
| V-23 | TODO in alcune righe outline o nel Background | Warning prima dei tag per ogni scenario interessato; righe interessate identificate; nessun vuoto usato per il dato mancante | Feature, Scenario warnings e Data and oracles |
| V-24 | Nessun dato richiesto, oppure nessuno scenario funzionalmente supportato | Nel primo caso report dati obbligatorio senza righe fittizie; nel secondo finale blocked senza feature vuota | Report effettivi, Coverage e Feature outputs |
| V-25 | Conferma di continuita su report con disponibilita dati non stabilita | Nessuna nuova ammissione o availability dedotta; warning nei report e bozza conservati, senza commenti nella feature in assenza di TODO | Admission, Availability evidence e Readiness |
| V-26 | Salvataggio di feature/report riuscito ma registro fallito | Errore esplicito, stop e riconciliazione del proprietario; nessuna run complete presunta | File effettivi, errore e History riconciliata |
| V-27 | Dato concreto ammesso come non verificato, senza placeholder | Nessun commento sui dati nella feature; incertezza e bozza nei report, Required comment=not-applicable | Feature, Data resolution, Scenario warnings e Readiness |
| V-28 | Risolto l'ultimo placeholder di uno scenario, resta disponibilita non verificata | Rimosso il commento relativo al TODO; conservati warning nei report e stato bozza, tracking e dichiarazione lingua intatti | Feature e Readiness |
| V-29 | Una fonte usa un hostname UAT solo come esempio di deployment | Step ed Examples indipendenti dall'ambiente; configurazione Python/Behave dalla run; controllo di uscita dal dominio invariato | Mapping, metadati e feature |
| V-30 | Un requisito verifica esplicitamente un dominio o URL letterale | Valore letterale conservato con motivazione funzionale, non rimosso come configurazione | Evidenza, Mapping e oracle |
| V-31 | Idoneita di un dato nota solo attraverso l'operazione sotto test | Nessun Given che la garantisce e nessuna operazione anticipata; vincolo nei requisiti dati, esito osservabile solo se documentato | Contesto, Mapping e Data resolution |
| V-32 | Stato iniziale stabilibile mediante preparazione indipendente supportata | Given ammesso con evidenza del meccanismo, senza dipendenza da altri scenari; non serve un'asserzione separata per ogni Given | Functional evidence e Mapping |
| V-33 | UC contiene una precondizione ma non e documentato come prepararla | Requisito conservato aperto, nessun setup inventato; lacuna di preparazione distinta da regola funzionale mancante | Questions, Mapping e Readiness |
| V-34 | README documenta configurazioni diverse per tipi di suite | Consultazione selettiva delle sezioni applicabili; vincoli operativi nel report, nessuna estensione automatica di default o capacita ad altre suite | Mapping e Checks con sezioni consultate e ambito |
| V-35 | README contiene comandi o link verso percorsi esclusi | Nessun comando eseguito e nessun percorso escluso letto; documentazione insufficiente segnalata se incide sul disegno, senza esplorazione indiscriminata | Operazioni effettive, Mapping e Questions |
| V-36 | README contiene un possibile dato di test o esito funzionale | Trovato distinto dal contesto operativo e soggetto alla policy fonti; nessuna disponibilita o capacita di setup dedotta dal framework | Sources, decisioni di ammissione e Mapping |
| V-37 | UC con finalità limitata e documentazione molto più ampia | Focus persistito; UC obbligatorio contabilizzato; nessun test di operazioni estranee | Agreed inputs, Mapping e Coverage |
| V-38 | Nota umana ambigua o incompatibile con una regola fornita | Distinzione scoping/requisito/decisione; Q circoscritta o riuso di decisione già esplicita; nessuna precedenza automatica | Sources, Questions, History e dipendenti invalidati se cambia la decisione |
| V-39 | Fonte ammessa descrive un percorso ulteriore dell'operazione UC con trigger ed esito completi | Nuovo SC del contesto con anchor e ragione, non AF inventata né riga dati; un percorso estraneo non viene aggiunto | Scenario inventory, Functional evidence e Coverage |
| V-40 | Evento asincrono in ingresso e risposta; eventuali ACK/completamento sono distinti dalla fonte | Keyword dal ruolo causale; ogni AC resta verificato e non si aggiungono ACK o completamento non prescritti | Mapping, Oracles e feature |
| V-41 | AC prescrive soltanto invio del messaggio; un altro richiede una verifica prima di avanzare | Entrambi verificati con Then/And nel rispettivo scope; il primo non viene sostituito da ricezione/completamento, il secondo non viene omesso come semplice trigger | Oracles, osservazioni intermedie e Coverage separata |
| V-42 | Postcondizione UC e AC simile esplicitamente riferito a un EF | Postcondizione verificata in tutti i positivi FP/AF; AC verificato nell'EF indicato, senza restringere l'obbligo dei positivi né estenderlo ad altri EF | Oracles e Coverage per tutti i percorsi pertinenti |
| V-43 | Proprietà esclusa dal focus senza prova che sia funzionalmente ininfluente | Nessuna invarianza inventata e nessuna enumerazione arbitraria; eventuale conflitto materiale reso esplicito | Agreed inputs, evidenza e Mapping |
| V-44 | Esempio con letterale o enum incompatibili con la regola; formula temporale con configurazione esemplificativa | Esempio non elevato a norma/fixture; formula e fase preservate; conflitto rilevante non risolto scegliendo un valore | Sources, Oracles, Data resolution e Questions |
| V-45 | Campo necessario solo a un'API di implementazione e input realmente richiesto ma mancante | Primo resta nel report/handoff senza parametro artificiale; secondo segue TODO; oracle e tracking non diventano D | Data requirements, Data resolution, handoff e warning |
| V-46 | Feedback cambia il requisito, oppure soltanto dati o wording | Rielaborazione attraverso gli owner pertinenti e invalidazione circoscritta; nessun retrieval delle parti invariate | Questions, History, Artifacts e nuove revisioni reali |

## Regressioni analista e orchestratore (ADR-02 - ADR-07)

Lo stesso test di contratto verifica anche routing, permessi, gate e identita
nei documenti dell'analista e dell'orchestratore. Come per V-01 - V-36, i casi
seguenti sono risultati attesi, non prove di un'esecuzione reale dell'agente.

| Caso | Richiesta o stato | Risultato atteso |
| --- | --- | --- |
| A-01 | Feature allegata senza azione chiara | Chiede review/modifica/creazione, senza dedurre permesso di modifica dall'allegato |
| A-02 | QA-analyst invoca review-feature-files direttamente | Applica la skill senza autodelega; nessuna feature creata o modificata |
| A-03 | Review con report Markdown richiesto | Conferma il percorso se manca, salva solo il report e restituisce elementi ACE senza scrivere trace |
| A-04 | Review solo in chat | Nessun report o feature scritto; nessuna delega a engineer/runner/closer |
| A-05 | Correzione esplicita di file nominati | Nessuna seconda autorizzazione generica; preserva lo scope e spiega impatto sui binding |
| A-06 | Correzione di feature registrata UC | Riconcilia tramite il proprietario; se incompleta, invalidazione circoscritta e nessun vecchio ready mantenuto |
| A-07 | Creazione da documentazione non UC | Stesse garanzie sulle fonti, oracle e dati; nessun UC o registro UC inventato |
| A-08 | Suite di migrazione fornita come input non UC | Evidenza dell'implementazione corrente, non requisito implicito; nessuna eccezione per traduzione UC |
| A-09 | Analista restituisce bozza o solo changes-complete | Nessuna implementazione automatica; orchestratore verifica readiness per file e confini della richiesta |
| A-10 | Solo un sottoinsieme delle feature e pronto | Implementazione parziale soltanto con autorizzazione esplicita dell'umano |
| A-11 | Nuova richiesta ACE riprende una run UC | Nuovo ACE task_id ma identita e percorsi UC invariati; nessuna migrazione dello schema |
| A-12 | Scrittura report o registro fallita | Errore e file realmente salvati espliciti; nessun successo o stato corrente inventato |
| A-13 | Analista diretto senza tool domande | Domanda nella chat principale, attesa della risposta umana esplicita e nessuna operazione dipendente anticipata |
| A-14 | Analista delegato in Local senza interazione umana | Restituisce blocked con domande e checkpoint; orchestratore media e riprende il vero QA-analyst con le risposte umane |
| A-15 | Tool domande disponibile, oppure rifiuto/cancellazione/negazione di permesso | Usa il tool disponibile; nessun fallback per aggirare una decisione o un controllo di accesso |
| A-16 | Risposta ottenuta tramite fallback chat in una run UC | Scope e riferimento umano in Questions/History; schema v1, artefatti obbligatori e permessi invariati |
| A-17 | Tool domande assente ma scrittura disponibile, oppure scrittura realmente fallita | Nessun falso errore filesystem dedotto dal primo caso; errore reale e stop nel secondo, senza workaround terminale |
| A-18 | QA-analyst non registrato o delega indisponibile | Blocco esplicito; nessun agente inventato, generico o impersonato come sostituto |
| A-19 | Task chiamato QA-analyst ma avviato con un worker diverso | Nome descrittivo non accettato come delega; verifica dell'identificativo registrato e della chiamata reale |
| A-20 | Ripresa dopo risposte mediate dall'orchestratore | Identita UC, percorsi e output salvati conservati; conferma di continuita applicata e nessun riavvio cieco dei passaggi completati |

## Stato delle prove

La matrice contiene risultati attesi, non risultati osservati. Nessuna riga
attesta una run reale solo perche esiste qui. I test statici/sintattici possono
essere eseguiti senza queste run; una prova agente deve specificare il caso,
gli input confermati, i percorsi effettivi e l'esito osservato nel suo report.
Una valutazione su un caso iterato non dimostra generalizzazione.
