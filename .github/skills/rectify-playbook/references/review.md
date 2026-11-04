# Independent playbook correction review

You are not the correction author. Review only: do not edit the request,
playbook, instructions, contracts or audit, and do not apply the correction.
Use actual source reads and read-only checks, not the author's assurances.

## Required checks

- **scope**: Match the candidate to the original submitted request. Verify the
  actual external origin and separate correction-only task before reviewing
  its substance. Reject ordinary-cycle work, lifecycle-created handoffs,
  gate/evidence/approval bypasses, or unclear origin even when all hashes pass.
  An author's label of "external" is not proof; inspect the initiating request.
  Verify the
  explicit playbook, every P-XXX ID, current before content, minimal scope and
  preservation of untargeted behavior. A useful change outside those targets is
  still outside authorization.
- **contracts**: Read the authoritative project/agent/persona instructions and
  relevant schemas. Check every normative clause in the replacement against
  them. Missing facts stay unknown; preserve source attribution, nullability,
  exceptions, required verification and output shape. Do not make a defective
  lesson appear valid by weakening its governing contract.
- **conflicts**: Read the full target playbook and relevant active global/family
  lessons. Look for contradictions, duplicated directives, changed precedence,
  scope leakage, impossible combinations and model-dependent workarounds that
  conceal a generally invalid rule.
- **evidence**: Distinguish observed outputs, inspected external artifacts,
  reproducible counterexamples and unverified claims. A prior approval or a
  claimed successful test is not proof. Explain the causal defect and how the
  proposed text removes it. If necessary evidence cannot be inspected or
  reproduced, return `inconclusive`, not approval. Never invent missing traces.
- **regressions**: Derive adversarial cases from the defect and unaffected cases
  from the original contract. Check positive, negative, missing/null and
  conflicting-input cases where relevant. Define exact expected fields or
  measurable invariants, not merely plausible prose. Inspect existing test
  results where available and clearly distinguish actual execution from static
  reasoning. When the claim concerns model behavior, require actual suitable
  evaluation evidence; do not claim a static review establishes model reliability.
  Include preserved historical counters and any retrieval exclusions in the
  assessment. The correction must not rely on secretly resetting those fields.

Independently rerun the installed `rectify_playbook.js --request <file> --check`
when a compatible read-only shell is available; otherwise inspect the request
and sources and explicitly disclose the shell limitation. Never claim to have
run a command without its real output. Any source or candidate change invalidates
the prior review. Approve only when all five checks have a grounded result and
no unresolved finding remains.

## Return contract

Return one JSON object, not an edited request:

```json
{
  "rectification_id": "<exact check output>",
  "request_sha256": "<exact check output>",
  "review_state_sha256": "<exact check output>",
  "reviewer": "<actual independent harness agent/session identifier>",
  "independent": true,
  "verdict": "approve",
  "checks": {
    "scope": "Actual initiating external request, separate task, explicit targets and result.",
    "contracts": "Governing invariants and clause-by-clause result.",
    "conflicts": "Relevant lessons inspected and result.",
    "evidence": "Actual evidence, causal reasoning, and limitations.",
    "regressions": "Concrete cases, exact expected outcomes, actual checks and limitations."
  },
  "findings": []
}
```

Use `reject` or `inconclusive` instead of `approve` when appropriate and put
concrete blockers in `findings`. Never fill an unchecked section with a generic
"passed". Approval covers only this request and reviewed state. The applying
agent may transcribe your actual result but may not turn rejection, silence or
an incomplete response into approval.
