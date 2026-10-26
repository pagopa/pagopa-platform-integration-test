#0123456789
# language: it

@FEAT_003_Checkout_Back_Navigation_001
Funzionalità: Controllo della navigazione all'indietro nel flusso di Checkout

  Contesto:
    Dato che la pagina di checkout è aperta
    E la lingua impostata è l'italiano

  # D-001, D-002: codice avviso e CF Ente Creditore risolti con valore concreto (D-001 generato secondo il pattern 302YYXXXXXXXXXXXXX autorizzato dall'umano; D-002 fornito dalla fonte); disponibilita'/recuperabilita' in ambiente live NON verificata (righe dati-pagamento, inserisci-email, inserisci-carta, lista-psp -> inserisci-carta, lista-psp -> scegli-metodo)
  # D-003, D-004: indirizzo email risolto con il valore di esempio fornito dalla fonte ammessa, sintatticamente valido; nessuno stato di entità aggiuntivo richiesto (righe inserisci-carta, lista-psp -> inserisci-carta, lista-psp -> scegli-metodo)
  # Dati irrisolti: D-005, D-006, D-007, D-008 (riga lista-psp -> inserisci-carta); scenario non pronto all'esecuzione per questa riga
  @regression
  @checkout
  @positive
  @FEAT_003_Checkout_Back_Navigation_001_01
  Schema dello scenario: L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro
    Dato che <contesto>
    Quando l'utente accede alla pagina "<pagina_iniziale>"
    E l'utente preme una sola volta il pulsante "Indietro"
    Allora l'utente si trova nella pagina "<pagina_precedente>"

    Esempi:
      | pagina_iniziale        | pagina_precedente     | contesto                                                                                                                                                                                                  |
      | inserisci-dati-avviso  | home                  | l'utente si trova sulla home page del checkout                                                                                                                                                           |
      | dati-pagamento         | inserisci-dati-avviso | un avviso di pagamento valido ("302124502198375901", "77777777777") è stato inserito nella pagina di inserimento dati avviso, pronto per proseguire                                                     |
      | inserisci-email        | dati-pagamento        | un avviso di pagamento valido ("302124502198375901", "77777777777") è stato confermato fino alla pagina di riepilogo dati pagamento, pronta per proseguire                                               |
      | inserisci-carta        | scegli-metodo         | un avviso di pagamento valido ("302124502198375901", "77777777777") e un indirizzo email valido ("email@email.it", "email@email.it") sono stati confermati, con "Carta di Credito" selezionabile        |
      | lista-psp              | inserisci-carta       | un avviso di pagamento valido ("302124502198375901", "77777777777"), un indirizzo email valido ("email@email.it", "email@email.it") e dati carta validi ("__TODO_D005__", "__TODO_D006__", "__TODO_D007__", "__TODO_D008__") sono stati confermati fino alla pagina di inserimento dati carta |
      | lista-psp              | scegli-metodo         | un avviso di pagamento valido ("302124502198375901", "77777777777") e un indirizzo email valido ("email@email.it", "email@email.it") sono stati confermati, con il metodo "PayPal" selezionato (campione rappresentante; Apple Pay, BANCOMAT Pay e MyBank dichiarati equivalenti dalla fonte, non campionati singolarmente) |
