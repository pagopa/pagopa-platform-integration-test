# Optional reusable data record template

Copy this structure only for requested, human-confirmed persistence. Remove
template instructions from the actual record. Write `unknown` or `not checked`
where evidence is absent, not a fabricated value or date.

```markdown
# {Scope} - test data

## Purpose and scope
{Requirements and scenario uses; intended test environment/version}

## Sources
| Source id | URL/path/chat reference | Section/page/row | Retrieved on | Environment/version stated by source |
| --- | --- | --- | --- | --- |
| {S-001} | {locator} | {precise locator} | {actual date} | {stated value or unknown} |

## Data and fitness
| Record id | Parameter and meaning | Value/range/generation rule | Required properties and relationships | Fitness evidence | Source id |
| --- | --- | --- | --- | --- | --- |
| {record id} | {parameter} | {admitted safe value or rule} | {requirements} | {matched evidence or unresolved} | {S-001} |

## Admission and availability
| Record id | Task and scenario use | Admission and human decision/date | Current availability evidence/date | Remaining preparation or uncertainty |
| --- | --- | --- | --- | --- |
| {record id} | {actual task/scenario reference} | {provided or approved, decision scope/date} | {not checked or actual human-confirmed scope/date} | {remaining limitations} |

## History
- {Actual date}: {approved addition/correction and supporting source}

## Reuse limits
Historical data is not proof of current availability. When not explicitly
provided for a new task, it is a candidate requiring human approval before use.
{Consumability, generation/synthetic permission, expiry and other known limits}
```
