---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-002"
run_id: "20261119-01"
uc_input: "docs/use-cases/UC-FDR-002-v3.md"
uc_revision: "v3"
environment: uat
revision: 1
status: incomplete
updated_at: "2026-11-19T10:35:00+01:00"
inputs:
  - path: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-002/20261119-01/01-context.md"
    revision: 1
  - path: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-002/20261119-01/02-test-data.md"
    revision: 1
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |
| docs/use-cases/features/fdr-hybrid/FEAT_002_FdRHybrid_Invio_FDR1_e_recupero_FDR3.feature | uc-to-feature | created |

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |
| SC-001 … SC-005 (un solo Schema dello scenario `@fdrhybrid_002_01`, righe C-001 … C-006) | Precondizioni 1-7 | Contesto (6 Dato/E) | F-010 | Precondizioni condivise |
| SC-001 … SC-005 | Passi 1-2 | Dato (dati) + Quando invio legacy; Allora convalida, conserva, esito positivo | F-001, F-011, F-012 | Guardia VG-B1 |
| SC-001 … SC-005 | Passi 3-4 | Quando consultazione elenco FDR3; Allora flusso del PSP mittente entro il tempo massimo; E revisione prevista | F-002, F-003, F-007, F-008 | Passo 3 senza oracolo proprio |
| SC-001 … SC-005 | Passo 5 | Quando dettaglio; Allora ricevuto; E identificativo e date | F-004, F-006 | Stessa operazione |
| SC-001 … SC-005 | Passo 6 | Quando pagamenti; Allora tutti; E totali, tutti e soli, contenuto | F-005, F-006 | Stessa operazione |

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |
| Precondizioni 1-7 | SC-001 | docs/use-cases/features/fdr-hybrid/FEAT_002_FdRHybrid_Invio_FDR1_e_recupero_FDR3.feature | Il PSP invia un flusso con la modalità legacy e l'EC lo recupera con la modalità nuova | not-applicable (Contesto) | covered come Given; preparazione e rilievo implementativo |
| Passi 1-2 | SC-001 | stesso | stesso | tutte | covered |
| Passo 3 | SC-001 | stesso | stesso | tutte | partial: solo osservato dalla lettura; T non definito (Q-001) |
| Passi 4-6 | SC-001 | stesso | stesso | tutte | covered |
| AC-01, AC-03, AC-04 | SC-001 | stesso | stesso | tutte | covered |
| AC-02 | SC-001 | stesso | stesso | tutte | partial: fuso e precisione (Q-002) |
| AC-05 | SC-001 | stesso | stesso | tutte | partial: giorno dell'esito dipende da Q-002 |
| AC-06 | SC-001 | stesso | stesso | tutte | partial: nessun valore di T (Q-001) |
| AC-07 | SC-001 | stesso | stesso | tutte | partial: flusso e PSP coperti; revisione prevista non decisa (Q-005), nessun numero nella feature |
| Postcondizione 1 | SC-001 | stesso | stesso | tutte | partial: solo prova indiretta (esito positivo e successiva disponibilita) |
| Postcondizione 2 | SC-001 | stesso | stesso | tutte | partial: come AC-06, AC-02, AC-07 |
| Postcondizione 3 | SC-001 | stesso | stesso | not-applicable | uncovered: nessun oracolo documentato (Q-003) |
| Varianti VAR-02 … VAR-05 | SC-002 … SC-005 | stesso | stesso | righe 2, 3, 4-5, 6 | covered |

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |
| SC-001 | C-001 | D-001 … D-004 | O-001 … O-012 | 3 pagamenti; 100.00 x3; eseguito x3; indici 1, 1, 1. Non risolti: O-002, O-006, O-007, O-009, O-012 |
| SC-002 | C-002 | D-001 … D-004 | come sopra | 4 pagamenti; quattro esiti |
| SC-003 | C-003 | D-001 … D-004 | come sopra | indici 1, 3, 5 |
| SC-004 | C-004, C-005 | D-001 … D-004 | come sopra | 1 e 5 pagamenti |
| SC-005 | C-006 | D-001 … D-004 | come sopra | importi 0.01, 10.00, 1234.56, 999999.99 |

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |
| Q-001 | SC-001 … SC-005 | Tempo massimo di propagazione (QF-03) | open |
| Q-002 | SC-001 … SC-005 | Fuso e precisione (QF-06) | open |
| Q-003 | SC-001 … SC-005 | Oracolo della postcondizione 3 | open |
| Q-004 | Nessuno | Approvazione della mappa dei riferimenti | pending-approval |
| Q-005 | SC-001 … SC-005 | Revisione prevista (QF-11) | open |

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |
| Lingua e parole chiave | `behave --lang-help it` e rilettura | passed | Funzionalità, Contesto, Dato, Quando, Allora, E, Schema dello scenario, Esempi |
| Intestazione e tag del profilo | Rilettura contro il profilo | passed | tracking `#0123456789`, `# language: it`, tag |
| Indentazione, limite di 12 definizioni | Rilettura | passed | 1 definizione, 6 righe espanse |
| Nessuna cella vuota, placeholder, T o revisione numerica | Rilettura | passed | Nessun commento sui dati |
| Fonti ammesse | Confronto con 01-context | passed | La mappa pending-approval non e usata |
| Esecuzione, parser Python, test | Non eseguiti (vietati) | not-run | Valutazione per sola lettura |

## Engineer handoff
Un solo Schema dello scenario con 6 righe (C-001 … C-006); liste separate da virgole da trasformare in strutture (importi Decimal, esiti mappati ai codici della legacy). La guardia dell'invio produce "non valido" se l'esito non e positivo. Le letture dell'EC sono ripetute fino al tempo massimo configurato (non nel Gherkin); la revisione prevista va fissata in configurazione dopo Q-005. Dettagli in `report_traduzione_uc-fdr-002.md`. La bozza non e un permesso di implementare.

## Readiness
bozza. Motivi: Q-001, Q-002, Q-003, Q-005 aperte; Q-004 pending-approval; postcondizione 1 solo indiretta. La sintassi valutata per lettura non implica prontezza all'esecuzione.
