# Workflow UC: fonti, dati e feature

Questo e il contratto operativo `uc-workflow/v1`. Le tre skill condividono
il prefisso `uc-` e lavorano con il solo agente `QA-analyst`:

| Ordine | Skill | Responsabilita | Output obbligatorio |
| --- | --- | --- | --- |
| 0 | uc-to-feature, oppure la prima skill invocata manualmente | Confermare input e percorso; inizializzare il registro | `00-run.md` |
| 1 | [uc-scenario-context](../../.github/skills/uc-scenario-context/SKILL.md) | Precisare il comportamento e i valori attesi dalle fonti | `01-context.md` |
| 2 | [uc-test-data](../../.github/skills/uc-test-data/SKILL.md) | Risolvere i dati in ingresso, le combinazioni e gli stati | `02-test-data.md` |
| 3 | [uc-to-feature](../../.github/skills/uc-to-feature/SKILL.md) | Usare i due report per produrre Gherkin e copertura | Percorsi `.feature` concordati e `03-feature-report.md` |

Non genera UC dalla documentazione, Python, test eseguiti o commit automatici.
I nomi precedenti `document-scenario-context` e `resolve-test-data` sono
sostituiti dai nuovi nomi; `uc-to-feature` resta invariato. Non sono alias o skill
duplicate. Riavviare/ricaricare la discovery delle skill nell'harness se mostra
ancora i vecchi comandi. I comandi slash richiedono supporto dell'harness; in
alternativa chiedere esplicitamente al QA-analyst di leggere e usare la skill.
L'instradamento al solo analista e una prescrizione, non un controllo di accesso
garantito dal frontmatter.

## Percorsi, identita e formati

Una esecuzione riguarda **un UC**; piu UC usano registri distinti. Confermare
con l'umano task id, UC id, input UC, revisione UC, ambiente, percorsi feature e:

`docs/use-cases/workflow-runs/<task-id>/<uc-id>/<run-id>/`

### Identita distinte (ADR-07)

Qui `task_id` e il nome storico del campo che identifica la lavorazione UC:
resta stabile quando si riprende la stessa run. Non e il codice Jira
`PQ-<cifre>` assegnato all'umano, ne l'ACE `task_id` della particolare richiesta
in chat. Piu richieste ACE, con identificativi distinti, possono contribuire
alla stessa lavorazione UC e allo stesso ticket Jira.

Riutilizzare l'identita UC confermata alla ripresa; non rinominare directory o
riscrivere il frontmatter dei report per adeguarli al nuovo identificativo ACE.
Nella restituzione all'orchestratore distinguere Jira (se noto), identita UC
(`task_id`, `uc_id`, `run_id`) e ACE request ID ricevuto per la richiesta corrente.
Se serve un collegamento persistente, usare History con un evento amministrativo
reale, senza nuovi campi o invalidazioni dei contenuti.
`uc-workflow/v1`, template e report storici mantengono i campi e i valori esistenti.

### Vincoli dei percorsi

- `run-id`: `YYYYMMDD-NN`, data reale e progressivo libero a due cifre.
- `task-id` e `uc-id`: identificativi concordati, solo lettere, cifre e trattini.
  Vietati segmenti `..`, separatori, percorsi assoluti e nomi derivati dai dati.
- Riutilizzare una run solo su richiesta esplicita; non scegliere il report
  "piu recente" tramite glob. Non sovrascrivere output di un'altra run.
- UC incollato in chat: registrare un riferimento stabile al messaggio e una
  revisione confermata dall'umano, senza creare o modificare un UC sorgente.
- I percorsi nei documenti sono relativi alla root del repository, con `/`;
  i tool sul sistema Windows usano percorsi nativi con `\`.

Usare esattamente i template in [workflow-templates](workflow-templates/).
Ogni report e Markdown UTF-8 con frontmatter YAML, seguito dalle intestazioni
e tabelle del template, nello stesso ordine. Il testo descrittivo e in italiano;
nomi dei campi, intestazioni strutturali e valori enumerati restano quelli del
contratto. Nessun campo obbligatorio puo essere omesso. `unknown` per metadati
non noti; liste vuote `[]`; sezioni senza elementi contengono `Nessuno`.
Le tabelle conservano le colonne: escape `|` nei valori e nessuna riga fittizia.

Metadati comuni:

- `schema`: `uc-workflow/v1`; `artifact`: enum definito nel template.
- `producer_skill`: nome esatto della skill che ha scritto il documento.
- `task_id`, `uc_id`, `run_id`, `uc_input`, `uc_revision`, `environment`:
  identita concordata; la revisione non va dedotta da una data di accesso.
- `revision`: intero positivo, incrementato a ogni aggiornamento persistito.
- `status`: `ready`, `incomplete` o `blocked` per i report; il registro usa
  `in_progress`, `draft`, `complete` o `blocked`.
- `updated_at`: timestamp reale ISO 8601 con fuso orario.
- `inputs`: lista di oggetti `{path, revision}`, solo artefatti a monte realmente
  letti. Le fonti esterne sono nelle tabelle Sources, non in questa lista.

Vocabolari delle tabelle (non sinonimi):

| Colonna | Valori ammessi |
| --- | --- |
| Artifacts.State | `not_created`, `ready`, `incomplete`, `blocked`, `stale` |
| Sources.Admission e Data resolution.Admission | `provided`, `approved`, `pending-approval`, `rejected`, `unknown` |
| Functional evidence.State e Oracles.State | `supported`, `unresolved`, `conflict` |
| Fitness | `fit`, `unverified`, `unfit` |
| Questions.State e Decisions.State | `open`, `answered`, `declined`, `pending-approval` |
| Timing semantics | `maximum`, `minimum`, `exact`, `not-applicable`, `unknown` |
| Coverage and reason | `covered`, `partial`, `uncovered`, seguito da una motivazione se non covered |
| Feature outputs.Write result | `written`; file non scritti non compaiono in questa tabella |
| Optional catalogue | `not-requested`, `not-saved`, `pending-confirmation`, oppure percorso realmente salvato con decisione |

Nel registro aggiungere una riga `feature` per ogni `.feature` scritto:
produttore `uc-to-feature`, percorso concordato, revisione locale incrementale
e stato `ready` o `incomplete` coerente con il report finale. I report hanno
sempre le tre righe previste, anche quando non creati. `inputs` registra solo
file letti: un report finale bloccato per prerequisiti mancanti usa la lista
dei soli input effettivi (anche `[]`), non i percorsi fittizi del template.
Se un artefatto dichiarato non esiste, correggere il registro con l'errore e
non avanzare.

`Availability evidence` contiene `documented-not-checked`, `user-confirmed`
oppure `unknown-to-prepare`, seguito da fonte, scopo e data se presenti.
Gli SC devono esistere nell'inventario del registro; gli F/O/D nella run devono
essere definiti in `01-context.md`, i C in `02-test-data.md`. Le S sono locali
al report: un richiamo inter-report usa `01-context.md#S-001` o
`02-test-data.md#S-001` come identificativo testuale, non come link a un anchor
Markdown inesistente. Le questioni Q sono allocate nel registro e richiamate
nei report. Non confondere id dei requisiti con nomi di campi API o placeholder.

Identificativi stabili nella run: `SC-NNN` scenari/casi previsti, `S-NNN` fonti,
`F-NNN` evidenza funzionale, `O-NNN` oracle, `D-NNN` requisiti dati, `C-NNN`
combinazioni di dati, `Q-NNN` questioni. Non rinumerare o riciclare id eliminati.
Un caso poi raggruppato in un outline mantiene il proprio `SC-NNN`; il report
finale lo associa a file, titolo scenario e riga di Examples.

### Requisiti, casi e valori

Un D identifica un requisito dati con significato, ruolo e vincoli, non un
singolo valore. Piu SC possono usare lo stesso D con valori diversi nelle
rispettive C, senza creare un D per ogni riga. Due entita con ruoli distinti
o valori che devono essere diversi nello stesso caso richiedono D distinti,
definiti dal contesto con la relazione richiesta. Il report dati non assegna
nuovi D: propone la necessita e ritorna al contesto.

In Data resolution distinguere le risoluzioni per D e SC; se lo stesso SC
ha piu C con valori differenti, esplicitare i C pertinenti nella cella
`Value or TODO token`. Combinations associa ogni D al valore scelto:
nessuna risoluzione sovrascrive un altro valore dello stesso requisito.
Ogni valore selezionato deve corrispondere a una risoluzione con provenienza,
ammissione e idoneita; non ereditare queste proprieta da un altro valore.

`__TODO_D001__` identifica D-001, non e un valore concreto condiviso ne
un'asserzione di uguaglianza fra istanze. Si puo ripetere per lo stesso
requisito in casi diversi, mantenendo irrisolta ciascuna C interessata.
Per requisiti distinti usare token distinti; mai rinumerare i D esistenti
per differenziare semplici varianti di valore.

## Varianti dati e riferimenti AC ai flussi

Le AF rappresentano variazioni del percorso o dell'esito, non set di dati.
Le skill di supporto ricavano dimensioni, vincoli e combinazioni rilevanti
dalla documentazione e dal materiale ammessi anche senza AF dedicate.
Il numero di record di un catalogo non determina il numero di casi: niente
prodotto cartesiano o varianti arbitrarie. Restano obbligatori ammissione,
evidenza, idoneita e gestione separata della disponibilita.

L'inventario iniziale puo essere esteso durante l'analisi del contesto con nuovi
SC-NNN per casi supportati dello stesso flusso, senza modificare lo UC.
Registrare motivazione, fonti, AC e F/O/D applicabili nel contesto; i dati
riportano le combinazioni C-NNN per questi casi. Se la risoluzione dati scopre
un caso aggiuntivo, ritorna al contesto per registrarlo e collegarlo prima di
usarlo nelle combinazioni, senza avviare altri step in modalita manuale.
Riutilizzare gli F/O/D esistenti quando il significato non cambia. La traduzione
decide il raggruppamento finale: stesso comportamento e stesse verifiche
possono diventare righe di un outline; casi con insiemi di verifiche differenti
restano separati. Piu AC compatibili per lo stesso caso, invece, si verificano
nello stesso scenario con Then/And: il rapporto AC:flusso e AC:scenario puo
essere molti-a-uno per FP, AF ed EF/casi negativi. Non creare uno scenario per
AC, non conservare un solo AC per flusso e non considerare duplicati i
riferimenti allo stesso flusso in criteri distinti. Coverage conserva una
voce per ogni AC anche quando scenario e riga Examples coincidono.
Nuovi vincoli funzionali richiedono prima un aggiornamento del contesto,
poi dei dati, con normale invalidazione a valle.

E consigliato un riferimento verbale negli AC, per esempio `(FP)` o `(AF02)`,
ma non e un nuovo campo obbligatorio. La skill uc-to-feature definisce le
[forme riconosciute e la risoluzione](../../.github/skills/uc-to-feature/ac-flow-references.md):
case insensitive, spazi flessibili, acronimi anche puntati e confronto con
gli identificativi effettivi dello UC. Il riferimento include le varianti
supportate del flusso salvo limitazioni espresse dall'AC; non estende le
verifiche ad altri flussi. Riferimenti ambigui, duplicati o inesistenti
rimangono questioni esplicite. Nessun riferimento non significa FP di default.

## Registro e proprieta degli output

Il QA-analyst inizializza [00-run.template.md](workflow-templates/00-run.template.md)
prima di produrre qualsiasi report. Il registro contiene input concordati,
inventario iniziale dei casi desunti dallo UC e **percorsi attesi** degli output.
`not_created` non e prova che un documento esista.

La skill funzionale scrive solo `01-context.md`; quella dati solo
`02-test-data.md` (oltre all'eventuale catalogo autorizzato); la traduzione scrive
le feature concordate e `03-feature-report.md`. Il registro e condiviso con
questi permessi, non con un generico diritto di riscrittura:

| Sezione o operazione | Chi puo aggiornarla | Limite |
| --- | --- | --- |
| Agreed inputs e identita | Skill inizializzatrice; poi skill attiva con conferma umana | Registrare input concordati; un cambiamento sostanziale invalida gli output dipendenti |
| Scenario inventory | uc-to-feature (iniziale); uc-scenario-context | Allocare SC stabili e motivati; uc-test-data propone nuovi casi senza registrarli autonomamente |
| Questions | Tutte e tre le skill | Allocare Q globali e aggiornare solo decisioni pertinenti con riferimento umano; non cambiare decisioni altrui senza conferma |
| Artifacts: produzione | Skill proprietaria dell'output | Aggiornare solo la propria riga dopo salvataggio riuscito; uc-to-feature gestisce anche le righe feature |
| Artifacts: invalidazione | Skill che rileva modifica o errore | Marcare stale gli output dipendenti gia creati senza cambiare produttore, percorso o revisione degli output altrui |
| History e metadati registro | Skill attiva | Appendere eventi reali e aggiornare revision, updated_at e status del registro |

Ogni aggiornamento persistito del registro incrementa la sua revisione e
mantiene History, inventario e decisioni precedenti. Allocare Q non basta
a risolverla: la stessa decisione e il suo scopo devono essere coerenti nel
registro e nel report proprietario. Quando la decisione cambia il contenuto
di un altro report, invalidarlo e rinviare alla sua skill; non editarlo.

Mai dichiarare prodotto un file se il tool non lo ha scritto. Se il salvataggio
di un output o del registro fallisce, riportare l'errore e fermarsi prima del
passaggio successivo; segnalare i file eventualmente gia scritti e non
dichiarare completata la run. Alla ripresa riconciliare l'operazione incompleta
con la skill proprietaria. Non scrivere skill, UC sorgenti, altre specifiche,
Python o ACE durante l'esecuzione dell'analista.

Il report dati e sempre obbligatorio, anche se contiene solo requisiti mancanti
e TODO; non e il catalogo opzionale `docs/use-cases/test-data/<scope>/`.
Il report funzionale e obbligatorio anche quando lo UC basta: cita lo UC come
fonte, registra le informazioni sufficienti e non cerca fonti inutili.
I report sono evidenza derivata, **non nuove specifiche autoritative**.
Nel report funzionale `inputs` e `[]`: lo UC e identificato nei metadati e in
Sources. Il report dati registra la revisione del contesto; il report finale
registra quelle di contesto e dati. Non registrare la revisione continuamente
crescente del registro come dipendenza: la sua identita/inventario e comunque
verificata a ogni passaggio.

## Esecuzione automatica

Invocare `/uc-to-feature` con UC, task id, fonti e destinazione, oppure:

> Usa uc-to-feature per questo UC, con analisi funzionale e dati, e registra
> gli output secondo uc-workflow/v1.

L'analista:

1. Conferma gli input mancanti e crea/legge `00-run.md`.
2. Valida lo UC e prepara l'inventario `SC-NNN`, senza importare suite esistenti.
3. Invoca o legge e applica `uc-scenario-context`; salva `01-context.md`.
4. Legge quel file, poi invoca o applica `uc-test-data`; salva `02-test-data.md`.
5. Rilegge registro e report dai percorsi registrati, valida identita, revisione,
   stato e riferimenti; produce feature e `03-feature-report.md`.
6. Aggiorna il registro e restituisce i percorsi realmente prodotti, produttori,
   stati, questioni aperte e controlli effettivamente svolti.

Le skill di supporto non richiamano automaticamente la traduzione: le
restituiscono gli artefatti, evitando cicli ricorsivi. La skill dati, se scopre
una domanda funzionale, la registra e restituisce il controllo alla traduzione,
che ripete contesto, poi dati, solo per la parte cambiata.

## Esecuzione manuale, uno step alla volta

Selezionare `QA-analyst` nel selettore agente; i comandi sono:

```text
/uc-scenario-context Analizza questo UC e queste fonti. Task <task-id>.
Crea la run <run-id> per <uc-id>; conferma con me input e percorso del registro.
```

Fermarsi e leggere `01-context.md`, chiarire/approvare i candidati se necessario.
Poi:

```text
/uc-test-data Usa il registro <percorso-root-relativo>/00-run.md
e il suo 01-context.md. Risolvi i requisiti con queste fonti di dati.
```

La skill verifica il prerequisito funzionale: se manca, non lo sintetizza dalla
memoria e non avvia autonomamente altri step in modalita manuale. Chiede di
eseguire `uc-scenario-context`.

Infine:

```text
/uc-to-feature Usa il registro <percorso-root-relativo>/00-run.md
in modalita assemble-only. Leggi i due report e produci le feature concordate.
```

In `assemble-only` non riesegue skill di supporto: se report mancanti, stale,
incompatibili o bloccanti, spiega quale step eseguire. In modalita automatica
puo invece invocare solo i passaggi necessari per renderli correnti.
Invocare la prima skill gia autorizza i report contrattuali nella run confermata,
ma non approva fonti autonomamente scoperte o valori di dati.

## Ripresa, invalidazione e controlli

Prima di consumare un report, controllare frontmatter, sezioni, colonne e id;
leggere il percorso esatto dal registro. Verificare che produttore, artefatto,
UC, task, run, ambiente e revisione coincidano. Una stringa `producer_skill`
non basta a garantire la provenienza: confrontare la riga Artifacts, History e
le fonti/decisioni del report. Se un report e esterno o modificato manualmente,
chiedere conferma e farlo validare dalla skill proprietaria, senza fingere che
lo abbia prodotto essa.

### Conferma di continuita alla ripresa

Il contratto resta `uc-workflow/v1`: nessun nuovo campo, fingerprint, parser
operativo o comando e richiesto all'analista. Revisioni e History da sole
non rilevano modifiche di contenuto che conservano i metadati. La verifica
di continuita e umana, non una certificazione automatica di integrita.

Alla ripresa di una run esistente, anche tra comandi manuali o dopo
un'interruzione, prima di riusare o sovrascrivere output chiedere conferma
tramite lo strumento domande. Presentare un inventario esatto di input UC,
fonti/passaggi usati, profilo/input concordati, report da consumare e feature
gia registrate, con percorsi, revisioni e stati noti. Chiedere se i contenuti
sono invariati rispetto a quelli registrati, non solo se i numeri coincidono;
una risposta generica non copre file non elencati. I file mancanti o
illeggibili restano errori, anche se l'umano li dichiara invariati.

Registrare risposta, scopo, riferimento umano e timestamp in una Q di
Questions e in History, usando le colonne esistenti. Se l'umano conferma
la continuita, e i controlli strutturali passano, si possono riusare report
correnti senza ripetere retrieval. Una conferma vale per i percorsi e le
revisioni elencati nella ripresa corrente; una nuova ripresa o una modifica
richiede un nuovo controllo. Non ripetere la domanda fra passaggi automatici
consecutivi della stessa esecuzione senza interruzioni o modifiche esterne.

Se viene dichiarata una modifica, marcarne l'artefatto e i dipendenti stale
prima del riuso; la skill proprietaria valida/riproduce il contenuto e
incrementa la revisione. Non adottare ciecamente producer_skill o revision
di un file modificato: registrare la provenienza manuale in History.
In assemble-only fermarsi e indicare la skill da rieseguire, senza retrieval.
Se la continuita non e confermata o non e verificabile, registrare la
questione aperta/declined, marcare stale gli output esistenti coinvolti e
bloccare la ripresa; non presumere che siano correnti.

Le feature ai percorsi concordati si possono leggere solo per verificare
la corrispondenza con il report, le modifiche dichiarate e la destinazione
di scrittura, mai come fonte di requisiti, step o convenzioni. Una feature
modificata non diventa una fonte funzionale: fermarsi prima di sovrascriverla,
chiarire con l'umano come preservare le modifiche e far riconciliare alla
traduzione il report con UC e fonti ammesse. Non cancellare file o modifiche
manuali automaticamente.

La conferma di continuita non approva nuovi candidati e non rinnova la
disponibilita dei dati nell'ambiente. I report v1 precedenti si possono
riusare solo dopo questa conferma e i controlli correnti; enum non canonici
o altre incompatibilita richiedono rivalidazione della skill proprietaria,
non una conversione silenziosa del consumatore.

### Invalidazione e stato della run

Ogni report registra le revisioni dei propri input. Cambi di UC, contesto,
vincoli o decisioni rendono `stale` gli output a valle nel registro; non si
aggiorna soltanto il numero in `inputs`. La skill proprietaria deve rielaborare
il contenuto e incrementare la revisione. Rivalutare l'idoneita dei dati se
cambiano i requisiti; non riutilizzare approvazioni oltre il loro scopo.
Confermare che l'input UC e ancora la revisione registrata a ogni ripresa;
se non verificabile, chiedere all'umano.

| Contenuto cambiato | Output da invalidare nel registro |
| --- | --- |
| UC, ambiente o decisione funzionale | context, test-data, feature-report, feature |
| 01-context.md | test-data, feature-report, feature |
| Fonte o decisione solo dati | test-data, feature-report, feature |
| 02-test-data.md | feature-report, feature |
| Feature registrata modificata manualmente | feature interessata, feature-report |
| 03-feature-report.md modificato manualmente | feature-report, feature |
| History o sola conferma di continuita | Nessuno |

La tabella include tutte le righe feature dipendenti, non solo i report.
Un artefatto modificato manualmente e anch'esso stale; se e appena stato
rielaborato dal proprietario, la sua nuova riga riporta lo stato effettivo.
`not_created` resta tale; invalidare un output mai creato non lo rende
esistente. Conservare le revisioni registrate degli output invalidati:
solo il produttore le incrementa dopo una scrittura riuscita.
Modifiche al profilo, agli input Gherkin o ai percorsi feature invalidano
feature-report e feature; se cambiano anche il significato funzionale,
invalidare pure contesto e dati.

Quando si invalida un risultato esistente, la run passa a `in_progress`,
non resta complete/draft sulla base del vecchio report. Una ripresa fermata
per identita, accesso o continuita non confermata usa `blocked`, con la Q
pertinente. La sola modifica amministrativa del registro non invalida
report o feature: non usare la revisione o l'intero contenuto di 00-run.md
come dipendenza a monte. Non creare cicli di auto-invalidazione.

`01-context.md`: `ready` solo senza lacune funzionali bloccanti; `incomplete`
per copertura parziale esplicita; `blocked` per conflitto/identita non risolti.
`02-test-data.md`: `ready` solo con tutti i dati richiesti idonei e ammessi e
stati necessari stabiliti; `incomplete` per TODO o incertezze. Dati mancanti
non bloccano la produzione di una feature **bozza**. Un conflitto funzionale
o input non valido produce `blocked`, non valori presunti.

Con contesto incompleto, la traduzione puo produrre solo scenari supportati,
segnalando tutta la copertura mancante; non inventa azioni/Then per riempire
il file. Se nessuno scenario e supportato, non crea una feature vuota: scrive
un report finale `blocked`, senza registrare feature inesistenti. Non consuma
report `blocked`, `stale` o `not_created`.

La feature applica le instructions Gherkin; non eredita le tabelle Markdown.
Placeholder e commenti seguono la skill dati: solo i placeholder irrisolti
richiedono commenti sui dati nella feature. Provenienza, approvazione,
idoneita e disponibilita restano nei report, anche quando non esistono TODO.
Nella tabella Scenario warnings del report dati, Required comment contiene
`not-applicable` quando non occorre un commento; l'incertezza resta nelle
colonne esistenti e in Data resolution/Readiness, senza cambiare lo schema.
L'ambiente resta nei metadati e nell'applicabilita delle fonti; hostname e
base URL di deployment sono risolti dalla configurazione della run, non
fissati negli step, salvo requisito funzionale esplicito. I Given richiedono
evidenza di preparazione o osservazione indipendente dall'operazione testata:
un vincolo di idoneita del dato non basta a garantirne lo stato iniziale.
La mancanza di tale evidenza e distinta da una lacuna nella regola funzionale;
una precondizione UC non attuabile non viene eliminata, ma resta aperta.
Il report finale verifica anche
coerenza dei riferimenti, combinazioni, oracle e tutti gli SC/AC/AF/EF coperti
o esclusi con ragione. La sintassi controllata non implica disponibilita
dell'ambiente, step Python implementati o test eseguiti. L'analista non esegue
parser/test da terminale: dichiara controlli statici effettivi, oppure il
risultato di un controllo autorizzato fornito esternamente.

Prima di chiudere una run, verificare:

1. Tutti i file dichiarati `ready`/`incomplete`/`blocked` nel registro esistono;
   produttore e revisione dei report coincidono col frontmatter.
2. `inputs` del report dati e finale coincidono con le revisioni a monte
   realmente consumate; revisioni discordanti rendono l'output `stale`.
3. Ogni azione/oracle applicato nella feature ha evidenza `supported` con
   fonte `provided` o `approved`. Evidenza non ammessa non copre un requisito.
4. Ogni valore applicato proviene da una riga del report dati ammessa e idonea,
   oppure esplicitamente autorizzata come non verificata con warning. Tutte
   le combinazioni rispettano i vincoli, senza prodotto cartesiano inventato.
5. Tutti i TODO e le incertezze hanno warning nei report per ogni scenario
   interessato; solo i TODO richiedono commenti nelle feature. La risoluzione
   dell'ultimo TODO rimuove il relativo commento, non le incertezze residue
   nei report. Null intenzionali non sono TODO. Tutti gli elementi UC sono
   in Coverage.
6. Registro `complete` solo con report finale `ready`; `draft` con finale
   `incomplete`; `blocked` con finale `blocked`; altrimenti `in_progress`.
   Il report deve essere corrente anche nel registro e i controlli di
   continuita applicabili devono essere soddisfatti. Un report finale blocked
   non riabilita le feature stale di una generazione precedente.
   Questo stato non autorizza sviluppo/esecuzione automatici.

## Verifica del contratto

I [casi di regressione](uc-workflow-validation.md) fissano risultati attesi
per proprieta, identita, ripresa, granularita, enum e TODO. I test statici e
sintattici degli asset sono eseguiti esternamente all'analista e non sono
test della suite applicativa. La loro riuscita non dimostra che l'agente
abbia completato una run reale; tale verifica richiede input umani e run
confermati, e registra controlli effettivi nel report finale.

## Fonti e portabilita

La [policy fonti](../../.github/skills/uc-scenario-context/source-policy.md)
resta unica per ammissione, approvazione e privacy. Persistire un candidato
come `pending-approval` non lo rende utilizzabile nella feature. Storici e
cataloghi sono candidati, non stato corrente dell'ambiente.
Le skill dipendono da questo repository, dalle sue instructions e dall'agente:
copiarle da sole a livello utente non rende il workflow portabile.
