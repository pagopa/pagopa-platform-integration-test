#!/usr/bin/env node
'use strict';

// Contabilità deterministica dei contatori used/helped/hurt (e della loro
// scomposizione a due livelli helped_confirmed/helped_provisional/
// hurt_confirmed/hurt_provisional) sui bullet dei playbook, a partire dalle
// trace. Non è compito del curator (LLM): è pura somma meccanica di
// playbook_bullets_seen/cited + outcome.status + outcome.evaluated_by su un
// batch di trace — stessa logica per cui il gate fa solo controlli meccanici
// e lascia il giudizio all'umano.
//
// Tier di evaluated_by (vedi trace.schema.json): 'verified'/'manual'/
// 'user_feedback'/'gate_replay'/'reflector_llm' sono evidenza CONFERMATA
// (bucket _confirmed); qualunque altro valore — incluso il self-report
// immediato '<team>-auto', assente, o non riconosciuto — è solo PROVVISORIO
// (bucket _provisional). helped/hurt restano l'aggregato storico
// (helped_confirmed+helped_provisional / hurt_confirmed+hurt_provisional),
// ma non guidano più da soli le decisioni strutturali del curator (vedi
// prompts/curator.md) né l'esclusione live (vedi scripts/retrieval.js).
//
// Trace di correzione (doc.corrects, vedi trace.schema.json): dichiarano
// esplicitamente un array counter_adjustments di {bullet_id, field, delta}
// da sommare ai contatori del bullet referenziato — applicati così come
// sono, senza dedurre nulla, in aggiunta al conteggio normale di questa
// stessa trace (che può restare vuota se la correzione non è di per sé un
// nuovo utilizzo del bullet).
//
// Batch: stessa definizione di prompts/reflector.md — tutti i file in
// ace/traces/ (non in traces/processed/). Va eseguito PRIMA di invocare
// il reflector sullo stesso batch, altrimenti i contatori restano
// indietro rispetto alle trace più recenti (non è un problema di
// correttezza, solo di freschezza: le trace non processate aspettano
// comunque il prossimo run).
//
// Idempotenza: ogni trace processata viene marcata con
// `counted_for_playbook_at` (vedi trace.schema.json) e non viene
// riprocessata in run successivi, indipendentemente da quando reflector
// la sposta in traces/processed/ — le due cose sono disaccoppiate.
//
// Uso:
//   node ace/scripts/update_counters.js            # applica i delta
//   node ace/scripts/update_counters.js --check    # stampa i delta, non scrive
//   node ace/scripts/update_counters.js --task-id <id> # limita il batch al task

const fs = require('fs');
const path = require('path');
const {
  REPO_ROOT, parsePlaybookFile, serializeFile, listPlaybookFiles, listArchiveFiles,
  assertSafeWritePath, acquireMutationLock,
} = require('./lib/playbook');
const retrieval = require('./retrieval');

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

const JOURNAL_PATH = path.join(REPO_ROOT, 'ace', 'state', 'counter-update.json');

function atomicWrite(targetPath, content) {
  assertSafeWritePath(targetPath);
  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  const temporary = `${targetPath}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, content);
  fs.renameSync(temporary, targetPath);
}

function recoverPendingJournal(verbose) {
  if (!fs.existsSync(JOURNAL_PATH)) return false;
  const journal = readJSON(JOURNAL_PATH);
  for (const entry of journal.writes || []) {
    atomicWrite(path.join(REPO_ROOT, entry.path), entry.content);
  }
  fs.unlinkSync(JOURNAL_PATH);
  if (verbose) console.log(`Recuperato aggiornamento contatori incompleto (${journal.trace_count} trace).`);
  return true;
}

function collectUnprocessedTraces(taskId) {
  // Guarda sia ace/traces/ sia ace/traces/processed/: la marcatura
  // counted_for_playbook_at e lo spostamento in processed/ (fatto dal
  // reflector) sono disaccoppiati, quindi una trace può finire in
  // processed/ prima di essere mai stata contata (es. run passati in cui
  // questo script non è stato lanciato). Va comunque contata una sola
  // volta, indipendentemente da dove si trova.
  const dirs = [
    path.join(REPO_ROOT, 'ace', 'traces'),
    path.join(REPO_ROOT, 'ace', 'traces', 'processed'),
  ];

  const traces = [];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir, { withFileTypes: true })
      .filter((e) => e.isFile() && e.name.endsWith('.json'))
      .map((e) => path.join(dir, e.name));

    for (const abs of files) {
      const doc = readJSON(abs);
      if (doc.counted_for_playbook_at) continue; // già contata in un run precedente
      if (taskId && doc.task_id !== taskId) continue;
      traces.push({ abs, doc });
    }
  }
  return traces;
}

// Tier "forte" di outcome.evaluated_by (vedi trace.schema.json): una trace
// con uno di questi valori conta come evidenza CONFERMATA (bucket
// _confirmed). Qualunque altro valore — incluso il self-report immediato
// '<team>-auto', assente, o un valore non riconosciuto/typo — conta come
// evidenza solo PROVVISORIA (bucket _provisional). Default deliberatamente
// prudente: solo un match esplicito con uno di questi 5 valori promuove a
// "confirmed", mai un'assenza o un valore inatteso.
const STRONG_EVALUATED_BY = new Set(['verified', 'manual', 'user_feedback', 'gate_replay', 'reflector_llm']);

function tierOf(evaluatedBy) {
  return STRONG_EVALUATED_BY.has(evaluatedBy) ? 'confirmed' : 'provisional';
}

function emptyDelta() {
  return {
    used: 0, helped: 0, hurt: 0, helped_confirmed: 0, helped_provisional: 0, hurt_confirmed: 0, hurt_provisional: 0,
  };
}

// Una trace originale referenziata da `corrects` deve esistere da qualche
// parte in ace/traces/ o ace/traces/processed/ (le due cose sono
// disaccoppiate, vedi collectUnprocessedTraces sopra) — non è un requisito
// bloccante (questo script non giudica, applica comunque l'aggiustamento
// dichiarato), ma la sua assenza è un'anomalia da segnalare esplicitamente.
function originalTraceExists(taskId, agent) {
  const name = `${taskId}__${agent}.json`;
  return fs.existsSync(path.join(REPO_ROOT, 'ace', 'traces', name))
    || fs.existsSync(path.join(REPO_ROOT, 'ace', 'traces', 'processed', name));
}

function computeDeltas(traces) {
  const deltas = new Map(); // id -> { used, helped, hurt, helped_confirmed, helped_provisional, hurt_confirmed, hurt_provisional }
  const warnings = [];

  const bump = (id, field, amount = 1) => {
    if (!deltas.has(id)) deltas.set(id, emptyDelta());
    deltas.get(id)[field] += amount;
  };

  for (const { doc, abs } of traces) {
    const seen = doc.playbook_bullets_seen || [];
    const cited = doc.playbook_bullets_cited || [];
    const status = doc.outcome && doc.outcome.status;
    const evaluatedBy = doc.outcome && doc.outcome.evaluated_by;
    const tier = tierOf(evaluatedBy);

    if (cited.length && !evaluatedBy) {
      warnings.push(`${path.basename(abs)}: outcome.evaluated_by assente — trattato come "provisional" per prudenza (nessun contatore _confirmed senza un tier esplicito riconosciuto).`);
    }

    for (const id of seen) bump(id, 'used');

    for (const id of cited) {
      if (!seen.includes(id)) {
        warnings.push(`${path.basename(abs)}: id "${id}" citato ma non presente in playbook_bullets_seen — contato comunque come used, ma segnalo l'incoerenza.`);
        bump(id, 'used');
      }
      if (status === 'success') {
        bump(id, 'helped');
        bump(id, tier === 'confirmed' ? 'helped_confirmed' : 'helped_provisional');
      } else if (status === 'failure') {
        bump(id, 'hurt');
        bump(id, tier === 'confirmed' ? 'hurt_confirmed' : 'hurt_provisional');
      }
      // "partial": nessun segnale su helped/hurt (né confirmed/provisional), resta solo used.
    }

    // Trace di correzione (vedi trace.schema.json, corrects): aggiustamenti
    // espliciti dichiarati da chi scrive la correzione, applicati così come
    // sono — questo script non deduce nulla, si limita a sommare, in
    // aggiunta al conteggio normale sopra (che per una pura correzione può
    // restare a zero, se seen/cited di questa trace sono vuoti).
    if (doc.corrects && Array.isArray(doc.corrects.counter_adjustments)) {
      if (!originalTraceExists(doc.corrects.task_id, doc.corrects.agent)) {
        warnings.push(`${path.basename(abs)}: trace di correzione referenzia "${doc.corrects.task_id}__${doc.corrects.agent}" ma non trovo quel file in ace/traces/ né ace/traces/processed/ — applico comunque gli aggiustamenti dichiarati (non è compito di questo script giudicare la validità del riferimento), ma segnalo l'anomalia.`);
      }
      for (const adj of doc.corrects.counter_adjustments) {
        bump(adj.bullet_id, adj.field, adj.delta);
      }
    }
  }

  return { deltas, warnings };
}

function applyDeltas(deltas) {
  const touchedFiles = new Map(); // relPath -> parsed
  const applied = [];
  const notFound = [];
  const ambiguous = [];
  const clamped = [];

  const allRelPaths = [...listPlaybookFiles(), ...listArchiveFiles()];
  const TIERED_FIELDS = ['used', 'helped', 'hurt', 'helped_confirmed', 'helped_provisional', 'hurt_confirmed', 'hurt_provisional'];

  function loadFile(relPath) {
    if (touchedFiles.has(relPath)) return touchedFiles.get(relPath);
    const abs = path.join(REPO_ROOT, relPath);
    assertSafeWritePath(abs);
    const parsed = parsePlaybookFile(fs.readFileSync(abs, 'utf8'));
    touchedFiles.set(relPath, parsed);
    return parsed;
  }

  for (const [id, delta] of deltas) {
    // BUG STORICO (corretto qui): si cercava il bullet scorrendo
    // allRelPaths e ci si fermava al primo file in cui lo si trovava,
    // attribuendo silenziosamente i contatori al bullet sbagliato quando
    // lo stesso ID esisteva (per un difetto di integrità dei dati) in più
    // file. Le trace non portano informazione di scope per gli ID citati,
    // quindi qui non si può disambiguare come in apply_delta.js (che ha
    // final_scope): l'unica scelta sicura è NON decidere da soli,
    // segnalare l'ambiguità e non scrivere nulla per quell'ID finché la
    // collisione non è risolta a livello di playbook.
    const matches = [];
    for (const relPath of allRelPaths) {
      const parsed = loadFile(relPath);
      const bullet = parsed.bullets.find((b) => b.id === id);
      if (bullet) matches.push({ relPath, bullet });
    }
    if (!matches.length) { notFound.push(id); continue; }
    // Solo le occorrenze NON deprecated contano come ambigue: un bullet
    // deprecated in archivio che condivide per storia lo stesso ID con un
    // bullet attivo altrove (es. una collisione passata già risolta con
    // una DEPRECATE mirata) è storico e non riceve più scritture — non è
    // una vera ambiguità su cui attribuire il delta di oggi.
    const liveMatches = matches.filter((m) => m.bullet.status !== 'deprecated');
    if (liveMatches.length > 1) {
      ambiguous.push({ id, files: liveMatches.map((m) => m.relPath) });
      continue;
    }
    const found = liveMatches[0] || matches[0];
    found.bullet.used += delta.used;
    found.bullet.helped += delta.helped;
    found.bullet.hurt += delta.hurt;
    found.bullet.helped_confirmed += delta.helped_confirmed;
    found.bullet.helped_provisional += delta.helped_provisional;
    found.bullet.hurt_confirmed += delta.hurt_confirmed;
    found.bullet.hurt_provisional += delta.hurt_provisional;

    // Le trace di correzione possono dichiarare delta negativi (es.
    // rimuovere un provisional attribuito per errore): clampa a 0 invece di
    // scrivere un contatore negativo (bullet.schema.json impone minimum:0)
    // e segnala esplicitamente, così un aggiustamento errato/eccessivo non
    // produce silenziosamente dati non validi.
    for (const field of TIERED_FIELDS) {
      if (found.bullet[field] < 0) {
        clamped.push({ id, field, wouldBe: found.bullet[field] });
        found.bullet[field] = 0;
      }
    }

    applied.push({
      id,
      file: found.relPath,
      delta,
      totals: {
        used: found.bullet.used,
        helped: found.bullet.helped,
        hurt: found.bullet.hurt,
        helped_confirmed: found.bullet.helped_confirmed,
        helped_provisional: found.bullet.helped_provisional,
        hurt_confirmed: found.bullet.hurt_confirmed,
        hurt_provisional: found.bullet.hurt_provisional,
      },
    });
  }

  return {
    touchedFiles, applied, notFound, ambiguous, clamped,
  };
}

function run({ checkOnly = false, verbose = true, taskId } = {}) {
  const releaseLock = checkOnly ? null : acquireMutationLock('update_counters');
  if (releaseLock) process.once('exit', releaseLock);
  if (!checkOnly && recoverPendingJournal(verbose)) {
    retrieval.run({ checkOnly: false, verbose });
    releaseLock();
    return { applied: [], warnings: [], recovered: true };
  }
  const traces = collectUnprocessedTraces(taskId);
  if (!traces.length) {
    if (verbose) console.log('Nessuna trace non ancora contata in ace/traces/.');
    if (releaseLock) releaseLock();
    return { applied: [], warnings: [] };
  }

  const { deltas, warnings } = computeDeltas(traces);
  if (verbose) {
    for (const w of warnings) console.log(`ATTENZIONE: ${w}`);
    if (!deltas.size) console.log(`${traces.length} trace lette, nessun bullet citato/visto (playbook_bullets_seen/cited vuoti).`);
  }

  const { touchedFiles, applied, notFound, ambiguous, clamped } = applyDeltas(deltas);

  if (verbose) {
    for (const a of applied) {
      console.log(`[${a.id}] +used:${a.delta.used} +helped:${a.delta.helped} (confirmed:${a.delta.helped_confirmed >= 0 ? '+' : ''}${a.delta.helped_confirmed} provisional:${a.delta.helped_provisional >= 0 ? '+' : ''}${a.delta.helped_provisional}) +hurt:${a.delta.hurt} (confirmed:${a.delta.hurt_confirmed >= 0 ? '+' : ''}${a.delta.hurt_confirmed} provisional:${a.delta.hurt_provisional >= 0 ? '+' : ''}${a.delta.hurt_provisional}) → totali used:${a.totals.used} helped:${a.totals.helped} hurt:${a.totals.hurt} (helped_confirmed:${a.totals.helped_confirmed} helped_provisional:${a.totals.helped_provisional} hurt_confirmed:${a.totals.hurt_confirmed} hurt_provisional:${a.totals.hurt_provisional}) (${a.file})`);
    }
    for (const id of notFound) {
      console.log(`ATTENZIONE: id "${id}" citato in una trace ma non trovato in nessun playbook/archive — ignorato.`);
    }
    for (const a of ambiguous) {
      console.log(`ATTENZIONE: id "${a.id}" citato in una trace ma AMBIGUO — presente in più file (${a.files.join(', ')}). Integrità dei dati compromessa (collisione di ID): contatori NON aggiornati per questo ID finché la collisione non viene risolta a livello di playbook (vedi ace/scripts/lib/playbook.js#detectIdCollisions).`);
    }
    for (const c of clamped) {
      console.log(`ATTENZIONE: [${c.id}] il contatore "${c.field}" sarebbe andato sotto zero (${c.wouldBe}) dopo un aggiustamento (probabilmente da una trace di correzione) — clampato a 0. Verifica la trace che ha causato l'aggiustamento.`);
    }
  }

  if (checkOnly) {
    if (verbose) console.log(`(--check) ${traces.length} trace, ${applied.length} bullet aggiornati, nessuna scrittura eseguita.`);
    return {
      applied, warnings, ambiguous, clamped, wouldWrite: touchedFiles.size > 0,
    };
  }

  if (notFound.length || ambiguous.length) {
    if (verbose) {
      console.log('Nessuna scrittura eseguita e nessuna trace marcata come contata: risolvi tutti gli ID mancanti o ambigui e rilancia.');
    }
    process.exitCode = 1;
    if (releaseLock) releaseLock();
    return {
      applied: [], warnings, ambiguous, clamped, notFound, blocked: true,
    };
  }

  const now = new Date().toISOString();
  const writes = [];
  for (const [relPath, parsed] of touchedFiles) {
    writes.push({
      path: relPath.replace(/\\/g, '/'),
      content: serializeFile(parsed.prefix, parsed.bullets, parsed.suffix),
    });
  }
  for (const { abs, doc } of traces) {
    doc.counted_for_playbook_at = now;
    writes.push({
      path: path.relative(REPO_ROOT, abs).replace(/\\/g, '/'),
      content: `${JSON.stringify(doc, null, 2)}\n`,
    });
  }
  atomicWrite(JOURNAL_PATH, `${JSON.stringify({
    created_at: now,
    trace_count: traces.length,
    writes,
  }, null, 2)}\n`);
  recoverPendingJournal(false);
  retrieval.run({ checkOnly: false, verbose });

  if (verbose) {
    console.log(`Contate ${traces.length} trace, aggiornati ${applied.length} bullet in ${touchedFiles.size} file playbook.`);
  }

  if (releaseLock) releaseLock();
  return {
    applied, warnings, ambiguous, clamped,
  };
}

module.exports = { run };

if (require.main === module) {
  const taskIndex = process.argv.indexOf('--task-id');
  const taskId = taskIndex === -1 ? undefined : process.argv[taskIndex + 1];
  if (taskIndex !== -1 && !taskId) {
    console.error('Uso: node ace/scripts/update_counters.js [--check] [--task-id <task-id>]');
    process.exitCode = 1;
  } else {
    run({ checkOnly: process.argv.includes('--check'), taskId });
  }
}
