"""Build a compact AI-analysis prompt from Allure or JUnit raw results.

Reads all `*-result.json` files under an Allure results directory, keeps only
failed / broken test cases, and optionally reads failures from JUnit XML files.
The generated Markdown prompt asks the model to categorize each failure and
suggest an action.

Optionally (`AI_PROMPT_SOAP_EVIDENCE=true`) each failure also carries the error
details found *inside* the HTTP responses captured by the scenario: a SOAP
`outcome=KO` + `faultCode` returned with HTTP 200 does not fail the step that
received it, so the scenario usually breaks later with an unrelated message.

The prompt is kept inside a character budget (`MAX_PROMPT_CHARS`) by shortening
traces and evidence first and dropping trailing failures only as a last resort.

Environment variables:
    ALLURE_RESULTS_DIR        Directory containing Allure raw results (default: allure-results).
    JUNIT_RESULTS_DIR         Optional directory containing JUnit XML result files.
    PROMPT_OUTPUT             Destination path for the generated prompt (default: ai-analysis-input/prompt.txt).
    SUITE_LABEL               Human-readable suite name used in the prompt header (default: WISP).
    MAX_FAILURES              Cap on number of failures included (default: 20).
    MAX_TRACE_CHARS           Cap on trace length per failure (default: 1500).
    MAX_PROMPT_CHARS          Soft cap on the whole prompt length, 0 disables it (default: 16000).
    AI_PROMPT_SOAP_EVIDENCE   "true" to add response evidence to every failure (default: false).
    MAX_EVIDENCE_ITEMS        Cap on evidence items per failure (default: 3).
    MAX_EVIDENCE_CHARS        Cap on the length of one evidence item (default: 400).
    MAX_EVIDENCE_TOTAL_CHARS  Cap on the evidence of the whole prompt (default: 4000).
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple
from urllib.parse import urlparse
from xml.etree import ElementTree

# Attachment text written by the suites' `execute_request` helper; the status line is optional
# because reports generated before it was introduced do not have it.
_ATTACHMENT_RE = re.compile(
    r"^URL:\s*(?P<url>\S+)[ \t]*\r?\n"
    r"(?:HTTP status:\s*(?P<status>\d{3})[ \t]*\r?\n)?"
    r"Response:\s*\r?\n(?P<body>.*)\Z",
    re.DOTALL,
)
_RESPONSE_ATTACHMENT_SUFFIX = "Received response"
_MAX_ATTACHMENT_CHARS = 200_000
_OUTCOME_TAGS = ("outcome", "esito", "esitocomplessivooperazione")
_EXCEPTION_PREFIX_RE = re.compile(r"^[\w.]*(?:Error|Exception):\s*")
_VERSION_SEGMENT_RE = re.compile(r"v\d+")
_MAX_FAULTS_PER_RESPONSE = 3
_STEP_NAME_CHARS = 50


def _clean(value: Any) -> str:
    """Return a stripped string, tolerating None and non-string inputs."""
    if value is None:
        return ""
    return str(value).strip()


def _shorten(text: str, limit: int) -> str:
    """Collapse whitespace and cut `text` to `limit` characters, marking the cut with an ellipsis."""
    flat = " ".join(text.split())
    if limit <= 0:
        return ""
    if len(flat) <= limit:
        return flat
    return flat[: max(limit - 1, 0)].rstrip() + "…"


def _local_name(tag: Any) -> str:
    """Return an XML tag without its `{namespace}` prefix; non-string tags (comments) give ''."""
    if not isinstance(tag, str):
        return ""
    return tag.rsplit("}", 1)[-1]


def _iter_step_attachments(steps: Any) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """Yield `(step name, attachment)` pairs of an Allure result in execution order, nested steps included."""
    for step in steps or []:
        if not isinstance(step, dict):
            continue
        name = _clean(step.get("name"))
        for attachment in step.get("attachments") or []:
            if isinstance(attachment, dict):
                yield name, attachment
        yield from _iter_step_attachments(step.get("steps"))


def _read_attachment(path: Path) -> Optional[str]:
    """Read a bounded amount of an attachment file, returning None when it cannot be read."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(_MAX_ATTACHMENT_CHARS)
    except OSError:
        return None


def _parse_xml(body: str) -> Optional[ElementTree.Element]:
    """Parse `body` as XML, returning None when it is not well-formed XML."""
    if not body.lstrip().startswith("<"):
        return None
    try:
        return ElementTree.fromstring(body.strip())
    except ElementTree.ParseError:
        return None


def _summarise_xml(root: ElementTree.Element, endpoint: str, status_code: Optional[int]) -> Optional[Dict[str, Any]]:
    """Summarise a SOAP response when it reports a non-OK outcome or carries a fault, else return None."""
    response_root = root
    for element in root.iter():
        if _local_name(element.tag).lower() == "body":
            response_root = next(iter(element), element)
            break

    outcomes: List[str] = []
    faults: List[str] = []
    for element in response_root.iter():
        name = _local_name(element.tag)
        if name.lower() in _OUTCOME_TAGS and _clean(element.text):
            outcomes.append(f"{name}={_clean(element.text)}")
        elif name.lower() == "fault":
            fields = {_local_name(child.tag).lower(): _clean(child.text) for child in element}
            parts = []
            for key, label in (("faultcode", "faultCode"), ("faultstring", "faultString"),
                               ("description", "description"), ("id", "id")):
                if fields.get(key):
                    value = fields[key]
                    parts.append(f"{label}={value}" if key in ("faultcode", "id") else f'{label}="{value}"')
            if parts:
                faults.append(" · ".join(parts))

    outcome_is_ko = any(item.split("=", 1)[1].upper() != "OK" for item in outcomes)
    if not faults and not outcome_is_ko:
        return None

    detail = " · ".join(outcomes + faults[:_MAX_FAULTS_PER_RESPONSE])
    return {
        "endpoint": endpoint,
        "operation": _local_name(response_root.tag),
        "http_status": status_code,
        "detail": detail,
    }


def _summarise_text(body: str, endpoint: str, status_code: Optional[int]) -> Optional[Dict[str, Any]]:
    """Summarise a non-XML response (JSON, HTML, plain text) when it signals an error, else return None."""
    try:
        parsed_json = json.loads(body)
    except ValueError:
        parsed_json = None

    if isinstance(parsed_json, dict):
        embedded = parsed_json.get("statusCode", parsed_json.get("status"))
        embedded_status = embedded if isinstance(embedded, int) and not isinstance(embedded, bool) else None
        effective_status = status_code if status_code is not None else embedded_status
        outcome = parsed_json.get("outcome")
        failing_outcome = isinstance(outcome, str) and outcome.upper() != "OK"
        if not failing_outcome and not (effective_status is not None and effective_status >= 400):
            return None
        detail = "non-XML JSON body: " + json.dumps(parsed_json, ensure_ascii=False, separators=(",", ":"))
    elif isinstance(parsed_json, list):
        if status_code is None or status_code < 400:
            return None
        detail = "non-XML JSON body: " + json.dumps(parsed_json, ensure_ascii=False, separators=(",", ":"))
    else:
        looks_like_html = body.lstrip().lower().startswith(("<!doctype html", "<html"))
        if status_code is not None and status_code < 400:
            return None
        if status_code is None and looks_like_html:
            return None
        detail = "non-XML body: " + body

    return {"endpoint": endpoint, "operation": "", "http_status": status_code, "detail": detail}


def parse_response_attachment(text: str) -> Optional[Dict[str, Any]]:
    """Summarise a captured HTTP response attachment when it carries failure information.

    Returns None for responses that look healthy (SOAP `outcome=OK`, JSON without an error status
    or outcome, HTML pages with a 2xx status) and for attachments that are not request/response
    dumps, so only the diagnostic responses reach the prompt.
    """
    match = _ATTACHMENT_RE.match(text.strip())
    if match is None:
        return None
    url = match.group("url")
    status_code = int(match.group("status")) if match.group("status") else None
    body = match.group("body").strip()
    if not body:
        return None

    parsed_url = urlparse(url)
    segments = [segment for segment in parsed_url.path.split("/") if segment]
    if len(segments) > 1 and _VERSION_SEGMENT_RE.fullmatch(segments[-1]):
        endpoint = "/".join(segments[-2:])  # `.../node-for-psp/v1`: the bare version says nothing
    else:
        endpoint = segments[-1] if segments else parsed_url.netloc

    root = _parse_xml(body)
    if root is not None:
        return _summarise_xml(root, endpoint, status_code)
    return _summarise_text(body, endpoint, status_code)


def collect_response_evidence(result: Dict[str, Any], results_dir: Path) -> List[Dict[str, Any]]:
    """Collect the distinct error-bearing HTTP responses attached to the steps of an Allure result.

    Items keep execution order and repeated identical responses are folded into a `count`.
    """
    evidence: List[Dict[str, Any]] = []
    index_by_key: Dict[Tuple[str, str, str], int] = {}
    for step_name, attachment in _iter_step_attachments(result.get("steps")):
        source = _clean(attachment.get("source"))
        if not source or not _clean(attachment.get("name")).endswith(_RESPONSE_ATTACHMENT_SUFFIX):
            continue
        text = _read_attachment(results_dir / Path(source).name)
        item = parse_response_attachment(text) if text else None
        if item is None:
            continue
        key = (item["endpoint"], str(item["http_status"]), item["detail"])
        if key in index_by_key:
            evidence[index_by_key[key]]["count"] += 1
            continue
        item["step"] = step_name
        item["count"] = 1
        index_by_key[key] = len(evidence)
        evidence.append(item)
    return evidence


def load_failures(allure_results_dir: Path, collect_evidence: bool = False) -> List[Dict[str, Any]]:
    """Extract failed/broken test cases from the Allure raw JSON results.

    With `collect_evidence` each failure also gets an `evidence` list built from its step attachments.
    """
    failures: List[Dict[str, Any]] = []
    if not allure_results_dir.is_dir():
        print(f"[build_ai_prompt] allure results dir '{allure_results_dir}' not found")
        return failures

    for path in sorted(allure_results_dir.glob("*-result.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:  # noqa: BLE001 - skip malformed test-case files
            print(f"[build_ai_prompt] skipping '{path}': {exc}")
            continue

        status = data.get("status")
        if status not in ("failed", "broken"):
            continue

        details = data.get("statusDetails") or {}
        failure: Dict[str, Any] = {
            "name": _clean(data.get("name")) or "unknown",
            "fullName": _clean(data.get("fullName")),
            "status": _clean(status),
            "message": _clean(details.get("message")),
            "trace": _clean(details.get("trace")),
        }
        if collect_evidence:
            failure["evidence"] = collect_response_evidence(data, allure_results_dir)
        failures.append(failure)
    return failures


def load_junit_failures(junit_results_dir: Path) -> List[Dict[str, Any]]:
    """Extract failed and errored test cases from JUnit XML result files."""
    failures: List[Dict[str, Any]] = []
    if not junit_results_dir.is_dir():
        print(f"[build_ai_prompt] JUnit results dir '{junit_results_dir}' not found")
        return failures

    for path in sorted(junit_results_dir.glob("*.xml")):
        try:
            root = ElementTree.parse(path).getroot()
        except (ElementTree.ParseError, OSError) as exc:
            print(f"[build_ai_prompt] skipping '{path}': {exc}")
            continue

        for test_case in root.iter("testcase"):
            problem = test_case.find("failure")
            status = "failed"
            if problem is None:
                problem = test_case.find("error")
                status = "broken"
            if problem is None:
                continue

            name = _clean(test_case.get("name")) or "unknown"
            class_name = _clean(test_case.get("classname"))
            failures.append(
                {
                    "name": name,
                    "fullName": f"{class_name}.{name}" if class_name else name,
                    "status": status,
                    "message": _clean(problem.get("message")),
                    "trace": _clean(problem.text),
                }
            )

    return failures


def _cross_source_key(failure: Dict[str, Any]) -> Tuple[str, str]:
    """Return the identity used to match one failure reported by both Allure and JUnit.

    The two formats disagree on `fullName` and on the exception-class prefix of the message
    (`AssertionError: x` vs `x`), so only the scenario name and the normalised message are compared.
    """
    message = _EXCEPTION_PREFIX_RE.sub("", " ".join(_clean(failure.get("message")).split()))
    return _clean(failure.get("name")), message[:200]


def drop_junit_duplicates(
    allure_failures: List[Dict[str, Any]], junit_failures: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Return the JUnit failures that Allure did not already report.

    Matching is one-to-one, so two distinct scenarios sharing name and message stay two entries.
    """
    unmatched = Counter(_cross_source_key(failure) for failure in allure_failures)
    remaining: List[Dict[str, Any]] = []
    for failure in junit_failures:
        key = _cross_source_key(failure)
        if unmatched[key] > 0:
            unmatched[key] -= 1
            continue
        remaining.append(failure)
    return remaining


def _format_evidence(items: List[Dict[str, Any]], max_items: int, max_item_chars: int, budget_chars: int) -> List[str]:
    """Render the first `max_items` evidence items as bullet lines, trimmed to `budget_chars` overall."""
    lines: List[str] = []
    used = 0
    for item in items[:max_items]:
        label = item["operation"] or item["endpoint"]
        where = f" @ {item['endpoint']}" if item["operation"] and item["endpoint"] else ""
        http = f"HTTP {item['http_status']}" if item["http_status"] is not None else "HTTP n/a"
        repeated = f" (x{item['count']})" if item.get("count", 1) > 1 else ""
        step = _shorten(item.get("step", ""), _STEP_NAME_CHARS)
        prefix = f'  - step "{step}" · {label}{where} · {http} · ' if step else f"  - {label}{where} · {http} · "
        line = prefix + _shorten(item["detail"], max_item_chars) + repeated
        remaining = budget_chars - used
        if remaining <= len(prefix):
            break
        line = line if len(line) <= remaining else _shorten(line, remaining)
        lines.append(line)
        used += len(line)
    return lines


def _render_prompt(
    failures: List[Dict[str, Any]],
    suite_label: str,
    total_failures: int,
    trace_chars: int,
    evidence_items: int,
    evidence_chars: int,
    evidence_total_chars: int,
    reduced: bool,
) -> str:
    """Render the Markdown prompt for `failures` (already capped) using the given detail level."""
    with_evidence = [failure for failure in failures if failure.get("evidence")]
    per_failure_budget = evidence_total_chars // len(with_evidence) if with_evidence and evidence_items > 0 else 0

    header = (
        f"You are a senior QA engineer. Analyse the failures from the '{suite_label}' integration test suite.\n"
        "For each failure, produce a Markdown block with EXACTLY this structure (preserve heading levels):\n\n"
        "# <number>. <failure name — copy it verbatim from the input>\n"
        "- **status**: <value>\n"
        "- **fullName**: `<value>`\n"
        "- **message**: <value>\n"
        "- **trace**:\n"
        "```\n"
        "<trace — copy verbatim, truncate to 5 lines if longer>\n"
        "```\n"
        "### Root cause\n"
        "<1-2 lines>\n\n"
        "### Category\n"
        "<one of: application bug | test data | environment | flaky>\n\n"
        "### Recommended action\n"
        "<1-2 lines>\n\n"
        "---\n\n"
        "After all failures, add a ## Common patterns section if recurring root causes emerge.\n\n"
    )
    if per_failure_budget > 0:
        header += (
            "Some failures list **evidence**: error details returned INSIDE the HTTP responses captured by the "
            "scenario (e.g. a SOAP `outcome=KO` with a `faultCode` returned with HTTP 200, which the test does not "
            "fail on at that step, or a non-XML HTTP 500 body). The scenario usually fails later with an unrelated "
            "message, so treat the evidence as the strongest hint of the real root cause: cite the faultCode / HTTP "
            "status in the Root cause instead of blaming the final assertion. Do not copy the evidence into your "
            "answer.\n\n"
        )
    header += f"**Total failures: {total_failures}**\n\n--- FAILURES ---\n\n"

    parts: List[str] = [header]
    for idx, failure in enumerate(failures, start=1):
        trace = failure["trace"][:trace_chars]
        block = (
            f"# {idx}. {failure['name']}\n"
            f"- **status**: {failure['status']}\n"
            f"- **fullName**: `{failure['fullName']}`\n"
            f"- **message**: {failure['message']}\n"
            f"- **trace**:\n```\n{trace}\n```\n"
        )
        lines = (
            _format_evidence(failure.get("evidence") or [], evidence_items, evidence_chars, per_failure_budget)
            if per_failure_budget > 0
            else []
        )
        if lines:
            block += "- **evidence** (error details returned inside HTTP responses):\n" + "\n".join(lines) + "\n"
        parts.append(block)

    omitted = total_failures - len(failures)
    if omitted > 0:
        parts.append(f"\n_... {omitted} more failures omitted._\n")
    if reduced:
        parts.append("\n_Note: details were shortened to fit the token budget._\n")

    return "\n".join(parts)


def build_prompt(
    failures: List[Dict[str, Any]],
    suite_label: str,
    max_failures: int,
    max_trace_chars: int,
    *,
    max_prompt_chars: int = 0,
    max_evidence_items: int = 3,
    max_evidence_chars: int = 400,
    max_evidence_total_chars: int = 4000,
) -> str:
    """Render the Markdown prompt sent to the AI model.

    With `max_prompt_chars > 0` the prompt is reduced until it fits: first traces and evidence are
    shortened level by level, then trailing failures are dropped (always keeping at least one).
    Evidence is only rendered for failures that carry an `evidence` list.
    """
    unique_failures: List[Dict[str, Any]] = []
    seen_failures = set()
    for failure in failures:
        identity = (
            failure.get("fullName", "").strip() or failure["name"].strip(),
            failure["status"].strip().lower(),
            failure["message"].strip(),
        )
        if identity in seen_failures:
            continue
        seen_failures.add(identity)
        unique_failures.append(failure)
    failures = unique_failures

    if not failures:
        return (
            f"No test failures found in the '{suite_label}' suite. "
            "Confirm that the execution was complete and that no tests were unintentionally skipped. "
            "Reply in English, in a single sentence."
        )

    shown = failures[:max_failures]
    levels = [
        (max_trace_chars, max_evidence_items, max_evidence_chars),
        (min(max_trace_chars, 800), max_evidence_items, max_evidence_chars),
        (min(max_trace_chars, 400), min(max_evidence_items, 2), min(max_evidence_chars, 300)),
        (min(max_trace_chars, 200), min(max_evidence_items, 1), min(max_evidence_chars, 300)),
        (0, min(max_evidence_items, 1), min(max_evidence_chars, 200)),
        (0, 0, 0),
    ]

    def render(count: int, level: Tuple[int, int, int], reduced: bool) -> str:
        """Render the first `count` failures at the given `(trace, items, item chars)` level."""
        return _render_prompt(
            shown[:count], suite_label, len(failures), level[0], level[1], level[2],
            max_evidence_total_chars, reduced,
        )

    prompt = render(len(shown), levels[0], False)
    if max_prompt_chars <= 0 or len(prompt) <= max_prompt_chars:
        return prompt

    for level in levels[1:]:
        prompt = render(len(shown), level, True)
        if len(prompt) <= max_prompt_chars:
            return prompt

    count = len(shown)
    while count > 1 and len(prompt) > max_prompt_chars:
        count -= 1
        prompt = render(count, levels[-1], True)
    return prompt


def _env_flag(name: str) -> bool:
    """Return True when the environment variable holds a truthy value (`true`, `1`, `yes`)."""
    return os.environ.get(name, "").strip().lower() in ("true", "1", "yes")


def main() -> None:
    """Entry point: read env, load failures, write prompt file."""
    allure_dir = Path(os.environ.get("ALLURE_RESULTS_DIR", "allure-results"))
    junit_dir_value = os.environ.get("JUNIT_RESULTS_DIR")
    output_path = Path(os.environ.get("PROMPT_OUTPUT", "ai-analysis-input/prompt.txt"))
    suite_label = os.environ.get("SUITE_LABEL", "WISP")
    max_failures = int(os.environ.get("MAX_FAILURES", "20"))
    max_trace_chars = int(os.environ.get("MAX_TRACE_CHARS", "1500"))
    max_prompt_chars = int(os.environ.get("MAX_PROMPT_CHARS", "16000"))
    collect_evidence = _env_flag("AI_PROMPT_SOAP_EVIDENCE")
    max_evidence_items = int(os.environ.get("MAX_EVIDENCE_ITEMS", "3"))
    max_evidence_chars = int(os.environ.get("MAX_EVIDENCE_CHARS", "400"))
    max_evidence_total_chars = int(os.environ.get("MAX_EVIDENCE_TOTAL_CHARS", "4000"))

    failures = load_failures(allure_dir, collect_evidence=collect_evidence)
    if junit_dir_value:
        failures.extend(drop_junit_duplicates(failures, load_junit_failures(Path(junit_dir_value))))
    prompt = build_prompt(
        failures,
        suite_label,
        max_failures,
        max_trace_chars,
        max_prompt_chars=max_prompt_chars,
        max_evidence_items=max_evidence_items,
        max_evidence_chars=max_evidence_chars,
        max_evidence_total_chars=max_evidence_total_chars,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(prompt, encoding="utf-8")
    evidence_count = sum(len(failure.get("evidence") or []) for failure in failures)
    print(
        f"[build_ai_prompt] wrote '{output_path}' "
        f"({len(prompt)} chars, {len(failures)} failures, {evidence_count} evidence items, "
        f"budget {max_prompt_chars or 'off'})"
    )


if __name__ == "__main__":
    main()
