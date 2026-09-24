#!/usr/bin/env node
'use strict';

// Gate deterministico: valida un file di decisioni del curator PRIMA che
// apply_delta.js tocchi i playbook. Uso:
//   node ace/scripts/gate.js <decisions-file.json> [--sign-off]
//
// Importante: questo script fa SOLO controlli meccanici — struttura, enum,
// collisioni di ID, compatibilità tra operazione e stato attuale del
// bullet (es. PROMOTE solo su 'quarantined', niente UPDATE/DEPRECATE su
// bullet già 'deprecated', niente MERGE che includa il target stesso o
// bullet già deprecated), esistenza delle trace citate come evidenza. Il
// "set di regressione" si divide quindi in due parti distinte, non in una
// sola:
// - la parte strutturale/di stato sopra: automatizzata qui, deterministica.
// - il conflitto SEMANTICO tra il nuovo contenuto e gli altri bullet attivi
//   dello stesso scope (es. una nuova regola che ne contraddice un'altra
//   già attiva senza essere marcata come tale): questo NON è automatizzato
//   di proposito, richiede un giudizio (umano o LLM), non un controllo
//   deterministico — è per questo che l'agente warden lo pone esplicitamente
//   come checklist alla revisione umana prima del sign-off (vedi
//   prompts/warden.md), invece di provare a scriptarlo qui.
// Per questo il gate non firma mai da solo: richiede sempre --sign-off
// esplicito, che rappresenta la revisione umana.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {
  REPO_ROOT, loadBulletSchema, loadProjectConfig, loadAgentNames, collectExistingIds, scopeToRelPath,
  findAllBulletLocations, detectIdCollisions, SAFE_SCOPE_ID_RE, assertSafeWritePath,
  computeReviewStateHash,
} = require('./lib/playbook');

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function sha256File(p) {
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
}

function main() {
  const args = process.argv.slice(2);
  const decisionsPathArg = args.find((a) => !a.startsWith('--'));
  const signOff = args.includes('--sign-off');
  const verifyOnly = args.includes('--verify-only');

  if (!decisionsPathArg) {
    console.error('Uso: node ace/scripts/gate.js <decisions-file.json> [--sign-off]');
    process.exit(2);
  }

  const decisionsPath = path.resolve(decisionsPathArg);
  const decisionsRel = path.relative(REPO_ROOT, decisionsPath).replace(/\\/g, '/');
  if (decisionsRel.startsWith('../') || path.isAbsolute(decisionsRel)
      || !decisionsRel.startsWith('ace/proposals/') || decisionsRel.includes('/applied/')) {
    throw new Error('Il file decisioni deve trovarsi direttamente in ace/proposals/.');
  }
  if (!decisionsPath.endsWith('-decisions.json')) {
    throw new Error('Il file decisioni deve terminare con -decisions.json.');
  }
  const decisionsDoc = readJSON(decisionsPath);
  if (!decisionsDoc || !decisionsDoc.batch_id || !Array.isArray(decisionsDoc.decisions)) {
    throw new Error('File decisioni malformato: batch_id e decisions[] sono obbligatori.');
  }
  if (!SAFE_SCOPE_ID_RE.test(decisionsDoc.batch_id)) {
    throw new Error(`batch_id non sicuro: ${decisionsDoc.batch_id}.`);
  }
  if (!decisionsDoc.source_proposals_file
      || path.basename(decisionsDoc.source_proposals_file) !== decisionsDoc.source_proposals_file) {
    throw new Error('source_proposals_file deve essere un nome file locale ad ace/proposals/.');
  }

  const proposalsPath = path.join(path.dirname(decisionsPath), decisionsDoc.source_proposals_file);
  const proposalsDoc = fs.existsSync(proposalsPath) ? readJSON(proposalsPath) : null;
  if (!proposalsDoc || !Array.isArray(proposalsDoc.proposals)) {
    throw new Error('File proposte mancante o malformato.');
  }
  if (proposalsDoc.batch_id !== decisionsDoc.batch_id) {
    throw new Error('batch_id non coincide tra proposte e decisioni.');
  }
  const proposalsById = new Map();
  for (const proposal of proposalsDoc.proposals) proposalsById.set(proposal.proposal_id, proposal);

  const schema = loadBulletSchema();
  const projectConfig = loadProjectConfig();
  // La lista di agenti validi vive in config/project.json (vedi
  // lib/playbook.js), non più come enum hardcoded nello schema: così lo
  // schema resta identico da progetto a progetto, e solo la config
  // cambia. Se il wizard di installazione non è stato completato,
  // loadAgentNames() lancia un errore esplicito invece di validare contro
  // placeholder non risolti.
  const agentEnum = loadAgentNames();
  const configuredFamilies = new Set(Object.values(projectConfig.agent_families || {}).flat());
  const scopeTypeEnum = schema.properties.scope.properties.type.enum;
  const idPattern = new RegExp(schema.properties.id.pattern);

  const existingIds = collectExistingIds();
  const tracesProcessedDir = path.join(REPO_ROOT, 'ace', 'traces', 'processed');
  const validProcessedTaskIds = new Set();
  if (fs.existsSync(tracesProcessedDir)) {
    for (const file of fs.readdirSync(tracesProcessedDir).filter((name) => name.endsWith('.json'))) {
      try {
        const trace = readJSON(path.join(tracesProcessedDir, file));
        const structurallyValid = trace
          && typeof trace.task_id === 'string'
          && agentEnum.includes(trace.agent)
          && file === `${trace.task_id}__${trace.agent}.json`
          && typeof trace.started_at === 'string'
          && Array.isArray(trace.playbook_bullets_seen)
          && Array.isArray(trace.playbook_bullets_cited)
          && Array.isArray(trace.actions)
          && trace.outcome
          && ['success', 'partial', 'failure'].includes(trace.outcome.status)
          && Array.isArray(trace.friction);
        if (structurallyValid) validProcessedTaskIds.add(trace.task_id);
      } catch {
        // Malformed trace files are deliberately excluded from evidence.
      }
    }
  }
  const liveExclusionsPath = path.join(REPO_ROOT, 'ace', 'state', 'live-exclusions.json');
  const liveExclusions = fs.existsSync(liveExclusionsPath)
    ? new Set((readJSON(liveExclusionsPath).live_exclusions || []).map((entry) => entry.id))
    : new Set();
  const validOperations = new Set(['ADD', 'UPDATE', 'DEPRECATE', 'MERGE', 'PROMOTE', 'REJECT']);

  const results = [];
  let allMechanicalPass = true;
  const decisionProposalIds = decisionsDoc.decisions
    .filter((decision) => decision && typeof decision.proposal_id === 'string')
    .map((decision) => decision.proposal_id);
  const duplicateDecisionIds = [...new Set(decisionProposalIds.filter(
    (proposalId, index) => decisionProposalIds.indexOf(proposalId) !== index,
  ))];
  if (duplicateDecisionIds.length) {
    allMechanicalPass = false;
    results.push({
      proposal_id: 'BATCH-DUPLICATE-PROPOSAL-CHECK',
      operation: 'CHECK',
      mechanical_status: 'FAIL',
      checks: [{
        pass: false,
        message: `proposal_id duplicati nel batch: ${duplicateDecisionIds.join(', ')}`,
      }],
    });
  }
  const proposalIds = proposalsDoc.proposals.map((proposal) => proposal.proposal_id);
  const duplicateProposalIds = [...new Set(proposalIds.filter(
    (proposalId, index) => proposalIds.indexOf(proposalId) !== index,
  ))];
  const missingDecisions = proposalIds.filter((proposalId) => !decisionProposalIds.includes(proposalId));
  if (duplicateProposalIds.length || missingDecisions.length) {
    allMechanicalPass = false;
    results.push({
      proposal_id: 'BATCH-PROPOSAL-COMPLETENESS-CHECK',
      operation: 'CHECK',
      mechanical_status: 'FAIL',
      checks: [
        ...duplicateProposalIds.map((proposalId) => ({
          pass: false,
          message: `proposal_id duplicato nel file proposte: ${proposalId}.`,
        })),
        ...missingDecisions.map((proposalId) => ({
          pass: false,
          message: `Nessuna decisione presente per la proposta ${proposalId}.`,
        })),
      ],
    });
  }
  const affectedIds = new Map();
  for (const decision of decisionsDoc.decisions.filter(Boolean)) {
    if (decision.operation === 'REJECT') continue;
    const ids = decision.operation === 'MERGE'
      ? [decision.target_bullet_id, ...(decision.merged_from || [])]
      : [decision.target_bullet_id];
    for (const id of ids.filter(Boolean)) {
      if (!affectedIds.has(id)) affectedIds.set(id, []);
      affectedIds.get(id).push(decision.proposal_id);
    }
  }
  const conflictingIds = [...affectedIds.entries()].filter(([, proposalIds]) => proposalIds.length > 1);
  if (conflictingIds.length) {
    allMechanicalPass = false;
    results.push({
      proposal_id: 'BATCH-CONFLICTING-OPERATIONS-CHECK',
      operation: 'CHECK',
      mechanical_status: 'FAIL',
      checks: conflictingIds.map(([id, proposalIds]) => ({
        pass: false,
        message: `Il bullet ${id} è coinvolto da più decisioni nello stesso batch: ${proposalIds.join(', ')}.`,
      })),
    });
  }

  for (const d of decisionsDoc.decisions) {
    const checks = [];
    const fail = (msg) => checks.push({ pass: false, message: msg });
    const pass = (msg) => checks.push({ pass: true, message: msg });

    if (!d || typeof d !== 'object') {
      fail('Decisione non valida.');
      allMechanicalPass = false;
      results.push({
        proposal_id: null,
        operation: null,
        mechanical_status: 'FAIL',
        checks,
      });
      continue;
    }
    if (!validOperations.has(d.operation)) {
      fail(`operation non valida: ${d.operation}`);
    }
    if (!d.proposal_id || typeof d.proposal_id !== 'string') {
      fail('proposal_id mancante o non valido.');
    }

    const proposal = proposalsById.get(d.proposal_id);
    const isLiveExclusion = d.operation === 'DEPRECATE'
      && d.proposal_id === `LIVE-EXCL-${d.target_bullet_id}`
      && liveExclusions.has(d.target_bullet_id);
    if (!proposal && !isLiveExclusion) {
      fail(`Proposta di origine non trovata: ${d.proposal_id} (file ${decisionsDoc.source_proposals_file})`);
    } else if (proposal) {
      const supporting = proposal.supporting_task_ids || [];
      if (!Array.isArray(supporting) || !supporting.length) {
        fail('Nessuna supporting_task_ids nella proposta di origine: evidenza non citabile.');
      } else {
        const missingTraces = supporting.filter(
          (taskId) => !validProcessedTaskIds.has(taskId),
        );
        if (missingTraces.length) {
          fail(`Trace di evidenza non trovate in ace/traces/processed/: ${missingTraces.join(', ')}`);
        } else {
          pass(`Evidenza verificata: ${supporting.length} task citato/i, trace presenti in ace/traces/processed/.`);
        }
      }
    } else {
      pass(`Esclusione live verificata per ${d.target_bullet_id}.`);
    }

    if (d.operation === 'REJECT') {
      const decisionPass = checks.every((check) => check.pass);
      if (!decisionPass) allMechanicalPass = false;
      results.push({
        proposal_id: d.proposal_id,
        operation: d.operation,
        mechanical_status: decisionPass ? 'PASS' : 'FAIL',
        checks,
      });
      continue;
    }

    if (!d.final_scope || !scopeTypeEnum.includes(d.final_scope.type)) {
      fail(`scope.type mancante o non valido: ${d.final_scope && d.final_scope.type}`);
    } else if (d.final_scope.type === 'agent' && !agentEnum.includes(d.final_scope.agent)) {
      fail(`scope.agent non valido: ${d.final_scope.agent}`);
    } else if (d.final_scope.type === 'family' && !SAFE_SCOPE_ID_RE.test(d.final_scope.family || '')) {
      fail(`scope.family mancante o non sicuro: ${d.final_scope.family}`);
    } else if (d.final_scope.type === 'family' && !configuredFamilies.has(d.final_scope.family)) {
      fail(`scope.family non configurato in agent_families: ${d.final_scope.family}`);
    } else {
      pass('scope valido');
    }

    if (!d.target_bullet_id || !idPattern.test(d.target_bullet_id)) {
      fail(`target_bullet_id non valido: ${d.target_bullet_id}`);
    } else if (d.operation === 'ADD') {
      if (existingIds.has(d.target_bullet_id)) fail(`ID già esistente, non riutilizzabile per ADD: ${d.target_bullet_id}`);
      else pass('ID nuovo, nessuna collisione');
      if (d.initial_status !== 'active') fail('ADD richiede initial_status: active.');
    } else if (['UPDATE', 'DEPRECATE', 'PROMOTE'].includes(d.operation)) {
      // Non ci si affida più a collectExistingIds() (una sola entry per
      // ID, potenzialmente ambigua): si guarda l'elenco COMPLETO dei file
      // in cui l'ID compare, e si richiede che il final_scope dichiarato
      // corrisponda a uno di essi quando l'ID è ambiguo (presente in più
      // di un file). Questo è il controllo che avrebbe impedito ad
      // apply_delta.js di operare sul file sbagliato in caso di
      // collisione di ID.
      const locations = findAllBulletLocations(d.target_bullet_id);
      const expectedRel = d.final_scope && scopeTypeEnum.includes(d.final_scope.type)
        ? scopeToRelPath(d.final_scope) : null;
      const atExpected = expectedRel ? locations.find((l) => l.relPath === expectedRel) : null;

      if (!locations.length) {
        fail(`Bullet non trovato per ${d.operation}: ${d.target_bullet_id}`);
      } else if (locations.length > 1 && !atExpected) {
        fail(`ID "${d.target_bullet_id}" ambiguo: trovato in più file (${locations.map((l) => l.relPath).join(', ')}) ma nessuno corrisponde al final_scope dichiarato (${expectedRel || 'n/d'}) — impossibile determinare in modo sicuro su quale bullet operare senza disambiguare esplicitamente lo scope nella decisione.`);
      } else {
        const existing = atExpected || locations[0];
        if (locations.length > 1) {
          pass(`ID ambiguo (${locations.length} occorrenze) ma risolto in modo sicuro tramite final_scope: operazione su "${existing.relPath}"`);
        }
        if (d.operation === 'PROMOTE' && existing.status !== 'quarantined') {
          fail(`PROMOTE richiede un bullet in stato 'quarantined', trovato '${existing.status}': ${d.target_bullet_id}`);
        } else if (d.operation === 'DEPRECATE' && existing.status === 'deprecated') {
          fail(`DEPRECATE su bullet già 'deprecated': ${d.target_bullet_id}`);
        } else if (d.operation === 'UPDATE' && existing.status === 'deprecated') {
          fail(`UPDATE su bullet 'deprecated': ${d.target_bullet_id} — gli id deprecati non si riattivano con UPDATE, serve un ADD nuovo o un PROMOTE se era solo quarantined`);
        } else {
          pass(`bullet esistente trovato in "${existing.relPath}", stato '${existing.status}' compatibile con ${d.operation}`);
        }
      }
    } else if (d.operation === 'MERGE') {
      const sources = d.merged_from || [];
      if (existingIds.has(d.target_bullet_id)) {
        fail(`ID già esistente, non riutilizzabile come target MERGE: ${d.target_bullet_id}`);
      } else {
        pass('ID target MERGE nuovo, nessuna collisione');
      }
      if (!Array.isArray(sources) || sources.length < 2) {
        fail('MERGE richiede almeno due merged_from.');
      } else if (new Set(sources).size !== sources.length) {
        fail('MERGE non accetta id duplicati in merged_from.');
      } else if (sources.includes(d.target_bullet_id)) {
        fail(`merged_from non può includere il target_bullet_id stesso: ${d.target_bullet_id}`);
      } else {
        const missing = sources.filter((id) => !existingIds.has(id));
        const alreadyDeprecated = sources.filter((id) => existingIds.get(id) && existingIds.get(id).status === 'deprecated');
        if (missing.length) fail(`merged_from con id inesistenti: ${missing.join(', ')}`);
        else if (alreadyDeprecated.length) fail(`merged_from con id già 'deprecated', non fondibili: ${alreadyDeprecated.join(', ')}`);
        else pass('tutti i merged_from esistono e non sono già deprecated');
      }
      if (d.initial_status !== 'active') fail('MERGE richiede initial_status: active.');
    }

    if (!d.final_content || typeof d.final_content !== 'string' || !d.final_content.trim()) {
      fail('final_content mancante o vuoto');
    } else if (/^(?:## P-\d+\s+—|tags:|counters:|provenance:|<!--|-->)/m.test(d.final_content)) {
      fail('final_content contiene una riga riservata alla struttura del playbook.');
    } else {
      pass('final_content presente e privo di righe strutturali riservate');
    }

    const decisionPass = checks.every((c) => c.pass);
    if (!decisionPass) allMechanicalPass = false;
    results.push({
      proposal_id: d.proposal_id,
      operation: d.operation,
      target_bullet_id: d.target_bullet_id,
      mechanical_status: decisionPass ? 'PASS' : 'FAIL',
      checks,
    });
  }

  // Controllo batch-level (non per singola decisione): qualunque
  // collisione di ID esistente nell'intero universo playbook+archivio
  // DEVE essere toccata da almeno una decisione di questo batch (una
  // UPDATE/DEPRECATE/PROMOTE il cui target_bullet_id coincide con l'ID in
  // collisione), altrimenti il batch la lascerebbe silenziosamente
  // irrisolta per un altro ciclo. Le collisioni toccate da questo batch
  // sono già validate nel dettaglio (scope/ambiguità) dal controllo
  // per-decisione sopra.
  const unresolvedCollisions = detectIdCollisions();
  if (unresolvedCollisions.length) {
    allMechanicalPass = false;
    results.push({
      proposal_id: 'BATCH-ID-COLLISION-CHECK',
      operation: 'CHECK',
      mechanical_status: 'FAIL',
      checks: unresolvedCollisions.map((c) => ({
        pass: false,
        message: `ID "${c.id}" duplicato tra più file playbook (${c.files.join(', ')}): integrità dei dati compromessa, va risolta manualmente prima che qualunque batch possa essere firmato.`,
      })),
    });
  }

  const report = {
    batch_id: decisionsDoc.batch_id,
    gated_at: new Date().toISOString(),
    source_decisions_file: decisionsRel,
    source_decisions_sha256: sha256File(decisionsPath),
    source_proposals_file: path.relative(REPO_ROOT, proposalsPath).replace(/\\/g, '/'),
    source_proposals_sha256: fs.existsSync(proposalsPath) ? sha256File(proposalsPath) : null,
    review_state_sha256: computeReviewStateHash(),
    all_mechanical_pass: allMechanicalPass,
    replay_note: "Il set di regressione si divide in due parti: (1) struttura + compatibilità operazione/stato del bullet (PROMOTE solo da quarantined, niente UPDATE/DEPRECATE/MERGE su bullet già deprecated, ecc.) + esistenza dell'evidenza citata — verificate meccanicamente qui; (2) conflitto semantico col resto del playbook dello stesso scope — non automatizzato di proposito (richiede giudizio umano o LLM), posto come checklist esplicita dall'agente warden alla revisione umana prima del sign-off. Il sign-off umano resta obbligatorio prima che apply_delta possa procedere.",
    signed_off: false,
    results,
  };

  const reportPath = decisionsPath.replace(/-decisions\.json$/, '-gate-report.json');

  if (signOff) {
    if (!allMechanicalPass) {
      console.error('Impossibile firmare: alcuni controlli meccanici falliscono. Vedi report per i dettagli.');
    } else {
      report.signed_off = true;
      report.signed_off_at = new Date().toISOString();
    }
  }

  if (!verifyOnly) {
    assertSafeWritePath(reportPath);
    fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
  }
  const reportRel = path.relative(REPO_ROOT, reportPath).replace(/\\/g, '/');
  console.log(verifyOnly ? `Gate verificato senza scritture per ${decisionsRel}` : `Gate report scritto in ${reportRel}`);
  console.log(`Esito meccanico complessivo: ${allMechanicalPass ? 'PASS' : 'FAIL'}${signOff ? `, signed_off: ${report.signed_off}` : ''}`);
  if (!allMechanicalPass) process.exitCode = 1;
}

main();
