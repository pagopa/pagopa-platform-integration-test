# language: it
@fdr3_009_Verifica_Paginazione_Organizzazione
Funzionalità: Verifica paginazione per le API organizzazione

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_009_01
  Scenario: Creazione del flusso di rendicontazione per test paginazione
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_009_02
  Scenario: Inserimento pagamenti per test paginazione
    Dato che il PSP deve inviare 100 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 20
    E che lo scenario "Creazione del flusso di rendicontazione per test paginazione" è stato eseguito con successo
    Quando il PSP aggiunge 100 pagamenti la cui somme è 20 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_009_03
  Scenario: Pubblicazione del flusso per test paginazione
    Dato che lo scenario "Inserimento pagamenti per test paginazione" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Pubblicazione" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200

  @runnable
  @fdr3_009_04
  Scenario: Verifica paginazione FdR pubblicati pagina 1
    Dato che lo scenario "Pubblicazione del flusso per test paginazione" è stato eseguito con successo
    E la configurazione psp è valorizzata come pspId nei parametri di query
    E l'organizzazione aggiunge ieri come createdGt nei parametri di query
    E l'organizzazione aggiunge 1 come page nei parametri di query
    E l'organizzazione aggiunge 1 come size nei parametri di query
    Quando l'organizzazione invia la richiesta di "recupero di tutti i fdr pubblicati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200
    E l'organizzazione riceve pagina 1 con 1 elementi come risposta

  @runnable
  @fdr3_009_05
  Scenario: Verifica paginazione FdR pubblicati pagina 2
    Dato che lo scenario "Pubblicazione del flusso per test paginazione" è stato eseguito con successo
    E la configurazione psp è valorizzata come pspId nei parametri di query
    E l'organizzazione aggiunge ieri come createdGt nei parametri di query
    E l'organizzazione aggiunge 2 come page nei parametri di query
    E l'organizzazione aggiunge 1 come size nei parametri di query
    Quando l'organizzazione invia la richiesta di "recupero di tutti i fdr pubblicati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200
    E l'organizzazione riceve pagina 2 con 1 elementi come risposta

  @runnable
  @fdr3_009_06
  Scenario: Verifica paginazione pagamenti pubblicati pagina 1
    Dato che lo scenario "Pubblicazione del flusso per test paginazione" è stato eseguito con successo
    E l'organizzazione aggiunge ieri come createdGt nei parametri di query
    E l'organizzazione aggiunge 1 come page nei parametri di query
    E l'organizzazione aggiunge 99 come size nei parametri di query
    E la revisione del FdR è 1
    Quando l'organizzazione invia la richiesta di "recupero di tutti i pagamenti creati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200
    E l'organizzazione riceve pagina 1 con 99 elementi come risposta

  @runnable
  @fdr3_009_07
  Scenario: Verifica paginazione pagamenti pubblicati pagina 2
    Dato che lo scenario "Pubblicazione del flusso per test paginazione" è stato eseguito con successo
    E l'organizzazione aggiunge ieri come createdGt nei parametri di query
    E l'organizzazione aggiunge 2 come page nei parametri di query
    E l'organizzazione aggiunge 1 come size nei parametri di query
    E la revisione del FdR è 1
    Quando l'organizzazione invia la richiesta di "recupero di tutti i pagamenti creati dall'organizzazione" con il payload "None"
    Allora l'organizzazione riceve il codice di stato HTTP 200
    E l'organizzazione riceve pagina 2 con 1 elementi come risposta
