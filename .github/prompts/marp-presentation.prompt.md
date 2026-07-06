---
description: 'Author or update a Marp presentation deck from a brief (style, tone, color palette in human language or hex)'
agent: "Marp-presentation-engineer"
argument-hint: "<topic> [audience] [duration] [graphic-style] [tone] [colors: names or #hex]"
---

Delegate the task to the `Marp-presentation-engineer` agent, which must follow
the [`marp-presentation` skill](../skills/marp-presentation/SKILL.md)
end-to-end:

- Verify that `Marp for VS Code` (`marp-team.marp-vscode`) is installed; ask
  before installing.
- Run the user interview (graphic style, communicative tone, color palette,
  topic/audience/duration/outline) only for fields not already specified in
  this request.
- Accept the color palette as human-language tones, hex codes, or a mix.
- Complete the five-role palette (`primary`, `secondary`, `accent`, `light`,
  `bg`) via chromatic harmony when the user provided fewer values, applying
  WCAG AA contrast guardrails.
- Produce the deck under `docs/<slug>.md`. Render HTML only on request.

If no text prompt is provided with the `/marp-presentation` command, use the
chat context to determine the implicit request.

${input:Describe the deck (topic, audience, duration, graphic style, tone, color palette)}
