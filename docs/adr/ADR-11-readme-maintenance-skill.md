# ADR-11: Maintain README through a reusable skill

- Status: Accepted
- Date: 2026-10-22

## Context

README maintenance applies beyond suite closure. Mandatory append-only updates
created duplication and prevented correcting obsolete sections.

## Decision

Use [ppa-readme](../../.github/skills/ppa-readme/SKILL.md) for scoped assessment,
correction, extension and justified restructuring. The project instruction calls
for one assessment per coherent repository change set before an eventual commit.
Reuse an assessment only when current relevant contents are still covered.

## Consequences

No update is a valid, explained result. Broad unrelated restructuring requires
confirmation. Restricted agents return findings for an authorized writer without
expanding their permissions. No test, commit, push or PR is implicit.
Ignore maintenance remains conditional on new outputs actually needing rules.
