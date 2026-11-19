#0123456789
# language: it
@fdrhybrid_001_Pubblicazione_FDR3_Recupero_FDR1
Funzionalità: Pubblicazione di un flusso con la modalità nuova e recupero con la modalità legacy

  Contesto:
    Dato che il PSP e l'EC sono censiti e abilitati ad operare con le modalità nuova e legacy
    E che le credenziali del PSP e dell'EC sono valide per le rispettive modalità
    E che la coppia PSP-EC è gestita dal sistema dei flussi di rendicontazione
    E che i servizi di rendicontazione e di conversione sono operativi
    E che l'identificativo del flusso non è mai stato usato ed è valido per entrambe le modalità

  @fdrhybrid_001_01 @positive
  Schema dello scenario: Il PSP pubblica un flusso con la modalità nuova e l'EC lo recupera con la modalità legacy
    Dato che il flusso contiene <numero_pagamenti> pagamenti con importi <importi>, esiti <esiti> e indici di trasferimento <indici_trasferimento>
    Quando il PSP crea il flusso con la modalità nuova
    Allora la piattaforma crea il flusso in bozza
    Quando il PSP aggiunge i pagamenti al flusso
    Allora la piattaforma aggiunge i pagamenti alla bozza
    Quando il PSP pubblica il flusso
    Allora la piattaforma conferma la pubblicazione
    E il flusso risulta pubblicato alla prima revisione, con totali calcolati uguali a quelli dichiarati
    Quando l'EC consulta con la modalità legacy l'elenco dei flussi del PSP
    Allora l'elenco contiene il flusso entro il tempo massimo previsto dalla conferma della pubblicazione
    E la voce del flusso riporta identificativo e data e ora uguali a quelli pubblicati
    Quando l'EC richiede con la modalità legacy il flusso individuato
    Allora l'EC riceve il flusso completo
    E il documento ricevuto è valido rispetto allo schema della modalità legacy
    E l'identificativo del flusso ricevuto è uguale a quello pubblicato
    E la data e ora del flusso e il giorno di regolamento sono uguali a quelli pubblicati, senza spostamento del giorno di calendario
    E il numero e l'importo totale dei pagamenti dichiarati sono uguali a quelli pubblicati e a quelli ricostruiti dai pagamenti ricevuti
    E i pagamenti ricevuti sono tutti e soli quelli pubblicati, senza mancanti né duplicati
    E per ogni pagamento importo, esito, indice di trasferimento e giorno dell'esito sono uguali a quelli pubblicati

    Esempi:
      | numero_pagamenti | importi                           | esiti                                                                                          | indici_trasferimento |
      | 3                | 100.00, 100.00, 100.00            | eseguito, eseguito, eseguito                                                                   | 1, 1, 1              |
      | 4                | 100.00, 100.00, 100.00, 100.00    | eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT | 1, 1, 1, 1           |
      | 3                | 100.00, 100.00, 100.00            | eseguito, eseguito, eseguito                                                                   | 1, 3, 5              |
      | 1                | 100.00                            | eseguito                                                                                       | 1                    |
      | 5                | 100.00, 100.00, 100.00, 100.00, 100.00 | eseguito, eseguito, eseguito, eseguito, eseguito                                          | 1, 1, 1, 1, 1        |
      | 4                | 0.01, 10.00, 1234.56, 999999.99   | eseguito, eseguito, eseguito, eseguito                                                         | 1, 1, 1, 1           |
