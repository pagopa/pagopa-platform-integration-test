#3115780709
#language:it
@NodoInviaCarrelloRPT_MultiBeneficiario_007
Funzionalità: L'utente paga carrelli di pagamento multi-beneficiari su nodoInviaCarrelloRPT
  
  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_01
  Scenario: L'utente paga un carrello multibeneficiario con due RPT con un totale di due versamenti
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_02
  Scenario: L'utente paga un carrello multibeneficiario con due RPT con un totale di tre versamenti
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_03
  Scenario: L'utente paga un carrello multibeneficiario con due RPT con un totale di quattro versamenti
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_04
  Scenario: L'utente paga un carrello multibeneficiario con due RPT con un totale di cinque versamenti
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento multibeneficiario

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_05
  Scenario: L'utente tenta di pagare un carrello multibeneficiario con due RPT con un totale di sei versamenti, ma il carrello ha piu di 5 versamenti
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 5 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    E il tentativo di pagamento fallisce
    Allora la risposta contiene il campo description con valore 'Il carrello deve avere massimo 5 versamenti totali'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_06
  Scenario: L'utente tenta di pagare un carrello multibeneficiario con tre RPT con un versamento ciascuna, ma il carrello ha piu di 2 RPT
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    E il tentativo di pagamento fallisce
    Allora la risposta contiene il campo description con valore 'Il carrello non contiene solo 2 RPT'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_07
  Scenario: L'utente tenta di pagare un carrello multibeneficiario con due RPT, in cui la seconda ha due versamenti, ma la seconda RPT contiene piu di un versamento
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    E il tentativo di pagamento fallisce
    Allora la risposta contiene il campo description con valore 'La seconda RPT non contiene solo 1 versamento'

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @NodoInviaCarrelloRPT_MultiBeneficiario_007_08
  Scenario: L'utente tenta di pagare un carrello multibeneficiario con due RPT con una marca da bollo, ma fallisce perche una RPT ha la marca da bollo
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC senza verifica dell'URL di redirect
    E il tentativo di pagamento fallisce
    Allora la risposta contiene il campo description con valore 'Nessuna RPT deve contienere marca da bollo'
