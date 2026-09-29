# language: it
@Fdr3_001_AggiungiPagamenti
Funzionalità: Aggiunta di pagamenti a un flusso di rendicontazione

  Contesto:
    Dato i sistemi sono operativi

  @runnable
  @positive
  Scenario: Creazione del flusso di rendicontazione per il test di aggiunta pagamenti
    Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    E un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data del flusso univoca chiamata flow_date
    E un payload di creazione FdR
      """
        {
          "fdr": "$flow_name$",
          "fdrDate": "$flow_date$",
          "sender": {"type": "LEGAL_PERSON","id": "SELBIT2B","pspId": "#psp#"},
          "receiver": {"id": "APPBIT2B","organizationId": "#organization#"},
          "regulation": "SEPA - Bonifico",
          "regulationDate": "$flow_date$",
          "totPayments": $number_of_payments$,
          "sumPayments": $payments_amount$
        }
      """
    Quando il PSP invia la richiesta di creazione flusso tramite l'API "Create a new flow structure"
    Allora il PSP riceve il codice di stato HTTP 201
    E il flusso viene creato in stato "CREATED"

  @runnable
  Schema dello scenario: Aggiunta di pagamenti al flusso
    Dato che lo scenario "Creazione del flusso di rendicontazione per il test di aggiunta pagamenti" è stato eseguito con successo
    E che il PSP deve inviare <n> pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è <amount>
    Quando il PSP invia la richiesta di aggiunta pagamenti (API "Add payments") con <n> pagamenti per il flusso "flow_name"
    Allora il PSP riceve il codice di stato HTTP <code>
    E il sistema aggiorna correttamente i campi "totPayments" e "sumPayments" del flusso

    Esempi:
      | n    | amount | code |
      | 1    | 3      | 200  |
      | 1000 | 29999  | 200  |
      | 1001 | 30000  | 400  |
