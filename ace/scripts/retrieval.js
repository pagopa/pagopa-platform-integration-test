#!/usr/bin/env node
'use strict';

// Legge tutti i playbooks/*.md, applica il filtro di sicurezza, e
// sincronizza il risultato (solo id + content, mai contatori/provenance)
// nei file che la piattaforma dell'agente inietta/legge davvero. Quali
// file esattamente dipende dal progetto in cui ACE è installato — non è
// hardcoded qui, ma letto da config/project.json (vedi INSTALL_PROMPT_EMBEDDED.md):
// - i bullet di scope "global" vanno in `global_instructions_file` (es.
//   `.github/copilot-instructions.md` per Copilot, che lo legge in ogni
//   sessione automaticamente; o `CLAUDE.md` per Claude Code, stesso
//   meccanismo di auto-caricamento con nome diverso).
// - i bullet di scope "agent"/"family" vanno OGNUNO in un file dedicato
//   dentro `agent_instructions_dir`, perché iniettare tutto nel file
//   globale metterebbe i bullet di ogni agente nel contesto di TUTTI gli
//   altri (bloating), non solo di chi dovrebbe applicarli.
// - questi file dedicati in generale NON si auto-attaccano alla sessione
//   di un agente specifico (dipende dalla piattaforma: alcune supportano
//   un meccanismo di auto-attach su path/glob, altre no): il modo
//   affidabile e portabile è che ogni agente li legga esplicitamente
//   (es. con un tool di lettura file) come primo passo del proprio
//   workflow — vedi il passo iniettato dal wizard nei prompt degli agenti
//   e ace/README_EMBEDDED.md per il contratto generico.
//
// Uso:
//   node ace/scripts/retrieval.js            # scrive i file
//   node ace/scripts/retrieval.js --check    # stampa cosa cambierebbe, non scrive

const fs = require('fs');
const path = require('path');
const {
  REPO_ROOT, parsePlaybookFile, listPlaybookFiles, loadProjectConfig, loadAgentNames,
  enabledPlatforms, assertSafeWritePath,
} = require('./lib/playbook');

const BEGIN_MARKER = '<!-- ACE:BEGIN — generato da ace/scripts/retrieval.js, non modificare a mano tra questi marker -->';
const END_MARKER = '<!-- ACE:END -->';

// Stato persistito delle esclusioni live (hurt_confirmed > helped_confirmed,
// status persistito ancora "active"): senza questo file il curator non ha
// modo di scoprire queste esclusioni se non rileggendo a mano ogni playbook
// e ricalcolando la soglia da solo — questo file gliele consegna già pronte.
// Sovrascritto ad ogni run non--check; non è un log accumulativo, riflette
// solo lo stato live corrente.
const LIVE_EXCLUSIONS_STATE_PATH = path.join(REPO_ROOT, 'ace', 'state', 'live-exclusions.json');

// Soglia del filtro di sicurezza: un bullet con almeno MIN_SAMPLES usi e
// hurt_confirmed > helped_confirmed viene escluso immediatamente dal
// contesto servito, anche se il suo status persistito sui file è ancora
// "active" (lo status persistito si aggiorna solo al prossimo batch
// curator/apply_delta; questo controllo live esiste apposta per non
// aspettare quel batch). Confronta solo i contatori _confirmed (evidenza
// verificata/confermata esternamente — vedi bullet.schema.json e
// trace.schema.json, outcome.evaluated_by), non helped/hurt grezzi: un
// bullet con solo evidenza provvisoria (self-report immediato, es.
// '<team>-auto') non viene mai escluso live da solo, per costruzione —
// serve un segnale reale, non basta un'autovalutazione a caldo.
const MIN_SAMPLES_FOR_LIVE_EXCLUSION = 5;

function scopeKeyFromRelPath(relPath) {
  const base = path.basename(relPath, '.md');
  if (relPath.includes(`${path.sep}families${path.sep}`) || relPath.includes('/families/')) {
    return `family:${base}`;
  }
  return base; // "_global", "<orchestrator_agent>", "<subagent>", ecc.
}

function collectBullets() {
  const byScope = new Map(); // scopeKey -> [{id, content}]
  const excluded = []; // { id, scope, reason }

  for (const relPath of listPlaybookFiles()) {
    const raw = fs.readFileSync(path.join(REPO_ROOT, relPath), 'utf8');
    const { bullets } = parsePlaybookFile(raw);
    const scopeKey = scopeKeyFromRelPath(relPath);

    for (const b of bullets) {
      if (b.status === 'deprecated') {
        excluded.push({ id: b.id, scope: scopeKey, reason: 'status=deprecated' });
        continue;
      }
      if (b.status === 'quarantined') {
        excluded.push({ id: b.id, scope: scopeKey, reason: 'status=quarantined' });
        continue;
      }
      if (b.used >= MIN_SAMPLES_FOR_LIVE_EXCLUSION && b.hurt_confirmed > b.helped_confirmed) {
        excluded.push({
          id: b.id,
          scope: scopeKey,
          reason: `esclusione live: used=${b.used} hurt_confirmed=${b.hurt_confirmed} > helped_confirmed=${b.helped_confirmed} (grezzi: hurt=${b.hurt} helped=${b.helped}; soglia campioni: ${MIN_SAMPLES_FOR_LIVE_EXCLUSION}) — segnalare al prossimo batch curator per DEPRECATE/quarantena formale`,
        });
        continue;
      }
      if (!byScope.has(scopeKey)) byScope.set(scopeKey, []);
      byScope.get(scopeKey).push({ id: b.id, content: b.content });
    }
  }

  return { byScope, excluded };
}

function renderBulletList(bullets) {
  return bullets.map((b) => `- **[${b.id}]** ${b.content.replace(/\n+/g, ' ')}`).join('\n');
}

function renderGlobalBlock(bullets, teamName) {
  const preamble = [
    '## Lezioni operative ACE (playbook globale)',
    '',
    `Generato automaticamente da \`ace/scripts/retrieval.js\` a partire da \`playbooks/_global.md\`. Si applica all'orchestratore e a tutti gli agenti partecipanti${teamName ? ` del team ${teamName}` : ''}. Se applichi una di queste lezioni, citane l'id tra parentesi quadre (es. \`[P-003]\`).`,
    '',
  ].join('\n');
  if (!bullets || !bullets.length) return `${preamble}\n_Nessun bullet attivo al momento della generazione._`;
  return `${preamble}\n${renderBulletList(bullets)}`;
}

function renderAgentBlock(scopeKey, bullets) {
  const label = scopeKey.startsWith('family:') ? `family "${scopeKey.slice(7)}"` : `\`${scopeKey}\``;
  const preamble = [
    `## Lezioni operative ACE per ${label}`,
    '',
    `Generato automaticamente da \`ace/scripts/retrieval.js\` a partire da \`playbooks/${scopeKey.startsWith('family:') ? `families/${scopeKey.slice(7)}` : scopeKey}.md\`. Non auto-iniettato dalla piattaforma: va letto esplicitamente (vedi il passo dedicato nel workflow dell'agente). Se applichi una di queste lezioni, citane l'id tra parentesi quadre (es. \`[P-002]\`).`,
    '',
  ].join('\n');
  if (!bullets || !bullets.length) return `${preamble}\n_Nessun bullet attivo al momento della generazione._`;
  return `${preamble}\n${renderBulletList(bullets)}`;
}

function syncMarkedFile(absPath, block, checkOnly) {
  assertSafeWritePath(absPath);
  const existing = fs.existsSync(absPath) ? fs.readFileSync(absPath, 'utf8') : '';
  const wrapped = `${BEGIN_MARKER}\n\n${block}\n\n${END_MARKER}`;

  let next;
  const beginIdx = existing.indexOf(BEGIN_MARKER);
  const endIdx = existing.indexOf(END_MARKER);
  if (beginIdx !== -1 && endIdx !== -1 && endIdx > beginIdx) {
    next = existing.slice(0, beginIdx) + wrapped + existing.slice(endIdx + END_MARKER.length);
  } else if (existing.trim() === '') {
    next = `${wrapped}\n`;
  } else {
    next = `${existing.replace(/\s+$/, '')}\n\n${wrapped}\n`;
  }

  const changed = next !== existing;
  if (checkOnly) return changed;
  if (changed) {
    fs.mkdirSync(path.dirname(absPath), { recursive: true });
    fs.writeFileSync(absPath, next);
  }
  return changed;
}

function removeMarkedBlock(absPath, checkOnly, unlinkWhenEmpty = false) {
  assertSafeWritePath(absPath);
  if (!fs.existsSync(absPath)) return false;
  const existing = fs.readFileSync(absPath, 'utf8');
  const beginIdx = existing.indexOf(BEGIN_MARKER);
  const endIdx = existing.indexOf(END_MARKER);
  if (beginIdx === -1 || endIdx < beginIdx) return false;
  let before = existing.slice(0, beginIdx);
  let after = existing.slice(endIdx + END_MARKER.length);

  // Remove only the separator added around the generated block. Everything
  // else, including fenced content and repeated blank lines, is project-owned.
  const precedingSeparator = /(\r?\n)(\r?\n)$/.exec(before);
  if (precedingSeparator) before = before.slice(0, -precedingSeparator[2].length);
  const followingBreak = /^(\r?\n)/.exec(after);
  if (followingBreak) after = after.slice(followingBreak[1].length);
  const needsSeam = before && after && !/\r?\n$/.test(before) && !/^\r?\n/.test(after);
  const rendered = `${before}${needsSeam ? (followingBreak?.[1] || '\n') : ''}${after}`;
  if (!checkOnly) {
    if (rendered) fs.writeFileSync(absPath, rendered);
    else if (unlinkWhenEmpty) fs.unlinkSync(absPath);
    else fs.writeFileSync(absPath, '');
  }
  return true;
}

function instructionsPathFor(scopeKey, agentInstructionsDir) {
  const name = scopeKey.startsWith('family:') ? `ace-family-${scopeKey.slice(7)}` : `ace-${scopeKey}`;
  return path.join(REPO_ROOT, agentInstructionsDir, `${name}.instructions.md`);
}

function globalInstructionsPath(platform, integrationMode) {
  return integrationMode === 'mediated'
    ? path.join(REPO_ROOT, platform.agent_instructions_dir, 'ace-global.instructions.md')
    : path.join(REPO_ROOT, platform.global_instructions_file);
}

// Filtra solo le esclusioni "live" (le uniche non già visibili leggendo lo
// `status` persistito sul bullet) e le persiste per il curator (vedi
// prompts/curator.md, sezione Input) — non scrive nulla in --check.
function writeLiveExclusionsState(excluded, checkOnly) {
  const liveOnly = excluded.filter((e) => e.reason.startsWith('esclusione live'));
  if (checkOnly) return;
  const state = { generated_at: new Date().toISOString(), live_exclusions: liveOnly };
  fs.mkdirSync(path.dirname(LIVE_EXCLUSIONS_STATE_PATH), { recursive: true });
  fs.writeFileSync(LIVE_EXCLUSIONS_STATE_PATH, `${JSON.stringify(state, null, 2)}\n`);
}

// Riutilizzabile da altri script (es. apply_delta.js, che la incatena in
// automatico dopo aver scritto i playbook, per non lasciare mai i file
// generati disallineati in attesa di un run manuale dimenticato).
function run({ checkOnly = false, verbose = true } = {}) {
  const config = loadProjectConfig();
  const agentScopes = loadAgentNames();

  const { byScope, excluded } = collectBullets();
  writeLiveExclusionsState(excluded, checkOnly);

  const totalIncluded = [...byScope.values()].reduce((n, arr) => n + arr.length, 0);
  if (verbose) {
    console.log(`Bullet inclusi: ${totalIncluded}`);
    if (excluded.length) {
      console.log('Bullet esclusi:');
      for (const e of excluded) console.log(`  - [${e.id}] (${e.scope}): ${e.reason}`);
    }
  }

  const changedFiles = [];
  const configuredFamilyKeys = Object.values(config.agent_families || {})
    .flat()
    .map((family) => `family:${family}`);
  const familyKeys = listPlaybookFiles()
    .filter((relativePath) => relativePath.replace(/\\/g, '/').startsWith('playbooks/families/'))
    .map(scopeKeyFromRelPath);
  const agentAndFamilyKeys = [...new Set([
    ...agentScopes,
    ...familyKeys,
    ...configuredFamilyKeys,
  ])];

  for (const platform of enabledPlatforms(config)) {
    const mode = config.integration_mode || 'embedded';
    if (mode === 'mediated') {
      const platformGlobalPath = path.join(REPO_ROOT, platform.global_instructions_file);
      if (removeMarkedBlock(platformGlobalPath, checkOnly)) {
        changedFiles.push(path.relative(REPO_ROOT, platformGlobalPath));
      }
    } else {
      const staleMediatedPath = globalInstructionsPath(platform, 'mediated');
      if (removeMarkedBlock(staleMediatedPath, checkOnly, true)) {
        changedFiles.push(path.relative(REPO_ROOT, staleMediatedPath));
      }
    }
    const globalPath = globalInstructionsPath(platform, mode);
    const globalChanged = syncMarkedFile(
      globalPath,
      renderGlobalBlock(byScope.get('_global'), config.team_name),
      checkOnly,
    );
    if (globalChanged) changedFiles.push(path.relative(REPO_ROOT, globalPath));

    for (const scopeKey of agentAndFamilyKeys) {
      const bullets = byScope.get(scopeKey) || [];
      const targetPath = instructionsPathFor(scopeKey, platform.agent_instructions_dir);
      const changed = syncMarkedFile(targetPath, renderAgentBlock(scopeKey, bullets), checkOnly);
      if (changed) changedFiles.push(path.relative(REPO_ROOT, targetPath));
    }
  }

  if (verbose) {
    if (checkOnly) {
      console.log(changedFiles.length
        ? `File che cambierebbero (--check, nessuna scrittura eseguita): ${changedFiles.map((f) => f.replace(/\\/g, '/')).join(', ')}`
        : 'Nessuna modifica necessaria.');
    } else {
      console.log(changedFiles.length
        ? `Sincronizzati: ${changedFiles.map((f) => f.replace(/\\/g, '/')).join(', ')}`
        : 'Nessuna modifica necessaria.');
    }
  }

  return changedFiles;
}

module.exports = {
  collectBullets, globalInstructionsPath, instructionsPathFor, run,
};

if (require.main === module) {
  run({ checkOnly: process.argv.includes('--check') });
}
