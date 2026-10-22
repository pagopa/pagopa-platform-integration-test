# QA closure workflow (ADR-08 through ADR-13)

QA-closer prepares documentation and performs only authorized publication actions.
It does not run tests, fix code/features, choose a new branch, or capture ACE traces.
Read the complete workflow before closure; stop if required inputs cannot be read.

## Closure input contract (ADR-08)

The orchestrator supplies the following facts, using explicit `unknown` or
`not-applicable` for missing evidence rather than invented success:

| Input | Required content |
| --- | --- |
| Identity and scope | Expected work branch; Jira key if known; current ACE request ID; UC identity if applicable; exact intended files and work type |
| Verification | Runner's exact command, suite/environment, time, branch/revision and relevant working-tree contents verified, exit status, passed/failed/error/skipped/undefined counts, exclusions and flaky findings |
| Evidence | Actual output/artifact/log paths or accessible references; what was not checked; whether verification covers all requested changes |
| Documentation | README assessment and its covered contents/scope, if already performed |
| Publication plan | Independent `commit`, `push` and `create_pr` decisions (`true`, `false` or unresolved), exact commit message, remote/head/base choices and PR inputs where applicable |
| Prior closure state | README assessment, error report, commit hash, push result and PR URL already produced, including errors or partial completion |

A larger test count or a previously failing test is not required for a legitimate
update/refactor. Passing applicable checks of the intended changes is the normal
publication gate. The runner supplies evidence, not just "all green".

Before publication, compare evidence against the actual relevant current contents,
including staged/unstaged inputs, configuration and dependencies. A matching HEAD
alone does not establish freshness for uncommitted changes. Missing/unreadable
artifacts, unexplained exclusions, zero executed tests, relevant undefined/skipped
cases or unresolved flaky findings do not count as blanket success. Return gaps
to the orchestrator for the runner or a scoped human decision; do not rerun tests
or waive failures yourself. Do not demand the full repository suite when targeted
verification adequately covers the authorized change.

Reader-only documentation and ignore updates do not automatically invalidate
test results; changes to execution inputs or executable code/configuration do.
If relevant contents changed after verification, stop publication and request
fresh evidence. Never relabel an unverified result as passed.

## Actions and approval gates (ADR-09 and ADR-10)

1. Check terminal type and repository state from the root using read-only Git
   commands. Confirm the current branch is the expected work branch. Detached HEAD,
   `main`, the repository default branch, or any unexpected branch blocks Git
   publication. Report it; do not checkout, switch, create a branch or repair
   routing inside QA-closer.
2. Confirm exact intended files and preserve pre-existing staging/edits. Add only
   relevant README/ignore outputs explicitly covered by closure. Unrelated staged
   content blocks a commit until its scope is resolved; do not include it or
   unstage it silently. Do not stage local reports or ignored files forcibly.
3. Resolve each action independently through the dedicated question tool only
   when needed. Reuse clear user authorizations; explicit refusal takes precedence.

| Decision | Meaning |
| --- | --- |
| `commit: true` | Create a scoped commit after the evidence gate, using the exact orchestrator message |
| `push: true` | Publish the authorized commits to the confirmed destination, after the evidence gate |
| `create_pr: true` | Open/reuse the authorized PR after the evidence gate and required publication |
| Any explicit `false` | Skip that action; do not ask again to override a refusal |
| Unresolved decision | Ask before that action; test success does not supply consent |

A PR request can use an already published branch without a new commit or push.
If a PR needs an unpublished commit but push is forbidden, report the dependency
and stop that action; do not override the refusal. `create_pr: false` does not
cancel an independently authorized commit/push. A no-push/commit-only restriction
must be passed explicitly to the commit skill rather than relying on its default.

4. Before a push, inspect outgoing commits as well as the current index: existing
   commits can contain unrelated or unverified work. If their authorization or
   verified scope is unclear, stop and resolve it. Recheck branch, destination,
   relevant contents and approval before each publication action, including resume.
5. Use [ppa-commit](../../../.github/skills/ppa-commit/SKILL.md) as the Git procedure
   source, passing the exact file scope, message and push restriction. Preserve the
   subject/body and apply its required trailer policy. A message conflict is a
   blocker, not permission to rewrite the orchestrator message.
   For an authorized push-only action or retry of an existing commit, use only
   the skill's push procedure; never invoke its commit/staging steps again.
6. Use [ppa-pr](../../../.github/skills/ppa-pr/SKILL.md) only when authorized. Preserve
   reviewers, release labels, explicit source/target routing and PR template rules.
   PR-body completion is not a standalone error report. Reuse existing PRs rather
   than creating duplicates; do not silently edit an existing PR without permission.

No merge, force push, amend, history rewriting, hook bypass, staging-all shortcut,
secret publication or generated-output inclusion is authorized by closure.

## Documentation and ignore maintenance (ADR-11)

Apply [ppa-readme](../../../.github/skills/ppa-readme/SKILL.md) once for the current
coherent change set, or reuse an assessment that actually covers its current
contents. A new suite may need usage/location documentation; a fix may need a
targeted correction or no README change. Correct obsolete material instead of
appending duplicate suite sections. Report `no-update-needed` when appropriate.

Inspect existing ignore rules only for new local/generated outputs from this
work. Add a narrowly scoped rule only if needed; preserve existing rules and
tracked files. Do not create or edit `.gitignore` merely because closure ran.
Local ignored reports remain local; publication requires a separate authorized
destination, not an automatic ignore exception.

## Error-only Markdown reporting (ADR-12)

Create or update a standalone closure report **only for work on test suites with
unresolved errors in the relevant evidence**, including unresolved intermittent
failures explicitly reported by the runner. Successful work, non-suite repository
maintenance, a missing count increase, or a Git/PR/tool failure alone does not
generate a suite report. Earlier failures resolved by current verified results
do not require a new error report.

- Normal publication requires successful verification. With unresolved suite
  errors, the orchestrator may request **report-only** closure: no commit, push
  or PR through this path. A possible partial/failing-work publication requires
  a separate explicit decision outside successful closure, not a warning bypass.
- First reuse the runner's relevant Markdown failure report when it already
  documents the same evidence. Do not generate a duplicate for the same failure.
  If a report is missing/incomplete, write or extend an agreed `.md` path under
  `reports/`, preserving existing findings and recording the evidence used.
- Write in Italian: concise summary and counts, affected tests/files, actual
  errors and limited traceback evidence, established/suspected cause distinguished,
  attempts, remaining blockers and next steps. Do not invent execution or counts.
  Unknown values remain unknown; unavailable evidence is an explicit limitation.
- No HTML/Allure generation or serving, Confluence templates/API, external
  publication, or template lookup for a standalone report. The GitHub PR template
  remains mandatory when creating a PR through ppa-pr.
- Use only actual runner artifacts; do not run tests to reconstruct a report.
  Avoid secrets and personal data. A failed report write is an explicit partial
  failure, not a saved report. Final chat status and ACE trace elements remain
  required even when no standalone report is applicable.

## ACE boundary and recovery (ADR-13)

The analyst/engineer/runner/closer return trace elements; the orchestrator owns
capture and project privacy finalization. Do not create or edit ACE files here.
ACE files are excluded from closure scope by default. Include only explicitly
authorized trace files with actual evidence of successful privacy finalization
for those contents; a filename or a human statement alone is not proof of a
successful sanitization command. Raw or uncertain trace contents must not be
staged, committed or published.

The closer's own trace is captured after its result by the orchestrator. It
need not be in the commit it describes. There is no recursive commit to include
that trace and no second automatic publication after finalization.

Return actual state before stopping. On resumption, verify recorded state using
read-only Git/gh checks; do not infer success from an earlier attempted command.

| Last verified state | Resume behavior |
| --- | --- |
| No commit created | Reconcile partial documentation/report writes, current scope, evidence and approval before retrying |
| Commit created, push failed or not attempted | Preserve the hash; retry only the authorized push, not a new commit |
| Push verified, PR failed or not attempted | Recheck authorization and existing PR, then perform only the needed PR step |
| PR verified | Return its actual metadata/URL; do not duplicate it |
| Prior state cannot be established | Report the uncertainty and ask before any potentially duplicate write |

The same approved actions may be retried only within unchanged scope/destination;
new edits, commits, destinations or a later refusal require reassessment. Never
amend to hide a failed step. New uncommitted work is not part of a prior commit
and does not justify repeating the old closure blindly.

## Output

Return a concise result to the orchestrator, not only the commit/PR skill's
individual output:

- Closure mode and result: `completed`, `report-only`, `partial` or `blocked`;
  verified evidence scope and unresolved issues.
- README assessment/changed sections; ignore changes or why unnecessary.
- Error report path actually saved/reused, or `not-applicable`; not a success report.
- Commit message/hash or explicit not-created/skipped; push destination/result
  and PR URL/result, with failed, skipped and existing states distinguished.
- Next safe action for recovery, if any.
- Actual actions, checks, lesson IDs and friction for the current ACE request.

Never claim an artifact, published branch, completed PR or passed test without
its corresponding evidence.
