# language: en
@FEAT_01_Checkout @e2e @checkout @ui
Feature: Disponibilita opzione login in tutte le fasi del flusso di pagamento
  L'utente checkout vuole verificare che l'opzione di login sia disponibile nelle varie fasi del flusso di pagamento

  Background:
    Given La pagina di checkout e aperta
    And La lingua e impostata su "it"

  @positive
  @FEAT_01_Checkout_scenario_01
  Scenario: Opzione login disponibile durante l'inserimento dei dati avviso
    When L'utente inserisce i dati dell'avviso
    Then Il pulsante di login e visibile e abilitato
    And Il titolo del pulsante di login e "Accedi"

  @positive
  @FEAT_01_Checkout_scenario_02
  Scenario: Opzione login disponibile durante l'inserimento dei dati di pagamento
    When L'utente inserisce i dati dell'avviso
    And L'utente inserisce i dati di pagamento
    Then Il pulsante di login e visibile e abilitato
    And Il titolo del pulsante di login e "Accedi"

  @positive
  @FEAT_01_Checkout_scenario_03
  Scenario: Opzione login disponibile durante l'inserimento dell'email
    When L'utente inserisce i dati dell'avviso
    And L'utente inserisce i dati di pagamento
    And L'utente inserisce l'email
    Then Il pulsante di login e visibile e abilitato
    And Il titolo del pulsante di login e "Accedi"

  @positive
  @FEAT_01_Checkout_scenario_04
  Scenario: Opzione login disponibile durante la selezione del metodo di pagamento
    When L'utente inserisce i dati dell'avviso
    And L'utente inserisce i dati di pagamento
    And L'utente inserisce l'email
    And L'utente seleziona il metodo di pagamento
    Then Il pulsante di login e visibile e abilitato
    And Il titolo del pulsante di login e "Accedi"
