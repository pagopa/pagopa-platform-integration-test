"""Generate a local mock AI-analysis page for visual preview.

Usage:
    python .github/scripts/preview_analysis.py

Opens the rendered HTML in the default browser. Override output path with
the PREVIEW_OUTPUT env var (default: tmp_fetched/analysis_preview.html).
"""

from __future__ import annotations

import json
import os
import webbrowser
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

_MOCK_ANALYSIS = """\
# 1. Utente paga un pagamento singolo con marca da bollo già esistente in GPD
- **status**: failed
- **fullName**: `nodoInviaRPT: Utente paga un pagamento singolo con versamento e marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
File "src/integration/wisp/steps/steps.py", line 185, in user_redirected_to_checkout
    steputils.check_wisp_session_timers_del_and_rts_were_sent(context)
  File "src/integration/wisp/utility/steps_utils.py", line 898, in check_wisp_session_...
    check_event(context, 'receipt-ok', 'status', 'RT_SEND_SUCCESS')
AssertionError: There are not events with business process receipt-ok.
```

### Root cause
The `receipt-ok` event is never produced, suggesting the RT (Ricevuta Telematica) send step is
silently failing downstream — likely a timeout or an unreachable endpoint during the UAT run.

### Category
environment

### Recommended action
Check the RT-send service logs for the relevant session ID and verify that the UAT endpoint
is reachable and responding within the configured timeout window.

---

# 2. L'utente paga un carrello multibeneficiario già esistente in GPD
- **status**: failed
- **fullName**: `nodoInviaCarrelloRPT: L'utente paga un carrello multibeneficiario già esistente in GPD`
- **message**: AssertionError: The status code is not 200. Current value: 302.
- **trace**:
```
File "src/integration/wisp/steps/steps.py", line 235, in nm1_to_nmu_fails
    steputils.check_fail_nm1_to_nmu_conversion(context)
  File "src/integration/wisp/utility/steps_utils.py", line 944, in check_fail_nm1_to_nmu...
    check_status_code(context, 'user', '200')
AssertionError: The status code is not 200. Current value: 302.
```

### Root cause
The endpoint returns an HTTP 302 redirect instead of 200. The NM1→NMU conversion
is likely routing the request to a different host/path in the UAT environment.

### Category
environment

### Recommended action
Inspect the Location header of the 302 response to determine where the redirect points.
Update the base URL configuration for this flow if the UAT routing has changed.

---

# 3. Utente paga pagamento singolo senza marca da bollo
- **status**: failed
- **fullName**: `nodoInviaRPT: Utente paga un pagamento singolo senza marca da bollo`
- **message**: AssertionError: There are not events with business process receipt-ok.
- **trace**:
```
AssertionError: There are not events with business process receipt-ok.
```

### Root cause
Same as failure #1 — the `receipt-ok` event is missing. The root cause appears to be
independent of the stamp flag, pointing to a systemic RT-send problem.

### Category
environment

### Recommended action
Same as failure #1; treat #1 and #3 as a single incident.

---

## Common patterns
Two out of three failures share the exact same assertion (`receipt-ok` event missing),
indicating a **systemic RT-send issue** in the UAT environment rather than isolated test
defects. The multibeneficiary 302 is a separate routing misconfiguration. Priority fix:
restore RT-send connectivity in UAT, then re-run the full suite.
"""


def main() -> None:
    """Render the mock analysis markdown to a local HTML file and open it."""
    output = Path(os.environ.get("PREVIEW_OUTPUT", "tmp_fetched/analysis_preview.html"))
    output.parent.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(".github/templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("analysis-template.html")
    rendered = template.render(
        suite_label="WISP",
        timestamp="2026-07-08_12:00:00",
        model="openai/gpt-4.1",
        analysis_markdown_json=json.dumps(_MOCK_ANALYSIS),
    )

    output.write_text(rendered, encoding="utf-8")
    print(f"[preview_analysis] written → {output.resolve()}")
    webbrowser.open(output.resolve().as_uri())


if __name__ == "__main__":
    main()
