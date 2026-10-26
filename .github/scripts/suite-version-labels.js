'use strict';

const { suites } = require('../nrt-suites.json');

const VERSION_LABELS = new Set(['minor', 'major', 'patch']);
const DEPENDENCY_BOTS = new Set(['dependabot[bot]', 'renovate[bot]']);
const SUITE_IDS = suites.map(suite => suite.id.toLowerCase());

function resolveSuiteVersionLabels({ labels, author }) {
  const names = labels.map(name => name.toLowerCase());

  if (names.includes('skip')) {
    return { status: 'skip', message: 'Skipping suite versioning because the skip label is present.' };
  }

  if (DEPENDENCY_BOTS.has(author.toLowerCase())) {
    return { status: 'skip', message: `Skipping suite versioning for dependency updates by ${author}.` };
  }

  // Preserve the existing selection when multiple increment labels are present.
  const versionLabel = names.filter(name => VERSION_LABELS.has(name)).pop();
  if (!versionLabel) {
    return {
      status: 'invalid',
      message: 'Missing required labels. Please add major, minor, patch, or skip.',
    };
  }

  const suiteLabels = names.filter(name => SUITE_IDS.includes(name));
  if (suiteLabels.length === 0) {
    return {
      status: 'invalid',
      message: `Missing suite label. Please use one of: ${SUITE_IDS.join(', ')}. Add skip if no suite version should change.`,
    };
  }

  if (suiteLabels.length > 1) {
    return {
      status: 'invalid',
      message: 'More than one suite label is present. Please create separate PRs to version multiple suites, or use skip if no suite version should change.',
    };
  }

  return {
    status: 'bump',
    versionLabel,
    suiteLabel: suiteLabels[0],
    message: `The ${suiteLabels[0]} suite will receive a ${versionLabel} version bump.`,
  };
}

async function verifyPullRequestLabels({ github, context, core }) {
  const labels = await github.paginate(github.rest.issues.listLabelsOnIssue, {
    ...context.repo,
    issue_number: context.issue.number,
    per_page: 100,
  });
  const result = resolveSuiteVersionLabels({
    labels: labels.map(label => label.name),
    author: context.payload.pull_request.user.login,
  });

  core.setOutput('should_bump', result.status === 'bump' ? 'true' : 'false');
  if (result.status === 'invalid') {
    core.setFailed(result.message);
    return result;
  }

  core.info(result.message);
  if (result.status === 'bump') {
    core.setOutput('version_label', result.versionLabel);
    core.setOutput('suite_label', result.suiteLabel);
  }
  return result;
}

module.exports = { resolveSuiteVersionLabels, verifyPullRequestLabels };
