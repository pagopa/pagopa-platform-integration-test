#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { REPO_ROOT, assertSafeWritePath } = require('./lib/playbook');
const { runtimeStateDir } = require('./lib/runtime');

function execute(script, args = [], acceptedStatuses = [0]) {
  const result = spawnSync(process.execPath, [path.join(__dirname, script), ...args], {
    cwd: REPO_ROOT,
    encoding: 'utf8',
  });
  if (!acceptedStatuses.includes(result.status)) {
    throw new Error(`${script} failed: ${(result.stderr || result.stdout).trim()}`);
  }
  return result.stdout.trim();
}

function run(taskId = process.argv[2]) {
  const directory = runtimeStateDir(taskId);
  const delegations = path.join(directory, 'delegations');
  if (!fs.existsSync(delegations)) throw new Error(`No delegation manifests for task ${taskId}.`);
  const manifests = fs.readdirSync(delegations).filter((name) => name.endsWith('.json')).sort();
  if (!manifests.length) throw new Error(`No delegation manifests for task ${taskId}.`);
  const missing = manifests.filter((name) => {
    const agent = JSON.parse(fs.readFileSync(path.join(delegations, name), 'utf8')).canonical_agent;
    const traceName = `${taskId}__${agent}.json`;
    return !fs.existsSync(path.join(REPO_ROOT, 'ace', 'traces', traceName))
      && !fs.existsSync(path.join(REPO_ROOT, 'ace', 'traces', 'processed', traceName));
  });
  if (missing.length) throw new Error(`Missing captured traces for: ${missing.join(', ')}`);
  const counters = execute('update_counters.js', ['--task-id', taskId]);
  const threshold = execute('check_threshold.js', ['reflector'], [0, 1]);
  const state = { version: 1, task_id: taskId, manifests: manifests.length, counters, threshold };
  const target = assertSafeWritePath(path.join(directory, 'finalized.json'));
  fs.writeFileSync(target, `${JSON.stringify(state, null, 2)}\n`);
  console.log(JSON.stringify(state));
  return state;
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error(`ACE task finalization failed: ${error.message}`);
    process.exitCode = 1;
  }
}

module.exports = { run };
