---
schema: uc-translation-report/v1
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-001"
run_id: "20261119-01"
derived_from: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/03-feature-report.md"
revision: 1
status: draft
updated_at: "2026-11-19T10:15:00+01:00"
findings: 11
proposals: 2
---

# Report di traduzione - UC-FDR-001

Nota: il template `report-traduzione.template.md` non esiste nel repository; la struttura e dedotta dalla skill.

## Findings
| Id | Tipo | Riferimento | Dubbio o criticita | Fonte | Proposta | Effetto sulla feature |
| --- | --- | --- | --- | --- | --- | --- |
| FND-001 | funzionale-aperto | AC-06, passo 7 | Tempo massimo T non definito | razionale R-14, R-20, QF-03 | Decidere T (Q-001) | Step senza valore numerico |
| FND-002 | funzionale-aperto | AC-02, AC-05, AC-07 | Fuso e precisione non decisi | razionale QF-06 | Decidere (Q-002) | Verifiche date espresse senza fuso |
| FND-003 | funzionale-aperto | Postcondizione 3 | Nessun oracolo osservabile | razionale PO-A3, §1.4 | Decidere se escludere o definire (Q-003) | Nessuno step; uncovered |
| FND-004 | dato | Precondizioni 1, 2, 3, 5 | Nessun controllo documentato | dati tecnici RI-15 | Definire la preparazione in implementazione | Solo Given |
| FND-005 | implementativo | Passi 1-6 | Guardie VG-A1/VG-A2: esito "non valido", non "fallito"; scritture senza retry | dati tecnici §7.2, RI-07, RI-22 | Esito distinto | Nessuno |
| FND-006 | implementativo | Passi 8-9 | Esiti applicativi della legacy e compressione non documentati (DM-04, DM-16); "non ancora disponibile" da distinguere dagli errori | dati tecnici §9.3 | Rilevarli alla prima esecuzione approvata | Nessuno |
| FND-007 | dato | Passi 1, 3, 9 | Endpoint, chiavi, password, abilitazioni da accertare (DM-01/02/03/13/14) | dati tecnici §8.6 | Configurazione per ambiente | Nessuno |
| FND-008 | dato | Passi 1, 3 | Valori generati: identificativo unico (≤35 caratteri), date, IUV, IUR; Decimal; data esito a mezzogiorno UTC | dati tecnici §8, RI-05, RI-06 | Generatori | Nessuno |
| FND-009 | implementativo | Esecuzione | Suite, tag di selezione (non `@e2e` nel profilo), registrazione in nrt-suites.json, resource_group, esecuzione sequenziale | dati tecnici §11, RI-10 | Decidere in implementazione | Tag di selezione non aggiunto |
| FND-010 | implementativo | Esempi | Liste separate da virgole da trasformare in strutture | feature | Parsing nello step | Colonne a lista |
| FND-011 | implementativo | Sicurezza | Mascheramento dei segreti nei log | dati tecnici RI-11 | Applicare | Nessuno |

## Proposals
| Id | Ancora nel UC | Fonte | Scenario Gherkin proposto |
| --- | --- | --- | --- |
| SP-001 | Passo 3 | razionale R-05 | Scenario: il PSP aggiunge i pagamenti in piu richieste e la pubblicazione conserva tutti i pagamenti |
| SP-002 | Passo 6 | razionale R-06 | Scenario: la pubblicazione e rifiutata se i totali dichiarati non coincidono |
