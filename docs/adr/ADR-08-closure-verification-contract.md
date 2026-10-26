# ADR-08: Require scoped, current closure evidence

- Status: Accepted
- Date: 2026-10-22

## Context

The closer required an increase in passing tests or a fixed failure, but received
no precise verification contract. Legitimate updates could be rejected while old
"all green" results could be accepted.

## Decision

Use the [closure input contract](../workflows/qa-closer/closure.md#closure-input-contract-adr-08).
The runner returns actual command, environment, tested contents, counts, exclusions,
flaky findings and artifact references. The orchestrator passes these with scope,
branch, decisions and previous closure state.

## Consequences

An increased test count is not required. Relevant changes after verification
block publication pending fresh evidence. QA-closer never reruns tests, infers
missing success or demands an unrelated full-suite run.
