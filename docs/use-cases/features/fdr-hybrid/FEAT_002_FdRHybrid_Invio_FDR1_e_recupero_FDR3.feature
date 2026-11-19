#0123456789
# language: it
@fdrhybrid_002_Invio_FDR1_Recupero_FDR3
Funzionalità: Invio di un flusso con la modalità legacy e recupero con la modalità nuova

  Contesto:
    Dato che il PSP e l'EC sono censiti e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione
    E che il PSP e l'EC dispongono delle credenziali e delle abilitazioni previste per le due modalità
    E che la coppia PSP-EC è gestita dal sistema dei flussi di rendicontazione
    E che le modalità legacy e nuova e la conversione dalla legacy alla nuova sono operative
    E che il PSP e l'EC sono noti anche alla modalità nuova
    E che l'identificativo del flusso non è mai stato usato dal PSP ed è valido per entrambe le modalità

  @fdrhybrid_002_01 @positive
  Schema dello scenario: Il PSP invia un flusso con la modalità legacy e l'EC lo recupera con la modalità nuova
    Dato che il flusso contiene <numero_pagamenti> pagamenti con importi <importi>, esiti <esiti> e indici di trasferimento <indici_trasferimento>
    Quando il PSP invia il flusso con la modalità legacy
    Allora la piattaforma convalida l'invio, conserva il flusso e risponde con esito positivo
    Quando l'EC consulta con la modalità nuova l'elenco dei flussi pubblicati del PSP
    Allora l'elenco contiene il flusso associato al PSP mittente entro il tempo massimo previsto dalla conferma dell'invio
    E la voce del flusso riporta la revisione prevista
    Quando l'EC richiede il dettaglio del flusso individuato
    Allora l'EC riceve il dettaglio del flusso pubblicato
    E l'identificativo del flusso recuperato è uguale a quello inviato
    E la data e ora del flusso e il giorno di regolamento sono uguali a quelli inviati, senza spostamento del giorno di calendario
    Quando l'EC richiede i pagamenti del flusso
    Allora l'EC ottiene tutti i pagamenti del flusso
    E il numero e l'importo totale dichiarati sono uguali a quelli inviati e a quelli ricostruiti dai pagamenti recuperati
    E i pagamenti recuperati sono tutti e soli quelli inviati, senza mancanti, duplicati o aggiunti
    E per ogni pagamento importo, esito, indice di trasferimento e giorno dell'esito sono uguali a quelli inviati

    Esempi:
      | numero_pagamenti | importi                                | esiti                                                                                              | indici_trasferimento |
      | 3                | 100.00, 100.00, 100.00                 | eseguito, eseguito, eseguito                                                                       | 1, 1, 1              |
      | 4                | 100.00, 100.00, 100.00, 100.00         | eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT | 1, 1, 1, 1           |
      | 3                | 100.00, 100.00, 100.00                 | eseguito, eseguito, eseguito                                                                       | 1, 3, 5              |
      | 1                | 100.00                                 | eseguito                                                                                           | 1                    |
      | 5                | 100.00, 100.00, 100.00, 100.00, 100.00 | eseguito, eseguito, eseguito, eseguito, eseguito                                                   | 1, 1, 1, 1, 1        |
      | 4                | 0.01, 10.00, 1234.56, 999999.99        | eseguito, eseguito, eseguito, eseguito                                                             | 1, 1, 1, 1           |
