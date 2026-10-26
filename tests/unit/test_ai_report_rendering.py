"""Unit tests for rendering AI analysis beside a published report."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".github" / "scripts"))

from process_reports import deploy_ai_analysis


def test_deploy_ai_analysis_renders_only_the_current_report(tmp_path, monkeypatch) -> None:
    """Render HTML and Markdown in the report without creating history output."""
    repository_root = Path(__file__).resolve().parents[2]
    monkeypatch.chdir(repository_root)

    artifact_dir = tmp_path / "artifacts"
    analysis_artifact = artifact_dir / "tas-ai-analysis"
    analysis_artifact.mkdir(parents=True)
    (analysis_artifact / "analysis.md").write_text("# Root cause\nNetwork timeout", encoding="utf-8")
    (analysis_artifact / "response.json").write_text(
        json.dumps({"modelVersion": "test-model"}), encoding="utf-8"
    )
    timestamp = "2026-10-23_14-05-09"
    report_dir = tmp_path / "public" / "TAS" / timestamp
    report_dir.mkdir(parents=True)

    deploy_ai_analysis(
        artifact_dir=artifact_dir,
        run_dir=report_dir,
        last_history_dir=None,
        analysis_artifact_name="tas-ai-analysis",
        suite_label="checkout e2e",
        timestamp=timestamp,
        history_url=None,
    )

    analysis_dir = report_dir / "analysis"
    rendered_html = (analysis_dir / "index.html").read_text(encoding="utf-8")
    assert "Root cause" in rendered_html
    assert "test-model" in rendered_html
    assert "Storico" not in rendered_html
    assert (analysis_dir / "analysis.md").read_text(encoding="utf-8") == (
        "# Root cause\nNetwork timeout"
    )
    assert not (tmp_path / "last-history").exists()

    history_report = tmp_path / "public" / "NRT" / "2026-10-23_14-05-10"
    history_report.mkdir(parents=True)
    deploy_ai_analysis(
        artifact_dir=artifact_dir,
        run_dir=history_report,
        last_history_dir=tmp_path / "public" / "NRT" / "last-history",
        analysis_artifact_name="tas-ai-analysis",
        suite_label="checkout e2e",
        timestamp="2026-10-23_14-05-10",
    )
    history_html = (history_report / "analysis" / "index.html").read_text(encoding="utf-8")
    assert 'href="../../index.html"' in history_html