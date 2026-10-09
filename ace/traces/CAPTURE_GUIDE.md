# Come catturare una trace

**Automatico dal workflow dell'orchestratore** (se il wizard ha inserito
il passo dedicato — vedi
[INSTALL_PROMPT_EMBEDDED.md](../../INSTALL_PROMPT_EMBEDDED.md) o
[INSTALL_PROMPT_MEDIATED.md](../../INSTALL_PROMPT_MEDIATED.md), secondo la
modalità installata): in modalità embedded l'orchestratore partecipante genera
la trace; in modalità mediata lo fa soltanto il wrapper opt-in `-ace`, mai il
wrapper standard. La trace viene scritta come ultimo passo, subito dopo la
risposta. Se la tua
piattaforma non offre un hook di lifecycle nativo a cui agganciarsi (es.
chat interattiva senza eventi post-risposta), questa automazione è un
passo scritto esplicitamente nel prompt dell'orchestratore, non una
funzione della piattaforma. Limite noto di questo approccio: l'esito
(`outcome`) è auto-valutato subito dopo la risposta, **senza** aver visto
un'eventuale reazione successiva dell'utente — per questo queste trace
portano di norma il valore `evaluated_by` definito da
`provisional_evaluator` in
[ace/config/project.json](../config/project.json), es. `"acme-auto"`, un segnale più
debole (autovalutazione/self-report) di una conferma esterna. Il reflector
e `scripts/update_counters.js` pesano queste trace di conseguenza — vedi
["A fine task: quando usare `verified`"](#a-fine-task-quando-usare-verified)
e ["Prima di invocare il reflector (alla soglia)"](#prima-di-invocare-il-reflector-alla-soglia-giro-retrospettivo-sulle-trace-deboli)
più sotto.

Il resto di questa guida resta valido come **processo manuale di
fallback**: usalo se una trace auto-generata manca o è incompleta. Se
invece vuoi **correggere** l'esito di una trace già scritta con il senno
di poi (perché hai visto come l'utente ha reagito, o perché una verifica
successiva ha confermato/smentito il self-report originale), **non
sovrascrivere mai il file originale in place**: scrivi una trace di
correzione separata, come descritto in
["Prima di invocare il reflector (alla soglia)"](#prima-di-invocare-il-reflector-alla-soglia-giro-retrospettivo-sulle-trace-deboli)
più sotto — non aspettare comunque troppo a farlo, i dettagli si perdono
in fretta.

## Quando

Dopo ogni sessione completa del team (risposta in chat + eventuali
side-effect come salvataggio file o commit/push), prima di passare al
task successivo non correlato.

## Granularità: una trace per agente coinvolto

Il campo `agent` in [trace.schema.json](../schema/trace.schema.json) è
singolare: se la sessione ha coinvolto più subagenti, crea **una trace
per ciascun subagente effettivamente coinvolto**, più eventualmente una
per `orchestratore` se vuoi valutare anche l'orchestrazione
stessa (scelta dei subagenti, coerenza finale). Usa lo **stesso
`task_id`** per tutte le trace della stessa sessione, così il reflector
può correlarle in fase di batch.

## Dove salvarle

`ace/traces/<task_id>__<agent>.json`, es.
`ace/traces/2026-08-07-esempio-di-slug__<orchestrator_agent>.json`
(dove `<orchestrator_agent>` è il valore esatto di `orchestrator_agent` in
[ace/config/project.json](../config/project.json)).

## Come compilare i campi

- **task_id**: slug leggibile, es. `data-ISO + 2-3 parole della richiesta`.
- **agent**: il subagente, o l'agente orchestratore (il nome esatto in
  `orchestrator_agent`), a cui questa trace si riferisce. Deve combaciare
  con uno dei nomi in [ace/config/project.json](../config/project.json).
- **started_at / ended_at**: orari approssimativi della sessione, dai
  timestamp della chat.
- **request_summary**: parafrasi in una riga della richiesta originale
dell'utente (non incollare l'intera conversazione).
- **playbook_bullets_seen / playbook_bullets_cited**: array vuoti finché
i playbook restano vuoti — non c'è nulla da citare. Popolali solo
quando esisteranno bullet reali nel contesto servito.
- **actions**: sintesi delle azioni rilevanti (non il transcript
  verbatim) — es. "il subagente X ha proposto Y", "l'agente Z ha salvato
  il file W".
- **outcome.status**: `success` / `partial` / `failure`, in base a
  com'è andata realmente (l'utente ha corretto qualcosa? il file è stato
  salvato senza errori? l'informazione era accurata?).
- **outcome.evaluated_by**: se stai scrivendo questa trace come processo
  manuale di fallback (nessuna auto-generazione avvenuta), usa `"manual"`
  — vedi nota in cima a questo file. Se sei l'orchestratore a fine task e
  hai verificato concretamente l'esito contro un fatto controllabile
  (non solo un self-report immediato), vedi
  ["A fine task: quando usare `verified`"](#a-fine-task-quando-usare-verified)
  sotto prima di scegliere il valore.
- **notes**: qualunque osservazione libera utile al reflector futuro.
- **friction**: elenco di intoppi operativi incontrati durante
  l'esecuzione, anche se recuperati da solo e il task è comunque
  riuscito — es. comando lanciato dalla cartella sbagliata e poi
  ripetuto da quella corretta, tool/binario non disponibile e sostituito
  con un'alternativa, dipendenza mancante, retry necessario dopo un
  errore. Campo pensato apposta per il caso in cui `outcome.status` resta
  `success` ma qualcosa ha comunque intralciato il percorso: senza
  questo campo, quel tipo di attrito resta invisibile al reflector anche
  quando si ripete identico ad ogni sessione. **Obbligatorio, non
  opzionale**: `[]` è una risposta valida solo se hai verificato
  attivamente che non c'è stato nessun intoppo, non un default per
  pigrizia o omissione — stesso principio di `relation_to_existing: none`
  nel reflector.

## A fine task: quando usare `verified`

Oltre al `provisional_evaluator` configurato (self-report immediato, il default
quando l'orchestratore genera la trace subito dopo aver risposto, senza
alcun controllo aggiuntivo) e `"manual"` (processo di fallback descritto
in cima a questo file), `outcome.evaluated_by` supporta un terzo valore
intermedio: `"verified"` (vedi
[trace.schema.json](../schema/trace.schema.json)).

Usalo quando, **come parte dello stesso task, prima di scrivere la
trace**, hai controllato concretamente l'affermazione contro un fatto
verificabile — non solo creduto che fosse vera. Esempi concreti:
- hai riletto il file appena scritto e il suo contenuto corrisponde
  davvero a quanto dichiarato (non solo "l'ho scritto, quindi c'è");
- hai eseguito un comando/test e ne hai osservato l'output reale (non
  solo assunto che sarebbe passato);
- hai verificato che una sequenza di passi richiesta è stata rispettata
  nell'ordine giusto (non solo ricordato di averla seguita).

In tutti questi casi, la verifica concreta va anche **dichiarata in
`actions`** (es. `{"description": "riletto il file X e confrontato il
contenuto con quanto atteso", "tool": "..."}`), non solo affermata in
`outcome.detail` — altrimenti non è distinguibile da un self-report.

**Non autoassegnarti `verified` per un giudizio creduto o non
controllato.** Se ti "sembra" che il task sia andato bene, o se ti fidi
del fatto che il tool non ha riportato errori senza aver riletto il
risultato, resta sul `provisional_evaluator` configurato — quello è il valore onesto
per un'autovalutazione, per quanto ragionevole. `verified` non è un modo
per far sembrare più solida una valutazione che in realtà resta un
self-report: è un livello intermedio tra self-report e conferma umana, non
equivalente a nessuno dei due, e va usato solo quando c'è davvero un
controllo dichiarabile alle spalle. Un uso disinvolto di `verified`
vanifica lo scopo per cui esiste — distinguere le trace su cui il curator
può appoggiare decisioni difficili da invertire come DEPRECATE/PROMOTE/
baking (vedi [prompts/curator.md](../prompts/curator.md)) — e sposta
silenziosamente verso `helped_confirmed`/`hurt_confirmed` (vedi
[bullet.schema.json](../schema/bullet.schema.json)) evidenza che in realtà
è solo provvisoria.

## Prima di invocare il reflector (alla soglia): giro retrospettivo sulle trace deboli

Questo passo è a carico dell'orchestratore (resta l'unico agente che
scrive le trace — vincolo di
[config/project.json](../config/project.json), `orchestrator_agent`
singolo, non negoziabile) e va eseguito **solo quando la soglia del
reflector è stata raggiunta**, non ad ogni sessione. Per questo la
sequenza a fine sessione, nel momento in cui si avvicina la soglia,
diventa:

1. genera le trace del task come sempre;
2. esegui `node ace/scripts/check_threshold.js reflector` — conta i file
   in `ace/traces/` indipendentemente da `counted_for_playbook_at`, quindi
   funziona anche prima di aver aggiornato i contatori;
3. **se `reached: true`**: prima di lanciare `update_counters.js`, fai il
   giro retrospettivo descritto sotto ed eventualmente scrivi le trace di
   correzione che ne risultano;
4. **solo dopo** esegui `node ace/scripts/update_counters.js` (processerà
   nello stesso passaggio sia le trace normali sia le eventuali correzioni
   appena scritte);
5. invoca il reflector.

Se al punto 2 `reached: false`, salta i punti 3-4 e procedi come sempre
(`update_counters.js` poi basta, come nelle sessioni che non toccano la
soglia).

**Perché in questo ordine**: `scripts/update_counters.js` dichiara
esplicitamente di dover girare prima del reflector sullo stesso batch. Se
lo lasci girare prima di aver fatto il giro retrospettivo, non è un errore
fatale (una correzione scritta dopo si applica comunque, vedi sotto: i
delta si sommano indipendentemente da quando arrivano), ma il punto di
questo passo è non *dimenticarsene* mai prima della soglia — rispettare
l'ordine qui sopra evita di doverci pensare caso per caso.

### Cosa fare nel giro retrospettivo

Elenca le trace ancora presenti in `ace/traces/` (non `processed/`) con
`outcome.evaluated_by` a tier debole (self-report, tipicamente
il `provisional_evaluator` configurato — vedi
[trace.schema.json](../schema/trace.schema.json) per l'elenco dei tier
forti). Per ciascuna, chiediti: **da quando è stata scritta, è arrivato un
segnale reale sullo stesso ambito?** Es. l'utente ha corretto o confermato
esplicitamente in una sessione successiva qualcosa che quella trace
riguardava, oppure una verifica concreta (non solo un'impressione) ha
smentito o confermato l'esito originale.

- **Se no**: non fare nulla, la trace resta a tier debole così com'è — non
  forzare una correzione senza un segnale reale solo per "irrobustire"
  l'evidenza.
- **Se sì**: scrivi una **trace di correzione** — un file nuovo e separato
  in `ace/traces/`, mai una riscrittura in place dell'originale.
  Referenzia l'originale con il campo `corrects` (vedi
  [trace.schema.json](../schema/trace.schema.json)), con lo stesso schema
  di nome file delle altre trace (`<task_id>__<agent>.json`, dove
  `task_id`/`agent` qui sono quelli **nuovi** di questa correzione, non
  quelli dell'originale — quelli vanno dentro `corrects`):

```json
{
  "task_id": "<nuovo-task-id-per-la-correzione>",
  "agent": "<orchestrator_agent da ace/config/project.json>",
  "started_at": "...",
  "ended_at": "...",
  "playbook_bullets_seen": [],
  "playbook_bullets_cited": [],
  "actions": [
    { "description": "giro retrospettivo prima della soglia reflector: l'utente ha confermato esplicitamente in sessione successiva che <...>" }
  ],
  "outcome": {
    "status": "success",
    "evaluated_by": "user_feedback",
    "detail": "Verifica retrospettiva completata."
  },
  "friction": [],
  "corrects": {
    "task_id": "<task_id della trace originale>",
    "agent": "<agent della trace originale>",
    "reason": "Cosa è arrivato dopo che ha motivato la correzione, e perché.",
    "counter_adjustments": [
      { "bullet_id": "P-XXX", "field": "helped_provisional", "delta": -1 },
      { "bullet_id": "P-XXX", "field": "helped_confirmed", "delta": 1 }
    ]
  }
}
```

`counter_adjustments` va dichiarato esplicitamente da te (l'orchestratore
che scrive la correzione): `scripts/update_counters.js` lo applica
meccanicamente così com'è, non lo deduce da solo. Tipicamente sposta un
delta da un bucket `_provisional` al corrispondente `_confirmed` (conferma
arrivata) o lo riduce/inverte (smentita arrivata) per ciascun bullet
citato nella trace originale — vedi
[bullet.schema.json](../schema/bullet.schema.json). `counter_adjustments:
[]` è una risposta valida se hai verificato che non serve alcun
aggiustamento (es. il self-report originale si è rivelato corretto, non
cambia nulla nei contatori, ma vuoi comunque lasciare traccia di aver
controllato).

## Esempio di struttura (placeholder, NON dati reali)

```json
{
  "task_id": "2026-08-07-esempio",
  "agent": "<uno dei nomi in ace/config/project.json: orchestrator_agent o uno dei subagents>",
  "started_at": "2026-08-07T12:00:00Z",
  "ended_at": "2026-08-07T12:05:00Z",
  "request_summary": "<parafrasi della richiesta utente>",
  "playbook_bullets_seen": [],
  "playbook_bullets_cited": [],
  "actions": [
    { "description": "<azione rilevante>", "tool": "<tool usato, se noto>" }
  ],
  "outcome": {
    "status": "success",
    "evaluated_by": "manual",
    "detail": "<perché è andata bene o male>"
  },
  "notes": "<osservazioni libere>",
  "friction": [
    { "description": "<intoppo operativo, es. comando lanciato dalla cartella sbagliata>", "recovered": true }
  ]
}
```

Questo file è un template di processo, non un esempio di lezione: non
contiene bullet né dati inventati sul dominio del progetto.
