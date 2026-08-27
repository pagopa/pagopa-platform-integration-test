---
name: add-catalog-asset
description: |
  Skill for authoring a new MCP catalog manifest + asset body from a real source
  Markdown file (a SKILL.md, *.agent.md, *.prompt.md, or *.instructions.md). Use
  when the user wants to add a new distributable asset to the modelless MCP
  catalog scaffold. The skill deterministically infers `kind`, `id`, and
  `description` from the source file's name and frontmatter — falling back to
  Markdown content inference only as a last resort — then writes the manifest
  YAML and (if needed) the asset body file, ready for commit/PR/rebuild. Replaces
  the runtime `POST /v1/assets` API (removed as unnecessary: real usage is
  push/PR + image rebuild, not a live write endpoint).
---

# Add Catalog Asset skill

Single source of truth for turning a real repo asset file (skill/agent/prompt/
policy Markdown) into a catalog manifest under
`mcp_blueprint/modelless-mcp/mcp-server-scaffold/manifests/`. The catalog itself
has **no runtime write API**: this skill is how new assets are authored, and they
reach a running deployment the normal way — commit, push, PR, image rebuild
(the `Dockerfile` already does `COPY manifests ./manifests` and
`COPY app ./app`, and `AssetCatalog.load_dir()` picks up every `manifests/*.yaml`
at startup — no code change needed for a rebuild to include new files).

## When to use

Use when the user provides (by path or pasted content) a source Markdown file and
asks to register/add it to the MCP catalog scaffold as a new distributable asset.

## Inputs

- `source` (required): the source Markdown file — a file path in the repo, or
  its raw content pasted/attached in context.
- `id`, `version`, `install_target_path` (ask the user if not provided — see
  step 4; these cannot be reliably inferred from the source content alone).
- `visibility`, `owner` (optional; default `visibility: private`, `owner` from
  context or asked once).

## Procedure (for the local model)

### 1. Read the source and split frontmatter from body

Read the source file (or use the provided content). If it starts with a `---`
YAML block, parse it as `frontmatter`; everything after the closing `---` is
`body`. If there is no frontmatter block, treat `frontmatter` as empty and warn
the user — real assets in this repo always declare one.

If `body` is empty after stripping the frontmatter, stop and ask the user for a
valid source file: an asset with no content cannot be registered.

### 2. Infer `kind` — try each rule in order, stop at the first match

Apply the rules **in this exact order**. Only fall through to the next rule set
if the current one does not produce a match. Never skip straight to content
inference (rule set C) if rule sets A or B already resolved it.

**A. Filename convention (most reliable — matches this repo's real authoring
convention, confirmed across all existing assets):**

- Filename is exactly `SKILL.md` (case-insensitive) → `skill`
- Filename ends with `.agent.md` → `agent`
- Filename ends with `.prompt.md` → `prompt`
- Filename ends with `.instructions.md` → `policy`

**B. Frontmatter key signals (use only when no filename is available, e.g. the
user pasted raw content, or the filename doesn't match any pattern above):**

- Has `argument-hint` → `prompt` (every real prompt in this repo declares it)
- Has any of `tools`, `agents`, `user-invocable`, `model` → `agent`
- Has `applyTo` **and** also `name` → `skill` (skills declare both; a bare
  `applyTo` with no `name` is the policy shape — see next)
- Has `applyTo` and nothing else from the signals above → `policy`

**C. Content inference (absolute last resort — only if A and B are both
inconclusive):**

- Body has `## Inputs` and/or `## Procedure`/`## Output contract` headings →
  `skill`
- Body describes a multi-step workflow that delegates/hands off to named
  sub-agents → `agent`
- Body is a short imperative paragraph containing a `${input:...}` placeholder →
  `prompt`
- Body is a flat list of rules/conventions with no `## Procedure`-style
  structure → `policy`

If even (C) is inconclusive, **stop and ask the user** to state the `kind`
explicitly. Do not guess silently.

Report to the user which rule matched (e.g. "inferred `kind: skill` from the
filename `SKILL.md`") for transparency.

### 3. Infer `id`

- `skill`: kebab-case name of the **parent directory** of a `SKILL.md` file
  (e.g. `.github/skills/mermaid-flow/SKILL.md` → `mermaid-flow`). If content was
  pasted with no path, kebab-case the frontmatter `name`.
- `agent`: filename stem with the `.agent.md` suffix stripped, kebab-cased
  (e.g. `QA-orchestrator.agent.md` → `qa-orchestrator`).
- `prompt`: filename stem with the `.prompt.md` suffix stripped, kebab-cased
  (e.g. `qa.prompt.md` → `qa`).
- `policy`: filename stem with the `.instructions.md` suffix stripped,
  kebab-cased (e.g. `gherkin.instructions.md` → `gherkin`).
- No usable filename in any case above: kebab-case the frontmatter `name`, or
  the first `# Heading` in the body if `name` is absent.

Always validate the result against `^[a-z0-9][a-z0-9-]*$` (the same rule the
catalog itself enforces) and check it doesn't collide with an existing
`manifests/*.yaml` id. If invalid or colliding, show the derived id to the user
and ask for confirmation or an alternative — do not silently rename.

### 4. Infer `description`

- Primary: the frontmatter `description` field, verbatim (every real asset in
  this repo has one).
- Fallback (last resort, content-based): the first non-empty paragraph of the
  body after stripping headings.

### 5. Ask the user only for what truly isn't inferable

- `version`: default `1.0.0` for a brand-new asset unless the user says
  otherwise.
- `install_target_path`: the local hard-install destination. Propose a default
  from the convention (`.github/skills/<id>/SKILL.md`,
  `.github/agents/<PascalName>.agent.md`, `.github/prompts/<id>.prompt.md`,
  `.github/instructions/<id>.instructions.md`) but confirm with the user, since
  the exact casing/prefix (e.g. `QA-` vs `qa-`) isn't derivable from `id` alone.
- `visibility` / `owner`: ask once if not already clear from context; otherwise
  default `visibility: private`.

### 6. Map kind-specific frontmatter fields into the manifest

Only map fields that are actually present — never invent values:

| kind | frontmatter key | manifest field |
|---|---|---|
| agent | `tools` | `tools` |
| agent | `agents` | `subagents` |
| agent | `user-invocable` | `user_invocable` |
| prompt | `agent` | `target_agent` |
| policy | `applyTo` | `apply_to` |

### 7. Write the files

1. Asset body: `mcp_blueprint/modelless-mcp/mcp-server-scaffold/app/assets/<kind>.<id>.md`
   — the verbatim frontmatter + body copied from the source (mirrors the
   existing `skill.mermaid-flow.md` / `agent.qa-orchestrator.md` convention).
2. Manifest: `mcp_blueprint/modelless-mcp/mcp-server-scaffold/manifests/<kind>.<id>.yaml`
   — following the field order/style of the existing sample manifests and the
   matching template in `manifests/_templates/<kind>.yaml`. Always include
   `install.target_path` (required by `AssetCatalog.register_dict`) and
   `body_file: <kind>.<id>.md`.

Do not call any HTTP endpoint — there isn't one. Both files are created directly
in the working tree.

### 8. Report back

Summarize for the user: inferred `kind`/`id`/`description` and which rule
resolved each, the two file paths written, and remind them that:

- Loading the new asset in a **locally running** server requires a restart
  (`docker compose restart`, or re-run `uvicorn` if running directly) —
  `AssetCatalog.load_dir()` only runs at startup.
- Shipping it to any other deployment requires committing both files and
  rebuilding the image (`docker compose up --build`) or letting CI do it on
  merge — there is no live registration call.

## Output contract

- Exactly one new (or updated, if `overwrite`-equivalent is confirmed with the
  user) manifest file under `manifests/`.
- Exactly one new (or updated) asset body file under `app/assets/`, unless the
  manifest uses inline `body`/`template` instead of `body_file` (acceptable for
  short prompt/policy content, but `body_file` is the default for consistency).
- No HTTP calls, no server restart performed by the skill itself — only file
  writes in the working tree, left for the user to commit/PR/rebuild.
