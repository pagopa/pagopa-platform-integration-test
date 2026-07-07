"""Build a compact AI-analysis prompt from Allure raw results.

Reads all `*-result.json` files under an Allure results directory, keeps only
failed / broken test cases, and writes a Markdown prompt to disk. The prompt
asks the model to categorize each failure and suggest an action.

Environment variables:
    ALLURE_RESULTS_DIR   Directory containing Allure raw results (default: allure-results).
    PROMPT_OUTPUT        Destination path for the generated prompt (default: ai-analysis-input/prompt.txt).
    SUITE_LABEL          Human-readable suite name used in the prompt header (default: WISP).
    MAX_FAILURES         Cap on number of failures included (default: 20).
    MAX_TRACE_CHARS      Cap on trace length per failure (default: 1500).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List


def _clean(value: Any) -> str:
    """Return a stripped string, tolerating None and non-string inputs."""
    if value is None:
        return ""
    return str(value).strip()


def load_failures(allure_results_dir: Path) -> List[Dict[str, str]]:
    """Extract failed/broken test cases from the Allure raw JSON results."""
    failures: List[Dict[str, str]] = []
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
        failures.append(
            {
                "name": _clean(data.get("name")) or "unknown",
                "fullName": _clean(data.get("fullName")),
                "status": _clean(status),
                "message": _clean(details.get("message")),
                "trace": _clean(details.get("trace")),
            }
        )
    return failures


def build_prompt(
    failures: List[Dict[str, str]],
    suite_label: str,
    max_failures: int,
    max_trace_chars: int,
) -> str:
    """Render the Markdown prompt sent to the AI model."""
    if not failures:
        return (
            f"No test failures found in the '{suite_label}' suite. "
            "Confirm that the execution was complete and that no tests were unintentionally skipped. "
            "Reply in English, in a single sentence."
        )

    header = (
        f"You are a senior QA engineer. Analyse the failures from the '{suite_label}' integration test suite.\n"
        "For each failure provide a concise Markdown response using this structure:\n"
        "## Root cause (1-2 lines)\n"
        "## Category ( application bug | test data | environment | flaky )\n"
        "## Recommended action (1-2 lines)\n\n"
        "At the end, add a **Common patterns** section if recurring root causes emerge.\n\n"
        f"**Total failures: {len(failures)}**\n\n"
    )

    parts: List[str] = [header]
    for idx, failure in enumerate(failures[:max_failures], start=1):
        trace = failure["trace"][:max_trace_chars]
        parts.append(
            f"## {idx}. {failure['name']}\n"
            f"- **status**: {failure['status']}\n"
            f"- **fullName**: `{failure['fullName']}`\n"
            f"- **message**: {failure['message']}\n"
            f"- **trace**:\n```\n{trace}\n```\n"
        )

    if len(failures) > max_failures:
        parts.append(f"\n_... {len(failures) - max_failures} more failures omitted._\n")

    return "\n".join(parts)


def main() -> None:
    """Entry point: read env, load failures, write prompt file."""
    allure_dir = Path(os.environ.get("ALLURE_RESULTS_DIR", "allure-results"))
    output_path = Path(os.environ.get("PROMPT_OUTPUT", "ai-analysis-input/prompt.txt"))
    suite_label = os.environ.get("SUITE_LABEL", "WISP")
    max_failures = int(os.environ.get("MAX_FAILURES", "20"))
    max_trace_chars = int(os.environ.get("MAX_TRACE_CHARS", "1500"))

    failures = load_failures(allure_dir)
    prompt = build_prompt(failures, suite_label, max_failures, max_trace_chars)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(prompt, encoding="utf-8")
    print(
        f"[build_ai_prompt] wrote '{output_path}' "
        f"({len(prompt)} chars, {len(failures)} failures)"
    )


if __name__ == "__main__":
    main()
