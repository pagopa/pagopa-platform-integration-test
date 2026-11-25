# language: it
@FEAT_007_Checkout
Funzionalità: Creazione del carrello di pagamento
  Come Ente Creditore (EC)
  il sistema espone l'endpoint carrello di PagoPA Checkout
  cosi che un flusso di pagamento possa essere avviato e venga restituito un reindirizzamento checkout

  Contesto:
    Dato l'host di checkout configurato tramite variabile d'ambiente

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

  @cart @checkout
  @FEAT_007_Checkout_SCENARIO_04
  Schema dello scenario: Creazione del carrello con <count> avvisi di pagamento
    Quando l'utente invia un carrello con <count> avvisi di pagamento
    Allora la risposta ha codice di stato <status_code>

    @positive
    @FEAT_007_Checkout_SCENARIO_04_01
    Esempi: avvisi nel limite consentito
      | count | status_code |
      | 5     | 302         |

    @negative
    @FEAT_007_Checkout_SCENARIO_04_02
    Esempi: avvisi oltre il limite consentito
      | count | status_code |
      | 6     | 400         |
