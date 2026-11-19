---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-001"
run_id: "20261119-01"
uc_input: "docs/use-cases/UC-FDR-001-v3.md"
uc_revision: "v3"
environment: uat
revision: 1
status: incomplete
updated_at: "2026-11-19T10:12:00+01:00"
inputs:
  - path: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/01-context.md"
    revision: 1
  - path: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-001/20261119-01/02-test-data.md"
    revision: 1
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |
| docs/use-cases/features/fdr-hybrid/FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature | uc-to-feature | created |

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |
| SC-001 … SC-005 (un solo Schema dello scenario `@fdrhybrid_001_01`, righe C-001 … C-006) | Precondizioni 1-6 | Contesto (5 Dato/E) | F-010 | Precondizioni condivise |
| SC-001 … SC-005 | Passi 1-6 | Dato (dati) + Quando/Allora di creazione, aggiunta, pubblicazione + E di prima revisione e totali | F-001, F-002, F-011 | Ogni azione con il suo esito osservabile |
| SC-001 … SC-005 | Passi 7-8 | Quando consultazione elenco; Allora elenco contiene il flusso entro il tempo massimo; E voce con identificativo e data e ora | F-003, F-004, F-007, F-008 | Passo 7 senza oracolo proprio |
| SC-001 … SC-005 | Passo 9 | Quando richiesta del flusso; Allora flusso completo; E XSD, id, date, totali, pagamenti tutti e soli, contenuto | F-005, F-006, F-008 | Verifiche della stessa operazione |

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |
| Precondizioni 1-6 | SC-001 | docs/use-cases/features/fdr-hybrid/FEAT_001_FdRHybrid_Pubblicazione_FDR3_e_recupero_FDR1.feature | Il PSP pubblica un flusso con la modalità nuova e l'EC lo recupera con la modalità legacy | not-applicable (Contesto e Dato) | covered come Given; la preparazione e un rilievo implementativo |
| Passi 1-6 | SC-001 | stesso | stesso | tutte | covered |
| Passo 7 | SC-001 | stesso | stesso | tutte | partial: osservato solo dalla lettura dell'elenco; T non definito (Q-001) |
| Passi 8-9 | SC-001 | stesso | stesso | tutte | covered |
| AC-01, AC-03, AC-04, AC-08 | SC-001 | stesso | stesso | tutte | covered |
| AC-02 | SC-001 | stesso | stesso | tutte | partial: fuso e precisione da definire (Q-002) |
| AC-05 | SC-001 | stesso | stesso | tutte | partial: importo, esito, indice coperti; giorno dell'esito dipende da Q-002 |
| AC-06 | SC-001 | stesso | stesso | tutte | partial: verificato "entro il tempo massimo previsto" senza valore (Q-001) |
| AC-07 | SC-001 | stesso | stesso | tutte | partial: identificativo coperto; data e ora dipendono da Q-002 |
| Postcondizione 1 | SC-001 | stesso | stesso | tutte | covered (lettura lato PSP, guardia VG-A2) |
| Postcondizione 2 | SC-001 | stesso | stesso | tutte | partial: come AC-06 e AC-02 |
| Postcondizione 3 | SC-001 | stesso | stesso | not-applicable | uncovered: nessun oracolo documentato (Q-003) |
| Varianti VAR-02 … VAR-05 | SC-002 … SC-005 | stesso | stesso | righe 2, 3, 4-5, 6 | covered |

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |
| SC-001 | C-001 | D-001 … D-004 | O-001 … O-012 | 3 pagamenti; 100.00 x3; eseguito x3; indici 1, 1, 1. Non risolti: O-002, O-006, O-007, O-012 |
| SC-002 | C-002 | D-001 … D-004 | come sopra | 4 pagamenti; i quattro esiti ammessi |
| SC-003 | C-003 | D-001 … D-004 | come sopra | indici 1, 3, 5 |
| SC-004 | C-004, C-005 | D-001 … D-004 | come sopra | 1 e 5 pagamenti |
| SC-005 | C-006 | D-001 … D-004 | come sopra | importi 0.01, 10.00, 1234.56, 999999.99 |

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |
| Q-001 | SC-001 … SC-005 | Tempo massimo di propagazione (QF-03) | open |
| Q-002 | SC-001 … SC-005 | Fuso e precisione di istanti e giorni (QF-06) | open |
| Q-003 | SC-001 … SC-005 | Oracolo della postcondizione 3 | open |
| Q-004 | Nessuno | Approvazione della mappa dei riferimenti | pending-approval |

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |
| Lingua e parole chiave | `behave --lang-help it` e rilettura del file | passed | Funzionalità, Contesto, Dato, Quando, Allora, E, Schema dello scenario, Esempi |
| Intestazione e tag del profilo | Rilettura contro il profilo Gherkin | passed | tracking `#0123456789`, `# language: it`, tag di feature e scenario |
| Indentazione, limite di 12 definizioni | Rilettura | passed | 1 definizione di scenario, 6 righe espanse |
| Nessuna cella vuota, nessun placeholder, nessun valore di T | Rilettura | passed | Nessun commento sui dati necessario |
| Nessun valore o requisito non supportato dalle fonti ammesse | Confronto con 01-context | passed | La mappa pending-approval non e usata |
| Esecuzione, parser Python, test | Non eseguiti (vietati) | not-run | Sintassi e copertura valutate solo per lettura |

## Engineer handoff
Un solo Schema dello scenario con 6 righe: ogni riga e una combinazione (C-001 … C-006) di numero di pagamenti, importi, esiti e indici di trasferimento, espressi come liste separate da virgole da trasformare in struttura (importi come Decimal; esiti mappati ai codici della legacy). Gli step di creazione, aggiunta e pubblicazione contengono le guardie VG-A1/VG-A2: se falliscono il test e "non valido", non fallito. Gli step di lettura ripetono l'interrogazione fino al tempo massimo configurato (T non nel Gherkin). Dettagli in `report_traduzione_uc-fdr-001.md`. La bozza non e un permesso di implementare.

## Readiness
bozza. Motivi: Q-001 (T, AC-06), Q-002 (fuso e precisione, AC-02, AC-05, AC-07), Q-003 (postcondizione 3 non coperta), Q-004 pending-approval. La sintassi valutata per lettura non implica prontezza all'esecuzione.
