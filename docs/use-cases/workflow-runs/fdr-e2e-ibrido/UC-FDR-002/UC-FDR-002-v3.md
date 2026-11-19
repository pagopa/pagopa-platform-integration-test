## UC-FDR-002 - Invio FDR1 e recupero FDR3 (bozza v3)

JTBD di riferimento : JTBD-{NNN} (da assegnare)
Attore principale : PSP (Prestatore di Servizi di Pagamento)
Attori secondari : EC (Ente Creditore)

### Precondizioni

- PSP ed EC sono censiti sulla piattaforma e abilitati rispettivamente a inviare e a ricevere flussi di rendicontazione.
- PSP ed EC dispongono delle credenziali e delle abilitazioni previste per le due modalità.
- La coppia PSP/EC è gestita dalla piattaforma FDR: i suoi flussi non sono inoltrati a un gestore esterno.
- L'identificativo scelto per il flusso non è mai stato usato dal PSP.
- La modalità legacy, la modalità nuova e la conversione dalla legacy alla nuova sono operative.
- Il flusso da trattare è valido per entrambe le modalità.
- PSP ed EC sono noti anche alla modalità nuova, così che la conversione possa creare il flusso.

### Flusso principale

1. Il PSP invia il flusso con la modalità legacy (FDR1).
2. La piattaforma convalida l'invio, conserva il flusso e risponde con esito positivo.
3. La piattaforma converte il flusso e lo rende disponibile nella modalità nuova (FDR3). Il passaggio è asincrono rispetto alla conferma al PSP.
4. L'EC consulta con la modalità nuova (FDR3) i flussi pubblicati del PSP e individua il flusso.
5. L'EC richiede il dettaglio del flusso.
6. L'EC richiede i pagamenti del flusso e li ottiene tutti.

### Flussi alternativi (AF)

Nessuno

### Eccezioni (EF)

Nessuno

### Postcondizioni

- Il flusso inviato con la modalità legacy è conservato dalla piattaforma.
- Lo stesso flusso è pubblicato nella modalità nuova ed è leggibile dall'EC, completo e con contenuto equivalente a quello inviato.
- Il flusso pubblicato non è più modificabile né cancellabile.

### Acceptance Criteria

- AC-01: L'identificativo del flusso recuperato coincide con quello inviato. (FP)
- AC-02: Data e ora del flusso e giorno di regolamento coincidono con quelli inviati, senza spostamenti del giorno di calendario. (FP)
- AC-03: Numero e importo totale dichiarati coincidono con quelli inviati e con quelli dei pagamenti recuperati. (FP)
- AC-04: I pagamenti recuperati sono tutti e soli quelli inviati: nessuno manca, è duplicato o è aggiunto. (FP)
- AC-05: Ogni pagamento recuperato ha lo stesso contenuto del pagamento inviato. (FP)
- AC-06: Il flusso diventa disponibile all'EC nella modalità nuova entro il tempo massimo previsto dalla conferma dell'invio. (FP)
- AC-07: L'elenco consultato dall'EC contiene il flusso associato al PSP mittente, con la revisione prevista. (FP)
