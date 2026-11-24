# PQ-845 - Sincronizzazione automatica del manifest Gherkin e sinossi AI delle feature

Piano di implementazione, scritto per essere eseguito passo per passo anche da un modello con budget ridotto. Non contiene codice: indica cosa creare, con quali regole e come verificare. Ogni passo è autosufficiente e ha un criterio di uscita.

## 1. Obiettivo

Sostituire l'automazione che aggiorna le pagine Confluence dai feature file con un'automazione che mantiene il manifest `.github/gherkin-manifest.yml`, letto da QA Central Hub (Knowledge Base > Gherkin Feature Files).

| Cosa | Esito atteso |
|---|---|
| Nuovo workflow GitHub | A valle di una PR unita su `main`, ma solo se serve (D25: manifest o sinossi mancanti, oppure la PR tocca feature, manifest o sinossi), crea o aggiorna `.github/gherkin-manifest.yml` |
| Nuovo script Python | Legge i `.feature` sotto `src/`, riempie il manifest, rimuove le voci dei file non più presenti |
| Sinossi AI | Per ogni feature attiva del manifest, una sinossi descrittiva globale (lunghezza proporzionale al numero di scenari, al massimo 80 parole, D24) generata con le API Gemini già usate dall'analisi dei report Allure, salvata in un file separato `.github/gherkin-synopses.json` (D15) |
| Workflow Confluence `syncFeatureFile.yaml` | Deprecato e spento: nessun trigger automatico |
| Branch | `PQ-845-gherkin-manifest-sync`, staccato da `main` |

Fuori scope: modifiche a QA Central Hub (altro repository: anche la lettura del file delle sinossi, vedi D15), cancellazione dello script Confluence, modifica dei feature file, i `.feature` sotto `docs/use-cases` (il requisito indica solo `src/`).

## 2. Evidenze raccolte (verificate il 2026-11-20 su `main` allineato a `origin/main`)

### 2.1 Workflow da deprecare

- File: `.github/workflows/syncFeatureFile.yaml`, nome `Sync Feature File between github and confluence`.
- Trigger: `pull_request` (branch `main`, tipo `closed`) e `workflow_dispatch`.
- Fa checkout di `main` con `fetch-depth: 2`, elenca i `.feature` cambiati con `git diff HEAD^ HEAD`, poi lancia `.github/scripts/auto_sync_feature_page.py <file>` per ognuno, con i secret `CONFLUENCE_KEY` e `CONFLUENCE_EMAIL`.
- Non controlla `merged == true`: gira anche sulle PR chiuse senza merge. Il nuovo workflow deve correggere questo difetto.
- Script e documentazione collegati: `.github/scripts/auto_sync_feature_page.py`, `.github/page_components/feature_page/`, `docs/auto sync feature file/Auto sync feature file.md`.
- Da NON toccare: `src/utility/confluence_utils.py` e `.github/workflows/create_report_page.yml` (pubblicano le pagine di report, sono un'altra funzione).
- Il README non descrive il workflow di sync Confluence (la sezione "Pagina report su Confluence" riguarda solo i report).

### 2.2 Precedente da imitare per il trigger e il push

`.github/workflows/bump-suite-version.yml` ha la stessa filosofia: `pull_request` chiusa + `workflow_dispatch`, condizione `github.event.pull_request.merged == true`, checkout di `main`, script Python, poi commit e `git push` diretto fatto da `github-actions[bot]` (permessi `contents: write`). Copiare da lì: struttura, SHA pinnati delle action, identità del bot.

SHA pinnati già in uso (riusarli identici, non scaricare versioni nuove):

- `actions/checkout@f43a0e5ff2bd294095638e18286ca9a3d1956744 # v3`
- `actions/setup-python@7f4fc3e22c37d6ff65e88745f38bd3157c663f7c # v4`

### 2.3 Il manifest

Il template è `C:\Users\dquero\pagopa\pagopa-qa-centralhub\docs\gherkin-feature-files\reference\manifest\gherkin-manifest.template.yml`. La documentazione completa delle regole di validazione sta in `...\gherkin-feature-files\04-manifest-yaml.md` (sezioni 3, 5 e 6). Esiste anche un esempio compilato: `...\reference\manifest\gherkin-manifest.yml` (nello stesso repository centralhub, per sola lettura).

Il backend è severo: un solo errore fa fallire l'intera sincronizzazione e il portale mostra i dati precedenti. Per questo lo script deve validare prima di scrivere.

Regole da implementare (riassunto operativo):

| Campo | Regola |
|---|---|
| radice | solo `version` (intero `1`) e `suites` (lista non vuota, almeno una suite con `enabled` vero) |
| `suites[].id` | `[a-z0-9_-]`, 1-64 caratteri, unico |
| `suites[].label` | facoltativo, 1-100 caratteri |
| `suites[].root` | facoltativo, cartella relativa alla radice del repository, `/` finale ignorato |
| `suites[].enabled` | booleano vero (mai stringa), default `true` |
| `suites[].features` | lista (anche vuota); ogni voce è un blocco |
| `features[].id` | `[A-Za-z0-9_-]`, 1-80 caratteri, unico nella suite ignorando maiuscole/minuscole |
| `features[].path` | relativo a `root`, finisce in `.feature`, senza `/` iniziale, `..`, `//`, `\`, spazi ai bordi; sempre tra virgolette doppie |
| `features[].test_type` | **Non si scrive più (D26).** Oggi il backend lo richiede (`AUTOMATICO` o `MANUALE`): vedi il prerequisito esterno del paragrafo 4 |
| `features[].estimate_days` | facoltativo, numero 0-365 con al massimo 2 decimali |
| `features[].enabled` | booleano, default `true` |
| globale | nessun percorso intero (`root` + `path`) ripetuto, nemmeno tra suite diverse; niente alias YAML; nessuna chiave doppia; massimo 256 KB, UTF-8 |

Ruolo dei campi: `id` della feature più `id` della suite sono l'identità con cui il portale lega i dati scritti a mano (stato, owner, reviewer, link Jira). Cambiare o riusare un id fa perdere il legame. Questo vincola lo script: gli id già presenti non si cambiano mai.

### 2.4 Feature file in `src/` (inventario da cui ricavare i test)

Pattern di scoperta (decisione D13): `src/**/features`, cioè solo i `.feature` che hanno una cartella chiamata esattamente `features` tra la root della suite e il file. Su `main` oggi questo dà 46 file in 12 suite: gli 11 file di `src/integration/fdr3/feature/` (singolare) restano esclusi. Per questo il piano include la rinomina della cartella in `features` (decisione D14, passo R del paragrafo 4.1); a rinomina fatta il risultato è 57 file in 13 suite `src/<tipo>/<nome>` con `tipo` in `api`, `integration`, `e2e`.

| Suite (cartella) | File | Nota |
|---|---|---|
| `src/integration/wisp` | 7 | sottocartelle `features/nodoInviaRPT/` e `features/nodoInviaCarrelloRPT/` |
| `src/e2e/checkout` | 7 | nomi con spazi, es. `FEAT_005_Checkout - Back Navigation Control.feature` |
| `src/integration/fdr3` | 11 (dopo il passo R) | oggi la cartella si chiama `feature/` (singolare) e non rispetta `src/**/features`: va rinominata in `features` |
| `src/integration/fdr` | 10 | nome con apostrofo e accento (`...dell'EC.feature`, `...più pagamenti.feature`) |
| `src/integration/ebollo` | 3 | tutti con primo tag `@eBollo` (collisione) e parola chiave inglese `Feature:` |
| `src/integration/cup` | 1 | |
| `src/integration/tas_fail`, `tas_mixed`, `tas_pass` | 3 + 3 + 3 | suite dimostrative del servizio TAS |
| `src/api/auth-service`, `cart`, `ecommerce-cdc` | 1 + 1 + 1 | |
| `src/api/checkout-npg` | 6 | |

Il registro `.github/nrt-suites.json` contiene solo 3 suite: `wisp` (`WISP`, `src/integration/wisp`), `checkout` (`Checkout E2E`, `src/e2e/checkout`), `fdr3` (`FDR-3`, `src/integration/fdr3`), con i campi `id`, `label`, `behave_path`. Questi id coincidono con il nome della cartella.

Convenzione dei tag: la riga `#<idPaginaConfluence>` e la riga `# language: it` (anche senza spazio: `#language:it`) compaiono in testa ad alcuni file; poi, prima della riga `Funzionalità:` o `Feature:`, ci sono i tag a livello di feature. Il primo di questi è l'id candidato. Casi limite verificati:

- `FEAT_005_FdR3_Recupero degli fdR da parte degli EC.feature` (suite `fdr`): nessun tag prima di `Funzionalità:`, i tag `@runnable`, `@positive`, `@FdR3_005_01` appartengono allo scenario.
- I tre file `ebollo` hanno tutti `@eBollo` come primo tag: id candidato uguale.
- Alcuni tag non sono id validi (es. `@Crea_FdR(id_fdr="...")` ha parentesi e virgolette): vanno scartati se sono i primi.

### 2.5 Workflow e script Gemini per l'analisi dei report (da riusare per le sinossi)

Componenti esistenti, letti il 2026-11-20:

| Componente | Cosa fa | Cosa serve per le sinossi |
|---|---|---|
| `.github/workflows/ai-report-analysis.yml` (`workflow_call` e `workflow_dispatch`) | Due job: `check-model-catalog` interroga `GET /v1beta/models` con il secret `REPORT_ANALYSIS_GEMINI_API_KEY`, filtra la catena di fallback (`gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-pro-preview`, `gemini-2.5-pro`) e produce gli output `available_models` e `model_limits`; `call-inference` scrive un solo prompt su file, lancia `gemini_analysis.py` e carica `analysis.md` e `response.json` come artifact | Non è riusabile con `workflow_call` per le sinossi: restituisce solo un artifact per prompt, quindi servirebbero decine di chiamate (una per feature) e il risultato andrebbe riletto dagli artifact. Si riusa invece il codice Python |
| `.github/scripts/gemini_analysis.py` | Motore generico, importabile (ha `main` protetto): `generate_analysis(prompt, models, max_output_tokens, base_url, api_key, thinking_level, model_limits)` prova i modelli in ordine, riprova una volta sui 429 e 503, scarta i modelli il cui limite di input non basta, ritorna `(modello, risposta, testo)`; `finish_reason(risposta)` segnala `MAX_TOKENS`; `parse_model_limits`, `estimate_tokens`, `format_usage`. Il pensiero dei modelli conta nel limite di output (`thinkingLevel` `low` consigliato) | Riuso diretto di queste funzioni dentro un ciclo sulle feature, senza modificare il file |
| `.github/scripts/build_ai_prompt.py` | Costruisce il prompt dei report a partire da Allure e JUnit | Nessun riuso: i dati sono diversi. Si imita solo lo stile (script con docstring, tetti di dimensione, messaggi `[nome_script]`) |
| Chiamanti | `nrt-main-dispatch-tests.yml`, `checkout-e2e-tests.yml`, `openapi-fdr-tests.yml` usano `uses: ./.github/workflows/ai-report-analysis.yml` con un artifact di prompt | Non vanno toccati |

Parametri da ricordare: il valore predefinito `max_tokens` dei workflow è `32` (serve solo alla demo): per le sinossi servono almeno 1024 token di output, pensiero incluso. Il catalogo dei modelli sta in uno step bash dentro il workflow, non in una funzione Python: il nuovo workflow lo ripete (D22).

### 2.6 Dove salvare le sinossi: confronto (O5)

| Opzione | Pro | Contro | Esito |
|---|---|---|---|
| Campo `synopsis` nel manifest | Un solo file; il backend lo legge già | Il backend rifiuta le chiavi sconosciute: finché non è aggiornato, un solo campo in più fa fallire tutta la sincronizzazione del portale (rilascio da coordinare nei due repository). Prosa generata nel file curato a mano: circa 25 paragrafi fino a 80 parole nei diff; il manifest è rigenerato e riscritto dall'emettitore, che non ha spazio per testo libero; contrasta con la regola del backend «niente dati derivati nel manifest» | Scartata |
| Commento nel `.feature` | Il testo viaggia con il file | Il bot riscrive file scritti dagli analisti (regole di modifica dei feature, id stabili, ADR-46); cambia lo sha del file e ogni modifica richiede un commit su codice di test; un commento non è letto dal backend, quindi serve comunque una modifica lato portale; si mescolano contenuto curato e derivato | Scartata |
| Descrizione Gherkin sotto `Funzionalità:` | Il backend già legge la descrizione dal file | Stessi problemi del commento sul bot che riscrive i feature, e in più sostituisce o confonde la descrizione scritta dall'autore | Scartata |
| File separato `.github/gherkin-synopses.json` | Non rompe nulla se nessuno lo legge; dati derivati separati da quelli curati; cache per hash; diff leggibili; correzione a mano con `locked` | Un file in più; il backend deve imparare a leggerlo; chiave da tenere allineata al manifest (mitigata: lo script legge il manifest e pota le voci morte) | **Scelta (D15)** |
| Generazione lato backend, alla sincronizzazione | Nessun file né commit nel repository; la cache per sha esiste già nel backend; un solo posto per modello e prompt | Chiave Gemini e logica AI nel backend di centralhub; sincronizzazione che oggi è deterministica diventa dipendente da un servizio esterno; non è nel perimetro di questo repository | Alternativa futura se il file separato non basta |
| Pubblicazione su `gh-pages` o come artifact | Nessun commit sul `main` | La cache richiede di rileggere il file precedente da un altro ramo; più parti mobili, nessuna storia delle modifiche nel `main` | Scartata |

## 3. Decisioni di progetto

| # | Decisione | Motivo |
|---|---|---|
| D1 | Il manifest si rigenera sempre dall'intero albero `src/`, non dal diff del commit | Il diff non vede le cancellazioni; la rigenerazione è idempotente e si ripara da sola |
| D2 | Lo script preserva ogni dato scritto a mano nelle voci esistenti (`id`, `estimate_days`, `enabled`, `label`, suite `enabled`) | Sono dati che solo una persona può dare; l'id non si deve mai cambiare |
| D3 | Le voci esistenti si riconoscono per percorso; un file spostato si riconosce per id (stesso id derivato) | Mantiene l'identità nei rename e quindi i dati del portale |
| D4 | Id nuovo = primo tag del file prima di `Funzionalità:`/`Feature:`, senza `@`; se mancante, non valido o in conflitto, nome del file senza estensione ripulito | Convenzione del template, con ripiego deterministico per i file che non la seguono |
| D5 | `estimate_days` delle voci nuove: assente | La stima non è ricavabile dai feature file |
| D6 | Suite nuove: attive solo se presenti in `.github/nrt-suites.json` (per `behave_path` uguale alla loro cartella), altrimenti `enabled: false` con le feature comunque elencate | Allinea l'esempio di centralhub (attive solo le suite del registro, il resto spento); abilitare una suite diventa una riga. Evita di pubblicare per sbaglio le suite dimostrative `tas_*` |
| D7 | Le suite e le voci senza più file vengono rimosse, anche se `enabled: false` | È la richiesta "rimuove le info morte"; il portale cancella da solo le righe non più selezionate |
| D8 | Output scritto da un emettitore proprio, non da `yaml.dump` | Garantisce virgolette doppie sui percorsi, ordine dei campi e diff stabili |
| D9 | I commenti liberi scritti a mano nel manifest non sono preservati | Tradeoff accettato per non aggiungere dipendenze (`ruamel.yaml`); l'intestazione del file lo dichiara; vedi decisione aperta O2 |
| D10 | Lo script valida il risultato con le regole del paragrafo 2.3 prima di scrivere; in caso di errore non scrive e termina con codice 2 | Un manifest invalido bloccherebbe la sincronizzazione del portale |
| D11 | Il workflow committa e pusha direttamente su `main` con `github-actions[bot]`, solo se il file è cambiato | Stesso meccanismo di `bump-suite-version.yml` |
| D12 | Dipendenza: solo `pyyaml` (lettura con `safe_load`), installata nel workflow con `pip install` come negli altri workflow | `requirements.txt` non contiene YAML; non va modificato |
| D13 | Scoperta con il pattern `src/**/features`: sotto la root di ogni suite si considerano solo i `.feature` con un antenato chiamato `features` | Indicazione esplicita di Daniele; esclude `feature/` singolare e i `.feature` fuori da cartelle `features` |
| D14 | Rinominare `src/integration/fdr3/feature` in `src/integration/fdr3/features` con `git mv`, in un commit dedicato, prima dello script | Richiesta di Daniele: porta `fdr3` dentro il pattern D13 senza eccezioni nello script. Il layout diventa uguale a `wisp` (`features/` e `steps/` fratelli) |
| D15 | Le sinossi vivono in un file separato `.github/gherkin-synopses.json`, non nel manifest e non come commento nei `.feature`. Chiave: id della suite e id della feature (la stessa identità del manifest) | Il backend di centralhub rifiuta le chiavi sconosciute del manifest (`features[0] has unknown keys`): aggiungere `synopsis` farebbe fallire l'intera sincronizzazione del portale finché il backend non viene aggiornato. Un file a parte è ignorato finché nessuno lo legge, quindi può uscire prima del consumatore. Separa anche i dati curati a mano (manifest) dai dati derivati (sinossi) e non fa riscrivere dal bot i `.feature` scritti dagli analisti. Confronto nel paragrafo 2.6; decisione aperta O5 |
| D16 | Un nuovo script `.github/scripts/gherkin_synopsis.py` importa `gemini_analysis.py` e lo chiama in ciclo per le sole feature da (ri)generare | Evita una `workflow_call` per feature e non modifica il motore esistente |
| D17 | Una voce si rigenera solo se manca, se l'hash del testo ripulito è cambiato o se è cambiata la versione del prompt, salvo `locked: true`. Hash: `sha256` del testo ripulito preceduto dalla versione del prompt | Costo e rumore minimi, diff stabili; cambiare solo tag o commenti non rigenera nulla; permette di correggere a mano una sinossi bloccandola |
| D18 | Al modello si invia il testo del feature file senza tag e senza commenti (righe che iniziano con `@` e righe che iniziano con `#`, fuori dai blocchi di docstring) | Richiesta di Daniele; evita anche di inviare gli id di pagina Confluence e i link |
| D19 | La sinossi è un solo paragrafo di testo semplice, in italiano, con un numero massimo di parole P(n) che dipende dal numero di scenari (D24, mai oltre 80), globale per il feature file e non scenario per scenario; lo script la valida (parole, righe, markup, risposta troncata) e ritenta una volta con un vincolo più stretto prima di rinunciare | Il modello non rispetta sempre i limiti di lunghezza |
| D20 | Un guasto dell'AI non blocca mai il manifest: lo step delle sinossi ha `continue-on-error: true`; i progressi già ottenuti vengono comunque scritti; senza chiave API lo script esce senza errore | Il manifest è il dato critico per il portale, la sinossi è accessoria |
| D21 | Il prompt sta in `.github/templates/feature-synopsis-prompt.txt` con i segnaposto `{feature_text}` e `{max_words}`; la costante `PROMPT_VERSION` nello script si incrementa a ogni modifica del prompt o della formula D24 | Stesso schema dei template del repository (file di testo con segnaposti); la versione fa rigenerare tutto, in modo voluto |
| D22 | Il passo di scoperta dei modelli Gemini è ripetuto nel nuovo workflow (copia dello step di `ai-report-analysis.yml`) | Non si modifica il workflow esistente usato da altri tre workflow; il rischio è la divergenza della lista di modelli (vedi rischi). Un'azione composita condivisa è un refactor futuro |
| D23 | Si generano sinossi solo per feature con `enabled` vero in suite con `enabled` vero; le voci esistenti di suite o feature spente restano, quelle senza più voce nel manifest si rimuovono | Contiene i costi (25 chiamate alla prima esecuzione sui dati reali, non 57) e vale la stessa regola dei dati morti del manifest |
| D24 | Numero massimo di parole: `P(n) = min(80, 30 + (50/11) * (n - 1))`, con `n` = numero di scenari del feature file (almeno 1) e risultato arrotondato per difetto a un intero | Formula indicata da Daniele: 30 parole per un solo scenario, crescita lineare fino a 80 a partire da 12 scenari. L'arrotondamento per difetto non supera mai il valore della formula. La tabella dei valori è nel paragrafo S.2 |
| D25 | Il workflow parte alla chiusura con merge di una PR su `main` (come `bump-suite-version.yml`), ma un job iniziale di valutazione lascia procedere la sincronizzazione solo se è vero almeno uno di due criteri, in OR: (1) manca il manifest oppure manca il file delle sinossi su `main`; (2) tra i file modificati dalla PR c'è almeno un `.feature` sotto `src/`, oppure il manifest, oppure il file delle sinossi. `workflow_dispatch` salta la valutazione e procede sempre. Il filtro `paths` del trigger non si usa. Gli script e il template del prompt non sono criteri | Evita cicli inutili (checkout, installazioni, chiamate al catalogo Gemini) per le PR che non c'entrano. Il criterio 1 fa da autoguarigione: se manca un file, la prima PR unita lo ricrea, senza aspettare un intervento manuale. `paths` non può esprimere un OR con l'assenza di un file, quindi la valutazione si fa nel workflow. Per modifiche a script o prompt resta il lancio manuale (con `force_synopses` se cambia `PROMPT_VERSION`) |
| D26 | Il campo `test_type` non compare più nel manifest generato: lo script non lo scrive mai. Se un manifest esistente lo contiene (per esempio aggiunto a mano), lo script lo ignora in lettura e non lo riscrive, quindi sparisce alla prima rigenerazione | Richiesta di Daniele. Effetto collaterale: la documentazione di centralhub (`04-manifest-yaml.md`, righe 62 e 202) dichiara `test_type` obbligatorio e il parser lo rifiuta se manca; finché centralhub non lo rende facoltativo o lo toglie, il portale rifiuta il manifest. È un prerequisito esterno (paragrafo 4) |

Stato delle decisioni aperte:

- O1: default D6. Alternativa: attivare tutte le suite scoperte.
- O2: default D9. Alternativa: `ruamel.yaml` per preservare i commenti.
- O3: se `main` fosse protetta e il push del bot fosse rifiutato, passare a una PR automatica (`peter-evans/create-pull-request`, con SHA pinnato da verificare). Si scopre solo alla prima esecuzione reale.
Decisioni confermate da Daniele: O1, O2 e O3 restano ai default indicati. O4 è risolta: la scoperta usa il pattern `src/**/features` (D13) e non include `docs/use-cases`. Daniele ha chiesto anche la rinomina della cartella di `fdr3` (D14). O5 è risolta: le sinossi vanno in un file separato (D15), confermato da Daniele; le alternative scartate sono nel paragrafo 2.6.

## 4. Preparazione

1. Verificare il terminale (PowerShell o Bash) come richiesto da `AGENTS.md`.
2. Partire da `main` aggiornata: `git checkout main`, `git pull --ff-only`.
3. Creare il branch: `git checkout -b PQ-845-gherkin-manifest-sync`. Questo piano (file non tracciato) segue il checkout; includerlo nel primo commit.
4. Leggere, prima di scrivere codice Python: `.github/instructions/python-scripts.instructions.md` (obbligatorio per `AGENTS.md`). Regole rilevanti: docstring in inglese su ogni funzione nuova, annotazioni di tipo sulle API nuove, errori espliciti e distinti (input non valido, esito atteso negativo, guasto tecnico), nessun `valore or default` dove 0, `False` e `""` sono validi.
5. Controllare le README di `src/utility` come richiesto dalla regola di riuso. Atteso: nessuna utility copre manifest o YAML; lo script è tooling CI sotto `.github/scripts` e non importa da `src`.

**Prerequisito esterno (D26).** Il manifest generato non ha `test_type`, ma oggi QA Central Hub lo richiede in ogni feature (errore: `suite 's' features[0] must be a block with 'id', 'path' and 'test_type'`) e la colonna del database non ammette valori nulli. Prima di unire la PR di questo task, centralhub deve accettare voci senza `test_type` (facoltativo con un valore predefinito, oppure rimosso). Il lavoro è fuori da questo repository e va concordato con chi lo mantiene; se non fosse pronto, il manifest verrebbe rifiutato e il portale continuerebbe a mostrare i dati precedenti. L'implementazione di questo piano non dipende da quel lavoro: lo script, i test e il workflow si possono completare comunque.

### 4.1 Passo R - Rinomina della cartella `fdr3` (D14)

Da fare subito dopo la preparazione e prima dello script, così lo script e i suoi test vedono già la struttura finale.

1. Verifica preliminare dei riferimenti: cercare con `git grep` le stringhe `fdr3/feature` e `fdr3\feature` (separatore Windows) in tutto il repository, escluso questo piano. Sul `main` del 2026-11-20 non risultano riferimenti al percorso `src/integration/fdr3/feature` in workflow, script, README, `behave.ini` o file Python della suite; se ne compaiono di nuovi, aggiornarli e citarli nel commit. `.github/nrt-suites.json` non cambia (`behave_path` è la radice `src/integration/fdr3`). Controllare anche la `README.md` dentro `src/integration/fdr3`.
2. Prima della rinomina, annotare la situazione di riferimento con Behave in sola verifica (nessun test vero, nessun servizio esterno): `behave src/integration/fdr3 --dry-run --format plain --no-summary` dalla radice. Annotare il numero di feature (attese 11) e di scenari. Se in locale la verifica non parte (dipendenze mancanti), dirlo nel riepilogo finale invece di saltarla in silenzio. Non lanciare run reali: seguono `.github/instructions/run-tests.instructions.md` e non servono qui.
3. Rinominare con `git mv src/integration/fdr3/feature src/integration/fdr3/features`. Usare `git mv` e non copia più cancellazione, perché la storia dei file resti seguibile; contenuto e nomi dei `.feature` non cambiano. Non toccare `steps/`, `environment.py`, `helper.py` né i file di configurazione della suite.
4. Dopo la rinomina: la cartella `feature` non esiste più, `features` contiene gli 11 file, `git status` mostra solo 11 rinomine. Ripetere il `--dry-run` di Behave e confrontare feature e scenari con il valore annotato: devono coincidere. Behave trova i `.feature` ricorsivamente sotto `src/integration/fdr3` e gli `steps` accanto a `environment.py`, come per `wisp` che ha già `features/` e `steps/` affiancate: la rinomina non dovrebbe cambiare nulla, ma va verificato.
5. Ripetere la ricerca del punto 1: nessun riferimento residuo.
6. Commit dedicato, per esempio `refactor: rename fdr3 feature folder to features`, separato da script e workflow per poterlo annullare da solo.

Effetto sul resto del piano: da qui `fdr3` rientra nel pattern D13 e nel manifest, come suite attiva perché presente nel registro `.github/nrt-suites.json`.

## 5. Passo A - Script `.github/scripts/gherkin_manifest_sync.py`

Il file nuovo vive accanto agli altri script (`.github/scripts/`). Usare solo la libreria standard più `yaml`. Evitare sintassi recente: la versione Python in CI è `3.x`, non esiste un minimo dichiarato.

### A.1 Interfaccia a riga di comando

| Opzione | Default | Effetto |
|---|---|---|
| `--repo-root` | cartella corrente | radice del repository |
| `--manifest` | `.github/gherkin-manifest.yml` | percorso del manifest, relativo alla radice |
| `--registry` | `.github/nrt-suites.json` | registro NRT usato solo per decidere label e attivazione delle suite nuove |
| `--check` | assente | non scrive; codice 1 se il file andrebbe cambiato |
| `--dry-run` | assente | non scrive; stampa il riepilogo |

Codici di uscita: 0 (nessuna modifica necessaria o scrittura riuscita), 1 (solo con `--check`: il manifest non è allineato), 2 (errore: manifest esistente non valido, risultato non valido, I/O). L'ultima riga stampata in caso di errore spiega la causa e il file coinvolto. Una funzione `main` accetta `argv` e restituisce il codice, così i test non lanciano processi.

### A.2 Funzioni (una responsabilità ciascuna, tutte con docstring inglese)

Descrivere i dati scambiati con strutture semplici (dizionari o `dataclass`), non con classi pesanti.

1. **Scoperta dei file.** Per ogni cartella `src/<tipo>/<nome>` con `tipo` in `api`, `integration`, `e2e`, cercare ricorsivamente `*.feature` e tenere solo quelli il cui percorso relativo alla root ha almeno una cartella chiamata esattamente `features` (D13; confronto sensibile alle maiuscole; la cartella `feature` non vale). Ignorare cartelle nascoste e `__pycache__`. Restituire percorsi POSIX relativi a `root`, ordinati senza distinzione di maiuscole. Le cartelle senza feature non producono suite. Conservare i percorsi come restituisce il filesystem (non rinormalizzare gli accenti).
2. **Id di suite.** Nome cartella in minuscolo, caratteri fuori da `[a-z0-9_-]` sostituiti con `-`, massimo 64 caratteri. Se due cartelle producono lo stesso id, usare `<tipo>-<nome>` per entrambe. Se la suite è nel registro NRT (confronto su `behave_path` uguale alla root), usare l'`id` e la `label` del registro.
3. **Lettura del registro.** Se manca o non è JSON, trattarlo come vuoto e avvisare (non è un errore: serve solo per D6).
4. **Id candidato della feature.** Leggere il file in UTF-8 (tollerare il BOM). Scorrere le righe fino alla prima riga che inizia, ignorando maiuscole e spazi, con `Funzionalità:`, `Funzionalita:` o `Feature:`. Nelle righe precedenti, ignorare quelle vuote e quelle che iniziano con `#`; alla prima riga che inizia con `@` prendere il primo token, togliere la `@`. Il candidato è valido solo se rispetta `[A-Za-z0-9_-]{1,80}`. Se non c'è alcun tag prima della parola chiave, o il primo non è valido, non c'è candidato.
5. **Id di ripiego.** Nome del file senza `.feature`; ogni sequenza di caratteri fuori da `[A-Za-z0-9_-]` diventa un solo `_`; togliere `_` ai bordi; massimo 80 caratteri. Mai vuoto: se resta vuoto usare `feature`.
6. **Assegnazione degli id alle voci nuove di una suite.** Prima riservare gli id delle voci esistenti ancora vive, confrontati senza maiuscole. Poi calcolare i candidati di tutte le voci nuove. Un candidato va usato solo se è unico tra le voci nuove e non è riservato; se compare più volte tra le nuove, tutte quelle voci usano l'id di ripiego (comportamento simmetrico, non vince il primo). Se anche l'id di ripiego collide, aggiungere `_2`, `_3`... in ordine di percorso, rispettando il limite di 80 caratteri. Risultato atteso sui dati reali: i tre `ebollo` prendono il nome del file; `FEAT_005_FdR3_Recupero...` prende il nome del file ripulito.
7. **Lettura del manifest esistente.** Se il file non c'è, partire da un manifest vuoto (`version: 1`, nessuna suite). Se c'è, leggerlo con `yaml.safe_load` e validarlo con la funzione del punto 10: se è invalido, terminare con codice 2 senza sovrascrivere (lo deve correggere una persona).
8. **Riconciliazione.** Algoritmo per ogni suite del manifest esistente, nell'ordine in cui compare:
   1. Se la root non esiste sul disco o non contiene più file, la suite è morta: rimuoverla (D7).
   2. Una suite si considera gestita se la sua root è esattamente una cartella `src/<tipo>/<nome>` scoperta al punto 1; altrimenti è manuale (es. aggiunta a mano con altra root): per le manuali si rimuovono solo le voci dei file inesistenti e non si aggiungono voci nuove.
   3. Voci vive: quelle il cui `root/path` esiste. Voci morte: le altre.
   4. Solo per le suite gestite: i file presenti sul disco ma non nel manifest sono nuovi. Prima del conteggio come nuovi, controllare i rename: se l'id candidato di un file nuovo coincide (senza maiuscole) con l'id di una voce morta della stessa suite, la voce morta viene aggiornata al nuovo percorso e tutti i suoi campi restano; il file non è più nuovo.
   5. Le voci nuove ricevono id (punto 6), nessuna stima, `enabled` assente. Il campo `test_type` non si legge e non si scrive (D26): se una voce esistente lo contiene, viene scartato.
   6. Le voci finali sono ordinate per percorso (senza maiuscole). I campi delle voci esistenti restano identici (compresi `enabled: false` e `estimate_days`).
   7. Se la suite resta senza voci, rimuoverla.
   Poi aggiungere in coda le suite scoperte che non corrispondono ad alcuna suite del manifest (per root), ordinate per root, con le regole di D6 (`enabled: false` esplicito se non nel registro; con `label` solo se nel registro). Se un id suite proposto collide con uno già presente, usare `<tipo>-<nome>`; se collide ancora, terminare con codice 2 indicando le due root.
9. **Emissione.** Costruire il testo a mano (non con `yaml.dump`):
   - intestazione commentata fissa: una riga che dice che il file è mantenuto da `.github/workflows/gherkin-manifest-sync.yml` e `.github/scripts/gherkin_manifest_sync.py`; quali campi si possono modificare a mano (`label`, `enabled`, `estimate_days`, `enabled` di suite); l'avviso di non cambiare mai un `id` e di non scrivere commenti dentro il file perché la rigenerazione li perde; il rimando al template di centralhub per l'elenco dei campi. Sintetizzare l'intestazione dal template citato nel paragrafo 2.3, senza copiarlo per intero;
   - `version: 1`, riga vuota, `suites:`;
   - per ogni suite, nell'ordine: `id`, `label` (se presente), `root`, `enabled` (scritto solo quando vale `false`; il valore delle suite esistenti si conserva così com'è letto, quello delle suite nuove segue D6), `features`;
   - per ogni voce, nell'ordine: `id`, `path`, `estimate_days` (se presente), `enabled` (solo se `false`); mai `test_type` (D26);
   - il percorso e la `root` sempre tra virgolette doppie con escape di `\` e `"`, accenti e apostrofi lasciati in chiaro (UTF-8); un valore numerico senza virgolette; booleani come `true`/`false`; riga vuota tra una suite e la successiva;
   - nuove righe `\n`, nessun BOM, riga finale terminata da `\n`. Scrivere il file in modalità binaria per evitare la conversione in CRLF su Windows.
10. **Validazione.** Funzione che applica la tabella del paragrafo 2.3 su una struttura già letta, restituisce l'elenco dei messaggi di errore (vuoto se valida). Controllare anche le dimensioni (256 KB). Eseguirla due volte: sul manifest esistente (punto 7) e sulla struttura finale prima di scrivere. Messaggi in inglese, nello stile del backend, con suite e posizione: es. `suite 'x': the feature id 'A' appears twice`. Includere anche il controllo "almeno una suite attiva" (D6 garantisce wisp e checkout sui dati reali).
11. **Riepilogo.** Stampare righe `[INFO]` con numero di suite e feature, e per ogni modifica: voce aggiunta (suite, id, percorso), rimossa, spostata (vecchio e nuovo percorso), suite aggiunta o rimossa. Stampare `[INFO] manifest unchanged` se nulla cambia. Il testo è pensato per finire nel riepilogo del job.
12. **Scrittura.** Scrivere solo se il contenuto emesso differisce byte per byte dal file esistente. In `--check` e `--dry-run` non scrivere mai.

Proprietà obbligatorie: idempotenza (due esecuzioni consecutive producono lo stesso file), determinismo (stesso input, stesso output su Linux e Windows), nessuna modifica ai file sotto `src/`.

## 6. Passo B - Test `.github/scripts/tests/test_gherkin_manifest_sync.py`

Seguire lo stile di `.github/scripts/tests/test_populate_tables.py`: caricare `gherkin_manifest_sync.py` con `importlib` da percorso, fixture `module` a livello di modulo, docstring inglese in ogni test, uso di `tmp_path` per creare piccoli alberi `src/...` e manifest fittizi. Nessun accesso di rete, nessuna dipendenza oltre a `pytest` e `yaml`.

Casi minimi (uno ciascuno):

| Area | Caso |
|---|---|
| Id candidato | tag prima di `Funzionalità:` letto; con `Feature:` inglese; con righe `#` e vuote in testa; nessun tag prima della parola chiave (tag di scenario ignorati); primo tag con parentesi scartato; file con BOM |
| Id di ripiego | spazi, apostrofi e accenti nel nome diventano `_`; troncamento a 80; mai vuoto |
| Collisioni | tre file con lo stesso primo tag prendono tutti l'id di ripiego; collisione anche di ripiego dà `_2`; candidato uguale (senza maiuscole) a un id esistente |
| Scoperta | ricorsiva sotto `features` (anche sottocartelle, es. `features/a/b.feature`); un `.feature` in `feature/` (singolare) o fuori da `features` è escluso; ignora cartelle nascoste; tipo non ammesso ignorato |
| Suite | id da cartella; collisione di id tra tipi usa il prefisso; label e attivazione dal registro; suite non nel registro `enabled: false`; registro mancante o rotto tollerato con avviso |
| Riconciliazione | manifest assente: creazione completa; file nuovo aggiunto; file cancellato rimosso; file cancellato con `enabled: false` rimosso; rename riconosciuto per id con `estimate_days` e `enabled` preservati; voce esistente con `test_type`: la chiave viene scartata e non riscritta, e una seconda esecuzione non modifica nulla; suite senza più file rimossa; suite manuale (root non gestita) solo potata; dati scritti a mano preservati; ordine delle voci per percorso |
| Emissione | percorsi sempre tra virgolette doppie, anche con spazi, apostrofi, accenti, `\` e `"`; ordine dei campi; `enabled` solo se `false`; fine file con `\n`; il testo emesso, riletto con `yaml.safe_load`, passa la validazione |
| Validazione | una prova per ogni riga della tabella 2.3 (chiave sconosciuta, id fuori pattern, id doppio ignorando maiuscole, percorso con `..`, `\`, `//`, senza `.feature`, chiave `test_type` presente nell'output (non ammessa, D26), stima 365,01 o 3 decimali, percorso intero ripetuto tra suite, nessuna suite attiva) |
| CLI | `--check` con file allineato dà 0 e con file diverso dà 1 senza scrivere; `--dry-run` non scrive; manifest esistente invalido dà 2 e il file resta intatto; due esecuzioni consecutive: la seconda non modifica il file |

Test di non regressione sui dati reali (può essere un solo test marcato in modo da poter essere saltato se `src/` non c'è): sul repository vero, in memoria, lo script produce 13 suite e 57 feature, tutte le voci valide, 3 suite attive (`wisp` 7, `checkout` 7, `fdr3` 11) e 10 spente, id unici in ogni suite, ogni percorso esistente sul disco.

Esecuzione: `python -m pytest .github/scripts/tests/test_gherkin_manifest_sync.py -v` dalla radice del repository. Se `pytest` o `pyyaml` non sono installati, installarli nell'ambiente locale (sono già usati dai test esistenti; questa verifica non richiede alcun servizio esterno). Il file `requirements.txt` non va toccato.

## 7. Passo C - Primo manifest generato

1. Eseguire lo script dalla radice: prima `--dry-run` e leggere il riepilogo (deve elencare 13 suite e 57 feature, tutte "aggiunte").
2. Eseguire senza opzioni: crea `.github/gherkin-manifest.yml`.
3. Verifiche a mano sul file generato:
   - 3 suite attive (`wisp`, `checkout`, `fdr3`) con le label del registro, 10 spente con `enabled: false`; i percorsi di `fdr3` iniziano con `features/`;
   - per `wisp` e `checkout` gli id coincidono con il primo tag e con l'esempio compilato in centralhub (`NodoInviaRPT_NoStamp_001`, `CheckoutBackNavigation_005`, `FEAT_001_Checkout` per `login_availability.feature`);
   - i tre `ebollo` e il file `FEAT_005_FdR3_Recupero...` usano l'id di ripiego e sono unici;
   - nessun percorso ripetuto;
   - i percorsi con spazi, apostrofi e accenti sono tra virgolette doppie.
4. Rieseguire lo script: il manifest non cambia (`unchanged`) e `--check` esce con 0.
5. Commit del manifest: fa parte del primo commit funzionale (il workflow si limita poi ad aggiornarlo).

## 7b. Passo S - Sinossi AI delle feature

Il passo S si fa dopo il primo manifest (passo C): lo script delle sinossi legge il manifest come unica fonte di suite, id e percorsi.

### S.1 File nuovi

| File | Contenuto |
|---|---|
| `.github/scripts/gherkin_synopsis.py` | Script che genera e mantiene le sinossi |
| `.github/templates/feature-synopsis-prompt.txt` | Prompt con i segnaposto `{feature_text}` e `{max_words}` |
| `.github/scripts/tests/test_gherkin_synopsis.py` | Test, senza rete |
| `.github/gherkin-synopses.json` | Dati generati (non si crea a mano; vedi S.5) |

### S.2 Prompt (D21)

Il template è in italiano, in forma di istruzioni, con il feature file in fondo. Contenuto da riprodurre (si può rifinire il lessico, non le regole):

> Sei un analista QA. Di seguito trovi il contenuto di un feature file Gherkin, già privo di tag e commenti.
> Scrivi una sinossi descrittiva dell'intero feature file, non scenario per scenario.
> Regole: al massimo `{max_words}` parole; un solo paragrafo di testo semplice, senza elenchi, titoli, markdown o virgolette; descrivi che cosa verifica la funzionalità nel suo insieme, in quale contesto e con quali esiti attesi, trattando in modo aggregato i casi positivi e negativi; non elencare gli scenari, non citare gli step alla lettera, né identificativi, nomi di tag, valori di test o dati sensibili; scrivi in italiano anche se il file è in inglese; rispondi solo con la sinossi, senza preambolo.
> Feature file: `{feature_text}`

La costante `PROMPT_VERSION` (testo, per esempio `"1"`) parte da `1` e si incrementa a ogni modifica sostanziale del template e a ogni modifica della formula del numero di parole.

Numero di parole (D24). `n` è il numero di scenari del testo ripulito (S.4, punto 2b); `P(n) = min(80, 30 + (50/11) * (n - 1))`, arrotondato per difetto. Se `n` è 0 si usa `n = 1`. Valori attesi (da usare nei test):

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 o più |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P(n) | 30 | 34 | 39 | 43 | 48 | 52 | 57 | 61 | 66 | 70 | 75 | 80 |

(valori esatti prima dell'arrotondamento: 30; 34,55; 39,09; 43,64; 48,18; 52,73; 57,27; 61,82; 66,36; 70,91; 75,45; 80). Per evitare errori di virgola mobile calcolare con interi: divisione intera di `330 + 50 * (n - 1)` per `11`, poi limitare a 80 (equivale alla formula arrotondata per difetto). Nei test confrontare con la tabella, non con la formula riscritta.

### S.3 Interfaccia

| Opzione | Default | Effetto |
|---|---|---|
| `--repo-root` | cartella corrente | radice del repository |
| `--manifest` | `.github/gherkin-manifest.yml` | manifest da leggere (non viene mai modificato) |
| `--synopses` | `.github/gherkin-synopses.json` | file di output |
| `--prompt-template` | `.github/templates/feature-synopsis-prompt.txt` | template del prompt |
| `--max-calls` | `60` | tetto di chiamate AI per esecuzione; le voci restanti si fanno alla prossima |
| `--pause-seconds` | `2` | pausa tra due chiamate, per non saturare le quote |
| `--max-output-tokens` | `1024` | limite di output, pensiero incluso |
| `--thinking-level` | `low` | livello di pensiero |
| `--force` | assente | rigenera anche le voci con hash invariato, ma non quelle con `locked: true` |
| `--dry-run` | assente | non chiama l'API e non scrive: stampa quali voci verrebbero generate, mantenute, rimosse e il testo ripulito della prima |

Variabili d'ambiente (le stesse di `gemini_analysis.py`): `GEMINI_API_KEY`, `AVAILABLE_MODELS` (array JSON), `MODEL_LIMITS` (oggetto JSON, facoltativo), `BASE_URL` (default dell'API v1beta). Codici di uscita: 0 (tutto a posto, anche con nessuna modifica o senza chiave API: in quel caso si stampa `skipped: no GEMINI_API_KEY`), 1 (almeno una feature non è riuscita; il file viene scritto con quanto ottenuto), 2 (errore di configurazione: manifest assente o invalido, template senza segnaposto, `AVAILABLE_MODELS` assente o vuoto con chiave presente).

### S.4 Funzioni (docstring inglese, una responsabilità ciascuna)

1. **Caricamento del motore.** Importare `gemini_analysis` dalla cartella dello script (importazione per percorso come fanno i test esistenti, senza modificare `sys.path` in modo globale permanente). Se l'importazione fallisce, uscire con 2.
2. **Pulizia del testo (D18).** Leggere il file in UTF-8 (tollerare il BOM) e restituire il testo ripulito: eliminare le righe il cui primo carattere non bianco è `#` e quelle il cui primo carattere non bianco è `@`; non toccare nulla dentro i blocchi di docstring (righe delimitate da `"""` o da tre apici inversi), perché lì un `#` o una `@` sono contenuto; rimuovere gli spazi finali, ridurre le righe vuote consecutive a una, togliere le righe vuote a inizio e fine; normalizzare i fine riga a `\n`. Non rimuovere i commenti a fine riga (rari, non richiesti). Attenzione: le righe `|` delle tabelle `Esempi` restano.
2b. **Conteggio degli scenari (D24).** Sul testo già ripulito, contare le righe il cui primo carattere non bianco inizia con una di queste parole chiave seguita da `:`: `Scenario`, `Scenario Outline`, `Scenario Template`, `Schema dello scenario`, `Esempio`, `Example` (confronto senza distinzione di maiuscole). Uno `Scenario Outline` vale 1, non una per riga di `Esempi`; le righe `Esempi:`/`Examples:` e le righe `|` non si contano; gli scenari dentro commenti o docstring non esistono già dopo la pulizia o vanno ignorati (le righe dentro un blocco di docstring non si contano). Restituisce un intero maggiore o uguale a 0. Una seconda funzione, `max_words_for(n)`, applica la formula D24 e restituisce l'intero.
3. **Hash.** `sha256` esadecimale dell'insieme `PROMPT_VERSION`, una riga vuota e il testo ripulito, in UTF-8, con prefisso `sha256:`. Dipende solo da testo e prompt: cambiare tag, commenti o spazi finali non cambia l'hash.
4. **Lettura del file delle sinossi.** Se manca, partire da una struttura vuota. Se esiste ma non è JSON valido o ha una forma diversa dallo schema S.5, uscire con 2 senza sovrascriverlo.
5. **Lettura del manifest.** Con `yaml.safe_load`; usare solo `suites[].id`, `root`, `enabled`, `features[].id`, `path`, `enabled`. Percorso completo del feature: `root` più `path`. Se il manifest è invalido o mancante, uscire con 2. Non duplicare la validazione del manifest: basta una lettura difensiva con messaggi chiari.
6. **Selezione (D17, D23).** Per ogni coppia (suite, feature) attiva: la voce è da generare se manca, se l'hash differisce, se `prompt_version` del file differisce da `PROMPT_VERSION` o se c'è `--force`; non è da generare se `locked` è vero. Il file della feature non esiste: avvisare e saltare. Voci di suite o feature spente: lasciarle intatte. Voci con coppia non più presente nel manifest: da rimuovere. Ordine di lavoro: ordine del manifest; fermarsi a `--max-calls` e dichiarare quante restano.
7. **Costruzione del prompt.** Calcolare `n` e `P(n)` dal testo ripulito. Sostituire `{feature_text}` con il testo ripulito e `{max_words}` con `P(n)`; il template deve contenere entrambi i segnaposto, altrimenti uscire con 2. Se il testo ripulito è vuoto (file senza contenuto) non chiamare l'API: avviso e salto.
8. **Generazione di una voce.** Chiamare `generate_analysis` con i modelli di `AVAILABLE_MODELS`, `--max-output-tokens` e `--thinking-level`. Se la risposta ha `finish_reason` uguale a `MAX_TOKENS`, considerarla non valida. Normalizzare e validare il testo (punto 9). Se non valido, ritentare una sola volta aggiungendo in coda al prompt una riga come `Il tentativo precedente superava il limite o il formato: scrivi al massimo X parole in un solo paragrafo, senza elenchi.` dove X vale `max(20, P(n) - 10)`. Se anche il secondo tentativo è non valido, la voce non cambia (resta la vecchia sinossi se c'era) e si conta un fallimento. Un'eccezione di `generate_analysis` (tutti i modelli falliti) conta come fallimento della voce e non ferma il ciclo; dopo tre fallimenti consecutivi per errori di rete o quota interrompere il ciclo (la quota giornaliera è probabilmente esaurita) e uscire con 1.
9. **Normalizzazione e validazione.** Togliere virgolette o apici che racchiudono l'intero testo, un'eventuale etichetta iniziale tipo `Sinossi:`, riunire le righe in una sola con spazi singoli. Rifiutare: testo vuoto; più di `P(n)` parole, con `n` degli scenari del feature (parole = sequenze separate da spazi); presenza di righe che iniziano con `-`, `*`, `#` o con un numero seguito da punto (elenchi o titoli); presenza di `@` (tag); più di un paragrafo dopo la normalizzazione non è più verificabile, quindi basta il controllo sui marcatori. Nessun troncamento automatico del testo: una sinossi tagliata a metà frase è peggio di nessuna.
10. **Scrittura.** Struttura finale in S.5, con le voci ordinate per id di suite e di feature; `json.dumps` con indentazione di 2 spazi, `ensure_ascii` falso, chiavi nell'ordine fisso dello schema, riga finale a capo, fine riga `\n`, scrittura in modalità binaria. Scrivere solo se il contenuto differisce da quello esistente. Scrivere sempre anche se qualche voce è fallita (i progressi si salvano).
11. **Riepilogo.** Righe `[INFO]` con voci generate, mantenute, bloccate, rimosse, fallite e il numero di chiamate; usare il formato `tee` nel riepilogo del job come per il manifest. Stampare anche il consumo di token con `format_usage` della risposta, se disponibile. Non stampare mai la chiave.

### S.5 Schema del file `.github/gherkin-synopses.json`

```text
{
  "version": 1,
  "prompt_version": "1",
  "suites": {
    "<id suite>": {
      "<id feature>": {
        "path": "<root>/<path>",        informativo, per ritrovare il file
        "content_hash": "sha256:<64 esadecimali>",
        "model": "<modello che ha risposto>",
        "synopsis": "<testo, una riga, al massimo P(n) parole>",
        "locked": true                  presente solo se vero
      }
    }
  }
}
```

Regole: nessun campo con data o ora (renderebbe instabili i diff); `locked: true` si imposta a mano su una voce corretta da una persona e protegge sinossi e hash; chiavi uniche; identità come nel manifest. Modello e contratto da esportare a centralhub: `docs/gherkin-manifest-sync/export/gherkin-synopses.template.json` e `docs/gherkin-manifest-sync/export/gherkin-synopses.contract.md` (già scritti; ogni modifica allo schema qui sopra va riportata anche lì, e la voce di esempio del modello deve restare valida per lo script). Il file è un contratto verso QA Central Hub: la lettura lato backend è un lavoro separato nell'altro repository (fuori scope), che può uscire prima o dopo perché il file non rompe nulla.

### S.6 Test (`test_gherkin_synopsis.py`, stile di `test_populate_tables.py`, senza rete)

Iniettare la funzione di generazione nello script (parametro con default `generate_analysis`) così i test usano un finto generatore. Casi minimi: pulizia (tag e commenti tolti, riga `#language` e id pagina tolti, `@` e `#` dentro docstring conservati, righe vuote ridotte, tabelle `Esempi` conservate); hash invariato al cambiare di soli tag o commenti e variato al cambiare del contenuto o di `PROMPT_VERSION`; selezione (voce nuova, voce invariata, voce con hash diverso, `locked`, suite e feature spente, voce morta rimossa, feature mancante sul disco, tetto `--max-calls`); formula (tutti i valori della tabella S.2 da n = 1 a n = 12, n = 0 trattato come 1, n = 40 limitato a 80); conteggio scenari (`Scenario`, `Scenario Outline` contato una volta con più righe di `Esempi`, `Esempio`, `Example`, righe commentate non contate, righe dentro docstring non contate); validazione (limite uguale a P(n): per un feature con 1 scenario 30 parole accettate e 31 rifiutate, con 12 scenari 80 accettate e 81 rifiutate, elenco, `@`, testo vuoto, etichetta `Sinossi:` rimossa, virgolette rimosse); ritentativo (primo tentativo non valido e secondo valido; entrambi non validi lasciano la voce vecchia); risposta `MAX_TOKENS` rifiutata; tre fallimenti consecutivi interrompono il ciclo con codice 1 dopo aver scritto i progressi; senza chiave: esce con 0 senza scrivere; file delle sinossi invalido: codice 2 e file intatto; emissione deterministica e idempotente; `--dry-run` non chiama il generatore e non scrive. Più un test sui dati reali, marcato come saltabile: sul manifest vero, `--dry-run` seleziona 25 voci (suite attive `wisp` 7, `checkout` 7, `fdr3` 11) e il testo ripulito di nessuna contiene `@` a inizio riga né righe che iniziano con `#`.

Esecuzione: `python -m pytest .github/scripts/tests/test_gherkin_synopsis.py -v`.

### S.7 Prima esecuzione

Il file delle sinossi non va generato a mano in locale: la chiave `REPORT_ANALYSIS_GEMINI_API_KEY` è un secret di GitHub. In locale si verificano solo `--dry-run` e i test. La prima generazione avviene nel workflow: alla chiusura con merge della PR (il file delle sinossi non esiste ancora, quindi il criterio 1 di D25 è vero e la sincronizzazione parte; se il workflow non partisse per la PR che lo introduce, lanciare un `workflow_dispatch`). Dopo la prima esecuzione leggere il file prodotto: ogni sinossi deve rispettare il proprio P(n), essere un paragrafo e descrivere la feature nel suo insieme; se la qualità è scarsa, rifinire il template, incrementare `PROMPT_VERSION` e rilanciare con `force_synopses`.

## 8. Passo D - Workflow `.github/workflows/gherkin-manifest-sync.yml`

Il nome file segue il kebab-case già in uso (`bump-suite-version.yml`). Specifica:

| Elemento | Valore |
|---|---|
| `name` | `Sync Gherkin manifest` |
| `on.pull_request` | `branches: [main]`, `types: [closed]`, nessun filtro `paths` (D25: la valutazione dei criteri si fa nel primo job) |
| `on.workflow_dispatch` | un input booleano `force_synopses` (default `false`): rigenera tutte le sinossi non bloccate |
| `permissions` | Per job, nessun permesso a livello di workflow: `evaluate_trigger` ha `contents: read` e `pull-requests: read`; `sync_gherkin_manifest` ha `contents: write` (l'unico di scrittura) |
| `concurrency` | gruppo `gherkin-manifest-sync`, `cancel-in-progress: false` |
| Job 1 | `evaluate_trigger` su `ubuntu-latest`, `timeout-minutes: 5`, condizione `github.event_name == 'workflow_dispatch' || github.event.pull_request.merged == true`; output `run` (`true` o `false`) e `reason` (testo) |
| Job 2 | `sync_gherkin_manifest` su `ubuntu-latest`, `timeout-minutes: 30`, `needs: evaluate_trigger`, condizione `needs.evaluate_trigger.outputs.run == 'true'` (senza `always()`: se il job 1 è saltato, anche il 2 lo è) |

Passi del job `evaluate_trigger` (D25), nell'ordine:

1. Checkout di `main` con la stessa action pinnata, `ref: main`, `fetch-depth: 1`. Serve solo per controllare l'esistenza dei file nello stato attuale di `main`.
2. Un solo step `id: gate`, con `shell: bash`, che riceve tramite `env` (mai interpolando nel comando): `EVENT_NAME` (`github.event_name`), `PR_NUMBER` (`github.event.pull_request.number`), `REPO` (`github.repository`) e `GH_TOKEN` (`github.token`). Logica, nell'ordine:
   - se `EVENT_NAME` è `workflow_dispatch`: `run=true`, `reason` "esecuzione manuale", fine;
   - criterio 1: se `.github/gherkin-manifest.yml` oppure `.github/gherkin-synopses.json` non esiste: `run=true`, `reason` con il nome del file mancante, fine;
   - criterio 2: scaricare l'elenco dei file della PR con `gh api "repos/$REPO/pulls/$PR_NUMBER/files" --paginate` e `--jq` che stampi, per ogni file, `filename` e, se presente, `previous_filename` (così un `.feature` spostato o rinominato fuori da `src/` conta comunque). Salvare l'elenco in un file temporaneo e cercarvi con `grep -Eq` un nome che corrisponda a `^(src/.+\.feature|\.github/gherkin-manifest\.yml|\.github/gherkin-synopses\.json)$`. Se c'è: `run=true`, `reason` "la PR modifica feature, manifest o sinossi";
   - se la chiamata `gh api` fallisce: `run=true`, `reason` "elenco dei file della PR non disponibile" (si sceglie di sincronizzare nel dubbio: la sincronizzazione è idempotente e senza modifiche non committa);
   - altrimenti `run=false`, `reason` "nessun criterio soddisfatto".
3. Scrivere `run` e `reason` in `$GITHUB_OUTPUT` e una riga con `reason` nel riepilogo del job (`$GITHUB_STEP_SUMMARY`), così in Actions si capisce sempre perché il workflow ha fatto o non ha fatto il lavoro.

Verifica locale della logica di corrispondenza (senza GitHub): passare all'espressione regolare un elenco di nomi di prova e controllare che corrispondano `src/api/wisp/features/a.feature`, `src/integration/fdr3/features/b.feature`, `.github/gherkin-manifest.yml`, `.github/gherkin-synopses.json`, e che non corrispondano `README.md`, `src/utility/rest/client.py`, `docs/use-cases/x.feature`, `.github/scripts/gherkin_manifest_sync.py`, `.github/gherkin-manifest.yml.bak`.

Passi del job `sync_gherkin_manifest`, nell'ordine:

1. Checkout con la stessa action pinnata di `bump-suite-version.yml`, `ref` come in quel workflow (`main` per la PR, `github.ref` per il dispatch), `fetch-depth: 1` (non serve la storia: la rigenerazione è completa).
2. Setup Python con l'action pinnata, `python-version: '3.x'`.
3. Installazione: aggiornare `pip` e installare `pyyaml` (lo script delle sinossi usa solo la libreria standard più `yaml`; `gemini_analysis.py` usa solo la libreria standard).
4. Esecuzione dello script con `shell: bash` esplicito (così `pipefail` è attivo), con l'output copiato nel riepilogo del job (`tee -a "$GITHUB_STEP_SUMMARY"`). Un codice di uscita diverso da 0 fa fallire il job: il workflow non deve mai pushare un manifest non validato.
5. Scoperta dei modelli Gemini (D22): ripetere lo step `Check fallback model availability` di `.github/workflows/ai-report-analysis.yml` (chiamata `GET /models` con `x-goog-api-key`, stessa lista di candidati, stessi due output `available_models` e `model_limits` ricavati con `jq`), con `id: catalog`, chiave presa da `secrets.REPORT_ANALYSIS_GEMINI_API_KEY` passata come variabile d'ambiente dello step. Mettere un commento che rimanda al workflow originale: se si cambia la lista lì, va cambiata anche qui. Lo step ha `continue-on-error: true` (D20).
6. Sinossi: eseguire `python3 .github/scripts/gherkin_synopsis.py` con `shell: bash`, `continue-on-error: true`, output copiato nel riepilogo del job. Variabili d'ambiente: `GEMINI_API_KEY` (dal secret), `AVAILABLE_MODELS` e `MODEL_LIMITS` dagli output di `catalog`, e `FORCE_SYNOPSES` dall'input; l'opzione `--force` si aggiunge solo se `FORCE_SYNOPSES` è `true` (decisione presa dentro lo script bash dello step, mai interpolando input nel comando). Se lo step `catalog` è fallito, `AVAILABLE_MODELS` è vuoto: lo script lo gestisce (esce con 2 senza aver toccato il file), il job prosegue.
7. Commit e push, solo se il manifest o il file delle sinossi sono cambiati: controllare con `git status --porcelain -- .github/gherkin-manifest.yml .github/gherkin-synopses.json` (copre anche i file nuovi non tracciati). Se non è cambiato niente, terminare con successo senza commit. Se è cambiato: configurare `user.name` `github-actions[bot]` e `user.email` `github-actions[bot]@users.noreply.github.com`, `git add` dei due file (solo quelli esistenti), commit con messaggio `chore: sync gherkin manifest and synopses`, `git pull --rebase origin main` per assorbire un eventuale push concorrente (`bump-suite-version.yml` pusha su `main` nello stesso momento di un merge), poi `git push`. Se il push fallisce, il job fallisce (non riprovare in ciclo).

Regole di sicurezza del workflow: nessun valore proveniente dalla PR (titolo, branch, corpo, numero) deve finire dentro un comando `run`: si passa sempre con `env`; l'unico secret usato è `REPORT_ANALYSIS_GEMINI_API_KEY`, solo negli step Gemini (non servono `CONFLUENCE_*`); alle PR chiuse che vengono da fork i secret non sono disponibili: lo script delle sinossi esce senza errore e il manifest viene comunque aggiornato; al feature file inviato a Gemini si applica la pulizia D18 e non si inviano altri dati del repository; il push con `GITHUB_TOKEN` non riattiva altri workflow, quindi non c'è rischio di ciclo.

Il comportamento atteso a regime: la PR che aggiunge, sposta o cancella un `.feature` viene unita, il workflow parte, commit del bot su `main` con il manifest e le sinossi aggiornati (solo le feature nuove o modificate generano chiamate AI); una PR che non tocca feature, manifest o sinossi, con entrambi i file presenti, viene valutata dal job 1 (pochi secondi) e il job 2 viene saltato; se invece manca uno dei due file, qualunque PR unita fa partire la sincronizzazione e lo ricrea; una PR chiusa senza merge non fa nulla (condizione `merged`, nessun job). Il `concurrency` è a livello di workflow: una esecuzione accodata valuta i criteri solo dopo la fine della precedente, quindi vede i file appena committati dal bot.

## 9. Passo E - Deprecazione del workflow Confluence

Modifiche a `.github/workflows/syncFeatureFile.yaml`:

1. Rimuovere il blocco `pull_request` dal `on`. Lasciare `workflow_dispatch` come unica via manuale (utile se serve riallineare una pagina a mano).
2. Cambiare il `name` anteponendo `[DEPRECATED] ` al nome attuale.
3. Aggiungere in testa al file un commento su 3 righe: workflow deprecato da PQ-845, sostituito da `gherkin-manifest-sync.yml`, la rimozione di workflow e script è prevista in una PR successiva.
4. Non modificare passi, permessi o secret: lo scopo è spegnere il trigger, non rifattorizzare.

Modifiche di documentazione sul codice deprecato (senza cambiare il comportamento):

- `.github/scripts/auto_sync_feature_page.py`: aggiungere in testa un commento breve di deprecazione con il rimando al nuovo workflow. Va rispettata la regola Python di `AGENTS.md` (leggere le istruzioni Python prima di editare): non toccare altro, non aggiungere docstring a funzioni non modificate.
- `docs/auto sync feature file/Auto sync feature file.md`: aggiungere in cima un avviso `> Deprecato (PQ-845)` che spiega che l'aggiornamento automatico delle pagine Confluence è spento e rimanda a `docs/gherkin-manifest-sync/implementation-plan.md` e alla sezione README nuova. Il resto del documento resta invariato come riferimento storico.

Fuori dal repository (da segnalare a Daniele, non da fare qui): disattivare il workflow dalla UI di GitHub Actions è facoltativo dopo il merge; i secret `CONFLUENCE_KEY` e `CONFLUENCE_EMAIL` restano perché usati da `create_report_page.yml`.

## 10. Passo F - README (ADR-11)

Dopo l'ultimo cambio, applicare la skill `.github/skills/ppa-readme/SKILL.md` una sola volta per l'insieme delle modifiche (regola di `AGENTS.md`). Contenuti attesi, da verificare con la skill e non da copiare alla lettera:

- sezione "Struttura del repository": aggiungere `.github/gherkin-manifest.yml` e `.github/scripts/gherkin_manifest_sync.py` nel blocco `.github/` (l'albero attuale elenca solo `workflows/`, `scripts/`, `templates/`, `html/`);
- sezione "Esecuzione in CI": nuovo paragrafo "Manifest Gherkin" con trigger, effetto, come rigenerare in locale (`python .github/scripts/gherkin_manifest_sync.py`, con `--check` e `--dry-run`), cosa si può modificare a mano nel manifest e il rimando al template di centralhub;
- nello stesso paragrafo: le sinossi AI (cosa sono, dove stanno, che cosa viene inviato a Gemini, `locked`, `PROMPT_VERSION`, come rigenerarle con `force_synopses`, il comando `--dry-run` locale) e il riferimento al contratto del file `.github/gherkin-synopses.json`;
- una riga che segnali il workflow Confluence di sync come deprecato e spento (oggi il README non lo cita; non servono altre correzioni);
- "Tracciabilita delle fonti": aggiungere i nuovi file, se la sezione elenca i riferimenti per workflow.

Un esito "nessun aggiornamento" non è accettabile qui: i file nuovi cambiano il comportamento della CI.

## 11. Ordine di esecuzione e criteri di uscita

| Passo | Contenuto | Uscita |
|---|---|---|
| 0 | Preparazione (paragrafo 4) | Branch `PQ-845-gherkin-manifest-sync` creato da `main`, piano nel working tree |
| R | Rinomina `fdr3` (paragrafo 4.1) | Cartella `features` presente, `feature` assente, 11 rinomine in `git status`, nessun riferimento residuo, dry-run Behave invariato |
| 1 | Script (paragrafo 5) | Script completo, `--dry-run` sul repository vero termina con 0 e riepilogo coerente |
| 2 | Test (paragrafo 6) | Tutti i test verdi, compreso il caso sui dati reali (13 suite, 57 feature) |
| 3 | Primo manifest (paragrafo 7) | `.github/gherkin-manifest.yml` presente, seconda esecuzione senza modifiche, `--check` con codice 0 |
| S | Sinossi (paragrafo 7b) | Template, script e test creati; test verdi; `--dry-run` sul manifest vero seleziona 25 voci; nessuna chiamata AI in locale |
| 4 | Workflow nuovo (paragrafo 8) | File YAML valido: controllare la sintassi (es. `python -c "import yaml; yaml.safe_load(open(...))"`) e rileggere trigger, permessi per job, condizione `merged`, `needs` e le uscite del job di valutazione; provare le corrispondenze del paragrafo 8 |
| 5 | Deprecazione (paragrafo 9) | `syncFeatureFile.yaml` senza `pull_request`, nome con `[DEPRECATED]`; script e doc con avviso |
| 6 | README (paragrafo 10) | Skill `ppa-readme` applicata, sezioni aggiornate |
| 7 | Chiusura | `git status` pulito rispetto all'elenco file di questo piano (paragrafo 12); sotto `src/` risulta modificata solo la rinomina di `fdr3` |

Un commit per passo logico (rinomina `fdr3`, script e test del manifest, manifest, script e test delle sinossi, workflow, deprecazione, README) con messaggi Conventional Commits in inglese, minuscoli, all'imperativo, per esempio `refactor: rename fdr3 feature folder to features`, `feat: add gherkin manifest sync script`, `feat: add feature synopsis generation with gemini`, `feat: add gherkin manifest sync workflow`, `chore: deprecate confluence feature sync workflow`, `docs: document gherkin manifest sync`. Commit, push e PR solo su richiesta esplicita di Daniele; per la PR usare la skill `.github/skills/ppa-pr/SKILL.md`. Se l'esecuzione avviene tramite agenti ACE, il task di tracciamento segue le regole di `AGENTS.md` (addon di privacy prima di committare le trace).

## 12. File toccati

| File | Azione |
|---|---|
| `src/integration/fdr3/feature/*.feature` (11 file) | spostati in `src/integration/fdr3/features/` con `git mv`, contenuto invariato |
| `.github/scripts/gherkin_manifest_sync.py` | nuovo |
| `.github/scripts/tests/test_gherkin_manifest_sync.py` | nuovo |
| `.github/gherkin-manifest.yml` | nuovo (generato dallo script) |
| `.github/scripts/gherkin_synopsis.py` | nuovo |
| `.github/scripts/tests/test_gherkin_synopsis.py` | nuovo |
| `.github/templates/feature-synopsis-prompt.txt` | nuovo |
| `.github/gherkin-synopses.json` | nuovo, generato dal workflow alla prima esecuzione (non committato nella PR) |
| `.github/workflows/gherkin-manifest-sync.yml` | nuovo |
| `.github/workflows/syncFeatureFile.yaml` | modificato (trigger spento, nome, commento) |
| `.github/scripts/auto_sync_feature_page.py` | modificato (solo commento di deprecazione) |
| `docs/auto sync feature file/Auto sync feature file.md` | modificato (solo avviso in testa) |
| `README.md` | modificato (paragrafo 10) |
| `docs/gherkin-manifest-sync/implementation-plan.md` | questo piano |
| `docs/gherkin-manifest-sync/export/gherkin-synopses.template.json` | già creato: modello del file delle sinossi, da esportare a centralhub; non va modificato dall'implementazione salvo se cambia lo schema S.5 |
| `docs/gherkin-manifest-sync/export/gherkin-synopses.contract.md` | già creato: contratto del file (campi, regole di lettura), da esportare insieme al modello; va tenuto allineato a S.5 |

Non toccare: `src/**` (salvo la rinomina di `fdr3`), `requirements.txt`, `src/utility/confluence_utils.py`, `.github/workflows/create_report_page.yml`, `.github/nrt-suites.json`, `.github/workflows/ai-report-analysis.yml` e `.github/scripts/gemini_analysis.py` (si riusano senza modifiche), il repository `pagopa-qa-centralhub`.

## 13. Rischi e trappole note

| Rischio | Mitigazione |
|---|---|
| `main` protetta rifiuta il push del bot | Il precedente `bump-suite-version.yml` indica che il push diretto funziona; se non fosse così, vedere O3 |
| Manifest invalido blocca il portale | Validazione prima della scrittura, manifest esistente invalido ferma lo script (codice 2) senza sovrascrivere |
| Id che cambia e il portale perde i dati scritti a mano | Gli id esistenti non si toccano mai (D2); rename riconosciuto per id (D3) |
| Collisione `@eBollo` e simili | Regola simmetrica del punto A.2.6; verificata dal test sui dati reali |
| Percorsi con accento o apostrofo | Emissione in UTF-8 con virgolette doppie; test dedicato; non rinormalizzare Unicode |
| CRLF su Windows | Scrittura binaria con `\n`; verificare che `git` non segnali l'intero file come modificato |
| Corsa tra `bump-suite-version.yml` e il nuovo workflow su `main` | `concurrency` e `git pull --rebase` prima del push |
| Commenti scritti a mano persi alla rigenerazione | Dichiarato nell'intestazione del manifest (D9); alternativa in O2 |
| Lista dei modelli Gemini copiata nel nuovo workflow che diverge da quella di `ai-report-analysis.yml` | Commento di rimando in entrambi i punti; refactor futuro in azione composita (D22) |
| Quota Gemini esaurita o modello non disponibile | Catena di fallback del motore esistente; tre fallimenti consecutivi fermano il ciclo; le voci già generate si salvano; il manifest non ne risente (D20) |
| Sinossi troppo lunga (con P(n) basso, per esempio 30 parole per un solo scenario, il modello sfora più spesso), non pertinente o con riferimenti a tag | Validazione e un solo ritentativo con limite più stretto; nessun troncamento; se i fallimenti sono frequenti, regolare il prompt o aggiungere una tolleranza esplicita (decisione di Daniele); `locked` per le correzioni a mano; `PROMPT_VERSION` per rigenerare tutto |
| Contenuto dei feature inviato a un servizio esterno | Il repository è lo stesso i cui report vanno già a Gemini; si inviano solo testo senza tag e commenti; controllare a campione che nei feature non ci siano segreti prima della prima generazione |
| Prima esecuzione più lunga del previsto | 25 chiamate sui dati reali, pausa di 2 secondi, `timeout-minutes: 30`, tetto `--max-calls`; le voci restanti si fanno alla esecuzione successiva |
| Il backend di centralhub richiede ancora `test_type` e rifiuta il manifest (D26) | Concordare prima la modifica a centralhub (paragrafo 4); fino ad allora non unire la PR su `main`, o lasciare il portale sui dati precedenti. Il rifiuto non rompe il portale: mostra l'ultima sincronizzazione riuscita |
| Una PR che sposta solo cartelle senza toccare `.feature` | Il criterio 2 non scatta e non serve: il manifest non cambia; `workflow_dispatch` permette il riallineamento manuale |
| Modifica a script, template o `PROMPT_VERSION` senza altre modifiche rilevanti | Non è un criterio (D25): lanciare a mano `workflow_dispatch`, con `force_synopses` se serve rigenerare tutto; altrimenti la rigenerazione scatterebbe alla prima PR successiva che tocca un feature, con un picco di chiamate |
| Un file resta assente per sempre (per esempio manca la chiave Gemini, quindi lo script delle sinossi esce senza scrivere) | Il criterio 1 resta vero e ogni PR unita fa partire la sincronizzazione: costo accettato (pochi minuti, nessun commit se non cambia nulla); si risolve fornendo la chiave |
| L'elenco dei file della PR è molto lungo | L'API restituisce al massimo 3000 file; oltre, o se la chiamata fallisce, si sincronizza nel dubbio (D25) |
| Il push del bot può riattivare il workflow? | No: i push con `GITHUB_TOKEN` non scatenano altri workflow e comunque il trigger è la chiusura di una PR, non un push |

## 14. Criteri di accettazione finali

1. `python .github/scripts/gherkin_manifest_sync.py --check` esce con 0 dopo la prima generazione e con 1 dopo aver aggiunto o cancellato un `.feature` di prova (da annullare subito).
2. Cancellando un file di prova, la sua voce sparisce; ricreandolo con lo stesso primo tag in un'altra cartella, il nuovo percorso eredita id e stima.
3. Il manifest passa tutte le regole del paragrafo 2.3 (verificato dai test) e riporta 13 suite, 57 feature, 3 suite attive, e non contiene mai la chiave `test_type` (D26).
4. `syncFeatureFile.yaml` non ha più trigger automatici; `gherkin-manifest-sync.yml` ha trigger `pull_request` chiusa su `main` senza filtro `paths`, con `merged`, e `workflow_dispatch`; il job `evaluate_trigger` lascia procedere solo con i criteri di D25 (file mancante, oppure PR con feature, manifest o sinossi), il job di sincronizzazione ha `needs` su di esso.
5. Nessun file fuori dall'elenco del paragrafo 12 è modificato; `git diff --stat -M` mostra la rinomina di `fdr3` come 11 spostamenti al 100% di somiglianza.
6. Il file delle sinossi, dopo la prima esecuzione, ha una voce per ognuna delle 25 feature attive, ciascuna con al massimo P(n) parole (30 per un solo scenario, 80 da 12 scenari) e nessun `@` né elenchi; una seconda esecuzione senza modifiche ai feature non fa nessuna chiamata AI e non cambia il file; cambiando solo un tag o un commento in un `.feature` la voce non si rigenera; con Gemini non raggiungibile il manifest viene comunque aggiornato e committato.
7. Dopo il merge: verificare in Actions, con tre PR di prova unite su `main` (o ragionando sui log se non è possibile), che una PR che tocca solo `README.md` con entrambi i file presenti salti il job 2 (`reason`: nessun criterio soddisfatto), che una PR che tocca un `.feature` lo esegua e che, rimuovendo a mano un file dei due, qualunque PR lo esegua. Poi prima esecuzione manuale (`workflow_dispatch`) per verificare il push del bot, poi controllo nel portale (variabili `GHERKIN_REF` e `GHERKIN_MANIFEST_PATH` del backend di centralhub, fuori da questo repository).
