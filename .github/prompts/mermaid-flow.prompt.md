---
description: 'Generate or refresh Mermaid workflow diagrams (Markdown, optional SVG) for one or more source files'
agent: "Mermaid-flow-engineer"
argument-hint: "<source files or categories> [orientation=TD|LR] [svg=yes|no]"
---

Delegate the task to the `Mermaid-flow-engineer` agent, which must follow the
[`mermaid-flow` skill](../skills/mermaid-flow/SKILL.md) end-to-end:

- Markdown output is always produced under `docs/flows/`.
- SVG output is produced under `docs/flows/images/` only when explicitly
  requested. If the user did not say, the agent asks once before starting.
- Default orientation is top-down (`flowchart TD`). Use left-to-right
  (`flowchart LR`) only when the user asks for it.
- Verify and, if needed, install required CLI/tools (Node, npm, Mermaid CLI,
  local browser, Puppeteer config) before rendering SVG.

If no text prompt is provided with the `/mermaid-flow` command, use the chat
context to determine the implicit request.

${input:Describe which source files to diagram, orientation (TD/LR), and whether SVG is required}
