Feature: L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT

  Background:
    Given i sistemi sono operativi


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con un versamento
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con due versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con tre versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con quattro versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con cinque versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 5 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con tre RPT con un versamento ciascuna
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con quattro RPT con un versamento ciascuna
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con cinque RPT con un versamento ciascuna
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con due RPT con un totale di cinque versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con tre RPT con un totale di cinque versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento


  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con tre RPT con un totale di dieci versamenti
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi riprova con successo
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    And l'utente viene reindirizzato su Checkout senza completare il pagamento multibeneficiario
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Then il pagamento fallisce having a quantity of transfers above the limit e viene restituito l'errore PPT_SINTASSI_XSD
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Then il pagamento fallisce having a quantity of transfers above the limit e viene restituito l'errore PPT_SINTASSI_XSD
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout senza completare il pagamento multibeneficiario
