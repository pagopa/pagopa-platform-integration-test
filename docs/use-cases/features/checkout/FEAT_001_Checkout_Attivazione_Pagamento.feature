#0123456789
# language: it
@FEAT_001_Checkout_Attivazione_Pagamento_001
Funzionalità: Avvio del pagamento Checkout fino al reindirizzamento esterno

  Contesto:
    Dato che l'utente si trova nella homepage "https://uat.checkout.pagopa.it/"
    E la lingua del Checkout è impostata su "it"

  # Dati e stati non verificati nell'ambiente: D-001, D-002, D-004, D-005, D-006, D-008; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_001_Checkout_Attivazione_Pagamento_001_01
  Scenario: Avvio del pagamento con carta di credito e scelta del PSP
    Dato che l'avviso "302042025112600001" dell'ente "77777777777" è disponibile e non è già pagato
    E il metodo "Carta di credito" è disponibile per l'avviso
    E la carta di test è utilizzabile con il PSP "Postepay" disponibile per l'avviso
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il CF ente creditore "77777777777"
    E l'utente preme "Continua" nella pagina di inserimento dati avviso
    E l'utente preme "Vai al pagamento" nel riepilogo dei dati dell'avviso
    E l'utente inserisce "mail@pagopa.it" nei campi "Indirizzo email" e "Ripeti di nuovo"
    E l'utente preme "Continua" nella pagina di inserimento email
    E l'utente sceglie il metodo "Carta di credito"
    E l'utente compila i dettagli della carta di test
      | numero_carta     | scadenza | cvv | intestata_a |
      | 5255000260000014 | 12/30    | 123 | Test test   |
    E l'utente preme "Continua" nella pagina di inserimento carta
    E l'utente seleziona tramite radio button il PSP con nome "Postepay"
    E l'utente preme "Continua" nella lista PSP
    E l'utente preme il pulsante "Paga" relativo al totale visualizzato nel riepilogo del pagamento
    Allora il browser viene reindirizzato al di fuori del dominio "uat.checkout.pagopa.it"

  # Tutte le righe: D-001, D-002, D-005, D-006, D-008 non verificati nell'ambiente; scenario non pronto all'esecuzione
  # D-005 irrisolto nelle righe Apple Pay, BANCOMAT Pay e MyBank
  @regression
  @checkout
  @positive
  @FEAT_001_Checkout_Attivazione_Pagamento_001_02
  Schema dello scenario: Avvio del pagamento con metodo alternativo e scelta del PSP
    Dato che l'avviso "302042025112600001" dell'ente "77777777777" è disponibile e non è già pagato
    E il metodo "<metodo>" è disponibile per l'avviso
    E il PSP con identificativo "<psp>" è disponibile per il metodo "<metodo>" e per l'avviso
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il CF ente creditore "77777777777"
    E l'utente preme "Continua" nella pagina di inserimento dati avviso
    E l'utente preme "Vai al pagamento" nel riepilogo dei dati dell'avviso
    E l'utente inserisce "mail@pagopa.it" nei campi "Indirizzo email" e "Ripeti di nuovo"
    E l'utente preme "Continua" nella pagina di inserimento email
    E l'utente sceglie il metodo "<metodo>"
    E l'utente seleziona tramite radio button il PSP con identificativo "<psp>"
    E l'utente preme "Continua" nella lista PSP
    E l'utente preme il pulsante "Paga" relativo al totale visualizzato nel riepilogo del pagamento
    Allora il browser viene reindirizzato al di fuori del dominio "uat.checkout.pagopa.it"

    Esempi:
      | metodo       | psp           |
      | PayPal       | BCITITMM      |
      | Apple Pay    | __TODO_D005__ |
      | BANCOMAT Pay | __TODO_D005__ |
      | MyBank       | __TODO_D005__ |

  # Tutte le righe: D-001, D-002, D-006, D-008 non verificati nell'ambiente; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_001_Checkout_Attivazione_Pagamento_001_03
  Schema dello scenario: Avvio del pagamento con accesso diretto al riepilogo dopo la scelta del metodo
    Dato che l'avviso "302042025112600001" dell'ente "77777777777" è disponibile e non è già pagato
    E il metodo "<metodo>" è disponibile per l'avviso
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il CF ente creditore "77777777777"
    E l'utente preme "Continua" nella pagina di inserimento dati avviso
    E l'utente preme "Vai al pagamento" nel riepilogo dei dati dell'avviso
    E l'utente inserisce "mail@pagopa.it" nei campi "Indirizzo email" e "Ripeti di nuovo"
    E l'utente preme "Continua" nella pagina di inserimento email
    E l'utente sceglie il metodo "<metodo>"
    E l'utente preme il pulsante "Paga" relativo al totale visualizzato nel riepilogo del pagamento
    Allora il browser viene reindirizzato al di fuori del dominio "uat.checkout.pagopa.it"

    Esempi:
      | metodo               |
      | Google Pay           |
      | Conto iCONTO         |
      | Conto Intesa Sanpaolo |
      | Fabrick Pay By Bank   |
      | Klarna               |
