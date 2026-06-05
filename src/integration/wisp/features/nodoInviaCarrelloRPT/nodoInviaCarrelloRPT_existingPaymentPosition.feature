Feature: L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT

  Background:
    Given i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  Scenario: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    And una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then l'utente viene reindirizzato su Checkout completando il pagamento
    And la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a DRAFT
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato non valido
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a DRAFT
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a DRAFT
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato non valido
    Given un carrello di RPT non-multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a DRAFT
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido
    Given un carrello di RPT for multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a DRAFT
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato valido
    Given un carrello di RPT for multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato non valido
    Given un carrello di RPT for multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a DRAFT
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  Scenario: L'utente paga un carrello multibeneficiario gia esistente in GPD
    Given un carrello di RPT for multibeneficiary
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    And una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    When l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Then la conversione al nuovo modello fallisce nel wisp-converter
    And la ricevuta KO è inviata
