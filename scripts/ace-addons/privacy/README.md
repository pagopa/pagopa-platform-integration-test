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

## First use on each machine

From the repository root, install Node.js 18+ and Python 3.10+, then run:

```powershell
node scripts\ace-addons\privacy\finalize-task.js --setup
```

On Windows the bootstrap uses `py -3`; set `PYTHON` to a Python executable if
that launcher is not available. On other systems it uses `python3`. The setup
creates a local, ignored `.venv` and installs pinned Presidio/spaCy packages and
the English/Italian small spaCy models. Requires access to PyPI and the spaCy
model distribution; no Docker or global Python packages are needed. Re-run
setup after changing requirements or models.

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
