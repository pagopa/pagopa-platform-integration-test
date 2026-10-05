'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { REPO_ROOT } = require('../../../ace/scripts/lib/playbook');
const { prepareDelegation, captureTrace, runtimeStateDir } = require('../../../ace/scripts/lib/runtime');
const { run } = require('./finalize-task');

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
