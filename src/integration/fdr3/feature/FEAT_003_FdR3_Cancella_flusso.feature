# language: it
@Fdr3_003_CancellaFlusso
Funzionalità: Cancellazione di un flusso di rendicontazione

  Contesto:
    Dato i sistemi sono operativi

  @runnable
  @positive
  Scenario: Creazione del flusso e inserimento pagamenti preliminari
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

  Scenario: Cancellazione del flusso
    Dato che l'inserimento dei pagamenti è avvenuto con successo
    Quando il PSP invia la richiesta di cancellazione del flusso (API "Delete flow")
    Allora il PSP riceve il codice di stato HTTP 200

  @runnable
  Scenario: Verifica cancellazione del flusso
    Dato che la cancellazione del flusso è stata eseguita con successo
    E la configurazione dell'organizzazione è valorizzata come organizationId nei parametri di query
    E la configurazione del PSP è valorizzata come flow_name nei parametri di query
    Quando il PSP richiede la lista dei flussi pubblicati (API "Get all published FdR")
    Allora il PSP riceve il codice di stato HTTP 200
    E la lista dei flussi restituita non contiene il flusso con fdr = "flow_name"
