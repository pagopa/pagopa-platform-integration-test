"""Isolated regressions for Quality Gate dispatch and stored Allure links."""

import contextlib
from datetime import datetime
import io
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.models.test_models import Test_runs as RunModel
from src.utility.constants import ALLURE_BASE_URL


ORCHESTRATOR = runpy.run_path(str(REPO_ROOT / "scripts/tas_orchestrator.py"))
with mock.patch.dict("sys.modules", {"src.conf.configuration": mock.Mock()}):
    INGESTION = runpy.run_path(str(REPO_ROOT / ".github/scripts/populate_tables.py"))


class QualityGateTests(unittest.TestCase):
    def test_dispatch_defaults_to_tas_and_forwards_quality_gate_only_when_enabled(self):
        """Keep old workflow refs compatible unless QG is explicitly requested."""
        for enabled in (False, True):
            with self.subTest(enabled=enabled):
                arguments = ["--suite", "checkout", "--env", "uat", "--caller-id", "unit-test"]
                if enabled:
                    arguments.append("--is-quality-gate-run")
                args = ORCHESTRATOR["build_parser"]().parse_args(arguments)
                self.assertEqual(args.is_quality_gate_run, enabled)
                with (
                    mock.patch.dict(os.environ, {"TAS_GITHUB_TOKEN": "fake"}, clear=True),
                    mock.patch.object(ORCHESTRATOR["GitHubClient"], "trigger_workflow") as dispatch,
                    contextlib.redirect_stdout(io.StringIO()),
                ):
                    self.assertEqual(ORCHESTRATOR["run"](args), 0)
                inputs = dispatch.call_args.kwargs["inputs"]
                if enabled:
                    self.assertEqual(inputs["isQualityGateRun"], "true")
                else:
                    self.assertNotIn("isQualityGateRun", inputs)

    def test_ingestion_links_follow_origin_instead_of_nrt_suite_folder(self):
        """Group QG by suite/category while preserving flat TAS and NRT URLs."""
        start = 1793613600000
        timestamp = datetime.fromtimestamp(start / 1000).strftime("%Y-%m-%d_%H:%M:%S")
        summary = {
            "statistic": {"total": 1, "passed": 1, "failed": 0, "broken": 0, "skipped": 0},
            "time": {"start": start, "stop": start + 1000, "duration": 1000},
        }
        with tempfile.TemporaryDirectory() as temporary_dir:
            summary_path = Path(temporary_dir) / "summary.json"
            summary_path.write_text(json.dumps(summary), encoding="utf-8")
            for origin, test_type, nrt_folder, expected in (
                ("TAS", None, None, "TAS"),
                ("QG", "e2e", None, "QG/checkout-e2e"),
                ("QG", "integration", None, "QG/checkout-integration"),
                ("QG", "api", None, "QG/checkout-api"),
                ("TAS", None, "checkout-e2e-tests", "TAS"),
                ("QG", "e2e", "checkout-e2e-tests", "QG/checkout-e2e"),
                ("NRT", None, "checkout-e2e-tests", "checkout-e2e-tests"),
            ):
                with self.subTest(origin=origin, test_type=test_type, nrt_folder=nrt_folder):
                    test_run = RunModel(test_origin=origin)
                    result = INGESTION["populate_test_run"](
                        test_run, str(summary_path), None, "checkout", nrt_folder,
                        test_type=test_type,
                    )
                    self.assertEqual(result.test_origin, origin)
                    self.assertEqual(
                        result.allure_url, f"{ALLURE_BASE_URL}{expected}/{timestamp}/index.html",
                    )

    def test_qg_ingestion_rejects_missing_or_invalid_suite_category(self):
        """Fail before reading artifacts when QG cannot identify its history folder."""
        for test_object, test_type in (
            ("checkout", None), ("checkout", ""), ("checkout", "invalid"), ("", "e2e"),
        ):
            with self.subTest(test_object=test_object, test_type=test_type):
                with self.assertRaisesRegex(ValueError, "QG report links require"):
                    INGESTION["populate_test_run"](
                        RunModel(test_origin="QG"), "unused", None, test_object, None,
                        test_type=test_type,
                    )


if __name__ == "__main__":
    unittest.main()