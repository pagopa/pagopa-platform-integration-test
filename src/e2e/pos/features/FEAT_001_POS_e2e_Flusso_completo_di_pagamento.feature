#language: it
@pos_001_e2e_Flusso_di_pagamento
Funzionalità: Esecuzione del flusso di pagamento 

    Contesto:
        Dato che i sistemi sono operativi

    
    @runnable
    @pos_001_01 @e2e
    Scenario: Esecuzione completa del flusso di pagamento con type TO_CREATE e init completo
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE"
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E la posizione debitoria risulta creata e con status "PAID" 
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "SUCCESS"


    @runnable
    @pos_001_02 @e2e
    Scenario: Esecuzione completa del flusso di pagamento con type TO_CREATE_PROVIDED_IUV e con uno IUV e init completo
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE_PROVIDED_IUV" e con uno IUV
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E la posizione debitoria risulta creata con lo IUV fornito e con status "PAID" 
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "SUCCESS"


    @runnable
    @pos_001_03 @e2e
    Scenario: Esecuzione completa del flusso di pagamento con type CI_PROVIDED e fornisce un notice_number e init completo
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e fornisce un notice_number
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E lo stato della posizione debitoria è "PAID"
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "SUCCESS"

    @runnable
    @pos_001_04 @e2e
    Scenario: Esecuzione completa del flusso di pagamento con type TO_CREATE e init parziale
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di lista POS
        Allora il Gestionale Interface ritorna la lista POS
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE" 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E la posizione debitoria risulta creata e con status "PAID" 
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "SUCCESS"


    @runnable
    @pos_001_05 @e2e
    Scenario: Esecuzione completa del flusso di pagamento con type TO_CREATE_PROVIDED_IUV e con uno IUV e init parziale
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di lista POS
        Allora il Gestionale Interface ritorna la lista POS
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE_PROVIDED_IUV" e con uno IUV
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E la posizione debitoria risulta creata con lo IUV fornito e con status "PAID" 
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "SUCCESS"


    @runnable
    @pos_001_06 @e2e
    Scenario: Esecuzione completa del flusso di pagamento con type CI_PROVIDED e fornisce un notice_number e init parziale
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di lista POS
        Allora il Gestionale Interface ritorna la lista POS
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e fornisce un notice_number
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "200"
        E lo stato della posizione debitoria è "PAID"
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "SUCCESS"
