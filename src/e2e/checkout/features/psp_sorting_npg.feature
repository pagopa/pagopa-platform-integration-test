# language: it

@FEAT_005_Checkout
@e2e
@checkout
@ui
Funzionalità: Ordinamento lista PSP in Checkout
  L'utente checkout vuole poter ordinare la lista PSP (Payment Service Provider)
  cosi da poter scegliere il prestatore piu conveniente per commissione o nome

  Contesto:
    Dato La pagina di checkout è aperta
    E La lingua è impostata su "it"
    E L'utente inserisce un codice avviso valido con prefisso "30202"
    E L'utente inserisce un codice fiscale valido del pagatore

  # ──────────────────────────────────────────────
  # Ordinamento pagina di riepilogo
  # ──────────────────────────────────────────────

  @smoke
  @positive
  @FEAT_005_Checkout_scenario_01
  Scenario: La lista PSP è ordinata per commissione in ordine crescente nella pagina di riepilogo
    Quando L'utente inserisce le informazioni dell'avviso
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga nella pagina di riepilogo
    E L'utente inserisce e conferma l'email
    E L'utente seleziona il metodo di pagamento "PPAL"
    E L'utente seleziona il PSP con id radio "BCITITMM"
    E L'utente clicca il pulsante continua della lista PSP
    E L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    E L'utente clicca il pulsante "ordina per commissione"
    E L'utente clicca il pulsante "ordina per commissione"
    Allora La lista delle commissioni PSP è ordinata in ordine crescente
    E L'utente annulla il pagamento

  @smoke
  @positive
  @FEAT_005_Checkout_scenario_02
  Scenario: La lista PSP è ordinata per commissione in ordine decrescente nella pagina di riepilogo
    Quando L'utente inserisce le informazioni dell'avviso
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga nella pagina di riepilogo
    E L'utente inserisce e conferma l'email
    E L'utente seleziona il metodo di pagamento "PPAL"
    E L'utente seleziona il PSP con id radio "BCITITMM"
    E L'utente clicca il pulsante continua della lista PSP
    E L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    E L'utente clicca il pulsante "ordina per commissione"
    Allora La lista delle commissioni PSP è ordinata in ordine decrescente
    E L'utente annulla il pagamento

  @smoke
  @positive
  @FEAT_005_Checkout_scenario_03
  Scenario: La lista PSP è ordinata per nome in ordine decrescente nella pagina di riepilogo
    Quando L'utente inserisce le informazioni dell'avviso
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga nella pagina di riepilogo
    E L'utente inserisce e conferma l'email
    E L'utente seleziona il metodo di pagamento "PPAL"
    E L'utente seleziona il PSP con id radio "BCITITMM"
    E L'utente clicca il pulsante continua della lista PSP
    E L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    E L'utente clicca il pulsante "ordina per nome"
    Allora La lista dei nomi PSP è ordinata in ordine alfabetico decrescente
    E L'utente annulla il pagamento

  @smoke
  @positive
  @FEAT_005_Checkout_scenario_04
  Scenario: La lista PSP è ordinata per nome in ordine crescente nella pagina di riepilogo
    Quando L'utente inserisce le informazioni dell'avviso
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga nella pagina di riepilogo
    E L'utente inserisce e conferma l'email
    E L'utente seleziona il metodo di pagamento "PPAL"
    E L'utente seleziona il PSP con id radio "BCITITMM"
    E L'utente clicca il pulsante continua della lista PSP
    E L'utente clicca il pulsante modifica PSP nella pagina di riepilogo
    E L'utente clicca il pulsante "ordina per nome"
    E L'utente clicca il pulsante "ordina per nome"
    Allora La lista dei nomi PSP è ordinata in ordine alfabetico crescente
    E L'utente annulla il pagamento
  # ──────────────────────────────────────────────
  # Ordinamento pagina di selezione PSP
  # ──────────────────────────────────────────────

  @smoke
  @positive
  @FEAT_005_Checkout_scenario_05
  Scenario: La lista PSP è ordinata per nome nella pagina di selezione PSP
    Quando L'utente inserisce le informazioni dell'avviso
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga nella pagina di riepilogo
    E L'utente inserisce e conferma l'email
    E L'utente seleziona il metodo di pagamento "PPAL"
    E La pagina di selezione PSP è caricata
    E L'utente clicca il pulsante ordina lista PSP
    E L'utente seleziona l'opzione radio "ordina per nome"
    E L'utente clicca il pulsante mostra risultati
    Allora La lista dei nomi PSP è ordinata in ordine alfabetico crescente

  @smoke
  @positive
  @FEAT_005_Checkout_scenario_06
  Scenario: La lista PSP è ordinata per commissione nella pagina di selezione PSP
    Quando L'utente inserisce le informazioni dell'avviso
    E L'utente clicca il pulsante verifica
    E L'utente clicca il pulsante paga nella pagina di riepilogo
    E L'utente inserisce e conferma l'email
    E L'utente seleziona il metodo di pagamento "PPAL"
    E La pagina di selezione PSP è caricata
    E L'utente clicca il pulsante ordina lista PSP
    E L'utente seleziona l'opzione radio "ordina per importo"
    E L'utente clicca il pulsante mostra risultati
    Allora La lista delle commissioni PSP è ordinata in ordine crescente
