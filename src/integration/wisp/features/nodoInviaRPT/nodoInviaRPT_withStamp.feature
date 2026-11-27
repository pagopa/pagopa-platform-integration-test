#3119448801
#language:it
@integration
@NodoInviaRPT_WithStamp_002
Funzionalità: Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT
  
  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaRPT_WithStamp_002_01
  @nodo_invia_rpt
  @positive
  Scenario: Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo
    Data una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaRPT_WithStamp_002_02
  @nodo_invia_rpt
  @positive
  Scenario: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
    Data una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaRPT_WithStamp_002_03
  @nodo_invia_rpt
  @positive
  Scenario: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
    Data una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaRPT_WithStamp_002_04
  @nodo_invia_rpt
  @positive
  Scenario: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
    Data una singola RPT di tipo BBT con 4 versamenti di cui 2 sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaRPT_WithStamp_002_05
  @nodo_invia_rpt
  @positive
  Scenario: Utente paga un pagamento singolo di tipo PO con nessun versamento semplice e una marca da bollo
    Data una singola RPT di tipo PO con 1 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora la risposta contiene il vecchio URL WISP

  # ===============================================================================================
  # ===============================================================================================

  @runnable
  @NodoInviaRPT_WithStamp_002_06
  @nodo_invia_rpt
  @negative
  Scenario: Utente paga un pagamento singolo di tipo PO con un versamento semplice e una marca da bollo, ma fallisce la validazione semantica
    Data una singola RPT di tipo PO con 2 versamenti di cui 1 sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC ma il pagamento fallisce
    Allora il pagamento fallisce having invalid semantic validation due to incorrect RPT structure e viene restituito l'errore PPT_SEMANTICA
