#3115780688
#language:it
@integration
@NodoInviaCarrelloRPT_NoStamp_004
Funzionalità: L'utente paga carrelli di pagamento senza marche da bollo su nodoInviaCarrelloRPT
  
  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_01
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con un versamento
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_02
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con due versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_03
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con tre versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_04
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con quattro versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_05
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con singola RPT con cinque versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 5 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_06
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con tre RPT con un versamento ciascuna
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_07
  @nodo_invia_carrello_rpt
  @positive
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

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_08
  @nodo_invia_carrello_rpt
  @positive
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

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_09
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con due RPT per un totale di cinque versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_10
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con tre RPT per un totale di cinque versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_11
  @nodo_invia_carrello_rpt
  @positive
  Scenario: L'utente paga un carrello con tre RPT per un totale di dieci versamenti
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_12
  @nodo_invia_carrello_rpt
  @positive
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

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_13
  @nodo_invia_carrello_rpt
  @negative
  Scenario: L'utente tenta di pagare un carrello con una RPT che ha una quantita di versamenti oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce essendo il numero di versamenti oltre il limite e viene restituito l'errore PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_14
  @nodo_invia_carrello_rpt
  @negative
  Scenario: L'utente tenta di pagare un carrello con due RPT che hanno una quantita di versamenti oltre il limite
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 6 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    Allora il pagamento fallisce essendo il numero di versamenti oltre il limite e viene restituito l'errore PPT_SINTASSI_XSD

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaCarrelloRPT_NoStamp_004_15
  @nodo_invia_carrello_rpt
  @negative
  Scenario: L'utente tenta di pagare un carrello con due RPT ma la chiusura del pagamento fallisce
    Dato un carrello di RPT non-multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout senza completare il pagamento multibeneficiario
