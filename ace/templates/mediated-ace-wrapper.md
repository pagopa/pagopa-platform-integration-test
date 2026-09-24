## ACE mediated orchestrator wrapper

Expose this wrapper only at the configured `<standard-runtime-name>-ace`
entrypoint. Keep the standard entrypoint and shared canonical persona ACE-free.
Load that same persona here, preserving compatible platform metadata, tools,
model, normal delegates, and project guardrails. Expose the generated
reflector runtime `__ACE_REFLECTOR_RUNTIME_NAME__` as an additional delegate.

For each bounded delegation, assign a stable task id and run
`prepare_delegation.js --task-id <id> --agent <canonical-id> --platform
<configured-platform>`. The explicit `--platform` is mandatory even when only
one platform is enabled. Read its manifest and dedicated
`ace-global.instructions.md` plus the listed agent/family instruction files.
Invoke exactly the unchanged worker runtime named by the manifest, passing the
manifest lessons through the task-local mediated adapter and preserving the
canonical id.

Return the selected, seen, and cited lesson ids. Cited ids must be a subset of
seen ids, and seen ids must be a subset of the manifest's selected ids.
Collect and verify the result, then use `capture_trace.js` for every actual
contributor and `finalize_task.js` once. If the reflector threshold is reached,
invoke `__ACE_REFLECTOR_RUNTIME_NAME__`, which delegates to the generated
curator runtime `__ACE_CURATOR_RUNTIME_NAME__`; preserve the generated warden
runtime `__ACE_WARDEN_RUNTIME_NAME__`, deterministic gate, and explicit human
sign-off chain. Never write platform-global instructions,
modify workers, or bypass the capture/finalize helpers.
