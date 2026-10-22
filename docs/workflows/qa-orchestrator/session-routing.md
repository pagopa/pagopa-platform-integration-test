# QA orchestrator session routing

This is the mandatory entry procedure for the QA orchestrator, established by
[ADR-01](../../adr/ADR-01-qa-orchestrator-session-routing.md). Read it before
requiring a Jira key or suite name, changing branches, or delegating QA execution.
It does not authorize Git changes merely because the document is being read.

## Identities and scope

- `jira_key`: the human's Jira issue, matching `^PQ-[0-9]+$`, for example `PQ-714`.
  The numeric part is not restricted to three digits.
- Jira branch: a branch matching `^PQ-[0-9]+(?:-.+)?$`. Extract its issue key from
  the prefix, not from an ACE identifier.
- ACE `task_id`: a unique, filesystem-safe identifier for a particular request
  in chat, assigned by the orchestrator according to the ACE capture guide.
  Keep it stable across that request's delegations and traces. A subsequent
  independent request gets a new ID even on the same Jira issue or branch;
  continuations of the same request retain the ID. Do not ask the human for a
  Jira issue merely to name a trace or use the issue key alone as the trace ID.

Stay within QA-related work. A suite name is needed when the operational work
actually requires it, not as a prerequisite for questions or exploration.

## Entry and interaction

1. Check the terminal type. From the repository root, inspect
   `git branch --show-current` and `git status --porcelain=v1 --untracked-files=all`.
   Check command exit codes; on failure, report the error and stop Git actions.
2. Determine the requested workflow from explicit user intent:
   **1: New work**, **2: Resume work**, or **3: Exploration**.
   If unclear, ask the user to choose through the dedicated question tool.
   Do not equate a missing Jira key with an invalid request.
3. Follow the matrix below. Ask one decision at a time, reuse supplied answers,
   and do not repeat a Jira-key question when a valid key is already available.
   A supplied key is not consent to change from another branch to `main`.
4. Before work, summarize the chosen mode, current/resulting branch, and Jira
   association, if any. Assign a separate ACE request ID when substantive work
   or delegation begins; branch selection alone does not define the trace ID.

## Decision matrix

| Current branch | Requested workflow | Required behavior |
|---|---|---|
| `main` | 1: New work | Obtain a valid Jira key from the request or ask for it. Follow **Create a new work branch**. |
| `main` | 2: Resume work | Stop: there is no current Jira work branch to resume. Explain that the user must select an existing work branch or explicitly choose another workflow. Do not silently turn this into workflow 1 or switch branches. |
| `main` | 3: Exploration | Ask whether to create a dedicated branch for possible output files (**recommended**) or remain on `main`. Staying requires no Jira key and no Git transition. If branching is chosen, obtain the Jira key and follow **Create a new work branch**; remain in exploration mode afterward. |
| Jira branch | 1: New work | Obtain the new Jira key from the request or ask for it. Explain that creating the branch requires switching to `main`, and request explicit approval. If approved, apply the transition gate and follow **Create a new work branch**. Otherwise stop the branch-creation path. |
| Jira branch | 2: Resume work | Ask the user to confirm that the request belongs to the displayed current branch and its Jira issue. If yes, keep that branch unchanged and proceed. If no, obtain the intended Jira key, explain the switch to `main`, and request explicit approval; on approval, transition to workflow 1 and follow **Create a new work branch**. |
| Jira branch | 3: Exploration | Ask whether the session concerns the displayed current branch. If yes, proceed without switching or requiring a Jira key. If no, ask whether to create a dedicated branch for possible output files (**recommended**) or remain on the current branch. If staying, preserve the branch without attributing the unrelated request to its Jira issue. If branching, obtain the Jira key, explain and obtain approval for switching to `main`, then follow **Create a new work branch**; remain in exploration mode. |

For a non-Jira branch, do not infer a Jira association: workflow 2 stops with
an explanation; workflow 1 uses the same approval-before-`main` path as any
non-`main` branch; workflow 3 asks whether the request relates to the current
branch and follows the corresponding exploration choice above.

For detached HEAD, report the state and stop workflows 1 and 2 until the user
resolves the branch choice. Workflow 3 may continue as discussion without Git
transitions; explain that a named branch must be selected before creating
repository files. Never guess a branch or attach HEAD automatically.

## Git transition gate

Immediately before **each** checkout, switch, or branch creation, re-run
`git status --porcelain=v1 --untracked-files=all`. Also apply this check before
updating `main`. Approval does not bypass it, and an earlier clean check does not
replace it.

- Interpret the two status columns: `X` is the index, `Y` the working tree.
  A working-tree modification (`Y` other than a space), an untracked entry
  (`??`), or any unresolved conflict blocks the transition.
- Report the blocking paths and stop the requested transition and dependent
  operations. Do not stage, stash, commit, discard, clean, or force a switch to
  get past the gate. Let the user resolve the state and explicitly resume.
- Staged-only changes do not by themselves violate the unstaged-change rule.
  Preserve them and disclose them before a proposed transition; if their task
  association is unclear, ask before carrying them to another work branch.
  Git errors or overwrite warnings always stop the sequence.
- A dirty working tree does not prevent discussion or work explicitly authorized
  on the same branch; do not apply the transition gate as a blanket session ban.
- Approval refusal or a failed Git command ends the transition path. Never
  silently continue on the old branch under the assumption that switching worked.

## Create a new work branch

Use this procedure only after the matrix's choices and approvals are complete.

1. Obtain a valid `jira_key`. Reject malformed values and ask for correction.
   Collect a readable branch suffix: for a new test suite, preserve
   `<jira_key>-<suite-name>-test-suite`; for other work or exploration, use
   `<jira_key>-<short-description>`. Ask for a missing description or suite name.
   Validate the resulting name with `git check-ref-format --branch`.
2. Check that `main` and the intended remote are available. If the target branch
   name already exists locally or on the remote, stop and ask whether to resume
   that branch or choose another name. Never reset or replace an existing branch.
   Missing refs, remote ambiguity, or failed checks are blockers, not permission
   to invent a base branch.
3. If not already on `main`, explain the transition and obtain approval if not
   already granted. Apply the transition gate, then use `git switch main`.
   Check success before continuing.
4. Fetch the remote and update `main` using a fast-forward-only pull from its
   confirmed remote `main` ref. Check the transition gate before the update.
   Stop on fetch/pull failure or divergence; do not merge, rebase, or reset to
   force the update. Recheck the intended new branch's remote availability
   after fetching to avoid using a stale branch-existence result.
5. Apply the transition gate again, then create and switch to the new branch
   using `git switch -c <new-branch> main`. Verify the resulting branch with
   `git branch --show-current`; report any mismatch and stop.
6. Return to the selected mode: operational QA for workflow 1, or exploration
   for workflow 3. Creating an exploration branch does not authorize execution.

## Handoff and mode changes

- **Workflows 1 and 2:** enter the persona's new-suite or modification/fix
  sequence according to the requested work, not according to whether the branch
  is new. Workflow 2 never renames the branch to match a suite convention.
  Delegate operational QA work; preserve runner approvals, the five-iteration
  limit, closer gates, and explicit PR intent.
- **Workflow 3:** answer QA questions, discuss hypotheses, and formulate plans
  without mandatory sub-agent delegation. Delegate a bounded specialist
  question only when needed. Do not automatically implement tests/features,
  run tests, invoke QA-closer, commit, push, or create a PR. Produce requested
  planning documents only on the branch chosen by the user, including `main`
  when explicitly retained. Do not create repository files just to record a plan
  that was only requested in chat.
- If exploration becomes implementation, ask whether to start new work
  (workflow 1) or resume the current Jira branch (workflow 2), then reapply
  routing against the actual current branch. An earlier choice to remain on
  `main` for exploration is not authorization to implement there.
- ACE bookkeeping remains applicable to actual substantive contributions,
  including orchestrator-only exploration. It does not authorize a branch
  change, a commit, or a QA-closer handoff. Keep the trace ID separate from
  Jira and sanitize captured traces before counters or reflection.
