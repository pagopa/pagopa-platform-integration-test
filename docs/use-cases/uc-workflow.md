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

## Registro e proprieta degli output

Il QA-analyst inizializza [00-run.template.md](workflow-templates/00-run.template.md)
prima di produrre qualsiasi report. Il registro contiene input concordati,
inventario iniziale dei casi desunti dallo UC e **percorsi attesi** degli output.
`not_created` non e prova che un documento esista.

La skill funzionale scrive solo `01-context.md`; quella dati solo
`02-test-data.md` (oltre all'eventuale catalogo autorizzato); la traduzione scrive
le feature concordate e `03-feature-report.md`. Tutte aggiornano la propria riga
Artifacts e la History di `00-run.md` dopo una scrittura riuscita, indicando
produttore, percorso, revisione e stato. Mai dichiarare prodotto un file se
il tool non lo ha scritto. Se il salvataggio fallisce, riportare l'errore e
fermarsi prima del passaggio successivo: testo in chat non e un artefatto
persistito. Non scrivere skill, UC sorgenti, altre specifiche, Python o ACE.

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

Ogni report registra le revisioni dei propri input. Cambi di UC, contesto,
vincoli o decisioni rendono `stale` gli output a valle nel registro; non si
aggiorna soltanto il numero in `inputs`. La skill proprietaria deve rielaborare
il contenuto e incrementare la revisione. Rivalutare l'idoneita dei dati se
cambiano i requisiti; non riutilizzare approvazioni oltre il loro scopo.
Confermare che l'input UC e ancora la revisione registrata a ogni ripresa;
se non verificabile, chiedere all'umano.

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
Placeholder e commenti seguono la skill dati. Il report finale verifica anche
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
5. Tutti i TODO e le incertezze hanno warning per ogni scenario interessato;
   null intenzionali non sono TODO. Tutti gli elementi UC sono in Coverage.
6. Registro `complete` solo con report finale `ready`; `draft` con finale
   `incomplete`; `blocked` con finale `blocked`; altrimenti `in_progress`.
   Questo stato non autorizza sviluppo/esecuzione automatici.

## Fonti e portabilita

La [policy fonti](../../.github/skills/uc-scenario-context/source-policy.md)
resta unica per ammissione, approvazione e privacy. Persistire un candidato
come `pending-approval` non lo rende utilizzabile nella feature. Storici e
cataloghi sono candidati, non stato corrente dell'ambiente.
Le skill dipendono da questo repository, dalle sue instructions e dall'agente:
copiarle da sole a livello utente non rende il workflow portabile.
