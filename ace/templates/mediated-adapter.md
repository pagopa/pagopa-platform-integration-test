## ACE mediated task-local adapter

This block is task-local context supplied by the opt-in ACE orchestrator. It
must not be installed in the worker's persona, wrapper, or global platform
instructions.

- Apply only lessons present in the supplied delegation manifest.
- Preserve each lesson's stable `P-NNN` id and cite every lesson actually used.
- Return result, checks, lesson ids seen and cited, notes, and deliberately
  assessed friction to the ACE orchestrator.
- Do not write ACE traces, state, proposals, decisions, or playbooks. The
  orchestrator owns the lifecycle.
