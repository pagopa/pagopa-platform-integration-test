@FEAT_005_Checkout @e2e @checkout @ui
Feature: Ordinamento lista PSP in Checkout
  L'utente checkout vuole poter ordinare la lista PSP (Payment Service Provider)
  cosi da poter scegliere il prestatore piu conveniente per commissione o nome

  Background:
    Given La pagina di checkout e aperta
    And La lingua e impostata su "it"
    And L'utente inserisce un codice avviso valido con prefisso "30202"
    And L'utente inserisce un codice fiscale valido del pagatore

  # ──────────────────────────────────────────────
  # Ordinamento pagina di riepilogo
  # ──────────────────────────────────────────────

  @positive
  @FEAT_005_Checkout_scenario_01
  Scenario: La lista PSP e ordinata per commissione in ordine crescente nella pagina di riepilogo
    When L'utente inserisce le informazioni dell'avviso
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga nella pagina di riepilogo
    And L'utente inserisce e conferma l'email
    And L'utente seleziona il metodo di pagamento "PPAL"
    And L'utente seleziona il PSP con id radio "BCITITMM"
    And L'utente clicca il pulsante continua della lista PSP
    And L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    And L'utente clicca il pulsante "ordina per commissione"
    And L'utente clicca il pulsante "ordina per commissione"
    Then La lista delle commissioni PSP e ordinata in ordine crescente
    And L'utente annulla il pagamento

  @positive
  @FEAT_005_Checkout_scenario_02
  Scenario: La lista PSP e ordinata per commissione in ordine decrescente nella pagina di riepilogo
    When L'utente inserisce le informazioni dell'avviso
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga nella pagina di riepilogo
    And L'utente inserisce e conferma l'email
    And L'utente seleziona il metodo di pagamento "PPAL"
    And L'utente seleziona il PSP con id radio "BCITITMM"
    And L'utente clicca il pulsante continua della lista PSP
    And L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    And L'utente clicca il pulsante "ordina per commissione"
    Then La lista delle commissioni PSP e ordinata in ordine decrescente
    And L'utente annulla il pagamento

  @positive
  @FEAT_005_Checkout_scenario_03
  Scenario: La lista PSP e ordinata per nome in ordine decrescente nella pagina di riepilogo
    When L'utente inserisce le informazioni dell'avviso
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga nella pagina di riepilogo
    And L'utente inserisce e conferma l'email
    And L'utente seleziona il metodo di pagamento "PPAL"
    And L'utente seleziona il PSP con id radio "BCITITMM"
    And L'utente clicca il pulsante continua della lista PSP
    And L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    And L'utente clicca il pulsante "ordina per nome"
    Then La lista dei nomi PSP e ordinata in ordine alfabetico decrescente
    And L'utente annulla il pagamento

  @positive
  @FEAT_005_Checkout_scenario_04
  Scenario: La lista PSP e ordinata per nome in ordine crescente nella pagina di riepilogo
    When L'utente inserisce le informazioni dell'avviso
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga nella pagina di riepilogo
    And L'utente inserisce e conferma l'email
    And L'utente seleziona il metodo di pagamento "PPAL"
    And L'utente seleziona il PSP con id radio "BCITITMM"
    And L'utente clicca il pulsante continua della lista PSP
    And L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    And L'utente clicca il pulsante "ordina per nome"
    And L'utente clicca il pulsante "ordina per nome"
    Then La lista dei nomi PSP e ordinata in ordine alfabetico crescente
    And L'utente annulla il pagamento
  # ──────────────────────────────────────────────
  # Ordinamento pagina di selezione PSP
  # ──────────────────────────────────────────────

  @positive
  @FEAT_005_Checkout_scenario_05
  Scenario: La lista PSP e ordinata per nome nella pagina di selezione PSP
    When L'utente inserisce le informazioni dell'avviso
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga nella pagina di riepilogo
    And L'utente inserisce e conferma l'email
    And L'utente seleziona il metodo di pagamento "PPAL"
    And La pagina di selezione PSP e caricata
    And L'utente clicca il pulsante ordina lista PSP
    And L'utente seleziona l'opzione radio "ordina per nome"
    And L'utente clicca il pulsante mostra risultati
    Then La lista dei nomi PSP e ordinata in ordine alfabetico crescente

  @positive
  @FEAT_005_Checkout_scenario_06
  Scenario: La lista PSP e ordinata per commissione nella pagina di selezione PSP
    When L'utente inserisce le informazioni dell'avviso
    And L'utente clicca il pulsante verifica
    And L'utente clicca il pulsante paga nella pagina di riepilogo
    And L'utente inserisce e conferma l'email
    And L'utente seleziona il metodo di pagamento "PPAL"
    And La pagina di selezione PSP e caricata
    And L'utente clicca il pulsante ordina lista PSP
    And L'utente seleziona l'opzione radio "ordina per importo"
    And L'utente clicca il pulsante mostra risultati
    Then La lista delle commissioni PSP e ordinata in ordine crescente
