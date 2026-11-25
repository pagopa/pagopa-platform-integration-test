#3119448822
#language:it
@integration
@NodoInviaCarrelloRPT_WithStamp_005
Funzionalità: L'utente paga carrelli di pagamento con marche da bollo su nodoInviaCarrelloRPT
  
  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_01
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT senza versamento semplice e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_02
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con un versamento semplice e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_03
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con due versamenti semplici e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_04
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con due RPT, entrambe senza versamento semplice e con una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_05
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con due RPT, entrambe con un versamento semplice e una marca da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_06
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con due RPT, con quantita diverse di versamenti semplici e marche da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 4 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_07
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con tre RPT, con quantita diverse di versamenti semplici e marche da bollo
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 4 versamenti di cui 2 sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_08
  @nodo_invia_carrello_rpt
  @negative
  Scenario: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti e marche da bollo oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 6 versamenti di cui 3 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce essendo il numero di versamenti oltre il limite e viene restituito l'errore PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_WithStamp_005_09
  @nodo_invia_carrello_rpt
  @negative
  Scenario: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti e marche da bollo oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 6 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce essendo il numero di versamenti oltre il limite e viene restituito l'errore PPT_SINTASSI_XSD
