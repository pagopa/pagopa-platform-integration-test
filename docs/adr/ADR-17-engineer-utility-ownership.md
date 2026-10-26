# ADR-17: Separate bindings and wiring from reusable utility ownership

- Status: Accepted
- Date: 2026-10-22

## Decision

Follow the [ownership contract](../workflows/qa-engineer/implementation.md#file-and-utility-ownership-adr-17).
QA-engineer owns scoped bindings/assertions and authorized hook wiring.
Python-utility-engineer owns reusable utility changes, local and shared.

## Consequences

Reuse existing APIs first. Delegation specifies owned paths, API, behaviour,
compatibility and unit cases. No duplicate helpers hidden in hooks or steps.
Unavailable delegation is a dependency blocker, not permission to take over.
