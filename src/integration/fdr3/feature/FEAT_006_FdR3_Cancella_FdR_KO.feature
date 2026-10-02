#language: it
@fdr3_006_Cancellazione_FdR
Funzionalità: Cancellazione di FdR creati
  Flusso: creazione, inserimento pagamenti, cancellazione e verifiche negative

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_006_1
  Scenario: Creazione del FdR
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
      """
        {
          "fdr": "$flow_name$",
          "fdrDate": "$flow_date$",
          "sender": {
            "type": "LEGAL_PERSON",
            "id": "SELBIT2B",
            "pspId": "#psp#",
            "pspName": "Bank",
            "pspBrokerId": "#broker_psp#",
            "channelId": "#channel#",
            "password": "#channel_password#"
          },
          "receiver": {
        "id": "APPBIT2B",
        "organizationId": "#organization#",
        "organizationName": "Comune di XYZ"
          },
          "regulation": "SEPA - Bonifico xzy",
          "regulationDate": "$flow_date$",
          "bicCodePouringBank": "UNCRITMMXXX",
          "totPayments": $tot_payments$,
          "sumPayments": $sum_payments$
        }
      """
    Quando il PSP invia la richiesta "Create a new flow structure" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_006_2
  Scenario: Aggiunta di pagamenti
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E che lo scenario "Creazione del FdR" è stato eseguito con successo
    Quando il PSP invia la richiesta "Add payments" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_006_3
  Scenario: Cancellazione del FdR non trovato
    Dato che lo scenario "Aggiunta di pagamenti" è stato eseguito con successo
    E il PSP imposta un flow_name non valido
    Quando il PSP invia la richiesta "Delete flow" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 404

  @fdr3_006_4
  Scenario: Cancellazione del FdR bad request
    Dato che lo scenario "Aggiunta di pagamenti" è stato eseguito con successo
    E il PSP imposta un psp non valido
    Quando il PSP invia la richiesta "Delete flow" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 400

  @runnable
  @fdr3_006_5
  Scenario: Cancellazione del FdR con subscription_key non valida
    Dato che lo scenario "Cancellazione del FdR non trovato" è stato eseguito con successo
    Quando il PSP invia la richiesta "Delete flow" con il payload "None" con subscription_key non valida
    Allora il PSP riceve il codice di stato HTTP 401
