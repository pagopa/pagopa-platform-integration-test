---
schema: uc-workflow/v1
artifact: context
producer_skill: uc-scenario-context
task_id: "{task-id}"
uc_id: "{uc-id}"
run_id: "{run-id}"
uc_input: "{path-or-stable-chat-reference}"
uc_revision: "{human-confirmed-revision}"
environment: unknown
revision: 1
status: incomplete
updated_at: "{ISO-8601-with-offset}"
inputs: []
---

# UC - Functional context

## Sources
| Source id | Locator | Section or page | Retrieved at | Environment and version | Admission | Human decision reference |
| --- | --- | --- | --- | --- | --- | --- |

## Functional evidence
| Evidence id | Scenario id | UC element | Question | Supported detail | Source id and passage | State |
| --- | --- | --- | --- | --- | --- | --- |

## Mapping
| Scenario id | UC step | Proposed action or check | Evidence ids | Reason for granularity |
| --- | --- | --- | --- | --- |

## Oracles
| Oracle id | Scenario id | AC or postcondition | Property and expected value | Timing semantics | Evidence ids | State |
| --- | --- | --- | --- | --- | --- | --- |

## Data requirements
| Data id | Scenario id | Parameter and meaning | Constraints and relationships | Required entity state | Evidence ids |
| --- | --- | --- | --- | --- | --- |

## Questions
| Question id | Scenario id | Missing detail or conflict | Human decision and scope | State |
| --- | --- | --- | --- | --- |

## Readiness
{State, supported and missing coverage, blockers; no test execution claims}
