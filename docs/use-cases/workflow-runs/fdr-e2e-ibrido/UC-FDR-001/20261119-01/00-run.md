---
schema: uc-workflow/v1
artifact: run
producer_skill: uc-to-feature
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-001"
run_id: "20261119-01"
uc_input: "docs/use-cases/UC-FDR-001-v3.md"
uc_revision: "v3"
environment: uat
revision: 2
status: draft
updated_at: "2026-11-19T10:18:00+01:00"
inputs: []
---

# UC - Run

## Agreed inputs
| Item | Value | Human confirmation |
| --- | --- | --- |
| Functional sources | `docs/fdr-e2e-ibrido-01-razionale-uc-v3.md` (razionale v3), `docs/fdr-e2e-ibrido-02-dati-tecnici-v3.md` (dati tecnici v3) | Richiesta all'analista, 2026-11-19 (ACE task `2026-11-19-fdr-uc-to-feature-093800`) |
| Data sources | `docs/fdr-e2e-ibrido-02-dati-tecnici-v3.md` (§6.3, §8) | Richiesta all'analista, 2026-11-19 (ACE task `2026-11-19-fdr-uc-to-feature-093800`) |
| Feature paths | `docs/use-cases/features/fdr-hybrid/FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature` | Richiesta all'analista, 2026-11-19 |
| Run directory | `docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/` | Richiesta all'analista, 2026-11-19 |
| Gherkin profile inputs | tracking `#0123456789`; suite `FdRHybrid` (tag `@fdrhybrid_001_…`) | Richiesta all'analista, 2026-11-19 |
| Identita | Jira PQ-827, branch `PQ-827-fdr-e2e-test-design`; ACE request `2026-11-19-fdr-uc-to-feature-093800`; identita UC `fdr-e2e-ibrido` / `UC-FDR-001` / `20261119-01` | Richiesta all'analista, 2026-11-19 |
| Focus e confini | Percorso di successo del flusso principale (UC senza AF ed EF); nessun Python, test, commit, push o PR | UC-FDR-001-v3 e richiesta, 2026-11-19 |

## Scenario inventory
| Scenario id | UC elements | Behaviour to cover |
| --- | --- | --- |
| SC-001 | Precondizioni 1-6, passi 1-9, postcondizioni 1-3, AC-01 … AC-08 | Pubblicazione del flusso con la modalita nuova (FDR3) e recupero con la modalita legacy (FDR1): percorso di successo |
| SC-002 | Passi 3 e 6, AC-03 … AC-05 | Variante: i quattro esiti ammessi dei pagamenti |
| SC-003 | Passi 3 e 6, AC-05 | Variante: indice di trasferimento 1, 3, 5 |
| SC-004 | Passi 3 e 6, AC-03, AC-04 | Variante: 1 e 5 pagamenti |
| SC-005 | Passi 3 e 6, AC-03, AC-05 | Variante: importi estremi, totale come somma |

## Artifacts
| Artifact | Producer skill | Path | Revision | State |
| --- | --- | --- | --- | --- |
| context | uc-scenario-context | docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/01-context.md | 1 | incomplete |
| test-data | uc-test-data | docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/02-test-data.md | 1 | ready |
| feature-report | uc-to-feature | docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/03-feature-report.md | 1 | incomplete |

## Questions
| Question id | Stage | Question | Decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | uc-scenario-context | Tempo massimo di propagazione (QF-03) | Nessuna decisione | open |
| Q-002 | uc-scenario-context | Fuso e precisione di istanti e giorni (QF-06) | Nessuna decisione | open |
| Q-003 | uc-scenario-context | Oracolo della postcondizione 3 | Nessuna decisione | open |
| Q-004 | uc-scenario-context | Approvazione della mappa dei riferimenti | Nessuna decisione | pending-approval |

## History
| Timestamp | Skill or human | Action | Output path and revision | Invalidated outputs |
| --- | --- | --- | --- | --- |
| 2026-11-19T09:52:00+01:00 | uc-to-feature | Registro inizializzato con input concordati dalla richiesta e inventario iniziale | 00-run.md rev 1 | Nessuno |
| 2026-11-19T09:58:00+01:00 | uc-scenario-context | Contesto creato, stato incomplete; inventario esteso a SC-002 … SC-005 | 01-context.md rev 1 | Nessuno |
| 2026-11-19T10:02:00+01:00 | uc-test-data | Dati risolti, stato ready | 02-test-data.md rev 1 | Nessuno |
| 2026-11-19T10:12:00+01:00 | uc-to-feature | Feature e report creati, prontezza bozza; report di traduzione creato | 03-feature-report.md rev 1 | Nessuno |
