#language: it
@fdr3_003_Cancellazione_flusso
Funzionalità: Cancellazione di un flusso di rendicontazione

  Contesto:
    Dato che i sistemi sono operativi

  @fdr3_003_01
  Scenario: Creazione del flusso e inserimento pagamenti preliminari
    Dato un nome di flusso di rendicontazione univoco chiamato flow_name
    E una data di flusso di rendicontazione univoco chiamato flow_date
    E un payload di creazione FdR create_payload
    Quando il PSP invia la richiesta di "Creazione di una nuova struttura di flusso" con il payload "create_payload"
    Allora il PSP riceve il codice di stato HTTP 201

  @fdr3_003_02
  Scenario: Inserimento di 3 pagamenti
    Dato che il PSP deve inviare 3 pagamenti al flusso
    E che la somma totale dei pagamenti da inviare è 300
    E che lo scenario "Creazione del flusso e inserimento pagamenti preliminari" è stato eseguito con successo
    Quando il PSP aggiunge 3 pagamenti la cui somma è 300 al flusso di rendicontazione flow_name come payments_payload
    E il PSP invia la richiesta di "Aggiunta pagamenti" con il payload "payments_payload"
    Allora il PSP riceve il codice di stato HTTP 200

  @fdr3_003_03
  Scenario: Cancellazione del flusso
    Dato che lo scenario "Inserimento di 3 pagamenti" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Cancellazione flusso" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200

  @runnable
  @fdr3_003_04
  Scenario: Verifica cancellazione del flusso
    Dato che lo scenario "Cancellazione del flusso" è stato eseguito con successo
    Quando il PSP invia la richiesta di "Recupero di tutti i FdR pubblicati dal PSP" con il payload "None"
    Allora il PSP riceve il codice di stato HTTP 200
    E la lista dei flussi restituita non contiene il flusso con fdr = "flow_name"

