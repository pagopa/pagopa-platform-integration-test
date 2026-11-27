'use strict';

const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const BASE = 'main';
const BRANCH_PATTERN = /^automation\/gherkin-sync\/run-[0-9]+-[0-9]+$/;
const GENERATED_FILES = new Set([
  '.github/gherkin-manifest.yml',
]);

function git(cwd, ...args) {
  return execFileSync('git', args, {
    cwd,
    encoding: 'utf8',
    env: { ...process.env, GIT_TERMINAL_PROMPT: '0' },
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trimEnd();
}

function names(value) {
  return value ? value.split('\0').filter(Boolean) : [];
}

function ensureGeneratedOnly(cwd) {
  const changed = names(git(cwd, 'diff', '--name-only', '-z', 'origin/main...HEAD'));
  const unexpected = changed.filter(name => !GENERATED_FILES.has(name));
  if (unexpected.length) {
    throw new Error(`The sync PR contains unrelated files: ${unexpected.join(', ')}`);
  }
  return changed;
}

function rejectHumanManifestCommits(cwd) {
  const revisions = git(
    cwd, 'rev-list', '--first-parent', 'origin/main..HEAD', '--', '.github/gherkin-manifest.yml',
  ).split('\n').filter(Boolean);
  for (const revision of revisions) {
    const [name, email] = git(cwd, 'show', '-s', '--format=%an%x00%ae', revision).split('\0');
    if (name !== 'github-actions[bot]' || email !== 'github-actions[bot]@users.noreply.github.com') {
      throw new Error('The sync PR contains a manual manifest edit; review and merge it before regenerating.');
    }
  }
}

function isSyncPullRequest(pr, repository) {
  return pr.user?.login === 'github-actions[bot]'
    && pr.head?.repo?.full_name === repository
    && BRANCH_PATTERN.test(pr.head.ref)
    && pr.base?.ref === BASE;
}

async function prepareSyncBranch({ github, context, core, cwd = process.cwd(), env = process.env }) {
  const repository = `${context.repo.owner}/${context.repo.repo}`;
  const pulls = await github.paginate(github.rest.pulls.list, {
    ...context.repo, state: 'open', base: BASE, per_page: 100,
  });
  const existing = pulls.filter(pr => isSyncPullRequest(pr, repository));
  if (existing.length > 1) {
    throw new Error('More than one Gherkin sync PR is open; resolve the duplicates before retrying.');
  }

  const runId = String(context.runId);
  const attempt = env.GITHUB_RUN_ATTEMPT;
  if (!/^[0-9]+$/.test(runId) || !attempt || !/^[0-9]+$/.test(attempt)) {
    throw new Error('A numeric GitHub run ID and attempt are required for the sync branch.');
  }
  const pr = existing[0];
  const branch = pr ? pr.head.ref : `automation/gherkin-sync/run-${runId}-${attempt}`;
  git(cwd, 'fetch', '--no-tags', 'origin', 'refs/heads/main:refs/remotes/origin/main');
  const baseSha = git(cwd, 'rev-parse', 'refs/remotes/origin/main');
  git(cwd, 'config', 'user.name', 'github-actions[bot]');
  git(cwd, 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com');

  if (pr) {
    git(cwd, 'fetch', '--no-tags', 'origin', `refs/heads/${branch}:refs/remotes/origin/${branch}`);
    git(cwd, 'switch', '-c', branch, '--track', `origin/${branch}`);
    try {
      git(cwd, 'merge', '--no-edit', 'origin/main');
    } catch (error) {
      core.error(`Could not merge main into sync PR #${pr.number}; inspect the Git error and resolve conflicts before retrying.`);
      throw error;
    }
    ensureGeneratedOnly(cwd);
    rejectHumanManifestCommits(cwd);
  } else {
    git(cwd, 'switch', '-c', branch, 'origin/main');
  }
  core.setOutput('branch', branch);
  core.setOutput('pr_number', pr ? String(pr.number) : '');
  core.setOutput('base_sha', baseSha);
  core.info(pr ? `Reusing sync PR #${pr.number}.` : `Preparing a new sync branch: ${branch}.`);
}

function renderPullRequestBody(template, runUrl, manifestOutcome) {
  const sections = {
    '#### List of Changes': 'Update the generated Gherkin manifest.',
    '#### Motivation and Context': 'Keep the repository data aligned with merged feature changes. Review the manifest before merging.',
    '#### How Has This Been Tested?': [
      'No tests are run by the generation workflow.',
      `Initial generation step outcome: manifest **${manifestOutcome}**.`,
      `Check the [workflow run](${runUrl}), later update comments and PR checks.`,
    ].join('\n\n'),
    '#### Screenshots (if appropriate):': 'Not applicable.',
  };
  let body = template;
  for (const [heading, text] of Object.entries(sections)) {
    if (body.split(heading).length !== 2) {
      throw new Error(`The pull request template must contain exactly one '${heading}' heading.`);
    }
    body = body.replace(heading, `${heading}\n\n${text}`);
  }
  return body;
}

async function getOpenSyncPullRequest(github, repository, branch, number) {
  const { data: pr } = await github.rest.pulls.get({ ...repository, pull_number: number });
  const name = `${repository.owner}/${repository.repo}`;
  if (pr.state !== 'open' || !isSyncPullRequest(pr, name) || pr.head.ref !== branch) {
    throw new Error(`Sync PR #${number} is no longer open on ${branch}; rerun the workflow.`);
  }
  return pr;
}

async function ensureSkipLabel(github, repository, pr) {
  if (!pr.labels.some(label => label.name === 'skip')) {
    await github.rest.issues.addLabels({
      ...repository, issue_number: pr.number, labels: ['skip'],
    });
  }
}

async function publishSyncPullRequest({ github, context, core, cwd = process.cwd(), env = process.env }) {
  const branch = env.SYNC_BRANCH;
  const baseSha = env.SYNC_BASE_SHA;
  const numberText = env.SYNC_PR_NUMBER;
  if (!BRANCH_PATTERN.test(branch || '') || !/^[0-9a-f]{40,64}$/.test(baseSha || '')) {
    throw new Error('The prepared sync branch or base commit is invalid.');
  }
  if (numberText && !/^[1-9][0-9]*$/.test(numberText)) {
    throw new Error('The prepared sync PR number is invalid.');
  }
  if (git(cwd, 'branch', '--show-current') !== branch) {
    throw new Error('The current branch is not the prepared sync branch.');
  }
  const number = numberText ? Number(numberText) : null;
  const runUrl = `${env.GITHUB_SERVER_URL}/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;
  const body = number ? null : renderPullRequestBody(
    fs.readFileSync(path.join(cwd, '.github', 'PULL_REQUEST_TEMPLATE.md'), 'utf8'),
    runUrl, env.MANIFEST_OUTCOME,
  );

  for (const file of GENERATED_FILES) {
    if (fs.existsSync(path.join(cwd, file)) || git(cwd, 'ls-files', '-z', '--', file)) {
      git(cwd, 'add', '--all', '--', file);
    }
  }
  const staged = names(git(cwd, 'diff', '--cached', '--name-only', '-z'));
  if (staged.some(name => !GENERATED_FILES.has(name))) {
    throw new Error('Unrelated files are staged; no commit or pull request was created.');
  }
  if (staged.length) {
    git(cwd, 'commit', '-m', 'chore: sync Gherkin manifest');
  }

  git(cwd, 'fetch', '--no-tags', 'origin', 'refs/heads/main:refs/remotes/origin/main');
  if (git(cwd, 'rev-parse', 'refs/remotes/origin/main') !== baseSha) {
    throw new Error('main changed during generation; rerun the workflow against the latest base.');
  }
  if (!ensureGeneratedOnly(cwd).length) {
    core.info('No generated changes to propose.');
    return;
  }

  if (number) {
    await getOpenSyncPullRequest(github, context.repo, branch, number);
  }
  const updated = !number || git(cwd, 'rev-parse', 'HEAD') !== git(cwd, 'rev-parse', `refs/remotes/origin/${branch}`);
  git(cwd, 'push', 'origin', `HEAD:refs/heads/${branch}`);
  let pr;
  if (number) {
    pr = await getOpenSyncPullRequest(github, context.repo, branch, number);
  } else {
    try {
      ({ data: pr } = await github.rest.pulls.create({
        ...context.repo,
        base: BASE,
        head: branch,
        title: 'chore: sync Gherkin manifest',
        body,
      }));
    } catch (error) {
      core.error(`The branch ${branch} was pushed, but the PR was not created.`);
      throw error;
    }
  }
  core.setOutput('pr_url', pr.html_url);
  try {
    await ensureSkipLabel(github, context.repo, pr);
  } catch (error) {
    core.error(`Sync PR ${pr.html_url} exists, but its skip label could not be applied.`);
    throw error;
  }
  if (number && updated) {
    try {
      await github.rest.issues.createComment({
        ...context.repo,
        issue_number: number,
        body: `Updated by [workflow run](${runUrl}). Manifest: **${env.MANIFEST_OUTCOME}**. Check the run and PR checks.`,
      });
    } catch (error) {
      core.error(`Sync PR ${pr.html_url} was updated, but its run summary comment could not be posted.`);
      throw error;
    }
  }
  core.notice(`Gherkin sync PR ready for review: ${pr.html_url}`);
}

module.exports = { prepareSyncBranch, publishSyncPullRequest };
