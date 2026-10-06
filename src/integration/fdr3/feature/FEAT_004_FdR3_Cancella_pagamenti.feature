# language: it
@fdr3_004_Rimozione_pagamenti
Funzionalità: Rimozione di pagamenti da un flusso di rendicontazione

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_004_01
  Scenario: Creazione del flusso e inserimento iniziale di pagamenti
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_004_02
  Scenario: Inserimento di 3 pagamenti
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E che lo scenario "Creazione del flusso e inserimento iniziale di pagamenti" è stato eseguito con successo
    Quando il PSP aggiunge 3 pagamenti la cui somme è 300 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_004_03
  Scenario: Verifica pagamenti creati
    Dato che lo scenario "Inserimento di 3 pagamenti" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Recupero pagamenti creati" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene 3 pagamenti

  @fdr3_004_04
  Scenario: Rimozione di 1 pagamento
    Dato che lo scenario "Verifica pagamenti creati" è stato eseguito con successo
    Quando il PSP rimuove 1 pagamento dal flusso di rendicontazione flow_name come remove_payment_payload
    E il PSP invia la richiesta di "Cancellazione pagamenti" con il payload "remove_payment_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_004_05
  Scenario: Verifica pagamenti dopo cancellazione
    Dato che lo scenario "Rimozione di 1 pagamento" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Recupero pagamenti creati" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene 2 pagamenti

  @runnable
  @fdr3_004_06
  Scenario: Tentativo di pubblicazione dopo cancella pagamenti
    Dato che lo scenario "Verifica pagamenti dopo cancellazione" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Pubblicazione" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 400
