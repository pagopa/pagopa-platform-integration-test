"""Unit tests for building the TAS AI analysis prompt."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".github" / "scripts"))

from build_ai_prompt import build_prompt, load_failures, load_junit_failures


def test_build_prompt_deduplicates_allure_and_junit_failures(tmp_path: Path) -> None:
    """Parse matching Allure and JUnit failures and include them only once."""
    allure_dir = tmp_path / "allure-results"
    junit_dir = tmp_path / "junit"
    allure_dir.mkdir()
    junit_dir.mkdir()
    (allure_dir / "allure-result.json").write_text(
        json.dumps(
            {
                "name": "Create payment",
                "fullName": "payments.Create payment",
                "status": "failed",
                "statusDetails": {
                    "message": "ValueError: rejected",
                    "trace": "Allure trace",
                },
            }
        ),
        encoding="utf-8",
    )
    (junit_dir / "results.xml").write_text(
        "<testsuite><testcase name='Create payment' classname='payments'>"
        "<failure message='ValueError: rejected'>JUnit trace</failure>"
        "</testcase></testsuite>",
        encoding="utf-8",
    )

    failures = load_failures(allure_dir) + load_junit_failures(junit_dir)

    prompt = build_prompt(failures, "payments integration", 20, 1500)

    assert "**Total failures: 1**" in prompt
    assert prompt.count("# 1. Create payment") == 1
    assert "# 2. Create payment" not in prompt
    assert "Allure trace" in prompt
    assert "JUnit trace" not in prompt


def test_build_prompt_keeps_same_test_with_different_failure_messages() -> None:
    """Keep distinct failures for a test when their messages differ."""
    failures = [
        {
            "name": "Create payment",
            "fullName": "payments.Create payment",
            "status": "failed",
            "message": "Connection refused",
            "trace": "First trace",
        },
        {
            "name": "Create payment",
            "fullName": "payments.Create payment",
            "status": "failed",
            "message": "Request timed out",
            "trace": "Second trace",
        },
    ]

    prompt = build_prompt(failures, "payments integration", 20, 1500)

    assert "**Total failures: 2**" in prompt
    assert "Connection refused" in prompt
    assert "Request timed out" in prompt


def test_build_prompt_keeps_distinct_tests_with_the_same_short_name() -> None:
    """Use fully qualified names to distinguish otherwise identical failures."""
    failures = [
        {
            "name": "Create payment",
            "fullName": "payments.Create payment",
            "status": "failed",
            "message": "Connection refused",
            "trace": "First trace",
        },
        {
            "name": "Create payment",
            "fullName": "refunds.Create payment",
            "status": "failed",
            "message": "Connection refused",
            "trace": "Second trace",
        },
    ]

    prompt = build_prompt(failures, "payments integration", 20, 1500)

    assert "**Total failures: 2**" in prompt
    assert "payments.Create payment" in prompt
    assert "refunds.Create payment" in prompt