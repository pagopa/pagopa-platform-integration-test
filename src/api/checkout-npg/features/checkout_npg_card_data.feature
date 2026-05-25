# language: it
@FEAT_010_Checkout
Funzionalità: Checkout eCommerce - gateway di pagamento NPG
  Valida i flussi API di checkout eCommerce per il recupero e la validazione dei dati carta NPG.

  Contesto:
    Dato l'host di checkout configurato tramite variabile d'ambiente
    E le variabili d'ambiente NPG di checkout configurate

  # ---------------------------------------------------------------------------
  # Dati carta NPG
  # ---------------------------------------------------------------------------

  @checkout @npg @card @positive
  @FEAT_010_Checkout_SCENARIO_01
  Scenario: I dati carta vengono recuperati con successo dopo la compilazione dei campi NPG
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    E i campi carta NPG sono compilati con dati carta di test
    Quando l'utente recupera i dati carta per la sessione corrente
    Allora la risposta ha codice di stato 200
    E i dati carta corrispondono ai valori della carta di test

  @checkout @npg @card @negative
  @FEAT_010_Checkout_SCENARIO_02
  Scenario: I dati carta non sono disponibili con order id errato
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    Quando l'utente recupera i dati carta con un order id errato
    Allora la risposta ha codice di stato 401

  @checkout @npg @card @negative
  @FEAT_010_Checkout_SCENARIO_03
  Scenario: I dati carta non sono disponibili con transaction id errato
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    Quando l'utente recupera i dati carta con un transaction id errato
    Allora la risposta ha codice di stato 401

  @checkout @npg @card @negative
  @FEAT_010_Checkout_SCENARIO_04
  Scenario: I dati carta non sono disponibili quando manca l'auth token
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    Quando l'utente recupera i dati carta senza auth token
    Allora la risposta ha codice di stato 401
