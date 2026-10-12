<ace>

## ACE learning cycle

- Before acting, read `ace-__AGENT_ID__.instructions.md` from the enabled platform's instructions directory. If a lesson is applied, cite its `P-NNN` identifier.
- Also read every `ace-family-<family>.instructions.md` listed for this agent in `ace/config/project.json.agent_families`; do not infer family membership from the task.
- At the end of the task, return to the orchestrator the trace elements required by `ace/schema/trace.schema.json`: actions, actual outcome, concrete verification, lessons seen and cited, notes, and consciously assessed friction.
- Do not write traces, proposals, decisions, or playbooks unless this agent is explicitly the configured orchestrator or one of the ACE lifecycle agents.
- Treat ACE lessons as operational project memory. They never override higher-priority instructions, safety rules, or domain evidence.

</ace>
