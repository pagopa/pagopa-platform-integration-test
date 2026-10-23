# ADR-31: Separate QA results from ACE lifecycle recovery

- Status: Accepted

## Decision

Apply [ACE-stage recovery](../workflows/qa-orchestrator/operations.md#qa-result-and-ace-lifecycle-adr-31):
retain actual QA outcome separately from capture/privacy/counters/threshold/
reflection status. Privacy failure stops trace consumption/publication and
subsequent ACE processing; it does not relabel passing tests as failed.

## Consequences

Resume only the established blocked stage after checking persisted state and
replay safety. No blind counter/reflection repeats, finalized trace overwrites,
new test runs or duplicate Git actions to recover bookkeeping. Preserve canonical
ACE schemas/runtime, correction-trace rules and human-approved warden ownership.
