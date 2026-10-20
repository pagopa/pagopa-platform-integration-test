# Checkout - raccolta dati di test

## Scopo e condizioni di utilizzo

Raccolta di dati per provare il pagamento di un avviso, la selezione del
prestatore di servizi di pagamento (PSP), la gestione degli errori, la
validazione dei campi e la navigazione nel Checkout.

Utilizzare questi dati esclusivamente in ambienti di test, mai in produzione.
Tutti i dati di questo documento valgono indifferentemente per gli ambienti
**dev** e **uat**: non occorrono valori diversi in base all'ambiente.
La disponibilita di carte, PSP, metodi e comportamenti simulati dipende dalla
configurazione dell'ambiente. Le associazioni PSP/carta e i dati negativi
indicati come **da verificare** sono candidati di prova, non garanzie di esito.

Non utilizzare dati personali o carte reali. Questa raccolta non contiene
password o credenziali di accesso. Per le prove autenticate occorre disporre
separatamente di un'utenza di test autorizzata.

## Ente creditore e lingua

| Dato | Valore | Significato e utilizzo |
| --- | --- | --- |
| Codice fiscale ente creditore | `77777777777` | Identifica l'ente di test da abbinare al codice avviso per verificarne i dati e avviare il pagamento. E composto da 11 cifre e non va utilizzato come codice fiscale personale del pagatore. |
| Lingua | `it` | Seleziona l'italiano per provare etichette, messaggi e interazioni del Checkout. |

## Codici avviso

### Avvisi generabili tramite prefisso

Nel mock di test, **qualunque codice avviso numerico che inizi con uno dei
prefissi seguenti e abbia 18 cifre totali e funzionante** per la famiglia
indicata. Il prefisso occupa 5 cifre: aggiungere quindi **13 cifre arbitrarie
da 0 a 9**.

Usare il CF ente `77777777777`. La regola riguarda l'avviso, non garantisce
il completamento del pagamento con qualunque carta o PSP.

| Prefisso | Formato completo | Famiglia di pagamento | Possibile utilizzo |
| --- | --- | --- | --- |
| `30200` | `^30200[0-9]{13}$` | Multibeneficiario, conti postali per entrambi i beneficiari | Provare verifica, riepilogo e pagamento di avvisi con ripartizione tra beneficiari su conti postali. |
| `30201` | `^30201[0-9]{13}$` | Multibeneficiario, primo conto postale e secondo bancario | Provare pagamenti con beneficiari che utilizzano tipi di conto differenti. |
| `30202` | `^30202[0-9]{13}$` | Multibeneficiario, primo conto bancario e secondo postale | Provare la diversa ripartizione tra beneficiari e la selezione o l'ordinamento dei PSP compatibili. |

I formati sono espressioni regolari: `[0-9]{13}` significa esattamente
13 cifre numeriche. Il codice completo va conservato come stringa, senza
spazi, separatori o conversioni numeriche.

**Riutilizzo:** un avviso gia pagato non puo essere pagato nuovamente senza
pulizia dell'ambiente. Generare un codice diverso oppure verificare che
l'avviso scelto non sia gia stato pagato.

### Avviso completo disponibile

| Codice avviso | CF ente | Significato e utilizzo | Condizione |
| --- | --- | --- | --- |
| `302042025112600001` | `77777777777` | Codice di 18 cifre della famiglia `30204`, monobeneficiario; utilizzabile come candidato per inserimento dati, riepilogo e navigazione del flusso. | Verificare disponibilita e stato del pagamento nell'ambiente prima dell'uso. |

## Carte di test

Il **PAN** e il numero della carta; la **scadenza** e espressa come mese/anno
(`MM/AA`); il **CVV** e il codice di sicurezza; l'**intestatario carta**
corrisponde al campo "Intestata a". I dati per compilare ciascuna carta
comprendono tutti e quattro i campi, riportati insieme nella tabella.

| Circuito | PAN | Scadenza | CVV | Intestatario carta | Possibile utilizzo |
| --- | --- | --- | --- | --- | --- |
| Mastercard | `5255000260000014` | `12/30` | `123` | `Test test` | Inserimento dati carta e prove di pagamento NPG con un PSP compatibile, tra cui Postepay e Worldline. |
| Visa | `4242424242424242` | `12/30` | `123` | `Test test` | Inserimento dati carta e prove di pagamento NPG con Worldpay o Worldline, secondo la configurazione disponibile. |

Inserire i PAN senza spazi. La scadenza deve essere ancora futura al momento
della prova. La compatibilita di una carta non conferma automaticamente
disponibilita del PSP o buon esito dell'autorizzazione.
L'intestatario `Test test` e un nome sintetico per compilare il campo senza
usare dati personali; resta da verificarne l'accettazione con il gateway
utilizzato.

| Dato complementare | Valore | Significato e utilizzo | Condizione |
| --- | --- | --- | --- |
| Email | `ecommerce-test-mailgroup@pagopa.it` | Candidato per inserimento e conferma email e ricezione delle notifiche di pagamento. | Verificare autorizzazione all'uso e accesso alla casella se si controlla la ricezione. |
| Email | `mail@pagopa.it` | Candidato per compilazione e conferma dei campi email. | Non presumere che la casella sia disponibile o che le notifiche siano consultabili. |

## Metodi di pagamento e PSP

| Dato | Valore | Significato e utilizzo | Condizione |
| --- | --- | --- | --- |
| Metodo carta | `CP` | Codice tecnico del metodo carta di credito/debito, per selezionare il pagamento con carta. | Verificare che il metodo sia abilitato. |
| Metodo PayPal | `PPAL` | Codice candidato per selezionare PayPal e provare scelta, modifica e ordinamento del PSP. | Codice e disponibilita da verificare nell'ambiente. |
| ID PSP Postepay | `PPAYITR1XXX` | Identificativo candidato per selezionare Postepay. | Associazione al PSP da verificare. |
| ID PSP Worldline | `BNLIITRR` | Identificativo candidato per selezionare Worldline. | Associazione al PSP da verificare. |
| ID PSP Worldpay | `WOLLNLB1` | Identificativo candidato per selezionare Worldpay. | Associazione al PSP da verificare. |
| ID PSP per PayPal | `BCITITMM` | Identificativo candidato per selezionare un PSP nel flusso PayPal. | Associazione al metodo e disponibilita da verificare. |
| Configurazione lista PSP | `enablePspPage=true` | Abilitazione della pagina di selezione PSP per provare il flusso carta o wallet salvato e la navigazione di ritorno. | Disponibilita e comportamento del flag da verificare nell'ambiente. |

Il nome commerciale e l'identificativo tecnico sono dati distinti.
La grafia `Wordline` e una variante da uniformare a **Worldline**, non un
ulteriore PSP.

### Combinazioni candidate per prove di pagamento

Queste combinazioni permettono di preparare prove complete, anche con utente
autenticato. **Le associazioni complete sono da verificare nell'ambiente.**
Completare il prefisso con 13 cifre e usare un avviso non gia pagato.

| PSP | Prefisso avviso | CF ente | PAN | Scadenza | CVV | Intestatario carta | ID PSP |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Postepay` | `30200` | `77777777777` | `5255000260000014` | `12/30` | `123` | `Test test` | `PPAYITR1XXX` |
| Worldline | `30201` | `77777777777` | `5255000260000014` | `12/30` | `123` | `Test test` | `BNLIITRR` |
| `Worldpay` | `30201` | `77777777777` | `4242424242424242` | `12/30` | `123` | `Test test` | `WOLLNLB1` |

## Avvisi per prove di errore

Usare il CF ente `77777777777`. Gli intervalli comprendono entrambi gli
estremi e contengono codici avviso di 18 cifre.

**Da verificare:** la configurazione del mock deve associare questi codici
agli errori indicati. La corretta lunghezza da sola non garantisce l'errore
desiderato. Gli intervalli seguenti non sono avvisi per pagamenti riusciti.

| Codice errore previsto | Avviso iniziale | Avviso finale | Significato e utilizzo | Attesa indicativa |
| --- | --- | --- | --- | --- |
| `PAA_PAGAMENTO_SCONOSCIUTO` | `302400000000000000` | `302409999999999999` | Provare la gestione di un avviso non riconosciuto e le indicazioni di assistenza. | `5` secondi |
| `PAA_PAGAMENTO_SCADUTO` | `302990000000000000` | `302999999999999999` | Provare il blocco del pagamento di un avviso scaduto. | `60` secondi |
| `PPT_STAZIONE_INT_PA_TIMEOUT` | `302980000000000000` | `302989999999999999` | Provare la gestione del timeout della stazione dell'ente creditore. | `60` secondi |
| `PAA_PAGAMENTO_DUPLICATO` | `302950100443009424` | `302950100443009424` | Provare il rifiuto di un pagamento duplicato usando il singolo codice indicato. | `5` secondi |
| `PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE` | `302970000000000000` | `302979999999999999` | Provare la gestione dell'ente creditore non raggiungibile e la visualizzazione del codice di assistenza. | Non definita |

Le attese sono valori indicativi per osservare la comparsa del messaggio,
non SLA o garanzie sui tempi di risposta. La scadenza dell'avviso e distinta
dalla scadenza di una transazione o di un token di pagamento.

### Messaggi associati agli errori

Testi candidati per controllare comprensibilita, localizzazione e coerenza
della comunicazione all'utente; la corrispondenza esatta va verificata
sulla versione del Checkout utilizzata.

| Errore | Intestazione | Corpo |
| --- | --- | --- |
| Avviso sconosciuto | Non riusciamo a trovare l’avviso | L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore. |
| Avviso scaduto | L’avviso è scaduto e non è più possibile pagarlo | Contatta l’Ente per maggiori informazioni. |
| Timeout | Si è verificato un errore imprevisto | Riprova, oppure contatta l’assistenza |
| Pagamento duplicato | Questo avviso è stato già pagato! | Vuoto: assenza di testo aggiuntivo da verificare |
| Ente irraggiungibile | L’Ente Creditore sta avendo problemi nella risposta | Codice di errore per l'assistenza |

## Dati per validazione dei campi

Questi input sono deliberatamente invalidi. Servono a provare i controlli
prima della verifica dell'avviso o della prosecuzione del pagamento.
I messaggi sono testi candidati da verificare sulla versione utilizzata.

| Campo | Dato di prova | Motivo / possibile utilizzo | Messaggio candidato |
| --- | --- | --- | --- |
| Codice avviso | `12345678901234567890` | 20 cifre: superamento della lunghezza di 18 cifre. | `Inserisci 18 cifre` |
| Codice avviso | `12345678` | 8 cifre: lunghezza insufficiente. | `Inserisci 18 cifre` |
| Codice avviso | `aaabbbcccdddeeefff` | 18 caratteri alfabetici: rifiuto di un codice non numerico. | `Inserisci 18 cifre` |
| CF ente | `1234567890` | 10 cifre: lunghezza inferiore alle 11 richieste. | `Inserisci 11 cifre` |
| CF ente | `123456789012345` | 15 cifre: lunghezza superiore alle 11 richieste. | `Inserisci 11 cifre` |
| CF ente | `aaabbbcccdd` | 11 caratteri alfabetici: rifiuto di un CF ente non numerico. | `Inserisci 11 cifre` |
| Email | `aaaaaaaaaa` | Assenza di separatore `@` e dominio. | `Inserisci un indirizzo email valido` |
| Email | `aaaaaaaaaa@` | Assenza del dominio dopo `@`. | `Inserisci un indirizzo email valido` |
| Email | `mail@gmail` | Dominio senza suffisso: prova della politica di validazione email dell'applicazione. | `Inserisci un indirizzo email valido` |
| Email e conferma | Due indirizzi validi ma diversi | Controllo della corrispondenza tra i due campi. | `Gli indirizzi email non coincidono` |
| Codice avviso, CF ente, email o conferma | Campo vuoto | Controllo dell'obbligatorieta: lasciare vuoto un solo campo alla volta e compilare gli altri correttamente. | `Campo obbligatorio` |

## Percorsi e dati per prove dell'interfaccia

I percorsi sono relativi alla base URL del Checkout dell'ambiente scelto.
Servono come riferimenti per prove di navigazione e riconoscimento delle
pagine; disponibilita e comportamento vanno verificati sulla versione utilizzata.

| Percorso | Significato e possibile utilizzo |
| --- | --- |
| `/` | Homepage: avvio del flusso e ritorno alla pagina iniziale. |
| `/inserisci-dati-avviso` | Inserimento del codice avviso e del CF ente; prove di campi obbligatori e accesso diretto. |
| `/dati-pagamento` | Riepilogo dei dati dell'avviso prima della prosecuzione al pagamento. |
| `/inserisci-email` | Inserimento e conferma email; prove di formato e corrispondenza. |
| `/scegli-metodo` | Scelta o modifica del metodo di pagamento. |
| `/inserisci-carta` | Inserimento di PAN, scadenza, CVV e intestatario. |
| `/lista-psp` | Selezione del PSP e prove di ordinamento per nome o commissione. |
| `/riepilogo-pagamento` | Riepilogo finale e modifica delle scelte prima del pagamento. |

### Coppie per prove di navigazione indietro

Le coppie seguenti sono riferimenti di comportamento da verificare, non
garanzie sulla cronologia del browser.

| Pagina di partenza | Pagina di ritorno | Possibile utilizzo |
| --- | --- | --- |
| `/inserisci-dati-avviso` | `/` | Ritorno alla homepage, anche dopo accesso diretto alla pagina di inserimento. |
| `/dati-pagamento` | `/inserisci-dati-avviso` | Ritorno alla compilazione dell'avviso. |
| `/inserisci-email` | `/dati-pagamento` | Ritorno al riepilogo dell'avviso. |
| `/scegli-metodo` | `/inserisci-email` | Ritorno ai dati di contatto. |
| `/inserisci-carta` | `/scegli-metodo` | Ritorno alla scelta del metodo. |
| `/lista-psp` | `/scegli-metodo` | Ritorno alla scelta del metodo dal flusso PSP. |

Dopo la modifica del metodo dal riepilogo finale, una sequenza candidata
per provare l'assenza di loop e:
`/scegli-metodo` → `/inserisci-email` → `/dati-pagamento` →
`/inserisci-dati-avviso` → `/`, senza ripetizioni.

### Etichette e opzioni

I testi seguenti aiutano a identificare controlli e azioni da provare.
La grafia esatta puo variare con la versione e la localizzazione.

| Valore | Significato e possibile utilizzo |
| --- | --- |
| `Accedi` | Avvio dell'autenticazione; controllo della disponibilita dell'accesso durante il pagamento. |
| `Inserisci tu i dati` | Avvio dell'inserimento manuale dell'avviso. |
| `Continua` | Validazione dei dati inseriti e passaggio alla fase successiva. |
| `Vai al pagamento` | Prosecuzione dal riepilogo dell'avviso al pagamento. |
| `Carte di Credito` | Scelta del pagamento con carta. |
| `Indietro` | Ritorno alla fase precedente e controllo dell'assenza di loop o uscite indesiderate. |
| `Modifica metodo di pagamento` | Cambio del metodo prima della conferma finale. |
| `ordina per commissione` | Prova dell'ordinamento dei PSP per costo, crescente e decrescente. |
| `ordina per nome` | Prova dell'ordinamento alfabetico dei PSP. |
| `ordina per importo` | Opzione candidata per ordinare i PSP secondo l'importo della commissione. |
| `Codice Avviso` | Campo per il codice numerico di 18 cifre. |
| `Codice Fiscale Ente Creditore` | Campo per il CF numerico di 11 cifre dell'ente, non del pagatore. |
| `Indirizzo email`; `Indirizzo Email` | Varianti di etichetta del campo email, utili per controlli di localizzazione e uniformita. |
| `Ripeti di nuovo` | Campo di conferma email, per controlli di corrispondenza e obbligatorieta. |
