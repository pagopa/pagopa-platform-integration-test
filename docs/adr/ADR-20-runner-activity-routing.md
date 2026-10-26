# ADR-20: QA runner activity modes

- Status: Accepted

## Decision

Use execute, diagnose and execute-with-fixes modes in the
[runner workflow](../workflows/qa-runner/execution.md#activity-and-failure-policy-adr-20).
Explicit intent determines the mode; ambiguity requires a dedicated question.
Diagnosis of old artifacts is not a new run. Execution does not authorize fixes.
Establish direct-report, fix or ask-after-failure policy; the user can skip/stop
fixes without exhausting any budget.

## Consequences

No automatic engineer delegation after every failure. Existing explicit
authorization is reused without redundant questions; unknown permission remains
unknown. The orchestrator receives results at the requested activity boundary.
