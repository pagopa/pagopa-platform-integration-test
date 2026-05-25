# language: it
@FEAT_011_Checkout
Funzionalità: Checkout eCommerce - gateway di pagamento NPG
  Valida i flussi API di checkout eCommerce per il recupero dei metodi di pagamento e il calcolo commissioni.

  Contesto:
    Dato che l'host di checkout e configurato tramite variabile d'ambiente
    E le variabili d'ambiente NPG di checkout sono configurate

  # ---------------------------------------------------------------------------
  # Metodi di pagamento
  # ---------------------------------------------------------------------------

  @checkout @npg @payment-methods @positive
  @FEAT_011_Checkout_SCENARIO_01
  Scenario: Tutti i metodi di pagamento v1 vengono recuperati con successo
    Quando l'utente recupera tutti i metodi di pagamento v1
    Allora la risposta ha codice di stato 200
    E la risposta dei metodi di pagamento v1 contiene i campi attesi e gli asset brand

  @checkout @npg @payment-methods @positive
  @FEAT_011_Checkout_SCENARIO_02
  Scenario: Tutti i metodi di pagamento v2 vengono recuperati con successo
    Quando l'utente recupera tutti i metodi di pagamento v2
    Allora la risposta ha codice di stato 200
    E la risposta dei metodi di pagamento v2 contiene i campi attesi

  @checkout @npg @payment-methods @positive
  @FEAT_011_Checkout_SCENARIO_03
  Scenario: I dettagli del metodo di pagamento carta di credito vengono recuperati
    Dato l'id del metodo di pagamento carta di credito e risolto
    Quando l'utente recupera i dettagli del metodo di pagamento carta di credito
    Allora la risposta ha codice di stato 200
    E il metodo di pagamento e CARDS con paymentTypeCode CP

  @checkout @npg @payment-methods @positive
  @FEAT_011_Checkout_SCENARIO_04
  Scenario: Il calcolo commissione per pagamento con carta di credito riesce
    Dato l'id del metodo di pagamento carta di credito e risolto
    E viene creata una sessione NPG
    E viene generato un codice avviso valido casuale
    E viene creata una transazione per la sessione corrente
    Quando l'utente calcola la commissione per il pagamento con carta di credito
    Allora la risposta ha codice di stato 200
    E la risposta della commissione contiene un metodo abilitato con bundles
