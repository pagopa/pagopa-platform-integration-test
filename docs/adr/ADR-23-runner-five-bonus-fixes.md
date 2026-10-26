# ADR-23: Five bonus fix attempts after the initial failure

- Status: Accepted

## Decision

The [fix loop](../workflows/qa-runner/execution.md#five-bonus-fix-attempts-adr-23)
starts only with authorization. The initial failure is attempt 0, followed by
up to five bonus fix attempts 1 through 5: at most six normal verification runs.
The user can skip fixes and go directly to the report or stop earlier.
Reserve/count attempts when started, preserve history and budgets across
delegations/resumption. No-change diagnostic retries need a separate finite
approval and cannot extend/reset the loop.

## Consequences

Engineer fixes require defect evidence and exact ownership; only integrated
corrections are reverified. Environment/service/configuration and functional
ambiguity return to the orchestrator. Exhaustion never triggers automatic reset,
retry-until-green or masking failed tests.
