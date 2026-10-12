'use strict';

// Helper condiviso da gate.js, apply_delta.js, retrieval.js, update_counters.js
// e check_threshold.js: legge/scrive i file playbooks/*.md nel formato
// bullet documentato in ogni playbook (intestazione HTML "Formato
// bullet"), e legge la configurazione di progetto (config/project.json)
// che rende questi script riusabili su progetti diversi senza toccare il
// codice. Non contiene logica di retrieval/injection: solo parsing e
// serializzazione del formato su disco + accesso alla config.

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const REPO_ROOT = path.resolve(__dirname, '..', '..', '..');
const ACE_ROOT = path.resolve(__dirname, '..', '..');
const SCHEMA_PATH = path.join(ACE_ROOT, 'schema', 'bullet.schema.json');
const PROJECT_CONFIG_PATH = path.join(ACE_ROOT, 'config', 'project.json');
const SAFE_SCOPE_ID_RE = /^[a-z0-9][a-z0-9._-]*$/;

function loadBulletSchema() {
  return JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf8'));
}

// Unica fonte di verità per nomi/percorsi specifici del progetto in cui
// ACE è stato installato (vedi INSTALL_PROMPT_EMBEDDED.md). Se un valore è ancora
// un placeholder non risolto (installazione non completata), lo segnala
// chi chiama tramite isUnresolvedPlaceholder(), non questa funzione: qui
// ci limitiamo a leggere il file cosi' com'e'. Nota: nessun commento di
// questo file contiene un token di placeholder letterale, altrimenti la
// verifica finale dell'installazione (grep dei placeholder residui in
// ace/ e playbooks/, vedi INSTALL_PROMPT_EMBEDDED.md Fase 10) darebbe un falso
// positivo permanente su scripts/lib/playbook.js.
function loadProjectConfig() {
  if (!fs.existsSync(PROJECT_CONFIG_PATH)) {
    throw new Error(`config/project.json non trovato in ${PROJECT_CONFIG_PATH}. Esegui prima il wizard di installazione appropriato.`);
  }
  const config = JSON.parse(fs.readFileSync(PROJECT_CONFIG_PATH, 'utf8'));
  validateProjectConfig(config);
  return config;
}

function isUnresolvedPlaceholder(value) {
  return typeof value === 'string' && /^__[A-Z0-9_]+__$/.test(value);
}

function assertSafeWritePath(targetPath) {
  const absolute = path.resolve(targetPath);
  const relative = path.relative(REPO_ROOT, absolute);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`Percorso di scrittura fuori dal progetto: ${targetPath}`);
  }
  let current = REPO_ROOT;
  for (const segment of relative.split(path.sep).filter(Boolean)) {
    current = path.join(current, segment);
    if (!fs.existsSync(current)) break;
    if (fs.lstatSync(current).isSymbolicLink()) {
      throw new Error(`Percorso di scrittura con link simbolico non consentito: ${current}`);
    }
  }
  return absolute;
}

function acquireMutationLock(owner) {
  const lockPath = path.join(ACE_ROOT, 'state', 'write.lock');
  assertSafeWritePath(lockPath);
  const pendingCounterJournal = path.join(ACE_ROOT, 'state', 'counter-update.json');
  if (owner !== 'update_counters' && fs.existsSync(pendingCounterJournal)) {
    throw new Error('Esiste un aggiornamento contatori incompleto. Esegui update_counters.js per recuperarlo prima di altre scritture ACE.');
  }
  const applicationsDir = path.join(ACE_ROOT, 'state', 'applications');
  if (fs.existsSync(applicationsDir)) {
    const incomplete = fs.readdirSync(applicationsDir)
      .filter((file) => file.endsWith('.json'))
      .map((file) => path.join(applicationsDir, file))
      .filter((file) => {
        try {
          return JSON.parse(fs.readFileSync(file, 'utf8')).status === 'applying';
        } catch {
          return true;
        }
      });
    if (incomplete.length && owner !== 'apply_delta') {
      throw new Error(`Esiste un'applicazione ACE incompleta: ${incomplete.join(', ')}. Recuperala manualmente prima di altre scritture.`);
    }
  }
  fs.mkdirSync(path.dirname(lockPath), { recursive: true });
  let descriptor;
  try {
    descriptor = fs.openSync(lockPath, 'wx');
  } catch (error) {
    if (error.code === 'EEXIST') {
      throw new Error(`ACE mutation lock already exists at ${lockPath}. Verify that no writer is running; remove it only after recovering any pending journal/application.`);
    }
    throw error;
  }
  fs.writeFileSync(descriptor, `${JSON.stringify({
    owner,
    pid: process.pid,
    acquired_at: new Date().toISOString(),
  }, null, 2)}\n`);
  fs.closeSync(descriptor);

  let released = false;
  return () => {
    if (released) return;
    released = true;
    if (fs.existsSync(lockPath)) fs.unlinkSync(lockPath);
  };
}

// Nomi di agente validi per questo progetto (orchestratore + subagenti),
// unica fonte di verità per lo scope.agent dei bullet/trace — sostituisce
// l'enum fisso che una versione precedente di questo schema aveva
// hardcoded (accoppiava lo schema al singolo progetto in cui è nato).
function enabledPlatforms(config) {
  return Object.entries(config.platforms || {})
    .filter(([, platform]) => platform && platform.enabled)
    .map(([name, platform]) => ({ name, ...platform }));
}

function validateProjectConfig(config) {
  if (!config || config.version !== 1) {
    throw new Error('config/project.json deve avere version: 1.');
  }
  const integrationMode = config.integration_mode || 'embedded';
  if (!['embedded', 'mediated'].includes(integrationMode)) {
    throw new Error('config/project.json: integration_mode deve essere embedded o mediated.');
  }
  if (!config.team_name || isUnresolvedPlaceholder(config.team_name)) {
    throw new Error('config/project.json richiede team_name risolto.');
  }
  if (!/^[a-z0-9][a-z0-9._-]*-auto$/.test(config.provisional_evaluator || '')
      || isUnresolvedPlaceholder(config.provisional_evaluator)) {
    throw new Error('config/project.json richiede provisional_evaluator nel formato <slug>-auto.');
  }
  if (!config.orchestrator_agent || isUnresolvedPlaceholder(config.orchestrator_agent)) {
    throw new Error('config/project.json richiede orchestrator_agent risolto.');
  }
  if (!Array.isArray(config.participating_agents)) {
    throw new Error('config/project.json richiede participating_agents come array.');
  }
  const invalidAgents = [config.orchestrator_agent, ...config.participating_agents]
    .filter((name) => !SAFE_SCOPE_ID_RE.test(name));
  if (invalidAgents.length) {
    throw new Error(`config/project.json contiene id agente non sicuri per i nomi file: ${invalidAgents.join(', ')}.`);
  }
  const duplicateAgents = config.participating_agents.filter(
    (name, index, all) => all.indexOf(name) !== index,
  );
  if (duplicateAgents.length) {
    throw new Error(`config/project.json contiene agenti duplicati: ${[...new Set(duplicateAgents)].join(', ')}.`);
  }
  if (config.agent_families !== undefined) {
    if (!config.agent_families || typeof config.agent_families !== 'object' || Array.isArray(config.agent_families)) {
      throw new Error('config/project.json: agent_families deve essere un oggetto.');
    }
    const validAgents = new Set([config.orchestrator_agent, ...config.participating_agents]);
    for (const [agent, families] of Object.entries(config.agent_families)) {
      if (!validAgents.has(agent)) {
        throw new Error(`config/project.json: agent_families contiene un agente non configurato: ${agent}.`);
      }
      if (!Array.isArray(families) || families.some((family) => !SAFE_SCOPE_ID_RE.test(family))) {
        throw new Error(`config/project.json: family non valida per ${agent}.`);
      }
    }
  }
  const platforms = enabledPlatforms(config);
  if (!platforms.length) {
    throw new Error('config/project.json deve abilitare almeno una piattaforma.');
  }
  for (const platform of platforms) {
    if (!['copilot', 'claude'].includes(platform.name)) {
      throw new Error(`config/project.json abilita una piattaforma non supportata: ${platform.name}.`);
    }
    for (const key of ['agents_dir', 'global_instructions_file', 'agent_instructions_dir']) {
      if (!platform[key] || isUnresolvedPlaceholder(platform[key])) {
        throw new Error(`config/project.json: platforms.${platform.name}.${key} mancante o non risolto.`);
      }
      const resolved = path.resolve(REPO_ROOT, platform[key]);
      if (path.isAbsolute(platform[key]) || (resolved !== REPO_ROOT && !resolved.startsWith(`${REPO_ROOT}${path.sep}`))) {
        throw new Error(`config/project.json: platforms.${platform.name}.${key} deve essere un percorso relativo interno al progetto.`);
      }
    }
    if (!/^[a-z0-9][a-z0-9-]*$/.test(platform.runtime_prefix || '')) {
      throw new Error(`config/project.json: platforms.${platform.name}.runtime_prefix non valido.`);
    }
    const canonicalAgents = config.participating_agents;
    if (platform.canonical_to_runtime !== undefined
        && (integrationMode === 'mediated' || Object.keys(platform.canonical_to_runtime).length)) {
      if (!platform.canonical_to_runtime
          || typeof platform.canonical_to_runtime !== 'object'
          || Array.isArray(platform.canonical_to_runtime)) {
        throw new Error(`config/project.json: ${platform.name}.canonical_to_runtime deve essere un oggetto.`);
      }
      const keys = Object.keys(platform.canonical_to_runtime);
      const missing = canonicalAgents.filter((agent) => !keys.includes(agent));
      const extra = keys.filter((agent) => !canonicalAgents.includes(agent));
      const values = keys.map((agent) => platform.canonical_to_runtime[agent]);
      if (missing.length || extra.length
          || values.some((value) => typeof value !== 'string' || !value.trim() || isUnresolvedPlaceholder(value))
          || new Set(values).size !== values.length) {
        throw new Error(`config/project.json: ${platform.name}.canonical_to_runtime deve mappare esattamente ogni id canonico a un runtime id univoco.`);
      }
    } else if (integrationMode === 'mediated') {
      throw new Error(`config/project.json: ${platform.name}.canonical_to_runtime è obbligatorio in modalità mediated.`);
    }
    if (platform.orchestrator_entrypoints !== undefined
        && (integrationMode === 'mediated'
          || Object.values(platform.orchestrator_entrypoints || {}).some(Boolean))) {
      const entrypoints = platform.orchestrator_entrypoints;
      if (!entrypoints || typeof entrypoints !== 'object' || Array.isArray(entrypoints)
          || !['project', 'ace'].every((key) => typeof entrypoints[key] === 'string'
            && entrypoints[key].trim() && !isUnresolvedPlaceholder(entrypoints[key]))
          || entrypoints.project === entrypoints.ace) {
        throw new Error(`config/project.json: ${platform.name}.orchestrator_entrypoints richiede entrypoint project e ace distinti.`);
      }
      if (integrationMode === 'mediated'
          && entrypoints.ace !== `${entrypoints.project}-ace`) {
        throw new Error(`config/project.json: ${platform.name}.orchestrator_entrypoints.ace deve essere l'entrypoint project con suffisso -ace.`);
      }
      if (integrationMode === 'mediated'
          && Object.values(platform.canonical_to_runtime).some(
            (runtime) => runtime === entrypoints.project || runtime === entrypoints.ace,
          )) {
        throw new Error(`config/project.json: ${platform.name} non può mappare un worker su un entrypoint orchestratore.`);
      }
    } else if (integrationMode === 'mediated') {
      throw new Error(`config/project.json: ${platform.name}.orchestrator_entrypoints è obbligatorio in modalità mediated.`);
    }
    if (!platform.tools || !['reflector', 'curator', 'warden'].every(
      (role) => Array.isArray(platform.tools[role]) && platform.tools[role].length,
    )) {
      throw new Error(`config/project.json: tools ACE incompleti per la piattaforma ${platform.name}.`);
    }
    for (const role of ['reflector', 'curator', 'warden']) {
      const tools = platform.tools[role];
      if (tools.some((tool) => typeof tool !== 'string' || !tool.trim())) {
        throw new Error(`config/project.json: tool non valido per ${platform.name}/${role}.`);
      }
      if (new Set(tools).size !== tools.length) {
        throw new Error(`config/project.json: tool duplicati per ${platform.name}/${role}.`);
      }
    }
    const delegationTools = platform.name === 'claude' ? ['Agent'] : ['agent', 'task'];
    for (const role of ['reflector', 'curator']) {
      if (!platform.tools[role].some((tool) => delegationTools.includes(tool))) {
        throw new Error(`config/project.json: ${platform.name}/${role} richiede un tool di delega.`);
      }
    }
    const questionTools = platform.name === 'claude'
      ? ['AskUserQuestion']
      : ['ask_user', 'vscode/askQuestions'];
    if (!platform.tools.warden.some((tool) => questionTools.includes(tool))) {
      throw new Error(`config/project.json: ${platform.name}/warden richiede un tool domanda dedicato.`);
    }
    const shellTools = platform.name === 'claude' ? ['Bash'] : ['powershell', 'bash', 'execute'];
    for (const role of ['reflector', 'curator', 'warden']) {
      if (!platform.tools[role].some((tool) => shellTools.includes(tool))) {
        throw new Error(`config/project.json: ${platform.name}/${role} richiede un tool shell.`);
      }
    }
  }
}

function loadAgentNames() {
  const config = loadProjectConfig();
  const names = [config.orchestrator_agent, ...config.participating_agents];
  const unresolved = names.filter(isUnresolvedPlaceholder);
  if (unresolved.length) {
    throw new Error(`config/project.json ha ancora placeholder non risolti negli agenti: ${unresolved.join(', ')}. Completa il wizard di installazione prima di eseguire questo script.`);
  }
  return [...new Set(names)];
}

const BULLET_FORMAT_COMMENT = [
  '<!--',
  'Formato bullet (scritto da ace/scripts/apply_delta.js, non a mano):',
  '',
  '## P-XXX — active|quarantined|deprecated — used:N helped:N hurt:N',
  'Contenuto operativo della lezione, in forma imperativa, specifico',
  'a questo progetto. Non ovvio per un professionista generico del dominio.',
  '',
  'tags: [tag1, tag2]',
  'counters: helped_confirmed=N; helped_provisional=N; hurt_confirmed=N; hurt_provisional=N',
  'provenance: source_trace_ids=[...]; created_at=...; created_by=reflector+curator; batch_id=...',
  '',
  'Tag, counters e provenance sono sempre presenti sui bullet reali (anche',
  'tags: [] se non servono tag fini) — servono al retrieval e all\'audit, non',
  'vanno iniettati nel contesto dell\'agente che lavora (solo id + content).',
  'counters distingue evidenza confermata da provvisoria (vedi',
  'ace/schema/bullet.schema.json, counters.helped_confirmed/helped_provisional/',
  'hurt_confirmed/hurt_provisional) e guida le decisioni strutturali del',
  'curator (DEPRECATE/PROMOTE/baking) — used/helped/hurt nell\'intestazione',
  'restano un aggregato storico retrocompatibile, non usato da solo per',
  'quelle decisioni.',
  '-->',
].join('\n');

// Usato da apply_delta.js quando un'operazione ADD/MERGE assegna il primo
// bullet a uno scope che non ha ancora un file playbook (es. un agente
// coinvolto nel ciclo ACE per la prima volta): senza questo fallback lo
// script andrebbe in errore assumendo che il file esista già, invece di
// crearlo al bisogno come già fa per playbooks/archive/*.md.
function defaultPlaybookSkeleton(relPath) {
  const base = path.basename(relPath, '.md');
  const isFamily = relPath.includes(`${path.sep}families${path.sep}`) || relPath.includes('/families/');
  const title = base === '_global' ? 'Playbook globale' : (isFamily ? `Playbook family — ${base}` : `Playbook — ${base}`);
  return {
    prefix: `# ${title}\n\n_Creato automaticamente da apply_delta.js al primo bullet assegnato a questo scope — nessun bullet reale ancora prima di questo._`,
    bullets: [],
    suffix: BULLET_FORMAT_COMMENT,
  };
}

function scopeToRelPath(scope) {
  if (!scope || !scope.type) throw new Error('scope.type mancante');
  if (scope.type === 'global') return path.join('playbooks', '_global.md');
  if (scope.type === 'agent') {
    if (!scope.agent) throw new Error("scope.agent mancante per scope.type='agent'");
    if (!SAFE_SCOPE_ID_RE.test(scope.agent)) throw new Error(`scope.agent non sicuro: ${scope.agent}`);
    return path.join('playbooks', `${scope.agent}.md`);
  }
  if (scope.type === 'family') {
    if (!scope.family) throw new Error("scope.family mancante per scope.type='family'");
    if (!SAFE_SCOPE_ID_RE.test(scope.family)) throw new Error(`scope.family non sicuro: ${scope.family}`);
    return path.join('playbooks', 'families', `${scope.family}.md`);
  }
  throw new Error(`scope.type sconosciuto: ${scope.type}`);
}

const BULLET_HEADING_RE = /^## (P-\d+) — (active|quarantined|deprecated) — used:(\d+) helped:(\d+) hurt:(\d+)\s*$/;

// Contatori a due livelli (vedi bullet.schema.json, counters.helped_confirmed/
// helped_provisional/hurt_confirmed/hurt_provisional): persistiti in una riga
// `counters:` dedicata, separata dall'intestazione `used:/helped:/hurt:`, per
// restare additivi e retrocompatibili — un bullet scritto prima di questa
// modifica non ha questa riga e va letto con questi 4 contatori a 0, non
// mancanti/undefined, così scripts/update_counters.js e scripts/retrieval.js
// possono sempre sommare/confrontare senza controlli di presenza.
const DEFAULT_TIERED_COUNTERS = {
  helped_confirmed: 0, helped_provisional: 0, hurt_confirmed: 0, hurt_provisional: 0,
};

function parseCountersLine(inner) {
  const result = { ...DEFAULT_TIERED_COUNTERS };
  for (const part of inner.split(';')) {
    const m = /^\s*([a-z_]+)\s*=\s*(-?\d+)\s*$/.exec(part);
    if (!m) continue;
    const [, key, value] = m;
    if (Object.prototype.hasOwnProperty.call(result, key)) result[key] = Number(value);
  }
  return result;
}

// Un file playbook è: prefisso (intro/prosa) + zero o più bullet + suffisso
// (il commento HTML "Formato bullet", sempre in fondo, preservato invariato).
function parsePlaybookFile(raw) {
  const lines = raw.split(/\r?\n/);
  const firstBulletIdx = lines.findIndex((l) => BULLET_HEADING_RE.test(l));
  const commentIdx = lines.findIndex((l) => l.trim().startsWith('<!--'));

  const prefixEnd = firstBulletIdx !== -1 ? firstBulletIdx : (commentIdx !== -1 ? commentIdx : lines.length);
  const suffixStart = commentIdx !== -1 && commentIdx >= prefixEnd ? commentIdx : lines.length;

  const prefixLines = lines.slice(0, prefixEnd);
  const bulletLines = lines.slice(prefixEnd, suffixStart);
  const suffixLines = lines.slice(suffixStart);

  const bullets = [];
  let current = null;
  for (const line of bulletLines) {
    const m = BULLET_HEADING_RE.exec(line);
    if (m) {
      if (current) bullets.push(finalizeBullet(current));
      current = {
        id: m[1], status: m[2],
        used: Number(m[3]), helped: Number(m[4]), hurt: Number(m[5]),
        ...DEFAULT_TIERED_COUNTERS,
        contentLines: [], tags: [], provenance: null,
      };
    } else if (current) {
      const trimmed = line.trim();
      if (trimmed.startsWith('tags:')) {
        current.tags = parseInlineArray(trimmed.slice('tags:'.length).trim());
      } else if (trimmed.startsWith('counters:')) {
        Object.assign(current, parseCountersLine(trimmed.slice('counters:'.length).trim()));
      } else if (trimmed.startsWith('provenance:')) {
        current.provenance = trimmed.slice('provenance:'.length).trim();
      } else {
        current.contentLines.push(line);
      }
    }
  }
  if (current) bullets.push(finalizeBullet(current));

  return {
    prefix: prefixLines.join('\n'),
    bullets,
    suffix: suffixLines.join('\n'),
  };
}

function finalizeBullet(b) {
  while (b.contentLines.length && b.contentLines[0].trim() === '') b.contentLines.shift();
  while (b.contentLines.length && b.contentLines[b.contentLines.length - 1].trim() === '') b.contentLines.pop();
  b.content = b.contentLines.join('\n');
  delete b.contentLines;
  return b;
}

function parseInlineArray(inner) {
  const m = /^\[(.*)\]$/.exec(inner);
  if (!m || !m[1].trim()) return [];
  return m[1].split(',').map((s) => s.trim()).filter(Boolean);
}

function bulletToMarkdown(b) {
  const heading = `## ${b.id} — ${b.status} — used:${b.used} helped:${b.helped} hurt:${b.hurt}`;
  const tagsLine = `tags: [${(b.tags || []).join(', ')}]`;
  const countersLine = `counters: helped_confirmed=${b.helped_confirmed || 0}; helped_provisional=${b.helped_provisional || 0}; hurt_confirmed=${b.hurt_confirmed || 0}; hurt_provisional=${b.hurt_provisional || 0}`;
  const provenanceLine = `provenance: ${b.provenance || ''}`;
  return [heading, '', b.content, '', tagsLine, countersLine, provenanceLine].join('\n');
}

// Rimuove il paragrafo placeholder "vuoto per ora / il playbook parte
// vuoto" quando si aggiunge il primo bullet reale a un file.
function stripEmptyPlaceholder(prefix) {
  const lines = prefix.split('\n');
  const idx = lines.findIndex((l) => l.includes('nessun bullet reale'));
  if (idx === -1) return prefix;
  let end = idx;
  while (end + 1 < lines.length && lines[end + 1].trim() !== '') end += 1;
  lines.splice(idx, end - idx + 1);
  return lines.join('\n').replace(/\n{3,}/g, '\n\n');
}

function serializeFile(prefix, bullets, suffix) {
  const trimmedPrefix = prefix.replace(/\s+$/, '');
  const bulletsBlock = bullets.map(bulletToMarkdown).join('\n\n');
  const trimmedSuffix = (suffix || '').replace(/^\s+/, '');
  const sections = [trimmedPrefix];
  if (bulletsBlock) sections.push(bulletsBlock);
  if (trimmedSuffix) sections.push(trimmedSuffix);
  return `${sections.join('\n\n')}\n`;
}

function listPlaybookFiles() {
  const dir = path.join(REPO_ROOT, 'playbooks');
  const result = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith('.md')) result.push(path.join('playbooks', entry.name));
  }
  const familiesDir = path.join(dir, 'families');
  if (fs.existsSync(familiesDir)) {
    for (const f of fs.readdirSync(familiesDir)) {
      if (f.endsWith('.md')) result.push(path.join('playbooks', 'families', f));
    }
  }
  return result;
}

function listArchiveFiles() {
  const dir = path.join(REPO_ROOT, 'playbooks', 'archive');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter((f) => f.endsWith('.md'))
    .map((f) => path.join('playbooks', 'archive', f));
}

// BUG STORICO (corretto qui): questa funzione indicizzava i bullet in una
// Map per ID iterando listPlaybookFiles()+listArchiveFiles() e
// sovrascriveva silenziosamente la entry precedente con l'ultimo file
// letto, nascondendo eventuali collisioni di ID tra file diversi (successo
// realmente in un progetto che usa questo kit, con lo stesso ID duplicato
// tra due file playbook diversi). Ora mantiene la PRIMA occorrenza trovata
// (deterministico, non dipende da quale file viene scritto per ultimo) e
// segnala esplicitamente ogni collisione invece di ignorarla. Chi ha
// bisogno del quadro completo di una collisione deve usare
// findAllBulletLocations()/detectIdCollisions().
function collectExistingIds() {
  const map = new Map();
  for (const rel of [...listPlaybookFiles(), ...listArchiveFiles()]) {
    const raw = fs.readFileSync(path.join(REPO_ROOT, rel), 'utf8');
    const { bullets } = parsePlaybookFile(raw);
    for (const b of bullets) {
      if (map.has(b.id)) {
        console.error(`ATTENZIONE: ID bullet duplicato rilevato: "${b.id}" e' presente sia in "${map.get(b.id).file}" sia in "${rel}". Integrita' dei dati compromessa: vedi detectIdCollisions().`);
        continue;
      }
      map.set(b.id, { file: rel, status: b.status });
    }
  }
  return map;
}

// Ritorna TUTTI i file (playbooks + archive) in cui un dato ID compare,
// con lo status del bullet in ciascuno. Normalmente questo array deve
// avere lunghezza al massimo 1 (l'unicita' dell'ID e' un invariante): la
// funzione serve proprio a rilevare le violazioni di quell'invariante
// invece di nasconderle dietro una Map indicizzata per ID.
function findAllBulletLocations(id) {
  const locations = [];
  for (const rel of [...listPlaybookFiles(), ...listArchiveFiles()]) {
    const raw = fs.readFileSync(path.join(REPO_ROOT, rel), 'utf8');
    const { bullets } = parsePlaybookFile(raw);
    const bullet = bullets.find((b) => b.id === id);
    if (bullet) locations.push({ relPath: rel, status: bullet.status });
  }
  return locations;
}

// Rileva le collisioni di ID "vive": stesso ID presente in più di un file
// tra quelli NON deprecated (active/quarantined). Un ID deprecated
// archiviato che condivide per storia il numero con un bullet attivo
// altrove (es. una collisione passata già risolta con una DEPRECATE
// mirata) non è più una condizione da bloccare: il bullet deprecated è
// storico, escluso dal retrieval, e non riceve più scritture da
// apply_delta.js/update_counters.js. Solo la coesistenza di più bullet
// NON deprecated con lo stesso ID è la vera violazione dell'invariante di
// unicità e va segnalata. Usata da gate.js come controllo meccanico
// esplicito di integrità dei dati, invece di scoprire la collisione solo
// a runtime quando apply_delta.js/update_counters.js cercano di scrivere
// un delta.
function detectIdCollisions() {
  const byId = new Map();
  for (const rel of [...listPlaybookFiles(), ...listArchiveFiles()]) {
    const raw = fs.readFileSync(path.join(REPO_ROOT, rel), 'utf8');
    const { bullets } = parsePlaybookFile(raw);
    for (const b of bullets) {
      if (!byId.has(b.id)) byId.set(b.id, []);
      byId.get(b.id).push({ relPath: rel, status: b.status });
    }

  }
  const collisions = [];
  for (const [id, locations] of byId) {
    const live = locations.filter((l) => l.status !== 'deprecated');
    if (live.length > 1) collisions.push({ id, files: live.map((l) => l.relPath) });
  }
  return collisions;
}

function computeReviewStateHash() {
  const relativePaths = [
    path.relative(REPO_ROOT, PROJECT_CONFIG_PATH),
    ...listPlaybookFiles(),
    ...listArchiveFiles(),
    path.join('ace', 'state', 'live-exclusions.json'),
  ].map((relativePath) => relativePath.replace(/\\/g, '/')).sort();
  const hash = crypto.createHash('sha256');
  for (const relativePath of relativePaths) {
    const absolutePath = path.join(REPO_ROOT, relativePath);
    hash.update(`${relativePath}\0`);
    hash.update(fs.existsSync(absolutePath) ? fs.readFileSync(absolutePath) : Buffer.from('<missing>'));
    hash.update('\0');
  }
  return hash.digest('hex');
}

module.exports = {
  REPO_ROOT,
  ACE_ROOT,
  loadBulletSchema,
  loadProjectConfig,
  enabledPlatforms,
  validateProjectConfig,
  loadAgentNames,
  isUnresolvedPlaceholder,
  defaultPlaybookSkeleton,
  scopeToRelPath,
  parsePlaybookFile,
  bulletToMarkdown,
  stripEmptyPlaceholder,
  serializeFile,
  listPlaybookFiles,
  listArchiveFiles,
  collectExistingIds,
  findAllBulletLocations,
  detectIdCollisions,
  SAFE_SCOPE_ID_RE,
  assertSafeWritePath,
  acquireMutationLock,
  computeReviewStateHash,
};
