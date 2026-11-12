#0123456789
# language: it
@FEAT_002_Checkout_Errori_Avviso_001
Funzionalità: Segnalazione degli errori durante la verifica dell'avviso

  Contesto:
    Dato che l'utente si trova nella homepage "https://uat.checkout.pagopa.it/"
    E la lingua del Checkout è impostata su "it"

  # Tutte le righe: D-002, D-007, D-008 e associazione mock/errore non verificati nell'ambiente; scenario non pronto all'esecuzione
  @regression
  @checkout
  @negative
  @FEAT_002_Checkout_Errori_Avviso_001_01
  Schema dello scenario: Visualizzazione del messaggio per avviso sconosciuto, scaduto o timeout
    Dato che il mock degli avvisi è configurato per i casi di errore documentati
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "<avviso>" e il CF ente creditore "77777777777"
    E l'utente preme "Continua" nella pagina di inserimento dati avviso
    Allora il Checkout mostra il messaggio di errore entro <tempo_massimo> secondi dal clic su "Continua"
    E il messaggio di errore ha il titolo "<titolo>"
    E il messaggio di errore ha la descrizione "<descrizione>"

    Esempi:
      | avviso             | tempo_massimo | titolo                                              | descrizione                                                                                                  |
      | 302400000000000000 | 5             | Non riusciamo a trovare l’avviso                      | L'avviso potrebbe essere stato già pagato. Per ricevere assistenza, contatta l’Ente Creditore.                   |
      | 302990000000000000 | 60            | L’avviso è scaduto e non è più possibile pagarlo       | Contatta l’Ente per maggiori informazioni.                                                                    |
      | 302980000000000000 | 60            | Si è verificato un errore imprevisto                  | Riprova, oppure contatta l’assistenza                                                                         |

  # D-002, D-007, D-008 e associazione mock/duplicato non verificati nell'ambiente; scenario non pronto all'esecuzione
  @regression
  @checkout
  @negative
  @FEAT_002_Checkout_Errori_Avviso_001_02
  Scenario: Visualizzazione del messaggio per avviso già pagato senza descrizione aggiuntiva
    Dato che il mock degli avvisi è configurato per il caso di pagamento duplicato
    Quando l'utente sceglie l'inserimento manuale dei dati dell'avviso
    E l'utente inserisce il codice avviso "302950100443009424" e il CF ente creditore "77777777777"
    E l'utente preme "Continua" nella pagina di inserimento dati avviso
    Allora il Checkout mostra il messaggio di errore entro 5 secondi dal clic su "Continua"
    E il messaggio di errore ha il titolo "Questo avviso è stato già pagato!"
    E il messaggio di errore non presenta una descrizione aggiuntiva
