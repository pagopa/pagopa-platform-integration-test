#language: it
@fdr3_008_0
Funzionalità: Verifica KO della pubblicazione FdR
  Flusso: creazione, inserimento pagamenti, pubblicazione negativa e verifiche sugli endpoint protetti

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_008_1
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
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_008_2
  Scenario: Aggiunta di pagamenti
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E che lo scenario "Creazione del FdR" è stato eseguito con successo
    Quando il PSP aggiunge 5 pagamenti la cui somme è 300 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_008_3
  Scenario: Pubblicazione FdR con bad request
    Dato che lo scenario "Aggiunta di pagamenti" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Pubblicazione" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 400

  @runnable
  @fdr3_008_4
  Scenario: Pubblicazione FdR non autorizzata
    Dato che lo scenario "Pubblicazione FdR con bad request" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Pubblicazione" con il payload "None" con subscription_key non valida
    Allora il PSP riceve il codice di stato HTTP 401
