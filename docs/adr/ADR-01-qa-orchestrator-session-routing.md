# ADR-01: Separate session routing from QA execution

- Status: Accepted
- Date: 2026-10-22

## Context

The orchestrator previously required a task ID and suite name and enforced a
new-suite branch before work could proceed. This conflated starting a Jira task,
resuming an existing branch, and discussing QA questions without implementation.
It also left the Jira issue key and ACE trace `task_id` ambiguous.

## Decision

Keep role responsibilities and QA execution sequences in the orchestrator persona.
Make [session routing](../workflows/qa-orchestrator/session-routing.md) the single,
mandatory operational source for three entry workflows:

1. New work: create a branch from `main` for a Jira issue.
2. Resume work: confirm and retain the existing Jira branch.
3. Exploration: discuss, formulate hypotheses, or plan without automatic branching
   or execution.

The persona and agent wrapper reference this routing document. Do not duplicate
its decision matrix across three workflow files or embed it in the wrapper.
Apply routing before requiring a Jira key, suite name, or operational delegation.

A Jira issue key has the form `PQ-<digits>` and identifies work assigned to the
human. An ACE `task_id` identifies a particular chat request. Several distinct
requests and trace task IDs may belong to the same Jira issue and branch.

Before every checkout, switch, or branch creation, block on unstaged changes,
untracked files, or unresolved conflicts. Staged-only changes are not an automatic
block under this policy and must never be silently unstaged or discarded.
Remaining on the current branch does not trigger this transition gate.

## Consequences

- Existing branches no longer need to match a newly computed suite branch name.
- Exploration does not require Jira or trigger implementation, tests, commit,
  push, or PR creation.
- Branch changes remain explicit, approved where required, and non-destructive.
- Operational QA delegation, test gates, iteration limits, and ACE lifecycle
  remain applicable within their respective scopes.
- Changes to entry behavior belong in the linked routing document; role changes
  remain in the persona. No ACE runtime, generated instructions, or playbooks
  are changed by this decision.
