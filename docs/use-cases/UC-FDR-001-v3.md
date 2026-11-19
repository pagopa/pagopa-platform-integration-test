## UC-FDR-001 - Pubblicazione FDR3 e recupero FDR1 (bozza v3)

JTBD di riferimento : JTBD-{NNN} (da assegnare)
Attore principale : PSP (Prestatore di Servizi di Pagamento)
Attori secondari : EC (Ente Creditore)

### Precondizioni

- PSP ed EC sono censiti sulla piattaforma e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione.
- PSP ed EC dispongono delle credenziali e delle abilitazioni previste per le due modalità.
- La coppia PSP/EC è gestita dalla piattaforma FDR: i suoi flussi non sono inoltrati a un gestore esterno.
- L'identificativo scelto per il flusso non è mai stato usato dal PSP.
- La modalità nuova, la modalità legacy e la conversione dalla nuova alla legacy sono operative.
- Il flusso da trattare è valido per entrambe le modalità.

### Flusso principale

1. Il PSP crea il flusso con la modalità nuova (FDR3).
2. La piattaforma convalida la richiesta e crea il flusso in bozza.
3. Il PSP aggiunge i pagamenti al flusso.
4. La piattaforma convalida i pagamenti e li aggiunge alla bozza.
5. Il PSP pubblica il flusso.
6. La piattaforma verifica la coerenza dei totali, pubblica il flusso e conferma l'operazione al PSP.
7. La piattaforma rende disponibile il flusso anche con la modalità legacy (FDR1). Il passaggio è asincrono rispetto alla conferma al PSP.
8. L'EC consulta con la modalità legacy (FDR1) i flussi del PSP e individua quello pubblicato.
9. L'EC richiede il flusso individuato e lo riceve completo.

### Flussi alternativi (AF)

Nessuno

### Eccezioni (EF)

Nessuno

### Postcondizioni

- Il flusso è pubblicato nella modalità nuova alla prima revisione, con totali coerenti.
- Lo stesso flusso è disponibile all'EC nella modalità legacy, completo e con contenuto equivalente a quello pubblicato.
- Il flusso pubblicato non è più modificabile né cancellabile.

### Acceptance Criteria

- AC-01: L'identificativo del flusso recuperato coincide con quello pubblicato. (FP)
- AC-02: Data e ora del flusso e giorno di regolamento coincidono con quelli pubblicati, senza spostamenti del giorno di calendario. (FP)
- AC-03: Numero e importo totale dichiarati coincidono con quelli pubblicati e con quelli dei pagamenti recuperati. (FP)
- AC-04: I pagamenti recuperati sono tutti e soli quelli pubblicati: nessuno manca, è duplicato o è aggiunto. (FP)
- AC-05: Ogni pagamento recuperato ha lo stesso contenuto del pagamento pubblicato. (FP)
- AC-06: Il flusso diventa disponibile all'EC nella modalità legacy entro il tempo massimo previsto dalla conferma della pubblicazione. (FP)
- AC-07: L'elenco consultato dall'EC contiene il flusso pubblicato, con il suo identificativo e la sua data e ora. (FP)
- AC-08: Il flusso ricevuto dall'EC è valido rispetto allo schema XSD della modalità legacy. (FP)
