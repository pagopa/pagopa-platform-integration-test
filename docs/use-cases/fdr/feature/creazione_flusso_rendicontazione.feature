# 1000000001
# language: it

# JTBD-001 | UC-FDR-001
@creazione_flusso_rendicontazione_001
Funzionalità: Creazione di un flusso di rendicontazione

  Come PSP
  voglio creare un flusso di rendicontazione (FdR) tramite fdr-microservice
  al fine di dichiarare i pagamenti regolati verso l'ente creditore

  @creazione_flusso_rendicontazione_001_01 @smoke @fdr @positive
  Scenario: Creazione di un FdR con dati validi
    Dato che i sistemi necessari all'elaborazione del flusso di rendicontazione sono disponibili
    E il PSP dispone delle configurazioni e delle credenziali necessarie per invocare fdr-microservice
    E il PSP dispone di un nome FdR univoco "$flow_name$" e di una data FdR univoca "$flow_date$"
    E il PSP dispone dei dati del mittente, del destinatario e della regolazione
    E il PSP conosce il numero totale "$number_of_payments$" e la somma complessiva "$payments_amount$" dei pagamenti da dichiarare nel FdR
    Quando il PSP invia a fdr-microservice la richiesta "create" con il seguente payload
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
        "totPayments": $number_of_payments$,
        "sumPayments": $payments_amount$
      }
      """
    Allora fdr-microservice restituisce lo stato HTTP 201
    E il FdR identificato da "$flow_name$" risulta presente nel sistema
    E il FdR contiene i dati del mittente, del destinatario, della regolazione e i totali dichiarati nella richiesta di creazione
