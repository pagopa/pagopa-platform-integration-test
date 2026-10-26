---
schema: uc-workflow/v1
artifact: feature-report
producer_skill: uc-to-feature
task_id: "{task-id}"
uc_id: "{uc-id}"
run_id: "{run-id}"
uc_input: "{path-or-stable-chat-reference}"
uc_revision: "{human-confirmed-revision}"
environment: unknown
revision: 1
status: incomplete
updated_at: "{ISO-8601-with-offset}"
inputs:
  - path: "{run-directory}/01-context.md"
    revision: 1
  - path: "{run-directory}/02-test-data.md"
    revision: 1
---

# UC - Feature report

## Feature outputs
| Root-relative feature path | Producer skill | Write result |
| --- | --- | --- |

## Mapping
| Scenario id | UC steps | Resulting Gherkin steps | Evidence ids | Granularity rationale |
| --- | --- | --- | --- | --- |

## Coverage
| UC element | Scenario id | Feature path | Scenario title | Examples row or not-applicable | Coverage and reason |
| --- | --- | --- | --- | --- | --- |

## Data and oracles
| Scenario id | Combination id or not-applicable | Data ids | Oracle ids | Applied values or unresolved ids |
| --- | --- | --- | --- | --- |

## Questions
| Question id | Scenario id | Missing detail or conflict | State |
| --- | --- | --- | --- |

## Checks
| Check | Method actually used | Result | Evidence |
| --- | --- | --- | --- |

## Engineer handoff
{Explain each scenario and any step-text change; draft is not permission to implement}

## Readiness
{pronta per lo sviluppo or bozza; reasons, missing coverage and unresolved ids;
syntax is not execution readiness}
