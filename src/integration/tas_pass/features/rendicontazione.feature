# qa-hub: FEAT_002_TasPass
# language: it
@TASPASS_002
Funzionalità: Verifica del flusso di rendicontazione verso l'ente creditore

  # ===============================================================================================
  # Scenari demo — suite tas_pass. Tutti gli scenari passano sempre.
  # ===============================================================================================

  @runnable @tas_pass @smoke
  @TASPASS_002_01
  Scenario: Il flusso di rendicontazione viene creato correttamente
    Dato che sono presenti transazioni da rendicontare
    Quando viene avviata la creazione del flusso di rendicontazione
    Allora il flusso di rendicontazione viene creato con successo

  # ===============================================================================================
  # ===============================================================================================

  @runnable @tas_pass @smoke
  @TASPASS_002_02
  Scenario: I dati del flusso di rendicontazione sono completi e coerenti
    Dato che il flusso di rendicontazione è stato creato
    Quando vengono verificati i dati del flusso
    Allora tutti i campi obbligatori del flusso risultano valorizzati

  # ===============================================================================================
  # ===============================================================================================

  @runnable @tas_pass @smoke
  @TASPASS_002_03
  Scenario: Il flusso di rendicontazione viene trasmesso all'ente creditore
    Dato che il flusso di rendicontazione è pronto per la trasmissione
    Quando viene avviata la trasmissione del flusso all'ente creditore
    Allora l'ente creditore conferma la ricezione del flusso
