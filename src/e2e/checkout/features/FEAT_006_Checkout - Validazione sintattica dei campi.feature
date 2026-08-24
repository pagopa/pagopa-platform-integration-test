#3236593816
#language:it
@CheckoutValidazioneCampi_006
Funzionalità: Validazione sintattica dei campi nel funnel di Checkout

  Contesto:
    Dato La pagina di checkout e aperta
	  E La lingua e impostata su "it"


#======================================================
#======================================================

@CheckoutValidazioneCampi_006_01
Schema dello scenario: Inserimento dati - errori -  Inserimento codice avviso errato
  Dato L’utente si trova sulla pagina /inserisci-dati-avviso
  Quando L’utente Inserisce il codice avviso {codice_avviso} all’interno della pagina
  E L’utente clicca sul tasto Continua
  Allora Il campo codice avviso viene segnalato in rosso
  E Viene mostrato il messaggio “inserisci 18 cifre” sotto il campo codice avviso
  
  Esempi:
  | codice_avviso        |
  | 12345678901234567890 |
  | 12345678             |
  | aaabbbcccdddeeefff   |

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_02
Schema dello scenario: Inserimento dati - errori -  Inserimento CF ente errato
  Dato L’utente si trova sulla pagina /inserisci-dati-avviso
  Quando L’utente Inserisce il CF ente {CF_ente} all’interno della pagina
  E L’utente clicca sul tasto Continua
  Allora Il campo codice avviso viene segnalato in rosso
  E Viene mostrato il messaggio “inserisci 11 cifre” sotto il campo codice fiscale ente creditore
  
  Esempi:
  | CF_ente         | 
  | 1234567890      |
  | 123456789012345 |
  | aaabbbcccdd     |

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_03
Schema dello scenario: Inserimento dati - errori -  Inserimento indirizzo mail non valido
  Dato L’utente si trova sulla pagina /inserisci-email
  Quando L’utente Inserisce l’indirizzo email {indirizzo_email} in uno dei due campi mail presenti nella pagina
  E L’utente clicca sul tasto Continua
  Allora Il campo codice avviso viene segnalato in rosso
  E Sul campo viene mostrato il messaggio di warning {messaggio_warning}
  E Sotto il campo viene mostrato il messaggio di errore {messaggio_errore}
  
  Esempi:
  | indirizzo_email | messaggio_warning                                                                   | messaggio_errore                   |
  | aaaaaaaaaa      | Aggiungi un simbolo "@" nell'indirizzo email. In "aaaaaaaaaa" manca un simbolo "@". | Inserisci un indirizzo mail valido |
  | aaaaaaaaaa@     | Inserisci una parte dopo "@". Il valore "aaaaaaaaaa@" è incompleto.                 | Inserisci un indirizzo mail valido |
  | mail@gmail      |                                                                                     | Inserisci un indirizzo mail valido |

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_04
Scenario: Inserimento dati - errori - indirizzo email diverso da ripeti
  Dato L’utente si trova sulla pagina /inserisci-email
  Quando L’utente inserisce un indirizzo email valido nel campo “Indirizzo Email”
  E L’utente inserisce un indirizzo email valido ma diverso dal precedente nel campo “Ripeti di Nuovo”
  E L’utente clicca sul tasto Continua
  Allora Il campo “Ripeti di Nuovo” viene segnalato in rosso
  E Sotto il campo “Ripeti di Nuovo” viene mostrato il messaggio di errore “Gli indirizzi email non coincidono”

#======================================================
#======================================================

@CheckoutValidazioneCampi_006_05
Schema dello scenario: Inserimento dati - errori -  Click sul tasto continua con campo non compilato
  Dato L’utente si trova sulla pagina {pagina_corrente}
  Quando L’utente lascia vuoto il solo campo {campo}
  E L’utente clicca sul tasto Continua
  Allora Sul campo {campo} viene mostrato il messaggio di warning " Compila questo campo "
  
  Esempi:
  | pagina_corrente         | campo                          |
  | /inserisci-dati-avviso  | Codice Avviso                  | 
  | /inserisci-dati-avviso  | Codice Fiscale Ente Creditore  | 
  | /inserisci-email        | Indirizzo Email                | 
  | /inserisci-email        | Ripeti di nuovo                | 

  
