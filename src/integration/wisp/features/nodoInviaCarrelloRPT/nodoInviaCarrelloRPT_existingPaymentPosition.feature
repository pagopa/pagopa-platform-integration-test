# qa-hub: FEAT_001_Wisp
# language: it
@WISP_001
Funzionalità: L'utente paga carrelli di pagamento da posizione debitoria esistente tramite nodoInviaCarrelloRPT
  
  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @WISP_001_01
  Scenario: L'utente paga un carrello con singola RPT senza marca da bollo gia esistente in GPD
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @WISP_001_02
  Scenario: L'utente paga un carrello con singola RPT con versamenti multipli gia esistente in GPD
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @WISP_001_03
  Scenario: L'utente paga un carrello con singola RPT con una marca da bollo gia esistente in GPD
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @WISP_001_04
  Scenario: L'utente paga un carrello con due RPT senza marca da bollo di cui una gia esistente in GPD
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @WISP_001_05
  Scenario: L'utente paga un carrello con due RPT con versamenti multipli gia esistente in GPD
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @happy_path
  @WISP_001_06
  Scenario: L'utente paga un carrello con due RPT con almeno una marca da bollo gia esistente in GPD
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 2 versamenti di cui 1 sono marche da bollo
    E una singola RPT di tipo BBT con 3 versamenti di cui 1 sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la posizione debitoria è chiusa

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_07
  Scenario: L'utente tenta di pagare un carrello con singola RPT gia esistente in GPD in stato non valido
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a DRAFT
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_08
  Scenario: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato valido
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 01 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_09
  Scenario: L'utente tenta di pagare un carrello con singola RPT inserita da ACA e in stato non valido
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 01 e stato uguale a DRAFT
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_10
  Scenario: L'utente tenta di pagare un carrello con due RPT gia esistenti in GPD in stato non valido
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a DRAFT
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_11
  Scenario: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato valido
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 01 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_12
  Scenario: L'utente tenta di pagare un carrello con due RPT inserite da ACA e in stato non valido
    Dato un carrello di RPT non multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 01 e stato uguale a DRAFT
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_13
  Scenario: L'utente tenta di pagare un carrello multibeneficiario gia esistente in GPD in stato non valido
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a DRAFT
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_14
  Scenario: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato valido
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 01 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_15
  Scenario: L'utente tenta di pagare un carrello multibeneficiario inserito da ACA e in stato non valido
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 01 e stato uguale a DRAFT
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata

  # ===============================================================================================
  # ===============================================================================================

  @nodo_invia_carrello_rpt @unhappy_path
  @WISP_001_16
  Scenario: L'utente paga un carrello multibeneficiario gia esistente in GPD
    Dato un carrello di RPT multi-beneficiario
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E una posizione debitoria esistente relativa alla prima RPT con segregation code uguale a 48 e stato uguale a VALID
    Quando l'utente tenta di pagare il carrello di RPT sul sito dell'EC
    Allora la conversione al nuovo modello fallisce nel wisp-converter
    E la ricevuta KO è inviata
