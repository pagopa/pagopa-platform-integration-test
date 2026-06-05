Feature: Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT

  Background:
    Given i sistemi sono operativi

    @runnable @nodo_invia_rpt @happy_path
    Scenario: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  @runnable @nodo_invia_rpt @happy_path
  Scenario: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
    Given una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

    @runnable @nodo_invia_rpt @happy_path
    Scenario: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
    Given una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: Utente tenta di pagare un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD in stato non valido
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a DRAFT
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato valido
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a VALID
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  Scenario: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido
    Given una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a DRAFT
    When l'utente tenta di pagare la RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata
