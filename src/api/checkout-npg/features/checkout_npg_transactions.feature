# language: it
@FEAT_014_Checkout
Funzionalità: Checkout eCommerce - gateway di pagamento NPG
  Valida i flussi API di checkout eCommerce per la gestione del ciclo di vita della transazione.

  Contesto:
    Dato l'host di checkout configurato tramite variabile d'ambiente
    E le variabili d'ambiente NPG di checkout configurate

  # ---------------------------------------------------------------------------
  # Transazioni
  # ---------------------------------------------------------------------------

  @checkout @npg @transaction @negative
  @FEAT_014_Checkout_SCENARIO_01
  Scenario: La creazione della transazione fallisce quando manca l'order id
    Dato viene generato un codice avviso valido casuale
    Quando l'utente crea una transazione senza order id
    Allora la risposta ha codice di stato 400

  @checkout @npg @transaction @positive
  @FEAT_014_Checkout_SCENARIO_02
  Scenario: La creazione della transazione con email mista maiuscola/minuscola riesce
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    Quando l'utente crea una transazione con email mista maiuscola/minuscola
    Allora la risposta ha codice di stato 200
    E la risposta della transazione e in stato ACTIVATED per il client checkout

  @checkout @npg @transaction @positive
  @FEAT_014_Checkout_SCENARIO_03
  Scenario: La creazione della transazione con email standard riesce e il pagamento in cache e ancora valido
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    Quando l'utente crea una transazione con email standard
    Allora la risposta ha codice di stato 200
    E la risposta della transazione e in stato ACTIVATED per il client checkout
    Quando l'utente verifica il pagamento in cache
    Allora la risposta ha codice di stato 200
    E la verifica del pagamento in cache restituisce dati di pagamento validi

  @checkout @npg @transaction @positive
  @FEAT_014_Checkout_SCENARIO_04
  Scenario: La transazione in stato ACTIVATED viene annullata con successo
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    Quando l'utente elimina la transazione
    Allora la risposta ha codice di stato 202

  @checkout @npg @transaction @positive
  @FEAT_014_Checkout_SCENARIO_05
  Scenario: Il recupero della transazione v1 restituisce stato AUTHORIZATION_REQUESTED
    Dato il flusso completo di autorizzazione NPG e eseguito
    Quando l'utente recupera la transazione per id v1
    Allora la risposta ha codice di stato 200
    E lo stato della transazione v1 e AUTHORIZATION_REQUESTED
    E il gateway della transazione v1 e NPG

  @checkout @npg @transaction @positive
  @FEAT_014_Checkout_SCENARIO_06
  Scenario: Il recupero esiti transazione v1 restituisce un codice esito valido
    Dato il flusso completo di autorizzazione NPG e eseguito
    Quando l'utente recupera gli esiti della transazione v1
    Allora la risposta ha codice di stato 200
    E la risposta degli esiti contiene un codice esito valido

  @checkout @npg @transaction @positive
  @FEAT_014_Checkout_SCENARIO_07
  Scenario: Il recupero della transazione v2 restituisce stato AUTHORIZATION_REQUESTED con info gateway
    Dato il flusso completo di autorizzazione NPG e eseguito
    Quando l'utente recupera la transazione per id v2
    Allora la risposta ha codice di stato 200
    E lo stato della transazione v2 e AUTHORIZATION_REQUESTED
    E il gatewayInfo della transazione v2 e NPG
