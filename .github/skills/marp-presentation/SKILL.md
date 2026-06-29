---
name: marp-presentation
description: |
  Skill for authoring Marp presentations (Markdown-first) from a user brief.
  Use when the user asks to create, scaffold, or update a Marp deck. The skill
  defines: tooling prerequisites (Marp for VS Code extension, Marp CLI for
  rendering), the user interview (graphic style, communicative tone, color
  palette), color-palette completion rules via chromatic harmony, deck layout
  conventions, and the output contract.
applyTo: "docs/**/*.md"
---

# Marp Presentation skill

Single source of truth for creating and updating Marp presentations in this
repository. Consumed by the `Marp-presentation-engineer` agent and by the
`/marp-presentation` prompt.

## Output contract

- Deck Markdown: `docs/<slug>.md` (slug in kebab-case, derived from the title).
- Optional HTML render: `reports/<slug>.html` (only when the user asks for a
  render or when validation is requested).
- Optional flow appendix: when the deck describes an AI/automation stack, the
  agent may delegate to the `Mermaid-flow-engineer` for appendix diagrams.

The deck must start with a valid YAML front matter block containing at least:

```yaml
---
marp: true
title: <Deck title>
description: <One-line description>
theme: default
paginate: true
size: 16:9
footer: <Short footer>
style: |
  :root {
    --color-primary:   <#hex>;
    --color-secondary: <#hex>;
    --color-accent:    <#hex>;
    --color-light:     <#hex>;
    --color-bg:        <#hex>;
  }
  ...
---
```

## Tooling prerequisites

1. **Marp for VS Code** extension (`marp-team.marp-vscode`):
   - Required for in-editor preview.
   - If the user does not have it installed, suggest installing it. When the
     user agrees, install non-interactively:
     - PowerShell: `code --install-extension marp-team.marp-vscode`
     - bash/zsh: `code --install-extension marp-team.marp-vscode`
   - Verify with `code --list-extensions | Select-String marp-vscode`
     (or `grep marp-vscode` on POSIX shells).
2. **Marp CLI** (only when an HTML/PDF render is requested):
   - Use `npx --yes @marp-team/marp-cli@latest <input.md> --html --output <output.html>`.
   - No global install required.

If `code` is not on PATH, report it and skip the install step; the deck can
still be authored.

## User interview (askQuestions)

Always run the interview before authoring a new deck, unless the user already
provided every required field in the request. Ask in this order, one question
per call:

1. **Graphic style** — short label. Example options to offer when none was
   provided: "minimalista", "corporate", "tecnico/dev", "editoriale",
   "playful". Allow free-form input.
2. **Communicative style/tone** — short label. Example options: "tecnico
   sintetico", "tecnico narrativo", "executive", "didattico", "ironico".
   Allow free-form input.
3. **Main color palette** — accept any of:
   - one or more named tones in human language (e.g. "blu pagoPA",
     "petrolio", "verde menta", "sabbia"),
   - explicit hex codes (e.g. `#1565c0`),
   - a mix of both, with optional role hints
     (`primary`, `secondary`, `accent`, `light`, `bg`).
   The user may provide fewer than five values; the missing roles are
   derived (see "Palette completion").
4. **Topic and structure outline** — if not already implied by the request:
   ask for the deck topic, target audience, duration, and the rough section
   list.
5. **Subtitle and footer customization** — ask two short questions:
   - Subtitle of the title slide (the H2 right below the deck title). Default
     proposal: a short tagline derived from the topic. Allow free-form input,
     including an empty value to skip the subtitle.
   - Footer text rendered on every slide (`footer:` front matter). Default
     proposal: `<deck title> | <repository or context> - <author>`. Ask the
     user for the author's display name if not already known, and append it
     to the footer in the form `<base text> - <author name>`. Allow the user
     to override the full footer string.

Skip a question entirely if the user already answered it in the original
request.

## Palette completion (chromatic harmony)

The deck must always expose five CSS variables: `--color-primary`,
`--color-secondary`, `--color-accent`, `--color-light`, `--color-bg`.

Completion rules, applied in order:

1. **Normalize inputs** to hex:
   - Human names map to a reasonable hex (e.g. "blu pagoPA" → `#1565c0`,
     "petrolio" → `#00695c`, "sabbia" → `#f5deb3`).
   - Hex inputs are kept as-is, lowercased.
2. **Assign roles** when the user provided hints; otherwise:
   - The first value becomes `primary`.
   - The second value becomes `secondary`.
   - The third value becomes `accent`.
   - The fourth value becomes `light`.
   - The fifth value becomes `bg`.
3. **Derive missing roles** from the supplied ones using HSL math:
   - `secondary` = primary with lightness +10–15%, same hue.
   - `accent` = primary shifted +30–60° on hue, saturation kept high.
   - `light` = primary with lightness ~92% and saturation reduced (~30%).
   - `bg` = primary with lightness ~96%, saturation reduced (~15%).
4. **Contrast guardrails**:
   - `primary` must keep WCAG AA contrast against white (>= 4.5:1).
     If not, darken until it does.
   - `light` and `bg` must keep WCAG AA contrast against `#0d2a4a`
     (default text). If not, lighten further.
5. Output the final five hex values in the deck's `style:` block as CSS
   variables, exactly as shown in the front matter template.

## Deck layout conventions

- Use the front matter template above; keep `theme: default` and override via
  the inline `style:` block.
- Provide CSS for: `section`, `h1`, `h2`, `strong`, `code`, `pre`, `table`,
  `th`, `td`, `footer`, `section::after`, `ul, ol`.
- For separator slides use class `section.extra-slide` (full background color,
  centered large H1, no footer/pagination).
- For diagram slides use class `section.flow-slide` with
  `img { width: 100%; max-height: 70vh; object-fit: contain; }`.
- Each content slide: one H1, optional H2, terse bullet lists, and an HTML
  comment with `Speaker note (mm:ss)` at the bottom.
- Target duration: 60–90 seconds per slide, unless the user asks otherwise.

## Communicative style mapping

Use the chosen tone to adjust phrasing and density:

| Tone | Bullet style | Sentence length | Examples |
| --- | --- | --- | --- |
| tecnico sintetico | short noun phrases | <= 12 words | "Workflow QA: 5 ruoli, 4 handoff." |
| tecnico narrativo | full sentences | 15–25 words | "Il QA-runner esegue Behave e..." |
| executive | outcome-first | <= 15 words | "Tempo di chiusura suite -40%." |
| didattico | spiegazione passo-passo | 20–30 words | "Per prima cosa, l'analyst..." |
| ironico | brevi con punchline | <= 18 words | usare con misura |

## Definition of done

- Deck file exists at `docs/<slug>.md` and starts with a valid front matter.
- The five `--color-*` CSS variables are present and consistent with the
  chosen palette.
- The deck contains at least: title slide, agenda slide, one or more content
  slides, takeaway slide.
- If a render was requested, `reports/<slug>.html` exists and was produced by
  Marp CLI.
- The skill never overwrites an existing deck without explicit user
  confirmation.
