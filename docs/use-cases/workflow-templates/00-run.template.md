---
schema: uc-workflow/v1
artifact: run
producer_skill: "{skill-that-initializes-the-run}"
task_id: "{task-id}"
uc_id: "{uc-id}"
run_id: "{YYYYMMDD-NN}"
uc_input: "{path-or-stable-chat-reference}"
uc_revision: "{human-confirmed-revision}"
environment: unknown
revision: 1
status: in_progress
updated_at: "{ISO-8601-with-offset}"
inputs: []
---

# UC - Run

## Agreed inputs
| Item | Value | Human confirmation |
| --- | --- | --- |
| Functional sources | {supplied locators or none} | {reference/date} |
| Data sources | {supplied locators or none} | {reference/date} |
| Feature paths | {exact root-relative paths} | {reference/date} |
| Run directory | {exact root-relative directory} | {reference/date} |
| Gherkin profile inputs | {required user values} | {reference/date} |

## Scenario inventory
| Scenario id | UC elements | Behaviour to cover |
| --- | --- | --- |

## Artifacts
| Artifact | Producer skill | Path | Revision | State |
| --- | --- | --- | --- | --- |
| context | uc-scenario-context | {run-directory}/01-context.md | 0 | not_created |
| test-data | uc-test-data | {run-directory}/02-test-data.md | 0 | not_created |
| feature-report | uc-to-feature | {run-directory}/03-feature-report.md | 0 | not_created |

## Questions
| Question id | Stage | Question | Decision and scope | State |
| --- | --- | --- | --- | --- |

## History
| Timestamp | Skill or human | Action | Output path and revision | Invalidated outputs |
| --- | --- | --- | --- | --- |
