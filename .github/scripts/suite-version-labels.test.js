'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');
const { suites } = require('../nrt-suites.json');
const { resolveSuiteVersionLabels, verifyPullRequestLabels } = require('./suite-version-labels');

function resolve(labels, author = 'contributor') {
  return resolveSuiteVersionLabels({ labels, author });
}

for (const labels of [
  ['skip'],
  ['skip', 'major'],
  ['minor', 'skip'],
  ['patch', 'skip'],
  ['major', 'patch', 'WISP', 'FDR3', 'skip'],
]) {
  test(`skip takes precedence over ${labels.join(', ')}`, () => {
    assert.equal(resolve(labels).status, 'skip');
  });
}

for (const version of ['major', 'minor', 'patch']) {
  test(`${version} still requires a suite for a human PR`, () => {
    const result = resolve([version]);
    assert.equal(result.status, 'invalid');
    assert.match(result.message, /Missing suite label/);
    assert.match(result.message, /skip/);
  });

  for (const suite of suites) {
    test(`${version} accepts the catalog suite ${suite.id}`, () => {
      const result = resolve([version, suite.id]);
      assert.equal(result.status, 'bump');
      assert.equal(result.versionLabel, version);
      assert.equal(result.suiteLabel, suite.id);
    });
  }
}

test('labels are case insensitive', () => {
  const result = resolve(['MaJoR', 'FdR3']);
  assert.equal(result.status, 'bump');
  assert.equal(result.versionLabel, 'major');
  assert.equal(result.suiteLabel, 'fdr3');
  assert.equal(resolve(['SKIP', 'MAJOR']).status, 'skip');
});

for (const labels of [[], ['documentation'], ['WISP']]) {
  test(`a human PR with ${JSON.stringify(labels)} still requires an increment or skip`, () => {
    const result = resolve(labels);
    assert.equal(result.status, 'invalid');
    assert.match(result.message, /Missing required labels/);
  });
}

test('the legacy fdr label is not an alias for fdr3', () => {
  assert.equal(resolve(['patch', 'fdr']).status, 'invalid');
  assert.equal(resolve(['patch', 'FDR3']).status, 'bump');
});

test('multiple suites remain invalid without skip', () => {
  const result = resolve(['patch', 'WISP', 'FDR3']);
  assert.equal(result.status, 'invalid');
  assert.match(result.message, /More than one suite label/);
});

test('multiple increment labels keep the existing last-label selection', () => {
  const result = resolve(['major', 'patch', 'WISP']);
  assert.equal(result.status, 'bump');
  assert.equal(result.versionLabel, 'patch');
});

test('unrelated labels do not interfere with a valid suite bump', () => {
  assert.equal(resolve(['size/small', 'python', 'patch', 'WISP']).status, 'bump');
});

for (const author of ['dependabot[bot]', 'renovate[bot]']) {
  for (const labels of [[], ['major'], ['minor', 'WISP', 'FDR3']]) {
    test(`${author} is exempt with ${JSON.stringify(labels)}`, () => {
      const result = resolve(labels, author);
      assert.equal(result.status, 'skip');
      assert.match(result.message, /dependency updates/);
      assert.equal(result.versionLabel, undefined);
      assert.equal(result.suiteLabel, undefined);
    });
  }
}

for (const author of ['github-actions[bot]', 'dependabot-helper[bot]', 'renovate-helper[bot]']) {
  test(`${author} does not receive a blanket bot exemption`, () => {
    assert.equal(resolve(['major'], author).status, 'invalid');
  });
}

test('a dependencies label alone does not exempt a human PR', () => {
  assert.equal(resolve(['dependencies', 'major']).status, 'invalid');
});

function createRuntime({ labels, author = 'contributor', payloadLabels = [], actor = 'reviewer' }) {
  const outputs = {};
  const errors = [];
  const messages = [];
  const calls = [];
  const runtime = {
    context: {
      repo: { owner: 'pagopa', repo: 'pagopa-platform-integration-test' },
      issue: { number: 170 },
      actor,
      payload: {
        pull_request: {
          user: { login: author },
          labels: payloadLabels.map(name => ({ name })),
        },
      },
    },
    github: {
      rest: {
        issues: {
          listLabelsOnIssue() {
            throw new Error('Labels must be read through pagination');
          },
        },
      },
      async paginate(method, parameters) {
        calls.push({ method, parameters });
        return labels.map(name => ({ name }));
      },
    },
    core: {
      setOutput(name, value) { outputs[name] = value; },
      setFailed(message) { errors.push(message); },
      info(message) { messages.push(message); },
    },
  };
  return { runtime, outputs, errors, messages, calls };
}

test('verification reads current paginated labels instead of stale event labels', async () => {
  const { runtime, outputs, errors, calls } = createRuntime({
    labels: ['major', 'skip'],
    payloadLabels: ['major'],
  });
  await verifyPullRequestLabels(runtime);
  assert.deepEqual(outputs, { should_bump: 'false' });
  assert.deepEqual(errors, []);
  assert.deepEqual(calls, [{
    method: runtime.github.rest.issues.listLabelsOnIssue,
    parameters: { ...runtime.context.repo, issue_number: 170, per_page: 100 },
  }]);
});

test('removing skip restores validation even if the event payload still contains it', async () => {
  const { runtime, outputs, errors, messages } = createRuntime({
    labels: ['major'],
    payloadLabels: ['major', 'skip'],
  });
  await verifyPullRequestLabels(runtime);
  assert.deepEqual(outputs, { should_bump: 'false' });
  assert.equal(errors.length, 1);
  assert.match(errors[0], /Missing suite label/);
  assert.deepEqual(messages, []);
});

test('bot exemption uses the PR author even when a human changes the labels', async () => {
  const { runtime, outputs, errors } = createRuntime({
    labels: ['major'],
    author: 'dependabot[bot]',
    actor: 'reviewer',
  });
  await verifyPullRequestLabels(runtime);
  assert.deepEqual(outputs, { should_bump: 'false' });
  assert.deepEqual(errors, []);
});

test('a bot actor cannot exempt a human-authored PR', async () => {
  const { runtime, errors } = createRuntime({ labels: ['major'], actor: 'dependabot[bot]' });
  await verifyPullRequestLabels(runtime);
  assert.equal(errors.length, 1);
});

test('a valid FDR3 bump exports the exact outputs consumed by the workflow', async () => {
  const { runtime, outputs, errors } = createRuntime({ labels: ['major', 'FDR3'] });
  await verifyPullRequestLabels(runtime);
  assert.deepEqual(outputs, { should_bump: 'true', version_label: 'major', suite_label: 'fdr3' });
  assert.deepEqual(errors, []);
});

test('invalid labels never export a version or suite placeholder', async () => {
  const { runtime, outputs, errors } = createRuntime({ labels: [] });
  await verifyPullRequestLabels(runtime);
  assert.deepEqual(outputs, { should_bump: 'false' });
  assert.equal(errors.length, 1);
  assert.match(errors[0], /Missing required labels/);
});

test('GitHub API failures propagate without a success-shaped fallback', async () => {
  const { runtime, outputs, errors, messages } = createRuntime({ labels: ['skip'] });
  runtime.github.paginate = async () => { throw new Error('GitHub API unavailable'); };
  await assert.rejects(verifyPullRequestLabels(runtime), /GitHub API unavailable/);
  assert.deepEqual(outputs, {});
  assert.deepEqual(errors, []);
  assert.deepEqual(messages, []);
});
