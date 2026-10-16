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
| V-25 | Conferma di continuita su report con disponibilita dati non stabilita | Nessuna nuova ammissione o availability dedotta; warning e bozza conservati | Admission, Availability evidence e Readiness |
| V-26 | Salvataggio di feature/report riuscito ma registro fallito | Errore esplicito, stop e riconciliazione del proprietario; nessuna run complete presunta | File effettivi, errore e History riconciliata |

## Stato delle prove

La matrice contiene risultati attesi, non risultati osservati. Nessuna riga
attesta una run reale solo perche esiste qui. I test statici/sintattici possono
essere eseguiti senza queste run; una prova agente deve specificare il caso,
gli input confermati, i percorsi effettivi e l'esito osservato nel suo report.
Una valutazione su un caso iterato non dimostra generalizzazione.
