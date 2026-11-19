---
schema: uc-workflow/v1
artifact: test-data
producer_skill: uc-test-data
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-002"
run_id: "20261119-01"
uc_input: "docs/use-cases/UC-FDR-002-v3.md"
uc_revision: "v3"
environment: uat
revision: 1
status: ready
updated_at: "2026-11-19T10:28:00+01:00"
inputs:
  - path: "docs/use-cases/workflow-runs/fdr-e2e-ibrido/UC-FDR-002/20261119-01/01-context.md"
    revision: 1
---

# UC - Test data

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-003 | docs/fdr-e2e-ibrido-02-dati-tecnici-v3.md | §6.3, §8.3, §8.4, §8.5 | 2026-11-19 | UAT, v3 | provided | Richiesta all'analista, 2026-11-19 |
| S-002 | docs/fdr-e2e-ibrido-01-razionale-uc-v3.md | §6.5 (VAR-02 … VAR-05) | 2026-11-19 | UAT, v3 | provided | Richiesta all'analista, 2026-11-19 |
| S-006 | docs/use-cases/test-data/ | ricerca di cataloghi FDR | 2026-11-19 | repository | unknown | Nessun catalogo FDR trovato (esiste solo `checkout`); nessun valore ne deriva |

## Data resolution
| Data id | Scenario id | Parameter and constraints | Value or TODO token | Source id and passage | Admission | Fitness | Availability evidence | Unresolved reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | SC-001, SC-003 | Numero pagamenti, intero da 1 | 3 | S-002 §6.5 VAR-04; S-003 §8.3 | provided | fit | documented-not-checked | Nessuno |
| D-001 | SC-002, SC-005 | Numero pagamenti uguale alle liste | 4 | S-002 §6.5 | provided | fit | documented-not-checked | Nessuno |
| D-001 | SC-004 | Numero pagamenti | 1 e 5 (due righe) | S-002 §6.5 VAR-04 | provided | fit | documented-not-checked | Nessuno |
| D-002 | SC-001 … SC-004 | Importi a due decimali | 100.00 per pagamento | S-003 §8.4 | provided | fit | documented-not-checked | Nessuno |
| D-002 | SC-005 | Importi a due decimali, totale = somma | 0.01, 10.00, 1234.56, 999999.99 | S-002 §6.5 VAR-05 | provided | fit | documented-not-checked | Nessuno |
| D-003 | SC-001, SC-003, SC-004, SC-005 | Esito ammesso | eseguito per ogni pagamento | S-003 §8.5 | provided | fit | documented-not-checked | Nessuno |
| D-003 | SC-002 | Quattro esiti ammessi, "revocato" escluso | eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT | S-002 §6.5 VAR-02; S-003 §8.5 | provided | fit | documented-not-checked | Nessuno |
| D-004 | SC-001, SC-002, SC-004, SC-005 | Indice di trasferimento 1..5 | 1 per ogni pagamento | S-003 §8.3 | provided | fit | documented-not-checked | Nessuno |
| D-004 | SC-003 | Indice di trasferimento 1..5 | 1, 3, 5 | S-002 §6.5 VAR-03 | provided | fit | documented-not-checked | Nessuno |

## Combinations
| Combination id | Scenario id | Data ids and selected values | Relationship evidence | Fitness | Unresolved reason |
| --- | --- | --- | --- | --- | --- |
| C-001 | SC-001 | D-001=3; D-002=100.00 x3; D-003=eseguito x3; D-004=1, 1, 1 | Liste della stessa lunghezza di D-001 | fit | Nessuno |
| C-002 | SC-002 | D-001=4; D-002=100.00 x4; D-003=i quattro esiti; D-004=1 x4 | Una voce per pagamento | fit | Nessuno |
| C-003 | SC-003 | D-001=3; D-002=100.00 x3; D-003=eseguito x3; D-004=1, 3, 5 | Una voce per pagamento | fit | Nessuno |
| C-004 | SC-004 | D-001=1; D-002=100.00; D-003=eseguito; D-004=1 | Una voce per pagamento | fit | Nessuno |
| C-005 | SC-004 | D-001=5; D-002=100.00 x5; D-003=eseguito x5; D-004=1 x5 | Una voce per pagamento | fit | Nessuno |
| C-006 | SC-005 | D-001=4; D-002=0.01, 10.00, 1234.56, 999999.99; D-003=eseguito x4; D-004=1 x4 | Totale = somma esatta | fit | Nessuno |

## Decisions
| Question id | Candidate or data ids | Human decision and date | Scope | State |
| --- | --- | --- | --- | --- |
| Nessuno | | | | |

## Scenario warnings
| Scenario id | Affected combinations or all | Data ids | Required comment |
| --- | --- | --- | --- |
| SC-001 … SC-005 | all | D-001 … D-004 | not-applicable |

Incertezza senza placeholder: disponibilita dei valori documentata ma non verificata sull'ambiente; nessuna cella vuota.

## Optional catalogue
not-saved: nessun catalogo FDR esistente e nessuna richiesta di salvarne uno.

## Readiness
Stato: `ready`. D-001 … D-004 risolti per SC-001 … SC-005 con valori documentati (provided, fit). Nessun dato non risolto, nessuno stato di entita richiesto. Nessun controllo dal vivo eseguito.
