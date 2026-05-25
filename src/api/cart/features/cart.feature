# language: it
@FEAT_007_Checkout
Funzionalità: Creazione del carrello di pagamento
  Come Ente Creditore (EC)
  il sistema espone l'endpoint carrello di PagoPA Checkout
  cosi che un flusso di pagamento possa essere avviato e venga restituito un reindirizzamento checkout

  Contesto:
    Dato che l'host di checkout e configurato tramite variabile d'ambiente

  @cart @checkout @positive
  @FEAT_007_Checkout_SCENARIO_01
  Scenario: Creazione valida del carrello con un avviso di pagamento
    Dato un codice avviso casuale valido generato dal prefisso configurato in "NOTICE_CODE_PREFIX"
    E un codice fiscale PA valido configurato in "VALID_FISCAL_CODE_PA"
    Quando l'utente invia un carrello con email "test@test.it"
    Allora la risposta ha codice di stato 302
    E la risposta contiene l'header "location"
    E l'id del carrello viene estratto dall'header "location"

  @cart @checkout @positive
  @FEAT_007_Checkout_SCENARIO_02
  Scenario: Creazione del carrello con email in maiuscolo
    Dato un codice avviso casuale valido generato dal prefisso configurato in "NOTICE_CODE_PREFIX"
    E un codice fiscale PA valido configurato in "VALID_FISCAL_CODE_PA"
    Quando l'utente invia un carrello con email "TEST@test.IT"
    Allora la risposta ha codice di stato 302
    E la risposta contiene l'header "location"
    E l'id del carrello viene estratto dall'header "location"

  @cart @checkout @negative
  @FEAT_007_Checkout_SCENARIO_03
  Scenario: La creazione del carrello fallisce con body malformato
    Quando l'utente invia un carrello con un body non valido
    Allora la risposta ha codice di stato 400

  @cart @checkout @negative
  @FEAT_007_Checkout_SCENARIO_04
  Scenario: La creazione del carrello fallisce quando gli avvisi superano il massimo consentito
    Quando l'utente invia un carrello con 6 avvisi di pagamento
    Allora la risposta ha codice di stato 400
