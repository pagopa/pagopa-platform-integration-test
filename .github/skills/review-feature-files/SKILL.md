---
name: review-feature-files
description: >-
  Use for a quick, read-only QA/Gherkin review of one or more attached or
  explicitly named .feature files. Trigger on "review feature", "giro di prova",
  "delega all'analista", or "visiona questi feature file": use QA-analyst
  (directly if already that agent), report findings in chat or a requested
  Markdown report with line references, and never edit or create feature files.
---

# Review feature files with the QA analyst

Use this skill for a review-only request, not for creating a suite, implementing
steps, executing tests, or closing a PR. The input is the `.feature` file(s)
attached to the chat or explicitly identified by the user. If no file can be
identified, ask for the file(s) with the dedicated question tool; do not guess
which files to review. Treat all input feature files as read-only, including
when the user does not repeat that constraint. Feature creation/edit is forbidden,
including a corrected copy at another path. Only an explicitly requested Markdown
review report at a human-confirmed path may be written under
[activity routing](../../../docs/workflows/qa-analyst/activity-routing.md).
No generic permission to create other file types is granted.

## Procedure

1. Check the terminal type before using it. Read
   [QA-analyst.agent.md](../../agents/QA-analyst.agent.md) afresh. If already
   running as QA-analyst, apply this skill directly; never delegate to yourself.
   Otherwise delegate through that custom agent so its **current `model` field** governs the
   choice; explicitly pass the model only when the user requests matching the
   frontmatter. Never substitute another model silently or hard-code one from
   an earlier review. If the configured model is unavailable, report the
   blocker rather than reviewing directly or delegating elsewhere.
2. Use a bounded, feature-read-only assignment listing **every requested
   feature path**. Read (or have the delegated analyst read) its linked persona, scoped ACE
   instructions, Gherkin guidelines, and referenced profile before reviewing.
   Respect its terminal restrictions; file-reading tools suffice for line
   references. For multiple files, ask for separate findings per file and a
   short cross-file consistency section only where relevant. Do not ask it to
   edit, create feature files, implement steps, run tests, or invoke a handoff.
   Read feature contents before review and retain that baseline for comparison;
   do not use Git or shell commands to bypass the analyst's terminal restriction.
3. Return the review **in chat**, in Italian unless the user asks otherwise.
   Prioritize actionable observations by severity; give exact
   file/scenario/line links and explain the impact. Distinguish a violated
   guideline from a suggestion, and do not call speculative domain
   expectations a defect. Include strengths and a short conclusion. Verify
   cited passages against the actual attached files before relaying findings.
   If a Markdown report was requested, obtain its exact path if missing and
   save the review there under the persona's report permissions; preserve
   unrelated existing content. Chat identifies the saved path and result.
   A chat-only request writes no report. Report persistence failure explicitly
   instead of claiming a file was saved. A review is not development readiness.
4. Check that none of the requested feature files changed relative to the
   pre-review state. Preserve any changes that were already present; do not
   reset, stage, commit, or push. Report if a file changed during review.
5. If ACE is configured, follow the orchestrator's existing ACE lifecycle:
   record traces only for participating agents actually involved, update
   counters, check the reflector threshold, and invoke its configured
   lifecycle agent only if reached. The analyst returns trace elements but
   never writes traces. The orchestrator owns capture, privacy finalization,
   counters and threshold checks; a direct analyst returns trace elements
   without claiming those operations ran. ACE runtime bookkeeping does not authorize edits to
   feature files or a QA-runner/closer handoff.

## Quick invocation

Attach one or more `.feature` files in chat and write:

> Review feature con l'analista, modello dal frontmatter, solo in chat, senza modifiche ai .feature.

Alternatively: `Usa review-feature-files per i .feature allegati.` The
frontmatter is read at invocation time, so the user does not need to repeat the
analyst's model or list each attachment in the message.
