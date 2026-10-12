'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {
  REPO_ROOT, loadProjectConfig, loadAgentNames, enabledPlatforms, assertSafeWritePath,
} = require('./playbook');
const retrieval = require('../retrieval');

const SAFE_TASK_ID_RE = /^[a-z0-9][a-z0-9._-]*$/;

function toRelative(absolute) {
  return path.relative(REPO_ROOT, absolute).replace(/\\/g, '/');
}

function runtimeStateDir(taskId) {
  if (!SAFE_TASK_ID_RE.test(taskId || '')) {
    throw new Error(`Unsafe task id: ${taskId}`);
  }
  return assertSafeWritePath(path.join(REPO_ROOT, 'ace', 'state', 'runtime', taskId));
}

function platformByName(config, platformName) {
  const platforms = enabledPlatforms(config);
  const selected = platformName
    ? platforms.find((platform) => platform.name === platformName)
    : (platforms.length === 1 ? platforms[0] : null);
  if (!selected) {
    throw new Error(platformName
      ? `Enabled platform not found: ${platformName}`
      : 'More than one platform is enabled; pass --platform.');
  }
  return selected;
}

function selectedLessons(config, canonicalAgent) {
  const { byScope } = retrieval.collectBullets();
  const scopes = [
    '_global',
    canonicalAgent,
    ...(config.agent_families?.[canonicalAgent] || []).map((family) => `family:${family}`),
  ];
  const lessons = scopes.flatMap((scope) => (byScope.get(scope) || []).map((item) => ({
    id: item.id,
    scope,
    content: item.content,
  })));
  lessons.sort((left, right) => left.id.localeCompare(right.id)
    || left.scope.localeCompare(right.scope));
  const duplicates = lessons.filter((lesson, index) => (
    index > 0 && lesson.id === lessons[index - 1].id
  ));
  if (duplicates.length) {
    throw new Error(`Duplicate selected lesson ids: ${[...new Set(duplicates.map((item) => item.id))].join(', ')}`);
  }
  return lessons;
}

function prepareDelegation({ taskId, agent, platformName, requestSummary }) {
  const config = loadProjectConfig();
  if (!loadAgentNames().includes(agent)) throw new Error(`Unknown canonical agent: ${agent}`);
  const mode = config.integration_mode || 'embedded';
  if (mode === 'mediated' && !platformName) {
    throw new Error('Mediated delegation requires an explicit --platform.');
  }
  const platform = platformByName(config, platformName);
  const lessons = selectedLessons(config, agent);
  const selected = lessons.map((lesson) => lesson.id);
  const instructionFiles = [
    retrieval.globalInstructionsPath(platform, mode),
    retrieval.instructionsPathFor(agent, platform.agent_instructions_dir),
    ...(config.agent_families?.[agent] || []).map((family) => (
      retrieval.instructionsPathFor(`family:${family}`, platform.agent_instructions_dir)
    )),
  ].map(toRelative);
  const runtimeAgent = mode === 'mediated' && agent === config.orchestrator_agent
    ? platform.orchestrator_entrypoints.ace
    : (platform.canonical_to_runtime?.[agent] || `${platform.runtime_prefix}/${agent}`);
  const manifest = {
    version: 1,
    integration_mode: mode,
    task_id: taskId,
    canonical_agent: agent,
    runtime_agent: runtimeAgent,
    platform: platform.name,
    orchestrator_entrypoints: platform.orchestrator_entrypoints || null,
    instruction_files: instructionFiles,
    lessons,
    playbook_bullets_selected: selected,
  };
  if (requestSummary) manifest.request_summary = requestSummary;
  manifest.manifest_id = crypto
    .createHash('sha256')
    .update(JSON.stringify(manifest))
    .digest('hex');
  const directory = runtimeStateDir(taskId);
  fs.mkdirSync(path.join(directory, 'delegations'), { recursive: true });
  const target = assertSafeWritePath(path.join(directory, 'delegations', `${agent}.json`));
  fs.writeFileSync(target, `${JSON.stringify(manifest, null, 2)}\n`);
  return { manifest, path: target };
}

function readManifest(manifestPath) {
  const absolute = assertSafeWritePath(path.resolve(manifestPath));
  const manifest = JSON.parse(fs.readFileSync(absolute, 'utf8'));
  const directory = runtimeStateDir(manifest.task_id);
  const expectedPath = path.join(directory, 'delegations', `${manifest.canonical_agent}.json`);
  if (absolute !== expectedPath) throw new Error('Manifest path does not match its task and canonical agent.');
  const unsigned = { ...manifest };
  delete unsigned.manifest_id;
  const expectedId = crypto.createHash('sha256').update(JSON.stringify(unsigned)).digest('hex');
  if (manifest.manifest_id !== expectedId) {
    throw new Error('Delegation manifest consistency checksum does not match.');
  }
  return { absolute, manifest };
}

function assertUniqueStrings(value, name) {
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')
      || new Set(value).size !== value.length) {
    throw new Error(`${name} must be an array of unique strings.`);
  }
}

function isDateTime(value) {
  return typeof value === 'string' && !Number.isNaN(Date.parse(value));
}

function validateTraceDocument(trace) {
  if (!trace || typeof trace !== 'object' || Array.isArray(trace)) {
    throw new Error('Trace must be a JSON object.');
  }
  const allowed = new Set([
    'task_id', 'agent', 'started_at', 'ended_at', 'request_summary',
    'playbook_bullets_seen', 'playbook_bullets_cited', 'playbook_bullets_selected',
    'actions', 'outcome', 'corrects', 'notes', 'friction', 'counted_for_playbook_at',
  ]);
  const extras = Object.keys(trace).filter((key) => !allowed.has(key));
  if (extras.length) throw new Error(`Trace has unsupported fields: ${extras.join(', ')}`);
  if (!SAFE_TASK_ID_RE.test(trace.task_id || '') || typeof trace.agent !== 'string'
      || !isDateTime(trace.started_at) || (trace.ended_at && !isDateTime(trace.ended_at))) {
    throw new Error('Trace has invalid task_id, agent, or timestamps.');
  }
  for (const key of ['request_summary', 'notes']) {
    if (trace[key] !== undefined && typeof trace[key] !== 'string') {
      throw new Error(`Trace ${key} must be a string.`);
    }
  }
  if (trace.counted_for_playbook_at !== undefined && !isDateTime(trace.counted_for_playbook_at)) {
    throw new Error('Trace counted_for_playbook_at must be a date-time.');
  }
  assertUniqueStrings(trace.playbook_bullets_seen, 'trace.playbook_bullets_seen');
  assertUniqueStrings(trace.playbook_bullets_cited, 'trace.playbook_bullets_cited');
  if (!Array.isArray(trace.actions) || trace.actions.some((action) => (
    !action || typeof action !== 'object' || Array.isArray(action)
    || typeof action.description !== 'string'
    || Object.keys(action).some((key) => !['description', 'tool', 'timestamp'].includes(key))
    || (action.tool !== undefined && typeof action.tool !== 'string')
    || (action.timestamp !== undefined && !isDateTime(action.timestamp))
  ))) {
    throw new Error('Trace actions do not satisfy the trace schema.');
  }
  if (!trace.outcome || typeof trace.outcome !== 'object' || Array.isArray(trace.outcome)
      || !['success', 'partial', 'failure'].includes(trace.outcome.status)
      || Object.keys(trace.outcome).some((key) => !['status', 'evaluated_by', 'detail'].includes(key))
      || (trace.outcome.evaluated_by !== undefined && typeof trace.outcome.evaluated_by !== 'string')
      || (trace.outcome.detail !== undefined && typeof trace.outcome.detail !== 'string')) {
    throw new Error('Trace outcome does not satisfy the trace schema.');
  }
  if (!Array.isArray(trace.friction) || trace.friction.some((item) => (
    !item || typeof item !== 'object' || Array.isArray(item)
    || typeof item.description !== 'string' || typeof item.recovered !== 'boolean'
    || Object.keys(item).some((key) => !['description', 'recovered'].includes(key))
  ))) {
    throw new Error('Trace friction does not satisfy the trace schema.');
  }
  if (trace.corrects !== undefined) {
    const correction = trace.corrects;
    if (!correction || typeof correction !== 'object' || Array.isArray(correction)
        || Object.keys(correction).some(
          (key) => !['task_id', 'agent', 'reason', 'counter_adjustments'].includes(key),
        )
        || !['task_id', 'agent', 'reason'].every((key) => typeof correction[key] === 'string')
        || !Array.isArray(correction.counter_adjustments)
        || correction.counter_adjustments.some((adjustment) => (
          !adjustment || typeof adjustment !== 'object' || Array.isArray(adjustment)
          || Object.keys(adjustment).some((key) => !['bullet_id', 'field', 'delta'].includes(key))
          || typeof adjustment.bullet_id !== 'string'
          || !['helped', 'hurt', 'helped_confirmed', 'helped_provisional',
            'hurt_confirmed', 'hurt_provisional'].includes(adjustment.field)
          || !Number.isInteger(adjustment.delta)
        ))) {
      throw new Error('Trace correction does not satisfy the trace schema.');
    }
  }
}

function captureTrace({ manifestPath, tracePath }) {
  const { manifest } = readManifest(manifestPath);
  const trace = JSON.parse(fs.readFileSync(path.resolve(tracePath), 'utf8'));
  validateTraceDocument(trace);
  if (trace.task_id !== manifest.task_id || trace.agent !== manifest.canonical_agent) {
    throw new Error('Trace task_id and agent must match the delegation manifest.');
  }
  const selected = manifest.playbook_bullets_selected || [];
  const seen = trace.playbook_bullets_seen;
  const cited = trace.playbook_bullets_cited;
  assertUniqueStrings(selected, 'manifest.playbook_bullets_selected');
  assertUniqueStrings(seen, 'trace.playbook_bullets_seen');
  assertUniqueStrings(cited, 'trace.playbook_bullets_cited');
  if (seen.some((id) => !selected.includes(id))) {
    throw new Error('Every seen lesson must be present in the manifest selected set.');
  }
  if (cited.some((id) => !seen.includes(id))) {
    throw new Error('Every cited lesson must be present in the trace seen set.');
  }
  trace.playbook_bullets_selected = selected;
  const target = assertSafeWritePath(path.join(
    REPO_ROOT, 'ace', 'traces', `${manifest.task_id}__${manifest.canonical_agent}.json`,
  ));
  const processedTarget = assertSafeWritePath(path.join(
    REPO_ROOT, 'ace', 'traces', 'processed',
    `${manifest.task_id}__${manifest.canonical_agent}.json`,
  ));
  fs.mkdirSync(path.dirname(target), { recursive: true });
  const duplicate = [target, processedTarget].find((candidate) => fs.existsSync(candidate));
  if (duplicate) throw new Error(`Trace already exists: ${toRelative(duplicate)}`);
  fs.writeFileSync(target, `${JSON.stringify(trace, null, 2)}\n`);
  return { trace, path: target };
}

module.exports = {
  SAFE_TASK_ID_RE, captureTrace, prepareDelegation, readManifest, runtimeStateDir,
  validateTraceDocument,
};
