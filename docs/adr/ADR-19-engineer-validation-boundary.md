# ADR-19: Return verifiable implementation without automatic execution

- Status: Accepted
- Date: 2026-10-22

## Decision

Use the [validation/result contract](../workflows/qa-engineer/implementation.md#validation-and-return-adr-19).
Remove engineer and utility-specialist frontmatter handoffs. Both perform
read-based checks only; the specialist prepares unit tests for runner execution.

## Consequences

Distinguish implemented-not-run, partial, blocked and review-complete.
Runner execution needs approved commands; no extra terminal permissions are added.
No inferred passing tests, publication consent or ACE trace writes. Existing
authorized runner fix-loop resumption remains valid.
