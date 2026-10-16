"""Local regression tests for NRT GitHub Pages indexes."""

import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest


SOURCE_ROOT = Path(__file__).resolve().parents[2]
PUBLISHER = runpy.run_path(str(Path(__file__).with_name("nrt-publish-indexes.py")))


class PublisherTests(unittest.TestCase):
    def setUp(self):
        """Create an isolated site with the repository's real templates."""
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.original_cwd = Path.cwd()
        self.original_tz = os.environ.get("TZ")
        self.addCleanup(self.restore_environment)
        os.chdir(self.workspace.name)
        shutil.copytree(SOURCE_ROOT / ".github" / "templates", ".github/templates")
        Path("public").mkdir()
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def restore_environment(self):
        """Restore the caller's directory and timezone."""
        os.chdir(self.original_cwd)
        if self.original_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = self.original_tz
        if hasattr(PUBLISHER["time"], "tzset"):
            PUBLISHER["time"].tzset()

    def write_report(self, name, start, passed=5, array=False):
        """Write a minimal Allure report with object or array summary sections."""
        report = Path("public/checkout-e2e-tests") / name
        (report / "widgets").mkdir(parents=True)
        time_data = {"start": start, "stop": start + 65000, "duration": 65000}
        statistic = {"passed": passed, "failed": 2, "skipped": 1}
        summary = {
            "time": [time_data] if array else time_data,
            "statistic": [statistic] if array else statistic,
        }
        (report / "widgets/summary.json").write_text(json.dumps(summary))
        (report / "index.html").write_text(f"Allure report {name}")
        return report

    def test_latest_report_and_history_index(self):
        """Keep old runs, select by start time, and exclude latest from the index."""
        old = self.write_report("99", 1000, passed=3)
        latest = self.write_report("10", 2000, passed=7, array=True)
        stale = latest.parent / "last-history"
        stale.mkdir()
        (stale / "stale.txt").write_text("obsolete")
        technical = Path("public/checkout-e2e-tests-uat/last-history")
        technical.mkdir(parents=True)
        (technical / "history.json").write_text("unchanged")

        stats = PUBLISHER["update_suite"](latest.parent)
        self.assertEqual(stats["passed"], 7)
        for report in (old, latest, stale):
            self.assertTrue((report / "stats.json").is_file())
        self.assertFalse((stale / "stale.txt").exists())
        self.assertEqual((stale / "index.html").read_text(), "Allure report 10")
        index = (latest.parent / "index.html").read_text(encoding="utf-8")
        self.assertIn("./99/index.html", index)
        self.assertIn("./10/index.html", index)
        self.assertNotIn("./last-history/index.html", index)
        self.assertIn("Passed: 7", index)
        self.assertEqual((technical / "history.json").read_text(), "unchanged")
        self.assertEqual(PUBLISHER["update_suite"](latest.parent), stats)

    def test_dashboard_includes_registry_and_unavailable_suites(self):
        """Render real counters and mark unpublished suites without broken links."""
        self.write_report("32", 1000)
        registry = {"suites": [
            {"id": "checkout", "label": "Checkout <E2E>", "allure_subfolder": "checkout-e2e-tests"},
            {"id": "fdr3", "label": "FDR-3", "allure_subfolder": "fdr3-tests"},
        ]}
        Path(".github/nrt-suites.json").write_text(json.dumps(registry))
        PUBLISHER["main"]()
        dashboard = Path("public/index.html").read_text(encoding="utf-8")
        self.assertIn("Checkout &lt;E2E&gt;", dashboard)
        self.assertIn("./checkout-e2e-tests/index.html", dashboard)
        self.assertIn("Passed: 5", dashboard)
        self.assertIn("Failed: 2", dashboard)
        self.assertIn("Skipped: 1", dashboard)
        self.assertIn("0:01:05", dashboard)
        self.assertIn("FDR-3", dashboard)
        self.assertIn("Report non ancora disponibile", dashboard)
        self.assertNotIn("./fdr3-tests/index.html", dashboard)
        self.assertIn("UTC", dashboard)
        self.assertTrue(Path("public/.nojekyll").exists())

    def test_invalid_summary_fails_without_overwriting_index(self):
        """Reject missing counters instead of publishing success-shaped defaults."""
        report = self.write_report("32", 1000)
        summary_path = report / "widgets/summary.json"
        summary = json.loads(summary_path.read_text())
        del summary["statistic"]["passed"]
        summary_path.write_text(json.dumps(summary))
        index = report.parent / "index.html"
        index.write_text("existing index")
        with self.assertRaises(KeyError):
            PUBLISHER["update_suite"](report.parent)
        self.assertEqual(index.read_text(), "existing index")
        self.assertFalse((report / "stats.json").exists())

    def test_empty_suite_warns(self):
        """Do not advertise a suite without usable report data."""
        root = Path("public/empty-tests")
        root.mkdir()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertIsNone(PUBLISHER["update_suite"](root))
        self.assertIn("::warning::", output.getvalue())

    def test_invalid_times_fail(self):
        """Reject invalid start and stop times before creating statistics."""
        report = self.write_report("32", 1000)
        summary_path = report / "widgets/summary.json"
        original = json.loads(summary_path.read_text())
        for key, value in (("start", 0), ("start", True), ("stop", 999)):
            with self.subTest(key=key, value=value):
                summary = {**original, "time": {**original["time"], key: value}}
                summary_path.write_text(json.dumps(summary))
                with self.assertRaises(ValueError):
                    PUBLISHER["update_suite"](report.parent)
                self.assertFalse((report / "stats.json").exists())


if __name__ == "__main__":
    unittest.main()
