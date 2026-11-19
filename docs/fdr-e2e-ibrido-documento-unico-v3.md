# FDR e2e ibrido: documento unico per UC, feature e implementazione (v3)

| Campo | Valore |
| --- | --- |
| Jira | PQ-827 |
| Branch | `PQ-827-fdr-e2e-test-design` |
| Stato | bozza di lavoro: riunisce in un solo testo il razionale funzionale, i dati tecnici e la mappa dei riferimenti degli UC (tutti nella versione 3) e li collega alle feature; per leggere UC e feature, scrivere il codice e mantenere i dati |
| Ambiente | UAT, l'unico trattato |
| Data | 19/11/2026 |
| UC | [UC-FDR-001-v3](use-cases/UC-FDR-001-v3.md) e [UC-FDR-002-v3](use-cases/UC-FDR-002-v3.md) |
| Feature | [FEAT_001](use-cases/features/fdr-hybrid/FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature) e [FEAT_002](use-cases/features/fdr-hybrid/FEAT_002_FdRHybrid_Invio_FDR1_e_recupero_FDR3.feature), bozze del 19/11/2026 |
| Documenti fusi | [razionale funzionale v3](fdr-e2e-ibrido-01-razionale-uc-v3.md), [dati tecnici v3](fdr-e2e-ibrido-02-dati-tecnici-v3.md) e [mappa dei riferimenti](use-cases/mappa-riferimenti-UC-FDR-v3.md), non modificati dalla fusione |

## Premesse

Il dominio FDR (Flussi di Rendicontazione) vive una fase di transizione: la modalità storica (FDR1) convive con quella nuova (FDR3), perché PSP ed EC non possono migrare tutti nello stesso momento. A tenere allineate le due modalità lavorano due convertitori, uno per direzione. Il task chiede scenari e2e che dimostrino un fatto semplice da enunciare e meno da verificare: un flusso scritto con una modalità deve essere letto, completo e corretto, con l'altra.

Questo documento riunisce in un solo testo i tre che lo precedono: il razionale funzionale, i dati tecnici e la mappa dei riferimenti degli UC. In più collega ogni voce degli UC agli step delle due feature. Descrive solo ciò che serve a capire la funzionalità e a eseguire UC-FDR-001 e UC-FDR-002 con FEAT_001 e FEAT_002.

Assunzioni:

- l'ambiente è UAT;
- il test percorre le API che PSP ed EC usano davvero, senza frontend e senza scorciatoie verso i componenti interni: è black-box;
- le regole derivano dalla documentazione fornita e dai contratti pubblicati. Non sono state eseguite chiamate verso gli ambienti né risolti segreti, quindi nulla di quanto segue è un comportamento osservato: ogni comportamento atteso va verificato alla prima esecuzione approvata;
- le voci marcate "proposta" sono scelte del redattore e non vincolano;
- gli identificativi R, VAR, VG, QF, DM, RI, DV, DT e FT sono quelli dei documenti di origine. I registri dei run in `docs/use-cases/workflow-runs/fdr-e2e-ibrido` li citano, quindi non sono consecutivi.

### Riservatezza dei dati

Il documento non contiene segreti né valori di configurazione. Dove le fonti riportavano identità di test, nomi di segreti, host o dati anagrafici, qui compare un segnaposto. Restano in chiaro i dati pubblici (contratti e repository `pagopa-api`, con il commit di riferimento) e quelli non identificativi (importi, esiti, indici, date di esempio). Lunghezze e vincoli di formato dei dati omessi restano documentati (§10.6), perché servono a costruire flussi validi.

| Segnaposto | Che cosa sostituisce | Dove si trova il valore |
| --- | --- | --- |
| `<CODICE_PSP>`, `<INTERMEDIARIO_PSP>`, `<CANALE_PSP>` | identità di test del PSP | sezione `global_configuration` di `src/integration/fdr3/uat.yaml` |
| `<CODICE_EC>`, `<INTERMEDIARIO_EC>`, `<STAZIONE_EC>` | identità di test dell'EC | come sopra |
| `<PASSWORD_CANALE>`, `<PASSWORD_STAZIONE>` | password di canale e di stazione | segreti della suite, risolti con il meccanismo del repository (sezione Configurazione del [README](../README.md)) |
| `<CHIAVE_SOTTOSCRIZIONE>` | chiavi di sottoscrizione dei gateway REST e SOAP; i nomi dei segreti e delle variabili che le contengono sono omessi | come sopra |
| `<HOST_API_UAT>`, `<HOST_UPLOAD_UAT>` | host dei gateway UAT | sezioni `fdr` e `psp` della configurazione di fdr3 (`<HOST_API_UAT>`); `<HOST_UPLOAD_UAT>` è il dominio alternativo citato da FT-03 (DM-13) |
| `<ID_MITTENTE>`, `<NOME_PSP>`, `<NOME_EC>`, `<DESCRIZIONE_REGOLAMENTO>`, `<BIC>` | dati anagrafici di test del corpo di creazione | `src/integration/fdr3/payloads.yaml` |
| `<ID_FLUSSO>`, `<IUV>`, `<IUR>` | valori generati a ogni run | generatori (§10.1, §10.3) |

### Come leggere il documento

Ogni elemento che altre parti devono poter richiamare ha una sigla stabile.

| Sigla | Significato | Dove |
| --- | --- | --- |
| R-nn | regola funzionale di dominio, con fonte | §3 |
| VAR-nn | dimensione di variazione dei dati: diventa una colonna degli Esempi | §4.4 |
| VG-xx | verifica di guardia: controllo dell'implementazione su un'azione del PSP, che non è un AC | §4.5, §9.2 |
| QF-nn | questione funzionale aperta | §13.1 |
| DM-nn | dato mancante o da verificare | §10.7 |
| RI-nn | rilievo implementativo | §12.5 |
| DV-n, DT-n | divergenza fra le fonti, divergenza tecnica | §13.3 |
| FT-nn | fonte | §14 |

Precondizioni, passi, postcondizioni e AC degli UC si citano con la numerazione degli UC, per esempio "UC-FDR-001 passo 7" o "AC-06". AC-01 … AC-06 sono comuni ai due UC; AC-07 e AC-08 sono specifici. I testi degli UC compaiono in corsivo fra caporali («»), gli step delle feature in `codice`. Le citazioni delle feature omettono il commento di tracciamento della prima riga di ciascun file.

### Indice

1. Il task e il test
2. Il dominio in breve
3. Regole funzionali di riferimento
4. Elementi comuni ai due UC
5. UC-FDR-001 e FEAT_001: pubblicazione con la modalità nuova, recupero con la legacy
6. UC-FDR-002 e FEAT_002: invio con la modalità legacy, recupero con la nuova
7. Contratti e ambiente UAT
8. Interfacce delle due modalità
9. Oracoli e guardie
10. Dati di test
11. Attesa e asincronia
12. Implementazione
13. Questioni aperte e stato delle feature
14. Fonti e tracciabilità
15. Riepilogo e considerazioni finali

## 1. Il task e il test

### 1.1 La richiesta

> Sul dominio FDR sarebbe molto utile mettere a terra degli scenari e2e che consentano di coprire alcuni use case importanti dell'ecosistema FDR:
>
> - Scenari ibridi (es.: PSP che pubblica flussi (write) mediante la nuove API (FDR3) / EC che scarica i flussi (read) utilizzando le vecchie API (FDR1) e viceversa);
> - Convertitori xml->json e json->xml;
>
> Da notare che il primo punto copre anche il check sul punto 2.

### 1.2 Come viene letta

In soldoni, la richiesta si traduce in un test automatico e ripetibile che usa la funzionalità come la userebbero PSP ed EC: stesse modalità di accesso, stesse credenziali, nessuna scorciatoia verso i componenti interni. Il test impersona entrambi gli attori e chiude il percorso dal lato dell'EC, perché è lì che si vede se il flusso è arrivato intero.

```text
UC-FDR-001   PSP --[modalità nuova: crea, aggiungi pagamenti, pubblica]--> FDR3
                --[conversione JSON -> XML, asincrona]--> FDR1 <--[modalità legacy: elenco, flusso]-- EC

UC-FDR-002   PSP --[modalità legacy: invia il flusso]--> FDR1
                --[conversione XML -> JSON, asincrona]--> FDR3 <--[modalità nuova: elenco, dettaglio, pagamenti]-- EC
```

Due conseguenze guidano il resto del documento:

- i convertitori non hanno un test separato: li esercita ciascun percorso, uno per direzione;
- il significato di "leggere" dipende dalla modalità. Con la legacy l'EC ottiene l'elenco e poi il documento XML completo; con la nuova ottiene l'elenco, la testata del flusso e i pagamenti in pagine. Gli UC coprono l'intero percorso di lettura, non soltanto la prima richiesta.

### 1.3 Perché non basta la suite fdr3

La suite [fdr3](../src/integration/fdr3) verifica già percorsi REST dal PSP all'EC. L'analisi è statica: la suite non è stata eseguita.

| Aspetto | Copertura attuale di fdr3 |
| --- | --- |
| Percorso REST da PSP a EC | Presente: creazione, aggiunta dei pagamenti e pubblicazione, seguite da letture dell'EC (elenco dei flussi e pagamenti) |
| Contenuto letto rispetto a quello inviato | Parziale: si controllano numero di elementi per pagina, filtri su PSP e data, revisione e totale dei pagamenti; non si confrontano IUV, IUR, importi ed esiti con l'input |
| Dettaglio del flusso lato EC | Non fra le azioni previste; il dettaglio pubblicato si legge solo dal lato PSP |
| Invio e lettura con la modalità legacy | Assenti |
| Conversione fra XML e JSON, propagazione asincrona | Assenti: nessuna attesa e nessun confronto fra formati |

Evidenza: la suite copre il percorso REST da PSP a EC ma non attraversa mai il confine fra le due modalità. Il task ricade nelle righe oggi assenti, più il confronto del contenuto, che fdr3 verifica solo in parte.

### 1.4 Due UC, due feature

| | UC-FDR-001 | UC-FDR-002 |
| --- | --- | --- |
| Titolo | Pubblicazione FDR3 e recupero FDR1 | Invio FDR1 e recupero FDR3 |
| Il PSP scrive con | modalità nuova | modalità legacy |
| L'EC legge con | modalità legacy | modalità nuova |
| Conversione verificata | JSON verso XML | XML verso JSON |
| UC | [UC-FDR-001-v3](use-cases/UC-FDR-001-v3.md) | [UC-FDR-002-v3](use-cases/UC-FDR-002-v3.md) |
| Feature | FEAT_001, `FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature` | FEAT_002, `FEAT_002_FdRHybrid_Invio_FDR1_e_recupero_FDR3.feature` |
| Tag di feature | `@fdrhybrid_001_Pubblicazione_FDR3_Recupero_FDR1` | `@fdrhybrid_002_Invio_FDR1_Recupero_FDR3` |
| Tag di scenario | `@fdrhybrid_001_01 @positive` | `@fdrhybrid_002_01 @positive` |
| Struttura | un Contesto e un solo Schema dello scenario con sei righe di Esempi (§10.5) | come FEAT_001 |
| Stato | bozza (§13.2) | bozza (§13.2) |

I due UC non hanno flussi alternativi né di eccezione. Un UC unico, con la direzione come dato, sarebbe preferibile se i due flussi coincidessero nei passi e nelle verifiche. Non coincidono in tre punti:

- attori e modalità di scrittura e di lettura cambiano da una direzione all'altra;
- i componenti attraversati sono diversi, perché i convertitori sono due;
- le verifiche specifiche non si sovrappongono: revisione e dettaglio hanno senso solo nella modalità nuova.

Verdetto: due UC, perché le differenze pesano più delle parti comuni. Queste ultime sono descritte una sola volta in §4 e ripetute in ciascun UC, che deve restare autonomo.

Le colonne degli Esempi sono liste separate da virgole, da trasformare in strutture nello step: gli importi in `Decimal`, gli esiti nei codici di §8.7. La colonna `numero_pagamenti` ripete la lunghezza delle liste. Proposta: il binding ne verifica la coerenza e, se non coincide, il caso è un errore del test e non un difetto della conversione.

## 2. Il dominio in breve

### 2.1 Il flusso di rendicontazione

Un flusso di rendicontazione è l'elenco dei pagamenti che un PSP ha eseguito a favore di un ente creditore (EC), con i dati del regolamento e i totali di controllo. Il PSP lo invia a pagoPA; l'EC lo recupera per riconciliare gli incassi. Un flusso contiene:

- identificativo e data e ora del flusso;
- mittente (il PSP, con tipo e codice identificativo, denominazione, intermediario e canale) e destinatario (l'EC);
- dati del regolamento: descrizione, data e, se presente, banca di riversamento;
- numero e importo totale dei pagamenti dichiarati;
- i singoli pagamenti, ciascuno con IUV, IUR, importo, esito, data dell'esito e indice di trasferimento.

### 2.2 Le due modalità

| Aspetto | Modalità legacy (FDR1) | Modalità nuova (FDR3) |
| --- | --- | --- |
| Formato | XML | JSON |
| Invio da parte del PSP | un'unica operazione con l'intero flusso | tre fasi: creazione della testata, aggiunta dei pagamenti (anche in più richieste), pubblicazione |
| Stato intermedio | nessuno | bozza (creato, poi con pagamenti inseriti) fino alla pubblicazione |
| Revisioni | non gestite | ogni pubblicazione rilascia una revisione e si conserva lo storico |
| Recupero da parte dell'EC | elenco dei flussi, poi richiesta del singolo flusso: arriva l'XML completo | elenco dei flussi pubblicati, dettaglio della testata, pagamenti in pagine |
| Motivo | modalità storica, con l'intero flusso in un solo messaggio | supera i limiti di dimensione dei messaggi e consente upload e download incrementali |

Evidenza: le due modalità non sono speculari, perché la nuova scompone in più fasi ciò che la legacy fa in un colpo solo. Questa asimmetria rende il confronto dei contenuti più delicato di un semplice controllo sull'esito delle richieste.

### 2.3 Il ciclo di vita di un flusso nella modalità nuova

- Il flusso nasce con la **creazione**, che ne definisce la testata e dichiara numero e importo totale dei pagamenti attesi. Da quel momento è una bozza (stato creato);
- con l'**aggiunta dei pagamenti** la bozza si popola (stato con pagamenti inseriti). I pagamenti si possono anche rimuovere, e la bozza si può cancellare per intero;
- con la **pubblicazione** il flusso diventa visibile all'EC (stato pubblicato) e riceve una revisione. Il flusso pubblicato non si modifica né si cancella;
- per una **nuova versione** si crea di nuovo lo stesso identificativo: nasce una nuova revisione, mentre la precedente resta presente;
- l'EC vede solo i flussi pubblicati e, negli elenchi, l'ultima revisione di ciascuno.

### 2.4 Conversione e propagazione

Per non obbligare PSP ed EC a migrare insieme, la piattaforma tiene allineate le due modalità. Dopo la pubblicazione di un flusso con la modalità nuova, lo storicizza e lo notifica alla componente legacy, che ne ricostruisce il documento XML. Dopo l'invio di un flusso con la modalità legacy, conserva l'XML e un convertitore ricrea il flusso nella modalità nuova, con creazione, aggiunta dei pagamenti e pubblicazione. Il requisito dichiarato è uno solo: la gestione del flusso deve essere trasparente a PSP ed EC (R-02).

Tre aspetti contano per gli UC:

- la propagazione è asincrona. La conferma data al PSP non dice quando l'altra modalità avrà il flusso e le fonti non fissano un limite di tempo (R-14);
- il documento che l'EC riceve non coincide byte per byte con quello prodotto dal PSP, perché il contenuto viene ricostruito: il confronto ha senso solo sul significato dei dati (§4.2);
- i flussi ottenuti per conversione non rientrano nel ciclo opposto (R-15).

### 2.5 Attori

| Attore | Ruolo nel task | UC-FDR-001 | UC-FDR-002 |
| --- | --- | --- | --- |
| PSP | scrive il flusso | modalità nuova | modalità legacy |
| EC | legge il flusso | modalità legacy | modalità nuova |
| Piattaforma pagoPA | riceve, valida, conserva, converte e rende disponibile il flusso | sistema | sistema |
| Test automatico | impersona PSP ed EC con le loro credenziali e modalità di accesso | esecutore | esecutore |

### 2.6 Glossario

| Termine | Significato |
| --- | --- |
| FdR | Flusso di Rendicontazione |
| PSP | Prestatore di Servizi di Pagamento: invia il flusso |
| EC | Ente Creditore: recupera il flusso |
| FDR1, modalità legacy | modalità storica, con messaggi XML |
| FDR3, modalità nuova | modalità con operazioni incrementali e dati in JSON |
| Bozza | flusso non ancora pubblicato, creato o con pagamenti inseriti |
| Revisione | versione numerata di un flusso pubblicato |
| Pubblicazione | passaggio che rende il flusso visibile all'EC |
| IUV | identificativo univoco di versamento |
| IUR | identificativo univoco di riscossione |
| Regolamento | operazione di regolamento economico cui il flusso si riferisce, con descrizione, data e, se presente, banca di riversamento |
| Intermediario, canale, stazione | identità con cui gli attori accedono: il PSP tramite il suo intermediario e il suo canale, l'EC tramite il suo intermediario e la sua stazione |
| Propagazione | passaggio asincrono del flusso da una modalità all'altra |
| Convertitore | componente che traduce il flusso da XML a JSON o viceversa |

## 3. Regole funzionali di riferimento

Le regole sono ricavate dalle fonti elencate in §14; dove una regola è un'inferenza del redattore, la colonna Fonte lo dice. Per formati e vincoli fa fede il contratto pubblicato (FT-11), non gli esempi dei documenti (DV-5).

| ID | Regola | Fonte | Usata da |
| --- | --- | --- | --- |
| R-01 | Durante la transizione PSP ed EC devono poter usare sia la modalità legacy sia la nuova senza disservizi: non si può imporre il passaggio a tutti nello stesso momento. | FT-01, FT-04, FT-05 | precondizione 5 |
| R-02 | La gestione di un flusso deve essere trasparente a PSP ed EC: ciò che è pubblicato con una modalità si recupera con l'altra, senza perdita di significato. | FT-04, FT-05 | AC-01 … AC-05 |
| R-03 | L'EC vede solo i flussi pubblicati; negli elenchi compare l'ultima revisione di ciascun flusso, come avviene nella modalità legacy. | FT-03 | UC-FDR-001 postcondizione 1; UC-FDR-002 passo 4 |
| R-04 | Un flusso nasce vuoto, riceve i pagamenti e viene pubblicato. Finché non è pubblicato è una bozza, modificabile e cancellabile; dopo la pubblicazione non si modifica né si cancella. Una nuova versione si ottiene creando di nuovo lo stesso identificativo, e genera una nuova revisione. | FT-03 | precondizione 4; UC-FDR-001 passi 1 … 6; postcondizione 3 |
| R-05 | I pagamenti si aggiungono a una bozza, al massimo 1000 per richiesta e con più richieste consecutive. Ogni pagamento ha un indice di posizione univoco nel flusso. | FT-03 | UC-FDR-001 passo 3 |
| R-06 | La pubblicazione verifica che numero e importo dei pagamenti inseriti coincidano con i totali dichiarati alla creazione; se non coincidono la rifiuta e il flusso resta in bozza. | FT-03, FT-12 | UC-FDR-001 passo 6; AC-03 |
| R-07 | Ogni pagamento è identificato da IUV e IUR. L'indice di posizione è una proprietà della modalità nuova, senza equivalente nella legacy. | FT-03, FT-11 | precondizione 6; AC-04, AC-05 |
| R-08 | Gli esiti ammessi per un pagamento in UAT sono quattro: eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT. | FT-11, FT-07 | VAR-02; AC-05 |
| R-09 | Il tipo di identificativo del mittente è persona giuridica, codice ABI o codice BIC, con corrispondenza uno a uno fra le due modalità. | FT-11, FT-07 | precondizione 6 |
| R-10 | Gli importi sono in euro con due decimali, ogni pagamento vale almeno 0,01 e il totale del flusso è la somma dei pagamenti. | FT-11 | AC-03, AC-05; VAR-05 |
| R-11 | Istante del flusso, giorno di regolamento e giorno dell'esito sono dati temporali distinti: il giorno di calendario originale non deve spostarsi passando da una modalità all'altra. Il fuso con cui la conversione interpreta le date legacy è indicato solo in FT-07. | FT-11, FT-07 | AC-02, AC-05; QF-06 |
| R-12 | L'identificativo del flusso deve essere valido per entrambe le modalità (lettere, cifre, trattino e underscore, al massimo 35 caratteri) e segue la convenzione data, codice PSP, trattino, suffisso. È unico per PSP, salvo le revisioni successive. | FT-02, FT-03, FT-11 | precondizioni 4 e 6; AC-01 |
| R-13 | Alcuni dati sono facoltativi nella modalità legacy e obbligatori nella nuova: denominazione del mittente, denominazione del destinatario, indice di trasferimento. Nei flussi di questi UC sono sempre valorizzati. Il confronto fra i due contratti è un'inferenza del redattore. | FT-05, FT-07, FT-11 | precondizione 6 |
| R-14 | Pubblicazione e invio rispondono subito, ma la disponibilità del flusso nell'altra modalità è asincrona. Non esiste un tempo massimo documentato; i meccanismi interni che le fonti descrivono (ripresa a un turno successivo del batch di storicizzazione, ritentativi con attesa crescente) non sono riconciliati fra loro né osservabili da PSP ed EC. | FT-03, FT-04, FT-05, FT-06, FT-07 | UC-FDR-001 passo 7; UC-FDR-002 passo 3; AC-06; QF-03 |
| R-15 | Un flusso ottenuto per conversione non viene riconvertito nella direzione opposta, per evitare cicli. | FT-02, FT-03 | contesto |
| R-16 | I flussi inoltrati a un gestore esterno vengono solo registrati dalla piattaforma ed esclusi dalla consultazione legacy. | FT-02 | precondizione 3 |
| R-17 | La piattaforma convalida PSP ed EC rispetto alle anagrafiche configurate: un'entità non nota fa rifiutare la richiesta, anche durante la conversione. | FT-03, FT-07 | precondizione 1; UC-FDR-002 precondizione 7 |
| R-18 | Le operazioni richiedono credenziali e abilitazioni proprie dell'attore, diverse nelle due modalità. | FT-03, FT-11 | precondizione 2 |
| R-19 | L'EC recupera in autonomia i flussi solo entro una finestra temporale, di lunghezza non documentata: oltre serve l'assistenza. Nella modalità nuova l'elenco copre per default dal primo giorno del mese precedente. | FT-03, FT-08 | UC-FDR-001 passo 8; UC-FDR-002 passo 4 |
| R-20 | Il requisito "meno di dieci secondi" vale per la singola richiesta, non per la propagazione fra le modalità. | FT-01 | AC-06; QF-03 |

## 4. Elementi comuni ai due UC

### 4.1 Precondizioni comuni

Valgono per entrambi gli UC; UC-FDR-002 ne ha una settima (§6.2).

| # | Precondizione | Regole |
| --- | --- | --- |
| 1 | PSP ed EC sono censiti sulla piattaforma e abilitati rispettivamente a inviare e a ricevere flussi | R-17 |
| 2 | PSP ed EC dispongono delle credenziali per entrambe le modalità: chiave di accesso per la nuova; credenziali di intermediario e canale (PSP) e di intermediario e stazione (EC) per la legacy | R-18 |
| 3 | La coppia PSP/EC è gestita dalla piattaforma FDR: i suoi flussi non sono inoltrati a un gestore esterno | R-16 |
| 4 | L'identificativo del flusso non è mai stato usato dal PSP: non esistono bozze né flussi pubblicati con lo stesso identificativo | R-04, R-12 |
| 5 | I servizi coinvolti (modalità nuova, modalità legacy e conversione nella direzione in esame) sono operativi in UAT | R-01 |
| 6 | Il flusso da trattare è valido per entrambe le modalità, cioè rispetta l'intersezione dei due contratti: identificativo, importi, date, denominazioni, esiti ammessi | R-07 … R-13 |

Come ciascuna precondizione si verifichi o si prepari è una questione implementativa (RI-15).

### 4.2 Criteri di accettazione comuni

Il confronto riguarda il significato dei dati, non la forma: né l'uguaglianza byte per byte, né il solo esito positivo delle richieste. Gli AC sono quelli che l'EC può osservare con le API e che servono a dire che il flusso è arrivato corretto. Bastano quattro verifiche: il flusso compare all'EC entro T (AC-06), l'EC lo trova nell'elenco (AC-07), il contenuto è equivalente a quello scritto dal PSP (AC-01 … AC-05) e, solo in UC-FDR-001, il documento è valido rispetto allo schema (AC-08). L'equivalenza è definita da AC-01 … AC-05, mentre AC-06 misura quando il flusso diventa disponibile. AC-01 … AC-06 valgono per il flusso principale di entrambi gli UC e per le loro varianti di dati.

| AC | Criterio | Cosa si confronta | Regole | Note |
| --- | --- | --- | --- | --- |
| AC-01 | Il flusso recuperato ha lo stesso identificativo di quello scritto dal PSP | identificativo | R-12 | confronto esatto |
| AC-02 | Le date del flusso coincidono | istante del flusso, giorno di regolamento | R-11 | fuso e precisione da definire (QF-06) |
| AC-03 | I totali coincidono | numero e importo totale dichiarati, uguali a quelli scritti dal PSP e a quelli ricostruiti dai pagamenti recuperati | R-06, R-10 | importi confrontati come decimali, mai come testo; un pagamento o una pagina mancanti emergono qui e in AC-04 |
| AC-04 | I pagamenti recuperati sono tutti e soli quelli scritti dal PSP | insieme dei pagamenti, abbinati per IUV e IUR: nessuno mancante, duplicato o in più | R-07 | ordine non vincolante: il confronto è per insieme |
| AC-05 | Ogni pagamento ha lo stesso contenuto | importo, esito, giorno dell'esito, indice di trasferimento | R-08, R-10, R-11 | giorno dell'esito: fuso e precisione da definire (QF-06) |
| AC-06 | Il flusso diventa disponibile all'EC nell'altra modalità entro il tempo massimo T | tempo fra la conferma di pubblicazione o di invio e la prima lettura riuscita | R-14, R-20 | T da definire (QF-03); il mancato arrivo è il fallimento di questo criterio (§4.3) |

Che cosa si confronta e che cosa no:

- si confrontano identificativo, istante del flusso, giorno di regolamento, numero e importo totale dichiarati, insieme dei pagamenti e, per ogni pagamento, importo, esito, giorno dell'esito e indice di trasferimento;
- non si confrontano revisione, stato e date di creazione, aggiornamento e pubblicazione: sono metadati propri della modalità nuova, senza equivalente nell'XML. L'unico controllo sulla revisione è in UC-FDR-002 AC-07; lo stato pubblicato lo verifica la guardia VG-A2 (§9.2);
- non si confrontano mittente, destinatario, descrizione e banca del regolamento: restano dati di input validi per entrambe le modalità (precondizione 6);
- non si confronta l'indice di posizione dei pagamenti: lo assegna il PSP nella modalità nuova e nella legacy non esiste, quindi i pagamenti si abbinano per IUV e IUR (R-07);
- le password di canale e di stazione non fanno parte del contenuto da confrontare e non vanno mai riportate in chiaro nei risultati.

### 4.3 Attesa e propagazione

La conversione è asincrona e le fonti non indicano un tempo massimo. Il valore di dieci secondi dichiarato come requisito (R-20) riguarda la singola richiesta e non la propagazione. L'AC-06 va quindi scritto con un tempo T, distinto per direzione se serve. Finché T non è concordato (QF-03) l'AC resta incompleto: §11 propone un valore di lavoro, da non presentare come garanzia. Il tempo parte dalla conferma di pubblicazione (UC-FDR-001) o di invio (UC-FDR-002).

Dal lato dell'EC un flusso "in arrivo" e un flusso perso non si distinguono: l'unico segnale è l'assenza oltre T. Per questo la mancata disponibilità entro T è il fallimento di AC-06 nel flusso principale: il test termina non conforme e riporta l'evidenza (tempo trascorso e ultime letture). Ciò che la piattaforma fa all'interno non è osservabile e non si asserisce.

### 4.4 Varianti dei dati

Le varianti riusano lo stesso flusso e le stesse verifiche: nelle feature diventano righe degli Esempi. Non serve il prodotto cartesiano: basta coprire ogni valore almeno una volta, scegliendo insiemi che esercitino anche i limiti. Il numero di righe è una scelta della stesura; quelle adottate e il significato del loro fallimento sono in §10.5.

| ID | Dimensione | Valori supportati | Regole | Note |
| --- | --- | --- | --- | --- |
| VAR-02 | Esito del pagamento | i quattro esiti ammessi | R-08 | |
| VAR-03 | Indice di trasferimento | da 1 a 5 | R-13 | facoltativo nella legacy; nei flussi di questi UC è sempre presente |
| VAR-04 | Numero di pagamenti | uno; alcuni (per esempio tre) | R-05 | entro il limite di una richiesta di aggiunta |
| VAR-05 | Importi | minimo ammesso; importi con decimali; importo elevato | R-10 | il totale dichiarato è sempre la somma dei pagamenti |

### 4.5 Azioni dell'attore e verifiche di guardia

Creazione, aggiunta dei pagamenti e pubblicazione (UC-FDR-001) e invio con la legacy (UC-FDR-002) sono prerequisiti del test. Non si verifica la scrittura del PSP in sé, ma la sua conseguenza sull'altra modalità: per questo quelle azioni non sono AC. L'implementazione le controlla con verifiche di guardia, definite in §9.2. Se una guardia non è soddisfatta il test è non valido e termina subito, senza attendere la propagazione. Il risultato non si legge come difetto della conversione.

## 5. UC-FDR-001 e FEAT_001: pubblicazione con la modalità nuova, recupero con la legacy

### 5.1 Intestazione

- **UC:** [UC-FDR-001-v3](use-cases/UC-FDR-001-v3.md), «Pubblicazione FDR3 e recupero FDR1»;
- **feature:** [FEAT_001](use-cases/features/fdr-hybrid/FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature);
- **JTBD di riferimento:** da assegnare (§13.1);
- **attore principale:** PSP; **attori secondari:** EC e piattaforma pagoPA (modalità nuova, convertitore, modalità legacy);
- **conversione verificata:** da JSON a XML.

### 5.2 Precondizioni

Valgono le precondizioni comuni di §4.1; UC-FDR-001 non ne ha altre. Nella feature stanno nel Contesto e sono tutte coperte come `Dato`/`E`. Come si preparano o si verificano è un rilievo implementativo (RI-15).

| # | UC | Contesto della feature | Regole, dati e implementazione | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | *«PSP ed EC sono censiti sulla piattaforma e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione.»* | `Dato che il PSP e l'EC sono censiti e abilitati ad operare con le modalità nuova e legacy` | R-17; identità di test in §7.4; nessun controllo documentato (RI-15) | DM-02 |
| 2 | *«PSP ed EC dispongono delle credenziali e delle abilitazioni previste per le due modalità.»* | `E che le credenziali del PSP e dell'EC sono valide per le rispettive modalità` | R-18; §7.4 | DM-03 |
| 3 | *«La coppia PSP/EC è gestita dalla piattaforma FDR: i suoi flussi non sono inoltrati a un gestore esterno.»* | `E che la coppia PSP-EC è gestita dal sistema dei flussi di rendicontazione` | R-16; §7.4, RI-15 | DM-02 |
| 4 | *«L'identificativo scelto per il flusso non è mai stato usato dal PSP.»* | `E che l'identificativo del flusso non è mai stato usato ed è valido per entrambe le modalità` (lo stesso step vale per la 6) | R-04, R-12; §10.1 | |
| 5 | *«La modalità nuova, la modalità legacy e la conversione dalla nuova alla legacy sono operative.»* | `E che i servizi di rendicontazione e di conversione sono operativi` | R-01; RI-15 | DM-14 |
| 6 | *«Il flusso da trattare è valido per entrambe le modalità.»* | lo step della precondizione 4 e i dati di `Dato che il flusso contiene …` | R-07 … R-13; §10.2, §10.3, §10.6 | |

### 5.3 Flusso principale

| Passo (UC) | Step della feature | Regole, dati e implementazione | Da chiarire |
| --- | --- | --- | --- |
| *«1. Il PSP crea il flusso con la modalità nuova (FDR3).»* | `Dato che il flusso contiene <numero_pagamenti> pagamenti con importi <importi>, esiti <esiti> e indici di trasferimento <indici_trasferimento>` (dati) e `Quando il PSP crea il flusso con la modalità nuova` | R-04, R-12. REST: creazione (§8.1) con il corpo di §8.4; dati in §10.1 e §10.2; guardia VG-A1 (201). Codice: §5.7 | DM-13 |
| *«2. La piattaforma convalida la richiesta e crea il flusso in bozza.»* | `Allora la piattaforma crea il flusso in bozza` | R-17. Nessun oracolo proprio: si osserva dall'esito del passo 1 (VG-A1) | |
| *«3. Il PSP aggiunge i pagamenti al flusso.»* | `Quando il PSP aggiunge i pagamenti al flusso` | R-05. REST: aggiunta (§8.1) in una sola richiesta, al massimo 1000 pagamenti; i pagamenti vengono dalla riga degli Esempi (§8.7, §10.3, §10.5); guardia VG-A1 (200). Codice: §5.7, RI-05, RI-20 | DM-13 |
| *«4. La piattaforma convalida i pagamenti e li aggiunge alla bozza.»* | `Allora la piattaforma aggiunge i pagamenti alla bozza` | Nessun oracolo proprio: si osserva dall'esito del passo 3 (VG-A1) | |
| *«5. Il PSP pubblica il flusso.»* | `Quando il PSP pubblica il flusso` | REST: pubblicazione, senza corpo (§8.1); guardia VG-A1 | DM-13 |
| *«6. La piattaforma verifica la coerenza dei totali, pubblica il flusso e conferma l'operazione al PSP.»* | `Allora la piattaforma conferma la pubblicazione` e `E il flusso risulta pubblicato alla prima revisione, con totali calcolati uguali a quelli dichiarati` | R-06. Conferma 200 (400 se i totali non coincidono: VG-A1). Lettura del flusso pubblicato lato PSP: VG-A2 (§9.2). Da qui parte T (§4.3) | |
| *«7. La piattaforma rende disponibile il flusso anche con la modalità legacy (FDR1). Il passaggio è asincrono rispetto alla conferma al PSP.»* | nessuno step proprio: lo osserva `Allora l'elenco contiene il flusso entro il tempo massimo previsto dalla conferma della pubblicazione` | R-14. Nessun oracolo proprio: lettura ripetuta dell'elenco legacy, solo letture (§11) | QF-03 |
| *«8. L'EC consulta con la modalità legacy (FDR1) i flussi del PSP e individua quello pubblicato.»* | `Quando l'EC consulta con la modalità legacy l'elenco dei flussi del PSP` | R-19. SOAP: elenco dei flussi (§8.5) con intermediario, stazione, password, dominio e PSP; busta grezza (RI-01, RI-02) | DM-01, DM-03, DM-04, DM-05 |
| *«9. L'EC richiede il flusso individuato e lo riceve completo.»* | `Quando l'EC richiede con la modalità legacy il flusso individuato` e `Allora l'EC riceve il flusso completo` | SOAP: richiesta del flusso (§8.5); `xmlRendicontazione` in base64, da decodificare (§8.5) e leggere come XML (§8.6) | DM-04, DM-16 |

Copertura della bozza: passi 1-6, 8 e 9 coperti; passo 7 parziale, perché si osserva solo dalla lettura e T non ha un valore (QF-03).

### 5.4 Postcondizioni

| # | UC | Come si osserva | Copertura della bozza |
| --- | --- | --- | --- |
| 1 | *«Il flusso è pubblicato nella modalità nuova alla prima revisione, con totali coerenti.»* | VG-A2: lettura lato PSP, stato pubblicato, revisione 1, totali calcolati uguali ai dichiarati; step `E il flusso risulta pubblicato alla prima revisione, con totali calcolati uguali a quelli dichiarati` | coperta |
| 2 | *«Lo stesso flusso è disponibile all'EC nella modalità legacy, completo e con contenuto equivalente a quello pubblicato.»* | AC-01 … AC-08 | parziale: dipende da QF-03 e QF-06 |
| 3 | *«Il flusso pubblicato non è più modificabile né cancellabile.»* | nessun oracolo: le fonti non descrivono un esito osservabile che la attesti; la conseguenza pratica è che i flussi di test restano in UAT (R-04, RI-09) | non coperta: nessuno step |

### 5.5 Acceptance Criteria

Le regole di confronto complete sono in §9.1.

| AC | UC | Step della feature | Oracolo | Copertura della bozza |
| --- | --- | --- | --- | --- |
| AC-01 | *«L'identificativo del flusso recuperato coincide con quello pubblicato.»* | `E l'identificativo del flusso ricevuto è uguale a quello pubblicato` | uguaglianza esatta di `identificativoFlusso` nel contenuto XML | coperto |
| AC-02 | *«Data e ora del flusso e giorno di regolamento coincidono con quelli pubblicati, senza spostamenti del giorno di calendario.»* | `E la data e ora del flusso e il giorno di regolamento sono uguali a quelli pubblicati, senza spostamento del giorno di calendario` | `dataOraFlusso` come istante UTC, `dataRegolamento` come data | parziale: fuso e precisione (QF-06) |
| AC-03 | *«Numero e importo totale dichiarati coincidono con quelli pubblicati e con quelli dei pagamenti recuperati.»* | `E il numero e l'importo totale dei pagamenti dichiarati sono uguali a quelli pubblicati e a quelli ricostruiti dai pagamenti ricevuti` | `numeroTotalePagamenti` e `importoTotalePagamenti` contro `datiSingoliPagamenti`, come `Decimal` a due cifre | coperto |
| AC-04 | *«I pagamenti recuperati sono tutti e soli quelli pubblicati: nessuno manca, è duplicato o è aggiunto.»* | `E i pagamenti ricevuti sono tutti e soli quelli pubblicati, senza mancanti né duplicati` | insiemi di coppie `(iuv, iur)` uguali, con conteggio delle occorrenze; senza ordine | coperto |
| AC-05 | *«Ogni pagamento recuperato ha lo stesso contenuto del pagamento pubblicato.»* | `E per ogni pagamento importo, esito, indice di trasferimento e giorno dell'esito sono uguali a quelli pubblicati` | per ogni coppia: importo `Decimal`, esito mappato (§8.7), indice di trasferimento, giorno dell'esito | parziale: il giorno dell'esito dipende da QF-06 |
| AC-06 | *«Il flusso diventa disponibile all'EC nella modalità legacy entro il tempo massimo previsto dalla conferma della pubblicazione.»* | `Allora l'elenco contiene il flusso entro il tempo massimo previsto dalla conferma della pubblicazione` | tempo fra la conferma di pubblicazione e la prima lettura dell'elenco legacy che contiene il flusso, entro T | parziale: la feature non ha un valore di T (QF-03) |
| AC-07 | *«L'elenco consultato dall'EC contiene il flusso pubblicato, con il suo identificativo e la sua data e ora.»* | `E la voce del flusso riporta identificativo e data e ora uguali a quelli pubblicati` | l'elenco legacy per il PSP contiene una voce `idRendicontazione` con `identificativoFlusso` e `dataOraFlusso` uguali a `fdr` e `fdrDate` pubblicati | parziale: identificativo coperto; data e ora dipendono da QF-06 |
| AC-08 | *«Il flusso ricevuto dall'EC è valido rispetto allo schema XSD della modalità legacy.»* | `E il documento ricevuto è valido rispetto allo schema della modalità legacy` | `xmlRendicontazione` decodificato (compressione da confermare, DM-16), ben formato e valido contro `FlussoRiversamento_1_0_5.xsd` con `lxml` | coperto |

### 5.6 La feature

Citazione di [FEAT_001](use-cases/features/fdr-hybrid/FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature), bozza del 19/11/2026, senza il commento di tracciamento:

```gherkin
# language: it
@fdrhybrid_001_Pubblicazione_FDR3_Recupero_FDR1
Funzionalità: Pubblicazione di un flusso con la modalità nuova e recupero con la modalità legacy

  Contesto:
    Dato che il PSP e l'EC sono censiti e abilitati ad operare con le modalità nuova e legacy
    E che le credenziali del PSP e dell'EC sono valide per le rispettive modalità
    E che la coppia PSP-EC è gestita dal sistema dei flussi di rendicontazione
    E che i servizi di rendicontazione e di conversione sono operativi
    E che l'identificativo del flusso non è mai stato usato ed è valido per entrambe le modalità

  @fdrhybrid_001_01 @positive
  Schema dello scenario: Il PSP pubblica un flusso con la modalità nuova e l'EC lo recupera con la modalità legacy
    Dato che il flusso contiene <numero_pagamenti> pagamenti con importi <importi>, esiti <esiti> e indici di trasferimento <indici_trasferimento>
    Quando il PSP crea il flusso con la modalità nuova
    Allora la piattaforma crea il flusso in bozza
    Quando il PSP aggiunge i pagamenti al flusso
    Allora la piattaforma aggiunge i pagamenti alla bozza
    Quando il PSP pubblica il flusso
    Allora la piattaforma conferma la pubblicazione
    E il flusso risulta pubblicato alla prima revisione, con totali calcolati uguali a quelli dichiarati
    Quando l'EC consulta con la modalità legacy l'elenco dei flussi del PSP
    Allora l'elenco contiene il flusso entro il tempo massimo previsto dalla conferma della pubblicazione
    E la voce del flusso riporta identificativo e data e ora uguali a quelli pubblicati
    Quando l'EC richiede con la modalità legacy il flusso individuato
    Allora l'EC riceve il flusso completo
    E il documento ricevuto è valido rispetto allo schema della modalità legacy
    E l'identificativo del flusso ricevuto è uguale a quello pubblicato
    E la data e ora del flusso e il giorno di regolamento sono uguali a quelli pubblicati, senza spostamento del giorno di calendario
    E il numero e l'importo totale dei pagamenti dichiarati sono uguali a quelli pubblicati e a quelli ricostruiti dai pagamenti ricevuti
    E i pagamenti ricevuti sono tutti e soli quelli pubblicati, senza mancanti né duplicati
    E per ogni pagamento importo, esito, indice di trasferimento e giorno dell'esito sono uguali a quelli pubblicati

    Esempi:
      | numero_pagamenti | importi                           | esiti                                                                                          | indici_trasferimento |
      | 3                | 100.00, 100.00, 100.00            | eseguito, eseguito, eseguito                                                                   | 1, 1, 1              |
      | 4                | 100.00, 100.00, 100.00, 100.00    | eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT | 1, 1, 1, 1           |
      | 3                | 100.00, 100.00, 100.00            | eseguito, eseguito, eseguito                                                                   | 1, 3, 5              |
      | 1                | 100.00                            | eseguito                                                                                       | 1                    |
      | 5                | 100.00, 100.00, 100.00, 100.00, 100.00 | eseguito, eseguito, eseguito, eseguito, eseguito                                          | 1, 1, 1, 1, 1        |
      | 4                | 0.01, 10.00, 1234.56, 999999.99   | eseguito, eseguito, eseguito, eseguito                                                         | 1, 1, 1, 1           |
```

### 5.7 Implementazione della pubblicazione con la modalità nuova

Nei passi 1-6 il PSP scrive con la modalità nuova. In soldoni, per questa parte si sfrutta il codice già prodotto da Marco Piccolo per la suite fdr3 (`src/integration/fdr3`), opportunamente impiegato per produrre i sei flussi delle righe dello Schema dello scenario di FEAT_001 (§10.5). Non si riscrive ciò che esiste: si adatta solo dove le righe lo richiedono.

Si riusano:

- `perform_fdr_action` e `DEFAULT_ENDPOINTS` in `src/integration/fdr3/utils_fdr.py`: azioni di creazione (201), aggiunta dei pagamenti (200), pubblicazione (200) e lettura del flusso pubblicato lato PSP (VG-A2). `perform_fdr_action` accetta il corpo già costruito (`payload_override`), quindi il corpo di ogni riga si prepara fuori e si passa dentro;
- il modello `create_payload` di `src/integration/fdr3/payloads.yaml` per il corpo di creazione (segnaposto per nome e data del flusso, identità e totali);
- la configurazione e la costruzione dei client REST degli hook di `src/integration/fdr3/environment.py` (sezioni `psp` e `fdr`; identità di `global_configuration` esposte come segnaposto);
- `generate_iuv` e `generate_uuid` di `src/utility/data_generators.py`, già usati da fdr3 per IUV e IUR;
- la convenzione di fdr3 per identificativo e data del flusso (§10.1).

Per ciascuna delle sei righe il test:

1. genera un identificativo unico per run e la data del flusso (§10.1);
2. costruisce il corpo di creazione dal modello, con `totPayments` uguale a `numero_pagamenti` e `sumPayments` uguale alla somma esatta degli importi della riga;
3. crea il flusso (201), aggiunge in una sola richiesta i pagamenti costruiti dalla riga (200) e pubblica (200). Sono le guardie VG-A1; nessuna delle tre azioni si ritenta (RI-07);
4. legge il flusso pubblicato lato PSP e controlla stato pubblicato, revisione 1 e totali calcolati uguali ai dichiarati (VG-A2);
5. da questo punto parte T e comincia la lettura legacy dell'EC (passi 7-9, §11).

Che cosa non si può usare così com'è:

- `_build_payments_payload(number, amount)` in `helper.py` divide il totale in parti uguali con `float`. Fissa inoltre `idTransfer` a 1, `payStatus` a `EXECUTED` e la data dell'esito all'ora corrente meno `i` giorni. Non serve quindi alle righe 2 (quattro esiti), 3 (indici di trasferimento 1, 3 e 5) e 6 (importi esatti, totale 1001244.56);
- le righe 1, 4 e 5, con pagamenti uguali, sarebbero producibili anche con la funzione esistente. La data dell'esito va però controllata comunque (RI-06), quindi conviene un solo generatore per tutte le righe;
- serve perciò un generatore parametrico a lato, che prenda dalla riga le liste di importi, esiti e indici, usi `Decimal`, parta dagli indici da 1 e fissi `payDate` a mezzogiorno UTC (RI-05, RI-06, RI-20). Proposta: non modificare il generatore di fdr3, per non toccare una suite già in uso;
- il modello `create_payload` invia `regulationDate` come istante mentre il contratto vuole una data, e fissa `receiver.id` a un valore diverso dal codice EC: vanno adattati (§10.2);
- `perform_fdr_action` sostituisce con una stringa vuota i segnaposto privi di valore e usa 1 come revisione se manca (RI-17): nella nuova suite un segnaposto vuoto è un errore del test;
- `checks` di `perform_fdr_action` confronta con `!=` valori letti come `float`: per gli importi serve il confronto con `Decimal` (RI-05);
- i client costruiti dagli hook di fdr3 registrano solo un avviso se la configurazione manca (RI-18);
- lo step di fdr3 "che lo scenario … è stato eseguito con successo" rieseguirebbe i passi di un altro scenario, quindi non si usa in flussi con attese asincrone (RI-14).

Importare codice di una suite di integrazione in una suite e2e richiede una decisione sulla collocazione (§12.4).

Verdetto: il codice di fdr3 copre creazione, aggiunta, pubblicazione e lettura lato PSP, mentre il generatore dei pagamenti va affiancato e non modificato.

## 6. UC-FDR-002 e FEAT_002: invio con la modalità legacy, recupero con la nuova

### 6.1 Intestazione

- **UC:** [UC-FDR-002-v3](use-cases/UC-FDR-002-v3.md), «Invio FDR1 e recupero FDR3»;
- **feature:** [FEAT_002](use-cases/features/fdr-hybrid/FEAT_002_FdRHybrid_Invio_FDR1_e_recupero_FDR3.feature);
- **JTBD di riferimento:** da assegnare (§13.1);
- **attore principale:** PSP; **attori secondari:** EC e piattaforma pagoPA (modalità legacy, convertitore, modalità nuova);
- **conversione verificata:** da XML a JSON.

### 6.2 Precondizioni

Valgono le precondizioni comuni di §4.1, più la settima. Nella feature stanno nel Contesto e sono tutte coperte come `Dato`/`E`. Come si preparano o si verificano è un rilievo implementativo (RI-15).

| # | UC | Contesto della feature | Regole, dati e implementazione | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | *«PSP ed EC sono censiti sulla piattaforma e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione.»* | `Dato che il PSP e l'EC sono censiti e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione` | R-17; identità di test in §7.4; nessun controllo documentato (RI-15) | DM-02 |
| 2 | *«PSP ed EC dispongono delle credenziali e delle abilitazioni previste per le due modalità.»* | `E che il PSP e l'EC dispongono delle credenziali e delle abilitazioni previste per le due modalità` | R-18; §7.4 | DM-03 |
| 3 | *«La coppia PSP/EC è gestita dalla piattaforma FDR: i suoi flussi non sono inoltrati a un gestore esterno.»* | `E che la coppia PSP-EC è gestita dal sistema dei flussi di rendicontazione` | R-16; §7.4, RI-15 | DM-02 |
| 4 | *«L'identificativo scelto per il flusso non è mai stato usato dal PSP.»* | `E che l'identificativo del flusso non è mai stato usato dal PSP ed è valido per entrambe le modalità` (lo stesso step vale per la 6) | R-04, R-12; §10.1 | |
| 5 | *«La modalità legacy, la modalità nuova e la conversione dalla legacy alla nuova sono operative.»* | `E che le modalità legacy e nuova e la conversione dalla legacy alla nuova sono operative` | R-01; RI-15 | DM-14 |
| 6 | *«Il flusso da trattare è valido per entrambe le modalità.»* | lo step della precondizione 4 e i dati di `Dato che il flusso contiene …` | R-07 … R-13; §10.2, §10.3, §10.6 | |
| 7 | *«PSP ed EC sono noti anche alla modalità nuova, così che la conversione possa creare il flusso.»* | `E che il PSP e l'EC sono noti anche alla modalità nuova` | R-17. Se non lo sono, la conversione non può creare il flusso e il percorso fallisce per un motivo estraneo al contenuto; nessun controllo documentato (RI-15) | DM-02 |

### 6.3 Flusso principale

| Passo (UC) | Step della feature | Regole, dati e implementazione | Da chiarire |
| --- | --- | --- | --- |
| *«1. Il PSP invia il flusso con la modalità legacy (FDR1).»* | `Dato che il flusso contiene <numero_pagamenti> pagamenti con importi <importi>, esiti <esiti> e indici di trasferimento <indici_trasferimento>` (dati) e `Quando il PSP invia il flusso con la modalità legacy` | SOAP: invio del flusso completo, testata e tutti i pagamenti, in un'unica operazione (§8.5). L'XML si genera dai dati della riga (§8.6, §10.3) e si valida offline prima di inviarlo (RI-04); busta grezza (RI-01, RI-02); il corpo dell'invio non si registra (RI-11) | DM-01, DM-03, DM-11, DM-16 |
| *«2. La piattaforma convalida l'invio, conserva il flusso e risponde con esito positivo.»* | `Allora la piattaforma convalida l'invio, conserva il flusso e risponde con esito positivo` | Guardia VG-B1 (§9.2): stato HTTP 200, albero XML analizzabile, nessun `fault`, `esito` registrato. Il valore positivo di `esito` non è documentato | DM-04 |
| *«3. La piattaforma converte il flusso e lo rende disponibile nella modalità nuova (FDR3). Il passaggio è asincrono rispetto alla conferma al PSP.»* | nessuno step proprio: lo osserva `Allora l'elenco contiene il flusso associato al PSP mittente entro il tempo massimo previsto dalla conferma dell'invio` | R-14. Nessun oracolo proprio: lettura ripetuta dell'elenco della modalità nuova, solo letture (§11) | QF-03, DM-14 |
| *«4. L'EC consulta con la modalità nuova (FDR3) i flussi pubblicati del PSP e individua il flusso.»* | `Quando l'EC consulta con la modalità nuova l'elenco dei flussi pubblicati del PSP` | R-19. REST: elenco dell'EC con `pspId` e `publishedGt` (§8.2, §8.3); il flusso si riconosce per uguaglianza esatta di `fdr` (RI-08) | |
| *«5. L'EC richiede il dettaglio del flusso.»* | `Quando l'EC richiede il dettaglio del flusso individuato` e `Allora l'EC riceve il dettaglio del flusso pubblicato` | REST: dettaglio con la `revision` letta dall'elenco (§8.2); l'azione non esiste in fdr3 e va aggiunta (§12.2) | |
| *«6. L'EC richiede i pagamenti del flusso e li ottiene tutti.»* | `Quando l'EC richiede i pagamenti del flusso` e `Allora l'EC ottiene tutti i pagamenti del flusso` | REST: pagamenti in pagine; il ciclo su `metadata.totPage` è un obbligo del passo e con `size` piccolo si esercita (§8.3, RI-13) | |

Copertura della bozza: passi 1, 2, 4, 5 e 6 coperti; passo 3 parziale, perché si osserva solo dalla lettura e T non ha un valore (QF-03).

### 6.4 Postcondizioni

| # | UC | Come si osserva | Copertura della bozza |
| --- | --- | --- | --- |
| 1 | *«Il flusso inviato con la modalità legacy è conservato dalla piattaforma.»* | nessun oracolo proprio: prova indiretta, cioè esito positivo dell'invio (VG-B1) e presenza del flusso nella modalità nuova dopo la conversione | parziale |
| 2 | *«Lo stesso flusso è pubblicato nella modalità nuova ed è leggibile dall'EC, completo e con contenuto equivalente a quello inviato.»* | AC-01 … AC-07 | parziale: dipende da QF-03, QF-06 e QF-11 |
| 3 | *«Il flusso pubblicato non è più modificabile né cancellabile.»* | nessun oracolo: le fonti non descrivono un esito osservabile che la attesti; la conseguenza pratica è che i flussi di test restano in UAT (R-04, RI-09) | non coperta: nessuno step |

### 6.5 Acceptance Criteria

Le regole di confronto complete sono in §9.1.

| AC | UC | Step della feature | Oracolo | Copertura della bozza |
| --- | --- | --- | --- | --- |
| AC-01 | *«L'identificativo del flusso recuperato coincide con quello inviato.»* | `E l'identificativo del flusso recuperato è uguale a quello inviato` | uguaglianza esatta di `fdr` del dettaglio | coperto |
| AC-02 | *«Data e ora del flusso e giorno di regolamento coincidono con quelli inviati, senza spostamenti del giorno di calendario.»* | `E la data e ora del flusso e il giorno di regolamento sono uguali a quelli inviati, senza spostamento del giorno di calendario` | `fdrDate` e `dataOraFlusso` come istanti UTC; `regulationDate` e `dataRegolamento` come date | parziale: fuso e precisione (QF-06) |
| AC-03 | *«Numero e importo totale dichiarati coincidono con quelli inviati e con quelli dei pagamenti recuperati.»* | `E il numero e l'importo totale dichiarati sono uguali a quelli inviati e a quelli ricostruiti dai pagamenti recuperati` | `totPayments` e `sumPayments` del dettaglio contro i pagamenti raccolti su tutte le pagine; `computedTotPayments` e `computedSumPayments` uguali ai dichiarati; `Decimal` a due cifre | coperto |
| AC-04 | *«I pagamenti recuperati sono tutti e soli quelli inviati: nessuno manca, è duplicato o è aggiunto.»* | `E i pagamenti recuperati sono tutti e soli quelli inviati, senza mancanti, duplicati o aggiunti` | insiemi di coppie `(iuv, iur)` uguali, con conteggio delle occorrenze; senza ordine | coperto |
| AC-05 | *«Ogni pagamento recuperato ha lo stesso contenuto del pagamento inviato.»* | `E per ogni pagamento importo, esito, indice di trasferimento e giorno dell'esito sono uguali a quelli inviati` | per ogni coppia: importo `Decimal`, esito mappato (§8.7), indice di trasferimento; `payDate` convertito in Europe/Rome contro `dataEsitoSingoloPagamento` | parziale: il giorno dell'esito dipende da QF-06 |
| AC-06 | *«Il flusso diventa disponibile all'EC nella modalità nuova entro il tempo massimo previsto dalla conferma dell'invio.»* | `Allora l'elenco contiene il flusso associato al PSP mittente entro il tempo massimo previsto dalla conferma dell'invio` | tempo fra la conferma dell'invio e la prima lettura dell'elenco della modalità nuova che contiene il flusso, entro T | parziale: la feature non ha un valore di T (QF-03) |
| AC-07 | *«L'elenco consultato dall'EC contiene il flusso associato al PSP mittente, con la revisione prevista.»* | lo step di AC-06 e `E la voce del flusso riporta la revisione prevista` | l'elenco con `pspId` e `publishedGt` contiene un elemento con `fdr` uguale a quello inviato e `pspId` del PSP mittente; la `revision` letta è quella attesa (DM-09) | parziale: flusso e PSP coperti; la revisione prevista non ha un numero nella feature (QF-11) |

### 6.6 La feature

Citazione di [FEAT_002](use-cases/features/fdr-hybrid/FEAT_002_FdRHybrid_Invio_FDR1_e_recupero_FDR3.feature), bozza del 19/11/2026, senza il commento di tracciamento:

```gherkin
# language: it
@fdrhybrid_002_Invio_FDR1_Recupero_FDR3
Funzionalità: Invio di un flusso con la modalità legacy e recupero con la modalità nuova

  Contesto:
    Dato che il PSP e l'EC sono censiti e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione
    E che il PSP e l'EC dispongono delle credenziali e delle abilitazioni previste per le due modalità
    E che la coppia PSP-EC è gestita dal sistema dei flussi di rendicontazione
    E che le modalità legacy e nuova e la conversione dalla legacy alla nuova sono operative
    E che il PSP e l'EC sono noti anche alla modalità nuova
    E che l'identificativo del flusso non è mai stato usato dal PSP ed è valido per entrambe le modalità

  @fdrhybrid_002_01 @positive
  Schema dello scenario: Il PSP invia un flusso con la modalità legacy e l'EC lo recupera con la modalità nuova
    Dato che il flusso contiene <numero_pagamenti> pagamenti con importi <importi>, esiti <esiti> e indici di trasferimento <indici_trasferimento>
    Quando il PSP invia il flusso con la modalità legacy
    Allora la piattaforma convalida l'invio, conserva il flusso e risponde con esito positivo
    Quando l'EC consulta con la modalità nuova l'elenco dei flussi pubblicati del PSP
    Allora l'elenco contiene il flusso associato al PSP mittente entro il tempo massimo previsto dalla conferma dell'invio
    E la voce del flusso riporta la revisione prevista
    Quando l'EC richiede il dettaglio del flusso individuato
    Allora l'EC riceve il dettaglio del flusso pubblicato
    E l'identificativo del flusso recuperato è uguale a quello inviato
    E la data e ora del flusso e il giorno di regolamento sono uguali a quelli inviati, senza spostamento del giorno di calendario
    Quando l'EC richiede i pagamenti del flusso
    Allora l'EC ottiene tutti i pagamenti del flusso
    E il numero e l'importo totale dichiarati sono uguali a quelli inviati e a quelli ricostruiti dai pagamenti recuperati
    E i pagamenti recuperati sono tutti e soli quelli inviati, senza mancanti, duplicati o aggiunti
    E per ogni pagamento importo, esito, indice di trasferimento e giorno dell'esito sono uguali a quelli inviati

    Esempi:
      | numero_pagamenti | importi                                | esiti                                                                                              | indici_trasferimento |
      | 3                | 100.00, 100.00, 100.00                 | eseguito, eseguito, eseguito                                                                       | 1, 1, 1              |
      | 4                | 100.00, 100.00, 100.00, 100.00         | eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT | 1, 1, 1, 1           |
      | 3                | 100.00, 100.00, 100.00                 | eseguito, eseguito, eseguito                                                                       | 1, 3, 5              |
      | 1                | 100.00                                 | eseguito                                                                                           | 1                    |
      | 5                | 100.00, 100.00, 100.00, 100.00, 100.00 | eseguito, eseguito, eseguito, eseguito, eseguito                                                   | 1, 1, 1, 1, 1        |
      | 4                | 0.01, 10.00, 1234.56, 999999.99        | eseguito, eseguito, eseguito, eseguito                                                             | 1, 1, 1, 1           |
```

Le sei righe degli Esempi sono le stesse di FEAT_001 (§10.5). Cambia il modo in cui si producono i dati: il PSP scrive con un messaggio SOAP che contiene l'XML del flusso (§8.5, §8.6) e l'EC legge con le API REST della modalità nuova (§8.2).

## 7. Contratti e ambiente UAT

### 7.1 Contratti da usare e dove trovarli

I contratti stanno nel repository pubblico [pagopa/pagopa-api](https://github.com/pagopa/pagopa-api), che raccoglie schemi XSD, WSDL e OpenAPI con un ciclo di rilascio diverso dalle SANP. Per UAT si usa l'ultima serie numerica `SANP3.x.y`, oggi `SANP3.13.0`, al commit `969833a6c8ff6e49137ba22757bc4656b99fcaba`. Il riferimento va ricontrollato prima di implementare: il 16/11/2026 e il 18/11/2026 l'ultima versione numerica era `SANP3.13.0` e puntava allo stesso commit. Per rifare la verifica:

```powershell
gh api --paginate "repos/pagopa/pagopa-api/branches?per_page=100" --jq ".[].name"
```

I collegamenti puntano al commit UAT.

| File | Contenuto | Serve a |
| --- | --- | --- |
| [wsdl/nodeForPsp.wsdl](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/wsdl/nodeForPsp.wsdl) | interfaccia del PSP verso il Nodo; contiene `nodoInviaFlussoRendicontazione` | UC-FDR-002 passo 1, VG-B1 |
| [wsdl/nodeForPa.wsdl](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/wsdl/nodeForPa.wsdl) | interfaccia dell'EC; contiene `nodoChiediElencoFlussiRendicontazione` e `nodoChiediFlussoRendicontazione` | UC-FDR-001 passi 8 e 9 |
| [wsdl/xsd/nodeForPsp.xsd](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/wsdl/xsd/nodeForPsp.xsd) | importato da `nodeForPsp.wsdl`; definisce `nodoInviaFlussoRendicontazioneRequest` e `nodoInviaFlussoRendicontazioneResponse` in un altro namespace, che l'operazione di invio non usa (DT-10) | caricamento di `nodeForPsp.wsdl` |
| [wsdl/xsd/nodoPerPsp.xsd](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/wsdl/xsd/nodoPerPsp.xsd) | messaggi di invio del flusso, richiesta e risposta | UC-FDR-002 passo 1, VG-B1 |
| [wsdl/xsd/nodeForPa.xsd](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/wsdl/xsd/nodeForPa.xsd) | messaggi di elenco e di richiesta del flusso | UC-FDR-001 passi 8 e 9 |
| [xsd-common/sac-common-types-1.0.xsd](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/xsd-common/sac-common-types-1.0.xsd) | tipi comuni: testi, password, risposta con fault | tutti i messaggi SOAP |
| [xsd-common/FlussoRiversamento_1_0_5.xsd](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/xsd-common/FlussoRiversamento_1_0_5.xsd) | contenuto del flusso XML | UC-FDR-001 AC-08 (validazione) e AC-01 … AC-05 (contenuto); UC-FDR-002 passo 1 (generazione) |
| [openapi/fdr_psp.json](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/openapi/fdr_psp.json) | API REST del PSP | UC-FDR-001 passi 1 … 6 |
| [openapi/fdr_organization.json](https://github.com/pagopa/pagopa-api/blob/969833a6c8ff6e49137ba22757bc4656b99fcaba/openapi/fdr_organization.json) | API REST dell'EC | UC-FDR-002 passi 4 … 6 |

Le dipendenze dei due WSDL si chiudono su sei file locali: i due WSDL, `wsdl/xsd/nodeForPsp.xsd`, `wsdl/xsd/nodoPerPsp.xsd`, `wsdl/xsd/nodeForPa.xsd` e `xsd-common/sac-common-types-1.0.xsd`. Lo schema del flusso non è importato da nessuno: serve a validare il contenuto XML, con la versione `1_0_5` del riferimento UAT.

Come acquisirli nel repository (proposta):

- oggi nel repository non c'è alcuna copia: nessun `.wsdl` o `.xsd`, e la cartella `src/e2e/fdr-hybrid` non esiste ancora (§12.4);
- tenere una copia versionata dei file della tabella sotto la futura suite, con la provenienza (riferimento e commit) in un file accanto. Per il lato SOAP sono sette: i due WSDL, i tre XSD sotto `wsdl/xsd`, i tipi comuni e lo schema del flusso. I due OpenAPI servono solo come riferimento per i corpi REST;
- preservare la struttura delle directory `wsdl/`, `wsdl/xsd/` e `xsd-common/`, perché gli import sono relativi (`xsd/nodeForPsp.xsd`, `../../xsd-common/sac-common-types-1.0.xsd`);
- non scaricare i contratti a runtime: il test deve essere ripetibile anche se il repository esterno cambia;
- aggiornare la copia in modo deliberato quando la serie SANP avanza.

Verifica dei contratti. Il 18/11/2026 i contratti sono stati riletti in sola lettura dal commit indicato, con le API pubbliche di GitHub; nessuna chiamata è andata verso gli ambienti. Risultano confermati:

- l'esistenza dei nove file e la chiusura delle dipendenze dei WSDL;
- il binding SOAP 1.1, stile `document`, `use="literal"`, con `SOAPAction` uguale al nome dell'operazione;
- gli indirizzi dichiarati dai WSDL (§7.3);
- il namespace della radice delle tre richieste (`http://ws.pagamenti.telematici.gov/`), con figli non qualificati perché gli schemi non dichiarano `elementFormDefault`;
- elementi, ordine, tipi e occorrenze dei messaggi;
- `esito` e `faultCode` come stringhe libere: il tipo comune `stOutcome`, con `OK` e `KO`, esiste ma queste primitive non lo usano;
- il contenuto del flusso: ordine, lunghezze, pattern, enumerazioni e occorrenze;
- le operazioni REST, con parametri (compresi i limiti di `page` e `size`), schemi, vincoli ed enumerazioni, nella versione 1.2.4 di entrambi gli OpenAPI;
- le corrispondenze campo per campo fra REST e XML, dichiarate nelle descrizioni degli OpenAPI.

Restano non verificati la raggiungibilità e il comportamento dei servizi in UAT, la validità di chiavi e password, gli esiti applicativi della legacy (DM-04) e la fonte normativa sulla compressione dell'XML (DM-16).

### 7.2 Endpoint REST della modalità nuova

| API | URL base UAT | Origine | Serve a |
| --- | --- | --- | --- |
| EC | `https://<HOST_API_UAT>/fdr-org/service/v1` | chiave `fdr` di `src/integration/fdr3/uat.yaml` | UC-FDR-002 passi 4 … 6 |
| PSP | `https://<HOST_API_UAT>/fdr-psp/service/v1` | chiave `psp` di `src/integration/fdr3/uat.yaml` | UC-FDR-001 passi 1 … 6 |

Due avvertenze. FT-03 prescrive per le API del PSP in UAT il dominio `<HOST_UPLOAD_UAT>`, per evitare errori di Gateway Timeout. La suite fdr3 usa invece `<HOST_API_UAT>`: la scelta è da confermare (DM-13). Inoltre l'OpenAPI del riferimento UAT dichiara server con il dominio dell'ambiente DEV: il campo `servers` dei contratti non va usato per ricavare l'ambiente (DT-2).

### 7.3 Endpoint SOAP della modalità legacy

| Operazione | Indirizzo dichiarato nel WSDL UAT | Precedente nel repository (suite WISP, UAT) |
| --- | --- | --- |
| Invio del flusso (PSP) | `https://<HOST_API_UAT>/nodo-auth/node-for-psp/v1` | `https://<HOST_API_UAT>/nodo/node-for-psp/v1` (`services.node_for_psp`) |
| Elenco e richiesta del flusso (EC) | `https://<HOST_API_UAT>/nodo-auth/node-for-pa/v1` | `https://<HOST_API_UAT>/nodo-auth/nodo-per-pa/v1` (`services.nodo_per_pa`) |

Evidenza: i due indirizzi per ciascuna operazione non coincidono e nessuna fonte dice quale serva alle primitive FDR in UAT; resta da stabilirlo prima di scrivere la configurazione (DM-01, DT-1).

Nella suite WISP gli indirizzi stanno in `src/integration/wisp/uat.yaml` sotto `services.node_for_psp` e `services.nodo_per_pa`, ciascuno con `url` e `subscription_key`. Le primitive FDR non sono instradate da WISP: il suo router, `get_primitive_url` in `src/integration/wisp/utility/routes.py`, conosce solo le primitive di quella suite. La nuova suite sceglie quindi da sé indirizzo, chiave e Content-Type per ciascuna primitiva.

### 7.4 Identità, chiavi e segreti

Le identità sono i valori di `global_configuration` in `src/integration/fdr3/uat.yaml`, esposti dagli hook di fdr3 come segnaposto. Sono identificativi di test e non segreti; qui sono omessi (vedi Riservatezza dei dati).

| Chiave | Valore | Usato come |
| --- | --- | --- |
| `psp` | `<CODICE_PSP>` | codice PSP (`pspId`, `identificativoPSP`) |
| `broker_psp` | `<INTERMEDIARIO_PSP>` | intermediario PSP |
| `channel` | `<CANALE_PSP>` | canale PSP |
| `channel_password` | `<PASSWORD_CANALE>`, segreto | password del canale |
| `organization` | `<CODICE_EC>` | codice EC (`organizationId`, `identificativoDominio`) |
| `broker_org` | `<INTERMEDIARIO_EC>` | intermediario EC |
| `station` | `<STAZIONE_EC>` | stazione EC |
| `station_password` | `<PASSWORD_STAZIONE>`, segreto | password della stazione |

Questi valori non dimostrano che la coppia sia abilitata alle primitive legacy né nota alla conversione: le precondizioni 1 e 3 e, in UC-FDR-002, la 7 restano da accertare (R-16, R-17, DM-02).

Chiavi e segreti necessari:

- **modalità nuova:** una chiave di sottoscrizione per l'EC (sezione `fdr`) e una per il PSP (sezione `psp`), con `key_name` e `key_value` (`<CHIAVE_SOTTOSCRIZIONE>`), già previste in fdr3 (R-18, precondizione 2);
- **modalità legacy:** le password di canale e di stazione, già previste come segnaposto, e l'eventuale chiave del gateway per le primitive SOAP (`<CHIAVE_SOTTOSCRIZIONE>`). Nella suite WISP la chiave viaggia nell'intestazione `Ocp-Apim-Subscription-Key` (costante in `src/integration/wisp/utility/constants.py`) (DM-03). Il precedente di WISP è un'analogia e non una conferma: verso l'interfaccia dell'EC usa una chiave di sottoscrizione dedicata (nome omesso), verso quella del PSP non invia alcuna chiave;
- la risoluzione segue il meccanismo del repository, descritto nella sezione Configurazione del [README](../README.md); i valori non vanno mai riportati nei log (RI-11).

### 7.5 Timeout, limiti e cache

- il client REST legge `timeout` in secondi, mentre la configurazione di fdr3 riporta `5000`: l'unità va chiarita prima di riusarla (RI-12);
- l'aggiunta dei pagamenti ha un limite di 50 richieste al secondo e 600 al minuto, con le intestazioni `x-remaining-calls-per-sec` e `x-remaining-calls-per-min` (FT-03): non incide su flussi piccoli;
- per l'elenco legacy FT-02 annuncia un sistema di cache lato APIM, con codice di errore in caso di troppe chiamate, ma lo stato non è confermato: il polling deve essere prudente (§11).

## 8. Interfacce delle due modalità

### 8.1 API REST della modalità nuova: lato PSP, scrittura

| Operazione | Metodo e percorso | Corpo e parametri | Successo | Serve a |
| --- | --- | --- | --- | --- |
| Creazione del flusso | `POST /psps/{pspId}/fdrs/{fdr}` | corpo `CreateFlowRequest` (§8.4, §8.7); `fdr` deve rispettare `[a-zA-Z0-9\-_]{1,35}` | 201 | UC-FDR-001 passo 1, VG-A1 |
| Aggiunta dei pagamenti | `PUT /psps/{pspId}/fdrs/{fdr}/payments/add` | corpo `{"payments": [...]}` con i pagamenti di §8.7; al massimo 1000 per richiesta | 200 | UC-FDR-001 passo 3, VG-A1 |
| Pubblicazione | `POST /psps/{pspId}/fdrs/{fdr}/publish` | nessun corpo | 200; 400 se i totali non coincidono | UC-FDR-001 passi 5 e 6, VG-A1 |
| Lettura del flusso pubblicato, lato PSP | `GET /psps/{pspId}/published/fdrs/{fdr}/revisions/{revision}/organizations/{organizationId}` | `revision` intero | 200 | UC-FDR-001 passo 6, VG-A2 |

Gli esiti previsti dall'OpenAPI sono 200 o 201, 400, 404 e 500; FT-03 aggiunge 401 e 403 (gateway) e 429 (limite di richieste). Il corpo di errore è `ErrorResponse`: `errorId`, `httpStatusCode`, `httpStatusDescription`, `appErrorCode` ed `errors` (elenco di `path` e `message`). Le azioni di creazione, aggiunta, pubblicazione e lettura sono già mappate in `DEFAULT_ENDPOINTS` di `src/integration/fdr3/utils_fdr.py` (§5.7).

### 8.2 API REST della modalità nuova: lato EC, lettura

| Operazione | Metodo e percorso | Parametri di query | Risposta | Serve a |
| --- | --- | --- | --- | --- |
| Elenco dei flussi pubblicati | `GET /organizations/{organizationId}/fdrs` | `pspId` (1..35), `flowDate`, `publishedGt` (date-time), `page` (da 1, default 1), `size` (da 1 a 1000, default 1000) | `PaginatedFlowsResponse`: `metadata` (`pageSize`, `pageNumber`, `totPage`), `count`, `data[]` con `fdr`, `pspId`, `revision`, `published`, `flowDate` | UC-FDR-002 passo 4, AC-07 |
| Dettaglio del flusso | `GET /organizations/{organizationId}/fdrs/{fdr}/revisions/{revision}/psps/{pspId}` | nessuno | `SingleFlowResponse`: `status`, `revision`, `created`, `updated`, `fdr`, `fdrDate`, `regulation`, `regulationDate`, `bicCodePouringBank`, `sender`, `receiver`, `published`, `computedTotPayments`, `computedSumPayments`, `totPayments`, `sumPayments` | UC-FDR-002 passo 5, AC-01 … AC-03 |
| Pagamenti del flusso | `GET /organizations/{organizationId}/fdrs/{fdr}/revisions/{revision}/psps/{pspId}/payments` | `page` (da 1, default 1), `size` (da 1, default 1000) | `PaginatedPaymentsResponse`: `metadata`, `count`, `data[]` con `index`, `iuv`, `iur`, `idTransfer`, `pay`, `payStatus`, `payDate` | UC-FDR-002 passo 6, AC-03 … AC-05 |

Il dettaglio del flusso lato EC non è fra le azioni di fdr3 e va aggiunto. Lo `status` del dettaglio vale `CREATED`, `INSERTED` o `PUBLISHED`. Lo schema `Sender` prevede anche `password`, mentre l'esempio di FT-03 non la riporta: va controllato che il dettaglio non la restituisca e, in ogni caso, non va registrata (RI-11).

### 8.3 Paginazione e correlazione

- le pagine sono numerate da 1 e `size` vale 1000 per default (massimo 1000 solo per l'elenco). Un flusso piccolo sta in una pagina, ma il ciclo su `metadata.totPage` va comunque implementato: se una pagina manca falliscono AC-03 e AC-04;
- per esercitare il ciclo di lettura con pochi pagamenti si usa un `size` piccolo, per esempio 2. Non si prova la paginazione della piattaforma, già verificata dalla suite fdr3: si evita che una pagina saltata dal test passi per un difetto di conversione;
- l'elenco dell'EC mostra la sola ultima revisione di ciascun flusso: dopo una nuova revisione la precedente non compare (R-03);
- l'ordinamento non è documentato: si confronta per insieme;
- l'elenco dell'EC si restringe con `pspId` e `publishedGt`, quest'ultimo in UTC e pari all'avvio della run meno un margine; senza `publishedGt` vale il default dell'inizio del mese precedente (R-19);
- il flusso si riconosce per uguaglianza esatta di `fdr`, mai per posizione o per conteggio: la coppia PSP/EC è condivisa con fdr3 e gli elenchi contengono anche flussi di altre run (RI-08).

### 8.4 Esempi di corpo

Sono dati di test coerenti con il contratto; i valori identificativi sono segnaposto (vedi Riservatezza dei dati). Corpo di creazione:

```json
{
  "fdr": "<ID_FLUSSO>",
  "fdrDate": "2026-11-16T09:30:15Z",
  "sender": {
    "type": "LEGAL_PERSON",
    "id": "<ID_MITTENTE>",
    "pspId": "<CODICE_PSP>",
    "pspName": "<NOME_PSP>",
    "pspBrokerId": "<INTERMEDIARIO_PSP>",
    "channelId": "<CANALE_PSP>",
    "password": "<PASSWORD_CANALE>"
  },
  "receiver": {
    "id": "<CODICE_EC>",
    "organizationId": "<CODICE_EC>",
    "organizationName": "<NOME_EC>"
  },
  "regulation": "<DESCRIZIONE_REGOLAMENTO>",
  "regulationDate": "2026-11-16",
  "bicCodePouringBank": "<BIC>",
  "totPayments": 3,
  "sumPayments": 300.00
}
```

Un elemento dell'elenco `payments` per l'aggiunta (se ne ripete uno per pagamento, con `index` consecutivi):

```json
{
  "index": 1,
  "iuv": "<IUV>",
  "iur": "<IUR>",
  "idTransfer": 1,
  "pay": 100.00,
  "payStatus": "EXECUTED",
  "payDate": "2026-11-16T12:00:00Z"
}
```

### 8.5 Operazioni SOAP della modalità legacy

**Convenzioni del messaggio**

- SOAP 1.1, stile `document`, `use="literal"`; l'intestazione `SOAPAction` è uguale al nome dell'operazione, senza prefissi;
- l'elemento radice del corpo sta nel namespace `http://ws.pagamenti.telematici.gov/`, mentre gli elementi figli non sono qualificati, perché lo schema non dichiara `elementFormDefault`. Nelle buste i figli compaiono quindi senza prefisso, come in quelle già usate dalla suite WISP;
- la suite WISP invia `Content-Type: application/xml` e `SOAPAction`; per le primitive FDR va verificato se il gateway richiede `text/xml` (DM-01) e se serve la chiave del gateway (DM-03);
- le credenziali viaggiano nel corpo, come password di canale o di stazione, non in intestazioni di autenticazione (R-18);
- nel WSDL del PSP due schemi definiscono elementi con lo stesso nome dell'invio. Quello usato dall'operazione, `nodoInviaFlussoRendicontazione`, sta in `nodoPerPsp.xsd` (namespace `http://ws.pagamenti.telematici.gov/`). `nodeForPsp.xsd` ha invece `nodoInviaFlussoRendicontazioneRequest` e `nodoInviaFlussoRendicontazioneResponse` in un altro namespace, che l'operazione non usa (DT-10).

**Le tre operazioni**

| Operazione | Richiesta, nell'ordine degli elementi | Risposta | Serve a |
| --- | --- | --- | --- |
| `nodoInviaFlussoRendicontazione` | `identificativoPSP`, `identificativoIntermediarioPSP`, `identificativoCanale`, `password`, `identificativoDominio`, `identificativoFlusso`, `dataOraFlusso`, `xmlRendicontazione` | `nodoInviaFlussoRendicontazioneRisposta`: `fault` (facoltativo), `esito` (testo, obbligatorio) | UC-FDR-002 passo 1, VG-B1 |
| `nodoChiediElencoFlussiRendicontazione` | `identificativoIntermediarioPA`, `identificativoStazioneIntermediarioPA`, `password`, `identificativoDominio` (facoltativo), `identificativoPSP` (facoltativo) | `fault` (facoltativo), `elencoFlussiRendicontazione` (facoltativo) con `totRestituiti` (intero obbligatorio) e `idRendicontazione` (da zero a n) composto da `identificativoFlusso` e `dataOraFlusso` | UC-FDR-001 passo 8, AC-06, AC-07 |
| `nodoChiediFlussoRendicontazione` | come l'elenco, più `identificativoFlusso` in fondo | `fault` (facoltativo), `xmlRendicontazione` (base64, facoltativo) | UC-FDR-001 passo 9, AC-01 … AC-05, AC-08 |

Tipi: `identificativo*` e `identificativoDominio` sono testi da 1 a 35 caratteri; `password` ha da 8 a 15 caratteri; `identificativoFlusso` è una stringa libera; `dataOraFlusso` è `xsd:dateTime`; `xmlRendicontazione` è `base64Binary`. Il `fault` contiene `faultCode` (stringa libera), `faultString`, `id` e, facoltativi, `description`, `serial`, `originalFaultCode`, `originalFaultString`, `originalDescription`. Quello dell'invio è un `faultBean` dello schema del PSP, quello delle letture un `ctFaultBean` dei tipi comuni, con gli stessi campi.

**Buste di esempio**

I segnaposto tra parentesi graffe seguono i nomi della configurazione (§7.4); i valori sono omessi. Invio del flusso (PSP):

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:ppt="http://ws.pagamenti.telematici.gov/">
  <soapenv:Header/>
  <soapenv:Body>
    <ppt:nodoInviaFlussoRendicontazione>
      <identificativoPSP>{psp}</identificativoPSP>
      <identificativoIntermediarioPSP>{broker_psp}</identificativoIntermediarioPSP>
      <identificativoCanale>{channel}</identificativoCanale>
      <password>{channel_password}</password>
      <identificativoDominio>{organization}</identificativoDominio>
      <identificativoFlusso>{flow_name}</identificativoFlusso>
      <dataOraFlusso>{flow_datetime}</dataOraFlusso>
      <xmlRendicontazione>{flow_xml_base64}</xmlRendicontazione>
    </ppt:nodoInviaFlussoRendicontazione>
  </soapenv:Body>
</soapenv:Envelope>
```

Elenco dei flussi (EC); la richiesta del singolo flusso è identica con l'elemento radice `ppt:nodoChiediFlussoRendicontazione` e, in coda, `<identificativoFlusso>{flow_name}</identificativoFlusso>`:

```xml
<ppt:nodoChiediElencoFlussiRendicontazione>
  <identificativoIntermediarioPA>{broker_org}</identificativoIntermediarioPA>
  <identificativoStazioneIntermediarioPA>{station}</identificativoStazioneIntermediarioPA>
  <password>{station_password}</password>
  <identificativoDominio>{organization}</identificativoDominio>
  <identificativoPSP>{psp}</identificativoPSP>
</ppt:nodoChiediElencoFlussiRendicontazione>
```

Il valore di `dataOraFlusso` nella busta deve coincidere con quello del contenuto XML.

**Decodifica del flusso ricevuto**

- `xmlRendicontazione` contiene il flusso XML codificato in base64: si decodifica, si legge come UTF-8 e si valida;
- FT-07 descrive il base64 dell'XML non compresso; la fonte normativa del Nodo non è stata consultata e la compressione resta da confermare (DM-16). Per difesa, in lettura si controlla la firma di compressione (`1f 8b` per gzip, `PK` per zip) e si decomprime se presente;
- il parser deve disabilitare la risoluzione di entità e DTD;
- la validazione contro `FlussoRiversamento_1_0_5.xsd` si fa con `lxml`, già presente come dipendenza di `zeep`.

**Esiti e fault**

`esito` è una stringa non enumerata e `faultCode` è libero: nessun contratto indica i valori. I tipi comuni definiscono `stOutcome` con i valori `OK` e `KO`, ma queste primitive non lo usano e dichiarano `esito` come `xsd:string`: l'ipotesi "OK" resta un'ipotesi. Non va assunto né "OK" né un codice particolare. La prima esecuzione approvata rileva l'esito dell'invio riuscito e la forma dell'elenco vuoto o del flusso non ancora disponibile, e li registra come evidenza (DM-04).

**Come inviare**

| Strada | Come | Pro | Contro |
| --- | --- | --- | --- |
| Busta grezza | `send_raw_soap_request` con una busta costruita da un modello | prassi della suite WISP; nessun WSDL a runtime; controllo totale su base64 e namespace | la risposta arriva senza namespace e si legge per percorsi di tag |
| Client da WSDL | `build_soap_client` con WSDL e XSD locali | richiesta e risposta tipizzate | richiede la copia versionata con import relativi (§7.1); l'indirizzo è quello del WSDL, se non si sostituisce |

Evidenza: le due strade sono entrambe disponibili nelle utility. La busta grezza è però la più vicina alla prassi del repository e non lega l'esecuzione alla copia dei contratti. **Proposta:** busta grezza per l'invio e per le letture, con WSDL e XSD come riferimento di contratto e per le validazioni offline.

### 8.6 Contenuto del flusso XML

Lo schema è `FlussoRiversamento_1_0_5.xsd`, con namespace `http://www.digitpa.gov.it/schemas/2011/Pagamenti/` e `elementFormDefault="qualified"`: tutti gli elementi sono qualificati, quindi nella radice `FlussoRiversamento` si usa il namespace predefinito.

**Testata**

| Elemento | Tipo e vincolo | Occorrenze |
| --- | --- | --- |
| `versioneOggetto` | stringa: `1.0` oppure `1.1` | 1 |
| `identificativoFlusso` | `[a-zA-Z0-9\-_]{1,35}` | 1 |
| `dataOraFlusso` | `xsd:dateTime` | 1 |
| `identificativoUnivocoRegolamento` | testo da 1 a 35 caratteri | 1 |
| `dataRegolamento` | `xsd:date` | 1 |
| `istitutoMittente` | `identificativoUnivocoMittente` (`tipoIdentificativoUnivoco` G, A o B e `codiceIdentificativoUnivoco` fino a 35 caratteri); `denominazioneMittente` da 3 a 70 caratteri | 1; denominazione 0..1 |
| `codiceBicBancaDiRiversamento` | testo da 1 a 35 caratteri | 0..1 |
| `istitutoRicevente` | `identificativoUnivocoRicevente` (tipo solo G; codice fino a 35 caratteri); `denominazioneRicevente` da 1 a 140 caratteri | 1; denominazione 0..1 |
| `numeroTotalePagamenti` | intero da 1, fino a 15 cifre | 1 |
| `importoTotalePagamenti` | decimale con esattamente due decimali, massimo 999999999.99 | 1 |
| `datiSingoliPagamenti` | vedi sotto | da 1 a n |

**Pagamento**

| Elemento | Tipo e vincolo | Occorrenze |
| --- | --- | --- |
| `identificativoUnivocoVersamento` | testo da 1 a 35 caratteri | 1 |
| `identificativoUnivocoRiscossione` | testo da 1 a 35 caratteri | 1 |
| `indiceDatiSingoloPagamento` | intero da 1 a 5 | 0..1 |
| `singoloImportoPagato` | decimale con esattamente due decimali, da 0.01 a 999999999.99 | 1 |
| `codiceEsitoSingoloPagamento` | `0`, `4`, `8` o `9` | 1 |
| `dataEsitoSingoloPagamento` | `xsd:date` | 1 |

**Modello**

```xml
<FlussoRiversamento xmlns="http://www.digitpa.gov.it/schemas/2011/Pagamenti/">
  <versioneOggetto>1.0</versioneOggetto>
  <identificativoFlusso>{flow_name}</identificativoFlusso>
  <dataOraFlusso>{flow_datetime}</dataOraFlusso>
  <identificativoUnivocoRegolamento>{regulation}</identificativoUnivocoRegolamento>
  <dataRegolamento>{regulation_date}</dataRegolamento>
  <istitutoMittente>
    <identificativoUnivocoMittente>
      <tipoIdentificativoUnivoco>G</tipoIdentificativoUnivoco>
      <codiceIdentificativoUnivoco>{sender_id}</codiceIdentificativoUnivoco>
    </identificativoUnivocoMittente>
    <denominazioneMittente>{psp_name}</denominazioneMittente>
  </istitutoMittente>
  <codiceBicBancaDiRiversamento>{bic}</codiceBicBancaDiRiversamento>
  <istitutoRicevente>
    <identificativoUnivocoRicevente>
      <tipoIdentificativoUnivoco>G</tipoIdentificativoUnivoco>
      <codiceIdentificativoUnivoco>{receiver_id}</codiceIdentificativoUnivoco>
    </identificativoUnivocoRicevente>
    <denominazioneRicevente>{organization_name}</denominazioneRicevente>
  </istitutoRicevente>
  <numeroTotalePagamenti>{tot_payments}</numeroTotalePagamenti>
  <importoTotalePagamenti>{sum_payments}</importoTotalePagamenti>
  <datiSingoliPagamenti>
    <identificativoUnivocoVersamento>{iuv}</identificativoUnivocoVersamento>
    <identificativoUnivocoRiscossione>{iur}</identificativoUnivocoRiscossione>
    <indiceDatiSingoloPagamento>{id_transfer}</indiceDatiSingoloPagamento>
    <singoloImportoPagato>{amount}</singoloImportoPagato>
    <codiceEsitoSingoloPagamento>{status_code}</codiceEsitoSingoloPagamento>
    <dataEsitoSingoloPagamento>{pay_date}</dataEsitoSingoloPagamento>
  </datiSingoliPagamenti>
</FlussoRiversamento>
```

Il valore di `versioneOggetto` accettato dalla piattaforma non è documentato oltre l'enumerazione: si propone `1.0` (DM-11).

### 8.7 Mapping fra le due modalità

La fonte è la descrizione dei campi negli OpenAPI di FT-11, che indica per ciascun campo il tag XML equivalente, integrata dall'XSD e da FT-07. Il mapping vale per entrambe le direzioni; le regole funzionali collegate sono R-07 … R-13. Serve a costruire un flusso valido per entrambe le modalità (precondizione 6) e a leggerlo.

**Testata**

| REST | Busta SOAP di invio | Contenuto XML | Note | Serve a |
| --- | --- | --- | --- | --- |
| `fdr` | `identificativoFlusso` | `identificativoFlusso` | uguale nei tre punti | AC-01, R-12 |
| `fdrDate` | `dataOraFlusso` | `dataOraFlusso` | istante; un XML senza offset è interpretato come Europe/Rome (FT-07, QF-06) | AC-02, R-11 |
| `sender.type` | | `istitutoMittente/identificativoUnivocoMittente/tipoIdentificativoUnivoco` | enumerazione sotto | precondizione 6, R-09 |
| `sender.id` | | `istitutoMittente/identificativoUnivocoMittente/codiceIdentificativoUnivoco` | | precondizione 6 |
| `sender.pspId` | `identificativoPSP` | | nel contenuto XML il codice PSP non compare: in lettura legacy si correla con il filtro dell'elenco | UC-FDR-001 passo 8, precondizione 6 |
| `sender.pspName` | | `istitutoMittente/denominazioneMittente` | facoltativo in XML, obbligatorio (3..70) in REST | precondizione 6, R-13 |
| `sender.pspBrokerId` | `identificativoIntermediarioPSP` | | | precondizione 2 |
| `sender.channelId` | `identificativoCanale` | | | precondizione 2 |
| `sender.password` | `password` | | facoltativa in REST, obbligatoria in XML (8..15); non si confronta | precondizione 2, RI-11 |
| `receiver.id` | | `istitutoRicevente/identificativoUnivocoRicevente/codiceIdentificativoUnivoco` | tipo fisso G | precondizione 6 |
| `receiver.organizationId` | `identificativoDominio` | | nel contenuto non compare | UC-FDR-001 passo 8, precondizione 6 |
| `receiver.organizationName` | | `istitutoRicevente/denominazioneRicevente` | facoltativo in XML, obbligatorio (1..140) in REST | precondizione 6, R-13 |
| `regulation` | | `identificativoUnivocoRegolamento` | | precondizione 6 |
| `regulationDate` | | `dataRegolamento` | data; la conversione la porta all'inizio del giorno italiano (FT-07) | AC-02, R-11 |
| `bicCodePouringBank` | | `codiceBicBancaDiRiversamento` | facoltativo in entrambe | precondizione 6 |
| `totPayments` | | `numeroTotalePagamenti` | | AC-03, R-06 |
| `sumPayments` | | `importoTotalePagamenti` | due decimali esatti in XML | AC-03, R-10 |
| | | `versioneOggetto` | solo XML | DM-11 |
| `revision`, `status`, `created`, `updated`, `published`, `computedTotPayments`, `computedSumPayments` | | | solo modalità nuova, senza equivalente XML | VG-A2, UC-FDR-002 AC-07, AC-03 |

**Pagamenti**

| REST | Contenuto XML | Note | Serve a |
| --- | --- | --- | --- |
| `index` | | nessun equivalente: lo assegna il PSP nella modalità nuova; il convertitore XML verso JSON lo assegna in sequenza da 1 (FT-07) | R-07 |
| `iuv` | `identificativoUnivocoVersamento` | chiave di abbinamento, insieme a `iur` | AC-04, R-07 |
| `iur` | `identificativoUnivocoRiscossione` | chiave di abbinamento, insieme a `iuv` | AC-04, R-07 |
| `idTransfer` | `indiceDatiSingoloPagamento` | da 1 a 5; facoltativo in XML, obbligatorio in REST | AC-05, VAR-03, R-13 |
| `pay` | `singoloImportoPagato` | numero in REST, esattamente due decimali in XML | AC-05, VAR-05, R-10 |
| `payStatus` | `codiceEsitoSingoloPagamento` | enumerazione sotto | AC-05, VAR-02, R-08 |
| `payDate` | `dataEsitoSingoloPagamento` | istante in REST, giorno in XML: il giorno di calendario originale va preservato | AC-05, R-11 |

**Enumerazioni**

Seguono R-09 per il tipo di mittente (il test usa solo `LEGAL_PERSON`) e R-08 per l'esito del pagamento. La prima colonna dell'esito è il testo che compare negli Esempi delle feature.

| `sender.type` | `tipoIdentificativoUnivoco` |
| --- | --- |
| `LEGAL_PERSON` | `G` |
| `ABI_CODE` | `A` |
| `BIC_CODE` | `B` |

| Esito negli Esempi | `payStatus` | `codiceEsitoSingoloPagamento` | Significato nello schema |
| --- | --- | --- | --- |
| eseguito | `EXECUTED` | `0` | pagamento eseguito |
| eseguito in stand-in | `STAND_IN` | `4` | eseguito in stand-in |
| eseguito in stand-in in assenza di RPT | `STAND_IN_NO_RPT` | `8` | eseguito in stand-in in assenza di RPT |
| eseguito in assenza di RPT | `NO_RPT` | `9` | eseguito in assenza di RPT |

**Normalizzazioni documentate**

Le regole seguenti descrivono il convertitore da XML a JSON e vengono da FT-05 e FT-07. Per la direzione opposta le fonti dicono solo che il contenuto è ricostruito (FT-06 parla di "nessuna trasformazione del payload").

- il contratto REST definisce `fdrDate` e `payDate` come istanti in UTC e dice che `regulationDate` e `payDate` preservano il giorno originale; non dice con quale fuso si determina quel giorno (QF-06);
- `dataOraFlusso` è convertita da Europe/Rome a UTC;
- `dataRegolamento` diventa una data, con inizio del giorno nell'offset italiano;
- l'indice dei pagamenti è assegnato in ordine da 1;
- i codici di esito e i tipi di mittente seguono le tabelle sopra.

## 9. Oracoli e guardie

### 9.1 Regole di confronto degli AC

Il confronto riguarda il significato dei dati (R-02) e usa il mapping di §8.7. Il valore atteso è sempre l'input generato dal test, non una lettura precedente dalla piattaforma. Le regole traducono AC-01 … AC-05 in confronti eseguibili e fissano come si osservano AC-06 e AC-07 (e AC-08 in UC-FDR-001); per le date resta aperta QF-06. Le azioni del PSP non sono AC e hanno le guardie di §9.2.

| AC | UC | Regola di confronto | Normalizzazione e tolleranza |
| --- | --- | --- | --- |
| AC-01 | entrambi | uguaglianza esatta di stringa fra l'identificativo scritto dal PSP e quello del flusso letto: in UC-FDR-001 `identificativoFlusso` del contenuto XML, in UC-FDR-002 `fdr` del dettaglio | nessuna |
| AC-02 | entrambi | `fdrDate` e `dataOraFlusso` convertiti in istanti UTC; `regulationDate` e `dataRegolamento` confrontate come date `AAAA-MM-GG` | un XML senza offset si legge come Europe/Rome; precisione al secondo, con troncamento dei decimali (DM-07, QF-06) |
| AC-03 | entrambi | numero e importo totale dichiarati uguali a quelli scritti dal PSP e a quelli ricostruiti dai pagamenti letti: in UC-FDR-001 `numeroTotalePagamenti` e `importoTotalePagamenti` del contenuto XML contro i `datiSingoliPagamenti`; in UC-FDR-002 `totPayments` e `sumPayments` del dettaglio contro i pagamenti raccolti su tutte le pagine, più `computedTotPayments` e `computedSumPayments` uguali ai dichiarati | `Decimal` a due cifre; il JSON si legge con `parse_float=Decimal` per non passare dai float (RI-05) |
| AC-04 | entrambi | insiemi di coppie `(iuv, iur)` uguali, con controllo dei duplicati contando le occorrenze | nessun ordine |
| AC-05 | entrambi | per ogni coppia: importo uguale come `Decimal`, esito mappato con §8.7, giorno dell'esito uguale, indice di trasferimento (`idTransfer`, `indiceDatiSingoloPagamento`) uguale | il giorno si confronta come data: `payDate` convertito in Europe/Rome contro `dataEsitoSingoloPagamento` (QF-06) |
| AC-06 | entrambi | tempo fra la conferma di pubblicazione o di invio e la prima lettura che contiene il flusso (UC-FDR-001: elenco legacy dell'EC; UC-FDR-002: elenco della modalità nuova), entro T; oltre T il test fallisce con l'evidenza raccolta (§11) | T da definire (§11, QF-03); l'assenza non distingue "non ancora" da "perso" |
| AC-07 | UC-FDR-001 | l'elenco legacy dell'EC, per il PSP, contiene una voce `idRendicontazione` con `identificativoFlusso` uguale a `fdr` e `dataOraFlusso` uguale a `fdrDate` pubblicati | identificativo esatto; la data come in AC-02 (QF-06) |
| AC-08 | UC-FDR-001 | il contenuto di `xmlRendicontazione`, decodificato (§8.5), è ben formato e si valida contro `FlussoRiversamento_1_0_5.xsd` con `lxml` | nessuna; il file è quello del riferimento UAT (§7.1) |
| AC-07 | UC-FDR-002 | l'elenco della modalità nuova, con `pspId` e `publishedGt`, contiene un elemento con `fdr` uguale a quello inviato e `pspId` del PSP mittente; la `revision` letta è quella attesa | revisione attesa da confermare (DM-09, QF-11); la `revision` letta serve alle richieste di dettaglio e dei pagamenti |

Le postcondizioni si verificano con gli stessi oracoli. La postcondizione 1 di UC-FDR-001 si verifica con la guardia VG-A2 (§9.2). La postcondizione 2 si verifica con AC-01 … AC-08 in UC-FDR-001 e con AC-01 … AC-07 in UC-FDR-002. La postcondizione 1 di UC-FDR-002, cioè la conservazione del flusso inviato con la legacy, non ha un oracolo proprio: la prova indiretta è la presenza del flusso nella modalità nuova dopo la conversione. Anche i passi della piattaforma (UC-FDR-001 passi 2, 4 e 7; UC-FDR-002 passi 2 e 3) sono privi di un oracolo proprio: si osservano attraverso l'esito della richiesta che li precede (le guardie di §9.2) o attraverso la lettura ripetuta di §11.

Evidenza: ogni criterio ha una regola applicabile con dati già contrattualizzati, salvo AC-02, AC-05 e AC-07 di UC-FDR-001 (fuso), AC-06 (tempo massimo) e la revisione in AC-07 di UC-FDR-002, che dipendono da risposte ancora aperte.

### 9.2 Verifiche di guardia

Le guardie controllano le azioni con cui l'attore scrive il flusso (§4.5). Non sono AC: se una guardia non è soddisfatta il test è non valido e termina subito, con l'evidenza, senza attendere la propagazione. L'esito va tenuto distinto da quello di un AC, perché dice che il prerequisito non si è realizzato e non che la conversione è difettosa (RI-22). Le azioni non si ritentano (RI-07).

| Guardia | UC | Verifica | Quando interrompe |
| --- | --- | --- | --- |
| VG-A1 | UC-FDR-001 passi 1-6 | creazione `201`, aggiunta dei pagamenti `200`, pubblicazione `200` (§8.1) | un esito diverso; in particolare `400` alla pubblicazione, che indica totali non coincidenti |
| VG-A2 | UC-FDR-001 passo 6, postcondizione 1 | lettura del flusso pubblicato lato PSP (§8.1): `status` `PUBLISHED`, `revision` uguale a 1, `computedTotPayments` e `computedSumPayments` uguali ai dichiarati | un valore diverso: la propagazione non può avvenire e si evita di attendere T |
| VG-B1 | UC-FDR-002 passo 2 | risposta SOAP all'invio (§8.5): stato HTTP 200, albero XML analizzabile, nessun `fault`, `esito` registrato. Il valore positivo di `esito` non è documentato (DM-04): finché non è rilevato la guardia controlla l'assenza di `fault` | un `fault` o una risposta non analizzabile (RI-19) |

## 10. Dati di test

### 10.1 Identificativo del flusso

- convenzione: data di oggi nel formato `AAAA-MM-GG`, codice PSP, un trattino e un suffisso numerico. La suite fdr3 usa la data UTC, il codice PSP e `%H%M%S%f`, cioè dodici cifre;
- con il codice PSP di UAT, di 11 caratteri, la lunghezza è 34, a fronte del limite di 35: va sempre verificata, perché un codice PSP più lungo di 12 caratteri la supera;
- per run ravvicinate si aggiunge una componente casuale, restando entro il limite;
- l'identificativo è unico per run e non deve essere mai stato usato dal PSP (precondizione 4); il flusso si riconosce per uguaglianza esatta (RI-08).

### 10.2 Valori base per il flusso principale (proposta)

| Dato | Valore | Origine |
| --- | --- | --- |
| codice PSP | `<CODICE_PSP>` | `global_configuration.psp` |
| intermediario PSP | `<INTERMEDIARIO_PSP>` | `global_configuration.broker_psp` |
| canale | `<CANALE_PSP>` | `global_configuration.channel` |
| codice EC | `<CODICE_EC>` | `global_configuration.organization` |
| intermediario EC | `<INTERMEDIARIO_EC>` | `global_configuration.broker_org` |
| stazione | `<STAZIONE_EC>` | `global_configuration.station` |
| `sender.type` | `LEGAL_PERSON` | `src/integration/fdr3/payloads.yaml` |
| `sender.id` | `<ID_MITTENTE>` | payloads.yaml |
| `sender.pspName` | `<NOME_PSP>` | payloads.yaml (tre caratteri o più) |
| `receiver.id` | `<CODICE_EC>` | proposta: coincide con il codice EC, a differenza del valore fisso del modello di fdr3 |
| `receiver.organizationName` | `<NOME_EC>` | payloads.yaml |
| `regulation` | `<DESCRIZIONE_REGOLAMENTO>` | payloads.yaml |
| `bicCodePouringBank` | `<BIC>` | payloads.yaml |
| numero e importo dei pagamenti | 3 pagamenti da 100.00, totale 300.00 | suite fdr3; è la riga 1 degli Esempi |

I valori della configurazione non sono stati verificati sul lato legacy (DM-02).

### 10.3 Generazione dei pagamenti

- `iuv`: `generate_iuv()` produce 15 cifre; l'unicità vale nella run;
- `iur`: `generate_uuid()` produce 32 caratteri esadecimali, dentro il limite di 35;
- `index`: da 1, consecutivo e univoco nel flusso;
- `idTransfer`: 1, salvo VAR-03;
- importi: `Decimal` con due decimali; l'importo base è 100.00 e il totale dichiarato è la somma esatta. Non si divide un totale per il numero di pagamenti con arrotondamento (RI-05);
- `payStatus`: `EXECUTED`, salvo VAR-02;
- `payDate`: mezzogiorno UTC di un giorno recente, per esempio `2026-11-16T12:00:00Z`, così il giorno coincide in UTC e in Europe/Rome (RI-06);
- in XML le stesse date sono scritte come `xsd:date`.

### 10.4 Valori concreti per le varianti

| VAR | Valori suggeriti | Note |
| --- | --- | --- |
| VAR-02 | un pagamento per ciascun esito: `EXECUTED` (0), `STAND_IN` (4), `STAND_IN_NO_RPT` (8), `NO_RPT` (9) | l'ordine non conta |
| VAR-03 | 1, 3 e 5 | |
| VAR-04 | 1; 3; 5 | in una sola richiesta di aggiunta |
| VAR-05 | 0.01; 10.00; 1234.56; 999999.99 | il totale è la somma |

Tipo e codice del mittente e banca di riversamento restano i valori base di §10.2: sono dati di input e non si confrontano.

### 10.5 Le sei righe degli Esempi e lettura dei fallimenti

Le feature di UC-FDR-001 e UC-FDR-002 hanno un solo Schema dello scenario con sei righe di Esempi, uguali nelle due direzioni (§5.6, §6.6). Questa sezione non introduce requisiti: i valori vengono da §10.2, §10.3 e §10.4, le varianti da §4.4. Descrive come sono composte le righe e che cosa dimostra il fallimento di ciascuna. Se le righe cambiano, va aggiornata.

La riga 1 è il caso base e ogni altra riga cambia una dimensione. Nelle righe 2 e 6 il numero di pagamenti (quattro) non è una scelta: lo dettano le liste dei valori, uno per esito e uno per importo, e varia insieme alla dimensione.

| Riga | Pagamenti | Importi | Esiti | Indici di trasferimento | Dimensione |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 100.00 ciascuno | `EXECUTED` | 1 ciascuno | caso base (§10.2) |
| 2 | 4 | 100.00 ciascuno | `EXECUTED`, `STAND_IN`, `STAND_IN_NO_RPT`, `NO_RPT` | 1 ciascuno | VAR-02 |
| 3 | 3 | 100.00 ciascuno | `EXECUTED` | 1, 3, 5 | VAR-03 |
| 4 | 1 | 100.00 | `EXECUTED` | 1 | VAR-04, un pagamento |
| 5 | 5 | 100.00 ciascuno | `EXECUTED` | 1 ciascuno | VAR-04, cinque pagamenti |
| 6 | 4 | 0.01, 10.00, 1234.56, 999999.99 | `EXECUTED` | 1 ciascuno | VAR-05 |

Ogni riga produce un flusso pubblicato che resta in UAT (RI-09): sei per feature, dodici per un'esecuzione completa, scritti uno alla volta (RI-10).

Il punto in cui il test si ferma dice che cosa è successo (§9.1, §9.2, RI-22):

- una guardia non soddisfatta (VG-A1, VG-A2, VG-B1): il test è non valido. La modalità di scrittura non ha accettato o non ha registrato i dati della riga e la conversione non è stata messa alla prova;
- AC-06: il flusso non è diventato disponibile entro T. L'EC non distingue "non ancora" da "perso". Da solo il fallimento non attribuisce la causa ai dati: lo fa il confronto con le altre righe, a parità di T e di coppia PSP/EC;
- AC-01 … AC-05, AC-07 e AC-08: il flusso è arrivato ma non è conforme. AC-08 (solo UC-FDR-001) dice che il documento non è valido rispetto allo schema. AC-07 dice che la voce dell'elenco non riporta ciò che il PSP ha scritto (identificativo, data e ora, revisione). Gli altri dicono che il contenuto non è equivalente. L'oracolo riporta il campo o il pagamento che differisce.

Le righe da 2 a 6 si leggono per differenza rispetto alla riga 1 e dicono qualcosa solo se la riga 1 è verde.

| Riga | Che cosa isola | Se fallisce, dimostra | Che cosa non dimostra |
| --- | --- | --- | --- |
| 1 | il percorso ibrido con dati semplici, gli stessi di fdr3 (§10.2) | che il flusso non arriva equivalente nemmeno nel caso tipico: nessun valore particolare può esserne la causa. Se sono rosse anche le righe da 2 a 6, la causa è comune a tutte (conversione non operativa per la coppia, precondizione 5 e DM-14; credenziali, precondizione 2; T troppo breve, DM-08; ambiente) e quelle righe non dicono nulla sulle varianti. Se è rossa solo questa, non è un difetto di dato: si esamina il tempo di propagazione osservato (§11) e solo dopo si riesegue la riga, come nuova esecuzione con un nuovo identificativo: le azioni non si ritentano (RI-07) e ogni flusso pubblicato resta in UAT (RI-09) | che le varianti funzionino; con pagamenti uguali non rileva un campo attribuito al pagamento sbagliato |
| 2 | la conversione dell'esito (R-08; codici 0, 4, 8, 9 di §8.7), diverso per ogni pagamento | che l'esito di almeno un pagamento non si conserva: per esempio `STAND_IN`, `STAND_IN_NO_RPT` o `NO_RPT` tradotto male, sostituito con `EXECUTED`, rifiutato o attribuito a un altro pagamento. AC-05 indica il pagamento e il codice. Le altre righe usano sempre `EXECUTED` (§10.3): un convertitore che scrivesse sempre 0 supererebbe tutte le righe tranne questa. Se la riga si ferma a una guardia (VG-A1, VG-B1), a non accettare l'esito è la modalità di scrittura e la conversione non è stata provata | un esito diverso dai quattro ammessi |
| 3 | la conservazione di `idTransfer` e `indiceDatiSingoloPagamento` con valori diversi da 1 e diversi fra i pagamenti (§8.7) | che l'indice di trasferimento non si conserva: per esempio portato a un valore predefinito, ricalcolato dalla posizione (1, 2, 3) o perso. Le altre righe usano sempre 1 (§10.3): un convertitore che ignorasse il campo le supererebbe tutte e solo questa lo scopre | i valori 2 e 4, non usati; l'indice di posizione dei pagamenti, che non si confronta (§4.2) |
| 4 | la collezione con un solo elemento (VAR-04, "uno") | che il pagamento singolo non si conserva: per esempio un elemento letto come valore anziché come elenco, un pagamento perso, totali che non tornano (AC-03, AC-04). Prima di attribuirlo al convertitore si verifica, sul documento ricevuto (UC-FDR-001) o su `count` e `metadata` della risposta (UC-FDR-002), che il test non abbia letto male l'elemento unico | il comportamento con più pagamenti, coperto dalle altre righe |
| 5 | il numero di pagamenti più alto previsto (cinque, "alcuni"), con pagamenti uguali | che il comportamento della conversione dipende dal numero di pagamenti: per esempio pagamenti troncati o raggruppati oltre una soglia, mancanti o duplicati (AC-04), totali che non si ricostruiscono (AC-03: 5 pagamenti, 500.00). In UC-FDR-002, con `size` 2 (§8.3), le pagine sono tre e l'ultima è parziale: una pagina saltata dal test fa fallire AC-03 e AC-04 anche con la conversione corretta (RI-13), e si esclude confrontando `metadata` e pagine raccolte | l'attribuzione dei campi ai singoli pagamenti, perché tutti hanno gli stessi valori e si distinguono solo per IUV e IUR; la paginazione della piattaforma, già verificata dalla suite fdr3 |
| 6 | la fedeltà di importi e totale (R-10; totale 1001244.56 come somma esatta): il minimo ammesso, un importo con zero finale, uno con migliaia e decimali, uno elevato | che importo o totale non si conservano: per esempio decimali persi o arrotondati (anche per una rappresentazione in virgola mobile), formato senza due decimali esatti (in UC-FDR-001 il documento non supera lo schema, AC-08), totali ricalcolati in modo diverso (AC-03). La riga 1 usa solo 100.00 e non lo scoprirebbe. Se la riga si ferma a VG-A1 (`400` alla pubblicazione) o a VG-A2 (totali calcolati diversi dai dichiarati), a non tornare è la modalità di scrittura e la conversione non è stata provata | importi oltre 999999.99 fino al limite dell'XML (999999999.99); più di due decimali, non ammessi (§10.6) |

Letture incrociate:

- una sola fra le righe 2, 3 e 6 rossa, con la riga 1 verde: il difetto riguarda quella dimensione (esito, indice di trasferimento, importo);
- una sola fra le righe 4 e 5 rossa: il difetto dipende dal numero di pagamenti, nell'elemento unico o a cinque;
- le righe 2 e 6 rosse e le altre verdi: il denominatore comune è il numero di pagamenti (quattro: in UC-FDR-002, con `size` 2, due pagine piene) e non l'esito né l'importo. Si indaga quindi prima la cardinalità;
- la stessa riga rossa in entrambe le direzioni: i convertitori sono due componenti distinti, quindi conviene escludere per prime le cause comuni (generatore dei dati, oracolo);
- una sola direzione rossa: la causa è nel convertitore di quella direzione (UC-FDR-001: da JSON a XML; UC-FDR-002: da XML a JSON).

Un fallimento prova una non conformità che l'EC può osservare con quei dati, non la causa interna: i meccanismi della piattaforma non sono osservabili (§4.3). A conti fatti, sei righe verdi provano la conservazione dei soli dati e delle sole combinazioni di §10.4, e nulla di più.

### 10.6 Vincoli dell'intersezione fra i contratti

Un flusso è utilizzabile per entrambe le direzioni solo se rispetta il vincolo più stretto fra REST e XML (precondizione 6).

| Campo | REST | XML | Da usare |
| --- | --- | --- | --- |
| identificativo del flusso | `[a-zA-Z0-9\-_]{1,35}` | uguale | uguale |
| codici (`id`, `pspId`, `pspBrokerId`, `channelId`, `organizationId`, `regulation`, `bicCodePouringBank`) | da 1 a 35 caratteri | `stText35`, da 1 a 35 | da 1 a 35 |
| `pspName` | da 3 a 70, obbligatorio | da 3 a 70, facoltativo | da 3 a 70, sempre presente nel flusso principale |
| `organizationName` | da 1 a 140, obbligatorio | da 1 a 140, facoltativo | da 1 a 140, sempre presente nel flusso principale |
| password di canale | `\w{8,15}` | da 8 a 15 caratteri | `\w{8,15}` |
| importo di un pagamento | numero con uno o due decimali | esattamente due decimali, da 0.01 a 999999999.99 | sempre due decimali esatti |
| importo totale | numero con uno o due decimali | esattamente due decimali, al massimo 999999999.99 | sempre due decimali esatti |
| numero totale dei pagamenti | intero da 1 | intero da 1, fino a 15 cifre | intero da 1 |
| `idTransfer` | da 1 a 5, obbligatorio | da 1 a 5, facoltativo | da 1 a 5 |
| esito del pagamento | quattro valori | 0, 4, 8, 9 | i quattro valori |

### 10.7 Dati mancanti o da verificare

| ID | Dato | Serve a | Stato | Chi può fornirlo (proposta) |
| --- | --- | --- | --- | --- |
| DM-01 | Indirizzi SOAP effettivi in UAT per l'invio e per la consultazione, e Content-Type richiesto | UC-FDR-002 passo 1; UC-FDR-001 passi 8 e 9 | due candidati per ciascuna operazione (§7.3) | team Nodo e APIM |
| DM-02 | Conferma che la coppia PSP/EC di test sia censita, gestita da FDR1 (non inoltrata a un gestore esterno), abilitata alle primitive legacy e nota alla conversione | precondizioni 1 e 3; UC-FDR-002 precondizione 7 | non verificata | team FDR e configurazione del Nodo |
| DM-03 | Chiave di sottoscrizione per le primitive SOAP: se serve e se coincide con una esistente della suite WISP (nomi omessi) o è nuova, con il nome del segreto e chi lo gestisce; validità delle password di canale e di stazione per le primitive legacy | precondizione 2 | assente | team APIM e chi gestisce i segreti |
| DM-04 | Esiti applicativi dei casi principali: valore di `esito` per l'invio riuscito; forma della risposta con elenco vuoto o flusso non ancora disponibile | VG-B1; UC-FDR-001 passi 8 e 9; §11 | non enumerati nei contratti (`esito` e `faultCode` sono `xsd:string`, §8.5); le pagine AS-IS delle tre primitive citate da FT-01 non sono state fornite | autori di FT-01, o rilevazione alla prima esecuzione |
| DM-05 | Criterio di selezione dell'elenco legacy: finestra temporale, filtro per PSP, paginazione, ordinamento | UC-FDR-001 passo 8, R-19 | non documentato | team FDR1 |
| DM-07 | Fuso e precisione per istanti e giorni | AC-02, AC-05, UC-FDR-001 AC-07, QF-06 | ipotesi Europe/Rome da FT-07 | team FDR |
| DM-08 | Tempo massimo T per direzione; in UC-FDR-001 anche la cadenza del batch di storicizzazione di FT-03, che precede la conversione | AC-06, QF-03 | non documentato; proposta in §11 | referente |
| DM-09 | Revisione attesa del flusso creato dalla conversione | UC-FDR-002 AC-07, QF-11 | ipotesi: la prima | team FDR |
| DM-11 | Modello XML di esempio (`nodoInviaFlussoRendicontazione.xml` nel progetto del convertitore da XML a JSON) e valore di `versioneOggetto` accettato | UC-FDR-002 passo 1 | non acquisito; alternativa: generare l'XML dall'XSD (§8.6) | team FDR |
| DM-13 | Dominio delle API PSP della modalità nuova in UAT: `<HOST_API_UAT>` o `<HOST_UPLOAD_UAT>` | UC-FDR-001 passi 1 … 6 | fdr3 usa `<HOST_API_UAT>`, FT-03 prescrive `<HOST_UPLOAD_UAT>` | team FDR |
| DM-14 | Abilitazione e operatività di entrambe le conversioni in UAT; la versione distribuita è un'informazione di provenienza | precondizione 5 | FT-06 cita la 0.2.11 per JSON verso XML; per XML verso JSON non è indicata | team FDR |
| DM-16 | Compressione dell'XML nel messaggio SOAP, in invio e in lettura | UC-FDR-002 passo 1; UC-FDR-001 passo 9 | FT-07 indica XML non compresso in base64; la fonte normativa non è stata consultata | rilevazione alla prima esecuzione, o specifiche SANP |

Evidenza: i dati che impediscono di eseguire sono operativi (DM-01 … DM-04 e DM-14); quelli che impediscono di chiudere gli oracoli sono DM-07 e DM-08, più DM-09 se si vuole asserire la revisione. I contratti, invece, bastano a scrivere corpi di richiesta e verifiche dei due UC.

## 11. Attesa e asincronia

### 11.1 Cosa si attende

- in UC-FDR-001 la comparsa del flusso nell'elenco legacy dell'EC, poi la richiesta del singolo flusso;
- in UC-FDR-002 la comparsa del flusso nell'elenco della modalità nuova, filtrato per `pspId` e `publishedGt`, poi dettaglio e pagamenti;
- il tempo parte dalla conferma di pubblicazione (UC-FDR-001) o di invio (UC-FDR-002); la propagazione è asincrona (R-14, DV-3).

### 11.2 Parametri di lavoro (proposta)

Sono valori tecnici, configurabili, e non vanno presentati come garanzia del servizio (R-14, R-20).

| Parametro | Valore proposto | Motivo |
| --- | --- | --- |
| intervallo di lettura | 10 secondi | prudente rispetto a cache e limiti dell'elenco legacy (§7.5) |
| timeout complessivo per direzione | 360 secondi | il convertitore da JSON a XML ritenta con attese fino a circa cinque minuti (FT-06); per XML verso JSON gli studi suggeriscono da 60 a 300 secondi. In UC-FDR-001 il valore non include la cadenza del batch di storicizzazione di FT-03, che non è documentata: se il tempo osservato la supera, il valore si alza (DM-08) |
| timeout per singola richiesta | valore esplicito, diverso da quello di fdr3 | vedi RI-12 |

Con questi valori l'attesa massima teorica è di 6 minuti per riga, quindi 36 minuti per direzione, perché le righe girano una alla volta (RI-10).

### 11.3 Regole di lettura ripetuta

- si ripetono solo letture: creazione, aggiunta, pubblicazione e invio legacy non sono idempotenti e non si ritentano mai;
- si distingue "non ancora disponibile" (elenco senza la voce, risposta di flusso non trovato) dagli errori veri (credenziali, errori del server, risposte malformate): il primo caso si ritenta, il secondo interrompe il test con l'evidenza;
- in UC-FDR-001 conviene interrogare l'elenco legacy per PSP e poi richiedere il flusso; in UC-FDR-002 si interroga l'elenco con `pspId` e `publishedGt`, poi dettaglio e pagamenti;
- il tempo di propagazione osservato va registrato nei risultati: è l'evidenza che oggi manca per fissare T (QF-03);
- se il flusso non compare entro il timeout, il test fallisce su AC-06 e riporta l'evidenza (tempo trascorso e ultime risposte). Non è un'eccezione (§4.3) e l'assenza non permette di concludere nulla sulla causa.

## 12. Implementazione

### 12.1 Riuso dal repository

Prima di scrivere codice nuovo per configurazione, chiamate REST o SOAP, autenticazione e gestione di percorsi JSON, la regola di [AGENTS.md](../AGENTS.md) impone di consultare i README di [src/utility](../src/utility/README.md). Il quadro che segue riguarda il task.

| Cosa | Dove | Come si usa | Cautele |
| --- | --- | --- | --- |
| Client REST con chiave in intestazione | `src/utility/rest`: `build_rest_client`, `build_api_key_auth_from_config` | come negli hook di `src/integration/fdr3/environment.py`: un client per l'EC (sezione `fdr`) e uno per il PSP (sezione `psp`) | l'unità del timeout (RI-12); negli hook di fdr3 un errore di costruzione del client è solo un avviso (RI-18) |
| Azioni REST di fdr3 | `src/integration/fdr3/utils_fdr.py`: `DEFAULT_ENDPOINTS`, `perform_fdr_action` | creazione, aggiunta dei pagamenti, pubblicazione e lettura del flusso pubblicato: sono il punto di partenza della scrittura del PSP in UC-FDR-001 (§5.7); in UC-FDR-002 servono elenco e pagamenti dell'EC, già presenti | manca il dettaglio lato EC; i segnaposto senza valore diventano stringa vuota e `revision` vale 1 se manca (RI-17); importare codice di una suite di integrazione in una suite e2e richiede una decisione sulla collocazione |
| Corpo di creazione | `src/integration/fdr3/payloads.yaml` | base del corpo di creazione | `regulationDate` è inviata come istante mentre il contratto vuole una data; `receiver.id` è fisso |
| Pagamenti | `_build_payments_payload` in `src/integration/fdr3/helper.py` | traccia per i pagamenti | usa `float` e divide il totale per il numero di pagamenti con arrotondamento: il totale può non coincidere con la somma (RI-05); fissa `idTransfer` e `payStatus` e ricava la data dell'esito dall'ora corrente (RI-20) |
| Invio SOAP grezzo | `src/utility/soap/soap_raw_client.py`: `send_raw_soap_request`, `get_raw_soap_text` | invio della busta e lettura di `esito`, `faultCode`, `xmlRendicontazione` | la risposta è senza namespace; il Content-Type predefinito è `application/xml` e si sovrascrive con `raw_headers`; l'intestazione del gateway passa da `extra_headers`; restituisce stato HTTP, albero XML (o `None` se non analizzabile) e intestazioni (RI-19) |
| Client SOAP da WSDL | `src/utility/soap/soap_client_factory.py`: `build_soap_client` | alternativa tipizzata | richiede la copia versionata dei contratti (§7.1) |
| Caricamento della configurazione | `load_configurations` e `load_commondata` in `src/conf/configuration.py` | file `uat.yaml` nella directory della suite, come in fdr3 | i segreti si risolvono col meccanismo del repository e non si stampano |
| Generatori di dati | `src/utility/data_generators.py`: `generate_iuv`, `generate_uuid` | IUV a 15 cifre, IUR a 32 caratteri esadecimali | entrambi rispettano il limite di 35 caratteri |
| Prassi SOAP | WISP: `src/integration/wisp/utility/constants.py`, `steps_utils.py`, `routes.py`, `utils.py` | busta grezza, `SOAPAction`, intestazione di sottoscrizione, offuscamento delle password negli allegati (`obfuscate_secrets`) | non contiene le primitive FDR; `execute_request` non imposta timeout e disattiva la verifica TLS (RI-21) |
| Validazione XML | `lxml`, dipendenza di `zeep` | validare il flusso contro l'XSD e, se utile, il corpo SOAP | `xmlschema` non è nei requisiti |

Le azioni REST, il corpo di creazione e la costruzione dei pagamenti di fdr3, con gli hook e le utility che li servono, sono il codice già prodotto da Marco Piccolo per la suite fdr3. Si sfrutta per la pubblicazione con la modalità nuova, adattato per produrre i sei flussi di FEAT_001 (§5.7).

### 12.2 Da scrivere ex novo

- l'azione REST di dettaglio lato EC e la lettura paginata dei pagamenti con numeri `Decimal`;
- il generatore del flusso, in JSON e in XML, con importi esatti e date controllate (§5.7 per il rapporto con il generatore di fdr3);
- il costruttore e il lettore delle buste SOAP per invio, elenco e richiesta del flusso;
- la decodifica del base64 e la validazione contro l'XSD;
- il confronto semantico degli oracoli e le verifiche di guardia (§9);
- l'attesa con letture ripetute (§11);
- le sezioni SOAP del file di configurazione UAT.

### 12.3 Prontezza per direzione

| Elemento | UC-FDR-001: FDR3 verso FDR1 | UC-FDR-002: FDR1 verso FDR3 |
| --- | --- | --- |
| Scrittura del PSP | REST: creazione, aggiunta e pubblicazione già implementate nelle azioni di fdr3 (§5.7); servono dati e corpi adattati (§10, RI-05, RI-20) e le guardie VG-A1 e VG-A2 (§9.2) | SOAP `nodoInviaFlussoRendicontazione`: contratto noto; busta e XML da scrivere, più la guardia VG-B1 (§9.2) |
| Lettura dell'EC | SOAP `nodoChiediElencoFlussiRendicontazione` e `nodoChiediFlussoRendicontazione`: contratto noto; buste e lettura da scrivere | REST: elenco e pagamenti già implementati in fdr3; dettaglio da aggiungere (§8.2) e paginazione completa da scrivere |
| Attesa e confronto | da scrivere: lettura ripetuta (§11), decodifica, validazione XSD e confronto dell'XML con l'input (§9) | da scrivere: lettura ripetuta (§11) e confronto di JSON e pagine con l'input (§9) |
| Da chiarire per eseguire | DM-01 (indirizzo dell'EC), DM-02, DM-03, DM-04, DM-05, DM-13, DM-14, DM-16 | DM-01 (indirizzo del PSP), DM-02, DM-03, DM-04, DM-11, DM-14, DM-16 |
| Da chiarire per chiudere gli oracoli | QF-03 (DM-08), QF-06 (DM-07) | QF-03 (DM-08), QF-06 (DM-07); QF-11 (DM-09) se si asserisce la revisione |

### 12.4 Collocazione, esecuzione e integrazione (proposta)

Il [README](../README.md) assegna ai flussi end-to-end la directory `src/e2e/<suite>`; il nome della suite è da concordare.

- **Posizione:** `src/e2e/fdr-hybrid`. Oggi le feature sono bozze in `docs/use-cases/features/fdr-hybrid`;
- **struttura suggerita:** `features/` per i feature file, `steps/` per gli step, `environment.py` per gli hook (configurazione, client REST per EC e PSP, preparazione SOAP), `uat.yaml` per la configurazione e `contracts/` per la copia dei contratti (§7.1);
- **configurazione:** le sezioni `fdr`, `psp` e `global_configuration` di `src/integration/fdr3/uat.yaml` più sezioni SOAP, per esempio `soap_psp` e `soap_ec`, con indirizzo, intestazioni ed eventuale chiave; il selettore è `TARGET_ENV=uat`;
- **selezione dei test:** la convenzione di checkout, cioè `--tags=@e2e` e `--tags=~@skip`, descritta nella sezione E2E del README. `@e2e` non è un'etichetta del profilo Gherkin e non è stato aggiunto alle feature: la decisione spetta alla stesura;
- **esecuzione:** dalla radice del repository, con interprete e formattatori della sezione E2E del README. Nessuna esecuzione è stata effettuata e ogni run richiede il piano approvato del runner.

Voce proposta per il registro [nrt-suites.json](../.github/nrt-suites.json), descritto in [nrt-process-architecture.md](nrt/nrt-process-architecture.md):

| Campo | Valore proposto |
| --- | --- |
| `id` | `fdr-hybrid` |
| `label` | `FDR hybrid E2E` |
| `behave_path` | `src/e2e/fdr-hybrid` |
| `tags` | `["@e2e", "~@skip"]` |
| `allure_subfolder` | `fdr-hybrid-tests` |
| `report_artifact` | `allure-report-fdr-hybrid` |
| `needs_playwright` | `false` |
| `envs` | `["uat"]` |
| `resource_group` | un valore condiviso con la voce `fdr3`, da introdurre su entrambe |
| `version` | `0.0.1` |

Il `resource_group` serve perché la coppia PSP/EC è condivisa con fdr3 e perché il convertitore da JSON a XML elabora un blob alla volta (RI-10). La serializzazione evita che le due suite si rallentino a vicenda e falsino i tempi di propagazione. La policy delle label di versione descritta nel README elenca gli ID del catalogo: aggiungere una suite richiede quindi di verificarne l'effetto.

### 12.5 Rilievi implementativi e rischi

- **RI-01. Costruzione della busta.** Radice con namespace, figli senza prefisso, base64 senza a capo; il Content-Type è da verificare (DM-01);
- **RI-02. Scelta del trasporto SOAP.** Si propone la busta grezza (§8.5);
- **RI-03. Decodifica e parsing sicuri.** Il contenuto ricevuto si decodifica e, per difesa, si controlla la firma di compressione; il parser disabilita entità e DTD (§8.5);
- **RI-04. Validazione offline.** Si valida contro l'XSD sia l'XML generato prima dell'invio (UC-FDR-002) sia quello ricevuto (UC-FDR-001): così un errore di costruzione si distingue da un difetto di conversione;
- **RI-05. Numeri.** Importi e totali sono `Decimal` a due cifre; il JSON si legge con `parse_float=Decimal`; il totale dichiarato è la somma esatta e non si ottiene dividendo con arrotondamento, come fa oggi fdr3. Il corpo di scrittura passa da `json_body` del client REST: la serializzazione dei `Decimal` come numeri JSON a due decimali va resa esplicita nel generatore. Il parametro `checks` di `perform_fdr_action` confronta con `!=` valori letti come `float`: per gli importi non basta;
- **RI-06. Date.** Si usa `zoneinfo` con Europe/Rome per le conversioni, istanti consapevoli del fuso al posto di `datetime.utcnow()`, confronto al secondo e `payDate` a mezzogiorno UTC per tenere allineato il giorno;
- **RI-07. Scritture non ripetibili.** Creazione, aggiunta, pubblicazione e invio legacy non sono idempotenti: nessun ritento automatico;
- **RI-08. Isolamento.** Identificativi unici per run e verifica per uguaglianza dell'identificativo, mai per conteggi degli elenchi. La coppia PSP/EC è condivisa con fdr3, le cui verifiche di paginazione contano gli elementi per PSP e data;
- **RI-09. Dati non cancellabili.** I flussi pubblicati restano in UAT (R-04): si contengono i volumi e non si cancella nulla che non sia della run. Un'esecuzione completa pubblica dodici flussi, sei per feature (§10.5);
- **RI-10. Sequenzialità.** Il convertitore da JSON a XML elabora un blob alla volta (FT-06): gli scenari ibridi non girano in parallelo fra loro né durante altre pubblicazioni sulla stessa coppia;
- **RI-11. Log e segreti.** Non si registrano password, chiavi di sottoscrizione né il corpo dell'invio SOAP, che contiene la password del canale. Il dump HTTP di fdr3 (`DUMP_HTTP=1`) stampa richieste e risposte intere: non va usato con i messaggi di questa suite senza mascheratura. Va controllato anche che il dettaglio REST non restituisca la password (§8.2);
- **RI-12. Timeout.** Il client REST legge secondi, la configurazione di fdr3 riporta `5000`: si definisce un timeout esplicito per richiesta. Aggiunta e pubblicazione possono incorrere nel timeout dell'ingress in UAT (FT-03, DM-13);
- **RI-13. Paginazione.** Con `size` di default un flusso piccolo sta in una pagina: per esercitare il ciclo sulle pagine si usa un `size` piccolo (§8.3). La lettura di tutte le pagine è un obbligo del passo 6 di UC-FDR-002: una pagina saltata fa fallire AC-03 e AC-04;
- **RI-14. Scenari autosufficienti.** Lo step "che lo scenario … è stato eseguito con successo" di fdr3 riesegue i passi dello scenario richiamato: non si replica in flussi con attese asincrone;
- **RI-15. Precondizioni senza controllo documentato.** Per le precondizioni 1, 3 e 5 di entrambi gli UC e per la 7 di UC-FDR-002 non esiste un controllo documentato. Un rifiuto per anagrafica si distingue da un difetto di conversione solo dall'esito di errore. Nelle feature sono `Dato`; come accertarle o prepararle va deciso nel codice;
- **RI-16. Nomi.** Esistono già le suite `fdr` (legacy) e `fdr3`, distinte nel README: la nuova suite usa un identificativo proprio e non sostituisce nessuna delle due;
- **RI-17. Segnaposto e revisione.** `perform_fdr_action` sostituisce con una stringa vuota i segnaposto privi di valore e usa `1` come `revision` se manca. In UC-FDR-002 la revisione si legge dall'elenco e un valore predefinito non deve poter far passare un controllo (QF-11); un segnaposto vuoto è un errore del test, non un dato;
- **RI-18. Client non inizializzati.** Gli hook di fdr3 registrano come avviso l'errore di costruzione dei client REST e proseguono: un client mancante emerge alla prima richiesta, lontano dalla causa. La nuova suite si ferma subito se mancano la configurazione o la chiave del client che usa;
- **RI-19. Risposte SOAP.** `send_raw_soap_request` restituisce stato HTTP, albero XML e intestazioni, e l'albero è `None` quando la risposta non è XML valido. Prima di classificare il caso come "non ancora disponibile" (§11.3) si controllano stato, albero e presenza del `fault`. Una risposta non analizzabile è un errore;
- **RI-20. Generatore dei pagamenti.** Oltre a `float` (RI-05), il generatore di fdr3 fissa `idTransfer` a 1 e `payStatus` a `EXECUTED`. Riparte inoltre da 1 per gli indici a ogni chiamata e ricava la data dell'esito dall'ora corrente UTC meno `i` giorni, con `i` da 0. VAR-02, VAR-03 e i giorni controllati di §10.3 richiedono un generatore nuovo o esteso (§5.7);
- **RI-21. Prassi di WISP da non copiare.** `execute_request` (`src/integration/wisp/utility/utils.py`) non imposta timeout e disattiva la verifica TLS (`verify=False`). La nuova suite usa `send_raw_soap_request`, che la mantiene attiva per default: un errore di certificato si diagnostica, non si aggira. Di WISP si può riprendere `obfuscate_secrets`, che nasconde le password (elemento XML e campo JSON) e un formato particolare della chiave del gateway, ma solo negli allegati Allure: va adattato ai tag delle primitive FDR;
- **RI-22. Guardie e AC.** Una guardia non soddisfatta (§9.2) e un AC fallito sono esiti diversi. La prima dice che un prerequisito non si è realizzato, il secondo che la conversione ha prodotto un contenuto o un tempo non conformi. I risultati devono distinguerli, per esempio con uno stato "non valido" per le guardie.

## 13. Questioni aperte e stato delle feature

### 13.1 Questioni funzionali aperte

Sono le sole domande funzionali che incidono sui due flussi principali, in ordine di impatto. I dubbi implementativi (endpoint, credenziali, formato dei messaggi, polling) non vanno posti al referente e sono raccolti in questo documento (§10.7, §12.5). Non serve nemmeno una risposta sul meccanismo interno con cui la piattaforma avvisa la modalità legacy: il test è black-box e non lo usa. La colonna delle ipotesi dice che cosa assumono le feature e il codice nell'attesa della risposta. I registri dei run sono in `docs/use-cases/workflow-runs/fdr-e2e-ibrido/<UC>/20261119-01/`.

| ID | Domanda | Dove incide | Ipotesi di lavoro | Registro del run |
| --- | --- | --- | --- | --- |
| QF-03 | Qual è il tempo massimo T di propagazione, per direzione, o con quale criterio si fissa? | AC-06 (UC-FDR-001 passo 7, UC-FDR-002 passo 3), che resta incompleto | timeout tecnico di 360 secondi con lettura ogni 10 secondi, da non presentare come garanzia (§11.2) | Q-001 |
| QF-06 | Con quale fuso si interpretano e si confrontano l'istante del flusso e i giorni di regolamento e di esito, e con quale precisione? | AC-02 e AC-05 di entrambi gli UC; AC-07 di UC-FDR-001 (data e ora); la parte temporale degli oracoli | istanti confrontati in UTC, con un XML senza offset letto come Europe/Rome; giorni confrontati come date, portando `payDate` a Europe/Rome; precisione al secondo (§8.7, §9.1) | Q-002 |
| QF-11 | Qual è la revisione attesa del flusso creato dalla conversione e va asserita? | AC-07 di UC-FDR-002; nessun blocco: ipotesi di lavoro | la prima; la revisione si legge dall'elenco e si confronta con 1 solo dopo la conferma | Q-005, solo UC-FDR-002 |
| senza sigla | Quale esito osservabile attesta che il flusso pubblicato non è più modificabile né cancellabile? | postcondizione 3 di entrambi gli UC | nessuna: le feature non la verificano | Q-003 |
| senza sigla | Quale identificativo e quale formulazione per il JTBD? | intestazione di entrambi gli UC | segnaposto `JTBD-{NNN}`. Formulazione proposta, da validare: "Quando pubblico o scarico un flusso di rendicontazione e la controparte usa l'altra modalità, voglio che il flusso arrivi completo e corretto, così da non dover coordinare un passaggio comune" | |

### 13.2 Stato delle feature

Le due feature sono in stato di bozza (19/11/2026). Non sono pronte per lo sviluppo finché QF-03, QF-06 e QF-11 non sono chiuse o rinunciate e non è deciso come trattare la postcondizione 3. Ciascuna ha una definizione di scenario (il limite del profilo Gherkin è 12) e sei righe espanse, senza celle vuote, segnaposto di dato, valore di T o numero di revisione. I controlli, secondo i registri dei run, sono stati fatti per lettura contro il profilo e con `behave --lang-help it`; nessun parser Python e nessuna esecuzione.

| Elemento | UC-FDR-001 (FEAT_001) | UC-FDR-002 (FEAT_002) |
| --- | --- | --- |
| Precondizioni | 1-6 coperte come `Dato`/`E` | 1-7 coperte come `Dato`/`E` |
| Passi | 1-6, 8 e 9 coperti; 7 parziale | 1, 2, 4, 5 e 6 coperti; 3 parziale |
| AC coperti | AC-01, AC-03, AC-04, AC-08 | AC-01, AC-03, AC-04 |
| AC parziali | AC-02, AC-05, AC-06, AC-07 | AC-02, AC-05, AC-06, AC-07 |
| Postcondizione 1 | coperta (VG-A2) | parziale: prova indiretta |
| Postcondizione 2 | parziale | parziale |
| Postcondizione 3 | non coperta | non coperta |
| Motivi della bozza | QF-03, QF-06, postcondizione 3 | QF-03, QF-06, QF-11, postcondizione 3 |

### 13.3 Divergenze fra le fonti

| ID | Punto | Fonti | Effetto |
| --- | --- | --- | --- |
| DV-3 | Momento e natura della storicizzazione: "durante la pubblicazione" in FT-01, asincrona dopo la pubblicazione in FT-03 | FT-01, FT-03 | R-14: si assume FT-03, più dettagliata; il tempo di propagazione resta non documentato |
| DV-5, DT-9 | Esempi di FT-03 non coerenti con le regole e con il contratto: stato "creato" in letture di flussi pubblicati; tipo di mittente con nomi diversi fra tabella dei dati ed esempi; importi come testo; numero di pagine non coerente con elementi e dimensione; data di regolamento ora come data, ora come istante | FT-03, FT-11 | gli esempi non sono oracolo né dati di test: fanno fede i contratti (FT-11) |
| DT-1 | Indirizzi SOAP: `nodo-auth/node-for-psp` e `nodo-auth/node-for-pa` nel WSDL contro `nodo/node-for-psp` e `nodo-auth/nodo-per-pa` nella suite WISP | FT-11, suite WISP | DM-01 |
| DT-2 | Server dichiarati negli OpenAPI del riferimento UAT: indicano il dominio dell'ambiente DEV | FT-11 | non usare i contratti per ricavare l'ambiente (§7.2) |
| DT-3 | Dominio delle API PSP in UAT: `<HOST_UPLOAD_UAT>` in FT-03, `<HOST_API_UAT>` nella configurazione di fdr3 | FT-03, `uat.yaml` | DM-13 |
| DT-10 | Elementi con lo stesso nome dell'invio in due namespace: `nodoInviaFlussoRendicontazione` in `nodoPerPsp.xsd` (`http://ws.pagamenti.telematici.gov/`), usato dall'operazione, e `nodoInviaFlussoRendicontazioneRequest` e `…Response` in `nodeForPsp.xsd` (`http://pagopa-api.pagopa.gov.it/node/nodeForPsp.xsd`), non usati dall'operazione | FT-11 | costruire la busta con il primo (§8.5) |

## 14. Fonti e tracciabilità

| ID | Fonte | Ruolo | Note |
| --- | --- | --- | --- |
| FT-01 | Design Review [Flussi di Rendicontazione] | cornice: casi d'uso, vincoli, fasi | stato in lavorazione; la sezione sugli SLA è un modello non compilato |
| FT-02 | FdR-1 [Flussi di Rendicontazione] | componenti e dati della modalità legacy | senza intestazione |
| FT-03 | FdR-3 [Flussi di Rendicontazione] | contratto business della modalità nuova | contiene esempi incoerenti (DV-5) |
| FT-04 | FdR-JSON-to-XML (Fase3 - Fase 1) [Flussi di Rendicontazione] | requisito di trasparenza; direzione nuova verso legacy | disegno in parte superato; intestazione non compilata |
| FT-05 | FdR-XML-to-JSON (Fase1 - Fase3) [Flussi di Rendicontazione] | direzione legacy verso nuova | intestazione non compilata |
| FT-06 | Studio di Contesto - FdR-JSON-to-XML | studio per l'automazione sul convertitore | descrive componenti interni; non è un contratto |
| FT-07 | Studio di Contesto - FdR-XML-to-JSON | studio per l'automazione sul convertitore | descrive componenti interni; non è un contratto |
| FT-08 | FdR API Assistenza | finestra di consultazione dell'EC (R-19) | stato in lavorazione |
| FT-11 | Repository pagopa-api, riferimento UAT SANP3.13.0 (commit `969833a`) | contratti pubblicati: OpenAPI REST, WSDL e XSD SOAP | fa fede per formati e vincoli |
| FT-12 | Suite [fdr3](../src/integration/fdr3) | copertura attuale e codice da riusare | analisi statica, non eseguita |
| FT-13 | [Template UC](../.github/skills/uc-to-feature/UC-template.md) e [workflow UC](use-cases/uc-workflow.md) | struttura degli UC e delle feature | |

Le esportazioni Confluence (da FT-01 a FT-08) sono fonti fornite, non validate: stato e versione non sono verificabili e alcune intestazioni sono modelli non compilati.

Che cosa è già risolto:

- i contratti SOAP (WSDL e XSD) e il mapping dei campi fra le due modalità sono stati acquisiti dal repository pagopa-api, riferimento UAT SANP3.13.0 (commit `969833a`): questo documento li usa;
- i contratti sono stati riletti in sola lettura il 18/11/2026 e coincidono con quanto qui descritto (§7.1);
- esiti e parametri delle API REST della modalità nuova sono definiti dagli OpenAPI dello stesso riferimento;
- restano aperti l'esito positivo dell'invio legacy, la forma della risposta con elenco vuoto o flusso non ancora disponibile e il criterio di selezione dell'elenco legacy (DM-04 e DM-05).

## 15. Riepilogo e considerazioni finali

A conti fatti, il task si riduce a due UC speculari, uno per direzione, che chiudono il percorso dal lato dell'EC e confrontano il significato dei dati. Le parti comuni (§4) pesano più di quelle specifiche e si scrivono una volta sola. La suite fdr3 copre già il lato REST: il valore nuovo sta nell'attraversare il confine fra le modalità, con attesa asincrona e confronto del contenuto. I contratti per i due flussi ci sono e sono precisi; quanto manca è quasi tutto operativo (indirizzi, credenziali, abilitazioni) o riguarda l'esito positivo della legacy. Il lavoro nuovo da scrivere è la parte SOAP, l'attesa asincrona e il confronto dei contenuti (§12.2). La pubblicazione con la modalità nuova si appoggia invece al codice di fdr3 di Marco Piccolo (§5.7).

Considerazioni finali:

1. nel perimetro del percorso di successo restano aperte tre sole questioni funzionali: il tempo massimo di propagazione (QF-03), fuso e precisione delle date (QF-06) e la revisione attesa dopo la conversione (QF-11). Ciascuna ha un'ipotesi di lavoro (§13.1). Finché restano aperte, le feature restano in bozza (§13.2);
2. gli AC sono otto in UC-FDR-001 e sette in UC-FDR-002 e sono verificabili con i dati già contrattualizzati, salvo la revisione attesa in UC-FDR-002 AC-07 (QF-11). Restano incompleti AC-02 e AC-05 (fuso e precisione, che toccano anche la data in UC-FDR-001 AC-07) e AC-06 (tempo massimo) fino alle risposte;
3. prima di scrivere codice conviene chiudere DM-01 … DM-04 e DM-14: senza indirizzi, chiavi e abilitazioni la prima esecuzione non ha senso;
4. la prima esecuzione approvata va pensata anche come rilevazione. Si raccolgono l'esito positivo dell'invio, che serve alla guardia VG-B1, la forma dell'elenco vuoto (DM-04), la compressione (DM-16), i tempi di propagazione con la cadenza del batch di storicizzazione (DM-08) e la revisione attesa (DM-09);
5. nella stesura del codice il riuso va dichiarato. Client REST e SOAP, generatori e configurazione esistono già, insieme alle azioni di fdr3 di Marco Piccolo (§5.7, §12.1). Restano da scrivere gli elementi di §12.2, comprese le guardie di §9.2, con le cautele RI-17 … RI-22;
6. le feature sono bozze; nessun codice è stato scritto e nessuna chiamata verso gli ambienti è stata eseguita.
