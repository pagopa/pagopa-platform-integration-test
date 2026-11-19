---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: "fdr-e2e-ibrido"
uc_id: "UC-FDR-001"
run_id: "20261119-01"
uc_input: "docs/use-cases/UC-FDR-001-v3.md"
uc_revision: "v3"
environment: uat
revision: 1
status: incomplete
updated_at: "2026-11-19T09:58:00+01:00"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |
| S-001 | docs/use-cases/UC-FDR-001-v3.md | intero UC (precondizioni, passi 1-9, postcondizioni, AC-01 … AC-08) | 2026-11-19 | UAT, v3 | provided | Richiesta all'analista, 2026-11-19 |
| S-002 | docs/fdr-e2e-ibrido-01-razionale-uc-v3.md | §1.4, §1.5 (D-01 … D-10), §4 (R-01 … R-20), §6, §6.5, §6.6, §7, §9 | 2026-11-19 | UAT, v3 | provided | Richiesta all'analista, 2026-11-19 |
| S-003 | docs/fdr-e2e-ibrido-02-dati-tecnici-v3.md | §3.1, §3.2, §4.2, §4.4, §5, §6, §7.1, §7.2, §8, §9, §12 | 2026-11-19 | UAT, contratti SANP3.13.0 (commit 969833a) | provided | Richiesta all'analista, 2026-11-19 |
| S-004 | README.md | Configurazione > E2E test; Suite disponibili > End-to-end; Esecuzione locale > E2E; Contribuire > Convenzioni Gherkin | 2026-11-19 | repository | unknown | Uso solo operativo (suite e2e, selezione ambiente, convenzioni); nessun valore o requisito funzionale ne deriva |
| S-005 | docs/use-cases/mappa-riferimenti-UC-FDR-v3.md | letta per orientamento, non usata come evidenza | 2026-11-19 | v3 | pending-approval | Q-004 |

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | SC-001 | Passi 1-6 | Quali esiti osservabili hanno creazione, aggiunta dei pagamenti e pubblicazione? | Il PSP esegue le tre fasi con la modalita nuova; ciascuna ha un esito osservabile: creazione in bozza (201), aggiunta dei pagamenti (200), pubblicazione (200, 400 se i totali non coincidono). Sono le guardie VG-A1: se non soddisfatte il test e non valido e termina senza attendere la propagazione | S-003 §3.1, §7.2; S-002 §6.6 | supported |
| F-002 | SC-001 | Passo 6, postcondizione 1 | Come si osserva che il flusso e pubblicato, alla prima revisione, con totali coerenti? | Lettura del flusso pubblicato dal lato PSP: stato pubblicato, revisione 1, totali calcolati uguali ai dichiarati (VG-A2) | S-003 §3.1, §7.2; S-002 §6.6 | supported |
| F-003 | SC-001 | Passo 7 | Il passo 7 ha un oracolo proprio? | No: la propagazione e asincrona e non ha oracolo proprio; si osserva con la lettura ripetuta dell'elenco legacy dell'EC (solo letture; "non ancora disponibile" si ritenta, gli errori veri interrompono) | S-003 §7.1 (nota finale), §9.1, §9.3; S-002 R-14 | supported |
| F-004 | SC-001 | Passo 8, AC-07 | Che cosa deve contenere l'elenco consultato dall'EC? | Una voce con identificativo del flusso uguale a quello pubblicato e data e ora uguale a quella pubblicata; il flusso si riconosce per uguaglianza esatta dell'identificativo, mai per conteggio | S-003 §7.1 (AC-A3), §3.3; S-002 §6.2 | supported (parte identificativo); la parte data e ora dipende da F-008 |
| F-005 | SC-001 | Passo 9, AC-08 | Che cosa riceve l'EC e come si verifica il formato? | Il documento XML completo, decodificato e validato contro lo schema XSD della modalita legacy (FlussoRiversamento_1_0_5.xsd) | S-003 §4.2, §4.4, §7.1 (AC-A4); S-002 D-09 | supported |
| F-006 | SC-001 | AC-01, AC-03, AC-04, AC-05 | Con quali regole si confrontano identificativo, totali, pagamenti e contenuto dei pagamenti? | Identificativo: uguaglianza esatta. Totali: numero e importo dichiarati uguali a quelli pubblicati e a quelli ricostruiti dai pagamenti, come decimali a due cifre. Pagamenti: insieme di coppie (IUV, IUR) senza ordine, senza mancanti ne duplicati. Contenuto: importo, esito, indice di trasferimento (e giorno dell'esito, vedi F-008) | S-003 §7.1 (AC-C1, AC-C5, AC-C6, AC-C7), §6.2, §6.3; S-002 §6.2, D-05 | supported |
| F-007 | SC-001 | AC-06, passo 7 | Qual e il tempo massimo di propagazione? | Non documentato (R-14, R-20). Il documento tecnico propone, solo come ipotesi di lavoro non vincolante, lettura ogni 10 secondi e timeout di 360 secondi | S-002 R-14, R-20, §6.3, §9 (QF-03); S-003 §9.2 | unresolved |
| F-008 | SC-001 | AC-02, AC-05 (giorno dell'esito), AC-07 (data e ora) | Con quale fuso e precisione si confrontano istanti e giorni? | Non deciso (QF-06). Ipotesi di lavoro non vincolante: istanti in UTC, XML senza offset letto come Europe/Rome, giorni come date, precisione al secondo. Resta fermo il requisito del UC: nessuno spostamento del giorno di calendario | S-002 R-11, §9 (QF-06); S-003 §6.4, §7.1 | unresolved |
| F-009 | SC-001 | Postcondizione 3 | Come si osserva che il flusso pubblicato non e piu modificabile ne cancellabile? | Nessun comportamento atteso osservabile e documentato: le fonti dicono solo che i dati di test restano nell'ambiente; le prove negative e le modifiche sono fuori perimetro | S-002 PO-A3, R-04, §1.4; S-003 RI-09 | unresolved |
| F-010 | SC-001 | Precondizioni 1-6 | Esiste un controllo documentato per ciascuna precondizione? | Nessun controllo documentato per PRE-C1, C3, C5; la verifica o preparazione e una questione implementativa (RI-15). Ogni precondizione resta un Given | S-003 RI-15, §8.6; S-002 §6.1 | supported (come Given); preparazione: Rilievo implementativo |
| F-011 | SC-002, SC-003, SC-004, SC-005 | Passi 3 e 6, AC-03 … AC-05 | Quali dimensioni dei dati variano a parita di flusso e di verifiche? | Esito del pagamento (4 valori ammessi, "revocato" escluso), indice di trasferimento (1..5), numero di pagamenti (1, 3, 5; in una sola richiesta di aggiunta, massimo 1000), importi (0.01, 10.00, 1234.56, 999999.99; totale = somma). Stessi passi e stesse verifiche | S-002 §6.5 (VAR-02 … VAR-05), R-05, R-08, R-10; S-003 §8.4, §8.5 | supported |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |
| SC-001 | Precondizioni 1-6 | Given: quattro precondizioni generali (censimento e abilitazione, credenziali, coppia gestita da FDR, servizi e conversione operativi) e il flusso con identificativo mai usato e valido per entrambe le modalita | F-010, F-011 | Ogni precondizione e un Given; la preparazione e un rilievo implementativo, non una lacuna |
| SC-001 | Passi 1-2 | When il PSP crea il flusso con la modalita nuova; Then la piattaforma lo crea in bozza | F-001 | L'esito puo interrompere il flusso (guardia): azione e verifica espliciti |
| SC-001 | Passi 3-4 | When il PSP aggiunge i pagamenti; Then la piattaforma li aggiunge alla bozza | F-001 | Come sopra |
| SC-001 | Passi 5-6, postcondizione 1 | When il PSP pubblica il flusso; Then conferma di pubblicazione e flusso pubblicato alla prima revisione con totali coerenti | F-001, F-002 | La conferma e l'istante da cui parte il tempo massimo (AC-06); la lettura lato PSP e l'osservabile della postcondizione 1 |
| SC-001 | Passo 7, passo 8, AC-06, AC-07 | When l'EC consulta con la modalita legacy i flussi del PSP; Then l'elenco contiene il flusso entro il tempo massimo previsto; And la voce riporta identificativo e data e ora uguali a quelli pubblicati | F-003, F-004, F-007, F-008 | Il passo 7 non ha oracolo proprio e si osserva dalla lettura ripetuta; il limite non e un valore del Gherkin finche T non e deciso |
| SC-001 | Passo 9, AC-01 … AC-05, AC-08, postcondizione 2 | When l'EC richiede il flusso individuato; Then lo riceve completo; And valido per XSD; And identificativo, date, totali, insieme dei pagamenti e contenuto dei pagamenti equivalenti a quelli pubblicati | F-005, F-006, F-008 | Verifiche compatibili della stessa operazione: un solo scenario, non uno per AC |
| SC-001 | Postcondizione 3 | Nessuna verifica: oracolo non documentato | F-009 | Non si inventa un controllo; resta Q-003 |
| SC-002 … SC-005 | Come SC-001 | Stessa struttura e stesse verifiche con valori diversi di esito, indice di trasferimento, numero di pagamenti e importi | F-011 | Variante di dati: righe di un solo outline |

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |
| O-001 | SC-001 … SC-005 | AC-01 | Identificativo del flusso ricevuto uguale (esatto) a quello pubblicato | not-applicable | F-006 | supported |
| O-002 | SC-001 … SC-005 | AC-02, AC-07 (data e ora) | Data e ora del flusso e giorno di regolamento uguali a quelli pubblicati, senza spostamento del giorno di calendario; fuso e precisione da definire | not-applicable | F-008 | unresolved |
| O-003 | SC-001 … SC-005 | AC-03 | Numero e importo totale dichiarati uguali a quelli pubblicati e a quelli ricostruiti dai pagamenti ricevuti | not-applicable | F-006 | supported |
| O-004 | SC-001 … SC-005 | AC-04 | Coppie (IUV, IUR) ricevute = coppie pubblicate, senza mancanti ne duplicati | not-applicable | F-006 | supported |
| O-005 | SC-001 … SC-005 | AC-05 (importo, esito, indice di trasferimento) | Per ogni coppia: importo uguale, esito corrispondente, indice di trasferimento uguale | not-applicable | F-006 | supported |
| O-006 | SC-001 … SC-005 | AC-05 (giorno dell'esito) | Giorno dell'esito uguale a quello pubblicato; fuso e precisione da definire | not-applicable | F-008 | unresolved |
| O-007 | SC-001 … SC-005 | AC-06 | Il flusso e disponibile all'EC nella modalita legacy entro il tempo massimo dalla conferma della pubblicazione; valore di T non definito | maximum | F-003, F-007 | unresolved |
| O-008 | SC-001 … SC-005 | AC-07 (identificativo) | L'elenco contiene una voce con identificativo uguale a quello pubblicato | not-applicable | F-004 | supported |
| O-009 | SC-001 … SC-005 | AC-08 | Il documento ricevuto e valido contro lo schema XSD della modalita legacy | not-applicable | F-005 | supported |
| O-010 | SC-001 … SC-005 | Postcondizione 1 | Flusso pubblicato alla prima revisione, con totali calcolati uguali ai dichiarati (lettura lato PSP) | not-applicable | F-002 | supported |
| O-011 | SC-001 … SC-005 | Postcondizione 2 | Flusso disponibile all'EC nella modalita legacy, completo e equivalente: e il complesso di O-001 … O-009 | not-applicable | F-004, F-005, F-006 | supported (per le parti non soggette a F-007 e F-008) |
| O-012 | SC-001 … SC-005 | Postcondizione 3 | Flusso non modificabile ne cancellabile: nessun esito osservabile documentato | not-applicable | F-009 | unresolved |

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |
| D-001 | SC-001, SC-004 | Numero di pagamenti del flusso (VAR-04) | Intero da 1; valori di lavoro 1, 3, 5; una sola richiesta di aggiunta (massimo 1000); uguale al numero di elementi delle liste degli altri parametri; il totale dichiarato e questo numero | Nessuno | F-011 |
| D-002 | SC-001, SC-005 | Importo di ciascun pagamento (VAR-05) | Due decimali esatti, da 0.01 a 999999999.99; l'importo totale dichiarato e la somma esatta; un valore per pagamento | Nessuno | F-011 |
| D-003 | SC-001, SC-002 | Esito di ciascun pagamento (VAR-02) | Uno dei quattro esiti ammessi (eseguito, eseguito in stand-in, eseguito in stand-in in assenza di RPT, eseguito in assenza di RPT); "revocato" non ammesso; un valore per pagamento | Nessuno | F-011 |
| D-004 | SC-001, SC-003 | Indice di trasferimento di ciascun pagamento (VAR-03) | Intero da 1 a 5; sempre presente; un valore per pagamento | Nessuno | F-011 |

Valori non promossi a D, perche il Python/Behave li puo fissare o generare e nessun esito dipende da essi: identificativo del flusso (unico per run, conforme a R-12), data e ora del flusso, data di regolamento, dati di mittente e destinatario, IUV, IUR, indice di posizione, data dell'esito, identita e credenziali di PSP ed EC, tempi di lettura. Sono rilievi implementativi (vedi Readiness).

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |
| Q-001 | SC-001 … SC-005 | Tempo massimo T di propagazione verso la modalita legacy (QF-03): valore, o criterio per fissarlo. Blocca la verifica quantitativa di AC-06 | Nessuna decisione ricevuta | open |
| Q-002 | SC-001 … SC-005 | Fuso e precisione con cui si confrontano istanti e giorni (QF-06). Blocca la parte temporale di AC-02, AC-05 e AC-07 | Nessuna decisione ricevuta | open |
| Q-003 | SC-001 … SC-005 | Postcondizione 3: quale esito osservabile attestare per "non piu modificabile ne cancellabile", o conferma che resti non verificata (le fonti la danno per fuori perimetro) | Nessuna decisione ricevuta | open |
| Q-004 | Nessuno | Approvazione della mappa dei riferimenti come fonte candidata (S-005); non usata come evidenza | Nessuna decisione ricevuta | pending-approval |

## Readiness
Stato: `incomplete`. Il percorso di successo e supportato per i passi 1-9, per AC-01, AC-03, AC-04, AC-08, per la parte identificativo di AC-07 e per le postcondizioni 1 e 2 (nelle parti non soggette a fuso e tempo massimo). Copertura parziale: AC-02, AC-05 (giorno dell'esito), AC-07 (data e ora) per Q-002; AC-06 per Q-001; postcondizione 2 di conseguenza. Postcondizione 3 non coperta (Q-003). Nessuna esecuzione, nessuna chiamata verso l'ambiente: tutto deriva dalla documentazione fornita.

Rilievo implementativo: Precondizioni 1, 2, 3, 5 del UC; non esiste un controllo documentato (S-003 RI-15); proposta: decidere in implementazione come accertarle o prepararle; una precondizione non soddisfatta rende il test non valido, non fallito.
Rilievo implementativo: Passi 1-6, guardie VG-A1 e VG-A2; una guardia non soddisfatta (esiti 201/200/200, stato pubblicato, revisione 1, totali calcolati = dichiarati) non e un AC fallito; proposta: esito distinto "non valido" (S-003 RI-22, §7.2), senza ritentare le scritture (RI-07).
Rilievo implementativo: Passo 8, AC-06; valore di T e cadenza di lettura non documentati; proposta: parametri configurabili (ipotesi di lavoro 10 s e 360 s, S-003 §9.2) senza presentarli come garanzia; registrare il tempo osservato (DM-08).
Rilievo implementativo: Passi 8-9; esiti applicativi della legacy (elenco vuoto, flusso non ancora disponibile, errori) non documentati (DM-04) e compressione dell'XML (DM-16); proposta: rilevarli alla prima esecuzione approvata e distinguere "non ancora disponibile" dagli errori veri (S-003 §9.3, RI-19).
Rilievo implementativo: Passo 1, 3, 9; indirizzi SOAP e dominio PSP, chiavi, password e abilitazioni (DM-01, DM-02, DM-03, DM-13, DM-14) da accertare prima di eseguire; proposta: risolverli da configurazione per ambiente (S-004: selettore dell'ambiente) senza fissare host negli step.
Rilievo implementativo: Passo 1, 3; valori generati o fissi non promossi a D (identificativo unico per run entro 35 caratteri, date, IUV, IUR, indici di posizione, mittente, destinatario); proposta: generatori e valori di base come da S-003 §8.1-§8.3, importi come Decimal (RI-05) e data dell'esito a mezzogiorno UTC (RI-06).
Rilievo implementativo: Esecuzione; selezione e collocazione della suite (src/e2e/fdr-hybrid, tag di selezione, registrazione e gruppo di risorsa condiviso con fdr3, esecuzione sequenziale) non definite nel README per questa suite; proposta: S-003 §11 e RI-10; il tag di selezione non e un'etichetta del profilo Gherkin e non e stato aggiunto alla feature.
