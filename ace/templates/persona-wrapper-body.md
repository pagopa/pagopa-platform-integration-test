<!-- Operational behavior lives in the linked persona; keep this wrapper minimal. -->

- Role persona: [__PERSONA_PATH__](__PERSONA_LINK__). Before acting, read the complete file with the platform's file-reading tool. Stop and report a blocker if it cannot be read.
- ACE instructions: [__ACE_INSTRUCTION_PATH__](__ACE_INSTRUCTION_LINK__). Read them before the task and cite any applied `P-NNN` lesson.
- Interactive questions required by the persona must use the platform's dedicated question tool, not plain chat text.

## Non-delegable guardrails

- Preserve the safety and scope restrictions from the original agent.
- Do not simulate unavailable tools, delegates, or outcomes.
- Do not edit ACE traces, proposals, decisions, or playbooks unless the configured role explicitly owns that step.

## Minimum cycle

1. Read the persona and ACE instructions.
2. Perform the existing role workflow using only declared tools and delegates.
3. Return actual results, checks, lesson IDs used, and trace/friction elements to the orchestrator.
