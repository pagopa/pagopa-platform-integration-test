# language: it
@FEAT_008_Checkout
Funzionalità: Servizio auth
  Valida i flussi del servizio auth

  Contesto:
    Dato che l'host di checkout e configurato tramite variabile d'ambiente
    E le variabili d'ambiente del servizio auth sono configurate

  @auth-service @checkout @positive
  @FEAT_008_Checkout_SCENARIO_01
  Scenario: Il flusso di autenticazione riuscito restituisce un token di sessione e il profilo utente atteso
    Quando l'utente richiede l'URL di login auth
    Allora la risposta ha codice di stato 200
    E la risposta di login auth espone un URL di reindirizzamento valido
    Quando l'utente apre l'URL di reindirizzamento auth
    Allora la risposta ha codice di stato 200
    E il codice auth viene estratto dalla risposta di reindirizzamento
    Quando l'utente scambia il codice auth con un token di sessione
    Allora la risposta ha codice di stato 200
    E il token auth viene restituito nella risposta
    Quando l'utente richiede il profilo utente autenticato con il token di sessione attivo
    Allora la risposta ha codice di stato 200
    E il profilo utente autenticato corrisponde all'utente auth configurato
    Quando l'utente esegue il logout dal servizio auth con il token di sessione attivo
    Allora la risposta ha codice di stato 204

  @auth-service @checkout @negative
  @FEAT_008_Checkout_SCENARIO_02
  Scenario: Codice auth non valido e token di sessione non valido vengono rifiutati
    Quando l'utente richiede l'URL di login auth
    Allora la risposta ha codice di stato 200
    E la risposta di login auth espone un URL di reindirizzamento valido
    Quando l'utente apre l'URL di reindirizzamento auth
    Allora la risposta ha codice di stato 200
    Quando l'utente scambia un codice auth non valido con un token di sessione
    Allora la risposta ha codice di stato 401
    Dato un token di sessione auth non valido
    Quando l'utente richiede una richiesta di pagamento autenticata con il token di sessione non valido
    Allora la risposta ha codice di stato 401
    Quando l'utente richiede il profilo utente autenticato con il token di sessione non valido
    Allora la risposta ha codice di stato 401