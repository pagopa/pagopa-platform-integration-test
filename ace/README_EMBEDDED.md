# ACE: Agentic Context Engineering — embedded integration

ACE is a framework that turns execution into durable operating memory for a team of agents. Instead of embedding the same rules in every prompt and improvising them task by task, the team records what actually happened, reflects on it, turns repeated patterns into structured proposals, validates those proposals, and then applies only the decisions that have real evidence behind them.

The result is a learning loop: `trace` files become evidence, `proposal` documents become candidate changes, and the `playbook` plus the generated `instructions` become the system's durable, reusable context.

This repository is the runtime template for the cycle. It does not contain a real domain application or a real team. It contains the generic engine that can be installed into a host project and then grown by that project's own evidence.

## Install, update, and migration

Install creates ACE where it is absent; use
[INSTALL_PROMPT_EMBEDDED.md](../INSTALL_PROMPT_EMBEDDED.md). Update advances an
existing installation without changing its integration paradigm; use
[UPDATE_PROMPT.md](../UPDATE_PROMPT.md). Migration changes embedded to
mediated (or materially restructures project-owned agent behavior) and needs a
separate plan and explicit approval.

An embedded installation that predates `integration_mode` is **legacy
embedded**. Its update should add `integration_mode: "embedded"` and refresh
ACE only in the agents that already participate. That normalization preserves
the paradigm and is not a migration; an updater must neither enroll additional
agents nor convert the installation to mediated mode.

For update inventory, the kit provides a read-only command:

```text
node <KIT_ROOT>/ace/scripts/inspect_update.js --target <TARGET_ROOT>
```

It reports detected mode, version and ownership evidence, conflicts, and
required configuration normalization without writing (`write_performed:
false`). `ace/runtime-version.json` defines the runtime version, ownership
classes, and hashes for kit-owned files. Treat both as evidence for the update
procedure, never as authority to overwrite project configuration, operational
behavior, playbooks, traces, or state.

## The ACE cycle, top-down

The best way to read ACE is from the outside in:

1. a task is executed by an agent;
2. a `trace` records what happened;
3. a `reflector` reads a batch of traces and proposes a change;
4. a `curator` turns proposals into typed `decision` objects;
5. a `warden` validates the decision and asks for explicit human sign-off;
6. the `playbook` is updated, then `instructions` are regenerated from it;
7. the next session starts with better context and cleaner operating rules.

This is not a diagnostic engine and not a business-logic engine. It is an operational learning loop that uses evidence to improve the agent system itself.

## Runtime structure

```text
ace/
├── config/
│   ├── project.json             # real runtime configuration for the host project
│   └── thresholds.json          # batch triggers for reflector / curator / warden
├── prompts/
│   ├── reflector.md             # how the `reflector` reads traces and proposes change
│   ├── curator.md               # how the `curator` turns proposals into decisions
│   └── warden.md                # how the `warden` validates and applies the signed-off delta
├── schema/
│   ├── trace.schema.json        # shape of one `trace`
│   └── bullet.schema.json       # shape of one `bullet` inside the `playbook`
├── proposals/
│   └── applied/                 # processed batches, decisions, and gate reports
├── scripts/
│   ├── generate_ace_agents.js   # renders platform wrappers and runtime agents
│   ├── retrieval.js             # regenerates platform `instructions` from the `playbook`
│   ├── check_threshold.js       # decides whether the next stage should trigger
│   ├── update_counters.js       # sums evidence from traces into bullet counters
│   ├── gate.js                  # mechanical validation before a write is allowed
│   ├── apply_delta.js           # applies the signed-off delta to the `playbook`
│   ├── inspect_update.js        # read-only update inventory and conflict report
│   └── validate_install.js      # verifies the installed runtime is structurally complete
├── runtime-version.json         # runtime version, ownership, and kit-file hashes
├── state/
│   └── live-exclusions.json     # runtime exclusions while a bad rule is under review
├── traces/
│   ├── processed/               # traces that have already been folded into a batch
│   └── CAPTURE_GUIDE.md         # how one trace should be written
├── playbooks/                  # durable source of learned rules
│   ├── _global.md
│   ├── families/
│   ├── archive/
│   └── <agent>.md
└── README_EMBEDDED.md          # embedded-integration lifecycle reference
```

The important architectural point is that the runtime is deliberately split between the durable, reviewable `playbook` and the generated, compact `instructions` used by the active session.

## The core objects in the loop

### `trace`

A `trace` is the evidence record for a task. It records the facts that matter to learning: which `playbook` bullets were seen, which were cited, what happened, and whether the outcome was verified.

Example:

```json
{
  "task_id": "T-204",
  "agent": "planner",
  "started_at": "2026-09-16T09:00:00Z",
  "ended_at": "2026-09-16T09:14:00Z",
  "playbook_bullets_seen": ["PR-011", "PR-015"],
  "playbook_bullets_cited": ["PR-011"],
  "outcome": {
    "status": "success",
    "evaluated_by": "verified"
  },
  "notes": "The file path check prevented a wrong-target write.",
  "friction": ["The path was ambiguous at first."],
  "counted_for_playbook_at": "2026-09-16T09:15:00Z"
}
```

### `proposal`

A `proposal` is a candidate rule, not a write. The `reflector` reads batches of `trace` files and produces structured hypotheses about what should change.

Example:

```json
{
  "proposal_id": "PR-042",
  "batch_id": "batch-2026-09-16",
  "relation_to_existing": "UPDATE",
  "target_bullet_id": "PR-011",
  "confidence": "high",
  "final_content": "Before writing a file, verify the destination path and extension before creating the file.",
  "rationale": "This was cited in two different tasks and prevented wrong-target writes."
}
```

### `decision`

A `decision` is the curator's typed response to a `proposal`. It says whether the proposal becomes `ADD`, `UPDATE`, `DEPRECATE`, `MERGE`, `PROMOTE`, or `REJECT`.

Example:

```json
{
  "proposal_id": "PR-042",
  "decision": "UPDATE",
  "target_bullet_id": "PR-011",
  "scope": "global",
  "curator_rationale": "The evidence is consistent and the rule is already close to the intended behavior."
}
```

## The lifecycle in four stages

```text
`trace` capture
        ↓
`reflector` reads batch and emits `proposal`
        ↓
`curator` turns proposal into `decision`
        ↓
`warden` validates and requests human sign-off
        ↓
`playbook` update + `instructions` regeneration
```

### 1. `trace` capture

The runtime records one `trace` per relevant agent per task. This is the raw evidence for the rest of the loop. A `trace` is intentionally compact: it is not a narrative of the session, only a structured record of relevant facts, outcomes, friction, and evidence.

### 2. `reflector`

The `reflector` works in batch. It reads all unprocessed `trace` files, detects recurring patterns, checks against the current `playbook`, and writes a structured `proposal` file. It never edits the `playbook` directly and it never decides operationally whether a rule should be live.

### 3. `curator`

The `curator` receives the batch of proposals and converts each one into a typed `decision`. This is the point where the system stops reacting to a single anecdote and starts turning noisy evidence into a defensible decision.

### 4. `warden`

The `warden` is the safety gate. It performs deterministic checks such as schema validity, ID consistency, and operation compatibility. It also blocks writes unless a human explicitly approves the final action. This is where the learning loop is kept honest.

## Human in the loop

ACE is intentionally not a silent auto-optimizer. The human remains part of the loop at the point where a change can actually affect the durable runtime.

The pattern is:

```text
mechanical validation -> explicit question -> human review -> signed-off write
```

This matters because the system is learning from real execution data, not manufacturing confidence. `gate.js` can check structure and consistency, but it cannot reliably judge semantic conflict between a new rule and the existing `playbook` in the same scope. That remains a human judgment.

The human sign-off is therefore not optional decoration. It is the mechanism that turns a proposed change into a real runtime decision. Without that explicit confirmation, `apply_delta.js` refuses to write, and `retrieval.js` will not regenerate the operational `instructions` from the new state.

In other words, the human is the final reviewer of the system's memory. The system can propose and validate; only the human decides whether the new rule belongs in the durable operating context.

## `playbook` and `instructions`: different content, different purpose

The difference is intentional. A `playbook` is the durable source of truth; `instructions` are the generated runtime view the active session sees.

```text
`playbook`                                              `instructions`
────────────────────────────────────────────────────────────────────────────────────
Source of truth for the team                             Generated runtime artifact
Has durable metadata: status, scope, tags, counters      Stripped to the operational directives
Stores provenance and evidence                           No governance metadata in the agent context
Designed for review, debate, promotion, deprecation      Designed for fast consumption by a live agent
May contain candidates, quarantine, archive states       Only active, safe, retrieved content is served
```

This separation exists for two reasons:

- The `playbook` must preserve the full lifecycle of a rule: how it was created, what evidence supports it, what status it has, and which counters it has accumulated.
- The `instructions` need to be compact, readable, and safe for an active agent to consume in-session. They are a filtered subset of the `playbook`, not a second source of truth.

A rule that has been deprecating or quarantined should not stay active in the generated context just because the system is still holding on to it in memory. Retrieval resolves that by applying the latest counters and exclusion policy before generating `instructions`.

## Example: the real `playbook` format, the schema, and the generated `instructions`

The most important correction is this: the real `playbook` on disk is not a standalone JSON object. It is a markdown file in `playbooks/*.md`, and the actual bullet format is the one parsed by [ace/scripts/lib/playbook.js](../ace/scripts/lib/playbook.js) and described in the comment inside [playbooks/_global.md](../playbooks/_global.md).

This means there are two layers to understand:

- the logical schema in [ace/schema/bullet.schema.json](../ace/schema/bullet.schema.json), which is the canonical JSON shape used for validation and runtime logic;
- the markdown serialization in the `playbook` file itself, which is what the script writes and reads on disk.

The real markdown format is:

```md
## P-014 — active — used:12 helped:9 hurt:1
Before creating a file, verify the target path and extension before writing.

tags: [filesystem, write, path]
counters: helped_confirmed=7; helped_provisional=2; hurt_confirmed=1; hurt_provisional=0
provenance: source_trace_ids=[T-108, T-201]; created_at=2026-09-16T10:00:00Z; created_by=reflector+curator; batch_id=batch-2026-09-16
```

The logical schema for the same rule is the JSON model used by validation, not the literal file format:

```json
{
  "id": "P-014",
  "status": "active",
  "scope": { "type": "global" },
  "content": "Before creating a file, verify the target path and extension before writing.",
  "tags": ["filesystem", "write", "path"],
  "counters": {
    "used": 12,
    "helped": 9,
    "hurt": 1,
    "helped_confirmed": 7,
    "helped_provisional": 2,
    "hurt_confirmed": 1,
    "hurt_provisional": 0
  },
  "provenance": {
    "source_trace_ids": ["T-108", "T-201"],
    "created_at": "2026-09-16T10:00:00Z",
    "created_by": "reflector+curator"
  }
}
```

The generated `instructions` are intentionally smaller and stripped of governance metadata. The same rule becomes:

```markdown
- **[P-014]** When the described procedure depends on a specific appliance or container (induction hob, microwave, sealed jar, roaster, etc.), always involve `<cook-physicist>` even if the user request does not explicitly contain keywords related to physics or safety.
```

The important point is that the `playbook` keeps the full operational record, while the `instructions` are only the filtered runtime view that the live agent consumes.

## Why `PR`?

The acronym `PR` in ACE is chosen to mean `playbook rule`. The underlying idea is that every bullet is a small, reviewable operational rule: a unit of knowledge that can be evaluated, promoted, updated, deprecated, or rejected as evidence changes.

This makes `PR` a meaningful identifier for the atomic unit of the learning loop, not a generic label. In a human-facing document, `PR` communicates that the object is an operational rule in the durable memory of the system, not just a temporary note or an arbitrary comment.

A good example is an identifier such as `PR-014`—short, stable, and semantically meaningful for a reviewed rule in the `playbook`.

## The structure of a `bullet`

A `bullet` is the smallest unit of learned instruction in ACE. The fields are intentionally separated between operational content and governance metadata.

```json
{
  "id": "PR-014",
  "status": "active",
  "scope": { "type": "global" },
  "content": "Check the target location before writing a new file.",
  "tags": ["filesystem", "write"],
  "counters": {
    "used": 12,
    "helped": 9,
    "hurt": 1
  },
  "provenance": {
    "source_trace_ids": ["T-108", "T-201"],
    "created_at": "2026-09-16T10:00:00Z",
    "created_by": "reflector+curator"
  }
}
```

The operational text is what an agent sees in-session. Everything else—counters, provenance, lifecycle state—exists to support governance and safe retrieval.

## Why the cycle is batch-oriented

ACE is designed around batches, not single-case reactions. A single task is not enough to justify a structural change to the `playbook`. The system waits until a meaningful set of traces exists, then runs the `reflector`, then the `curator`, then the `warden`.

This creates a disciplined learning rhythm:

- small daily signals are gathered as `trace` data;
- repeated patterns are aggregated in a batch;
- the system proposes only after evidence accumulates;
- only a signed-off `decision` can produce a durable change.

## Conclusion

ACE is not about automating the team away. It is about giving the team a structured memory that improves over time without forcing every rule into every prompt by hand.

The real pattern is simple:

```text
`trace` -> `proposal` -> `decision` -> `playbook` -> `instructions` -> better next session
```

What makes the system safe is the disciplined separation between evidence collection, proposal generation, review, and final human sign-off. That is the reason ACE can learn without silently drifting into inconsistent or unreviewed behavior.

## Appendix: quick purpose of each `ace` script

The runtime is intentionally small, but each script has a narrow role. The following appendix is a quick map of who does what, when it runs, and why it exists.

### `generate_ace_agents.js`

- Purpose: render or verify the per-platform agent wrappers used to invoke ACE roles.
- When: during setup or whenever the platform configuration changes.
- Why: ensure the host project has the correct wrapper agents for the configured runtime.

### `check_threshold.js`

- Purpose: determine whether the next stage should trigger automatically.
- When: after a session, after a reflector batch, or after a curator batch.
- Why: batch-driven learning needs a mechanical threshold, not a guess. If a threshold is below 1, the stage is treated as "skip" and remains manual-only.

### `update_counters.js`

- Purpose: sum trace evidence into the counters of each active bullet.
- When: before opening a new reflector batch and whenever evidence changes.
- Why: keep the durable playbook and the live exclusion logic aligned with real execution data.

### `retrieval.js`

- Purpose: generate the runtime `instructions` from the active `playbook` state.
- When: after a playbook change and before a live session consumes the context.
- Why: avoid drifting instructions and keep the session context derived from the reviewed source of truth.

### `gate.js`

- Purpose: perform deterministic validation of a curator decision file.
- When: before a human sign-off and before any write to the `playbook` is allowed.
- Why: check schema coherence, duplicate IDs, semantic safety constraints, and evidence existence.

### `apply_delta.js`

- Purpose: write the signed-off batch to the `playbook` and then re-run retrieval.
- When: only after `gate.js` passes and the human signs off.
- Why: this is the only stage that mutates the durable runtime knowledge.

### `validate_install.js`

- Purpose: verify the installation is structurally complete.
- When: after installation or before a run that assumes the runtime is ready.
- Why: fail early on missing or unresolved project configuration.

### `inspect_update.js`

- Purpose: inspect an existing installation against
  `runtime-version.json`, reporting versions, ownership states, conflicts, and
  configuration normalization without changing the target.
- When: before planning an update and again after its validation.
- Why: provide deterministic inventory evidence while leaving reconciliation
  decisions to [UPDATE_PROMPT.md](../UPDATE_PROMPT.md).

These scripts are intentionally narrow. They do not replace the human review step, and they do not all write state. The main pattern is: collect evidence -> count it -> propose -> decide -> gate -> human sign-off -> apply -> regenerate instructions.
