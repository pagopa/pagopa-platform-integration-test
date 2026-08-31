#3236593816
#language:it
@CheckoutValidazioneCampi_006
@e2e
@checkout
@ui
Funzionalità: Validazione sintattica dei campi nel funnel di Checkout

  Contesto:
    Dato La pagina di checkout è aperta
    E La lingua è impostata su "it"


#======================================================
#======================================================

@CheckoutValidazioneCampi_006_01
@runnable
Schema dello scenario: Inserimento dati - errori -  Inserimento codice avviso errato
  Dato L’utente si trova sulla pagina "/inserisci-dati-avviso"
  Quando L’utente Inserisce il codice avviso <codice_avviso> all’interno della pagina
  E L’utente clicca sul tasto "Continua"
  Allora Il campo "Codice Avviso" viene segnalato in rosso
  E Viene mostrato il messaggio "Inserisci 18 cifre" sotto il campo "Codice Avviso"
  
  Esempi:
  | codice_avviso        |
  | 12345678901234567890 |
  | 12345678             |
  | aaabbbcccdddeeefff   |

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_02
@runnable
Schema dello scenario: Inserimento dati - errori -  Inserimento CF ente errato
  Dato L’utente si trova sulla pagina "/inserisci-dati-avviso"
  Quando L’utente Inserisce il CF ente <cf_ente> all’interno della pagina
  E L’utente clicca sul tasto "Continua"
  Allora Il campo "Codice Fiscale Ente Creditore" viene segnalato in rosso
  E Viene mostrato il messaggio "Inserisci 11 cifre" sotto il campo "Codice Fiscale Ente Creditore"
  
  Esempi:
  | cf_ente         |
  | 1234567890      |
  | 123456789012345 |
  | aaabbbcccdd     |

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_03
@runnable
Schema dello scenario: Inserimento dati - errori -  Inserimento indirizzo email non valido
  Dato L’utente si trova sulla pagina "/inserisci-email"
  Quando L’utente Inserisce l’indirizzo email <indirizzo_email> in uno dei due campi email presenti nella pagina
  E L’utente clicca sul tasto "Continua"
  Allora Il campo "Indirizzo email" viene segnalato in rosso
  E Viene mostrato il messaggio "<messaggio_errore>" sotto il campo "Indirizzo email"
  
  Esempi:
  | indirizzo_email | messaggio_errore                   |
  | aaaaaaaaaa      | Inserisci un indirizzo email valido |
  | aaaaaaaaaa@     | Inserisci un indirizzo email valido |
  | mail@gmail      | Inserisci un indirizzo email valido |

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_04
@runnable
Scenario: Inserimento dati - errori - indirizzo email diverso da ripeti
  Dato L’utente si trova sulla pagina "/inserisci-email"
  Quando L’utente inserisce un indirizzo email valido nel campo "Indirizzo Email"
  E L’utente inserisce un indirizzo email valido ma diverso dal precedente nel campo "Ripeti di nuovo"
  E L’utente clicca sul tasto "Continua"
  Allora Il campo "Ripeti di nuovo" viene segnalato in rosso
  E Viene mostrato il messaggio "Gli indirizzi email non coincidono" sotto il campo "Ripeti di nuovo"

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_05
@runnable
Schema dello scenario: Inserimento dati - errori -  Click sul tasto continua con campo non compilato
  Dato L’utente si trova sulla pagina "<pagina_corrente>"
  Quando L’utente lascia vuoto il solo campo "<campo>"
  E L’utente clicca sul tasto "Continua"
  Allora Viene mostrato il messaggio "Campo obbligatorio" sotto il campo "<campo>"
  
  Esempi:
  | pagina_corrente         | campo                          |
  | /inserisci-dati-avviso  | Codice Avviso                  | 
  | /inserisci-dati-avviso  | Codice Fiscale Ente Creditore  | 
  | /inserisci-email        | Indirizzo email                |
  | /inserisci-email        | Ripeti di nuovo                | 

  
