---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
task_id: "back-navigation-control"
uc_id: "UC-CHECKOUT-003"
run_id: "20261020-01"
uc_input: "C:\\Users\\dquero\\Downloads\\UC-CHECKOUT-003 - Back Navigation Control.txt"
uc_revision: "1"
environment: uat
revision: 2
status: incomplete
updated_at: "2026-10-20T10:54:20+02:00"
inputs:
  - path: "docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01/01-context.md"
    revision: 2
  - path: "docs/use-cases/workflow-runs/back-navigation-control/UC-CHECKOUT-003/20261020-01/02-test-data.md"
    revision: 2
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |
| docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | uc-to-feature | written |

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |
| SC-001..SC-006 | Precondizioni | `Dato che la pagina di checkout è aperta` / `E la lingua impostata è l'italiano` (Contesto condiviso) | F-001 | Precondizioni comuni a tutte le righe, spostate in `Contesto` secondo la mappatura UC→Gherkin |
| SC-001..SC-006 | FP step 1 | `Quando l'utente accede alla pagina "<pagina_iniziale>"` | F-001..F-007 | Azione unica dell'attore; nessuna sotto-azione produce un esito osservabile intermedio da verificare separatamente per questo UC |
| SC-001..SC-006 | FP step 2 | `E l'utente preme una sola volta il pulsante "Indietro"` | F-001 | Azione singola, esplicitamente vincolata a una sola pressione dallo UC |
| SC-001..SC-006 | AC-01, Postcondizioni | `Allora l'utente si trova nella pagina "<pagina_precedente>"` | O-001 | Un solo esito osservabile verificabile tramite l'interfaccia (pagina corrente) |
| SC-002..SC-006 | Stato di partenza necessario per raggiungere `<pagina_iniziale>` | `Dato che <contesto>` (parametro di riga) | D-001..D-008 (per riga, vedi Data and oracles) | Predisposizione di sessione/dati, non un comportamento sotto test di questo UC; nessun accesso diretto a pagina profonda ipotizzato |
| SC-001..SC-006 | Varianti di dati dello stesso flusso (nessuna AF dedicata) | `Schema dello scenario` con `Esempi` (6 righe) | F-001..F-007 | Stesso comportamento e stesse verifiche (FP + AC-01) per tutte le righe; raggruppate in un unico outline senza prodotto cartesiano |

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |
| Precondizioni | SC-001..SC-006 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | not-applicable (Contesto) | covered |
| FP step 1-2, AC-01, Postcondizioni | SC-001 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | riga `inserisci-dati-avviso` | covered |
| FP step 1-2, AC-01, Postcondizioni | SC-002 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | riga `dati-pagamento` | covered |
| FP step 1-2, AC-01, Postcondizioni | SC-003 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | riga `inserisci-email` | covered |
| FP step 1-2, AC-01, Postcondizioni | SC-004 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | riga `inserisci-carta` | covered |
| FP step 1-2, AC-01, Postcondizioni | SC-005 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | riga `lista-psp` → `inserisci-carta` (SC-005, ramo carta) | covered |
| FP step 1-2, AC-01, Postcondizioni | SC-006 | docs/use-cases/features/checkout/FEAT_003_Checkout_Back_Navigation.feature | L'utente torna alla pagina precedente dopo una singola pressione del pulsante Indietro | riga `lista-psp` → `scegli-metodo` (SC-006, campione rappresentante PayPal; Apple Pay/BANCOMAT Pay/MyBank dichiarati equivalenti dalla fonte, non campionati singolarmente) | covered |
| Flussi alternativi (AF) | — | — | — | not-applicable | uncovered, nessuna AF definita nello UC (sezione vuota; nessuna AF inventata) |
| Eccezioni (EF) | — | — | — | not-applicable | uncovered, nessuna EF definita nello UC (sezione vuota; nessuna EF inventata) |
| Pagina `scegli-metodo` (pulsante Indietro generico) | — | — | — | not-applicable | uncovered, nessun pulsante "Indietro" documentato per questa pagina (01-context.md#F-008) |
| Pagina `riepilogo-pagamento` (pulsante Indietro generico) | — | — | — | not-applicable | uncovered, documentati solo i pulsanti "modifica" e "Annulla", non un pulsante "Indietro" generico (01-context.md#F-009) |
| Ramo Google Pay (e flussi dichiarati identici: Conto iConto, Intesa Sanpaolo, Fabrik Pay By Bank, Klarna) | — | — | — | not-applicable | uncovered, nessun pulsante "Indietro" generico documentato da `riepilogo-pagamento` per questo ramo (01-context.md#F-010) |
| Comando "indietro" nativo del browser (vs pulsante UI) | — | — | — | not-applicable | uncovered, lo UC non lo distingue dal pulsante UI; solo i pulsanti UI documentati hanno evidenza supportata (01-context.md#F-011) |

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |
| SC-001 | not-applicable | — | O-001 | Valore letterale `"home"`; nessun dato irrisolto |
| SC-002 | C-001 | D-001, D-002 | O-001 | `302124502198375901`, `77777777777` (risolti; disponibilita' live non verificata) |
| SC-003 | C-002 | D-001, D-002 | O-001 | `302124502198375901`, `77777777777` (risolti; disponibilita' live non verificata) |
| SC-004 | C-003 | D-001, D-002, D-003, D-004 | O-001 | `302124502198375901`, `77777777777`, `email@email.it`, `email@email.it` (risolti; disponibilita' live non verificata per D-001/D-002) |
| SC-005 | C-004 | D-001, D-002, D-003, D-004, D-005, D-006, D-007, D-008 | O-001 | `302124502198375901`, `77777777777`, `email@email.it`, `email@email.it` (risolti, disponibilita' live non verificata), `__TODO_D005__`..`__TODO_D008__` (irrisolti) |
| SC-006 | C-005 | D-001, D-002, D-003, D-004 | O-001 | `302124502198375901`, `77777777777`, `email@email.it`, `email@email.it` (risolti; disponibilita' live non verificata; riga campione rappresentante PayPal) |

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |
| Q-001 | SC-002, SC-003, SC-004, SC-005, SC-006 | Uso dei valori sintetici di "Note per gli sviluppatori.md" per D-001/D-003/D-004 (D-002 riconosciuto come valore direttamente fornito, non necessitava approvazione) | answered (approvato: RETTIFICA rispetto alla precedente registrazione erronea "declined" — nessun umano aveva mai negato l'autorizzazione, era solo assenza di permesso; D-001/D-003/D-004 ora risolti con valore concreto, disponibilita' live non verificata) |

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |
| Identita'/revisioni degli input a monte | Lettura effettiva dei frontmatter di 00-run.md (rev 5), 01-context.md (rev 2), 02-test-data.md (rev 2); confronto task_id/uc_id/run_id/uc_revision/environment | pass | Frontmatter coincidenti su tutti e tre i file (`uc_revision: "1"`, `environment: uat`) |
| Keyword Gherkin italiane | Riutilizzato l'esito gia' verificato nella revisione precedente (comando `behave --lang-help it`, unico comando terminale autorizzato alla persona, eseguito in 00-run.md rev 1); nessun nuovo comando terminale eseguito in questa revisione, poiche' nessuna keyword e' stata modificata | pass | Confermati in precedenza: Funzionalità (Feature), Contesto (Background), Schema dello scenario (Scenario Outline), Esempi (Examples), Dato/Data/Dati/Date (Given), Quando (When), Allora (Then), E (And); "Dato che" usa keyword "Dato" + testo "che ..." |
| Formato nome file vs profilo | Confronto manuale con il regex `^FEAT_\d{3}_{{SUITE}}_[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*\.feature$` | pass | `FEAT_003_Checkout_Back_Navigation.feature` con SUITE=`Checkout` (invariato) |
| Commento di tracciamento | Confronto manuale con il formato `#<10-digit-number>` | pass | `#0123456789` (10 cifre) sulla prima riga, prima della dichiarazione di lingua (invariato) |
| Colonne Examples non costanti | Lettura manuale della tabella Esempi | pass | `pagina_iniziale` 5 valori distinti su 6 righe (`lista-psp` ripetuto per SC-005/SC-006, disambiguato da `pagina_precedente` e `contesto`); `pagina_precedente` 5 valori distinti su 6 righe; `contesto` 6 valori distinti |
| Enum di stato/ammissione/idoneita'/disponibilita' | Confronto manuale con il vocabolario di uc-workflow.md | pass | Valori usati: `incomplete`, `provided`, `approved`, `pending-approval`, `declined`, `answered`, `fit`, `unverified`, `documented-not-checked`, `supported`, `unresolved` — tutti ammessi |
| Coerenza D-001/D-002/D-003/D-004 risolti con valore concreto e avvertenza di riga | Confronto manuale tra 02-test-data.md "Scenario warnings" e il commento sopra lo Scenario Outline nella feature | pass | Ogni riga SC-002..SC-006 riporta l'avvertenza su disponibilita' live non verificata; nessuna falsa disponibilita' dichiarata |
| Copertura dei TODO rimanenti (D-005..D-008) con avvertenza di riga | Confronto manuale tra 02-test-data.md "Scenario warnings" (SC-005) e il commento TODO sopra lo Scenario Outline | pass | D-005..D-008 compaiono nel commento, con indicazione della sola riga `lista-psp`→`inserisci-carta` interessata |
| Correzione scope D-003/D-004 per SC-003 | Confronto manuale tra 01-context.md rev 2 "Data requirements" e 02-test-data.md rev 2 "Data resolution"/"Combinations" | pass | SC-003 non compare piu' nello scope di D-003/D-004 in nessuno dei due report, ne' nella riga `inserisci-email` della feature |
| Campione rappresentante PayPal per SC-006 | Confronto manuale tra 01-context.md rev 2 Mapping e la riga `contesto` della feature per `lista-psp`→`scegli-metodo` | pass | Il metodo "PayPal" e' nominato esplicitamente; Apple Pay/BANCOMAT Pay/MyBank sono dichiarati equivalenti ma non campionati, nessuna implicazione di copertura per tutti e quattro |
| Eliminazione pagina pseudo-route con parentesi | Lettura manuale della colonna `pagina_iniziale` della tabella Esempi | pass | Nessuna riga contiene parentesi nel valore di `pagina_iniziale`; entrambe le righe `lista-psp` sono disambiguate da `pagina_precedente` e `contesto` |
| Rimozione precondizione non supportata "senza altri dati inseriti" | Confronto manuale tra 01-context.md#F-002 (nessuna menzione di questa restrizione) e la riga `inserisci-dati-avviso` della feature | pass | La riga ora riporta solo "l'utente si trova sulla home page del checkout" |
| Coerenza SC/AC/AF/EF in Coverage | Confronto manuale tra 00-run.md inventario SC-001..SC-006, UC AC-01/AF/EF e la tabella Coverage sopra | pass | Tutti gli SC coperti; AF/EF vuoti riportati come non applicabili; AC-01 coperto su tutte le righe |

## Engineer handoff

La feature contiene un `Contesto` condiviso (precondizioni dello UC: pagina di
checkout aperta, lingua italiana) e un unico `Schema dello scenario` con 6
righe in `Esempi`, una per ogni pulsante "Indietro" effettivamente documentato
nel materiale funzionale fornito. Ogni riga rappresenta un caso SC-NNN tracciato
nel registro (00-run.md) e nel contesto (01-context.md):

- `inserisci-dati-avviso` → `home` (SC-001): nessun dato di ingresso richiesto.
- `dati-pagamento` → `inserisci-dati-avviso` (SC-002): richiede un avviso di
  pagamento valido (`D-001`="302124502198375901", `D-002`="77777777777"),
  entrambi risolti; disponibilita'/recuperabilita' in ambiente live NON
  verificata (`documented-not-checked`).
- `inserisci-email` → `dati-pagamento` (SC-003): stesso requisito di SC-002,
  nessun dato email (accedere a `inserisci-email` precede l'inserimento
  dell'email stessa).
- `inserisci-carta` → `scegli-metodo` (SC-004): richiede anche un'email valida
  e la sua conferma (`D-003`/`D-004`="email@email.it", valore di esempio
  fornito dalla fonte ammessa).
- `lista-psp` → `inserisci-carta` (SC-005, ramo carta): richiede anche dati
  carta validi (`D-005`..`D-008`), rimasti `__TODO_Dxxx__`: nessuna fonte
  ammessa fornisce un valore concreto e nessuna generazione sintetica e'
  stata autorizzata per questi campi.
- `lista-psp` → `scegli-metodo` (SC-006, campione rappresentante PayPal):
  stesso requisito avviso+email di SC-004, nessun dato carta. Il metodo
  "PayPal" e' nominato esplicitamente come campione; Apple Pay, BANCOMAT Pay
  e MyBank sono dichiarati equivalenti dalla fonte ma non campionati
  singolarmente in questa riga.

Il valore di `pagina_iniziale` per le ultime due righe e' lo stesso
(`lista-psp`, non un nome di pagina con parentesi pseudo-route): le due righe
si disambiguano tramite `pagina_precedente` (`inserisci-carta` vs
`scegli-metodo`) e tramite il rispettivo `contesto`.

Nessun valore applicato e' dichiarato disponibile in ambiente live senza
verifica: D-001..D-004 sono concreti ma annotati come non verificati
(`documented-not-checked`); D-005..D-008 restano TODO. Entrambe le categorie
hanno la relativa avvertenza di riga nel commento sopra lo Schema dello
scenario.

## Readiness

Stato: `bozza`. SC-001..SC-004 e SC-006 hanno tutti i dati richiesti risolti
con valore concreto (D-001..D-004), ma la disponibilita'/recuperabilita' di
questi valori in ambiente `uat` non e' verificata (`documented-not-checked`):
la sintassi controllata non implica disponibilita' dell'ambiente ne'
esecuzione autorizzata. SC-005 resta bloccato dai dati carta mancanti
(D-005..D-008, nessuna fonte ammessa e nessuna autorizzazione sintetica).
Restano inoltre le lacune di copertura gia' riportate in 01-context.md: pagina
`scegli-metodo` (nessun pulsante "Indietro" generico documentato), pagina
`riepilogo-pagamento` (solo "modifica" e "Annulla" documentati), ramo Google
Pay ed equivalenti (nessun pulsante "Indietro" generico da `riepilogo-pagamento`
per questo ramo), e la distinzione pulsante UI "Indietro" vs comando nativo
"indietro" del browser (non posta dallo UC, non copribile con evidenza
supportata). Nessuna di queste lacune e' stata colmata per inferenza: restano
copertura parziale esplicita, non un'approvazione di ambito.

Il passo `Dato che <contesto>` descrive la predisposizione di stato/sessione
necessaria per raggiungere la pagina iniziale della riga (mai un accesso
diretto a pagina profonda): l'implementazione Python dovrà tradurlo nella
sequenza di navigazione/dati reale, sostituendo i token `__TODO_Dxxx__` solo
quando i valori saranno disponibili e ammessi. Il passo `Quando l'utente
accede alla pagina "<pagina_iniziale>"` rappresenta l'azione effettiva di
navigazione (inclusa, per le righe con dati, la sottomissione dei dati gia'
predisposti), mentre `E l'utente preme una sola volta il pulsante "Indietro"`
e `Allora l'utente si trova nella pagina "<pagina_precedente>"` implementano
rispettivamente FP step 2 e AC-01/Postcondizioni.

Nessun testo di step e' stato modificato rispetto ad una versione precedente:
e' la prima persistenza di questa feature in questa run.

Il commento TODO sopra lo Scenario Outline elenca tutti gli D-id irrisolti con
le righe interessate: nessuna riga e' eseguibile finche' D-001..D-008 non
sono risolti con valori ammessi e idonei. La riga `inserisci-dati-avviso` →
`home` non ha dati irrisolti ma resta comunque parte di una bozza complessiva.

## Readiness

`bozza`. Motivi:

- Requisiti dati aperti: D-001..D-008 sono tutti `__TODO_Dxxx__` (02-test-data.md,
  stato `incomplete`); nessun valore e' stato ammesso per questo UC (uso di
  dati sintetici dichiarato non autorizzato, Q-001).
- Lacune funzionali esplicite e non invenzioni: pagina `scegli-metodo` priva di
  pulsante Indietro documentato; pagina `riepilogo-pagamento` con soli pulsanti
  "modifica"/"Annulla"; ramo Google Pay (e flussi identici dichiarati: Conto
  iConto, Intesa Sanpaolo, Fabrik Pay By Bank, Klarna) privo di pulsante
  Indietro generico documentato da `riepilogo-pagamento`; distinzione tra
  pulsante UI "Indietro" e comando nativo "indietro" del browser assente nello
  UC, quindi non coperta.
- Le sezioni AF/EF dello UC sono vuote: nessun flusso alternativo o eccezione
  e' stato inventato per colmarle.

Nessun elemento supportato (SC-001..SC-006, AC-01) presenta ambiguita' o
conflitto bloccante. La sintassi Gherkin e' stata controllata staticamente
(vedi Checks) ma questo non costituisce esecuzione, disponibilita' di ambiente
o implementazione degli step Python: la feature non e' pronta per lo sviluppo
o l'esecuzione finche' i dati e le lacune sopra elencate non sono risolti.
