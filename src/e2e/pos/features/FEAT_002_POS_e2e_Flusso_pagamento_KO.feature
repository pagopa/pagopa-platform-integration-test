#language: it
@pos_002_e2e_Flusso_pagamento_KO
Funzionalità: Fallimento del flusso di pagamento

    Contesto:
        Dato che i sistemi sono operativi

    
    @runnable
    @pos_002_01 @e2e @negative
    Scenario: Esecuzione fallita del flusso di pagamento con type TO_CREATE_PROVIDED_IUV, iuv errato e init completo
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE_PROVIDED_IUV" e con uno IUV errato "11111" 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        E la posizione debitoria non è stata creata
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "ERROR"

    
    @runnable
    @pos_002_02 @e2e @negative
    Scenario: Esecuzione fallita del flusso di pagamento con type CI_PROVIDED, notice_number errato e init completo
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e notice_number errato  
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        E lo stato della posizione debitoria è "UNPAID"
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "ERROR"

    @runnable
    @pos_002_04 @e2e @negative
    Scenario: Esecuzione fallita del flusso di pagamento con type CI_PROVIDED, notice_number non esistente e init completo
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna la lista POS
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e notice_number non esistente  
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "ERROR"

    
    @runnable
    @pos_002_05 @e2e @negative
    Scenario: Esecuzione fallita del flusso di pagamento con type TO_CREATE_PROVIDED_IUV, iuv errato e init parziale
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di lista POS
        Allora il Gestionale Interface ritorna la lista POS
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "TO_CREATE_PROVIDED_IUV" e con uno IUV errato "11111" 
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        E la posizione debitoria non è stata creata
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "ERROR"

    @runnable
    @pos_002_06 @e2e @negative
    Scenario: Esecuzione fallita del flusso di pagamento con type CI_PROVIDED, notice_number errato e init parziale
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di lista POS
        Allora il Gestionale Interface ritorna la lista POS
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e notice_number errato  
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        E lo stato della posizione debitoria è "UNPAID"
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "ERROR"


    @runnable
    @pos_002_08 @e2e @negative
    Scenario: Esecuzione fallita del flusso di pagamento con type CI_PROVIDED, notice_number non esistente e init parziale
        Quando il Gestionale EC invia la chiamata di init con includeTerminals "true"
        Allora il Gestionale Interface ritorna uno status "200"
        E il Gestionale Interface ritorna un sessionId
        Quando il Gestionale EC invia la richiesta di lista POS
        Allora il Gestionale Interface ritorna la lista POS
        Quando il Gestionale EC invia la richiesta di avvio del flusso di pagamento con type "CI_PROVIDED" e notice_number non esistente
        Allora il Gestionale EC ottiene l'esito dell'operazione di pagamento con status "400"
        Quando il Gestionale EC invia la richiesta di recupero stato transazione al Gestionale Interface
        Allora il Gestionale EC ottiene lo stato transazione 
        E lo stato transazione è "ERROR"

    

    