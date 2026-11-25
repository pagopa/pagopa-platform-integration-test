# language: it

@FEAT_002_Checkout
@e2e
@checkout
@ui
Funzionalità: Flusso di accesso con SPID
  Un utente del sistema checkout vuole autenticarsi tramite SPID e disconnettersi al termine della sessione
  così da poter completare il pagamento con le proprie credenziali identitarie

  Contesto:
    Dato La pagina di checkout è aperta
    E La lingua è impostata su "it"

  @smoke
  @positive
  @FEAT_002_Checkout_scenario_01
  Scenario: Accesso SPID completato con successo
    Quando L'utente clicca sul pulsante di login
    Allora L'utente ha effettuato l'accesso

  @smoke
  @positive
  @FEAT_002_Checkout_scenario_02
  Scenario: Logout SPID completato con successo
    Dato L'utente ha effettuato l'accesso con SPID
    Quando L'utente clicca sul pulsante utente
    E L'utente clicca sul sottomenu esci
    E L'utente conferma l'azione di logout
    Allora L'utente ha effettuato correttamente il logout
