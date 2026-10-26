# ADR-32: Separate utility review, implementation and maintenance

- Status: Accepted

## Decision

Use the [utility activity contract](../workflows/python-utility-engineer/implementation.md#activity-routing-adr-32)
for review, implement/extend and fix/refactor. Review returns findings and only
an explicitly requested Markdown report; no implementation or corrected copies.
Explanation-only requests remain in chat.

## Consequences

Core routing belongs in the persona/workflow, not a mandatory new skill.
Explicit correction requests authorize their actual scope without redundant
generic questions; supplied files alone do not authorize changes.
