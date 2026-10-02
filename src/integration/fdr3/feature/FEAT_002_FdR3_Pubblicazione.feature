# language: it
@fdr3_002_Crea_revisione
Funzionalità: Workflow di creazione e gestione delle revisioni di un flusso di rendicontazione

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_002_01
  Scenario: Creazione del flusso iniziale utilizzato per i test di revisione
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E un payload di creazione FdR create_1_payload
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
    Quando il PSP invia la richiesta "Create a new flow structure" con il payload "create_1_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_002_02
  Scenario: Aggiunta di 3 pagamenti alla revisione iniziale
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E che lo scenario "Creazione del flusso iniziale utilizzato per i test di revisione" è stato eseguito con successo
    Quando il PSP aggiunge 3 pagamenti la cui somme è 300 al flusso di rendicontazione flow_name come payments_payload
    Quando il PSP invia la richiesta "Add payments" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_002_03
  Scenario: Pubblicazione della prima revisione
    Dato che lo scenario "Aggiunta di 3 pagamenti alla revisione iniziale" è stato eseguito con successo
    Quando il PSP invia la richiesta "Publish" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_002_04
  Scenario: Verifica revisione dopo prima pubblicazione
    Dato che lo scenario "Pubblicazione della prima revisione" è stato eseguito con successo
    Quando il PSP invia la richiesta "Get published FdR" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 1

  @fdr3_002_05
  Scenario: Creazione di una nuova versione (revisione 2) dello stesso FdR
    Dato una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_2_payload
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
    Quando il PSP invia la richiesta "Create a new flow structure" con il payload "create_2_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_002_06
  Scenario: Creazione della revisione 2 confermata
    Dato che lo scenario "Verifica revisione dopo prima pubblicazione" è stato eseguito con successo
    E che il PSP deve inviare 2 pagamenti al flusso
    E che lo scenario "Creazione di una nuova versione (revisione 2) dello stesso FdR" è stato eseguito con successo
    Quando il PSP invia la richiesta "Get created FdR" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 2
    E lo stato del flusso è "CREATED"

  @fdr3_002_07
  Scenario: Aggiunta di 2 pagamenti alla revisione 2
    Dato che lo scenario "Creazione della revisione 2 confermata" è stato eseguito con successo
    Quando il PSP aggiunge 2 pagamenti la cui somme è 300 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta "Add payments" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_002_08
  Scenario: Pubblicazione della revisione 2
    Dato che lo scenario "Aggiunta di 2 pagamenti alla revisione 2" è stato eseguito con successo
    Quando il PSP invia la richiesta "Publish" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_002_09
  Scenario: Verifica revisione dopo seconda pubblicazione
    Dato che lo scenario "Pubblicazione della revisione 2" è stato eseguito con successo
    Quando il PSP invia la richiesta "Get published FdR" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 2
    E la risposta contiene totPayments = 2

  @fdr3_002_10
  Scenario: Creazione della revisione 3
    Dato una data di flusso di rendicontazione univoco chiamato flow_date
    E che lo scenario "Verifica revisione dopo seconda pubblicazione" è stato eseguito con successo
    E che il PSP deve inviare 1 pagamento al flusso
    Quando il PSP invia la richiesta "Get created FdR" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la risposta contiene revision = 3
    E lo stato del flusso è "CREATED"

  @fdr3_002_11
  Scenario: Aggiunta di 2 pagamenti invece di 1 nella revisione 3
    Dato che lo scenario "Creazione della revisione 3" è stato eseguito con successo
    Quando il PSP aggiunge 2 pagamenti la cui somme è 300 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta "Add payments" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @runnable
  @fdr3_002_12
  Scenario: Tentativo di pubblicazione della revisione 3 non valido
    Dato che lo scenario "Aggiunta di 2 pagamenti invece di 1 nella revisione 3" è stato eseguito con successo
    Quando il PSP invia la richiesta "Publish" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 400
