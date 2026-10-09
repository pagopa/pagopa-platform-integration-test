---
name: review-behave-steps
description: >-
  Use for a quick, read-only QA review of one or more attached or explicitly
  named Python Behave step definition files. Trigger on "review step",
  "giro di prova step", "delega all'ingegnere", or "visiona questi step
  python": delegate to QA-engineer using the model currently declared in its
  frontmatter, report findings in chat with line references, and never edit or
  create step files.
---

# Review Behave step files with the QA engineer

Use this skill for a review-only request, not for creating a suite,
implementing steps, executing tests, or closing a PR. The input is the Python
file(s) under `src/**/steps/**/*.py` attached to the chat or explicitly
identified by the user. If no file can be identified, ask for the file(s) with
the dedicated question tool; do not guess which files to review. Treat all input
step files as read-only, including when the user does not repeat that
constraint. Step file creation/edit is forbidden. Other file types creation-only,
if needed, is allowed.

## Procedure

1. Check the terminal type before using it. Read
   [QA-engineer.agent.md](../../agents/QA-engineer.agent.md) afresh. Delegate
   through that custom agent so its current `model` field governs the choice;
   explicitly pass the model only when the user requests matching the
   frontmatter. Never substitute another model silently or hard-code one from an
   earlier review. If the configured model is unavailable, report the blocker
   rather than reviewing directly or delegating elsewhere.
2. Give the engineer a bounded, read-only assignment listing every requested
   step path. Have the engineer read its linked persona, scoped ACE
   instructions, Python and Behave-step guidelines, and referenced profile
   before reviewing. Respect its terminal restrictions; file-reading tools
   suffice for line references. For multiple files, ask for separate findings
   per file and a short cross-file consistency section only where relevant. Do
   not ask it to edit, create step files, implement logic, run tests, or invoke
   a handoff.
3. Return the review in chat, in Italian unless the user asks otherwise.
   Prioritize actionable observations by severity; give exact file/step/line
   links and explain the impact. Distinguish a violated guideline from a
   suggestion, and do not call speculative domain expectations a defect.
   Include strengths and a short conclusion. Verify cited passages against the
   actual attached files before relaying findings.
4. Check that none of the requested step files changed relative to the
   pre-review state. Preserve any changes that were already present; do not
   reset, stage, commit, or push. Report if a file changed during review.
5. If ACE is configured, follow the orchestrator's existing ACE lifecycle:
   record traces only for participating agents actually involved, update
   counters, check the reflector threshold, and invoke its configured lifecycle
   agent only if reached. The engineer returns trace elements but never writes
   traces. ACE runtime bookkeeping does not authorize edits to step files or a
   QA-runner/closer handoff.

## Quick invocation

Attach one or more step files under `src/**/steps/**/*.py` and write:

> Review step Behave con l'ingegnere, modello dal frontmatter, solo in chat, senza modifiche ai file Python.

Alternatively: `Usa review-behave-steps per i file step Behave allegati.` The
frontmatter is read at invocation time, so the user does not need to repeat the
engineer's model or list each attachment in the message.
