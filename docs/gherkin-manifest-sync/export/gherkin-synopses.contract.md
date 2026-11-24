# Contratto del file `.github/gherkin-synopses.json`

Documento da copiare insieme a `gherkin-synopses.template.json` nel repository che consuma il file (QA Central Hub). Il file è l'elenco delle sinossi descrittive dei feature file, una per feature, generate in automatico dal repository `pagopa/pagopa-platform-integration-test` (PQ-845). Il JSON non ammette commenti: le spiegazioni dei campi stanno qui, il modello da copiare sta nel file `.template.json`.

## 1. Dove sta e chi lo scrive

| Cosa | Valore |
|---|---|
| Percorso nel repository sorgente | `.github/gherkin-synopses.json` |
| Chi lo scrive | il workflow `.github/workflows/gherkin-manifest-sync.yml` (script `.github/scripts/gherkin_synopsis.py`), con un commit di `github-actions[bot]` su `main` |
| Chi lo legge | il backend di QA Central Hub, a ogni sincronizzazione, insieme al manifest `.github/gherkin-manifest.yml` |
| Modifiche a mano | solo `synopsis` e `locked` di una voce esistente (vedi sezione 3); mai chiavi, `content_hash` o struttura |
| Codifica | UTF-8 senza BOM, fine riga `\n`, indentazione di 2 spazi, riga finale a capo |

Il file è un dato derivato. Il manifest resta la fonte di quali suite e feature esistono e se sono attive: una sinossi senza voce nel manifest non va mostrata.

## 2. Struttura

```text
{
  "version": 1,
  "prompt_version": "1",
  "suites": {
    "<id suite>": {
      "<id feature>": { "path", "content_hash", "model", "synopsis", "locked" }
    }
  }
}
```

| Campo | Tipo | Obbligatorio | Significato |
|---|---|---|---|
| `version` | intero | sì | versione dello schema; oggi solo `1` |
| `prompt_version` | testo | sì | versione del prompt e della formula del numero di parole con cui sono state generate le voci; cambia quando si rigenera tutto. Il consumatore non la interpreta |
| `suites` | oggetto | sì | chiavi: id delle suite, uguali a `suites[].id` del manifest. Può essere vuoto |
| `suites.<suite>` | oggetto | sì | chiavi: id delle feature, uguali a `features[].id` del manifest nella stessa suite |
| `path` | testo | sì | percorso completo del feature file dalla radice del repository (`root` della suite più `path` della feature). Informativo, per ritrovare il file; l'identità resta la coppia (suite, feature), non il percorso |
| `content_hash` | testo | sì | `sha256:` seguito da 64 cifre esadecimali minuscole. Impronta del testo del feature file senza tag e commenti, unita alla versione del prompt. **Non è lo sha git del file** e non va ricalcolata né confrontata con altri valori: serve solo al generatore per sapere se rigenerare |
| `model` | testo | sì | modello che ha prodotto la sinossi (informativo) |
| `synopsis` | testo | sì | sinossi descrittiva dell'intero feature file, in italiano, su una sola riga, un solo paragrafo, senza elenchi né markdown, senza tag |
| `locked` | booleano | no | presente solo quando è `true`: la voce è stata corretta a mano e il generatore non la tocca più. Assente significa `false` |

Lunghezza di `synopsis`: al massimo `P(n)` parole, dove `n` è il numero di scenari del feature file: `P(n) = min(80, 30 + 50/11 · (n − 1))`, arrotondato per difetto (30 parole con 1 scenario, 80 da 12 scenari in poi). Il consumatore non deve ricalcolarlo né rifiutare una sinossi per la sua lunghezza.

Nessun campo contiene data o ora: così i diff del file restano limitati alle voci davvero cambiate.

## 3. Come intervenire a mano

Per correggere una sinossi: modificare `synopsis` nella voce e aggiungere `"locked": true`. Senza `locked` la correzione verrebbe sovrascritta alla prossima modifica del feature file. Per tornare alla sinossi automatica: togliere `locked` (e, se serve rigenerare subito, cancellare l'intera voce).

## 4. Regole per chi legge il file (consigli per il backend)

| Situazione | Comportamento consigliato |
|---|---|
| File assente | nessuna sinossi per nessuna feature; non è un errore |
| File non è JSON valido, `version` diversa da `1` o forma diversa dalla tabella | trattarlo come un errore di sincronizzazione del solo file delle sinossi: mantenere i dati precedenti e riportare il messaggio; non far fallire il resto della sincronizzazione del manifest |
| Feature del manifest senza voce | nessuna sinossi per quella feature (accade subito dopo aver aggiunto un file, finché il workflow non ha girato, o se la generazione è fallita) |
| Voce senza corrispondente nel manifest | ignorarla |
| Suite o feature con `enabled: false` nel manifest | non mostrare la sinossi |
| Chiavi sconosciute | ignorarle (a differenza del manifest, il file delle sinossi può acquisire campi nuovi senza cambiare `version`, in modo compatibile) |
| Voce con `synopsis` vuota o con i campi obbligatori mancanti | ignorare quella voce e segnalarlo nel log, senza invalidare le altre |

L'identità di una sinossi è la stessa del resto dei dati della feature nel portale: la coppia (id suite, id feature). Se l'id di una feature cambia nel manifest, la sinossi viene rigenerata con il nuovo id alla prima esecuzione utile.

## 5. Esempio minimo

Vedi `gherkin-synopses.template.json`: contiene una suite `my-suite` allineata al modello del manifest (`gherkin-manifest.template.yml`) con due feature, la seconda con `locked: true`. I valori di `content_hash` sono d'esempio e non corrispondono a file reali; i percorsi e le sinossi sono inventati.
