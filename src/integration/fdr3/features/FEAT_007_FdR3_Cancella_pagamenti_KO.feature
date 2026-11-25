#language: it
@fdr3_007_Cancellazione_pagamenti
Funzionalità: Rimozione di pagamenti da un FdR
  Flusso: creazione, inserimento pagamenti, rimozione e verifiche negative

  Contesto:
    Dato che i sistemi sono operativi

  @fdr3_007_1
  Scenario: Creazione del FdR
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_007_2
  Scenario: Aggiunta di pagamenti
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E che lo scenario "Creazione del FdR" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_007_3
  Scenario: Cancellazione di un pagamento - bad request
    Dato che lo scenario "Aggiunta di pagamenti" è stato eseguito con successo
    E il PSP imposta un psp non valido
    Quando il PSP invia la richiesta di "Cancellazione pagamenti" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 400

  @runnable @fdr3_007_4
  Scenario: Cancellazione di un pagamento - subscription_key non valida
    Dato che lo scenario "Cancellazione di un pagamento - bad request" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Cancellazione pagamenti" con il payload "None" con subscription_key non valida
    Allora il PSP riceve il codice di stato HTTP 401

