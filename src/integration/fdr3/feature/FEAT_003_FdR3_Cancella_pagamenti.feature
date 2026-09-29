# language: it
@Fdr3_003_CancellaPagamenti
Funzionalità: Rimozione di pagamenti da un flusso di rendicontazione

  Contesto:
    Dato i sistemi sono operativi

  @runnable
  @positive
  Scenario: Creazione del flusso e inserimento iniziale di pagamenti
    Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    E un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data del flusso univoca chiamata flow_date
    E un payload di creazione FdR
      """
        { "fdr": "$flow_name$", "fdrDate": "$flow_date$", "totPayments": $number_of_payments$, "sumPayments": $payments_amount$ }
      """
    Quando il PSP invia la richiesta di creazione flusso tramite l'API "Create a new flow structure"
    Allora il PSP riceve il codice di stato HTTP 201

  Scenario: Inserimento di 3 pagamenti
    Dato che il flusso è stato creato con successo
    E che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    Quando il PSP invia la richiesta di aggiunta pagamenti (API "Add payments") con 3 pagamenti per il flusso "flow_name"
    Allora il PSP riceve il codice di stato HTTP 200

  Scenario: Verifica pagamenti creati
    Dato che l'aggiunta dei pagamenti è avvenuta con successo
    Quando il PSP richiede i pagamenti creati (API "Get created payments")
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene 3 pagamenti

  Scenario: Rimozione di 1 pagamento
    Dato che sono presenti 3 pagamenti creati
    Quando il PSP invia la richiesta di rimozione di 1 pagamento per il flusso "flow_name"
    Allora il PSP riceve il codice di stato HTTP 200

  Scenario: Verifica pagamenti dopo cancellazione
    Dato che la rimozione del pagamento è avvenuta con successo
    Quando il PSP richiede i pagamenti creati (API "Get created payments")
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene 2 pagamenti

  @runnable
  Scenario: Tentativo di pubblicazione dopo cancella pagamenti
    Dato che dopo la cancellazione sono presenti 2 pagamenti
    Quando il PSP invia la richiesta di pubblicazione (API "Publish")
    Allora il PSP riceve il codice di stato HTTP 400
