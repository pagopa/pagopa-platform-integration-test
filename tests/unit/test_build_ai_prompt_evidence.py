"""Unit tests for response evidence, cross-source de-duplication and the prompt budget."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".github" / "scripts"))

from build_ai_prompt import (
    build_prompt,
    collect_response_evidence,
    drop_junit_duplicates,
    load_failures,
    parse_response_attachment,
)

ACTIVATE_KO = (
    "URL: https://api.uat.platform.pagopa.it/nodo/node-for-psp/v1\n"
    "Response:\n"
    '<?xml version="1.0" encoding="UTF-8" standalone="no" ?><Envelope><Body><activatePaymentNoticeV2Response>'
    "<outcome>KO</outcome><fault><faultCode>PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE</faultCode>"
    "<faultString>Errore di connessione verso la Stazione.</faultString><id>NodoDeiPagamentiSPC</id>"
    "<description/></fault></activatePaymentNoticeV2Response></Body></Envelope>"
)
ACTIVATE_OK = (
    "URL: https://api.uat.platform.pagopa.it/nodo/node-for-psp/v1\n"
    "HTTP status: 200\n"
    "Response:\n"
    "<Envelope><Body><activatePaymentNoticeV2Response><outcome>OK</outcome>"
    "<totalAmount>108.41</totalAmount><paymentToken>8e0eda2c4cc94eda</paymentToken>"
    "</activatePaymentNoticeV2Response></Body></Envelope>"
)
APIM_500 = (
    "URL: https://api.uat.platform.pagopa.it/nodo/node-for-psp/v1\n"
    "Response:\n"
    '{ "statusCode": 500, "message": "Internal server error", "activityId": "c42b75ea-98e8" }'
)


def _attachment(source: str, content: str, name: str = "Step: [pay] - Received response") -> dict:
    """Build an Allure attachment descriptor carrying its file content for the writer helper."""
    return {"name": name, "source": source, "type": "text/plain", "content": content}


def _write_allure_result(results_dir: Path, steps: list, name: str = "Pay a notice") -> None:
    """Write one failed Allure result with its attachment files next to it, like allure-behave does."""
    for step in steps:
        for attachment in step.get("attachments", []):
            (results_dir / attachment["source"]).write_text(attachment.pop("content"), encoding="utf-8")
        for nested in step.get("steps", []):
            for attachment in nested.get("attachments", []):
                (results_dir / attachment["source"]).write_text(attachment.pop("content"), encoding="utf-8")
    (results_dir / f"{name.replace(' ', '-')}-result.json").write_text(
        json.dumps(
            {
                "name": name,
                "fullName": f"Feature: {name}",
                "status": "failed",
                "statusDetails": {"message": "AssertionError: The field [paymentToken] does not exists.", "trace": "T"},
                "steps": steps,
            }
        ),
        encoding="utf-8",
    )


def test_parse_response_attachment_extracts_soap_ko_with_http_200() -> None:
    """A KO outcome with a fault is reported even though the SOAP call answered 200."""
    item = parse_response_attachment(ACTIVATE_KO)

    assert item["operation"] == "activatePaymentNoticeV2Response"
    assert item["endpoint"] == "node-for-psp/v1"
    assert item["http_status"] is None
    assert "outcome=KO" in item["detail"]
    assert "faultCode=PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE" in item["detail"]
    assert 'faultString="Errore di connessione verso la Stazione."' in item["detail"]
    assert "id=NodoDeiPagamentiSPC" in item["detail"]
    assert "description=" not in item["detail"]


def test_parse_response_attachment_ignores_healthy_responses() -> None:
    """OK SOAP outcomes, healthy JSON and 2xx HTML pages add no evidence."""
    assert parse_response_attachment(ACTIVATE_OK) is None
    assert parse_response_attachment('URL: https://h/closepayment\nHTTP status: 200\nResponse:\n{"outcome":"OK"}') is None
    assert parse_response_attachment('URL: https://h/events\nResponse:\n{"data":[{"status":"PAID"}],"count":1}') is None
    assert parse_response_attachment("URL: https://h/p\nHTTP status: 200\nResponse:\n<html><body>x</body></html>") is None
    assert parse_response_attachment("https://h/redirect?clientId=WISP_REDIRECT") is None
    assert parse_response_attachment("URL: https://h/x\nRequest:\n<a/>") is None


def test_parse_response_attachment_reports_non_xml_errors() -> None:
    """A non-XML body is evidence when it carries an error status, with or without the HTTP status line."""
    apim = parse_response_attachment(APIM_500)
    assert apim["http_status"] is None
    assert "activityId" in apim["detail"] and "500" in apim["detail"]

    with_status = parse_response_attachment("URL: https://h/v1\nHTTP status: 502\nResponse:\nBad Gateway")
    assert with_status["http_status"] == 502
    assert "Bad Gateway" in with_status["detail"]

    ko_json = parse_response_attachment(
        'URL: https://h/closepayment\nHTTP status: 200\nResponse:\n{"outcome":"KO","description":"no"}'
    )
    assert "KO" in ko_json["detail"]
    assert ko_json["endpoint"] == "closepayment"


def test_parse_response_attachment_handles_nodo_inviarpt_ko_and_soap_fault() -> None:
    """Italian nodoInviaRPT `esito` and SOAP 1.1 Fault envelopes are summarised too."""
    rpt = parse_response_attachment(
        "URL: https://h/nodo\nResponse:\n<Envelope><Body><nodoInviaRPTRisposta><esito>KO</esito>"
        "<fault><faultCode>PPT_SEMANTICA</faultCode><faultString>bad</faultString></fault>"
        "</nodoInviaRPTRisposta></Body></Envelope>"
    )
    assert rpt["operation"] == "nodoInviaRPTRisposta"
    assert "esito=KO" in rpt["detail"]
    assert "faultCode=PPT_SEMANTICA" in rpt["detail"]

    soap11 = parse_response_attachment(
        "URL: https://h/nodo\nHTTP status: 500\nResponse:\n"
        '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><s:Fault>'
        "<faultcode>s:Server</faultcode><faultstring>boom</faultstring></s:Fault></s:Body></s:Envelope>"
    )
    assert soap11["operation"] == "Fault"
    assert "faultCode=s:Server" in soap11["detail"]
    assert 'faultString="boom"' in soap11["detail"]


def test_collect_response_evidence_keeps_order_and_folds_repeats(tmp_path: Path) -> None:
    """Only error-bearing responses are kept and repeated identical ones are folded into a count."""
    steps = [
        {"name": "Given ok", "status": "passed"},
        {
            "name": "Then pay",
            "status": "failed",
            "attachments": [
                _attachment("a1.txt", ACTIVATE_OK),
                _attachment("a2.txt", ACTIVATE_KO),
                _attachment("a3.txt", ACTIVATE_KO),
                _attachment("a4.txt", APIM_500),
                _attachment("a5.txt", "ignored request", name="Step: [pay] - Sent request"),
            ],
            "steps": [{"name": "nested", "attachments": [_attachment("a6.txt", ACTIVATE_OK)]}],
        },
    ]
    _write_allure_result(tmp_path, steps)

    result = json.loads((tmp_path / "Pay-a-notice-result.json").read_text(encoding="utf-8"))
    evidence = collect_response_evidence(result, tmp_path)

    assert [item["operation"] for item in evidence] == ["activatePaymentNoticeV2Response", ""]
    assert evidence[0]["count"] == 2
    assert evidence[0]["step"] == "Then pay"


def test_collect_response_evidence_ignores_missing_files_and_path_traversal(tmp_path: Path) -> None:
    """A dangling or traversing attachment source never raises and never escapes the results dir."""
    results_dir = tmp_path / "allure-results"
    results_dir.mkdir()
    (tmp_path / "outside.txt").write_text(ACTIVATE_KO, encoding="utf-8")
    result = {
        "steps": [
            {
                "name": "s",
                "attachments": [
                    {"name": "x - Received response", "source": "missing.txt"},
                    {"name": "x - Received response", "source": "../outside.txt"},
                ],
            }
        ]
    }

    assert collect_response_evidence(result, results_dir) == []


def test_evidence_is_rendered_only_when_collected(tmp_path: Path) -> None:
    """Evidence appears in the prompt for opted-in loads and never otherwise."""
    steps = [{"name": "Then pay", "attachments": [_attachment("a.txt", ACTIVATE_KO), _attachment("b.txt", APIM_500)]}]
    _write_allure_result(tmp_path, steps)

    plain = build_prompt(load_failures(tmp_path), "WISP", 20, 1500)
    enriched = build_prompt(load_failures(tmp_path, collect_evidence=True), "WISP", 20, 1500)

    assert "evidence" not in plain
    assert "PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE" not in plain
    assert "- **evidence**" in enriched
    assert "outcome=KO · faultCode=PPT_STAZIONE_INT_PA_IRRAGGIUNGIBILE" in enriched
    assert "activityId" in enriched
    assert "strongest hint of the real root cause" in enriched


def test_evidence_respects_item_and_total_caps() -> None:
    """The evidence of the whole prompt stays inside its own budget, shared across failures."""
    evidence = [
        {"endpoint": "v1", "operation": f"Op{i}", "http_status": 200, "detail": "x" * 500, "step": "s", "count": 1}
        for i in range(5)
    ]
    failures = [
        {"name": f"T{n}", "fullName": f"F{n}", "status": "failed", "message": "m", "trace": "t", "evidence": evidence}
        for n in range(4)
    ]

    prompt = build_prompt(
        failures, "WISP", 20, 1500,
        max_evidence_items=3, max_evidence_chars=100, max_evidence_total_chars=600,
    )

    evidence_lines = [line for line in prompt.splitlines() if line.startswith("  - ")]
    assert evidence_lines
    assert all(len(line) <= 150 for line in evidence_lines)
    assert sum(len(line) for line in evidence_lines) <= 600


def test_drop_junit_duplicates_matches_allure_despite_prefix_and_fullname_differences() -> None:
    """The same scenario reported by Allure and JUnit is kept once, Allure (with evidence) winning."""
    allure = [
        {"name": "Pay", "fullName": "Feature: Pay", "status": "broken", "trace": "A",
         "message": "xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 0"},
        {"name": "Check", "fullName": "Feature: Check", "status": "failed", "trace": "A",
         "message": "AssertionError: There are not events with business process receipt-ok."},
    ]
    junit = [
        {"name": "Pay", "fullName": "features.x.Pay", "status": "broken", "trace": "J",
         "message": "not well-formed (invalid token): line 1, column 0"},
        {"name": "Check", "fullName": "features.x.Check", "status": "failed", "trace": "J",
         "message": "There are not events with business process receipt-ok."},
        {"name": "Other", "fullName": "features.x.Other", "status": "failed", "message": "boom", "trace": "J"},
    ]

    remaining = drop_junit_duplicates(allure, junit)

    assert [failure["name"] for failure in remaining] == ["Other"]


def test_drop_junit_duplicates_is_one_to_one_for_same_name_scenarios() -> None:
    """Two distinct scenarios sharing name and message are not collapsed into one."""
    base = {"name": "Postepay", "status": "failed", "message": "Timeout on locator", "trace": ""}
    allure = [dict(base, fullName="Checkout: Postepay")]
    junit = [dict(base, fullName="features.a.Postepay"), dict(base, fullName="features.b.Postepay")]

    assert len(drop_junit_duplicates(allure, junit)) == 1


def _long_failures(count: int, trace_len: int = 1500) -> list:
    """Build `count` distinct failures with long traces."""
    return [
        {"name": f"Scenario {n}", "fullName": f"F: Scenario {n}", "status": "failed",
         "message": f"Boom {n}", "trace": "frame\n" * (trace_len // 6)}
        for n in range(count)
    ]


def test_budget_disabled_keeps_full_detail() -> None:
    """Without a budget the prompt is rendered at full detail."""
    prompt = build_prompt(_long_failures(3), "WISP", 20, 1500)

    assert "shortened to fit" not in prompt
    assert prompt.count("frame") >= 3 * 200


def test_budget_shortens_traces_before_dropping_failures() -> None:
    """A tight budget shortens traces and keeps every failure when that is enough."""
    failures = _long_failures(10)
    budget = len(build_prompt(failures, "WISP", 20, 1500)) // 2

    prompt = build_prompt(failures, "WISP", 20, 1500, max_prompt_chars=budget)

    assert len(prompt) <= budget
    assert "shortened to fit the token budget" in prompt
    assert "# 10. Scenario 9" in prompt
    assert "more failures omitted" not in prompt


def test_budget_drops_trailing_failures_as_last_resort() -> None:
    """When even the leanest level does not fit, trailing failures are omitted with a note."""
    prompt = build_prompt(_long_failures(20), "WISP", 20, 1500, max_prompt_chars=2500)

    assert len(prompt) <= 2500
    assert "# 1. Scenario 0" in prompt
    assert "# 20. Scenario 19" not in prompt
    assert "more failures omitted" in prompt
    assert "**Total failures: 20**" in prompt


def test_budget_always_keeps_one_failure() -> None:
    """Even an impossible budget never produces an empty analysis request."""
    prompt = build_prompt(_long_failures(3), "WISP", 20, 1500, max_prompt_chars=10)

    assert "# 1. Scenario 0" in prompt


def _traceback(frames: int = 30) -> str:
    """Build a behave-like traceback: boilerplate frames first, the culprit and the assertion last."""
    boilerplate = "".join(
        f'  File "/opt/site-packages/behave/model.py", line {n}, in run\n    match.run(runner.context)\n'
        for n in range(frames)
    )
    culprit = (
        '  File "src/integration/wisp/utility/utils.py", line 33, in execute_request\n'
        "    object_response = xmlutils.fromstring(formatted_response)\n"
        "xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 1, column 0"
    )
    return boilerplate + culprit


def _single_failure(trace: str) -> list:
    """Wrap a traceback into one failure entry."""
    return [{"name": "S", "fullName": "F: S", "status": "broken", "message": "m", "trace": trace}]


def test_long_trace_keeps_its_final_frames_and_marks_the_cut() -> None:
    """The cut is taken from the head: the culprit frame and the exception stay, a marker says so."""
    trace = _traceback()
    assert len(trace) > 1500

    prompt = build_prompt(_single_failure(trace), "WISP", 20, 1500)

    assert "execute_request" in prompt
    assert "xml.etree.ElementTree.ParseError: not well-formed" in prompt
    assert "[... earlier frames omitted ...]" in prompt
    assert prompt.count("match.run(runner.context)") < 30


def test_trace_is_cut_on_a_line_boundary() -> None:
    """The line the cut lands in is dropped, so no half frame is shown."""
    trace = "\n".join(f"frame-number-{n:03d} " + "x" * 20 for n in range(100))

    prompt = build_prompt(_single_failure(trace), "WISP", 20, 200)

    shown = [line for line in prompt.splitlines() if line.startswith("frame-number-")]
    assert shown
    assert all(line.endswith("x" * 20) for line in shown)
    assert shown[-1].startswith("frame-number-099")


def test_short_trace_is_untouched_and_zero_limit_drops_it() -> None:
    """A trace within the cap has no marker; a zero cap leaves no trace text at all."""
    short = build_prompt(_single_failure("one\ntwo"), "WISP", 20, 1500)
    assert "one\ntwo" in short
    assert "earlier frames omitted" not in short

    none = build_prompt(_single_failure(_traceback()), "WISP", 20, 0)
    assert "execute_request" not in none
    assert "earlier frames omitted" not in none


def test_tight_budget_still_shows_the_assertion() -> None:
    """Even the narrow budget levels keep the exception line, which is what the analysis needs most."""
    full = build_prompt(_single_failure(_traceback()), "WISP", 20, 1500)

    prompt = build_prompt(_single_failure(_traceback()), "WISP", 20, 1500, max_prompt_chars=len(full) - 600)

    assert len(prompt) <= len(full) - 600
    assert "xml.etree.ElementTree.ParseError: not well-formed" in prompt
