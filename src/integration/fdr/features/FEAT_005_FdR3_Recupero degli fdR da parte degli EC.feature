#3087794199
#language: it

Funzionalità: Recupero defli FdR da parte degli Enti Creditori

  Contesto:
    Dati i sistemi sono operativi

#======================================================
#======================================================

@runnable 
@positive
@FdR3_005_01
Scenario: Recupero con successo di tutti i flussi di rendicontazione in stato PUBLISHED per un Ente Creditore
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema 
    E che esistono flussi di rendicontazione associati all'EC in stato "PUBLISHED"
    Quando l'EC invia una richiesta di recupero dei flussi tramite la api "Get all published flow related to creditor institution"
    Allora il sistema risponde con il codice di stato HTTP 200
    E il sistema restituisce la lista di tutti i flussi di rendicontazione associati all'EC che si trovano in stato "PUBLISHED"

# ===============================================================================================
# ===============================================================================================


@runnable
@positive
@FdR3_005_002
Scenario: Recupero con successo di uno specifico flusso di rendicontazione per un Ente Creditore e un PSP
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema
    E il PSP con pspId "99999000011" correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-1178" con revisione 1 esiste ed è in stato "PUBLISHED"
    Quando l'EC invia una richiesta di recupero del flusso tramite la api "Get single published flow related to creditor institution, searching by name and revision"
    Allora il sistema risponde con il codice di stato HTTP 200
    E il sistema restituisce i dettagli del flusso di rendicontazione richiesto

# ===============================================================================================
# ===============================================================================================

@runnable 
@negative
@FdR3_005_03
Scenario: Tentativo di recupero di uno specifico flusso non in stato PUBLISHED da parte di un EC
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema
    E il PSP "PSP DEMO" con pspId "ABI50004" correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-1178" con revisione 1 esiste ma NON è in stato "PUBLISHED"
    Quando l'EC invia una richiesta di recupero del flusso tramite la api "Get single published flow related to creditor institution, searching by name and revision"
    Allora il sistema risponde con il codice di stato HTTP 404
    E il flusso di rendicontazione non viene restituito all'EC

# ===============================================================================================
# ===============================================================================================


@runnable 
@negative
@FdR3_005_04
  Scenario: Tentativo di recupero di uno specifico flusso non esistente a sistema da parte di un EC
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema
    E il PSP "PSP DEMO" con pspId "ABI50004"  correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-117" con revisione 1 NON esiste a sistema
    Quando l'EC invia una richiesta di recupero del flusso tramite la api "Get single published flow related to creditor institution, searching by name and revision"
    Allora il sistema risponde con il codice di stato HTTP 404
    E il flusso di rendicontazione non viene restituito all'EC

# ===============================================================================================
# ===============================================================================================

@runnable
@positive
@FdR3_005_05
Scenario: Recupero con successo dei pagamenti di uno specifico flusso in stato PUBLISHED da parte di un EC
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema
    E il PSP "PSP DEMO" con pspId "ABI50004"  correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-1178" con revisione 1 esiste ed è in stato "PUBLISHED"
    Quando l'EC invia una richiesta di recupero dei pagamenti tramite la api "Get all payments of single published flow related to creditor institution, searching by name and revision"
    Allora il sistema risponde con il codice di stato HTTP 200
    E il sistema restituisce la lista dei pagamenti associati al flusso di rendicontazione richiesto

# ===============================================================================================
# ===============================================================================================

@runnable 
@negative
@FdR3_005_06
Scenario: Tentativo di recupero dei pagamenti di uno specifico flusso non in stato PUBLISHED da parte di un EC
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema
    E il PSP "PSP DEMO" con pspId "ABI50004"  correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-1178" con revisione 1 esiste ma NON è in stato "PUBLISHED"
    Quando l'EC invia una richiesta di recupero dei pagamenti tramite la api "Get all payments of single published flow related to creditor institution, searching by name and revision"
    Allora il sistema risponde con il codice di stato HTTP 404
    E la lista dei pagamenti associati al flusso di rendicontazione non viene restituita all'EC

# ===============================================================================================
# ===============================================================================================

@runnable 
@negative
@FdR3_005_07
Scenario: Tentativo di recupero dei pagamenti di uno specifico flusso non esistente da parte di un EC
    Dato l'EC "VOLTA" con organizationId "80126590159" correttamente censito a sistema
    E il PSP "PSP DEMO" con pspId "ABI50004"  correttamente censito a sistema
    E che il flusso di rendicontazione "2025-06-30ABI50004-117" con revisione 1 NON esiste a sistema
    Quando l'EC invia una richiesta di recupero dei pagamenti tramite la api "Get all payments of single published flow related to creditor institution, searching by name and revision"
    Allora il sistema risponde con il codice di stato HTTP 404
    E la lista dei pagamenti non viene restituita all'EC