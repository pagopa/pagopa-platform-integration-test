# Contratto del file `.github/gherkin-synopses.json`

Documento da copiare insieme a `gherkin-synopses.template.json` nel repository che consuma il file (QA Central Hub). Il file è l'elenco delle sinossi descrittive dei feature file, una per feature, generate dal repository `pagopa/pagopa-platform-integration-test` (PQ-845) e correggibili tramite PR. Il JSON non ammette commenti: le spiegazioni dei campi stanno qui, il modello da copiare sta nel file `.template.json`.

## 1. Dove sta e chi lo scrive

| Cosa | Valore |
|---|---|
| Percorso nel repository sorgente | `.github/gherkin-synopses.json` |
| Chi lo scrive | il workflow `.github/workflows/gherkin-manifest-sync.yml` (script `.github/scripts/gherkin_synopsis.py`) propone le modifiche in una PR cumulativa; arrivano su `main` solo dopo la revisione e il merge |
| Destinatario previsto | il backend di QA Central Hub, insieme al manifest `.github/gherkin-manifest.yml`; l'integrazione va verificata |
| Modifiche a mano | solo `synopsis` di una voce esistente, tramite PR anche da QA Hub (vedi sezione 3); mai chiavi, `content_hash` o struttura |
| Codifica | UTF-8 senza BOM, fine riga `\n`, indentazione di 2 spazi, riga finale a capo |

Il file è un dato derivato. Il manifest elenca le suite e le feature esistenti; stato e stime sono gestiti da QA Central Hub. Una sinossi senza voce nel manifest non va mostrata.

## 2. Struttura

```text
{
  "version": 1,
  "prompt_version": "1",
  "suites": {
    "<id suite>": {
      "<id feature>": { "path", "content_hash", "model", "synopsis", "prompt_version" }
    }
  }
}
```

| Campo | Tipo | Obbligatorio | Significato |
|---|---|---|---|
| `version` | intero | sì | versione dello schema; oggi solo `1` |
| `prompt_version` | testo | sì | versione predefinita del prompt con cui sono state generate le voci prive di un proprio `prompt_version`. Il consumatore non la interpreta |
| `suites` | oggetto | sì | chiavi: id delle suite, uguali a `suites[].id` del manifest. Può essere vuoto |
| `suites.<suite>` | oggetto | sì | chiavi: id delle feature, uguali a `features[].id` del manifest nella stessa suite |
| `path` | testo | sì | percorso completo del feature file dalla radice del repository (`root` della suite più `path` della feature). Serve a ritrovare il file e a conservare la sinossi quando cambia l'ID della feature; l'identità pubblicata resta la coppia (suite, feature) |
| `content_hash` | testo | sì | `sha256:` seguito da 64 cifre esadecimali minuscole. Impronta del testo utile della feature e della versione del prompt di riferimento. Dopo una modifica esplicita alla sinossi, il generatore propone di allinearla al testo della feature alla testa di quella PR, senza riscrivere la sinossi; la nuova impronta arriva su `main` con il merge della PR di sincronizzazione. **Non è lo sha git del file**: il consumatore non deve ricalcolarla né confrontarla |
| `model` | testo | sì | ultimo modello usato per la generazione automatica; resta informativo anche dopo una correzione umana |
| `synopsis` | testo | sì | sinossi descrittiva dell'intero feature file, in italiano, su una sola riga, un solo paragrafo, senza elenchi né markdown, senza tag. Una stringa vuota o composta solo da spazi è considerata mancante |
| `suites.<suite>.<feature>.prompt_version` | testo | no | versione del prompt per questa voce, se diversa da quella predefinita del documento. Il consumatore non la interpreta |

Lunghezza di `synopsis`: al massimo `P(n)` parole, dove `n` è il numero di scenari del feature file: `P(n) = min(80, 30 + 50/11 · (n − 1))`, arrotondato per difetto (30 parole con 1 scenario, 80 da 12 scenari in poi). Il consumatore non deve ricalcolarlo né rifiutare una sinossi per la sua lunghezza.

Nessun campo contiene data o ora: così i diff del file restano limitati alle voci davvero cambiate.

## 3. Come intervenire a mano

Per correggere una sinossi: modificare soltanto `synopsis` nella voce e aprire una PR. Il flusso previsto per QA Hub consente a un utente abilitato di correggere il testo dall'hub e proporre la modifica tramite PR; dopo il merge, l'hub recupera il testo pubblicato nel repository.

Il generatore confronta le singole voci tra merge-base e testa della PR. Se il testo di una sinossi cambia, esclude dalla generazione AI la feature corrispondente, anche quando la PR cambia anche il feature file. Una PR che modifica soltanto una sinossi non la fa rigenerare. Le altre feature della stessa PR restano eleggibili: modificare il JSON non le esclude tutte. Cambiare soltanto metadati o formattazione del JSON non equivale a modificare il testo della sinossi.

Se un'esecuzione accodata riguarda una PR precedente a una correzione umana già pubblicata su `main`, conserva la correzione invece di sovrascriverla. Se il branch cumulativo contiene già una sinossi per una modifica della feature successiva a quella correzione, una vecchia esecuzione non la annulla. La cronologia delle PR e dei commit GitHub permette di distinguere una correzione da un output AI pubblicato successivamente, anche se la PR automatica è stata unita con squash; se la provenienza non è verificabile, la sincronizzazione si ferma. Anche una correzione presente sul branch della PR cumulativa è preservata; se è incompatibile con una correzione pubblicata, la sincronizzazione si ferma per la risoluzione manuale.

La precedenza vale per quella PR, non è un blocco permanente. Una successiva PR che modifica soltanto il testo utile della feature può rigenerare la sinossi. Un testo svuotato o una voce rimossa nella PR non vengono ricreati nella stessa esecuzione; in una successiva sincronizzazione sono considerati mancanti. Il vecchio campo `locked` non ha più effetto e non viene ripubblicato dal generatore.

## 4. Regole per chi legge il file (consigli per il backend)

| Situazione | Comportamento consigliato |
|---|---|
| File assente | nessuna sinossi per nessuna feature; non è un errore |
| File non è JSON valido, `version` diversa da `1` o forma diversa dalla tabella | trattarlo come un errore di sincronizzazione del solo file delle sinossi: mantenere i dati precedenti e riportare il messaggio; non far fallire il resto della sincronizzazione del manifest |
| Feature del manifest senza voce | nessuna sinossi per quella feature (accade subito dopo aver aggiunto un file, finché la PR di sincronizzazione non è stata unita, o se la generazione è fallita) |
| Voce senza corrispondente nel manifest | ignorarla |
| Stato e visibilità della suite o feature | applicare le regole e i dati gestiti da QA Central Hub, senza ricavarli dal manifest |
| Chiavi sconosciute | ignorarle (a differenza del manifest, il file delle sinossi può acquisire campi nuovi senza cambiare `version`, in modo compatibile) |
| Voce con `synopsis` vuota o composta solo da spazi, o con i campi obbligatori mancanti | ignorare quella voce e segnalarlo nel log, senza invalidare le altre |

L'identità pubblicata di una sinossi è la stessa del resto dei dati della feature nel portale: la coppia (id suite, id feature). Se l'ID cambia nel manifest, il generatore riassocia la voce usando la stessa suite e lo stesso percorso. Salvo le esclusioni per modifica esplicita descritte sopra, genera le sinossi mancanti di tutte le suite e rigenera una voce esistente solo se il testo della feature senza tag e commenti cambia nella PR. Un cambio di prompt da solo non causa rigenerazioni.

## 5. Esempio minimo

Vedi `gherkin-synopses.template.json`: contiene una suite `my-suite` allineata al modello del manifest (`gherkin-manifest.template.yml`) con due feature. I valori di `content_hash` sono d'esempio e non corrispondono a file reali; i percorsi e le sinossi sono inventati.
