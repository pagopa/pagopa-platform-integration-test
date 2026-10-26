# ADR-13: Make closure resumable without recursive ACE commits

- Status: Accepted
- Date: 2026-10-22

## Context

Commit, push and PR can fail independently. The closer's trace is captured only
after it returns, so it cannot be required inside the commit it describes.

## Decision

Use [ACE boundaries and recovery](../workflows/qa-closer/closure.md#ace-boundary-and-recovery-adr-13).
The closer returns actual state and trace elements; the orchestrator captures
and privacy-finalizes traces. Include only explicitly scoped traces with real
sanitization evidence. Resume from the last verified publication state.

## Consequences

A failed push does not recreate a commit, and a failed PR does not repeat a push.
Recheck branch, scope, evidence, destination and consent on resume. No raw trace
publication, recursive trace commits, amendments or duplicate PRs are allowed.
