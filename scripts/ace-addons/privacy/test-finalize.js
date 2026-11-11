'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { REPO_ROOT } = require('../../../ace/scripts/lib/playbook');
const { prepareDelegation, captureTrace, runtimeStateDir } = require('../../../ace/scripts/lib/runtime');
const {
  run, setup, ensureEnvironment, requirementsFingerprint, STAMP_NAME,
} = require('./finalize-task');

function fakeEnvironment() {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'ace-privacy-env-'));
  const requirements = path.join(directory, 'requirements.txt');
  fs.writeFileSync(requirements, 'presidio-analyzer==0\n');
  const envDir = path.join(directory, '.venv');
  const calls = [];
  // Fake interpreter creation: the "venv" step materializes the python executable.
  const exec = (command, args) => {
    calls.push([command, ...args]);
    if (args.includes('venv')) {
      const python = path.join(envDir, process.platform === 'win32' ? 'Scripts' : 'bin',
        process.platform === 'win32' ? 'python.exe' : 'python');
      fs.mkdirSync(path.dirname(python), { recursive: true });
      fs.writeFileSync(python, '');
    }
    return '';
  };
  return { directory, requirements, envDir, calls, exec };
}

test('first use installs the environment automatically and stamps it', () => {
  const { directory, requirements, envDir, calls, exec } = fakeEnvironment();
  try {
    const installed = ensureEnvironment({ envDir, requirements, run: exec, log: () => {}, env: {} });
    assert.equal(installed, true);
    assert.ok(calls.some((call) => call.includes('venv')));
    assert.ok(calls.some((call) => call.includes('pip') && call.includes(requirements)));
    assert.equal(fs.readFileSync(path.join(envDir, STAMP_NAME), 'utf8'),
      requirementsFingerprint(requirements));
    calls.length = 0;
    assert.equal(ensureEnvironment({ envDir, requirements, run: exec, log: () => {}, env: {} }), false);
    assert.equal(calls.length, 0, 'a ready environment must not run any command');
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test('changed requirements trigger a reinstall', () => {
  const { directory, requirements, envDir, calls, exec } = fakeEnvironment();
  try {
    setup({ envDir, requirements, run: exec, log: () => {} });
    fs.appendFileSync(requirements, 'spacy==0\n');
    calls.length = 0;
    assert.equal(ensureEnvironment({ envDir, requirements, run: exec, log: () => {}, env: {} }), true);
    assert.ok(calls.some((call) => call.includes('pip')));
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test('automatic setup can be disabled and then fails with instructions', () => {
  const { directory, requirements, envDir, calls, exec } = fakeEnvironment();
  try {
    assert.throws(
      () => ensureEnvironment({
        envDir, requirements, run: exec, log: () => {}, env: { ACE_PRIVACY_NO_AUTOSETUP: '1' },
      }),
      /--setup/,
    );
    assert.equal(calls.length, 0);
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test('a missing Python 3.10+ interpreter gives an actionable error', () => {
  const { directory, requirements, envDir } = fakeEnvironment();
  try {
    assert.throws(
      () => setup({
        envDir, requirements, log: () => {}, run: () => { throw new Error('boom'); },
      }),
      /Python 3\.10\+ is required/,
    );
    assert.ok(!fs.existsSync(path.join(envDir, STAMP_NAME)));
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test('sanitizes the canonical trace before ACE counters run', () => {
  const taskId = `ace-privacy-selftest-${process.pid}-${Date.now()}`;
  const stateDir = runtimeStateDir(taskId);
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'ace-privacy-selftest-'));
  const target = path.join(REPO_ROOT, 'ace', 'traces', `${taskId}__qa-analyst.json`);
  try {
    const { path: manifestPath } = prepareDelegation({
      taskId, agent: 'qa-analyst', platformName: 'copilot',
    });
    const source = path.join(directory, 'input.json');
    fs.writeFileSync(source, JSON.stringify({
      task_id: taskId,
      agent: 'qa-analyst',
      started_at: '2026-01-01T00:00:00Z',
      playbook_bullets_seen: [],
      playbook_bullets_cited: [],
      actions: [{ description: 'Contact mario.rossi@example.com' }],
      outcome: { status: 'success', detail: 'Mario Rossi helped' },
      friction: [],
      request_summary: 'Email mario.rossi@example.com at https://example.com/account/mario.rossi',
    }));
    captureTrace({ manifestPath, tracePath: source });
    run(taskId);
    const result = JSON.parse(fs.readFileSync(target, 'utf8'));
    assert.equal(result.request_summary, 'Email <EMAIL_ADDRESS> at <URL>');
    assert.equal(result.actions[0].description, 'Contact <EMAIL_ADDRESS>');
    assert.equal(result.task_id, taskId);
    assert.ok(result.counted_for_playbook_at);
    assert.ok(fs.existsSync(path.join(stateDir, 'finalized.json')));
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
    if (fs.existsSync(target)) fs.unlinkSync(target);
    if (fs.existsSync(stateDir)) fs.rmSync(stateDir, { recursive: true, force: true });
  }
});
