# ADR-10: Separate commit, push and PR authorization

- Status: Accepted
- Date: 2026-10-22

## Context

The previous PR gate interpreted passing tests as consent to open a PR.
It did not clearly preserve an explicit refusal or independent push restrictions.

## Decision

Pass independent commit, push and PR decisions through the
[publication plan](../workflows/qa-closer/closure.md#actions-and-approval-gates-adr-09-and-adr-10).
Reuse explicit intent, ask for unresolved decisions, and preserve refusals.
Verification success is a technical gate, not an authorization.

## Consequences

Commit-only and no-push requests do not inherit a skill's default publication.
A PR may use an existing published branch; a forbidden required push blocks
that PR action instead of overriding consent. Existing PRs are not duplicated.
