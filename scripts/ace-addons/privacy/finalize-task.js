#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { REPO_ROOT } = require('../../../ace/scripts/lib/playbook');
const { SAFE_TASK_ID_RE, runtimeStateDir, validateTraceDocument } = require('../../../ace/scripts/lib/runtime');

const DIRECTORY = __dirname;
const ENV_DIR = path.join(DIRECTORY, '.venv');
const REQUIREMENTS = path.join(DIRECTORY, 'requirements.txt');
const STAMP_NAME = '.ace-privacy-ready';
const VERIFY_ENVIRONMENT = 'import presidio_analyzer, spacy; '
  + "[spacy.load(model) for model in ('en_core_web_sm', 'it_core_news_sm')]";

function pythonOf(envDir) {
  return path.join(envDir, process.platform === 'win32' ? 'Scripts' : 'bin',
    process.platform === 'win32' ? 'python.exe' : 'python');
}

const PYTHON = pythonOf(ENV_DIR);

function execute(command, args, input) {
  const result = spawnSync(command, args, {
    cwd: REPO_ROOT,
    input,
    encoding: 'utf8',
    maxBuffer: 16 * 1024 * 1024,
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    throw new Error(`${command} failed (${result.status}): ${(result.stderr || '').trim()}`);
  }
  return result.stdout;
}

function readRegularJson(file, label) {
  const descriptor = fs.openSync(file, 'r');
  try {
    if (!fs.fstatSync(descriptor).isFile()) throw new Error(`Not a regular ${label}: ${file}`);
    return JSON.parse(fs.readFileSync(descriptor, 'utf8'));
  } finally {
    fs.closeSync(descriptor);
  }
}

/** Hash of the requirements file: any change invalidates a previously installed environment. */
function requirementsFingerprint(file = REQUIREMENTS) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

/** Install Presidio, spaCy and both language models into the addon-local virtualenv. */
function setup({ envDir = ENV_DIR, requirements = REQUIREMENTS, run: exec = execute,
  log = (message) => console.error(message) } = {}) {
  const python = pythonOf(envDir);
  const launcher = process.env.PYTHON ? [process.env.PYTHON]
    : (process.platform === 'win32' ? ['py', '-3'] : ['python3']);
  log('ACE privacy: preparing the Presidio environment (first use or requirements changed; '
    + 'it downloads packages and may take a few minutes)...');
  try {
    exec(launcher[0], [...launcher.slice(1), '-c',
      'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)']);
  } catch (error) {
    throw new Error(`Python 3.10+ is required (tried "${launcher.join(' ')}"); install it or set `
      + `the PYTHON environment variable. ${error.message}`);
  }
  exec(launcher[0], [...launcher.slice(1), '-m', 'venv', envDir]);
  exec(python, ['-m', 'pip', 'install', '-r', requirements]);
  exec(python, ['-c', VERIFY_ENVIRONMENT]);
  fs.writeFileSync(path.join(envDir, STAMP_NAME), requirementsFingerprint(requirements));
  log('ACE privacy: environment ready.');
}

/**
 * Make sure the addon environment matches the requirements, installing it on first use.
 * Set ACE_PRIVACY_NO_AUTOSETUP=1 to fail with instructions instead of installing.
 */
function ensureEnvironment({ envDir = ENV_DIR, requirements = REQUIREMENTS, env = process.env,
  ...options } = {}) {
  const stamp = path.join(envDir, STAMP_NAME);
  const ready = fs.existsSync(pythonOf(envDir)) && fs.existsSync(stamp)
    && fs.readFileSync(stamp, 'utf8').trim() === requirementsFingerprint(requirements);
  if (ready) return false;
  if (env.ACE_PRIVACY_NO_AUTOSETUP === '1') {
    throw new Error('ACE privacy environment is missing or outdated and automatic setup is disabled; '
      + 'run: node scripts/ace-addons/privacy/finalize-task.js --setup');
  }
  setup({ envDir, requirements, ...options });
  return true;
}

function taskTraces(taskId) {
  if (!SAFE_TASK_ID_RE.test(taskId || '')) throw new Error('Expected a safe task ID.');
  const delegations = path.join(runtimeStateDir(taskId), 'delegations');
  const names = fs.readdirSync(delegations).filter((name) => name.endsWith('.json'));
  if (!names.length) throw new Error(`No delegation manifests for task ${taskId}.`);
  return names.map((name) => {
    const manifest = JSON.parse(fs.readFileSync(path.join(delegations, name), 'utf8'));
    const agent = manifest.canonical_agent;
    if (manifest.task_id !== taskId || typeof agent !== 'string'
        || !/^[a-zA-Z0-9_-]+$/.test(agent) || name !== `${agent}.json`) {
      throw new Error(`Unexpected delegation manifest: ${name}`);
    }
    return { agent, file: path.join(REPO_ROOT, 'ace', 'traces', `${taskId}__${agent}.json`) };
  });
}

function run(taskId) {
  const traces = taskTraces(taskId);
  // Before touching any trace: a failed bootstrap leaves the raw traces untouched.
  ensureEnvironment();
  const prepared = traces.map(({ agent, file }) => {
    const original = readRegularJson(file, 'trace file');
    validateTraceDocument(original);
    if (original.task_id !== taskId || original.agent !== agent || original.counted_for_playbook_at) {
      throw new Error(`Unexpected or already counted trace: ${file}`);
    }
    const output = execute(PYTHON, [path.join(DIRECTORY, 'sanitize.py')], JSON.stringify(original));
    const sanitized = JSON.parse(output);
    validateTraceDocument(sanitized);
    // Only the configured prose fields may change; all structural evidence must survive.
    const policy = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, 'config', 'ace-addons',
      'privacy', 'policy.json'), 'utf8'));
    const neutralize = (document) => {
      const copy = structuredClone(document);
      for (const field of policy.fields) {
        if (field.includes('[].')) {
          const [collection, key] = field.split('[].');
          for (const item of copy[collection] || []) item[key] = '';
        } else if (field.includes('.')) {
          const [parent, key] = field.split('.');
          if (copy[parent] && key in copy[parent]) copy[parent][key] = '';
        } else if (field in copy) copy[field] = '';
      }
      return copy;
    };
    if (JSON.stringify(neutralize(original)) !== JSON.stringify(neutralize(sanitized))) {
      throw new Error(`Sanitization changed structural evidence: ${file}`);
    }
    return { file, content: `${JSON.stringify(sanitized, null, 2)}\n` };
  });

  for (const { file, content } of prepared) {
    const temporary = path.join(path.dirname(file), `.${path.basename(file)}.${process.pid}.tmp`);
    try {
      fs.writeFileSync(temporary, content, { flag: 'wx' });
      fs.renameSync(temporary, file);
    } finally {
      try {
        fs.unlinkSync(temporary);
      } catch (error) {
        if (error.code !== 'ENOENT') throw error;
      }
    }
  }
  execute(process.execPath, [path.join(REPO_ROOT, 'ace', 'scripts', 'finalize_task.js'), taskId]);
  console.log(`Sanitized ${traces.length} ACE traces and finalized task ${taskId}.`);
}

if (require.main === module) {
  try {
    if (process.argv[2] === '--setup') setup();
    else if (process.argv[2] === '--ensure') ensureEnvironment();
    else run(process.argv[2]);
  } catch (error) {
    console.error(`ACE privacy addon failed: ${error.message}`);
    process.exitCode = 1;
  }
}

module.exports = {
  run, taskTraces, setup, ensureEnvironment, requirementsFingerprint, STAMP_NAME,
};
