#3115779999
#language:it
@NodoInviaRPT_NoStamp_001
Funzionalità: Utente paga un pagamento singolo senza marche da bollo tramite nodoInviaRPT
 
  Contesto:
    Dati i sistemi sono operativi

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_01
  Scenario: Utente paga un pagamento singolo con un versamento e nessuna marca da bollo
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_02
  Scenario: Utente paga un pagamento singolo con due versamenti e nessuna marca da bollo
    Data una singola RPT di tipo BBT con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_03
  Scenario: Utente paga un pagamento singolo con tre versamenti e nessuna marca da bollo
    Data una singola RPT di tipo BBT con 3 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_04
  Scenario: Utente paga un pagamento singolo con quattro versamenti e nessuna marca da bollo
    Data una singola RPT di tipo BBT con 4 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_05
  Scenario: Utente paga un pagamento singolo con cinque versamenti e nessuna marca da bollo
    Data una singola RPT di tipo BBT con 5 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_06
  Scenario: Utente paga un pagamento singolo di tipo PO con un versamento e nessuna marca da bollo
    Data una singola RPT di tipo PO con 1 versamenti di cui none sono marche da bollo
    Quando l'utente invia una richiesta nodoInviaRPT
    Allora l'utente riceve una risposta con esito positivo
    E la risposta contiene il vecchio URL WISP

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  @NodoInviaRPT_NoStamp_001_07
  Scenario: Utente paga un pagamento singolo di tipo PO con due versamenti e nessuna marca da bollo
    Data una singola RPT di tipo PO con 2 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC ma il pagamento fallisce
    Allora il pagamento fallisce having invalid semantic validation due to incorrect RPT structure e viene restituito l'errore PPT_SEMANTICA

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @happy_path
  @NodoInviaRPT_NoStamp_001_08
  Scenario: Utente esegue un primo reindirizzamento, poi ripete il reindirizzamento e completa il flusso di pagamento
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora la conversione al nuovo modello ha successo nel wisp-converter
    E l'utente viene reindirizzato nuovamente su Checkout completando il pagamento

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path
  @NodoInviaRPT_NoStamp_001_09
  Scenario: Utente tenta due volte di pagare la stessa RPT ma la conversione al nuovo modello fallisce
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    Quando l'utente tenta di pagare la RPT sul sito dell'EC
    Allora l'utente viene reindirizzato su Checkout completando il pagamento
    E la conversione al nuovo modello fallisce nel wisp-converter

  # ===============================================================================================
  # ===============================================================================================

  @runnable @nodo_invia_rpt @unhappy_path @to_fix
  @NodoInviaRPT_NoStamp_001_10
  Scenario: Utente tenta il pagamento, poi riprova il flusso ma fallisce
    Data una singola RPT di tipo BBT con 1 versamenti di cui none sono marche da bollo
    E l'utente ha tentato di pagare la RPT sul sito dell'EC
    Quando vengono inviate le richieste activatePaymentNoticeV2
    Allora la conversione al nuovo modello fallisce nel wisp-converter
