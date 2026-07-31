#0000000008
#language:it
@TAS_Mixed_002
Funzionalità: Validazione del flusso di pagamento tramite canale pagoPA

  # ===============================================================================================
  # Scenari demo — suite tas_mixed. Esito misto: scenario 1 fallisce, scenari 2 e 3 passano.
  # ===============================================================================================

  @runnable @tas_mixed @smoke
  @TAS_Mixed_002_01
  Scenario: L'utente avvia correttamente un pagamento singolo
    Dato che l'utente ha un avviso di pagamento valido
    Quando l'utente avvia il pagamento tramite il canale pagoPA
    Allora la richiesta di pagamento viene accettata dal sistema

  # ===============================================================================================
  # ===============================================================================================

  @runnable @tas_mixed @smoke
  @TAS_Mixed_002_02
  Scenario: Il pagamento viene elaborato e la transazione aggiornata
    Dato che una richiesta di pagamento è in corso di elaborazione
    Quando il sistema elabora la transazione
    Allora la transazione risulta completata con stato "CONFERMATO"

  # ===============================================================================================
  # ===============================================================================================

  @runnable @tas_mixed @smoke
  @TAS_Mixed_002_03
  Scenario: La ricevuta telematica viene generata al completamento del pagamento
    Dato che il pagamento è stato completato con successo
    Quando il sistema genera la ricevuta telematica
    Allora la ricevuta contiene i dati attesi della transazione
