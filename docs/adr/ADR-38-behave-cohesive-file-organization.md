# ADR-38: Cohesive binding organization without mandatory fragmentation

- Status: Accepted

## Decision

Use the [organization conventions](../../.github/instructions/behave-steps.instructions.md#step-file-organization-adr-38):
split by coherent responsibility when useful, not by a mandatory file count or
scenario numbering. A small cohesive suite may have one file; common_steps and
Given/When/Then ordering are contextual conventions, not automatic refactors.

## Consequences

Filenames/tags do not scope binding visibility. Preserve consumer compatibility
and unrelated files; no mass reorganization of existing suites.
