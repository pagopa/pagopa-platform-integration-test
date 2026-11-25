#0000000004
#language:it
@TAS_Fail_001
Funzionalità: Verifica dell'operatività dei servizi core della piattaforma pagoPA

  # ===============================================================================================
  # Scenari demo — suite tas_fail. Tutti gli scenari falliscono sempre.
  # ===============================================================================================

  @runnable @tas_fail @smoke
  @TAS_Fail_001_01
  Scenario: Il servizio di pagamento risponde correttamente alle richieste
    Dato che il servizio di pagamento è raggiungibile
    Quando viene inviata una richiesta di healthcheck
    Allora la risposta ha codice HTTP 200

  # ===============================================================================================
  # ===============================================================================================

  @runnable @tas_fail @smoke
  @TAS_Fail_001_02
  Scenario: La connettività verso il nodo dei pagamenti è attiva
    Dato che il nodo dei pagamenti è configurato
    Quando viene verificata la connettività di rete verso il nodo
    Allora il nodo risponde entro il tempo limite previsto

  # ===============================================================================================
  # ===============================================================================================

  @runnable @tas_fail @smoke
  @TAS_Fail_001_03
  Scenario: I parametri di configurazione dell'ambiente sono completi
    Dato che il sistema è configurato per l'ambiente di test
    Quando vengono verificati i parametri obbligatori di configurazione
    Allora tutti i parametri di configurazione risultano validi
