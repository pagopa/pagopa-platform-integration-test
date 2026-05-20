# Created by mpiccolo at 16/04/2026
@FEAT_002_Checkout @e2e @checkout @ui
Feature: Flusso di accesso con SPID

  Background:
    Given La pagina di checkout e aperta
    And La lingua e impostata su "it"

  @checkout @positive
  @FEAT_002_Checkout_scenario_01
  Scenario: Accesso SPID completato con successo
    When L'utente clicca sul pulsante di login
    Then L'utente ha effettuato l'accesso

  @checkout @positive
  @FEAT_002_Checkout_scenario_02
  Scenario: Logout SPID completato con successo
    Given L'utente ha effettuato l'accesso con SPID
    When L'utente clicca sul pulsante utente
    And L'utente clicca sul sottomenu esci
    And L'utente conferma l'azione di logout
    Then L'utente ha effettuato correttamente il logout
