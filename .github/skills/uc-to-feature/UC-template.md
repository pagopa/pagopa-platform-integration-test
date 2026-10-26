# Template Use Case (UC)

Struttura concordata per redigere gli UC. È il contratto di ingresso della
skill [uc-to-feature](SKILL.md).
Il flusso automatico e manuale e descritto in
[uc-workflow.md](../../../docs/use-cases/uc-workflow.md).

Le AF descrivono cambiamenti del percorso o dell'esito, non varianti dei dati.
L'analista ricava i set di dati rilevanti dalla documentazione e dal materiale
ammessi: piu set possono verificare lo stesso flusso con uno Scenario Outline,
senza una AF che li elenchi.

Per gli AC e consigliato, ma non obbligatorio, un riferimento verbale al flusso,
per esempio `AC01 - {criterio} (FP)` o `AC03 - {criterio} (AF02)`.
Sono ammesse le forme estese e abbreviate, senza distinzione maiuscole/minuscole
o rigidita sugli spazi, descritte nelle
[regole di riconoscimento](ac-flow-references.md).
Il riferimento si applica alle varianti dati del flusso, salvo condizioni
specifiche del criterio; non definisce da solo nuovi casi o valori.

```markdown
## UC-{PRODOTTO}-{NNN} - {Titolo breve}

JTBD di riferimento : JTBD-{NNN}
Attore principale : {ruolo utente o sistema}
Attori secondari : {oppure —}

### Precondizioni
- {cosa deve essere già vero prima che il flusso inizi}

### Flusso principale
1. {passo 1 - azione dell'attore o del sistema}
2. {passo 2}
...

### Flussi alternativi (AF)
- AF-01: {cosa succede se X - indica a quale passo del flusso principale si rientra}

### Eccezioni (EF)
- EF-01: {situazione anomala - comportamento atteso dal sistema}

### Postcondizioni
- {stato del sistema al termine del flusso con successo}

### Acceptance Criteria
- AC-01: {criterio verificabile - risposta sì/no senza interpretazione}
- AC-02: ...
```
