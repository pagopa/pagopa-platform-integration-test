'use strict';

const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');
const { prepareSyncBranch, publishSyncPullRequest } = require('./gherkin-sync-pr');

const MANIFEST = '.github/gherkin-manifest.yml';
const SYNOPSES = '.github/gherkin-synopses.json';
const TEMPLATE = fs.readFileSync(path.join(__dirname, '..', 'PULL_REQUEST_TEMPLATE.md'), 'utf8');

function git(cwd, ...args) {
  return execFileSync('git', args, {
    cwd,
    encoding: 'utf8',
    env: { ...process.env, GIT_TERMINAL_PROMPT: '0' },
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

function write(repo, file, content) {
  const destination = path.join(repo, file);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, content, 'utf8');
}

function configure(repo, root) {
  git(repo, 'config', 'user.name', 'Fixture author');
  git(repo, 'config', 'user.email', 'fixture@example.invalid');
  git(repo, 'config', 'commit.gpgsign', 'false');
  git(repo, 'config', 'core.autocrlf', 'false');
  git(repo, 'config', 'core.hooksPath', path.join(root, 'no-hooks'));
}

function commit(repo, message) {
  git(repo, 'add', '--all');
  git(repo, 'commit', '-m', message);
}

function fixture(t) {
  const root = fs.mkdtempSync(path.join(process.env.GHERKIN_SYNC_TEST_TMP || os.tmpdir(), 'gherkin-pr-'));
  const previousGlobal = process.env.GIT_CONFIG_GLOBAL;
  const previousSystem = process.env.GIT_CONFIG_NOSYSTEM;
  const gitconfig = path.join(root, 'gitconfig');
  fs.writeFileSync(gitconfig, '', 'utf8');
  process.env.GIT_CONFIG_GLOBAL = gitconfig;
  process.env.GIT_CONFIG_NOSYSTEM = '1';
  t.after(() => {
    if (previousGlobal === undefined) delete process.env.GIT_CONFIG_GLOBAL;
    else process.env.GIT_CONFIG_GLOBAL = previousGlobal;
    if (previousSystem === undefined) delete process.env.GIT_CONFIG_NOSYSTEM;
    else process.env.GIT_CONFIG_NOSYSTEM = previousSystem;
    fs.rmSync(root, { recursive: true, force: true });
  });
  const remote = path.join(root, 'remote.git');
  const author = path.join(root, 'author');
  const bot = path.join(root, 'bot');
  git(root, 'init', '--bare', '--initial-branch=main', remote);
  git(root, `--git-dir=${remote}`, 'config', 'core.hooksPath', path.join(root, 'no-hooks'));
  git(root, 'clone', remote, author);
  configure(author, root);
  write(author, MANIFEST, 'manifest: initial\n');
  write(author, SYNOPSES, '{"synopsis":"initial"}\n');
  write(author, '.github/PULL_REQUEST_TEMPLATE.md', TEMPLATE);
  commit(author, 'Fixture base');
  git(author, 'push', 'origin', 'main');
  git(root, 'clone', remote, bot);
  configure(bot, root);
  return { root, remote, author, bot };
}

function runtime(cwd, runId = 100, pulls = []) {
  const outputs = {};
  const errors = [];
  const calls = [];
  const context = { repo: { owner: 'example', repo: 'integration-test' }, runId };
  const github = {
    rest: {
      pulls: {
        list() { throw new Error('Pull requests must be paginated'); },
        async get({ pull_number }) {
          const pr = pulls.find(item => item.number === pull_number);
          if (!pr) throw new Error('PR not found');
          return { data: pr };
        },
        async create(parameters) {
          calls.push({ type: 'create', parameters });
          const pr = {
            number: pulls.length + 1,
            state: 'open',
            user: { login: 'github-actions[bot]' },
            head: { ref: parameters.head, repo: { full_name: 'example/integration-test' } },
            base: { ref: parameters.base },
            labels: [],
            html_url: `https://github.invalid/example/integration-test/pull/${pulls.length + 1}`,
            body: parameters.body,
          };
          pulls.push(pr);
          return { data: pr };
        },
      },
      issues: {
        async addLabels(parameters) {
          calls.push({ type: 'label', parameters });
          const pr = pulls.find(item => item.number === parameters.issue_number);
          pr.labels.push(...parameters.labels.map(name => ({ name })));
        },
        async createComment(parameters) {
          calls.push({ type: 'comment', parameters });
        },
      },
    },
    async paginate(method, parameters) {
      assert.equal(method, github.rest.pulls.list);
      assert.equal(parameters.state, 'open');
      return pulls.filter(pr => pr.state === 'open' && pr.base.ref === parameters.base);
    },
  };
  const core = {
    setOutput(name, value) { outputs[name] = value; },
    info() {},
    notice() {},
    error(message) { errors.push(message); },
  };
  const env = {
    GITHUB_RUN_ATTEMPT: '1',
    GITHUB_SERVER_URL: 'https://github.invalid',
    MANIFEST_OUTCOME: 'success',
    SYNOPSIS_OUTCOME: 'success',
  };
  return { github, context, core, cwd, env, outputs, errors, calls, pulls };
}

async function prepare(run) {
  await prepareSyncBranch(run);
  run.env.SYNC_BRANCH = run.outputs.branch;
  run.env.SYNC_BASE_SHA = run.outputs.base_sha;
  run.env.SYNC_PR_NUMBER = run.outputs.pr_number;
}

async function createPendingPr(fix, run) {
  await prepare(run);
  write(fix.bot, MANIFEST, 'manifest: generated\n');
  write(fix.bot, SYNOPSES, '{"synopsis":"generated"}\n');
  await publishSyncPullRequest(run);
  return run.pulls[0];
}

function clone(fix, name) {
  const destination = path.join(fix.root, name);
  git(fix.root, 'clone', fix.remote, destination);
  configure(destination, fix.root);
  return destination;
}

test('creates a review PR with both generated files, the repository template and skip label', async t => {
  const fix = fixture(t);
  const run = runtime(fix.bot);
  const base = git(fix.author, 'rev-parse', 'main');
  const pr = await createPendingPr(fix, run);

  assert.equal(pr.head.ref, 'automation/gherkin-sync/run-100-1');
  assert.equal(pr.base.ref, 'main');
  assert.deepEqual(pr.labels.map(label => label.name), ['skip']);
  assert.equal(git(fix.author, 'ls-remote', fix.remote, 'refs/heads/main').split('\t')[0], base);
  assert.deepEqual(
    git(fix.bot, 'diff', '--name-only', 'origin/main...HEAD').split('\n').sort(),
    [MANIFEST, SYNOPSES].sort(),
  );
  for (const comment of TEMPLATE.match(/<!---[\s\S]*?-->/g)) {
    assert.ok(pr.body.includes(comment));
  }
  for (const heading of TEMPLATE.match(/^#### .+$/gm)) {
    assert.ok(pr.body.includes(heading));
  }
  assert.ok(pr.body.includes('No tests are run by the generation workflow.'));
  assert.ok(pr.body.includes('workflow run'));
});

test('reuses the open PR and merges a newer main without overwriting its history', async t => {
  const fix = fixture(t);
  const first = runtime(fix.bot);
  const pr = await createPendingPr(fix, first);
  const previous = git(fix.bot, 'rev-parse', 'HEAD');
  write(fix.author, 'feature.feature', 'Feature: later change\n');
  commit(fix.author, 'Advance main');
  git(fix.author, 'push', 'origin', 'main');
  const main = git(fix.author, 'rev-parse', 'HEAD');

  const nextBot = clone(fix, 'next-bot');
  const next = runtime(nextBot, 101, first.pulls);
  await prepare(next);
  assert.equal(next.env.SYNC_BRANCH, pr.head.ref);
  assert.equal(next.env.SYNC_PR_NUMBER, String(pr.number));
  write(nextBot, MANIFEST, 'manifest: regenerated\n');
  await publishSyncPullRequest(next);
  assert.equal(first.pulls.length, 1);
  assert.equal(next.calls.some(call => call.type === 'create'), false);
  assert.equal(next.calls.filter(call => call.type === 'comment').length, 1);
  git(nextBot, 'merge-base', '--is-ancestor', previous, 'HEAD');
  git(nextBot, 'merge-base', '--is-ancestor', main, 'HEAD');
});

test('does not open a PR when there are no generated changes', async t => {
  const fix = fixture(t);
  const run = runtime(fix.bot);
  await prepare(run);
  await publishSyncPullRequest(run);
  assert.equal(run.pulls.length, 0);
  assert.equal(git(fix.bot, 'ls-remote', '--heads', 'origin', run.env.SYNC_BRANCH), '');
});

for (const scenario of ['complete', 'incomplete', 'unassociated']) {
  test(`inspects reviewer commits of a squashed sync PR; ${scenario}`, async t => {
    const fix = fixture(t);
    const sourceMerge = git(fix.author, 'rev-parse', 'HEAD');
    const oldBranch = 'automation/gherkin-sync/run-99-1';
    git(fix.author, 'switch', '-c', oldBranch);
    git(fix.author, 'config', 'user.name', 'github-actions[bot]');
    git(fix.author, 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com');
    write(fix.author, SYNOPSES, '{"synopsis":"generated"}\n');
    commit(fix.author, 'Generate synopsis');
    const generated = git(fix.author, 'rev-parse', 'HEAD');
    configure(fix.author, fix.root);
    write(fix.author, SYNOPSES, '{"synopsis":"reviewed"}\n');
    commit(fix.author, 'Review synopsis');
    const reviewed = git(fix.author, 'rev-parse', 'HEAD');
    git(fix.author, 'push', 'origin', oldBranch);
    git(fix.author, 'switch', 'main');
    git(fix.author, 'merge', '--squash', oldBranch);
    git(fix.author, 'commit', '-m', 'Squash sync PR');
    git(fix.author, 'push', 'origin', 'main');
    const published = git(fix.author, 'rev-parse', 'HEAD');
    const pr = {
      number: 42, state: 'closed', merged: true, commits: 2,
      user: { login: 'github-actions[bot]' },
      head: { ref: oldBranch, repo: { full_name: 'example/integration-test' } },
      base: { ref: 'main' }, labels: [],
    };
    const run = runtime(fix.bot, 100, [pr]);
    run.context.eventName = 'pull_request';
    run.context.payload = { pull_request: { merge_commit_sha: sourceMerge } };
    run.github.rest.repos = { listPullRequestsAssociatedWithCommit() {} };
    run.github.rest.pulls.listCommits = () => {};
    const listOpen = run.github.paginate;
    run.github.paginate = async (method, parameters) => {
      if (method === run.github.rest.repos.listPullRequestsAssociatedWithCommit) {
        assert.equal(parameters.commit_sha, published);
        return scenario === 'unassociated' ? [] : [pr];
      }
      if (method === run.github.rest.pulls.listCommits) {
        const commits = [
          { sha: generated, commit: { author: {
            name: 'github-actions[bot]', email: 'github-actions[bot]@users.noreply.github.com',
          } } },
          { sha: reviewed, commit: { author: { name: 'Reviewer', email: 'reviewer@example.invalid' } } },
        ];
        return scenario === 'incomplete' ? commits.slice(0, 1) : commits;
      }
      return listOpen(method, parameters);
    };
    if (scenario !== 'complete') {
      const expected = scenario === 'incomplete' ? /commit list.*incomplete or invalid/ : /Cannot identify the PR/;
      await assert.rejects(prepare(run), expected);
      return;
    }
    await prepare(run);
    assert.deepEqual(JSON.parse(run.outputs.published_reviews), { [published]: [reviewed] });
    assert.equal(git(fix.bot, 'cat-file', '-t', reviewed), 'commit');
  });
}

test('refuses to publish if main advances during generation', async t => {
  const fix = fixture(t);
  const run = runtime(fix.bot);
  await prepare(run);
  write(fix.bot, MANIFEST, 'manifest: generated\n');
  write(fix.author, 'unrelated.txt', 'new main\n');
  commit(fix.author, 'Advance main');
  git(fix.author, 'push', 'origin', 'main');
  await assert.rejects(publishSyncPullRequest(run), /main changed during generation/);
  assert.equal(run.pulls.length, 0);
  assert.equal(git(fix.bot, 'ls-remote', '--heads', 'origin', run.env.SYNC_BRANCH), '');
});

test('does not overwrite a concurrent reviewer push', async t => {
  const fix = fixture(t);
  const first = runtime(fix.bot);
  const pr = await createPendingPr(fix, first);
  const nextBot = clone(fix, 'next-bot');
  const next = runtime(nextBot, 101, first.pulls);
  await prepare(next);

  const reviewer = clone(fix, 'reviewer');
  git(reviewer, 'switch', '--track', `origin/${pr.head.ref}`);
  write(reviewer, SYNOPSES, '{"synopsis":"reviewer"}\n');
  commit(reviewer, 'Reviewer edit');
  git(reviewer, 'push', 'origin', pr.head.ref);
  const reviewed = git(reviewer, 'rev-parse', 'HEAD');
  write(nextBot, MANIFEST, 'manifest: new generation\n');
  await assert.rejects(publishSyncPullRequest(next));
  assert.equal(git(nextBot, 'ls-remote', 'origin', `refs/heads/${pr.head.ref}`).split('\t')[0], reviewed);
});

test('stops on a merge conflict with a human edit on main', async t => {
  const fix = fixture(t);
  const first = runtime(fix.bot);
  const pr = await createPendingPr(fix, first);
  const original = git(fix.bot, 'rev-parse', 'HEAD');
  write(fix.author, SYNOPSES, '{"synopsis":"human correction"}\n');
  commit(fix.author, 'Human correction');
  git(fix.author, 'push', 'origin', 'main');
  const nextBot = clone(fix, 'next-bot');
  const next = runtime(nextBot, 101, first.pulls);
  await assert.rejects(prepare(next));
  assert.match(next.errors[0], /resolve conflicts/);
  assert.equal(git(nextBot, 'ls-remote', 'origin', `refs/heads/${pr.head.ref}`).split('\t')[0], original);
});

test('refuses a sync branch containing unrelated reviewer changes', async t => {
  const fix = fixture(t);
  const first = runtime(fix.bot);
  const pr = await createPendingPr(fix, first);
  const reviewer = clone(fix, 'reviewer');
  git(reviewer, 'switch', '--track', `origin/${pr.head.ref}`);
  write(reviewer, 'unrelated.txt', 'reviewer content\n');
  commit(reviewer, 'Add unrelated content');
  git(reviewer, 'push', 'origin', pr.head.ref);
  const next = runtime(clone(fix, 'next-bot'), 101, first.pulls);
  await assert.rejects(prepare(next), /unrelated files: unrelated\.txt/);
});

test('does not regenerate over a manual manifest edit in the sync PR', async t => {
  const fix = fixture(t);
  const first = runtime(fix.bot);
  const pr = await createPendingPr(fix, first);
  const reviewer = clone(fix, 'reviewer');
  git(reviewer, 'switch', '--track', `origin/${pr.head.ref}`);
  write(reviewer, MANIFEST, 'manifest: reviewer edit\n');
  commit(reviewer, 'Review manifest');
  git(reviewer, 'push', 'origin', pr.head.ref);
  const next = runtime(clone(fix, 'next-bot'), 101, first.pulls);
  await assert.rejects(prepare(next), /manual manifest edit/);
});

test('stops if the sync PR was closed during generation', async t => {
  const fix = fixture(t);
  const first = runtime(fix.bot);
  const pr = await createPendingPr(fix, first);
  const previous = git(fix.bot, 'rev-parse', 'HEAD');
  const nextBot = clone(fix, 'next-bot');
  const next = runtime(nextBot, 101, first.pulls);
  await prepare(next);
  write(nextBot, MANIFEST, 'manifest: new generation\n');
  pr.state = 'closed';
  await assert.rejects(publishSyncPullRequest(next), /no longer open/);
  assert.equal(git(nextBot, 'ls-remote', 'origin', `refs/heads/${pr.head.ref}`).split('\t')[0], previous);
});

test('reports PR creation failure after pushing only the dedicated branch', async t => {
  const fix = fixture(t);
  const run = runtime(fix.bot);
  await prepare(run);
  write(fix.bot, MANIFEST, 'manifest: generated\n');
  run.github.rest.pulls.create = async () => { throw new Error('API denied PR creation'); };
  await assert.rejects(publishSyncPullRequest(run), /API denied PR creation/);
  assert.match(run.errors[0], /was pushed, but the PR was not created/);
  assert.ok(git(fix.bot, 'ls-remote', '--heads', 'origin', run.env.SYNC_BRANCH));
});

test('reports a label failure without pretending the existing PR was labelled', async t => {
  const fix = fixture(t);
  const run = runtime(fix.bot);
  await prepare(run);
  write(fix.bot, MANIFEST, 'manifest: generated\n');
  run.github.rest.issues.addLabels = async () => { throw new Error('API denied label'); };
  await assert.rejects(publishSyncPullRequest(run), /API denied label/);
  assert.equal(run.pulls.length, 1);
  assert.deepEqual(run.pulls[0].labels, []);
  assert.match(run.errors[0], /skip label could not be applied/);
});
