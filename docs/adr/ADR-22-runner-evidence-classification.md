# ADR-22: Classify verification from actual evidence

- Status: Accepted

## Decision

The [result contract](../workflows/qa-runner/execution.md#evaluate-the-result-adr-22)
uses passed, failed, blocked and inconclusive. Compare actual exit status, intended
selection, counts, execution errors and fresh artifacts. Explain omissions/skips,
undefined cases and coverage limits; unknown facts remain unknown.

## Consequences

Exit zero or zero failures alone cannot imply success. Intentional out-of-scope
exclusions do not invalidate a targeted passing run. Old artifacts are not new
verification, and an unexplained intermittent failure is not erased by a retry.
