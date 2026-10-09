#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { REPO_ROOT } = require('../../../ace/scripts/lib/playbook');
const { SAFE_TASK_ID_RE, runtimeStateDir, validateTraceDocument } = require('../../../ace/scripts/lib/runtime');

const DIRECTORY = __dirname;
const ENV_DIR = path.join(DIRECTORY, '.venv');
const PYTHON = path.join(ENV_DIR, process.platform === 'win32' ? 'Scripts' : 'bin',
  process.platform === 'win32' ? 'python.exe' : 'python');

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

function setup() {
  const systemPython = process.env.PYTHON || (process.platform === 'win32' ? 'py' : 'python3');
  execute(systemPython, process.platform === 'win32' && !process.env.PYTHON
    ? ['-3', '-m', 'venv', ENV_DIR] : ['-m', 'venv', ENV_DIR]);
  execute(PYTHON, ['-m', 'pip', 'install', '-r', path.join(DIRECTORY, 'requirements.txt')]);
  for (const model of ['en_core_web_sm', 'it_core_news_sm']) {
    execute(PYTHON, ['-m', 'spacy', 'download', model]);
  }
  console.log('ACE privacy dependencies installed.');
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
    else run(process.argv[2]);
  } catch (error) {
    console.error(`ACE privacy addon failed: ${error.message}`);
    process.exitCode = 1;
  }
}

module.exports = { run, taskTraces };
