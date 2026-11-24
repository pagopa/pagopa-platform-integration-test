#language: it
@pos_001_integration_Ottenimento_lista_POS
Funzionalità: Ottenimento di una lista di POS attivi per un PSP

    Contesto:
        Dato che i sistemi sono operativi

    @runnable
    @pos_001_01
    @integration
    @positive
    Scenario: Inizializzazione flusso e ottenimento sessionId
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "false"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId

    @runnable
    @pos_001_02 
    @integration
    @positive
    Scenario: Inizializzazione flusso e ottenimento sessionId e lista POS
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
         

    @runnable
    @pos_001_03
    @integration
    @negative
    Scenario: Inizializzazione flusso fallita con oggetto non valido
        Quando il Gestionale EC invia la chiamata di init con un oggetto non valido
        Allora il Gestionale Interface ritorna uno status "400"

    @runnable
    @pos_001_04
    @integration
    @negative
    Scenario: Inizializzazione flusso fallita con correlationId errato
        Quando il Gestionale EC invia la chiamata di init con con correlationId "11111"
        Allora il Gestionale Interface ritorna uno status "400"
        

    @runnable
    @pos_001_05
    @integration
    @positive
    Scenario: Ottentimento di una lista di POS attivi per un PSP
        Quando il Gestionale EC invia la chiamata per la lista POS
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS

    @runnable
    @pos_001_06
    @integration
    @negative
    Scenario: Ottentimento di una lista di POS attivi con correlationId errato
        Quando il Gestionale EC invia la chiamata per la lista POS con correlationId "11111"
        Allora il Gestionale Interface ritorna uno status "400"

    @runnable
    @pos_001_07 
    @integration
    @negative
    Scenario: Ottentimento di una lista di POS attivi con oggetto non valido
        Quando il Gestionale EC invia la chiamata per la lista POS con un oggetto non valido
        Allora il Gestionale Interface ritorna uno status "400"
