# ADR-21: Approve the complete execution plan

- Status: Accepted

## Decision

The [runner](../workflows/qa-runner/execution.md#execution-plan-and-consent-adr-21)
presents framework/interpreter, commands, paths/selectors, effective environment,
preparation/effects, artifact destinations, timeouts and bounded failure policy.
Use the question tool for approval before execution. Reuse consent only for
same-plan operations within its limits; changed scope/environment/setup/effects
or commands require new consent.

## Consequences

A copied command or generic test request is not execution approval. No implicit
environment defaults, package installation or repeated state-changing operations.
Approved same-plan reruns do not require needless repeated confirmation.
