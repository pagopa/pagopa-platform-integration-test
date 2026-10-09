# ACE: Agentic Context Engineering — integrazione embedded

ACE è un framework che trasforma l'esecuzione in memoria operativa duratura per un team di agenti. Invece di riscrivere le stesse regole in ogni prompt e di improvvisare di task in task, il team registra ciò che è accaduto davvero, riflette su quei fatti, trasforma i pattern ricorrenti in `proposal` strutturate, valida tali proposte e applica solo le `decision` che hanno evidenza reale alle spalle.

Il risultato è un loop di apprendimento: i file `trace` diventano evidenza, i documenti `proposal` diventano cambiamenti candidati e il `playbook` insieme alle `instructions` generate diventano il contesto duraturo e riutilizzabile del sistema.

Questo repository è il template del runtime del ciclo. Non contiene un'applicazione di dominio reale né un team reale. Contiene invece il motore generico che può essere installato in un progetto ospite e poi crescere con l'evidenza del progetto stesso.

## Installazione, aggiornamento e migrazione

L'installazione crea ACE dove non è presente; usa
[INSTALL_PROMPT_EMBEDDED.md](../INSTALL_PROMPT_EMBEDDED.md). L'aggiornamento
porta avanti un'installazione esistente senza cambiarne il paradigma; usa
[UPDATE_PROMPT.md](../UPDATE_PROMPT.md). La migrazione passa da embedded a
mediated (o ristruttura materialmente il comportamento degli agenti posseduto
dal progetto) e richiede un piano separato e un'approvazione esplicita.

Un'installazione embedded precedente a `integration_mode` è **legacy
embedded**. L'aggiornamento deve aggiungere `integration_mode: "embedded"` e
aggiornare ACE solo negli agenti già partecipanti. Questa normalizzazione
preserva il paradigma e non è una migrazione: non deve coinvolgere nuovi
agenti né convertire l'installazione alla modalità mediated.

Per l'inventario di aggiornamento il kit offre un comando di sola lettura:

```text
node <KIT_ROOT>/ace/scripts/inspect_update.js --target <TARGET_ROOT>
```

Riporta modalità rilevata, versioni, ownership, conflitti e normalizzazioni
richieste senza scrivere (`write_performed: false`).
`ace/runtime-version.json` definisce versione runtime, classi di ownership e
hash dei file posseduti dal kit. Entrambi forniscono evidenza alla procedura di
aggiornamento, ma non autorizzano a sovrascrivere configurazione, comportamento
operativo, playbook, trace o stato del progetto.

## Il ciclo ACE, letto dall'alto verso il basso

Il modo migliore di leggere ACE è partire dal risultato e risalire al meccanismo:

1. un task viene eseguito da un agente;
2. una `trace` registra ciò che è successo;
3. un `reflector` legge un batch di `trace` e propone un cambiamento;
4. un `curator` trasforma le `proposal` in oggetti `decision` tipizzati;
5. un `warden` convalida la `decision` e chiede un esplicito sign-off umano;
6. il `playbook` viene aggiornato e poi le `instructions` vengono rigenerate;
7. la sessione successiva parte con un contesto migliore e regole operative più chiare.

Questo non è un motore di diagnosi e non è un motore di business logic. È un loop operativo di apprendimento che usa evidenze per migliorare il sistema agente stesso.

## Struttura del runtime

```text
ace/
├── config/
│   ├── project.json             # configurazione reale del runtime del progetto ospite
│   └── thresholds.json          # trigger del batch per `reflector` / `curator` / `warden`
├── prompts/
│   ├── reflector.md             # come il `reflector` legge le `trace` e propone il cambiamento
│   ├── curator.md               # come il `curator` trasforma le `proposal` in `decision`
│   └── warden.md                # come il `warden` valida e applica il delta firmato
├── schema/
│   ├── trace.schema.json        # forma di una `trace`
│   └── bullet.schema.json       # forma di un `bullet` dentro il `playbook`
├── proposals/
│   └── applied/                 # batch processati, `decision` e report di gate
├── scripts/
│   ├── generate_ace_agents.js   # genera wrapper e agenti del runtime per piattaforma
│   ├── retrieval.js             # rigenera le `instructions` della piattaforma dal `playbook`
│   ├── check_threshold.js       # decide se il passaggio successivo deve essere attivato
│   ├── update_counters.js       # somma le evidenze delle `trace` nei contatori dei bullet
│   ├── gate.js                  # convalida meccanica prima che un write sia consentito
│   ├── apply_delta.js           # applica il delta firmato al `playbook`
│   ├── inspect_update.js        # inventario e conflitti di update, in sola lettura
│   └── validate_install.js      # verifica che il runtime installato sia strutturalmente completo
├── runtime-version.json         # versione runtime, ownership e hash dei file del kit
├── state/
│   └── live-exclusions.json     # esclusioni runtime mentre una regola cattiva è sotto revisione
├── traces/
│   ├── processed/               # `trace` già integrate in un batch
│   └── CAPTURE_GUIDE.md         # come scrivere una `trace`
├── playbooks/                  # sorgente duratura delle regole apprese
│   ├── _global.md
│   ├── families/
│   ├── archive/
│   └── <agent>.md
└── README_EMBEDDED_IT.md       # riferimento del ciclo con integrazione embedded
```

Il punto architetturale importante è che il runtime è volutamente separato tra il `playbook` duraturo e rivisitabile e le `instructions` generate, compatte e pronte per la sessione attiva.

## Gli oggetti centrali del ciclo

### `trace`

Una `trace` è la registrazione di evidenza di un task. Documenta i fatti che contano per l'apprendimento: quali bullet del `playbook` sono stati visti, quali sono stati citati, cosa è successo e se l'esito è stato verificato.

Esempio:

```json
{
  "task_id": "T-204",
  "agent": "planner",
  "started_at": "2026-09-16T09:00:00Z",
  "ended_at": "2026-09-16T09:14:00Z",
  "playbook_bullets_seen": ["PR-011", "PR-015"],
  "playbook_bullets_cited": ["PR-011"],
  "outcome": {
    "status": "success",
    "evaluated_by": "verified"
  },
  "notes": "La verifica del percorso del file ha evitato una scrittura nel target sbagliato.",
  "friction": ["Il percorso era ambiguo all'inizio."],
  "counted_for_playbook_at": "2026-09-16T09:15:00Z"
}
```

### `proposal`

Una `proposal` è una regola candidata, non una scrittura. Il `reflector` legge batch di file `trace` e produce ipotesi strutturate su ciò che deve cambiare.

Esempio:

```json
{
  "proposal_id": "PR-042",
  "batch_id": "batch-2026-09-16",
  "relation_to_existing": "UPDATE",
  "target_bullet_id": "PR-011",
  "confidence": "high",
  "final_content": "Prima di creare un file, verifica il percorso di destinazione e l'estensione prima di scrivere.",
  "rationale": "Questa regola è stata citata in due task diversi e ha impedito scritture nel percorso sbagliato."
}
```

### `decision`

Una `decision` è la risposta tipizzata del `curator` a una `proposal`. Dice se la proposta diventa `ADD`, `UPDATE`, `DEPRECATE`, `MERGE`, `PROMOTE` oppure `REJECT`.

Esempio:

```json
{
  "proposal_id": "PR-042",
  "decision": "UPDATE",
  "target_bullet_id": "PR-011",
  "scope": "global",
  "curator_rationale": "L'evidenza è coerente e la regola è già vicina al comportamento desiderato."
}
```

## Il ciclo in quattro fasi

```text
raccolta della `trace`
        ↓
`reflector` legge il batch e produce la `proposal`
        ↓
`curator` trasforma la `proposal` in `decision`
        ↓
`warden` convalida e richiede il sign-off umano
        ↓
aggiornamento del `playbook` + rigenerazione delle `instructions`
```

### 1. Raccolta della `trace`

Il runtime registra una `trace` per ogni agente rilevante per ogni task. Questa è l'evidenza grezza del resto del ciclo. Una `trace` è intenzionalmente compatta: non è una narrazione della sessione, ma un record strutturato di fatti rilevanti, esiti, attriti ed evidenze.

### 2. `reflector`

Il `reflector` lavora in batch. Legge tutti i file `trace` non processati, rileva pattern ricorrenti, controlla i dati rispetto al `playbook` corrente e scrive un file di `proposal` strutturato. Non modifica mai direttamente il `playbook` e non decide mai operativamente se una regola sia live.

### 3. `curator`

Il `curator` riceve il batch di proposte e converte ciascuna in una `decision` tipizzata. È il punto in cui il sistema smette di reagire a un caso isolato e inizia a trasformare un rumore di evidenza in una decisione difendibile.

### 4. `warden`

Il `warden` è la porta di sicurezza. Esegue controlli deterministici come validità dello schema, coerenza degli ID e compatibilità delle operazioni. Blocca anche le scritture a meno che un essere umano approvi esplicitamente l'azione finale. Qui il loop di apprendimento viene tenuto onesto.

## Human in the loop

ACE non è un ottimizzatore automatico silenzioso. L'essere umano resta nel loop nel punto in cui un cambiamento può influenzare davvero il runtime duraturo.

Il modello è:

```text
validazione meccanica -> domanda esplicita -> revisione umana -> scrittura firmata
```

Questo è importante perché il sistema impara dai dati di esecuzione reali, non inventa sicurezza. `gate.js` può controllare struttura e coerenza, ma non può valutare in modo affidabile il conflitto semantico tra una nuova regola e il `playbook` esistente nello stesso scope. Quella è una valutazione umana.

Il sign-off umano non è quindi un ornamento facoltativo. È il meccanismo che trasforma una proposta in una decisione reale del runtime. Senza quella conferma esplicita, `apply_delta.js` rifiuta di scrivere e `retrieval.js` non rigenera le `instructions` operative dallo stato nuovo.

In altre parole, l'umano è il revisore finale della memoria del sistema. Il sistema può proporre e validare; solo l'umano decide se la nuova regola appartiene al contesto operativo duraturo.

## `playbook` e `instructions`: contenuti diversi, scopi diversi

La differenza è intenzionale. Un `playbook` è la fonte di verità duratura; le `instructions` sono la vista generata, pronta per il runtime della sessione attiva.

```text
`playbook`                                                  `instructions`
────────────────────────────────────────────────────────────────────────────────────
Sorgente di verità per il team                              Artifact generato per il runtime
Ha metadati duraturi: status, scope, tags, counters         Sono ridotte alle direttive operative
Memorizza provenienza ed evidenza                           Non contengono metadati di governance nel contesto dell'agente
Pensato per revisione, confronto, promozione, deprecazione  Pensato per consumo rapido da parte di un agente live
Può contenere candidature, quarantena, archivi              Viene servito solo il contenuto attivo e sicuro
```

Questa separazione esiste per due motivi:

- il `playbook` deve mantenere il ciclo di vita completo di una regola: da dove viene, quale evidenza la supporta, in quale stato si trova e quali contatori ha accumulato;
- le `instructions` devono essere compatte, leggibili e sicure da consumare in-sessione. Sono un sottoinsieme filtrato del `playbook`, non una seconda fonte di verità.

Una regola deprecata o quarantinata non dovrebbe restare attiva nel contesto generato solo perché il sistema continua a trattenerla in memoria. Il retrieval risolve questo problema applicando i contatori più recenti e la politica di esclusione prima di generare le `instructions`.

## Esempio: il formato reale del `playbook`, lo schema e le `instructions` generate

La correzione più importante è questa: il `playbook` reale sul disco non è un oggetto JSON standalone. È un file markdown in `playbooks/*.md`, e il formato effettivo dei bullet è quello analizzato da [ace/scripts/lib/playbook.js](../ace/scripts/lib/playbook.js) e documentato nel commento interno di [playbooks/_global.md](../playbooks/_global.md).

Questo significa che ci sono due livelli da capire:

- lo schema logico in [ace/schema/bullet.schema.json](../ace/schema/bullet.schema.json), cioè la forma JSON canonica usata per validazione e logica del runtime;
- la serializzazione markdown nel file del `playbook`, cioè ciò che lo script scrive e legge davvero sul disco.

Il formato markdown reale è:

```markdown
## P-014 — active — used:12 helped:9 hurt:1
Prima di creare un file, verifica il percorso di destinazione e l'estensione prima di scrivere.

tags: [filesystem, write, path]
counters: helped_confirmed=7; helped_provisional=2; hurt_confirmed=1; hurt_provisional=0
provenance: source_trace_ids=[T-108, T-201]; created_at=2026-09-16T10:00:00Z; created_by=reflector+curator; batch_id=batch-2026-09-16
```

Lo schema logico per la stessa regola è il modello JSON usato per la validazione, non il formato letterale del file:

```json
{
  "id": "P-014",
  "status": "active",
  "scope": { "type": "global" },
  "content": "Prima di creare un file, verifica il percorso di destinazione e l'estensione prima di scrivere.",
  "tags": ["filesystem", "write", "path"],
  "counters": {
    "used": 12,
    "helped": 9,
    "hurt": 1,
    "helped_confirmed": 7,
    "helped_provisional": 2,
    "hurt_confirmed": 1,
    "hurt_provisional": 0
  },
  "provenance": {
    "source_trace_ids": ["T-108", "T-201"],
    "created_at": "2026-09-16T10:00:00Z",
    "created_by": "reflector+curator"
  }
}
```

Le `instructions` generate sono intenzionalmente più piccole e private dei metadati di governance. La stessa regola diventa:

```markdown
- **[P-014]** Quando il procedimento descritto dipende da un elettrodomestico o contenitore specifico (piastra a induzione, microonde, barattolo chiuso, roaster, ecc.), coinvolgi sempre `<cook-physicist>` anche se la domanda dell'utente non contiene parole chiave esplicite di fisica o sicurezza.
```

Il punto importante è che il `playbook` conserva tutto il record operativo, mentre le `instructions` sono solo la vista filtrata e pronta per il runtime che l'agente live consuma.

## Perché `PR`?

L'acronimo `PR` in ACE è scelto per significare `playbook rule`. L'idea di fondo è che ogni bullet sia una piccola regola operativa rivisitabile: un'unità di conoscenza che può essere valutata, promossa, aggiornata, deprecata o respinta man mano che cambiano le evidenze.

Questo fa di `PR` un identificatore significativo per l'unità atomica del loop di apprendimento, non un'etichetta generica. In un documento orientato all'uso umano, `PR` comunica che l'oggetto è una regola operativa nella memoria duratura del sistema, non solo una nota temporanea o un commento arbitrario.

Un esempio chiaro è un identificatore come `PR-014`: breve, stabile e semanticamente significativo per una regola già revisata nel `playbook`.

## La struttura di un `bullet`

Un `bullet` è l'unità minima di istruzione appresa in ACE. I campi sono separati tra contenuto operativo e metadati di governance.

```json
{
  "id": "PR-014",
  "status": "active",
  "scope": { "type": "global" },
  "content": "Controlla la destinazione prima di scrivere un nuovo file.",
  "tags": ["filesystem", "write"],
  "counters": {
    "used": 12,
    "helped": 9,
    "hurt": 1
  },
  "provenance": {
    "source_trace_ids": ["T-108", "T-201"],
    "created_at": "2026-09-16T10:00:00Z",
    "created_by": "reflector+curator"
  }
}
```

Il testo operativo è ciò che l'agente vede in-sessione. Tutto il resto — contatori, provenienza, stato del ciclo di vita — serve a supportare governance e retrieval sicuro.

## Perché il ciclo è batch-oriented

ACE è progettato attorno ai batch, non alle reazioni caso per caso. Un singolo task non è abbastanza per giustificare un cambiamento strutturale al `playbook`. Il sistema attende finché non esiste un insieme significativo di `trace`, poi esegue il `reflector`, poi il `curator` e infine il `warden`.

Questo crea un ritmo disciplinato di apprendimento:

- i segnali giornalieri vengono raccolti come dati `trace`;
- i pattern ricorrenti sono aggregati in un batch;
- il sistema propone solo dopo che l'evidenza si è accumulata;
- solo una `decision` firmata può produrre un cambiamento duraturo.

## Conclusione

ACE non serve a automatizzare via il team. Serve a dare al team una memoria strutturata che migliora nel tempo senza costringere ogni regola in ogni prompt a mano.

Il pattern reale è semplice:

```text
`trace` -> `proposal` -> `decision` -> `playbook` -> `instructions` -> prossima sessione migliore
```

Ciò che rende il sistema sicuro è la separazione disciplinata tra raccolta di evidenza, generazione di proposte, revisione e sign-off umano finale. È proprio questo il motivo per cui ACE può apprendere senza derivare silenziosamente verso comportamenti incoerenti o non rivisti.

## Appendice: focus rapido sullo scopo di ogni script in `ace`

Il runtime è intenzionalmente piccolo, ma ogni script ha un ruolo preciso. Questa appendice è una mappa rapida di chi fa cosa, quando lo fa e perché esiste.

### `generate_ace_agents.js`

- Scopo: renderizzare o verificare i wrapper degli agenti per piattaforma usati per invocare i ruoli ACE.
- Quando: durante l'installazione o ogni volta che cambia la configurazione della piattaforma.
- Perché: assicurare che il progetto ospite abbia gli agenti corretti per il runtime configurato.

### `check_threshold.js`

- Scopo: stabilire se il passaggio successivo deve scattare automaticamente.
- Quando: dopo una sessione, dopo un batch del reflector o dopo un batch del curator.
- Perché: l'apprendimento batch richiede una soglia meccanica, non un'ipotesi. Se la soglia è inferiore a 1, il passaggio viene trattato come "skip" e resta manual-only.

### `update_counters.js`

- Scopo: sommare le evidenze delle trace nei contatori di ciascun bullet attivo.
- Quando: prima di aprire un nuovo batch del reflector e ogni volta che cambiano le evidenze.
- Perché: mantenere il playbook duraturo e la logica live di esclusione allineati ai dati reali di esecuzione.

### `retrieval.js`

- Scopo: generare le `instructions` del runtime a partire dallo stato attivo del `playbook`.
- Quando: dopo una modifica al playbook e prima che una sessione viva consumi il contesto.
- Perché: evitare drift delle istruzioni e mantenere il contesto di sessione derivato dalla fonte di verità revisionata.

### `gate.js`

- Scopo: eseguire la validazione deterministica di un file di decisioni del curator.
- Quando: prima del sign-off umano e prima che qualsiasi scrittura al `playbook` sia consentita.
- Perché: verificare coerenza dello schema, ID duplicati, vincoli di sicurezza semantici ed esistenza delle evidenze.

### `apply_delta.js`

- Scopo: scrivere il batch firmato nel `playbook` e poi rilanciare il retrieval.
- Quando: solo dopo che `gate.js` passa e l'umano firma.
- Perché: questo è l'unico passaggio che modifica la conoscenza duratura del runtime.

### `validate_install.js`

- Scopo: verificare che l'installazione sia strutturalmente completa.
- Quando: dopo l'installazione o prima di un run che assume che il runtime sia pronto.
- Perché: fallire presto in presenza di configurazione mancante o non risolta.

### `inspect_update.js`

- Scopo: confrontare un'installazione esistente con
  `runtime-version.json` e riportare versioni, stati di ownership, conflitti e
  normalizzazioni senza modificare il target.
- Quando: prima di pianificare un aggiornamento e di nuovo dopo la validazione.
- Perché: offrire un inventario deterministico lasciando le decisioni di
  riconciliazione a [UPDATE_PROMPT.md](../UPDATE_PROMPT.md).

Questi script sono volutamente stretti. Non sostituiscono il passaggio di revisione umana e non tutti scrivono stato. Il pattern principale è: raccogli evidenza -> conta evidenza -> proponi -> decidi -> gate -> sign-off umano -> applica -> rigenera le istruzioni.
