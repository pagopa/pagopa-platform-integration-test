---
schema: uc-translation-report/v1
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-002"
run_id: "20261119-01"
derived_from: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-002/20261119-01/03-feature-report.md"
revision: 1
status: draft
updated_at: "2026-11-19T10:37:00+01:00"
findings: 10
proposals: 0
---

# Report di traduzione - UC-FDR-002

Nota: il template `report-traduzione.template.md` non esiste nel repository; la struttura e dedotta dalla skill.

## Findings
| Id | Tipo | Riferimento | Dubbio o criticita | Fonte | Proposta | Effetto sulla feature |
| --- | --- | --- | --- | --- | --- | --- |
| FND-001 | funzionale-aperto | AC-06, passo 3 | Tempo massimo T non definito | razionale R-14, R-20, QF-03 | Decidere T (Q-001) | Nessun valore numerico |
| FND-002 | funzionale-aperto | AC-02, AC-05 | Fuso e precisione non decisi | razionale QF-06 | Decidere (Q-002) | Date senza fuso |
| FND-003 | funzionale-aperto | Postcondizione 3 | Nessun oracolo osservabile | razionale PO-B3, §1.4 | Decidere (Q-003) | Nessuno step |
| FND-004 | funzionale-aperto | AC-07 | Revisione prevista non decisa (ipotesi 1) | razionale QF-11 | Decidere (Q-005) | "revisione prevista" senza numero |
| FND-005 | funzionale-aperto | Postcondizione 1 | La conservazione e provabile solo indirettamente | razionale §6.6 | Confermare la prova indiretta | Verifica nell'esito dell'invio |
| FND-006 | dato | Precondizioni 1, 2, 3, 5, 7 | Nessun controllo documentato; conoscenza di PSP ed EC da parte della modalita nuova | dati tecnici RI-15 | Definire la preparazione | Solo Given |
| FND-007 | implementativo | Passi 1-2 | Guardia VG-B1: "non valido", non "fallito"; scritture senza retry | dati tecnici §7.2, RI-07, RI-22 | Esito distinto | Nessuno |
| FND-008 | dato | Passi 1, 4-6 | Endpoint, credenziali, abilitazioni (DM-01/02/03/13/14); valori generati (identificativo ≤35 caratteri, date, IUV, IUR); Decimal | dati tecnici §8, RI-05, RI-06 | Configurazione e generatori | Nessuno |
| FND-009 | implementativo | Esecuzione | Suite, tag di selezione (non `@e2e` nel profilo), nrt-suites.json, resource_group, esecuzione sequenziale | dati tecnici §11, RI-10 | Decidere in implementazione | Tag non aggiunto |
| FND-010 | implementativo | Esempi, sicurezza | Liste separate da virgole da trasformare; mascheramento segreti | feature; RI-11 | Parsing e mascheramento | Colonne a lista |

## Proposals
Nessuno
