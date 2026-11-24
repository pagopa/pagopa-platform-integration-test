#9999999999
#language: it
@pos_002_integration_Flusso_di_pagamento
Funzionalità: Esecuzione del flusso di pagamento 

    Contesto:
        Dato che i sistemi sono operativi

    @runnable
    @pos_002_01 @integration
    Scenario: Creazione della posizione debitoria con IUV generato dal POS Gateway
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE" 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E la posizione debitoria risulta creata e con status "PAID" 
      
    @runnable
    @pos_002_02 @integration
    Scenario: Creazione della posizione debitoria con IUV fornito dall'Ente
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE_PROVIDED_IUV" e con uno IUV 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E la posizione debitoria risulta creata con lo IUV fornito e con status "PAID" 


    @runnable
    @pos_002_03 @integration
    Scenario: Attivazione del pagamento su una posizione debitoria esistente
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e fornisce un notice_number 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E lo stato della posizione debitoria è "PAID"

    
    @runnable
    @negative
    @pos_002_04 @integration
    Scenario: Creazione della posizione debitoria fallita per IUV non valido
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE_PROVIDED_IUV" e con uno IUV errato "111111"
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        E la posizione debitoria non è stata creata

    
    @runnable
    @negative
    @pos_002_05 @integration
    Scenario: Attivazione del pagamento fallita per notice_number non valido
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e notice_number errato 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        E lo stato della posizione debitoria è "UNPAID"