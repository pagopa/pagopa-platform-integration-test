---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-002"
run_id: "20261119-01"
uc_input: "docs/use-cases/UC-FDR-002-v3.md"
uc_revision: "v3"
environment: uat
revision: 1
status: incomplete
updated_at: "2026-11-19T10:25:00+01:00"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | docs/use-cases/UC-FDR-002-v3.md | intero UC (precondizioni, passi 1-6, postcondizioni, AC-01 … AC-07) | 2026-11-19 | UAT, v3 | provided | Richiesta all'analista, 2026-11-19 |
| S-002 | docs/fdr-e2e-ibrido-01-razionale-uc-v3.md | §1.4, §1.5, §4 (R-nn), §6, §6.5, §6.6, §7, §9 | 2026-11-19 | UAT, v3 | provided | Richiesta all'analista, 2026-11-19 |
| S-003 | docs/fdr-e2e-ibrido-02-dati-tecnici-v3.md | §3, §5, §6, §7.1, §7.2, §8, §9, §12 | 2026-11-19 | UAT, contratti SANP3.13.0 (commit 969833a) | provided | Richiesta all'analista, 2026-11-19 |
| S-004 | README.md | Configurazione > E2E test; Suite disponibili > End-to-end; Esecuzione locale > E2E; Contribuire > Convenzioni Gherkin | 2026-11-19 | repository | unknown | Uso solo operativo; nessun valore o requisito funzionale ne deriva |
| S-005 | docs/use-cases/mappa-riferimenti-UC-FDR-v3.md | letta per orientamento, non usata come evidenza | 2026-11-19 | v3 | pending-approval | Q-004 |

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | SC-001 | Passi 1-2, postcondizione 1 | Quale esito ha l'invio del flusso con la modalita legacy? | Il PSP invia il flusso con la legacy; la piattaforma convalida, conserva e risponde con esito positivo. E la guardia VG-B1: se non soddisfatta il test e non valido e termina senza attendere la propagazione | S-003 §7.2; S-002 §6.6 | supported |
| F-002 | SC-001 | Passo 3 | Il passo 3 ha un oracolo proprio? | No: conversione asincrona senza oracolo proprio; si osserva con la lettura ripetuta dell'elenco FDR3 dei flussi pubblicati dell'EC (solo letture) | S-003 §9.1, §9.3; S-002 R-14 | supported |
| F-003 | SC-001 | Passo 4, AC-07 | Che cosa contiene l'elenco FDR3? | Una voce per il flusso, associata al PSP mittente (identificativo del PSP) e con la revisione prevista; il flusso si riconosce per uguaglianza esatta dell'identificativo | S-003 §7.1, §3.3; S-002 §6.2 | supported (flusso e PSP); la revisione prevista non e decisa (F-007) |
| F-004 | SC-001 | Passo 5, AC-01, AC-02 | Che cosa verifica il dettaglio? | Identificativo uguale; data e ora del flusso e giorno di regolamento uguali, senza spostamento del giorno | S-003 §7.1; S-002 §6.2 | supported (identificativo); data e ora dipendono da F-006 |
| F-005 | SC-001 | Passo 6, AC-03, AC-04, AC-05 | Che cosa verificano i pagamenti? | Insieme di coppie (IUV, IUR) senza ordine, senza mancanti ne duplicati; totali come decimali a due cifre; contenuto: importo, esito, indice di trasferimento, giorno dell'esito | S-003 §7.1, §6.2, §6.3; S-002 §6.2, D-05 | supported (giorno dell'esito dipende da F-006) |
| F-006 | SC-001 | AC-02, AC-05 | Fuso e precisione? | Non deciso (QF-06); ipotesi di lavoro non vincolante. Fermo il requisito: nessuno spostamento del giorno di calendario | S-002 R-11, §9 | unresolved |
| F-007 | SC-001 | AC-07 | Qual e la revisione prevista nell'elenco? | Non deciso (QF-11); ipotesi di lavoro non vincolante: revisione 1 | S-002 §9 (QF-11) | unresolved |
| F-008 | SC-001 | AC-06, passo 3 | Tempo massimo di propagazione? | Non documentato (R-14, R-20, QF-03); ipotesi di lavoro non vincolante 10 s di lettura e 360 s di timeout | S-002 §9; S-003 §9.2 | unresolved |
| F-009 | SC-001 | Postcondizione 3 | Come si osserva che il flusso pubblicato non e piu modificabile ne cancellabile? | Nessun comportamento osservabile documentato; prove negative fuori perimetro | S-002 PO-B3, §1.4; S-003 RI-09 | unresolved |
| F-010 | SC-001 | Precondizioni 1-7 | Esistono controlli documentati? | Nessuno per le precondizioni di censimento e abilitazione (RI-15); la preparazione e un rilievo implementativo | S-003 RI-15, §8.6 | supported (come Given) |
| F-011 | SC-001 | Postcondizione 1 | Come si osserva che il flusso e conservato? | Solo indirettamente: l'esito positivo dell'invio e la successiva disponibilita nella modalita nuova; nessuna lettura diretta della modalita legacy documentata | S-002 §6.6; S-003 §7.2 | partial |
| F-012 | SC-002 … SC-005 | Passi 1 e 6, AC-03 … AC-05 | Quali dimensioni variano? | Esito (4 valori, "revocato" escluso), indice di trasferimento 1..5, numero di pagamenti (1, 3, 5), importi (0.01 … 999999.99) | S-002 §6.5; S-003 §8.4, §8.5 | supported |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |
| SC-001 | Precondizioni 1-7 | Given: precondizioni generali e flusso con identificativo mai usato e valido per entrambe le modalita | F-010 | Un Given per precondizione |
| SC-001 | Passi 1-2, postcondizione 1 | When il PSP invia il flusso con la modalita legacy; Then la piattaforma lo convalida, lo conserva e risponde con esito positivo | F-001, F-011 | Guardia di validita |
| SC-001 | Passi 3-4, AC-06, AC-07 | When l'EC consulta con la modalita nuova i flussi pubblicati del PSP; Then l'elenco contiene il flusso del PSP mittente con la revisione prevista entro il tempo massimo | F-002, F-003, F-007, F-008 | Passo 3 senza oracolo proprio |
| SC-001 | Passo 5, AC-01, AC-02 | When l'EC richiede il dettaglio; Then lo riceve; And identificativo, date | F-004, F-006 | Stessa operazione |
| SC-001 | Passo 6, AC-03 … AC-05 | When l'EC richiede i pagamenti; Then li ottiene tutti; And totali, tutti e soli, contenuto | F-005, F-006 | Stessa operazione |
| SC-001 | Postcondizione 3 | Nessuna verifica | F-009 | Q-003 |
| SC-002 … SC-005 | Come SC-001 | Stessa struttura con valori diversi | F-012 | Righe di un solo outline |

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |
| O-001 | SC-001 … SC-005 | AC-01 | Identificativo recuperato uguale all'inviato | not-applicable | F-004 | supported |
| O-002 | SC-001 … SC-005 | AC-02 | Data e ora e giorno di regolamento uguali, senza spostamento; fuso e precisione da definire | not-applicable | F-006 | unresolved |
| O-003 | SC-001 … SC-005 | AC-03 | Numero e importo dichiarati uguali agli inviati e ai ricostruiti dai pagamenti | not-applicable | F-005 | supported |
| O-004 | SC-001 … SC-005 | AC-04 | Coppie (IUV, IUR) recuperate = inviate | not-applicable | F-005 | supported |
| O-005 | SC-001 … SC-005 | AC-05 (importo, esito, indice) | Contenuto uguale per ogni pagamento | not-applicable | F-005 | supported |
| O-006 | SC-001 … SC-005 | AC-05 (giorno dell'esito) | Giorno dell'esito uguale; fuso da definire | not-applicable | F-006 | unresolved |
| O-007 | SC-001 … SC-005 | AC-06 | Flusso disponibile nella modalita nuova entro il tempo massimo dalla conferma dell'invio; T non definito | maximum | F-002, F-008 | unresolved |
| O-008 | SC-001 … SC-005 | AC-07 (flusso e PSP) | L'elenco contiene il flusso associato al PSP mittente | not-applicable | F-003 | supported |
| O-009 | SC-001 … SC-005 | AC-07 (revisione) | Revisione prevista; valore non deciso | not-applicable | F-007 | unresolved |
| O-010 | SC-001 … SC-005 | Postcondizione 1 | Flusso conservato: esito positivo dell'invio, prova solo indiretta | not-applicable | F-001, F-011 | supported (parziale) |
| O-011 | SC-001 … SC-005 | Postcondizione 2 | Flusso pubblicato e leggibile dall'EC, completo ed equivalente: O-001 … O-009 | not-applicable | F-003, F-004, F-005 | supported (per le parti non soggette a F-006, F-007, F-008) |
| O-012 | SC-001 … SC-005 | Postcondizione 3 | Nessun esito osservabile documentato | not-applicable | F-009 | unresolved |

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |
| D-001 | SC-001, SC-004 | Numero di pagamenti (VAR-04) | Intero da 1; valori 1, 3, 5; uguale al numero di elementi delle altre liste | Nessuno | F-012 |
| D-002 | SC-001, SC-005 | Importo di ciascun pagamento (VAR-05) | Due decimali esatti; totale = somma; un valore per pagamento | Nessuno | F-012 |
| D-003 | SC-001, SC-002 | Esito di ciascun pagamento (VAR-02) | Quattro esiti ammessi, "revocato" non ammesso | Nessuno | F-012 |
| D-004 | SC-001, SC-003 | Indice di trasferimento (VAR-03) | Intero da 1 a 5 | Nessuno | F-012 |

Valori non promossi a D (fissati o generati dall'implementazione): identificativo del flusso (unico per run), date, IUV, IUR, indici di posizione, mittente e destinatario, identita, credenziali, tempi di lettura.

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | SC-001 … SC-005 | Tempo massimo T di propagazione (QF-03) | Nessuna decisione ricevuta | open |
| Q-002 | SC-001 … SC-005 | Fuso e precisione di istanti e giorni (QF-06) | Nessuna decisione ricevuta | open |
| Q-003 | SC-001 … SC-005 | Postcondizione 3: oracolo osservabile o conferma di non copertura | Nessuna decisione ricevuta | open |
| Q-004 | Nessuno | Approvazione della mappa dei riferimenti (S-005) | Nessuna decisione ricevuta | pending-approval |
| Q-005 | SC-001 … SC-005 | Revisione prevista nell'elenco FDR3 (QF-11, AC-07) | Nessuna decisione ricevuta | open |

## Readiness
Stato: `incomplete`. Percorso di successo supportato per i passi 1-6, AC-01, AC-03, AC-04 e parte flusso e PSP di AC-07. Copertura parziale: AC-02 e giorno dell'esito di AC-05 (Q-002); AC-06 (Q-001); revisione di AC-07 (Q-005); postcondizione 1 (prova indiretta); postcondizione 2 di conseguenza. Postcondizione 3 non coperta (Q-003). Nessuna esecuzione e nessuna chiamata all'ambiente.

Rilievo implementativo: Precondizioni 1, 2, 3, 5, 7; nessun controllo documentato (S-003 RI-15); proposta: decidere in implementazione come accertarle o prepararle; non soddisfatte, il test e non valido, non fallito.
Rilievo implementativo: Passi 1-2, guardia VG-B1; esito non positivo dell'invio non e un AC fallito; proposta: esito "non valido" (S-003 §7.2, RI-22), senza retry della scrittura (RI-07).
Rilievo implementativo: Passi 3-4, AC-06; T e cadenza non documentati; proposta: parametri configurabili (ipotesi 10 s e 360 s, S-003 §9.2) senza presentarli come garanzia; registrare il tempo osservato.
Rilievo implementativo: Passi 1, 4-6; endpoint SOAP e REST, credenziali, abilitazioni e conoscenza di PSP ed EC da parte della modalita nuova da accertare (DM-01, DM-02, DM-03, DM-13, DM-14); proposta: configurazione per ambiente (S-004).
Rilievo implementativo: Passo 1; valori generati o fissi (identificativo unico entro 35 caratteri, date, IUV, IUR, indici di posizione); proposta: generatori e Decimal come da S-003 §8, RI-05, RI-06.
Rilievo implementativo: Esecuzione; collocazione e tag di selezione della suite, registrazione, gruppo di risorsa condiviso, esecuzione sequenziale (S-003 §11, RI-10); il tag di selezione non e nel profilo Gherkin e non e stato aggiunto.
