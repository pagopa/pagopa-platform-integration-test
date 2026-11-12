#1234567890
# language: it
@FEAT_004_Checkout_Back_Navigation_Control_004
Funzionalità: Ritorno alla pagina precedente del flusso Checkout

  Contesto:
    Dato che l'utente si trova nella Home del Checkout "https://uat.checkout.pagopa.it/"
    E la lingua del Checkout è impostata su "italiano"

  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_01
  Scenario: Ritorno dall'inserimento dati avviso alla Home
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    Allora l'utente visualizza la pagina di inserimento dati avviso "/inserisci-dati-avviso"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza la Home del Checkout "/"

  # Dati approvati ma non verificati in UAT: D-001, D-002; avviso valido e non pagato da verificare; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_02
  Scenario: Ritorno dal riepilogo ai dati avviso conservando i valori inseriti
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il codice fiscale ente creditore "77777777777"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati avviso
    Allora l'utente visualizza il riepilogo dati pagamento "/dati-pagamento"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza la pagina di inserimento dati avviso "/inserisci-dati-avviso"
    E il campo codice avviso mostra ancora il valore inserito "302042025112600001"
    E il campo codice fiscale ente creditore mostra ancora il valore inserito "77777777777"

  # Dati approvati ma non verificati in UAT: D-001, D-002; avviso valido e non pagato da verificare; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_03
  Scenario: Ritorno dall'inserimento email al riepilogo con i dati avviso ancora visibili
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il codice fiscale ente creditore "77777777777"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati avviso
    E l'utente preme il pulsante "Vai al pagamento" nel riepilogo dati pagamento
    Allora l'utente visualizza la pagina di inserimento email "/inserisci-email"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza il riepilogo dati pagamento "/dati-pagamento"
    E il riepilogo mostra ancora il codice avviso inserito "302042025112600001"
    E il riepilogo mostra ancora il codice fiscale ente creditore inserito "77777777777"

  # Dati approvati ma percorso non verificato in UAT: D-001, D-002, D-003; avviso valido e non pagato da verificare; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_04
  Scenario: Ritorno dalla scelta metodo ai dati email conservando entrambi i campi
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il codice fiscale ente creditore "77777777777"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati avviso
    E l'utente preme il pulsante "Vai al pagamento" nel riepilogo dati pagamento
    E l'utente inserisce "mail@pagopa.it" nei campi indirizzo email e "Ripeti di nuovo"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento email
    Allora l'utente visualizza la pagina di scelta metodo di pagamento "/scegli-metodo"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza la pagina di inserimento email "/inserisci-email"
    E il campo indirizzo email mostra ancora il valore inserito "mail@pagopa.it"
    E il campo "Ripeti di nuovo" mostra ancora il valore inserito "mail@pagopa.it"

  # Dati approvati ma percorso non verificato in UAT: D-001, D-002, D-003; avviso e metodo carta da verificare; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_05
  Scenario: Ritorno dall'inserimento carta alla scelta metodo di pagamento
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il codice fiscale ente creditore "77777777777"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati avviso
    E l'utente preme il pulsante "Vai al pagamento" nel riepilogo dati pagamento
    E l'utente inserisce "mail@pagopa.it" nei campi indirizzo email e "Ripeti di nuovo"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento email
    E l'utente seleziona il metodo di pagamento "Carta di Credito"
    Allora l'utente visualizza la pagina di inserimento dati carta "/inserisci-carta"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza la pagina di scelta metodo di pagamento "/scegli-metodo"

  # Dati approvati ma non verificati in UAT: D-001..D-007; avviso, accettazione carta e accesso lista PSP da verificare; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_06
  Scenario: Ritorno dalla lista PSP ai dati carta conservando tutti i campi
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il codice fiscale ente creditore "77777777777"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati avviso
    E l'utente preme il pulsante "Vai al pagamento" nel riepilogo dati pagamento
    E l'utente inserisce "mail@pagopa.it" nei campi indirizzo email e "Ripeti di nuovo"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento email
    E l'utente seleziona il metodo di pagamento "Carta di Credito"
    E l'utente inserisce i seguenti dati della carta
      | campo        | valore           |
      | Numero carta | 5255000260000014 |
      | Scadenza     | 12/30            |
      | CVV          | 123              |
      | Intestata a  | Test test        |
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati carta
    Allora l'utente visualizza la pagina di scelta PSP "/lista-psp"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza la pagina di inserimento dati carta "/inserisci-carta"
    E il campo numero carta mostra ancora il valore inserito "5255000260000014"
    E il campo scadenza carta mostra ancora il valore inserito "12/30"
    E il campo CVV mostra ancora il valore inserito "123"
    E il campo "Intestata a" mostra ancora il valore inserito "Test test"

  # Tutte le righe: dati approvati ma percorsi non verificati in UAT; D-001, D-002, D-003, avviso, metodi e lista PSP da verificare; scenario non pronto all'esecuzione
  @regression
  @checkout
  @positive
  @FEAT_004_Checkout_Back_Navigation_Control_004_07
  Schema dello scenario: Ritorno dalla lista PSP alla scelta del metodo di pagamento
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302042025112600001" e il codice fiscale ente creditore "77777777777"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento dati avviso
    E l'utente preme il pulsante "Vai al pagamento" nel riepilogo dati pagamento
    E l'utente inserisce "mail@pagopa.it" nei campi indirizzo email e "Ripeti di nuovo"
    E l'utente preme il pulsante "Continua" nella pagina di inserimento email
    E l'utente seleziona il metodo di pagamento "<metodo>"
    Allora l'utente visualizza la pagina di scelta PSP "/lista-psp"
    Quando l'utente preme 1 sola volta il pulsante "Indietro" del Checkout
    Allora l'utente visualizza la pagina di scelta metodo di pagamento "/scegli-metodo"

    Esempi:
      | metodo       |
      | PayPal       |
      | Apple Pay    |
      | BANCOMAT Pay |
      | MyBank       |
