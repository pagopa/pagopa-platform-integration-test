Feature: Utente paga un pagamento singolo con marca da bollo tramite nodoInviaRPT

  Background:
    Given i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con nessun versamento semplice e una marca da bollo
    Given una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con un versamento semplice e una marca da bollo
    Given una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con due versamenti semplici e una marca da bollo
    Given una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con due versamenti semplici e due marche da bollo
    Given una singola RPT di tipo BBT con 4 versamenti di cui 2 sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo di tipo PO con nessun versamento semplice e una marca da bollo
    Given una singola RPT di tipo PO con 1 versamenti di cui 1 sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then la risposta contiene il vecchio URL WISP

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: Utente paga un pagamento singolo di tipo PO con un versamento semplice e una marca da bollo, ma fallisce la validazione semantica
    Given una singola RPT di tipo PO con 2 versamenti di cui 1 sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC ma il pagamento fallisce
    Then il pagamento fallisce having invalid semantic validation due to incorrect RPT structure e viene restituito l'errore PPT_SEMANTICA
