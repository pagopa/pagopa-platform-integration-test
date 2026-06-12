# language: it
@FEAT_004_NodoInviaCarrelloRPT_NoStamp
Funzionalità: L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT

  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_01
  Scenario: L'utente paga un carrello con singola RPT con un versamento
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_02
  Scenario: L'utente paga un carrello con singola RPT con due versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_03
  Scenario: L'utente paga un carrello con singola RPT con tre versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_04
  Scenario: L'utente paga un carrello con singola RPT con quattro versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_05
  Scenario: L'utente paga un carrello con singola RPT con cinque versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 5 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_06
  Scenario: L'utente paga un carrello con tre RPT con un versamento ciascuna
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_07
  Scenario: L'utente paga un carrello con quattro RPT con un versamento ciascuna
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_08
  Scenario: L'utente paga un carrello con cinque RPT con un versamento ciascuna
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_09
  Scenario: L'utente paga un carrello con due RPT per un totale di cinque versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_10
  Scenario: L'utente paga un carrello con tre RPT per un totale di cinque versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_11
  Scenario: L'utente paga un carrello con tre RPT per un totale di dieci versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_12
  Scenario: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce, poi ritenta con successo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    E l'utente viene reindirizzato su Checkout senza completare il pagamento multibeneficiario
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_13
  Scenario: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce having a quantity of transfers above the limit e viene restituito l'errore PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_14
  Scenario: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce having a quantity of transfers above the limit e viene restituito l'errore PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @FEAT_004_NodoInviaCarrelloRPT_NoStamp_SCENARIO_15
  Scenario: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout senza completare il pagamento multibeneficiario
