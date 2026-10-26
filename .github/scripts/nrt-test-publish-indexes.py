"""Local regression tests for NRT GitHub Pages indexes."""

import contextlib
from datetime import datetime, timedelta
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest import mock

from process_reports import build_tas_index_page


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

    def test_tas_history_index_includes_complete_runs_newest_first(self):
        """List complete TAS reports newest-first without deleting prior runs."""
        root = Path("public/TAS")
        now = datetime.now().replace(microsecond=0)
        older_name = (now - timedelta(days=1)).strftime("%d-%m-%Y_%H:%M:%S")
        newer_name = now.strftime("%d-%m-%Y_%H:%M:%S")
        incomplete_name = (now + timedelta(seconds=1)).strftime("%d-%m-%Y_%H:%M:%S")
        backing_dirs = {
            older_name: root / "older-run",
            newer_name: root / "newer-run",
            incomplete_name: root / "incomplete-run",
            "last-history": root / "history-run",
        }
        for backing_dir in backing_dirs.values():
            backing_dir.mkdir(parents=True)
        (backing_dirs[older_name] / "index.html").write_text("Older report")
        (backing_dirs[newer_name] / "index.html").write_text("Newer report")
        analysis_dir = backing_dirs[newer_name] / "analysis"
        analysis_dir.mkdir()
        (analysis_dir / "index.html").write_text("AI analysis")
        (backing_dirs[incomplete_name] / "index.html").write_text("")
        (backing_dirs["last-history"] / "index.html").write_text("Not a timestamped run")

        report_dirs = []
        for name, backing_dir in backing_dirs.items():
            report_dir = mock.MagicMock()
            report_dir.name = name
            report_dir.is_dir.return_value = True
            report_dir.__truediv__.side_effect = lambda child, path=backing_dir: path / child
            report_dirs.append(report_dir)
        original_iterdir = Path.iterdir

        def iterdir(path):
            """Return virtual timestamped folders for the TAS root fixture."""
            if path == root:
                return iter(report_dirs)
            return original_iterdir(path)

        with mock.patch.object(Path, "iterdir", iterdir):
            build_tas_index_page(root)

        index = (root / "index.html").read_text(encoding="utf-8")
        self.assertLess(
            index.index(f"./{newer_name}/index.html"),
            index.index(f"./{older_name}/index.html"),
        )
        self.assertNotIn(f"./{incomplete_name}/index.html", index)
        self.assertNotIn("./last-history/index.html", index)
        self.assertIn(f' href="./{newer_name}/analysis/index.html"', index)
        self.assertNotIn(f' href="./{older_name}/analysis/index.html"', index)
        self.assertEqual(index.count("Apri analisi AI"), 1)
        self.assertTrue((backing_dirs[older_name] / "index.html").is_file())
        self.assertTrue((backing_dirs[newer_name] / "index.html").is_file())

    def test_tas_history_index_shows_empty_state_without_reports(self):
        """Render an empty state when no complete TAS reports are available."""
        root = Path("public/TAS")
        root.mkdir()

        build_tas_index_page(root)

        index = (root / "index.html").read_text(encoding="utf-8")
        self.assertIn("Nessun report disponibile.", index)
        self.assertNotIn('href="./', index)

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
        self.assertIn("./TAS/index.html", dashboard)
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

    def test_current_run_analysis_and_history_links(self):
        """Publish aggregate HTML and Markdown without changing unrelated reports."""
        old = self.write_report("old-run", 1000)
        current = self.write_report("current-run", 2000, array=True)
        newer = self.write_report("newer-run", 3000)
        previous_analysis = newer / "analysis"
        previous_analysis.mkdir()
        (previous_analysis / "index.html").write_text("previous analysis")
        matrix = {"include": [
            {"id": "checkout", "label": "Checkout", "allure_subfolder": "checkout-e2e-tests"},
            {"id": "missing", "label": "Missing", "allure_subfolder": "missing-tests"},
        ]}
        source = Path("nrt-allure-history/checkout-e2e-tests-uat/42/widgets")
        source.mkdir(parents=True)
        shutil.copyfile(current / "widgets/summary.json", source / "summary.json")
        analysis = Path("artifacts/nrt-ai-analysis")
        analysis.mkdir(parents=True)
        (analysis / "analysis.md").write_text("# Shared root cause", encoding="utf-8")
        (analysis / "response.json").write_text('{"modelVersion": "test-model"}')
        Path(".github/nrt-suites.json").write_text(json.dumps({"suites": matrix["include"]}))

        # Windows cannot create the colon-containing production timestamp paths.
        clock = mock.Mock(wraps=PUBLISHER["datetime"])
        clock.fromtimestamp = mock.Mock()
        clock.fromtimestamp.return_value.strftime.return_value = current.name
        with mock.patch.dict(PUBLISHER["main"].__globals__, datetime=clock):
            with mock.patch.dict(os.environ, {
                "AI_ANALYSIS_RESULT": "success",
                "SUITE_MATRIX": json.dumps(matrix),
                "TARGET_ENV": "uat",
                "RUN_NUMBER": "42",
            }):
                PUBLISHER["main"]()
        clock.fromtimestamp.assert_called_once_with(2.0, PUBLISHER["timezone"].utc)
        clock.fromtimestamp.return_value.strftime.assert_called_once_with("%Y-%m-%d_%H:%M:%S")

        rendered = (current / "analysis/index.html").read_text(encoding="utf-8")
        self.assertIn("Shared root cause", rendered)
        self.assertIn("AGGREGATE NRT ANALYSIS", rendered)
        self.assertIn("test-model", rendered)
        self.assertIn('href="../index.html"', rendered)
        self.assertEqual(
            (current / "analysis/analysis.md").read_text(encoding="utf-8"),
            "# Shared root cause",
        )
        self.assertFalse((old / "analysis").exists())
        self.assertFalse(Path("public/missing-tests").exists())
        self.assertEqual((previous_analysis / "index.html").read_text(), "previous analysis")
        self.assertEqual(
            (current.parent / "last-history/analysis/index.html").read_text(),
            "previous analysis",
        )
        index = (current.parent / "index.html").read_text(encoding="utf-8")
        self.assertIn("./current-run/analysis/index.html", index)
        self.assertNotIn("./old-run/analysis/index.html", index)

        PUBLISHER["update_suite"](current.parent)
        shutil.rmtree(newer)
        PUBLISHER["update_suite"](current.parent)
        self.assertEqual(
            (current.parent / "last-history/analysis/index.html").read_text(encoding="utf-8"),
            rendered,
        )

    def test_missing_or_empty_successful_analysis_fails(self):
        """Reject a successful AI job that did not produce a usable response."""
        matrix = {"include": []}
        with self.assertRaisesRegex(ValueError, "missing or empty"):
            PUBLISHER["publish_ai_analysis"](matrix, "uat", "42")
        analysis = Path("artifacts/nrt-ai-analysis")
        analysis.mkdir(parents=True)
        (analysis / "analysis.md").write_text(" \n")
        with self.assertRaisesRegex(ValueError, "missing or empty"):
            PUBLISHER["publish_ai_analysis"](matrix, "uat", "42")

    def test_failed_ai_does_not_block_allure_publication(self):
        """Keep Allure indexes available when the supplemental AI job fails."""
        current = self.write_report("current-run", 2000)
        Path(".github/nrt-suites.json").write_text(json.dumps({"suites": [
            {"id": "checkout", "label": "Checkout", "allure_subfolder": "checkout-e2e-tests"},
        ]}))
        with mock.patch.dict(os.environ, {"AI_ANALYSIS_RESULT": "failure"}):
            PUBLISHER["main"]()
        self.assertTrue((current / "stats.json").is_file())
        self.assertFalse((current / "analysis").exists())
        self.assertNotIn(
            "./current-run/analysis/index.html",
            (current.parent / "index.html").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
