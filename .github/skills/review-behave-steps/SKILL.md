---
name: review-behave-steps
description: >-
  Use for a quick, read-only QA review of one or more attached or explicitly
  named Python Behave step definition files. Trigger on "review step",
  "giro di prova step", "delega all'ingegnere", or "visiona questi step
  python": use QA-engineer directly if already that agent, otherwise delegate
  to it. Report findings in chat or a requested Markdown report with line
  references; never edit or create code or feature files.
---

# Review Behave step files with the QA engineer

Use this skill for a review-only request, not for creating a suite,
implementing steps, executing tests, or closing a PR. The input is the Python
file(s) under `src/**/steps/**/*.py` attached to the chat or explicitly
identified by the user. If no file can be identified, ask for the file(s) with
the dedicated question tool; do not guess which files to review. Treat all input
step files as read-only, including when the user does not repeat that
constraint. No code or feature file may be created or modified, including corrected
copies. Only an explicitly requested Markdown report at an agreed path may be
written. Read [the activity workflow](../../../docs/workflows/qa-engineer/implementation.md)
for permissions, result states and ACE ownership.

## Procedure

1. Check the terminal type before using it. Read
   [QA-engineer.agent.md](../../agents/QA-engineer.agent.md) afresh. When already
   QA-engineer, apply this skill directly; never self-delegate. Otherwise delegate
   through that custom agent so its current `model` field governs the choice;
   explicitly pass the model only when the user requests matching the
   frontmatter. Never substitute another model silently or hard-code one from an
   earlier review. If the configured model is unavailable, report the blocker
   rather than reviewing directly or delegating elsewhere.
2. Use a bounded, code-read-only assignment listing every requested
   step path. Read (or have the delegated engineer read) its linked persona, scoped ACE
   instructions, Python and Behave-step guidelines, and referenced profile
   before reviewing. Respect its terminal restrictions; file-reading tools
   suffice for line references. For multiple files, ask for separate findings
   per file and a short cross-file consistency section only where relevant. Do
   not ask it to edit, create step files, implement logic, run tests, or invoke
   a handoff.
   Retain the read baseline for comparison; no shell/Git checks are authorized
   for QA-engineer by this skill.
3. Return the review in chat, in Italian unless the user asks otherwise.
   Prioritize actionable observations by severity; give exact file/step/line
   links and explain the impact. Distinguish a violated guideline from a
   suggestion, and do not call speculative domain expectations a defect.
   Include strengths and a short conclusion. Verify cited passages against the
   actual attached files before relaying findings.
   For a requested Markdown report, confirm the path if missing, preserve unrelated
   existing content and report the actual saved path. Chat-only requests write
   no report. Failed writes are explicit, never reported as saved artifacts.
   Return `review-complete` or a precise partial/blocked result, not test success.
4. Check that none of the requested step files changed relative to the
   pre-review state. Preserve any changes that were already present; do not
   reset, stage, commit, or push. Report if a file changed during review.
5. If ACE is configured, follow the orchestrator's existing ACE lifecycle:
   the orchestrator records traces only for actual participating agents, performs
   privacy finalization, counters and threshold checks, and invokes lifecycle
   agents only as required. The engineer returns trace elements but never writes
   traces or claims that orchestrator operations ran during a direct invocation.
   ACE runtime bookkeeping does not authorize edits to step files or a
   QA-runner/closer handoff.

## Quick invocation

Attach one or more step files under `src/**/steps/**/*.py` and write:

> Review step Behave con l'ingegnere, modello dal frontmatter, solo in chat, senza modifiche ai file Python.

Alternatively: `Usa review-behave-steps per i file step Behave allegati.` The
frontmatter is read at invocation time, so the user does not need to repeat the
engineer's model or list each attachment in the message.
