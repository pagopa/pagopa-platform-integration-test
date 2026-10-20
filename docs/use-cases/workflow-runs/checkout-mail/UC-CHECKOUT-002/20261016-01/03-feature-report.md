---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
task_id: "checkout-mail"
uc_id: "UC-CHECKOUT-002"
run_id: "20261016-01"
uc_input: "Allegato chat: UC-CHECKOUT-002 - Validazione sintattica dei campi mail.txt"
uc_revision: "1"
environment: uat
revision: 3
status: ready
updated_at: "2026-10-16T11:50:00+02:00"
inputs:
  - path: "docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/01-context.md"
    revision: 2
  - path: "docs/use-cases/workflow-runs/checkout-mail/UC-CHECKOUT-002/20261016-01/02-test-data.md"
    revision: 2
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |
| docs/use-cases/features/checkout/checkout-email-sintattica.feature | uc-to-feature | written |

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |
| SC-001 | Flusso principale 1, 2; Postcondizione/AC-01 | 2 Quando (inserimento nei due campi) + 1 Quando (click) + 1 Allora (avanzamento) | F-001, F-002, F-003, F-009 | Due campi distinti restano due step When separati: ciascuno può essere sede di un'anomalia indipendente (EF-01/02 vs EF-03/04/05/06) |
| SC-002 | Flusso principale 1 sostituito da EF-01; AC-03 | 1 Quando (digitazione non valida) + 1 Allora (errore in tempo reale) + 1 Quando (click) + 2 Allora/E (persistenza errore, mancato avanzamento) | F-003, F-004, F-005 | Verifica intermedia (errore in tempo reale) richiesta da F-004 prima del tentativo di click richiesto da AC-03 (F-005) |
| SC-003 | Flusso principale 1 sostituito da EF-02; AC-02; AC-03 | 1 Quando (digitazione) + 1 Allora (errore generico durante la digitazione) + 1 Quando (click) + 1 Allora (persistenza dell'errore generico) + 1 E (warning specifico, in aggiunta all'errore) + 1 E (mancato avanzamento), parametrizzati in Esempi | F-003, F-004, F-005, F-006 | Due pattern di sintassi (assenza di "@"; assenza di parte dopo "@") condividono lo stesso comportamento e le stesse verifiche: un solo Schema dello scenario; errore e warning coesistono per risposta umana a Q-001 (S-004 in 01-context.md) |
| SC-004 | Flusso principale 1 (valido); Flusso principale 2 sostituito da EF-03; AC-03 | 1 Quando (inserimento valido passo 1) + 1 E (digitazione non valida passo 2) + 1 Allora (errore in tempo reale) + 1 Quando (click) + 2 Allora/E | F-002, F-003, F-004, F-005 | Il passo 1 valido è un'azione del flusso principale (When), non una precondizione, perché EF-03 presuppone che sia già avvenuta nello stesso scenario |
| SC-005 | Flusso principale 1 (valido); Flusso principale 2 sostituito da EF-04; AC-02; AC-03 | 1 Quando + 1 E (digitazione) + 1 Allora (errore generico durante la digitazione) + 1 Quando (click) + 1 Allora (persistenza dell'errore generico) + 1 E (warning specifico, in aggiunta all'errore) + 1 E (mancato avanzamento), parametrizzati in Esempi | F-002, F-003, F-004, F-005, F-006 | Stesso comportamento e stesse verifiche per i due pattern: un solo Schema dello scenario; errore e warning coesistono per risposta umana a Q-001 (S-004 in 01-context.md) |
| SC-006 | Flusso principale 1 (valido); Flusso principale 2 sostituito da EF-05/EF-06; AC-03; AC-04 | 1 Quando + 1 E (digitazione indirizzo diverso) + 1 Allora (errore di mancata coincidenza durante la digitazione) + 1 Quando (click) + 1 Allora (persistenza esplicita del messaggio di errore, AC-03) + 1 E (nessuna azione osservabile, AC-04) + 1 E (mancato avanzamento) | F-002, F-007, F-008 | EF-05 ed EF-06 sono la stessa anomalia osservata da due angolazioni compatibili: un solo scenario, con un'asserzione Then dedicata e distinta per la persistenza del messaggio (AC-03) e una per l'assenza di azione (AC-04) |

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |
| Flusso principale 1-2 | SC-001 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Inserimento di un indirizzo email sintatticamente valido e coincidente nei due campi | not-applicable | covered |
| Postcondizione | SC-001 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Inserimento di un indirizzo email sintatticamente valido e coincidente nei due campi | not-applicable | covered, la postcondizione è osservata direttamente tramite la navigazione alla pagina di scelta del metodo di pagamento, senza richiedere uno stato interno non esposto dallo UC |
| AC-01 | SC-001 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Inserimento di un indirizzo email sintatticamente valido e coincidente nei due campi | not-applicable | covered |
| EF-01 | SC-002 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Indirizzo email sintatticamente non valido al passo 1 | not-applicable | covered |
| EF-02 | SC-003 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Tentativo di proseguire con un indirizzo email malformato in un pattern specifico al passo 1 | riga 1 (assenza di "@"); riga 2 (assenza di parte dopo "@") | covered |
| EF-03 | SC-004 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Indirizzo email sintatticamente non valido al passo 2 | not-applicable | covered |
| EF-04 | SC-005 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Tentativo di proseguire con un indirizzo email di conferma malformato in un pattern specifico al passo 2 | riga 1 (assenza di "@"); riga 2 (assenza di parte dopo "@") | covered |
| EF-05 | SC-006 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Inserimento al passo 2 di un indirizzo email valido ma diverso da quello del passo 1 | not-applicable | covered |
| EF-06 | SC-006 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Inserimento al passo 2 di un indirizzo email valido ma diverso da quello del passo 1 | not-applicable | covered |
| AC-02 | SC-003, SC-005 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | (idem) | tutte le righe di entrambi gli Schemi | covered, conforme al chiarimento umano S-004 su Q-001: il warning compare in aggiunta all'errore generico persistente, non in sua sostituzione |
| AC-03 | SC-002, SC-003, SC-004, SC-005, SC-006 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | (idem) | not-applicable per SC-002/SC-004/SC-006; tutte le righe di entrambi gli Schemi per SC-003/SC-005 | covered, conforme al chiarimento umano S-004 su Q-001: l'errore generico resta visibile al click anche nei due pattern di EF-02/EF-04 |
| AC-04 | SC-006 | docs/use-cases/features/checkout/checkout-email-sintattica.feature | Inserimento al passo 2 di un indirizzo email valido ma diverso da quello del passo 1 | not-applicable | covered |

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |
| SC-001 | C-001 | D-001 | O-006 | `mario.rossi@esempio-test.it` (entrambi i campi) |
| SC-002 | C-002 | D-002 | O-001 | `mario.rossi@esempiotest` |
| SC-003 | C-003, C-004 | D-003, D-004 | O-001, O-003, O-004 | `mariorossiesempiotest.it`; `mario.rossi@` |
| SC-004 | C-005 | D-001, D-002 | O-001 | `mario.rossi@esempio-test.it` (passo 1); `mario.rossi@esempiotest` (passo 2) |
| SC-005 | C-006, C-007 | D-001, D-003, D-004 | O-001, O-003, O-004 | `mario.rossi@esempio-test.it` (passo 1); `mariorossiesempiotest.it` / `mario.rossi@` (passo 2) |
| SC-006 | C-008 | D-001, D-005 | O-002, O-005 | `mario.rossi@esempio-test.it` (passo 1); `luigi.verdi@esempio-test.it` (passo 2) |

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |
| Q-001 | SC-002, SC-003, SC-004, SC-005 | Ripartizione tra l'errore generico persistente al click (AC-03/EF-01/EF-03) e il warning specifico al click (EF-02/EF-04) per i pattern di sintassi non valida diversi da "assenza di @" e "assenza di parte dopo @"; chiarita con risposta esplicita dell'utente (S-004 in 01-context.md): l'errore generico resta sempre visibile al click, il warning si aggiunge nei due pattern nominati senza sostituirlo | answered |

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |
| Parole chiave Gherkin italiane (Funzionalità, Contesto, Schema dello scenario, Quando, Allora, Esempi, E) | Esecuzione autorizzata `behave --lang-help it` e confronto manuale con il testo scritto | Conforme | Output del comando, confrontato riga per riga con le keyword usate nella feature |
| Indentazione e struttura secondo il profilo (`feature:0, scenario:2, steps:4, examples:4, table_rows:6`) | Lettura visiva del file scritto e confronto con `.github/profiles/gherkin.profile.yaml` | Conforme | File `checkout-email-sintattica.feature` e profilo letto |
| Presenza del tag `Feature` (`@checkout_email_sintattica_001`) e tag di scenario uno per riga all'indentazione di profilo (correzione di una violazione presente nella revisione precedente, dove tutti i tag erano su un'unica riga e mancava il tag di `Funzionalità`) | Lettura visiva del file riscritto | Conforme dopo correzione | File `checkout-email-sintattica.feature`, sezione tag di ciascuno scenario e tag `Feature` |
| Commento di tracciamento `#0123456789` prima della riga `# language: it` | Lettura visiva del file scritto | Conforme | Prime due righe del file |
| Regola "nessuna colonna Examples con un solo valore" | Analisi manuale delle tabelle Esempi di SC-003 e SC-005 (entrambe le colonne variano su due righe) | Conforme | Tabelle Esempi nella feature |
| Copertura di tutti gli elementi UC (FP, EF-01..EF-06, Postcondizione, AC-01..AC-04) | Compilazione manuale della tabella Coverage da 01-context.md e 02-test-data.md | Completa, nessuna riserva residua dopo la risposta umana a Q-001 (S-004) | Tabella Coverage sopra |
| Risoluzione dei riferimenti verbali di flusso negli AC (FP, EF-01..EF-06) | Applicazione manuale delle regole di `ac-flow-references.md` (nessun riferimento esplicito presente nello UC fornito; applicabilità dedotta dal significato funzionale, come previsto per l'assenza di riferimento) | Conforme | AC-01..AC-04 nello UC, nessun riferimento verbale esplicito presente |

| Rivalidazione dopo `02-test-data.md` revisione 2 (correzione dell'`inputs` di contesto da revisione 1 a revisione 2) | Lettura reale di `02-test-data.md` revisione 2 e di `01-context.md` revisione 2; confronto riga per riga di Data resolution, Combinations (C-003/C-004/C-006/C-007) e Decisions con la feature già scritta | Conforme, nessuna modifica di contenuto richiesta: i valori D-001..D-005, gli oracle O-001..O-006 e il testo degli step erano già coerenti con la coesistenza errore/warning di Q-001; aggiornata solo la relazione evidenza nel report dati, non i valori applicati | `02-test-data.md` rev 2 (Combinations, Decisions), `01-context.md` rev 2 (F-004, F-005, F-006, O-001, O-003, O-004), feature `checkout-email-sintattica.feature` (step invariati) |

Nessun parser automatico, step Python o esecuzione `behave` della suite è stato eseguito;
i controlli sopra sono verifiche statiche manuali eseguite dall'analista.

## Engineer handoff
Sei scenari in un unico file, con `Contesto` condiviso (pagina email, lingua italiana).

1. **SC-001** (`@checkout_email_sintattica_001_01`): percorso positivo, stesso indirizzo
   nei due campi, verifica l'avanzamento alla pagina di scelta del metodo di pagamento.
2. **SC-002** (`_001_02`): sintassi non valida generica al passo 1. Verifica l'errore
   "Inserisci un indirizzo email valido" mostrato **durante la digitazione** (step `Quando
   l'utente digita...` seguito da un `Allora` esplicito "durante la digitazione", distinto
   volutamente da `inserisce` per segnalare la natura realtime del controllo), poi un
   secondo `Quando` per il click su Continua, con verifica che l'errore permanga e non
   ci sia avanzamento.
3. **SC-003** (`_001_03`): Schema dello scenario con 2 righe (assenza di "@"; assenza di
   parte dopo "@") al passo 1. Verifica, in ordine: l'errore generico mostrato **durante
   la digitazione** (stesso testo di SC-002, risposta umana a Q-001: l'errore generico si
   applica anche a questi due pattern); al click su Continua, la persistenza dello stesso
   errore generico **e** la comparsa aggiuntiva del warning specifico, testo esatto
   incluso (i due messaggi coesistono, il warning non sostituisce l'errore).
4. **SC-004** (`_001_04`): come SC-002 ma al passo 2, con un primo `Quando` che inserisce
   un indirizzo valido nel campo email (passo 1 del flusso principale) prima dell'anomalia.
5. **SC-005** (`_001_05`): come SC-003 ma al passo 2, con lo stesso passo 1 valido di
   precondizione funzionale e la stessa coesistenza errore/warning al click.
6. **SC-006** (`_001_06`): indirizzi validi ma diversi nei due campi: verifica l'errore
   di mancata coincidenza mostrato **durante la digitazione**, poi, al click su Continua,
   un'asserzione esplicita e distinta per la persistenza dello stesso messaggio di errore
   (AC-03) e una successiva per l'assenza di qualunque azione osservabile (AC-04 /
   EF-06), oltre al mancato avanzamento.

Nessun testo di step esistente è stato modificato rispetto all'implementazione (nessuno
step Python esiste ancora per questa feature): tutti gli step sono nuovi. Rispetto alla
revisione 1 di questo report sono stati aggiunti/modificati i seguenti step testuali, da
tenere a mente per la definizione degli step Python: un `Allora` esplicito "durante la
digitazione" subito dopo ogni `digita` dove prima c'era una verifica generica; negli
Schemi SC-003/SC-005, un `Allora` di persistenza dell'errore generico seguito da un `E`
per il warning (prima il warning era l'unica verifica al click); in SC-006, un `Allora`
di persistenza del messaggio di mancata coincidenza prima dell'`E` di assenza di azione.
L'uso distinto di "inserisce" (azione completata, senza verifica in tempo reale richiesta
in quel punto) e "digita" (azione la cui verifica in tempo reale è esplicitamente
richiesta subito dopo) resta intenzionale e va preservato nell'implementazione: non
unificare i due verbi in un'unica step definition che ignori questa distinzione.

Q-001 è stata risolta da una risposta umana esplicita (S-004 in 01-context.md): non
esiste più alcuna ripartizione esclusiva tra errore generico (EF-01/EF-03) e warning
specifico (EF-02/EF-04); l'errore generico persiste sempre al click e, nei due pattern
nominati, il warning compare in aggiunta. Non è richiesta ulteriore conferma prima
dell'implementazione per questo punto.

## Readiness
`pronta per lo sviluppo`. Motivi:
- Q-001 è stata risolta con risposta umana esplicita (S-004 in 01-context.md): l'errore
  generico persiste sempre al click; nei due pattern nominati di EF-02/EF-04 il warning
  specifico compare in aggiunta, senza sostituirlo. Nessuna ripartizione interpretativa
  residua tra errore e warning.
- Tutti i dati sono sintetici con evidenza di disponibilità `documented-not-checked`
  (nessuna verifica di ambiente live svolta), coerentemente con l'autorizzazione
  ricevuta per dati di solo inserimento campo.
- La correttezza sintattica Gherkin verificata manualmente non implica step Python
  implementati, ambiente disponibile o test eseguiti: non è permesso di implementazione
  o esecuzione automatica.
- Rivalidato dopo la correzione di `02-test-data.md` (passato a revisione 2 per
  allineare il proprio `inputs` a `01-context.md` revisione 2, invalidazione dovuta alla
  sola dipendenza stale, senza variazione dei valori D-001..D-005): la feature non
  richiede modifiche di contenuto; questo report passa a revisione 3 con `inputs`
  aggiornati a contesto revisione 2 e dati revisione 2.
