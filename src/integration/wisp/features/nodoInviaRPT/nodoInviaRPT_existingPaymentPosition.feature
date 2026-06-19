#3115780617
#language:it
@NodoInviaRPT_ExistingPaymentPosition_003
Funzionalità: Utente paga un pagamento singolo da posizione debitoria esistente tramite nodoInviaRPT

  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_ExistingPaymentPosition_003_01
  Scenario: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_ExistingPaymentPosition_003_02
  Scenario: Utente paga un pagamento singolo senza versamenti semplici e una marca da bollo gia esistente in GPD
    Data una singola RPT di tipo BBT con 1 versamenti di cui 1 sono marche da bollo
    E una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_ExistingPaymentPosition_003_03
  Scenario: Utente paga un pagamento singolo con un versamento e una marca da bollo gia esistente in GPD
    Data una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  @NodoInviaRPT_ExistingPaymentPosition_003_04
  Scenario: Utente tenta di pagare un pagamento singolo con un versamento e nessuna marca da bollo gia esistente in GPD in stato non valido
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 48 e stato uguale a DRAFT
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  @NodoInviaRPT_ExistingPaymentPosition_003_05
  Scenario: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato valido
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a VALID
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  @NodoInviaRPT_ExistingPaymentPosition_003_06
  Scenario: Utente tenta di pagare un pagamento singolo inserito da ACA e in stato non valido
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla first RPT con segregation code uguale a 01 e stato uguale a DRAFT
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata
