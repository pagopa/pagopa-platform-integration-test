#0123456789
# language: it

@checkout_email_sintattica_001
Funzionalità: Validazione sintattica dei campi email nel checkout
  Come utente del checkout PagoPA
  Voglio inserire e confermare un indirizzo email sintatticamente valido
  Per poter proseguire alla pagina di scelta del metodo di pagamento

  Contesto:
    Dato che l'utente si trova nella pagina di inserimento email
    E la lingua impostata è l'italiano

  @checkout
  @smoke
  @positive
  @checkout_email_sintattica_001_01
  Scenario: Inserimento di un indirizzo email sintatticamente valido e coincidente nei due campi
    Quando l'utente inserisce "mario.rossi@esempio-test.it" nel campo "Indirizzo email"
    E l'utente inserisce "mario.rossi@esempio-test.it" nel campo "Ripeti di nuovo"
    E l'utente clicca sul pulsante "Continua"
    Allora l'utente avanza alla pagina di scelta del metodo di pagamento

  @checkout
  @regression
  @negative
  @checkout_email_sintattica_001_02
  Scenario: Indirizzo email sintatticamente non valido al passo 1
    Quando l'utente digita "mario.rossi@esempiotest" nel campo "Indirizzo email"
    Allora il sistema mostra, durante la digitazione, sotto il campo "Indirizzo email" il messaggio di errore "Inserisci un indirizzo email valido"
    Quando l'utente clicca sul pulsante "Continua"
    Allora il messaggio di errore rimane visibile sotto il campo "Indirizzo email"
    E l'utente non avanza alla pagina di scelta del metodo di pagamento

  @checkout
  @regression
  @negative
  @checkout_email_sintattica_001_03
  Schema dello scenario: Tentativo di proseguire con un indirizzo email malformato in un pattern specifico al passo 1
    Quando l'utente digita "<email>" nel campo "Indirizzo email"
    Allora il sistema mostra, durante la digitazione, sotto il campo "Indirizzo email" il messaggio di errore "Inserisci un indirizzo email valido"
    Quando l'utente clicca sul pulsante "Continua"
    Allora il messaggio di errore rimane visibile sotto il campo "Indirizzo email"
    E il sistema mostra anche sul campo "Indirizzo email" il messaggio di warning "<messaggio>"
    E l'utente non avanza alla pagina di scelta del metodo di pagamento

    Esempi:
      | email                     | messaggio                                                                     |
      | mariorossiesempiotest.it  | Aggiungi un simbolo "@" nell'indirizzo email. Nel valore manca un simbolo "@" |
      | mario.rossi@              | Inserisci una parte dopo "@". Il valore è incompleto.                        |

  @checkout
  @regression
  @negative
  @checkout_email_sintattica_001_04
  Scenario: Indirizzo email sintatticamente non valido al passo 2
    Quando l'utente inserisce "mario.rossi@esempio-test.it" nel campo "Indirizzo email"
    E l'utente digita "mario.rossi@esempiotest" nel campo "Ripeti di nuovo"
    Allora il sistema mostra, durante la digitazione, sotto il campo "Ripeti di nuovo" il messaggio di errore "Inserisci un indirizzo email valido"
    Quando l'utente clicca sul pulsante "Continua"
    Allora il messaggio di errore rimane visibile sotto il campo "Ripeti di nuovo"
    E l'utente non avanza alla pagina di scelta del metodo di pagamento

  @checkout
  @regression
  @negative
  @checkout_email_sintattica_001_05
  Schema dello scenario: Tentativo di proseguire con un indirizzo email di conferma malformato in un pattern specifico al passo 2
    Quando l'utente inserisce "mario.rossi@esempio-test.it" nel campo "Indirizzo email"
    E l'utente digita "<conferma>" nel campo "Ripeti di nuovo"
    Allora il sistema mostra, durante la digitazione, sotto il campo "Ripeti di nuovo" il messaggio di errore "Inserisci un indirizzo email valido"
    Quando l'utente clicca sul pulsante "Continua"
    Allora il messaggio di errore rimane visibile sotto il campo "Ripeti di nuovo"
    E il sistema mostra anche sul campo "Ripeti di nuovo" il messaggio di warning "<messaggio>"
    E l'utente non avanza alla pagina di scelta del metodo di pagamento

    Esempi:
      | conferma                  | messaggio                                                                     |
      | mariorossiesempiotest.it  | Aggiungi un simbolo "@" nell'indirizzo email. Nel valore manca un simbolo "@" |
      | mario.rossi@              | Inserisci una parte dopo "@". Il valore è incompleto.                        |

  @checkout
  @regression
  @negative
  @checkout_email_sintattica_001_06
  Scenario: Inserimento al passo 2 di un indirizzo email valido ma diverso da quello del passo 1
    Quando l'utente inserisce "mario.rossi@esempio-test.it" nel campo "Indirizzo email"
    E l'utente digita "luigi.verdi@esempio-test.it" nel campo "Ripeti di nuovo"
    Allora il sistema mostra, durante la digitazione, sotto il campo "Ripeti di nuovo" il messaggio di errore "Gli indirizzi email non coincidono"
    Quando l'utente clicca sul pulsante "Continua"
    Allora il messaggio di errore rimane visibile sotto il campo "Ripeti di nuovo"
    E il click non produce alcuna azione osservabile
    E l'utente non avanza alla pagina di scelta del metodo di pagamento
