# ADR-18: Parallelize engineers only with disjoint write ownership

- Status: Accepted
- Date: 2026-10-22

## Decision

Apply [collision-free scheduling](../workflows/qa-engineer/implementation.md#collision-free-scheduling-adr-18)
before parallel work. Shared steps, hooks, helpers and unit tests have one writer;
group or serialize overlaps and recheck integrated bindings/context.

## Consequences

One engineer per feature is conditional, not an isolation guarantee. Assign
shared context/lifecycle contracts even for file-disjoint work. Report newly
discovered overlap before editing. Static checks do not prove runtime uniqueness.
