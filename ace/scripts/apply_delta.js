#!/usr/bin/env node
'use strict';

// Applica le operazioni di un batch curato ai file playbooks/*.md, ma solo
// se il gate report referenziato ha signed_off:true e all_mechanical_pass:true.
// Uso:
//   node ace/scripts/apply_delta.js <gate-report.json>
//
// Dopo l'applicazione, incatena retrieval.js (cosi' i file di istruzioni
// della piattaforma non restano mai disallineati in attesa di un run
// manuale dimenticato), poi sposta proposte + decisioni + report del
// batch in ace/proposals/applied/, cosi' non vengono ri-processati.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
const {
  REPO_ROOT, scopeToRelPath, parsePlaybookFile, serializeFile,
  stripEmptyPlaceholder, listPlaybookFiles, defaultPlaybookSkeleton, assertSafeWritePath,
  acquireMutationLock, computeReviewStateHash,
} = require('./lib/playbook');
const retrieval = require('./retrieval');

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function sha256File(p) {
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
}

function atomicWrite(targetPath, content) {
  assertSafeWritePath(targetPath);
  fs.mkdirSync(path.dirname(targetPath), { recursive: true });
  const temporary = `${targetPath}.${process.pid}.tmp`;
  fs.writeFileSync(temporary, content);
  fs.renameSync(temporary, targetPath);
}

function recoverPendingApplications() {
  const applicationsDir = path.join(REPO_ROOT, 'ace', 'state', 'applications');
  if (!fs.existsSync(applicationsDir)) return false;
  const pending = fs.readdirSync(applicationsDir)
    .filter((file) => file.endsWith('.json'))
    .map((file) => path.join(applicationsDir, file))
    .filter((file) => readJSON(file).status === 'applying');
  if (!pending.length) return false;
  for (const journalPath of pending) {
    const journal = readJSON(journalPath);
    for (const entry of journal.writes || []) {
      atomicWrite(path.join(REPO_ROOT, entry.path), entry.content);
    }
    retrieval.run({ checkOnly: false, verbose: true });
    for (const move of journal.moves || []) {
      const source = path.join(REPO_ROOT, move.source);
      const destination = path.join(REPO_ROOT, move.destination);
      if (!fs.existsSync(source)) continue;
      assertSafeWritePath(destination);
      fs.mkdirSync(path.dirname(destination), { recursive: true });
      fs.renameSync(source, destination);
    }
    atomicWrite(journalPath, `${JSON.stringify({
      ...journal,
      status: 'completed',
      completed_at: new Date().toISOString(),
    }, null, 2)}\n`);
    console.log(`Recuperata applicazione incompleta del batch ${journal.batch_id}.`);
  }
  return true;
}

function main() {
  const reportPathArg = process.argv[2];
  if (!reportPathArg) {
    console.error('Uso: node ace/scripts/apply_delta.js <gate-report.json>');
    process.exit(2);
  }
  const releaseLock = acquireMutationLock('apply_delta');
  process.once('exit', releaseLock);
  if (recoverPendingApplications()) {
    releaseLock();
    return;
  }

  const reportPath = path.resolve(reportPathArg);
  const reportRel = path.relative(REPO_ROOT, reportPath).replace(/\\/g, '/');
  if (reportRel.startsWith('../') || path.isAbsolute(reportRel)
      || !reportRel.startsWith('ace/proposals/') || reportRel.includes('/applied/')) {
    throw new Error('Il gate report deve trovarsi direttamente in ace/proposals/.');
  }
  const report = readJSON(reportPath);

  if (!report.signed_off) {
    console.error('Il gate report non è firmato (signed_off: false). Rilancia gate.js con --sign-off dopo revisione umana prima di applicare.');
    process.exit(1);
  }
  if (!report.all_mechanical_pass) {
    console.error('Il gate report segnala controlli meccanici falliti: rifiuto di procedere.');
    process.exit(1);
  }
  if (computeReviewStateHash() !== report.review_state_sha256) {
    console.error('Playbook, configurazione o stato live sono cambiati dopo il sign-off. Ripeti la revisione semantica e il gate.');
    process.exit(1);
  }

  const decisionsPath = path.resolve(REPO_ROOT, report.source_decisions_file);
  const decisionsRel = path.relative(REPO_ROOT, decisionsPath).replace(/\\/g, '/');
  if (decisionsRel.startsWith('../') || path.isAbsolute(decisionsRel)
      || !decisionsRel.startsWith('ace/proposals/') || decisionsRel.includes('/applied/')) {
    console.error('Il gate report riferisce un file decisioni fuori da ace/proposals/.');
    process.exit(1);
  }
  if (!fs.existsSync(decisionsPath) || sha256File(decisionsPath) !== report.source_decisions_sha256) {
    console.error('Il file decisioni è assente o è cambiato dopo il sign-off. Rilancia il gate e richiedi un nuovo sign-off umano.');
    process.exit(1);
  }
  const decisionsDoc = readJSON(decisionsPath);
  if (!decisionsDoc.source_proposals_file
      || path.basename(decisionsDoc.source_proposals_file) !== decisionsDoc.source_proposals_file) {
    console.error('source_proposals_file non è un nome file locale valido.');
    process.exit(1);
  }
  const proposalsPath = path.join(path.dirname(decisionsPath), decisionsDoc.source_proposals_file);
  if (!fs.existsSync(proposalsPath) || sha256File(proposalsPath) !== report.source_proposals_sha256) {
    console.error('Il file proposte è assente o è cambiato dopo il sign-off. Rilancia il gate e richiedi un nuovo sign-off umano.');
    process.exit(1);
  }
  const verification = spawnSync(
    process.execPath,
    [path.join(REPO_ROOT, 'ace', 'scripts', 'gate.js'), decisionsPath, '--verify-only'],
    { cwd: REPO_ROOT, encoding: 'utf8' },
  );
  if (verification.status !== 0) {
    console.error('Lo stato corrente non supera più il gate deterministico. Nessuna modifica applicata.');
    if (verification.stdout) console.error(verification.stdout.trim());
    if (verification.stderr) console.error(verification.stderr.trim());
    process.exit(1);
  }
  const proposalsDoc = fs.existsSync(proposalsPath) ? readJSON(proposalsPath) : { proposals: [] };
  const proposalsById = new Map(proposalsDoc.proposals.map((p) => [p.proposal_id, p]));

  const statusByProposal = new Map(report.results.map((r) => [r.proposal_id, r.mechanical_status]));
  const applicationsDir = path.join(REPO_ROOT, 'ace', 'state', 'applications');
  const applicationPath = path.join(applicationsDir, `${decisionsDoc.batch_id}.json`);
  if (fs.existsSync(applicationPath)) {
    console.error(`Il batch ${decisionsDoc.batch_id} è già completo o ha un'applicazione incompleta da recuperare manualmente: ${path.relative(REPO_ROOT, applicationPath)}.`);
    process.exit(1);
  }

  const touchedFiles = new Map(); // relPath -> parsed { prefix, bullets, suffix }

  function loadFile(relPath) {
    if (touchedFiles.has(relPath)) return touchedFiles.get(relPath);
    const abs = path.join(REPO_ROOT, relPath);
    // Un agente/family può ricevere il suo primo bullet in assoluto: in
    // quel caso non esiste ancora un file playbooks/<scope>.md da
    // leggere, e va creato al volo con lo scheletro standard invece di
    // fallire assumendo che esista sempre.
    const parsed = fs.existsSync(abs) ? parsePlaybookFile(fs.readFileSync(abs, 'utf8')) : defaultPlaybookSkeleton(relPath);
    touchedFiles.set(relPath, parsed);
    return parsed;
  }

  function findBullet(id, expectedRelPath) {
    // BUG STORICO (corretto qui): questa funzione cercava il bullet
    // scorrendo listPlaybookFiles() e si fermava al primo file in cui lo
    // trovava, ignorando completamente il final_scope della decisione. In
    // presenza di una collisione di ID tra due file (dovrebbe essere
    // impossibile, ma può succedere), questo faceva operare silenziosamente
    // sul bullet SBAGLIATO. Ora, se la decisione dichiara uno scope
    // (expectedRelPath), quel file viene controllato per primo e usato se
    // contiene l'ID: gate.js ha già verificato che questo sia sicuro
    // (nessuna ambiguità irrisolta) prima di firmare. Il fallback alla
    // ricerca globale resta solo per i casi in cui expectedRelPath non è
    // fornito (es. sorgenti di MERGE) o per compatibilità storica, ma
    // emette un avviso esplicito se usato dopo un miss sullo scope atteso,
    // invece di restare silenzioso.
    if (expectedRelPath) {
      const parsed = loadFile(expectedRelPath);
      const idx = parsed.bullets.findIndex((b) => b.id === id);
      if (idx !== -1) return { relPath: expectedRelPath, parsed, idx };
    }
    for (const relPath of listPlaybookFiles()) {
      if (relPath === expectedRelPath) continue; // già controllato sopra
      const parsed = loadFile(relPath);
      const idx = parsed.bullets.findIndex((b) => b.id === id);
      if (idx !== -1) {
        if (expectedRelPath) {
          console.error(`ATTENZIONE: bullet "${id}" atteso in "${expectedRelPath}" (da final_scope) ma non trovato lì; trovato invece in "${relPath}". Possibile collisione di ID o scope errato nella decisione: uso questo file come fallback, ma va verificato manualmente.`);
        }
        return { relPath, parsed, idx };
      }
    }
    return null;
  }

  function provenanceFor(decision) {
    const proposal = proposalsById.get(decision.proposal_id);
    const supporting = proposal ? (proposal.supporting_task_ids || []) : [];
    const parts = [];
    if (decision.merged_from && decision.merged_from.length) parts.push(`merged_from=[${decision.merged_from.join(', ')}]`);
    if (supporting.length) parts.push(`source_trace_ids=[${supporting.join(', ')}]`);
    parts.push(`created_at=${decisionsDoc.decided_at}`);
    parts.push('created_by=reflector+curator');
    parts.push(`batch_id=${decisionsDoc.batch_id}`);
    return parts.join('; ');
  }

  function appendUpdateProvenance(existing, decision) {
    return [
      existing,
      `updated_from=${decision.proposal_id}`,
      `updated_at=${decisionsDoc.decided_at}`,
      provenanceFor(decision),
    ].filter(Boolean).join('; ');
  }

  const applied = [];
  const skipped = [];

  for (const d of decisionsDoc.decisions) {
    if (d.operation === 'REJECT') {
      skipped.push({ proposal_id: d.proposal_id, reason: 'REJECT' });
      continue;
    }
    if (statusByProposal.get(d.proposal_id) !== 'PASS') {
      skipped.push({ proposal_id: d.proposal_id, reason: 'mechanical_status non PASS nel gate report' });
      continue;
    }

    if (d.operation === 'ADD') {
      const relPath = scopeToRelPath(d.final_scope);
      const parsed = loadFile(relPath);
      parsed.prefix = stripEmptyPlaceholder(parsed.prefix);
      parsed.bullets.push({
        id: d.target_bullet_id,
        status: d.initial_status || 'active',
        used: 0,
        helped: 0,
        hurt: 0,
        helped_confirmed: 0,
        helped_provisional: 0,
        hurt_confirmed: 0,
        hurt_provisional: 0,
        content: d.final_content,
        tags: [],
        provenance: provenanceFor(d),
      });
      applied.push({ proposal_id: d.proposal_id, operation: 'ADD', file: relPath, id: d.target_bullet_id });
      continue;
    }

    if (d.operation === 'UPDATE') {
      const expectedRel = d.final_scope ? scopeToRelPath(d.final_scope) : undefined;
      const found = findBullet(d.target_bullet_id, expectedRel);
      if (!found) { skipped.push({ proposal_id: d.proposal_id, reason: `bullet ${d.target_bullet_id} non trovato` }); continue; }
      found.parsed.bullets[found.idx].content = d.final_content;
      found.parsed.bullets[found.idx].provenance = appendUpdateProvenance(
        found.parsed.bullets[found.idx].provenance,
        d,
      );
      const targetRel = expectedRel || found.relPath;
      if (targetRel !== found.relPath) {
        const [moved] = found.parsed.bullets.splice(found.idx, 1);
        const newParsed = loadFile(targetRel);
        newParsed.prefix = stripEmptyPlaceholder(newParsed.prefix);
        newParsed.bullets.push(moved);
      }
      applied.push({ proposal_id: d.proposal_id, operation: 'UPDATE', file: targetRel, id: d.target_bullet_id });
      continue;
    }

    if (d.operation === 'PROMOTE') {
      const expectedRel = d.final_scope ? scopeToRelPath(d.final_scope) : undefined;
      const found = findBullet(d.target_bullet_id, expectedRel);
      if (!found) { skipped.push({ proposal_id: d.proposal_id, reason: `bullet ${d.target_bullet_id} non trovato` }); continue; }
      found.parsed.bullets[found.idx].status = 'active';
      found.parsed.bullets[found.idx].provenance = appendUpdateProvenance(
        found.parsed.bullets[found.idx].provenance,
        d,
      );
      applied.push({ proposal_id: d.proposal_id, operation: 'PROMOTE', file: found.relPath, id: d.target_bullet_id });
      continue;
    }

    if (d.operation === 'DEPRECATE') {
      const expectedRel = d.final_scope ? scopeToRelPath(d.final_scope) : undefined;
      const found = findBullet(d.target_bullet_id, expectedRel);
      if (!found) { skipped.push({ proposal_id: d.proposal_id, reason: `bullet ${d.target_bullet_id} non trovato` }); continue; }
      const [moved] = found.parsed.bullets.splice(found.idx, 1);
      moved.status = 'deprecated';
      moved.provenance = appendUpdateProvenance(moved.provenance, d);
      const archiveRel = path.join('playbooks', 'archive', path.basename(found.relPath));
      const archiveAbs = path.join(REPO_ROOT, archiveRel);
      let archiveParsed;
      if (touchedFiles.has(archiveRel)) {
        archiveParsed = touchedFiles.get(archiveRel);
      } else if (fs.existsSync(archiveAbs)) {
        archiveParsed = parsePlaybookFile(fs.readFileSync(archiveAbs, 'utf8'));
        touchedFiles.set(archiveRel, archiveParsed);
      } else {
        archiveParsed = {
          prefix: `# Archivio — ${path.basename(found.relPath, '.md')}\n\nBullet deprecated spostati qui da \`playbooks/${path.basename(found.relPath)}\`.`,
          bullets: [],
          suffix: '',
        };
        touchedFiles.set(archiveRel, archiveParsed);
      }
      archiveParsed.bullets.push(moved);
      applied.push({ proposal_id: d.proposal_id, operation: 'DEPRECATE', file: archiveRel, id: d.target_bullet_id });
      continue;
    }

    if (d.operation === 'MERGE') {
      const sourceIds = d.merged_from || [];
      const targets = sourceIds.map((id) => findBullet(id)).filter(Boolean);
      if (!targets.length) { skipped.push({ proposal_id: d.proposal_id, reason: 'nessun merged_from trovato' }); continue; }
      // Remove from the end of each file so indexes captured by findBullet
      // remain valid when multiple merge sources share the same playbook.
      const targetsByFile = new Map();
      for (const target of targets) {
        if (!targetsByFile.has(target.relPath)) targetsByFile.set(target.relPath, []);
        targetsByFile.get(target.relPath).push(target);
      }
      for (const fileTargets of targetsByFile.values()) {
        fileTargets.sort((a, b) => b.idx - a.idx);
        for (const target of fileTargets) {
          const [moved] = target.parsed.bullets.splice(target.idx, 1);
          moved.status = 'deprecated';
          const archiveRel = path.join('playbooks', 'archive', path.basename(target.relPath));
          let archiveParsed;
          if (touchedFiles.has(archiveRel)) {
            archiveParsed = touchedFiles.get(archiveRel);
          } else {
            const archiveAbs = path.join(REPO_ROOT, archiveRel);
            archiveParsed = fs.existsSync(archiveAbs)
              ? parsePlaybookFile(fs.readFileSync(archiveAbs, 'utf8'))
              : {
                prefix: `# Archivio — ${path.basename(target.relPath, '.md')}\n\nBullet deprecated o fusi provenienti da \`playbooks/${path.basename(target.relPath)}\`.`,
                bullets: [],
                suffix: '',
              };
            touchedFiles.set(archiveRel, archiveParsed);
          }
          archiveParsed.bullets.push(moved);
        }
      }
      const relPath = scopeToRelPath(d.final_scope);
      const parsed = loadFile(relPath);
      parsed.prefix = stripEmptyPlaceholder(parsed.prefix);
      parsed.bullets.push({
        id: d.target_bullet_id,
        status: d.initial_status || 'active',
        used: 0,
        helped: 0,
        hurt: 0,
        helped_confirmed: 0,
        helped_provisional: 0,
        hurt_confirmed: 0,
        hurt_provisional: 0,
        content: d.final_content,
        tags: [],
        provenance: provenanceFor(d),
      });
      applied.push({
        proposal_id: d.proposal_id, operation: 'MERGE', file: relPath, id: d.target_bullet_id, merged_from: sourceIds,
      });
      continue;
    }

    skipped.push({ proposal_id: d.proposal_id, reason: `operazione sconosciuta: ${d.operation}` });
  }

  assertSafeWritePath(applicationPath);
  const writes = [...touchedFiles.entries()].map(([relPath, parsed]) => ({
    path: relPath.replace(/\\/g, '/'),
    content: serializeFile(parsed.prefix, parsed.bullets, parsed.suffix),
  }));
  const appliedDir = path.join(REPO_ROOT, 'ace', 'proposals', 'applied');
  const moves = [proposalsPath, decisionsPath, reportPath].map((source) => ({
    source: path.relative(REPO_ROOT, source).replace(/\\/g, '/'),
    destination: path.relative(REPO_ROOT, path.join(appliedDir, path.basename(source))).replace(/\\/g, '/'),
  }));
  fs.mkdirSync(applicationsDir, { recursive: true });
  atomicWrite(applicationPath, `${JSON.stringify({
    batch_id: decisionsDoc.batch_id,
    decisions_sha256: report.source_decisions_sha256,
    status: 'applying',
    started_at: new Date().toISOString(),
    writes,
    moves,
  }, null, 2)}\n`);

  for (const entry of writes) {
    atomicWrite(path.join(REPO_ROOT, entry.path), entry.content);
  }

  if (touchedFiles.size > 0) {
    console.log('Playbook aggiornati: rilancio retrieval.js per risincronizzare i file di istruzioni della piattaforma...');
    retrieval.run({ checkOnly: false, verbose: true });
  }

  fs.mkdirSync(appliedDir, { recursive: true });
  for (const move of moves) {
    const source = path.join(REPO_ROOT, move.source);
    if (fs.existsSync(source)) {
      const destination = path.join(REPO_ROOT, move.destination);
      assertSafeWritePath(destination);
      fs.renameSync(source, destination);
    }
  }
  atomicWrite(applicationPath, `${JSON.stringify({
    batch_id: decisionsDoc.batch_id,
    decisions_sha256: report.source_decisions_sha256,
    status: 'completed',
    completed_at: new Date().toISOString(),
  }, null, 2)}\n`);
  releaseLock();

  console.log(`Applicate ${applied.length} operazioni, ${skipped.length} saltate.`);
  console.log('File playbook modificati:', [...touchedFiles.keys()].join(', ') || '(nessuno)');
  console.log('Batch spostato in ace/proposals/applied/.');
  if (skipped.length) {
    console.log('Saltate:', JSON.stringify(skipped, null, 2));
  }
}

main();
