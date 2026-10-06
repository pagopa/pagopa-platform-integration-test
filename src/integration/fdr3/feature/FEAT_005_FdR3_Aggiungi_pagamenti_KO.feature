# language: it

@fdr3_005_Verifica_KO_pagamenti
Funzionalità: Verifica KO dei pagamenti
  Verifiche negative sui flussi: creazione, aggiunta pagamenti in eccesso e richiesta con subscription key non valida

  Contesto:
    Dato i sistemi sono operativi

  @fdr3_005_1
  Scenario: Creazione del FdR
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_005_2
  Scenario: Aggiunta di pagamenti in eccesso
      Dato che il PSP deve inviare 1001 pagamenti al flusso
      E che la somma totale dei pagamenti da inviare è 9999
      E che lo scenario "Creazione del FdR" è stato eseguito con successo
      Quando il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
      Allora il PSP riceve il codice di stato HTTP 400

  @runnable
  @fdr3_005_3
  Scenario: Aggiunta pagamenti con subscription_key non valida
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 10
    E che lo scenario "Aggiunta di pagamenti in eccesso" è stato eseguito con successo
    Quando il PSP aggiunge 3 pagamenti la cui somme è 10 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "None" con subscription_key non valida
    Allora il PSP riceve il codice di stato HTTP 401
