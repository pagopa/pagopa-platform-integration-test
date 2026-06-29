---
name: mermaid-flow
description: |
  Skill for producing Markdown-first Mermaid workflow diagrams for assets in this
  repository. Use when the user asks to generate, regenerate, or render flow
  diagrams (Mermaid) for one or more source files (agents, prompts, instructions,
  documents). The skill defines: directory conventions, file naming, Mermaid
  authoring rules, optional SVG rendering pipeline with prerequisite checks, and
  output contract.
applyTo: "docs/flows/**"
---

# Mermaid Flow skill

Single source of truth for creating and rendering Mermaid workflow diagrams in
this repository. The skill is consumed by the `Mermaid-flow-engineer` agent and
by the `/mermaid-flow` prompt.

## Output contract

- Markdown files (always): `docs/flows/<basename>.md`
  - One Mermaid diagram per file, wrapped in a fenced ```mermaid code block.
  - Diagram orientation defaults to top-down (`flowchart TD`).
  - When the user asks for horizontal/left-to-right, use `flowchart LR`.
  - Each file begins with:
    1. An H1 title summarizing the asset.
    2. A `Source:` line referencing the original file with a relative link.
    3. The Mermaid fenced block.
- SVG files (optional): `docs/flows/images/<basename>.svg`
  - Produced only when the user opts in (see "Asking for SVG").
  - Same `<basename>` as the Markdown file.

## File naming rules

- `<basename>` is the source file stem in kebab-case, prefixed by its kind:
  - `.github/agents/<Name>.agent.md` → `agent-<name>.md` (lowercase, hyphens).
  - `.github/prompts/<name>.prompt.md` → `prompt-<name>.md`.
  - `.github/instructions/<name>.instructions.md` → `instruction-<name>.md`.
  - Any other Markdown source → `doc-<kebab-name>.md`.
- Never overwrite an existing flow file without confirming with the user.

## Diagram authoring rules

- Use `flowchart TD` by default, `flowchart LR` only when explicitly requested.
- Keep nodes short and self-explanatory; quote labels that contain reserved
  characters (slashes, colons, parentheses) using `"..."`.
- Prefer rectangles for actions, diamonds for decisions (`{...}`), and rounded
  shapes only when they add meaning.
- Encode branches with `-- Yes -->` / `-- No -->` for decisions.
- Keep each diagram below ~15 nodes; split otherwise.
- Always model the entry point, the main outcomes, and at least one failure or
  alternative branch where relevant.

## Asking for SVG

- If the user already stated whether SVG output is required, do not ask again.
- Otherwise, ask exactly once before starting work:
  - "Vuoi anche l'output SVG in `docs/flows/images/`, oltre al Markdown?"
- Markdown output is always produced regardless of the SVG answer.

## Orientation handling

- Default: `flowchart TD`.
- If the user says "orizzontale", "left-to-right", "LR", "da sinistra a destra",
  or equivalents, use `flowchart LR` for every diagram in the batch.
- Do not mix orientations inside the same batch unless explicitly requested.

## Prerequisite checks (only when SVG is requested)

Run the following checks once per session, in this order, before rendering SVG:

1. Node.js: `node --version`. Required to drive Mermaid CLI.
2. npm: `npm --version`. Required to install Mermaid CLI locally.
3. Mermaid CLI availability: check
   `.tmp-mermaid/node_modules/@mermaid-js/mermaid-cli/src/cli.js`.
   - If missing, install with:
     - PowerShell: `$env:PUPPETEER_SKIP_DOWNLOAD='1'; npm install --prefix .tmp-mermaid @mermaid-js/mermaid-cli@latest`
     - bash/zsh: `PUPPETEER_SKIP_DOWNLOAD=1 npm install --prefix .tmp-mermaid @mermaid-js/mermaid-cli@latest`
4. Local browser for Puppeteer: locate Microsoft Edge or Chrome at one of:
   - `C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`
   - `C:/Program Files/Microsoft/Edge/Application/msedge.exe`
   - `C:/Program Files/Google/Chrome/Application/chrome.exe`
5. Puppeteer config file `.tmp-mermaid/puppeteer-config.json` with:
   ```json
   {
     "executablePath": "<browser path>",
     "args": ["--no-sandbox", "--disable-setuid-sandbox"]
   }
   ```
   Create it if missing.

If any prerequisite cannot be satisfied, report the blocking step and stop SVG
generation; Markdown output must still be produced.

## SVG rendering procedure

For each Markdown flow file that contains a Mermaid block:

1. Extract the diagram body (text between the ```mermaid fences).
2. Write it to a temporary `.mmd` file (e.g. under the OS temp directory).
3. Render to SVG with:
   ```text
   node .tmp-mermaid/node_modules/@mermaid-js/mermaid-cli/src/cli.js \
     -p .tmp-mermaid/puppeteer-config.json \
     -i <tmp.mmd> \
     -o docs/flows/images/<basename>.svg \
     -b transparent
   ```
4. Delete the temporary file.
5. On parser errors caused by labels containing `/`, wrap the label text in
   double quotes (`A["/qa invocation"]`) and retry once.

## Cleanup

- After successful SVG rendering, `.tmp-mermaid/` and any `*.mmd` artifacts in
  `docs/flows/images/` are temporary and may be removed.
- Keep `docs/flows/*.md` and `docs/flows/images/*.svg` as the only permanent
  outputs of this skill.

## Definition of done

- All requested source files have a corresponding `docs/flows/<basename>.md`.
- Each Markdown file contains exactly one valid Mermaid block in the requested
  orientation.
- When SVG was requested, an `.svg` exists in `docs/flows/images/` for every
  Markdown file.
- The skill never edits source files referenced by the diagrams.
