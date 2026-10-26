# QA closure contract validation

The [closure workflow](closure.md) and [ppa-readme](../../../.github/skills/ppa-readme/SKILL.md)
are checked by the existing QA contract tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\unit\qa_workflow\test_uc_workflow_contract.py -q
```

These are development-time contract checks, not permissions for QA-closer to
run tests. They check asset clauses, tables, links and metadata, not a simulated
agent or real publication. A behavioural trial needs actual user-authorized
inputs and observed tool results. The following table records expected outcomes,
not evidence that these scenarios have been executed.

| Case | Input or state | Expected result |
| --- | --- | --- |
| C-01 | Passing targeted verification of a legitimate update without increased test count | Accept applicable evidence; no artificial improvement or full-suite requirement |
| C-02 | Executable/configuration changes after the reported run | Stop publication and return to orchestrator for fresh evidence; no closer test rerun |
| C-03 | Unexpected branch, main/default branch or detached HEAD | No publication or branch repair; explain the mismatch |
| C-04 | Unrelated staged files or outgoing commits | Stop the affected publication until scope is resolved; preserve unrelated work |
| C-05 | Green tests with create_pr false | No PR; independently authorized commit/push remain possible |
| C-06 | Commit-only request | Pass no-push restriction to ppa-commit; no implicit PR |
| C-07 | PR requested, unpublished commits, push forbidden | Report dependency; never override refusal |
| C-08 | Existing published branch and authorized PR, no new commit/push | Use existing branch and existing-PR checks without an empty commit |
| C-09 | Current README assessment covers unchanged relevant contents | Reuse it; no duplicate append, cosmetic edit or recursive assessment |
| C-10 | Restricted role discovers a README correction | Return required change for an authorized writer; do not bypass permissions |
| C-11 | Successful suite work or non-suite maintenance | No standalone closure report or HTML generation |
| C-12 | Unresolved suite errors with a runner Markdown report | Reuse report in report-only mode; no commit/push/PR |
| C-13 | Report needed but missing evidence or write failure | Mark unknowns/failure explicitly; no invented counts or saved-report claim |
| C-14 | Commit created, push failed | Verify existing hash and retry only authorized push |
| C-15 | Push verified, PR failed or already exists | Recheck authorization/existing PR and resume only needed PR action |
| C-16 | Closer returns before its ACE trace exists | Orchestrator captures/finalizes later; no raw trace staging or recursive commit |

When trying these with an agent, record input scope, authorizations, actual
evidence, partial results and the observed next action. Passing static assertions
does not prove that a live agent or Git operation followed this procedure.
