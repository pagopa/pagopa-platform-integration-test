Feature: Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT

  Background:
    Given i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
    Given una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
    Given una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
    Given una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo
    Given una singola RPT di tipo BBT con 5 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo di tipo PO con un versamento e nessuna marca da bollo
    Given una singola RPT di tipo PO con 1 versamenti di cui none sono marche da bollo
    When l'utente invia una richiesta nodoInviaRPT
    Then l'utente riceve una risposta con esito positivo
    And la risposta contiene il vecchio URL WISP

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: Utente paga un pagamento singolo di tipo PO con due versamenti e nessuna marca da bollo
    Given una singola RPT di tipo PO con 2 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC ma il pagamento fallisce
    Then il pagamento fallisce having invalid semantic validation due to incorrect RPT structure e viene restituito l'errore PPT_SEMANTICA

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then la conversione al nuovo modello ha successo nel wisp-converter
    And l'utente viene reindirizzato nuovamente su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la conversione al nuovo modello fallisce nel wisp-converter

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path @to_fix
  Scenario: Utente tenta il pagamento, poi riprova il flusso ma fallisce
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And l'utente ha tentato di pagare la RPT sul sito dell'EC
    When vengono inviate le richieste activatePaymentNoticeV2
    Then la conversione al nuovo modello fallisce nel wisp-converter
