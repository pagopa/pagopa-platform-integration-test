#!/usr/bin/env node
'use strict';

const { prepareDelegation } = require('./lib/runtime');

function valueOf(name) {
  const index = process.argv.indexOf(name);
  return index === -1 ? undefined : process.argv[index + 1];
}

function run() {
  const taskId = valueOf('--task-id') || process.argv[2];
  const agent = valueOf('--agent') || process.argv[3];
  const result = prepareDelegation({
    taskId,
    agent,
    platformName: valueOf('--platform'),
    requestSummary: valueOf('--request-summary'),
  });
  console.log(JSON.stringify({
    manifest: result.path,
    runtime_agent: result.manifest.runtime_agent,
    selected: result.manifest.playbook_bullets_selected,
  }));
  return result;
}

if (require.main === module) {
  try {
    run();
  } catch (error) {
    console.error(`ACE delegation preparation failed: ${error.message}`);
    process.exitCode = 1;
  }
}

module.exports = { run };
