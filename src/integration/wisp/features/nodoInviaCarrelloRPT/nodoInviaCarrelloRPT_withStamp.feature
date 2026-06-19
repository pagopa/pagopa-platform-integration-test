# language: it
@FEAT_005_NodoInviaCarrelloRPT_WithStamp
Funzionalità: L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT

  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_01
  Scenario: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_02
  Scenario: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_03
  Scenario: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_04
  Scenario: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_05
  Scenario: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_06
  Scenario: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 4 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_07
  Scenario: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 4 versamenti di cui 2 sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_08
  Scenario: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti e marche da bollo oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 6 versamenti di cui 3 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce essendo il numero di versamenti oltre il limite e viene restituito l'errore PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @FEAT_005_NodoInviaCarrelloRPT_WithStamp_SCENARIO_09
  Scenario: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti e marche da bollo oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 6 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce essendo il numero di versamenti oltre il limite e viene restituito l'errore PPT_SINTASSI_XSD
