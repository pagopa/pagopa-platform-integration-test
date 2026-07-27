# Tag di setup per FdR

Questi tag vengono usati nelle feature Gherkin per preparare automaticamente lo scenario prima dell'esecuzione. Sono interpretati dal file environment.py e attivano i metodi di supporto definiti in common.py.

## @Crea_FdR

Tag usato per creare un nuovo flusso di rendicontazione (FdR) e associarlo a un PSP.

### Parametri
- `id_fdr` (obbligatorio): identificativo del flusso da creare.
- `id_psp` (obbligatorio): identificativo del PSP da associare al flusso.

### Note importanti
- Se il valore contiene spazi, va scritto come valore URL-encoded, ad esempio `PSP%20DEMO`.
- In fase di esecuzione il valore viene decodificato automaticamente, quindi `PSP%20DEMO` diventa `PSP DEMO`.

### Esempio
```gherkin
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001", id_psp="PSP%20DEMO")
```

## @Inserisci_Pagamenti
Tag usato per inserire pagamenti nel flusso creato con @Crea_FdR.

### Parametri
- `totPayments` (obbligatorio): numero totale di pagamenti da inserire.
- `sumPayments` (obbligatorio): importo totale dei pagamenti.

### Esempio
```gherkin
@Inserisci_Pagamenti(totPayments=3, sumPayments=3000)
```

### @Pubblica_FdR
Tag usato per pubblicare il flusso FdR dopo la creazione e, se previsto, dopo l'inserimento dei pagamenti.

### Parametri
Nessun parametro.

### Esempio
```gherkin
@Pubblica_FdR
```

### Esempio completo
Di seguito un esempio di utilizzo combinato dei tre tag:
```gherkin
@Crea_FdR(id_fdr="2025-01-01PSPDEMO-0001", id_psp="PSP%20DEMO")
@Inserisci_Pagamenti(totPayments=3, sumPayments=3000)
@Pubblica_FdR
Scenario: Esempio di scenario FdR
```

