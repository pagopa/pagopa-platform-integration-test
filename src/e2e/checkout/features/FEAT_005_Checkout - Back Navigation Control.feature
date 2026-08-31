#3236693113
#language:it
@CheckoutBackNavigation_005
@e2e
@checkout
@ui
Funzionalità: Navigazione Lineare per il flusso di Pagamento

  Contesto:
    Dato La pagina di checkout è aperta
	  E La lingua è impostata su "it"

#======================================================
#======================================================

@CheckoutBackNavigation_005_01
@runnable
@happy_path
Scenario: Navigazione - Selezione tasto Inserisci tu i dati
  Dato L’utente si trova sulla pagina "/"
  Quando L’utente clicca sul tasto "Inserisci tu i dati"
  Allora L’utente viene reindirizzato sulla pagina "/inserisci-dati-avviso"
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_02
@runnable
@happy_path
Scenario: Navigazione - pagina dati avviso
  Dato L’utente si trova sulla pagina "/inserisci-dati-avviso"
  E L’utente ha compilato i dati avviso inserendo il codice avviso "302042025112600001" e il CF ente "77777777777"
  Quando L’utente clicca sul tasto "Continua"
  Allora L’utente viene reindirizzato sulla pagina "/dati-pagamento"
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_03
@runnable
@happy_path
Scenario: Navigazione - Conferma pagina di riepilogo
  Dato L’utente si trova sulla pagina "/dati-pagamento"
  Quando L’utente clicca sul tasto "Vai al pagamento"
  Allora L’utente viene reindirizzato sulla pagina "/inserisci-email"
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_04
@runnable
@happy_path
Scenario: Navigazione - Inserimento email
  Dato L’utente si trova sulla pagina "/inserisci-email"
  E L’utente ha inserito l’indirizzo email "mail@pagopa.it" in entrambi i campi della maschera
  Quando L’utente clicca sul tasto "Continua"
  Allora L’utente viene reindirizzato sulla pagina "/scegli-metodo"

#======================================================
#======================================================

@CheckoutBackNavigation_005_05
@runnable
@happy_path
Scenario: Navigazione - Scelta metodo di pagamento “Carte di Credito”
  Dato L’utente si trova sulla pagina "/scegli-metodo"
  Quando L’utente clicca sul tasto "Carte di Credito"
  Allora L’utente viene reindirizzato sulla pagina "/inserisci-carta"
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_06
@runnable
@happy_path
Schema dello scenario: Click sul tasto indietro riporta alla pagina precedente del flusso
  Dato L’utente si trova sulla pagina "<pagina_corrente>"
  Quando L’utente clicca sul tasto "Indietro"
  Allora L’utente viene reindirizzato sulla pagina "<pagina_precedente>"
  
  Esempi:
   | pagina_corrente        | pagina_precedente      |
   | /inserisci-dati-avviso | /                      |
   | /dati-pagamento        | /inserisci-dati-avviso |
   | /inserisci-email       | /dati-pagamento        |
   | /scegli-metodo         | /inserisci-email       |
   | /inserisci-carta       | /scegli-metodo         |
   | /lista-psp             | /scegli-metodo         |
   
#======================================================
#======================================================

@CheckoutBackNavigation_005_07
@runnable
@happy_path
Scenario: Assenza loop di navigazione per indietro successivi da pagina Modifica metodo di pagamento
  Dato L’utente si trova sulla pagina "/riepilogo-pagamento"
  E L’utente ha cliccato sul tasto "Modifica metodo di pagamento"
  E L’utente si trova sulla pagina "/scegli-metodo"
  Quando L’utente clicca ripetutamente sul tasto "Indietro"
  Allora L’utente ritorna sulla HP dopo aver visitato una ed una sola volta, in ordine, le pagine "/inserisci-email", "/dati-pagamento", "/inserisci-dati-avviso", senza ripetizioni né ritorni a pagine già visitate
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_08
@runnable
@happy_path
Scenario: Indietro da inserisci dati avviso per flusso con accesso diretto (senza history)
  Dato L’utente naviga sulla pagina "/inserisci-dati-avviso" selezionata da bookmark o URL diretto
  Quando L’utente clicca sul tasto "Indietro"
  Allora L’utente ritorna sulla HP senza uscire dall’applicativo 
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_09
Scenario: Flusso lista PSP - indietro da /scegli-metodo (metodo APM)
  Dato L’utente ha raggiunto la pagina "/lista-psp" dall’entry point "/scegli-metodo" (metodo APM)
  Quando L’utente clicca sul tasto "Indietro"
  Allora L’utente viene reindirizzato sulla pagina "/scegli-metodo"
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_10
Scenario: Flusso lista PSP - indietro da /inserisci-carta (flusso carta con enablePspPage=true)
  Dato L’utente ha raggiunto la pagina "/lista-psp" dall’entry point "/inserisci-carta" (flusso carta con enablePspPage=true)
  Quando L’utente clicca sul tasto "Indietro"
  Allora L’utente viene reindirizzato sulla pagina "/scegli-metodo"
  
#======================================================
#======================================================

@CheckoutBackNavigation_005_11
Scenario: Flusso lista PSP - indietro da /scegli-metodo (wallet salvato con enablePspPage=true)
  Dato L’utente ha raggiunto la pagina "/lista-psp" dall’entry point "/scegli-metodo" (wallet salvato con enablePspPage=true)
  Quando L’utente clicca sul tasto "Indietro"
  Allora L’utente viene reindirizzato sulla pagina "/scegli-metodo"
