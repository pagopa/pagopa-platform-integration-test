# Mappa dei riferimenti degli UC FDR (v3)

| Campo | Valore |
| --- | --- |
| Jira | PQ-827 |
| Branch | `PQ-827-fdr-e2e-test-design` |
| Stato | bozza di lavoro, accompagna gli UC v3 dopo la revisione degli AC del 18/11/2026 |
| Data | 18/11/2026 |
| UC | [UC-FDR-001-v3](UC-FDR-001-v3.md) e [UC-FDR-002-v3](UC-FDR-002-v3.md) |
| Documenti | [razionale funzionale v3](../fdr-e2e-ibrido-01-razionale-uc-v3.md) e [dati tecnici v3](../fdr-e2e-ibrido-02-dati-tecnici-v3.md) |

## Premesse

Gli UC v3 descrivono il comportamento: chi fa che cosa e che cosa deve risultare. Non portano sigle, fonti, collegamenti né dettagli tecnici. Questo file collega ogni voce degli UC ai documenti che ne portano regole, dati e passi tecnici, così che un dettaglio sia scritto in un posto solo.

Nelle tabelle "razionale" indica il documento funzionale e "tecnico" quello dei dati tecnici, entrambi nella versione 3; il simbolo § rinvia alle loro sezioni. Le sigle (R, D, PRE, FP, EF, PO, AC, VG, VAR, QF, DM, RI) sono quelle dei due documenti. Ogni UC conserva la numerazione dei suoi passi, precondizioni e postcondizioni e le righe seguono quell'ordine. Gli AC sono stati ridotti e rinumerati il 18/11/2026: la colonna "Era" riporta il numero precedente, e i criteri ritirati con i loro motivi sono nel razionale §6.2. Gli UC non hanno flussi alternativi, che sono fuori perimetro (razionale D-02), né flussi di eccezione, perché la mancata propagazione non si può provocare né osservare come eccezione (razionale D-10, §6.4).

Criterio di sintesi. Negli UC restano attori, azioni ed esiti attesi. Ne sono usciti i dati da fornire, i campi confrontati, le API, i formati e i parametri di attesa e di confronto. Dove un criterio resta generico, per esempio "stesso contenuto", la definizione operativa sta nella riga dei documenti indicata qui.

La colonna "Da chiarire" elenca ciò che non è ancora noto e tocca la voce; il quadro completo è nella sezione 3.

## 1. UC-FDR-001: pubblicazione FDR3 e recupero FDR1

Corrisponde a UC-A del razionale: il PSP scrive con la modalità nuova e l'EC legge con la legacy.

### 1.1 Precondizioni

| # | Voce | Razionale | Dettaglio | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | PSP ed EC censiti e abilitati | PRE-C1, R-17 | tecnico §2.3, RI-15 | DM-02 |
| 2 | credenziali e abilitazioni per le due modalità | PRE-C2, R-18 | tecnico §2.4 | DM-03 |
| 3 | coppia gestita da FDR, non da un gestore esterno | PRE-C3, R-16 | tecnico §2.3, RI-15 | DM-02 |
| 4 | identificativo mai usato dal PSP | PRE-C4, R-04, R-12 | tecnico §8.1 | — |
| 5 | servizi e conversione operativi | PRE-C5, R-01 | tecnico §8.6, RI-15 | DM-14 |
| 6 | flusso valido per entrambe le modalità | PRE-C6, R-07 … R-13 | tecnico §8.2, §8.3, §8.5 | — |

### 1.2 Flusso principale

| Passo | Razionale | Dati e regole | Implementazione | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | FP-A1, R-04, R-12 | razionale FP-A1; tecnico §3.4, §8.1, §8.2 | tecnico §3.1 (creazione), §10.1; guardia VG-A1 (§7.2) | DM-13 |
| 2 | FP-A2, R-17 | — | nessun oracolo proprio: si osserva dall'esito del passo 1 (tecnico §7.2, VG-A1) | — |
| 3 | FP-A3, R-05 | razionale FP-A3; tecnico §3.4, §6.2, §8.3 | tecnico §3.1 (aggiunta), RI-05, RI-20; guardia VG-A1 (§7.2) | DM-13 |
| 4 | FP-A4 | — | nessun oracolo proprio: si osserva dall'esito del passo 3 (tecnico §7.2, VG-A1) | — |
| 5 | FP-A5 | — | tecnico §3.1 (pubblicazione, senza corpo); guardia VG-A1 (§7.2) | DM-13 |
| 6 | FP-A6, R-06 | — | tecnico §3.1 (esiti e lettura lato PSP), §7.2 (VG-A1, VG-A2) | — |
| 7 | FP-A7, R-14 | — | tecnico §9 | QF-03 |
| 8 | FP-A8, R-19 | — | tecnico §4.2 (elenco), §4.3, §2.2, §2.4, §9.3 | DM-01, DM-03, DM-04, DM-05 |
| 9 | FP-A9 | — | tecnico §4.2 (richiesta del flusso), §4.3, §4.4, §5 | DM-16 |

### 1.3 Eccezioni

Nessuna. La mancata propagazione, che nelle versioni precedenti era EF-C1, non è riproducibile né osservabile come eccezione: nel razionale è ritirata (§6.4, D-10) e negli UC trova riscontro solo come fallimento di AC-06.

### 1.4 Postcondizioni

| # | Voce | Razionale | Dettaglio | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | pubblicato alla prima revisione, totali coerenti | PO-A1, R-04 | tecnico §7.2 (VG-A2) | — |
| 2 | disponibile all'EC nella modalità legacy, completo ed equivalente | PO-A2 (AC-C1, AC-C3, AC-C5 … AC-C7, AC-A3, AC-A4) | tecnico §7.1 | QF-06 |
| 3 | non più modificabile né cancellabile | PO-A3, R-04 | tecnico RI-09 | — |

### 1.5 Acceptance Criteria

| AC | Era | Razionale | Regola di confronto | Da chiarire |
| --- | --- | --- | --- | --- |
| AC-01 | AC-01 | AC-C1, R-12 | tecnico §7.1 (AC-C1): uguaglianza esatta dell'identificativo nel contenuto XML | — |
| AC-02 | AC-03 | AC-C3, R-11 | tecnico §7.1 (AC-C3), §6.4 | QF-06 |
| AC-03 | AC-05 | AC-C5, R-06, R-10 | tecnico §7.1 (AC-C5), RI-05 | — |
| AC-04 | AC-06 | AC-C6, R-07, D-05 | tecnico §7.1 (AC-C6): coppie IUV e IUR, senza ordine | — |
| AC-05 | AC-07 | AC-C7, R-08, R-10, R-11 | razionale §6.2 (AC-C7) per gli attributi; tecnico §7.1 (AC-C7) | QF-06 |
| AC-06 | AC-09 | AC-C9, R-14, R-20 | tecnico §7.1 (AC-C9), §9.2 | QF-03 |
| AC-07 | AC-13 | AC-A3 | tecnico §4.2 (voce dell'elenco), §7.1 (AC-A3) | QF-06 |
| AC-08 | AC-14 | AC-A4, D-09 | tecnico §7.1 (AC-A4), §4.4: validazione contro `FlussoRiversamento_1_0_5.xsd` | DM-16 |

Tolti dalla revisione del 18/11/2026: AC-02 (mittente e destinatario), AC-04 (regolamento), AC-08 (completezza) e AC-10 (unicità); AC-11 e AC-12 sono diventati le guardie VG-A1 e VG-A2 (tecnico §7.2). I motivi sono nel razionale §6.2.

AC-06: il requisito "meno di dieci secondi" riguarda la singola richiesta e non la propagazione (razionale R-20). Il tempo massimo del test non coincide con il tempo entro cui la piattaforma ritenta o segnala l'anomalia: le fonti ne danno solo stime (tecnico §9.2) e non documentano un limite (razionale R-14). Il mancato arrivo entro T è il fallimento di questo criterio e non un'eccezione (razionale §6.4).

## 2. UC-FDR-002: invio FDR1 e recupero FDR3

Corrisponde a UC-B del razionale: il PSP scrive con la modalità legacy e l'EC legge con la nuova.

### 2.1 Precondizioni

| # | Voce | Razionale | Dettaglio | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | PSP ed EC censiti e abilitati | PRE-C1, R-17 | tecnico §2.3, RI-15 | DM-02 |
| 2 | credenziali e abilitazioni per le due modalità | PRE-C2, R-18 | tecnico §2.4 | DM-03 |
| 3 | coppia gestita da FDR, non da un gestore esterno | PRE-C3, R-16 | tecnico §2.3, RI-15 | DM-02 |
| 4 | identificativo mai usato dal PSP | PRE-C4, R-04, R-12 | tecnico §8.1 | — |
| 5 | servizi e conversione operativi | PRE-C5, R-01 | tecnico §8.6, RI-15 | DM-14 |
| 6 | flusso valido per entrambe le modalità | PRE-C6, R-07 … R-13 | tecnico §8.2, §8.3, §8.5 | — |
| 7 | PSP ed EC noti anche alla modalità nuova | PRE-B1, R-17 | razionale §8.2; tecnico RI-15 | DM-02 |

### 2.2 Flusso principale

| Passo | Razionale | Dati e regole | Implementazione | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | FP-B1 | razionale FP-B1; tecnico §5.3, §6, §8.2, §8.3 | tecnico §4.2 (invio), §4.3, §2.2, §2.4, §10.1, RI-01, RI-04, RI-11 | DM-01, DM-03, DM-11, DM-16 |
| 2 | FP-B2 | — | tecnico §4.2 (risposta di invio), §4.5; guardia VG-B1 (§7.2) | DM-04 |
| 3 | FP-B3, R-14 | — | tecnico §9 | QF-03, DM-14 |
| 4 | FP-B4, R-19 | — | tecnico §3.2 (elenco), §3.3, §9.3 | — |
| 5 | FP-B5 | — | tecnico §3.2 (dettaglio, azione da aggiungere), §10.2 | — |
| 6 | FP-B6 | — | tecnico §3.2 (pagamenti), §3.3 (paginazione), RI-13 | — |

### 2.3 Eccezioni

Nessuna, per lo stesso motivo di UC-FDR-001 (sezione 1.3).

### 2.4 Postcondizioni

| # | Voce | Razionale | Dettaglio | Da chiarire |
| --- | --- | --- | --- | --- |
| 1 | flusso conservato dalla piattaforma | PO-B1 | tecnico §7: nessun oracolo proprio, prova indiretta con la presenza nella modalità nuova | — |
| 2 | pubblicato nella modalità nuova, completo ed equivalente | PO-B2 (AC-C1, AC-C3, AC-C5 … AC-C7, AC-B2) | tecnico §7.1 | QF-06, QF-11 |
| 3 | non più modificabile né cancellabile | PO-B3, R-04 | tecnico RI-09 | — |

### 2.5 Acceptance Criteria

| AC | Era | Razionale | Regola di confronto | Da chiarire |
| --- | --- | --- | --- | --- |
| AC-01 | AC-01 | AC-C1, R-12 | tecnico §7.1 (AC-C1): uguaglianza esatta dell'identificativo nel dettaglio | — |
| AC-02 | AC-03 | AC-C3, R-11 | tecnico §7.1 (AC-C3), §6.4 | QF-06 |
| AC-03 | AC-05 | AC-C5, R-06, R-10 | tecnico §7.1 (AC-C5), RI-05 | — |
| AC-04 | AC-06 | AC-C6, R-07, D-05 | tecnico §7.1 (AC-C6): coppie IUV e IUR, senza ordine | — |
| AC-05 | AC-07 | AC-C7, R-08, R-10, R-11 | razionale §6.2 (AC-C7) per gli attributi; tecnico §7.1 (AC-C7) | QF-06 |
| AC-06 | AC-09 | AC-C9, R-14, R-20 | tecnico §7.1 (AC-C9), §9.2 | QF-03 |
| AC-07 | AC-12 | AC-B2 | tecnico §3.2 (elenco), §7.1 (AC-B2) | QF-11 |

Tolti dalla revisione del 18/11/2026, per analogia con UC-FDR-001 (razionale D-11, da confermare): AC-02, AC-04, AC-08 e AC-10, che sono comuni; AC-11, diventato la guardia VG-B1 (tecnico §7.2); AC-13, assorbito da AC-03 (razionale §6.2). AC-07 non ha più il vincolo di unicità e conserva la revisione prevista.

Vale la stessa nota di UC-FDR-001 (sezione 1.5) per AC-06.

## 3. Punti aperti che toccano gli UC

| Aperto | Dove negli UC | Ipotesi di lavoro | Dove |
| --- | --- | --- | --- |
| QF-03: tempo massimo di propagazione (DM-08) | UC-FDR-001: passo 7, AC-06; UC-FDR-002: passo 3, AC-06 | timeout tecnico di 360 secondi con lettura ogni 10 secondi, da non presentare come garanzia | razionale §9; tecnico §9.2 |
| QF-06: fuso e precisione delle date (DM-07) | UC-FDR-001: AC-02, AC-05, AC-07, postcondizione 2; UC-FDR-002: AC-02, AC-05, postcondizione 2 | istanti in UTC, XML senza offset letto come Europe/Rome, giorni come date con la data dell'esito portata a Europe/Rome, precisione al secondo | razionale §9; tecnico §6.4, §7.1 |
| QF-11: revisione attesa dopo la conversione (DM-09) | UC-FDR-002: AC-07, postcondizione 2 | la prima revisione, letta dall'elenco e confrontata con 1 solo dopo conferma | razionale §9; tecnico §7.1 |
| DM-04: esiti applicativi della legacy | UC-FDR-002: passo 2 (guardia VG-B1); UC-FDR-001: passi 8 e 9 (elenco vuoto o flusso non ancora disponibile) | nessuna: da rilevare alla prima esecuzione approvata | tecnico §4.5, §8.6 |
| Dati operativi per eseguire (DM-01, DM-02, DM-03, DM-05, DM-11, DM-13, DM-14, DM-16) | per direzione | nessuna | tecnico §10.3 |
| JTBD | intestazione di entrambi gli UC | proposta da validare | razionale §5.3 |

## 4. Dettagli tolti dagli UC v2 e dove si trovano

La colonna "Dove era" usa la numerazione degli UC v2, identica a quella dei v3 prima della revisione degli AC del 18/11/2026; i numeri attuali sono nelle tabelle delle sezioni 1.5 e 2.5.

| Dettaglio | Dove era negli UC v2 | Dove si trova ora |
| --- | --- | --- |
| Dati da fornire alla creazione del flusso | UC-FDR-001, passo 1 | razionale FP-A1; tecnico §3.4, §8.1, §8.2 |
| Percorso fra le API di PSP ed EC, senza frontend né accessi interni | passo 1 di entrambi | razionale Premesse, D-03, §1.4 |
| Convalida della richiesta rispetto alle anagrafiche | UC-FDR-001, passo 2 | razionale FP-A2, R-17 |
| Dati di ciascun pagamento | UC-FDR-001, passo 3 | razionale FP-A3; tecnico §3.4, §6.2, §8.3 |
| Totali calcolati aggiornati a ogni aggiunta | UC-FDR-001, passo 4 | razionale FP-A4; tecnico §3.2, §6.1 |
| Documento XML ricostruito e ricevuto per intero | UC-FDR-001, passi 7 e 9 | razionale FP-A7, FP-A9; tecnico §4.4, §5 |
| Invio del flusso completo in un'unica operazione | UC-FDR-002, passo 1 | razionale FP-B1; tecnico §4.2 |
| Conversione con creazione, aggiunta e pubblicazione automatiche | UC-FDR-002, passo 3 | razionale FP-B3 |
| Filtro per PSP e revisione nella lettura dell'elenco | UC-FDR-002, passo 4 | razionale FP-B4; tecnico §3.2, §3.3 |
| Lettura dei pagamenti su più pagine | UC-FDR-002, passo 6 e AC-08 | razionale FP-B6; tecnico §3.3, RI-13 |
| Eccezione di mancata disponibilità del flusso nell'altra modalità, con ritentativi automatici e ripristino manuale | EF-01 di entrambi | razionale §6.4, R-14, AC-C9, D-10; tecnico §9.2, §9.3; non è un'eccezione: è il fallimento di AC-C9 |
| Dati di test che restano nell'ambiente | postcondizione 3 di entrambi | razionale PO-A3, PO-B3; tecnico RI-09 |
| Ambiente UAT | precondizione sui servizi operativi | intestazione di razionale e tecnico |
| Dati facoltativi legacy sempre presenti | UC-FDR-002, precondizione 6 | razionale R-13; tecnico §8.5 |
| Registrazione di PSP ed EC nella configurazione della modalità nuova | UC-FDR-002, precondizione 7 | razionale PRE-B1, R-17 |
| Campi confrontati per il pagamento | AC-07 | razionale §6.2; tecnico §7.1 |
| Confronto di mittente, destinatario e dati del regolamento | AC-02, AC-04 | ritirato dagli AC (razionale D-07, §6.2); restano dati di input validi per entrambe le modalità (PRE-C6) |
| Importi confrontati come decimali | AC-05 | razionale AC-C5; tecnico §7.1, RI-05 |
| Abbinamento dei pagamenti per IUV e IUR, senza ordine | AC-06 | razionale R-07, D-05; tecnico §7.1 |
| Fuso e precisione delle date | AC-03, AC-07 | razionale §9; tecnico §6.4, §7.1 |
| Requisito dei dieci secondi per la singola richiesta | AC-09 | razionale R-20 |
| Controllo di unicità nell'elenco | AC-10 | ritirato (razionale D-07, §6.2); la prova di assenza è fuori perimetro (razionale §1.4) |
| Formato del documento ricevuto dall'EC | UC-FDR-001, AC-14 | razionale AC-A4, D-09; tecnico §4.4, §5, §7.1 (validazione contro l'XSD) |
| Esito dell'invio senza errore applicativo | UC-FDR-002, AC-11 | passato a guardia: razionale §6.6 (VG-B1); tecnico §4.5, §7.2 |
| Revisione prevista | UC-FDR-002, AC-12 | razionale AC-B2, QF-11; tecnico §7.1 |
| Esito positivo di creazione, aggiunta e pubblicazione | UC-FDR-001, AC-11 | guardia VG-A1: razionale §6.6; tecnico §3.1, §7.2 |
| Flusso pubblicato alla prima revisione, con totali coerenti, letto dal lato del PSP | UC-FDR-001, AC-12 | guardia VG-A2: razionale §6.6; tecnico §3.1, §7.2 |
| Completezza del flusso letto dall'EC | AC-08 di entrambi | assorbita da AC-C5 e AC-C6 (razionale §6.2); tecnico RI-13 |
| Dettaglio pubblicato con totali coerenti | UC-FDR-002, AC-13 | assorbito da AC-C5 (razionale §6.2); tecnico §7.1 |

Evidenza: prima di toglierli dagli UC, i dettagli sono stati cercati nei documenti indicati e nessuno è risultato mancante.

## 5. Avvertenze sui documenti

La ricerca dei dettagli non ha trovato mancanze che impediscano di alleggerire gli UC. Restano questi punti.

1. **Regole di confronto.** Ogni AC ha ora la sua riga in tecnico §7.1 e ogni guardia in §7.2. Per VG-B1 manca il valore di `esito` dell'invio riuscito (DM-04): finché non è rilevato la guardia controlla solo l'assenza di `fault`.
2. **Passi della piattaforma senza oracolo.** I passi 2, 4 e 7 di UC-FDR-001 e i passi 2 e 3 di UC-FDR-002 non hanno un controllo proprio: si osservano dall'esito della richiesta precedente (guardie, tecnico §7.2) o dalla lettura ripetuta (tecnico §9).
3. **Questioni aperte.** QF-03, QF-06 e QF-11 non hanno risposta e le ipotesi di lavoro sono in razionale §9. Finché restano tali, AC-02, AC-05 e AC-06 di entrambi gli UC, AC-07 di UC-FDR-001 (data e ora dell'elenco) e AC-07 di UC-FDR-002 (revisione) restano incompleti.
4. **JTBD.** L'identificativo non è assegnato: gli UC portano il segnaposto.
5. **Allineamento dei documenti.** Il 18/11/2026 razionale e tecnico sono stati allineati agli UC v3: EF-C1 è ritirata (razionale D-10, §6.4) e i riferimenti agli UC v2 puntano ai v3.
6. **Estensione per analogia a UC-FDR-002.** I ritiri di AC-11 e AC-13 e il mantenimento di AC-12, con la revisione prevista, sono assunzioni del redattore (razionale D-11): vanno confermati.
