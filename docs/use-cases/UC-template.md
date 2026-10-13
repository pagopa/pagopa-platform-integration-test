# Template Use Case (UC)

Struttura concordata per redigere gli UC. È il contratto di ingresso della
skill [uc-to-feature](../../.github/skills/uc-to-feature/SKILL.md).
Il flusso automatico e manuale e descritto in [uc-workflow.md](uc-workflow.md).

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
