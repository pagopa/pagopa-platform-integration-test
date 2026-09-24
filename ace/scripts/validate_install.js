#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const {
  REPO_ROOT, loadProjectConfig, loadAgentNames, enabledPlatforms,
} = require('./lib/playbook');
const generator = require('./generate_ace_agents');
const retrieval = require('./retrieval');

const REQUIRED_RUNTIME_FILES = [
  'ace/runtime-version.json',
  'ace/schema/bullet.schema.json',
  'ace/schema/trace.schema.json',
  'ace/config/thresholds.json',
  'ace/scripts/apply_delta.js',
  'ace/scripts/check_threshold.js',
  'ace/scripts/gate.js',
  'ace/scripts/inspect_update.js',
  'ace/scripts/retrieval.js',
  'ace/scripts/update_counters.js',
  'ace/prompts/reflector.md',
  'ace/prompts/curator.md',
  'ace/prompts/warden.md',
  'playbooks/_global.md',
];
const REQUIRED_MEDIATED_FILES = [
  'ace/scripts/prepare_delegation.js',
  'ace/scripts/capture_trace.js',
  'ace/scripts/finalize_task.js',
  'ace/scripts/lib/runtime.js',
  'ace/templates/mediated-adapter.md',
  'ace/templates/mediated-ace-wrapper.md',
];

function fail(errors, message) {
  errors.push(message);
}

function normalizedSha256(file) {
  return crypto.createHash('sha256')
    .update(fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n'), 'utf8')
    .digest('hex');
}

function validateManifestInventory(errors, config) {
  const manifestPath = path.join(REPO_ROOT, 'ace', 'runtime-version.json');
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch (error) {
    fail(errors, `Cannot read runtime-version.json: ${error.message}`);
    return;
  }
  const kitOwned = {
    ...(manifest?.ownership?.kit_owned || {}),
    ...(manifest?.ownership?.mode_specific?.[config?.integration_mode || 'embedded'] || {}),
  };
  if (!kitOwned || typeof kitOwned !== 'object' || Array.isArray(kitOwned)) {
    fail(errors, 'runtime-version.json must declare ownership.kit_owned.');
    return;
  }
  for (const [relativePath, expectedHash] of Object.entries(kitOwned)) {
    if (!config?.integration_mode && REQUIRED_MEDIATED_FILES.includes(relativePath)) continue;
    const absolutePath = path.join(REPO_ROOT, relativePath);
    if (!fs.existsSync(absolutePath) || !fs.statSync(absolutePath).isFile()) {
      fail(errors, `Missing manifest-declared runtime file: ${relativePath}`);
    } else if (normalizedSha256(absolutePath) !== expectedHash) {
      fail(errors, `Manifest hash mismatch for runtime file: ${relativePath}`);
    }
  }
}

function findPlaceholders(root, relativePaths) {
  const matches = [];
  for (const relativePath of relativePaths) {
    const absolute = path.join(root, relativePath);
    if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) continue;
    const content = fs.readFileSync(absolute, 'utf8');
    if (/__[A-Z0-9_]+__/.test(content)) matches.push(relativePath);
  }
  return matches;
}

function run() {
  const errors = [];
  for (const relativePath of REQUIRED_RUNTIME_FILES) {
    if (!fs.existsSync(path.join(REPO_ROOT, relativePath))) {
      fail(errors, `Missing runtime file: ${relativePath}`);
    }
  }

  let config;
  try {
    config = loadProjectConfig();
  } catch (error) {
    fail(errors, error.message);
  }
  validateManifestInventory(errors, config);

  try {
    const thresholds = JSON.parse(fs.readFileSync(
      path.join(REPO_ROOT, 'ace', 'config', 'thresholds.json'),
      'utf8',
    ));
    for (const stage of ['reflector', 'curator', 'warden']) {
      if (!thresholds[stage]
          || !Number.isInteger(thresholds[stage].threshold)
          || thresholds[stage].threshold < 0) {
        fail(errors, `Invalid non-negative integer threshold for ${stage}.`);
      }
    }
  } catch (error) {
    fail(errors, `Cannot validate thresholds.json: ${error.message}`);
  }

  if (config) {
    const agents = loadAgentNames();
    const mode = config.integration_mode || 'embedded';
    if (mode === 'mediated') {
      for (const relativePath of REQUIRED_MEDIATED_FILES) {
        if (!fs.existsSync(path.join(REPO_ROOT, relativePath))) {
          fail(errors, `Missing mediated runtime file: ${relativePath}`);
        }
      }
    }
    for (const agent of agents) {
      const playbook = path.join(REPO_ROOT, 'playbooks', `${agent}.md`);
      if (!fs.existsSync(playbook)) fail(errors, `Missing scoped playbook: playbooks/${agent}.md`);
    }
    for (const platform of enabledPlatforms(config)) {
      const globalTarget = mode === 'mediated'
        ? path.join(REPO_ROOT, platform.agent_instructions_dir, 'ace-global.instructions.md')
        : path.join(REPO_ROOT, platform.global_instructions_file);
      if (!fs.existsSync(globalTarget)) {
        fail(errors, `Missing generated global ACE instructions: ${path.relative(REPO_ROOT, globalTarget).replace(/\\/g, '/')}`);
      }
      if (mode === 'mediated') {
        const platformGlobal = path.join(REPO_ROOT, platform.global_instructions_file);
        if (fs.existsSync(platformGlobal)
            && fs.readFileSync(platformGlobal, 'utf8').includes('<!-- ACE:BEGIN')) {
          fail(errors, `Mediated mode must not inject ACE into platform global instructions: ${platform.global_instructions_file}`);
        }
      }
      for (const agent of agents) {
        const instructions = path.join(
          REPO_ROOT,
          platform.agent_instructions_dir,
          `ace-${agent}.instructions.md`,
        );
        if (!fs.existsSync(instructions)) {
          fail(errors, `Missing generated instructions: ${path.relative(REPO_ROOT, instructions).replace(/\\/g, '/')}`);
        }
        const families = [...new Set(Object.values(config.agent_families || {}).flat())];
        for (const family of families) {
          const playbook = path.join(REPO_ROOT, 'playbooks', 'families', `${family}.md`);
          if (!fs.existsSync(playbook)) fail(errors, `Missing family playbook: playbooks/families/${family}.md`);
          const instructions = path.join(
            REPO_ROOT,
            platform.agent_instructions_dir,
            `ace-family-${family}.instructions.md`,
          );
          if (!fs.existsSync(instructions)) {
            fail(errors, `Missing generated family instructions: ${path.relative(REPO_ROOT, instructions).replace(/\\/g, '/')}`);
          }
        }
      }
    }
    if (generator.run({ checkOnly: true }).length) {
      fail(errors, 'ACE wrappers are stale. Run node ace/scripts/generate_ace_agents.js.');
    }
    if (retrieval.run({ checkOnly: true, verbose: false }).length) {
      fail(errors, 'ACE instructions are stale. Run node ace/scripts/retrieval.js.');
    }
  }

  const placeholders = findPlaceholders(REPO_ROOT, [
    'ace/config/project.json',
    ...REQUIRED_RUNTIME_FILES,
    ...(config && (config.integration_mode || 'embedded') === 'mediated'
      ? REQUIRED_MEDIATED_FILES.filter((relativePath) => !relativePath.startsWith('ace/templates/'))
      : []),
  ]);
  if (placeholders.length) {
    fail(errors, `Unresolved placeholders in: ${placeholders.join(', ')}`);
  }
  if (config && (config.integration_mode || 'embedded') === 'mediated') {
    const ignorePath = path.join(REPO_ROOT, '.gitignore');
    const ignore = fs.existsSync(ignorePath) ? fs.readFileSync(ignorePath, 'utf8') : '';
    if (!/^ace\/state\/(?:runtime\/)?\s*$/m.test(ignore)) {
      fail(errors, 'Runtime state must be ignored with ace/state/runtime/ or ace/state/.');
    }
  }

  if (errors.length) {
    console.error(`ACE installation validation failed (${errors.length}):`);
    for (const error of errors) console.error(`- ${error}`);
    process.exitCode = 1;
    return false;
  }
  console.log('ACE installation validation passed.');
  return true;
}

if (require.main === module) run();

module.exports = { run };
