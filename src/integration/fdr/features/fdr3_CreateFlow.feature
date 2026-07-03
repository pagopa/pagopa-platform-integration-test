# 3066232912
# language: it
@Fdr3_001
Funzionalità: Creazione di un nuovo flusso di rendicontazione

  Contesto:
    Dati i sistemi sono operativi

# ===============================================================================================
# ===============================================================================================

  @runnable
  @positive
  @Fdr3_001_01
  Scenario: Creazione di un nuovo flusso di rendicontazione
    Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    E un nuovo id flusso di rendicontazione pari a "2025-06-30ABI50004-1178"
    Quando il PSP invia una richiesta di creazione flusso tramite la POST "/psps/ABI50004/fdrs/2025-06-30ABI50004-1178" con un body valido
    Allora il sistema risponde con il codice di stato HTTP 201
    E il nuovo flusso viene creato con id "2025-06-30ABI50004-1178"
    E il flusso è in stato "CREATED"
    E il campo "revision" è pari a 1
    E il campo "last_update_date" è aggiornato all'ora corrente
    E il campo "creation_date" è aggiornato all'ora corrente
    E il blob object corrispondente viene salvato correttamente a sistema

# ===============================================================================================
# ===============================================================================================

  @runnable 
  @negative
  @Fdr3_001_02
  Schema dello scenario: L’identificativo del flusso di rendicontazione creato dal PSP non rispetta il formato standard
    Dato il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    Quando il PSP invia una richiesta di creazione flusso tramite la POST "/psps/ABI50004/fdrs/<data regolamento><istituto mittente>-<flusso>" con un body valido
    Allora il sistema risponde con il codice di stato HTTP 400
    E il flusso di rendicontazione non viene creato a sistema

    Esempi:
      | data regolamento | istituto mittente | flusso |
      | 30-06-2025       | ABI50004          | 1178   |
      | 2025-06-30       | ABI5000           | 1178  |
      | 2025-06-30       | ABI50004          | 11%8   |


# ===============================================================================================
# ===============================================================================================    

  @runnable 
  @negative
  @Fdr3_001_03
  Scenario: Tentativo di creazione di un nuovo flusso da parte di un PSP non abilitato (not ENABLED)
    Dato il PSP "PSPDEMO2" con pspId "ABIDEMO2" è censito a sistema
    E il PSP "PSPDEMO2" non è in stato "ENABLED"
    Quando il PSP invia una richiesta di creazione flusso tramite la POST "/psps/ABIDEMO2/fdrs/2025-06-30ABIDEMO2-1178" con un body valido
    Allora il sistema risponde con il codice di stato HTTP 400
    E il flusso di rendicontazione non viene creato a sistema

# ===============================================================================================
# ===============================================================================================

  @runnable 
  @negative
  @Fdr3_001_04
  Scenario: Tentativo di creazione di un nuovo flusso da parte di un PSP non censito
    Dato il PSP "PSPDEMO3" con pspId "ABIDEMO3" non è censito a sistema
    Quando il PSP invia una richiesta di creazione flusso tramite la POST "/psps/ABIDEMO3/fdrs/2025-06-30ABIDEMO3-1178" con un body valido
    Allora il sistema risponde con il codice di stato HTTP 400
    E il flusso di rendicontazione non viene creato a sistema

# ===============================================================================================
# ===============================================================================================

  @runnable 
  @positive 
  @Fdr3_001_05
  Scenario: Creazione di un flusso con ID già esistente in stato PUBLISHED 
    Dato il PSP "PSPDEMO" con pspId "ABI50004" correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-1178" esiste già in stato "PUBLISHED"
    Quando il PSP invia una richiesta di creazione flusso tramite la POST "/psps/ABI50004/fdrs/2025-06-30ABI50004-1178" con un body valido
    Allora il sistema risponde con il codice di stato HTTP 201
    E il flusso viene creato in stato "CREATED"
    E il campo "revision" è incrementato di 1 rispetto alla revisione esistente
    E il campo "last_update_date" è aggiornato all'ora corrente
    E il campo "creation_date" è aggiornato all'ora corrente
    E il nuovo blob object corrispondente viene salvato correttamente a sistema

# ===============================================================================================
# ===============================================================================================

  @runnable 
  @negative
  @Fdr3_001_06
  Schema dello scenario: Tentativo di creazione di un flusso con ID già esistente in uno stato non ammesso
    Dato il PSP "PSPDEMO" con pspId "ABI50004" correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-1178" esiste già in stato "<stato_esistente>"
    Quando il PSP invia una richiesta di creazione flusso tramite la POST "/psps/ABI50004/fdrs/2025-06-30ABI50004-1178" con un body valido
    Allora il sistema risponde con il codice di stato HTTP 400
    E il flusso di rendicontazione esistente non viene modificato a sistema

    Esempi:
      | stato_esistente |
      | CREATED         |
      | INSERTED        |



      






