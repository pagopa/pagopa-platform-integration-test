# Auto Sync Feature File Documentation

## Introduzione e Finalità

Lo script `create_feature_page.py` ha lo scopo di sincronizzare automaticamente il contenuto di un file `.feature` Gherkin (in lingua italiana) con una pagina Confluence esistente, tramite GitHub Actions. Ad ogni esecuzione, lo script legge il feature file, ne interpreta la struttura riga per riga, costruisce un corpo HTML strutturato e lo carica sulla pagina Confluence corrispondente, sovrascrivendo il contenuto esistente, preservando solo l'header già presente sulla pagina.

Lo script è pensato per mantenere la documentazione dei feature files sempre allineata al codice, senza intervento manuale.

---

## Spiegazione Tecnica del Funzionamento

### 1. Autenticazione
All'avvio, lo script legge e utilizza le credenziali Confluence per costruire un oggetto `HTTPBasicAuth` usato in tutte le chiamate HTTP successive.

### 2. Caricamento dei componenti HTML (`page_components/`)
Prima di elaborare il feature file, lo script legge una serie di template HTML parziali contenuti nella cartella `page_components/`, posizionata nella cartella .github. I template sono file `.txt` con segnaposto (`{placeholder}`) che vengono sostituiti dinamicamente durante la costruzione della pagina:

| File | Scopo |
|---|---|
| `scenario_header.txt` | Intestazione di ogni scenario (titolo + link opzionale); contiene i segnaposto `{scenario_title}` e `{link}` |
| `table_header.txt` | Header della tabella HTML che racchiude gli step del singolo scenario |
| `table_cell.txt` | Cella della tabella HTML per un gruppo di step; contiene il segnaposto `{step}` |
| `step_content.txt` | Singolo step (Given/When/Then/And) formattato; contiene il segnaposto `{step}` |
| `scenario_link.txt` | Blocco link da inserire nell'header dello scenario; contiene i segnaposto `{anchor}`, `{space}`, `{page}` |
| `code_macro.txt` | Macro Confluence per blocco di codice (usata per gli Esempi degli Scenario Outline); contiene il segnaposto `{code_block}` |
| `inline_code.txt` | Template per la formattazione inline del codice; contiene il segnaposto `{inline_code}` |

### 3. Recupero della pagina Confluence esistente
Lo script legge la **prima riga** del feature file per ricavare l'ID della pagina Confluence. Tramite l'API REST v2 di Confluence (`GET /wiki/api/v2/pages/<id>?body-format=storage`), recupera il contenuto corrente della pagina in formato Storage (XHTML), che diventa il punto di partenza su cui viene **accodato** il nuovo contenuto generato. In questo modo l'header esistente sulla pagina viene preservato intatto.

### 4. Parsing del feature file e costruzione del corpo HTML
Lo script scorre il file riga per riga e, in base alla parola chiave che inizia la riga, decide quale blocco HTML aggiungere al contenuto della pagina. L'engine tiene traccia dell'ultimo keyword significativo incontrato (`last_ins`) per gestire i flussi multi-riga (es. una sequenza di step `E` dopo un `Allora`, oppure le righe della tabella degli Esempi).

La logica dei blocchi principali è la seguente:

- **Tag `@...`** → viene estratto l'ID numerico dello scenario (terzo segmento dopo `_`) da utilizzare insieme al titolo del blocco Scenario successivo.
- **`Scenario` / `Scenario Outline`** → apre un nuovo blocco scenario: viene inserito l'header dello scenario (con l'ID e il link, se presenti) e l'intestazione della tabella degli step.
- **`Dato`** → primo step del flusso; viene accodato al buffer `content_to_add` senza ancora chiudere celle (non esiste una cella "precedente").
- **`Quando` / `Allora`** → chiude la cella corrente (flush del buffer), apre la successiva accodando il nuovo step al buffer.
- **`E`** → step di continuazione; viene sempre accodato al buffer corrente senza flush.
- **`Esempi:`** → attiva la modalità raccolta del blocco codice; il contenuto viene accumulato nel buffer.
- **`|`** (pipe) → se si è in modalità `Esempi`, ogni riga della tabella Gherkin viene aggiunta al buffer del blocco codice.
- **Riga vuota o non riconosciuta** → se `last_ins == Allora`, esegue il flush finale della cella e chiude la tabella (`</tr></tbody></table>`); se `last_ins == Esempi`, inserisce il blocco codice Confluence con tutto il contenuto accumulato.

### 5. Sostituzione del codice inline
Prima dell'analisi di ogni riga, lo script applica la regex `<\s*([A-Za-z0-9_]+)\s*>` per trasformare ogni occorrenza nel formato `<valore>` nel corrispondente template di codice inline Confluence, sostituendo il segnaposto `{inline_code}`.

### 6. Upload della pagina aggiornata
Una volta costruito il contenuto completo, lo script lo invia alla pagina Confluence tramite `PUT /wiki/api/v2/pages/<id>`, incrementando di 1 il numero di versione corrente e impostando il messaggio `"Updated feature file content via GitHub Action"`.

---

## Requisiti per il Feature File

Il feature file deve rispettare una struttura rigorosamente definita affinché lo script possa riconoscere e elaborare correttamente tutti i componenti.

### Linee obbligatorie iniziali

- **Prima riga** — deve contenere l'ID della pagina Confluence nel formato `#{idPagina}`. Il carattere `#` e gli spazi vengono rimossi automaticamente dallo script.
  ```
  #3111586225
  ```

- **Seconda riga** — deve riportare il linguaggio utilizzato nel formato `#language:it`. L'esecuzione fallirà se il linguaggio non è italiano (`it`). Questa riga è **obbligatoria**.
  ```
  #language:it
  ```

### Linguaggio e keyword riconosciute

- Il feature file **deve essere scritto in italiano**, almeno per quanto riguarda le keyword Gherkin (Contesto, Scenario, Dato, Quando, Allora, Esempi).
- Lo script riconosce esclusivamente le seguenti keyword:
  - `Contesto:` — sezione preliminare con punti di contesto comuni a più scenario
  - `Scenario` — apre un nuovo blocco scenario
  - `Dato` — step di tipo *Given*
  - `Quando` — step di tipo *When*
  - `Allora` — step di tipo *Then*
  - `E` — step di tipo *And* (continuazione del blocco precedente)
  - `Esempi:` — indica la sezione degli esempi di uno Scenario Outline
  - `|` — riga della tabella degli esempi (riconosciuta solo dopo `Esempi:`)

### Vincoli sulla struttura del file

- **Non utilizzare keyword o pipe come prima parola/carattere della riga** se non in questi contesti specifici:
  - Per i singoli punti della sezione di Contesto
  - Per gli step dello scenario
  - Per la tabella degli Esempi

- **Sezione di Contesto** — se presente, ogni riga di contesto deve iniziare con una variante di `Dato` (`Dato`, `Data`, `Dati`, `Date`) oppure con `E`. Questa sezione viene elaborata e inserita in un blocco di contesto separato sulla pagina Confluence.

### Tag e direttive speciali

- **Suite e scenario ID** — prima della riga del link e dello scenario, inserire un tag nel formato `@SUITE_NNN_NN` (es. `@CUP_001_01`). Il terzo segmento (numero dello scenario) viene estratto e aggiunto al titolo del blocco sulla pagina Confluence.

- **Link a pagina Confluence** — una riga nel formato `#link:{anchor}|{confluence_area_id}|{confluence_page_name}` deve precedere il `Scenario` a cui si riferisce. Inserisce un link cliccabile nell'header dello scenario. I tre valori sono:
  - `{anchor}`: ancora HTML di destinazione della pagina Confluence. **Nota bene**: se l'anchor contiene un emoji (verificabile dall'URL della pagina), l'emoji **deve essere presente** anche all'interno di questo campo.
  - `{confluence_area_id}`: ID o chiave dello space Confluence
  - `{confluence_page_name}`: titolo della pagina Confluence di destinazione

### Formattazione inline del codice

All'interno di qualsiasi step, i valori racchiusi tra parentesi angolari (es. `<nomeVariabile>`) vengono automaticamente formattati come codice inline nel template Confluence. La sintassi supportata è:
```
<[A-Za-z0-9_]+>
```

### Esempio completo di feature file

```
#3111586225                           
#language:it
@CUP_001
Funzionalità: Creazione di una posizione debitoria per CUP

  Contesto:
    Dati ...
    E ...

#----------------------------------------------------------
# Happy Path: flusso di creazione della posizione debitoria
#----------------------------------------------------------

@positivo
@CUP_001_01
#link:📜-Dettaglio-flusso-principale|IQCGJ|[CUP - 2027] UC-01: Creazione Posizione Debitoria
Scenario: Posizione debitoria per CUP creata correttamente
  Dato Il PSP ha ricevuto dalla Corporate un file di input valido che include i dati mandatori  
  E Il file di input contiene una sola chiave di identificazione Ente
  Quando Il PSP Invia la primitiva demandPaymentNotice includendo i dati mandatori
  E Il PSP Invia la primitiva demandPaymentNotice valorizzando un parametro identificativo
  Allora Viene creata correttamente la posizione debitoria
  E La posizione debitoria contiene il campo remittanceInformation: /RFB/{IUV}/CNR/{CF_Debitore}/TXT/Canone Unico Patrimoniale Saldo {anno}
  E La posizione debitoria contiene il campo payment.option.description : Canone Unico Patrimoniale {anno}
  E Il PSP Riceve la risposta demandPaymentNotice res con l'esito della creazione nel formato previsto per l'output
```

### Requisiti per la pagina Confluence

- **La pagina deve esistere** — lo script non crea nuove pagine; recupera e aggiorna una pagina già esistente tramite il suo ID.
- **L'header deve essere già presente sulla pagina** — lo script **preserva** il contenuto già esistente sulla pagina e vi **accoda** il nuovo contenuto generato dal feature file. Tutto ciò che si vuole mantenere fisso (es. titolo, introduzione, badge) deve essere inserito manualmente sulla pagina prima della prima esecuzione.
- **Il tag `h2` non deve essere inserito manualmente nella parte iniziale della pagina** — lo script usa il primo `h2` come delimitatore per capire dove termina la sezione da preservare e da quale punto iniziare a rigenerare il contenuto automatico. Un `h2` aggiunto manualmente in quella sezione può quindi alterare il punto di taglio e compromettere il risultato finale.
- **La pagina deve essere accessibile** — l'account le cui credenziali sono usate (`CONFLUENCE_EMAIL` / `CONFLUENCE_KEY`) deve avere permessi di lettura e scrittura sulla pagina target.
- **Le variabili d'ambiente devono essere configurate** nel workflow GitHub Actions:
  - `CONFLUENCE_EMAIL`: indirizzo email dell'account Atlassian
  - `CONFLUENCE_KEY`: API token dell'account Atlassian

---

## GitHub Action

La GitHub Action viene lanciata automaticamente alla chiusura di una pull request verso il branch `main`, ma è anche eseguibile manualmente tramite il workflow dispatch.

### Flusso di esecuzione

L'action segue i seguenti step:

1. **Specifica delle modalità di esecuzione** — configurazione dell'ambiente e delle opzioni di esecuzione
2. **Specifica dell'environment** — lettura delle variabili di configurazione (credenziali Confluence, ecc.)
3. **Git checkout** — checkout del branch corrente per ottenere le ultime modifiche
4. **Git diff** — identificazione dei file modificati dalla PR, filtrati per estensione `.feature`
5. **Setup dell'ambiente Python** — installazione e configurazione di Python nella runner
6. **Esecuzione dello script Python** — il file `create_feature_page.py` viene eseguito una volta per ogni file `.feature` trovato durante il git diff

---

## Script Python

Lo script `create_feature_page.py` si occupa di estrarre le informazioni dal feature file, recuperare la pagina Confluence da modificare, costruire il nuovo corpo della pagina e pubblicarlo su Confluence.

### Flusso di esecuzione dello script

1. **Creazione dell'oggetto di autenticazione** — lettura delle variabili d'ambiente `CONFLUENCE_EMAIL` e `CONFLUENCE_KEY` per costruire l'oggetto `HTTPBasicAuth`
2. **Recupero del metadata del feature file** — lettura della prima riga per ottenere l'ID della pagina Confluence e della seconda riga per verificare che la lingua sia impostata a italiano
3. **Recupero della pagina Confluence** — esecuzione di una chiamata HTTP GET all'API REST v2 di Confluence per ottenere il body della pagina in formato Storage (XHTML)
4. **Caricamento dei template HTML** — lettura dalla cartella `page_components/` dei file `.txt` contenenti i blocchi XHTML da usare per costruire la pagina
5. **Parsing e costruzione del body** — iterazione riga per riga sul feature file, aggiunta dinamica dei blocchi XHTML appropriati in base al contenuto e ai keyword riconosciuti
6. **Aggiornamento della pagina Confluence** — esecuzione di una chiamata HTTP PUT all'API REST v2 di Confluence per inviare il nuovo body, incrementando il numero di versione della pagina
