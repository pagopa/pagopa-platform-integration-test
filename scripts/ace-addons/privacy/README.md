# ACE privacy addon (project-owned)

This addon runs **after** ACE writes its canonical traces and **before** ACE
updates counters or starts the reflector. It does not change the installed ACE
runtime, schema, prompts, or personas. It only transforms prose fields; task
IDs, agent names, timestamps, playbook IDs, outcomes and counter adjustments
remain unchanged. Canonical files stay named `<task-id>__<agent>.json`, as
required by the unmodified ACE runtime. Do not commit the short-lived raw
version of these files.

For ACE framework installation and the embedded runtime lifecycle, see the
project documentation in [ace/README_EMBEDDED.md](../../../ace/README_EMBEDDED.md)
(and the Italian version [ace/README_EMBEDDED_IT.md](../../../ace/README_EMBEDDED_IT.md)).

## First use on each machine (automatic)

Prerequisites: Node.js 18+, Python 3.10+, and network access to PyPI and GitHub
releases (the spaCy models are installed from their release wheels). Nothing else
has to be done by hand: the first `finalize-task.js <task-id>` run detects the
missing environment, installs it and then continues. Expect a few minutes on a
clean machine (measured about 3.5 minutes); later runs skip this step.

The bootstrap:

- creates a local, ignored `.venv` (on Windows via `py -3`, elsewhere `python3`;
  set `PYTHON` to use another interpreter);
- installs everything listed in [requirements.txt](requirements.txt): pinned
  Presidio/spaCy and the English/Italian small spaCy models;
- verifies that both models load, and only then writes the marker
  `.venv/.ace-privacy-ready`, which stores a hash of `requirements.txt`. Changing
  the requirements invalidates the marker and triggers a reinstall on the next run.

The bootstrap runs before any trace is read or modified, so a failed install
leaves the raw traces untouched and the task unfinalized.

Other options:

- `node scripts\ace-addons\privacy\finalize-task.js --ensure` prepares the
  environment without processing any task (useful to warm up a machine or CI).
- `node scripts\ace-addons\privacy\finalize-task.js --setup` forces a reinstall.
- `ACE_PRIVACY_NO_AUTOSETUP=1` disables the automatic install: if the
  environment is missing or outdated, finalization stops with an error that
  points to `--setup`.

## Per-task workflow

1. Capture each participating agent's trace as usual, with
   `node ace\scripts\capture_trace.js --manifest <manifest> --trace <input>`.
   The raw canonical trace exists briefly in `ace\traces\`.
2. Before any ACE consumer or Git staging, run:

   ```powershell
   node scripts\ace-addons\privacy\finalize-task.js <task-id>
   ```

3. The addon reads exactly the task's delegation manifests, runs Presidio on
   each trace, verifies the ACE document and unchanged structural evidence,
   replaces canonical files with sanitized versions, and invokes the
   unmodified ACE `finalize_task.js` (counters and threshold). Only after
   success may the normal reflector workflow or commit proceed.

If detection, validation or installation fails, finalization stops and the
trace(s) must not be committed. The raw file remains available locally to
correct and retry; remove it manually if no retry is intended. Do not use
`finalize_task.js` directly or rerun the addon after counters have already
marked a trace. Older tracked traces are not migrated by this addon.

## Configuration

- [policy.json](../../../config/ace-addons/privacy/policy.json) selects
  languages/models, detectable entities, score threshold (with a URL-specific
  override because Presidio scores URLs at 0.6) and prose paths.
  Presidio runs the configured languages on each text value, merges overlapping
  detections and replaces each selected span with `<ENTITY_TYPE>`. The language
  models and Presidio recognizers may still yield false positives or miss PII:
  review the output before committing.
- [deny-list.json](../../../config/ace-addons/privacy/deny-list.json) contains
  known technical tokens **excluded from replacement** (Presidio `allow_list`);
  expand it when a false positive is verified. It is not a list of terms to
  redact.

This is a pragmatic post-capture step, not a guarantee that sensitive data can
never appear on disk or in Git. Avoid including secrets in ACE inputs at all.
