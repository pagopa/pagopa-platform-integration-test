"""Unit tests for rendering AI analysis beside a published report."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".github" / "scripts"))

from process_reports import deploy_ai_analysis, split_suite_sections


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


AGGREGATE_ANALYSIS = """Intro written by the model

## Suite: checkout
# 1. Checkout failure
```
## Suite: not-a-heading
```
### Root cause
PSP missing

## Common patterns
Checkout patterns

## Suite: fdr3
No failures

## Suite: WISP - 2 failures
# 1. Wisp failure
## Common patterns
Wisp patterns

## Cross-suite correlation
Shared downstream issue
"""


def test_split_suite_sections_keeps_each_suite_apart() -> None:
    """Split on suite headings, ignoring fenced code and leaving the cross-suite section out."""
    sections = split_suite_sections(AGGREGATE_ANALYSIS)

    assert list(sections) == ["checkout", "fdr3", "wisp"]
    assert sections["checkout"].startswith("## Suite: checkout")
    assert "## Suite: not-a-heading" in sections["checkout"]
    assert "Checkout patterns" in sections["checkout"]
    assert "Wisp" not in sections["checkout"]
    assert sections["fdr3"] == "## Suite: fdr3\nNo failures"
    assert "Wisp patterns" in sections["wisp"]
    assert "Shared downstream issue" not in sections["wisp"]
    assert "Intro written by the model" not in "".join(sections.values())


def test_split_suite_sections_without_suite_headings_is_empty() -> None:
    """Return no sections for a single-suite analysis."""
    assert split_suite_sections("# 1. Failure\n### Root cause\nTimeout") == {}


def test_split_suite_sections_closes_a_fence_only_with_the_same_marker() -> None:
    """Keep a heading hidden while a backtick fence contains a tilde fence, and see it once closed."""
    markdown = "## Suite: a\n```\n~~~\n## Suite: hidden\n~~~\n```\n## Suite: b\ntext"

    sections = split_suite_sections(markdown)

    assert list(sections) == ["a", "b"]
    assert "## Suite: hidden" in sections["a"]


def test_split_suite_sections_ignores_a_fence_that_is_never_closed() -> None:
    """Do not hide a suite heading behind a stray opening fence."""
    sections = split_suite_sections("## Suite: a\n```\ntrace\n## Suite: b\ntext")

    assert list(sections) == ["a", "b"]
    assert sections["b"] == "## Suite: b\ntext"


def test_split_suite_sections_matches_headings_loosely() -> None:
    """Accept any case and spell ids with punctuation the way the model writes them."""
    sections = split_suite_sections("## SUITE: FDR-3\nfirst\n## suite:Checkout E2E\nsecond")

    assert sections == {"fdr3": "## SUITE: FDR-3\nfirst", "checkout": "## suite:Checkout E2E\nsecond"}


def _write_aggregate_artifact(tmp_path: Path) -> Path:
    """Create the aggregate analysis artifact and return the artifacts directory."""
    artifact_dir = tmp_path / "artifacts"
    analysis_artifact = artifact_dir / "nrt-ai-analysis"
    analysis_artifact.mkdir(parents=True)
    (analysis_artifact / "analysis.md").write_text(AGGREGATE_ANALYSIS, encoding="utf-8")
    return artifact_dir


def test_deploy_ai_analysis_publishes_only_the_suite_section(tmp_path, monkeypatch) -> None:
    """Show one suite in index.html and keep the whole analysis in full.html and analysis.md."""
    monkeypatch.chdir(Path(__file__).resolve().parents[2])
    report_dir = tmp_path / "public" / "checkout-e2e-tests" / "run"
    report_dir.mkdir(parents=True)
    history_dir = tmp_path / "public" / "checkout-e2e-tests" / "last-history"

    deploy_ai_analysis(
        artifact_dir=_write_aggregate_artifact(tmp_path),
        run_dir=report_dir,
        last_history_dir=history_dir,
        analysis_artifact_name="nrt-ai-analysis",
        suite_label="Checkout E2E - aggregate NRT analysis",
        timestamp="run",
        suite_id="checkout",
        scoped_suite_label="Checkout E2E - NRT analysis",
    )

    for base in (report_dir, history_dir):
        index_html = (base / "analysis" / "index.html").read_text(encoding="utf-8")
        assert "PSP missing" in index_html
        assert "Wisp patterns" not in index_html
        assert "CHECKOUT E2E - NRT ANALYSIS" in index_html
        assert 'href="full.html"' in index_html
        full_html = (base / "analysis" / "full.html").read_text(encoding="utf-8")
        assert "PSP missing" in full_html and "Wisp patterns" in full_html
        assert "AGGREGATE NRT ANALYSIS" in full_html
        assert "full.html" not in full_html
        assert (base / "analysis" / "analysis.md").read_text(encoding="utf-8") == (
            AGGREGATE_ANALYSIS.strip()
        )


def test_deploy_ai_analysis_falls_back_to_the_whole_analysis(tmp_path, monkeypatch, capsys) -> None:
    """Warn and publish the whole analysis when the suite has no section, dropping a stale full.html."""
    monkeypatch.chdir(Path(__file__).resolve().parents[2])
    report_dir = tmp_path / "public" / "other-tests" / "run"
    (report_dir / "analysis").mkdir(parents=True)
    (report_dir / "analysis" / "full.html").write_text("stale", encoding="utf-8")

    deploy_ai_analysis(
        artifact_dir=_write_aggregate_artifact(tmp_path),
        run_dir=report_dir,
        last_history_dir=None,
        analysis_artifact_name="nrt-ai-analysis",
        suite_label="Other - aggregate NRT analysis",
        timestamp="run",
        suite_id="other",
        scoped_suite_label="Other - NRT analysis",
    )

    index_html = (report_dir / "analysis" / "index.html").read_text(encoding="utf-8")
    assert "PSP missing" in index_html and "Wisp patterns" in index_html
    assert "AGGREGATE NRT ANALYSIS" in index_html
    assert "full.html" not in index_html
    assert not (report_dir / "analysis" / "full.html").exists()
    assert "::warning::The AI analysis has no '## Suite: other' section" in capsys.readouterr().out


def test_deploy_ai_analysis_without_suite_id_leaves_other_files_alone(tmp_path, monkeypatch) -> None:
    """Keep the single-suite flow untouched: no splitting and no deletion of a full.html."""
    monkeypatch.chdir(Path(__file__).resolve().parents[2])
    report_dir = tmp_path / "public" / "TAS" / "run"
    (report_dir / "analysis").mkdir(parents=True)
    (report_dir / "analysis" / "full.html").write_text("unrelated", encoding="utf-8")

    deploy_ai_analysis(
        artifact_dir=_write_aggregate_artifact(tmp_path),
        run_dir=report_dir,
        last_history_dir=None,
        analysis_artifact_name="nrt-ai-analysis",
        suite_label="TAS",
        timestamp="run",
    )

    index_html = (report_dir / "analysis" / "index.html").read_text(encoding="utf-8")
    assert "PSP missing" in index_html and "Wisp patterns" in index_html
    assert (report_dir / "analysis" / "full.html").read_text(encoding="utf-8") == "unrelated"
