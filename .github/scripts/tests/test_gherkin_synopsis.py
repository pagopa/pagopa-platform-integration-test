"""Unit tests for gherkin_synopsis.py: cleaning, hashing, selection, word limits, validation, retries and exit codes.

No test reaches the network: every generation uses FakeGenerator, and the API key is a fake value.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "gherkin_synopsis.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ".github/gherkin-manifest.yml"
TEMPLATE = ".github/templates/feature-synopsis-prompt.txt"
SYNOPSES = ".github/gherkin-synopses.json"
TEST_TEMPLATE = "Massimo {max_words} parole.\n{feature_text}\n"
SHORT = "Verifica il flusso di pagamento nel suo insieme, con esiti positivi e negativi."
DOC = '"' * 3


@pytest.fixture(scope="module")
def sync():
    """Load gherkin_synopsis.py as a module without running its main()."""
    spec = importlib.util.spec_from_file_location("gherkin_synopsis", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gherkin_synopsis"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def gemini_env(monkeypatch):
    """Give every test a fake key and a one-model chain; tests that need no key delete it themselves."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    monkeypatch.setenv("AVAILABLE_MODELS", json.dumps(["model-a"]))
    monkeypatch.delenv("MODEL_LIMITS", raising=False)
    monkeypatch.delenv("BASE_URL", raising=False)


class FakeGenerator:
    """Scripted stand-in for gemini_analysis.generate_analysis that records every prompt.

    A script item is a text (answered with finishReason STOP), a (text, finish_reason) tuple,
    or an exception to raise. A call after the script ran out fails the test.
    """

    def __init__(self, script=()):
        """Store the scripted answers in call order."""
        self.script = list(script)
        self.prompts: list[str] = []

    def __call__(self, prompt, models, max_output_tokens, base_url, api_key, thinking_level="", model_limits=None):
        """Record the prompt and return the next scripted answer in the shape of generate_analysis."""
        self.prompts.append(prompt)
        if not self.script:
            raise AssertionError("unexpected AI call")
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        text, finish = item if isinstance(item, tuple) else (item, "STOP")
        response = {
            "candidates": [{"finishReason": finish}],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 5, "totalTokenCount": 15},
        }
        return "model-a", response, text


def words(count: int) -> str:
    """Return a text of exactly count words."""
    return " ".join(["parola"] * count)


def feature_text(tag: str, scenarios: int = 1) -> str:
    """Return a feature file with one tag line and the given number of scenarios."""
    lines = [f"@{tag}", "Funzionalità: test di prova", ""]
    for index in range(scenarios):
        lines += [f"  Scenario: caso {index}", "    Given un dato", "    Then un esito"]
    return "\n".join(lines) + "\n"


def write(path: Path, text: str) -> Path:
    """Create a UTF-8 file with the given text, creating its parent folders first."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def make_repo(root: Path, suites: list[str], features: list[tuple[str, str, str, str]]) -> Path:
    """Create a fake repository with a manifest, the prompt template and the feature files.

    Features are (suite id, feature id, file name, text) tuples, listed in the
    manifest in order and written under src/e2e/<suite>/features/.
    """
    manifest_suites = []
    for suite_id in suites:
        listed = [
            {"id": feature_id, "path": f"features/{name}"}
            for owner, feature_id, name, _text in features
            if owner == suite_id
        ]
        manifest_suites.append(
            {"id": suite_id, "root": f"src/e2e/{suite_id}", "features": listed}
        )
    write(root / MANIFEST, yaml.safe_dump({"version": 1, "suites": manifest_suites}, sort_keys=False, allow_unicode=True))
    write(root / TEMPLATE, TEST_TEMPLATE)
    for owner, _feature_id, name, text in features:
        write(root / f"src/e2e/{owner}/features/{name}", text)
    return root


def standard_repo(root: Path) -> Path:
    """Build the usual fixture: two features in suite alpha and one in suite beta."""
    return make_repo(
        root,
        ["alpha", "beta"],
        [
            ("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A", 1)),
            ("alpha", "FEAT_B", "b.feature", feature_text("FEAT_B", 3)),
            ("beta", "FEAT_C", "c.feature", feature_text("FEAT_C", 1)),
        ],
    )


def args(repo: Path, *extra: str) -> list[str]:
    """Return the command-line arguments for a run in repo with no pause between calls."""
    return ["--repo-root", str(repo), "--pause-seconds", "0", *extra]


def run_git(repo: Path, *arguments: str) -> str:
    """Run isolated Git fixture commands with fake identity and no hooks or signing."""
    return subprocess.run(
        [
            "git", "--no-pager", "-c", f"core.hooksPath={repo / '.git' / 'no-hooks'}",
            "-c", "user.name=QA test", "-c", "user.email=qa-tests@example.invalid",
            "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false",
            "-C", str(repo), *arguments,
        ],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout.strip()


def pr_changes(repo: Path, *paths: str) -> list[str]:
    """Create local PR snapshots and paginated metadata without changing the source repository."""
    if not (repo / ".git").exists():
        run_git(repo, "init", "--quiet")
        run_git(repo, "add", "--all")
        features = [path for path in paths if path.startswith("src/") and path.endswith(".feature")]
        if features:
            run_git(repo, "update-index", "--force-remove", "--", *features)
        run_git(repo, "commit", "--quiet", "--allow-empty", "-m", "Fixture base")
    base = run_git(repo, "rev-parse", "HEAD")
    run_git(repo, "add", "--all")
    run_git(repo, "commit", "--quiet", "--allow-empty", "-m", "Fixture PR")
    head = run_git(repo, "rev-parse", "HEAD")
    page = [{"filename": path, "status": "modified"} for path in paths]
    path = write(repo / ".git" / f"pr-files-{head}.json", json.dumps([page]))
    return [
        "--pr-files-file", str(path), "--pr-files-count", str(len(page)),
        "--pr-base", base, "--pr-head", head,
    ]


def read_synopses(repo: Path) -> dict:
    """Parse the synopses file written in repo."""
    return json.loads((repo / SYNOPSES).read_text(encoding="utf-8"))


def old_entry(path: str, synopsis: str) -> dict:
    """Return a synopsis entry with a fake hash, for files prepared as test setup."""
    return {"path": path, "content_hash": "sha256:" + "0" * 64, "model": "old-model", "synopsis": synopsis}


# ---------------------------------------------------------------- cleaning


def test_clean_removes_tag_and_comment_lines(sync):
    """Tag lines, '#' comment lines and language lines are dropped, and the feature lines are kept."""
    raw = "# language: it\n#<123456>\n@FEAT_001 @tag\nFunzionalità: x\n  # commento\n  @scenario_tag\n  Scenario: s\n    Given x\n"
    assert sync.clean_feature_text(raw) == "Funzionalità: x\n  Scenario: s\n    Given x"


def test_clean_keeps_at_and_hash_inside_docstrings(sync):
    """Lines starting with '@' or '#' inside a docstring block are content and stay."""
    raw = "\n".join(
        [
            "Funzionalità: x",
            "  Scenario: s",
            "    Given corpo",
            f"      {DOC}",
            "      # riga interna",
            "      @riga_interna",
            f"      {DOC}",
            "    Then esito",
            "  # commento fuori",
        ]
    )
    cleaned = sync.clean_feature_text(raw)
    assert "      # riga interna" in cleaned.split("\n")
    assert "      @riga_interna" in cleaned.split("\n")
    assert "  # commento fuori" not in cleaned


def test_clean_keeps_example_rows_and_tidies_blank_lines(sync):
    """Example table rows stay, trailing spaces go, blank runs become one, and CRLF line endings become LF."""
    raw = "\r\n\r\nFunzionalità: x\r\n\r\n\r\n  Scenario Outline: s\r\n    Examples:\r\n      | a | b |\r\n      | 1 | 2 |   \r\n\r\n\r\n"
    assert sync.clean_feature_text(raw) == (
        "Funzionalità: x\n\n  Scenario Outline: s\n    Examples:\n      | a | b |\n      | 1 | 2 |"
    )


# ---------------------------------------------------------------- hash


def test_hash_ignores_tags_comments_and_trailing_spaces(sync):
    """Changing only tags, comments or trailing spaces leaves the content hash unchanged."""
    base = sync.clean_feature_text("@A\nFunzionalità: x\n  Scenario: s\n    Given y\n")
    tagged = sync.clean_feature_text("@B @C\n# nota\nFunzionalità: x\n  Scenario: s\n    Given y   \n")
    digest = sync.compute_content_hash(base, "1")
    assert digest == sync.compute_content_hash(tagged, "1")
    assert digest.startswith("sha256:") and len(digest) == len("sha256:") + 64


def test_hash_changes_with_content_and_prompt_version(sync):
    """The hash changes when the cleaned text changes and when the prompt version changes."""
    text = sync.clean_feature_text("Funzionalità: x\n  Scenario: s\n    Given y\n")
    changed = sync.clean_feature_text("Funzionalità: x\n  Scenario: s\n    Given z\n")
    digest = sync.compute_content_hash(text, "1")
    assert digest != sync.compute_content_hash(changed, "1")
    assert digest != sync.compute_content_hash(text, "2")


# ---------------------------------------------------------------- word limit and scenarios


@pytest.mark.parametrize(
    "scenarios, expected",
    [(1, 30), (2, 34), (3, 39), (4, 43), (5, 48), (6, 52), (7, 57), (8, 61), (9, 66), (10, 70), (11, 75), (12, 80)],
)
def test_max_words_matches_the_table(sync, scenarios, expected):
    """The word limit for 1 to 12 scenarios follows the table of the plan (D24)."""
    assert sync.max_words_for(scenarios) == expected


def test_max_words_treats_zero_as_one_and_caps_at_eighty(sync):
    """Zero scenarios use the limit of one, and large counts never go above 80 words."""
    assert sync.max_words_for(0) == 30
    assert sync.max_words_for(40) == 80


def test_max_words_rejects_negative_counts(sync):
    """A negative scenario count is an error, not a silent default."""
    with pytest.raises(ValueError):
        sync.max_words_for(-1)


def test_count_scenarios_counts_outline_once_and_skips_example_rows(sync):
    """Each scenario keyword counts once, including Scenario Outline, while its Esempi rows do not count."""
    text = "\n".join(
        [
            "Funzionalità: x",
            "  Scenario: a",
            "  Scenario Outline: b",
            "    Esempi:",
            "      | x |",
            "      | 1 |",
            "  Esempio: c",
            "  Example: d",
            "  Scenario Template: e",
            "  Schema dello scenario: f",
        ]
    )
    assert sync.count_scenarios(text) == 6


def test_count_scenarios_ignores_docstrings_and_comments(sync):
    """Keywords inside docstrings, in comments or behind a tag do not count as scenarios."""
    text = "\n".join(
        [
            "Funzionalità: x",
            f"  {DOC}",
            "  Scenario: dentro il blocco",
            f"  {DOC}",
            "  Scenario: vero",
            "# Scenario: commentato",
            "@Scenario: con tag",
        ]
    )
    assert sync.count_scenarios(text) == 1


# ---------------------------------------------------------------- validation


def test_validate_accepts_the_limit_and_rejects_one_more(sync):
    """A text at the limit is accepted and one word more is rejected, for one and for twelve scenarios."""
    assert sync.validate_synopsis(words(30), sync.max_words_for(1)) == words(30)
    with pytest.raises(sync.SynopsisRejected):
        sync.validate_synopsis(words(31), sync.max_words_for(1))
    assert sync.validate_synopsis(words(80), sync.max_words_for(12)) == words(80)
    with pytest.raises(sync.SynopsisRejected):
        sync.validate_synopsis(words(81), sync.max_words_for(12))


@pytest.mark.parametrize(
    "answer",
    ["- primo\n- secondo", "* punto elenco", "# Titolo\nTesto", "1. prima voce", "Testo con @tag dentro", "   ", ""],
)
def test_validate_rejects_lists_headings_tags_and_empty_text(sync, answer):
    """Lists, headings, '@' and empty answers are rejected instead of being cut or repaired."""
    with pytest.raises(sync.SynopsisRejected):
        sync.validate_synopsis(answer, 80)


def test_normalize_removes_label_and_quotes_and_joins_lines(sync):
    """The 'Sinossi:' label, a bold label and wrapping quotes go, and the lines become one spaced line."""
    assert sync.normalize_synopsis('Sinossi: "Prima riga\ncontinua   qui."') == "Prima riga continua qui."
    assert sync.normalize_synopsis("**Sinossi:** testo breve") == "testo breve"


def test_label_followed_by_list_is_rejected(sync):
    """A label that leaves a list line behind is still a list, so the answer is rejected."""
    with pytest.raises(sync.SynopsisRejected):
        sync.validate_synopsis("Sinossi:\n- elenco", 80)


# ---------------------------------------------------------------- generation loop through main()


def test_retry_after_invalid_answer_uses_tighter_limit(sync, tmp_path, capsys):
    """An answer over the limit is retried once with a tighter limit; the second answer is stored."""
    repo = standard_repo(tmp_path)
    gen = FakeGenerator([words(31), SHORT, SHORT, SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 4
    assert "al massimo 20 parole" in gen.prompts[1]
    assert "al massimo 20 parole" not in gen.prompts[0]
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == SHORT
    output = capsys.readouterr()
    assert "test-key-not-real" not in output.out + output.err


def test_two_invalid_answers_keep_the_old_synopsis_and_exit_one(sync, tmp_path):
    """When both attempts are invalid the old synopsis stays, the other features go on, and the exit code is 1."""
    repo = standard_repo(tmp_path)
    write(repo / SYNOPSES, json.dumps({
        "version": 1,
        "prompt_version": "1",
        "suites": {"alpha": {"FEAT_A": old_entry("src/e2e/alpha/features/a.feature", "Vecchia sinossi.")}},
    }))
    changed = pr_changes(repo, "src/e2e/alpha/features/a.feature")
    gen = FakeGenerator([words(31), words(31), SHORT, SHORT])
    assert sync.main(args(repo, *changed), generator=gen) == 1
    stored = read_synopses(repo)["suites"]
    assert stored["alpha"]["FEAT_A"]["synopsis"] == "Vecchia sinossi."
    assert stored["alpha"]["FEAT_B"]["synopsis"] == SHORT
    assert sync.main(args(repo, *changed), generator=FakeGenerator([SHORT])) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == SHORT


def test_max_tokens_answer_is_rejected(sync, tmp_path):
    """An answer cut at the output limit is never stored, even when its text looks complete."""
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    gen = FakeGenerator([(SHORT, "MAX_TOKENS"), (SHORT, "MAX_TOKENS")])
    assert sync.main(args(repo), generator=gen) == 1
    assert read_synopses(repo)["suites"] == {}


def test_three_call_failures_in_a_row_stop_the_run_and_keep_progress(sync, tmp_path):
    """Three consecutive call failures stop the loop with exit 1; the synopsis already made is written."""
    features = [("alpha", f"FEAT_{index}", f"f{index}.feature", feature_text(f"FEAT_{index}")) for index in range(1, 6)]
    repo = make_repo(tmp_path, ["alpha"], features)
    gen = FakeGenerator([SHORT, RuntimeError("all models failed"), OSError("reset"), RuntimeError("quota")])
    assert sync.main(args(repo), generator=gen) == 1
    assert len(gen.prompts) == 4
    assert list(read_synopses(repo)["suites"]["alpha"]) == ["FEAT_1"]


def test_max_calls_defers_the_rest_and_next_run_continues(sync, tmp_path):
    """Missing synopses deferred by the call cap are generated on the next run."""
    repo = standard_repo(tmp_path)
    gen = FakeGenerator([SHORT])
    assert sync.main(args(repo, "--max-calls", "1"), generator=gen) == 0
    assert list(read_synopses(repo)["suites"]["alpha"]) == ["FEAT_A"]
    gen = FakeGenerator([SHORT, SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 2
    assert list(read_synopses(repo)["suites"]["alpha"]) == ["FEAT_A", "FEAT_B"]
    assert list(read_synopses(repo)["suites"]["beta"]) == ["FEAT_C"]


# ---------------------------------------------------------------- selection and schema


def test_output_follows_the_schema_and_keeps_accents(sync, tmp_path):
    """The file has version, prompt_version and suites; entries carry path, hash, model and synopsis; no date fields."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    raw = (repo / SYNOPSES).read_text(encoding="utf-8")
    data = json.loads(raw)
    assert list(data) == ["version", "prompt_version", "suites"]
    assert data["version"] == 1 and data["prompt_version"] == "1"
    entry = data["suites"]["alpha"]["FEAT_A"]
    assert list(entry) == ["path", "content_hash", "model", "synopsis"]
    assert entry["path"] == "src/e2e/alpha/features/a.feature"
    assert entry["model"] == "model-a"
    assert "data" not in raw and "time" not in raw
    assert "Verifica il flusso" in raw
    assert raw.endswith("}\n")
    assert list(data["suites"]) == ["alpha", "beta"]


def test_second_run_without_changes_makes_no_call_and_no_write(sync, tmp_path):
    """Running twice without changes makes no AI call and leaves the file byte for byte identical."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    first = (repo / SYNOPSES).read_bytes()
    gen = FakeGenerator([])
    assert sync.main(args(repo), generator=gen) == 0
    assert gen.prompts == []
    assert (repo / SYNOPSES).read_bytes() == first


def test_changed_text_regenerates_only_that_feature(sync, tmp_path):
    """Changed text regenerates only when its feature belongs to the selected PR."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    before = read_synopses(repo)["suites"]["alpha"]["FEAT_A"]
    write(repo / "src/e2e/alpha/features/b.feature", feature_text("FEAT_B", 2))
    unchanged = (repo / SYNOPSES).read_bytes()
    assert sync.main(args(repo), generator=FakeGenerator([])) == 0
    assert (repo / SYNOPSES).read_bytes() == unchanged
    gen = FakeGenerator(["Nuova sinossi di prova."])
    changed = pr_changes(repo, "src/e2e/alpha/features/b.feature")
    assert sync.main(args(repo, *changed), generator=gen) == 0
    assert len(gen.prompts) == 1
    stored = read_synopses(repo)["suites"]["alpha"]
    assert stored["FEAT_A"] == before
    assert stored["FEAT_B"]["synopsis"] == "Nuova sinossi di prova."


def test_paginated_pr_files_filter_deleted_and_unrelated_paths(sync, tmp_path):
    """Only existing feature paths in complete, paginated PR metadata are eligible."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    write(repo / a, feature_text("FEAT_A", 2))
    write(repo / b, feature_text("FEAT_B", 2))
    pages = [
        [{"filename": a, "status": "renamed", "previous_filename": "old.feature"}],
        [{"filename": b, "status": "removed"}, {"filename": "README.md", "status": "modified"}],
    ]
    changed = pr_changes(repo, a, b, "README.md")
    write(Path(changed[1]), json.dumps(pages))
    before_b = read_synopses(repo)["suites"]["alpha"]["FEAT_B"]
    gen = FakeGenerator(["Sinossi aggiornata."])
    assert sync.main(args(repo, *changed), generator=gen) == 0
    assert len(gen.prompts) == 1
    stored = read_synopses(repo)["suites"]["alpha"]
    assert stored["FEAT_A"]["synopsis"] == "Sinossi aggiornata."
    assert stored["FEAT_B"] == before_b


def test_tag_only_change_does_not_regenerate(sync, tmp_path):
    """Changing only a tag in a PR makes no AI call."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    write(repo / "src/e2e/alpha/features/a.feature", feature_text("ALTRO_TAG", 1))
    gen = FakeGenerator([])
    changed = pr_changes(repo, "src/e2e/alpha/features/a.feature")
    assert sync.main(args(repo, *changed), generator=gen) == 0
    assert gen.prompts == []


@pytest.mark.parametrize("synopsis", ["", "   "])
def test_missing_synopsis_is_generated_without_a_changed_feature(sync, tmp_path: Path, synopsis: str) -> None:
    """An empty synopsis is generated even without a PR feature selection."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    write(repo / SYNOPSES, json.dumps({
        "version": 1,
        "prompt_version": "1",
        "suites": {"alpha": {"FEAT_A": old_entry(path, synopsis)}},
    }))
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == SHORT


def test_prompt_version_change_does_not_trigger_regeneration(sync, tmp_path, monkeypatch):
    """Compare each entry with its original hash version, even after partial regeneration."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    monkeypatch.setattr(sync, "PROMPT_VERSION", "2")
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    write(repo / a, feature_text("NEW_TAG"))
    assert sync.main(args(repo, *pr_changes(repo, a)), generator=FakeGenerator([])) == 0

    write(repo / b, feature_text("FEAT_B", 2))
    changed = pr_changes(repo, b)
    assert sync.main(args(repo, *changed), generator=FakeGenerator([SHORT])) == 0
    data = read_synopses(repo)
    assert data["prompt_version"] == "1"
    assert data["suites"]["alpha"]["FEAT_B"]["prompt_version"] == "2"
    assert "prompt_version" not in data["suites"]["alpha"]["FEAT_A"]
    before = (repo / SYNOPSES).read_bytes()
    assert sync.main(args(repo, *changed), generator=FakeGenerator([])) == 0
    assert (repo / SYNOPSES).read_bytes() == before


@pytest.mark.parametrize(
    "feature_changed,synopsis_changed,expected_calls",
    [(True, False, 1), (True, True, 0), (False, True, 0)],
)
def test_pr_synopsis_edit_takes_precedence(
    sync, tmp_path: Path, feature_changed: bool, synopsis_changed: bool, expected_calls: int,
) -> None:
    """Feature-only edits generate text; synopsis edits win in both mixed and Hub-only PRs."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    paths = []
    if feature_changed:
        write(repo / path, feature_text("FEAT_A", 2))
        paths.append(path)
    if synopsis_changed:
        data = read_synopses(repo)
        data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione dall'hub."
        write(repo / SYNOPSES, json.dumps(data))
        paths.append(SYNOPSES)
    changed = pr_changes(repo, *paths)
    gen = FakeGenerator(["Nuova sinossi AI."] * expected_calls)
    assert sync.main(args(repo, *changed), generator=gen) == 0
    assert len(gen.prompts) == expected_calls
    expected = "Correzione dall'hub." if synopsis_changed else "Nuova sinossi AI."
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == expected
    assert sync.main(args(repo, *changed), generator=FakeGenerator([])) == 0

    pr_changes(repo)
    write(repo / path, "# Nuovo commento\n" + feature_text("ALTRO_TAG", 2 if feature_changed else 1))
    assert sync.main(args(repo, *pr_changes(repo, path)), generator=FakeGenerator([])) == 0
    write(repo / path, feature_text("FEAT_A", 3))
    assert sync.main(
        args(repo, *pr_changes(repo, path)), generator=FakeGenerator(["Sinossi della PR successiva."])
    ) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Sinossi della PR successiva."


def test_synopsis_edit_excludes_only_its_feature(sync, tmp_path: Path) -> None:
    """A JSON text edit protects only its feature, not other feature changes in the same PR."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    pr_changes(repo)
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    write(repo / a, feature_text("FEAT_A", 2))
    write(repo / b, feature_text("FEAT_B", 2))
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Sinossi scelta dall'utente."
    write(repo / SYNOPSES, json.dumps(data))
    gen = FakeGenerator(["Sinossi AI della seconda feature."])
    assert sync.main(args(repo, *pr_changes(repo, a, b, SYNOPSES)), generator=gen) == 0
    stored = read_synopses(repo)["suites"]["alpha"]
    assert len(gen.prompts) == 1
    assert stored["FEAT_A"]["synopsis"] == "Sinossi scelta dall'utente."
    assert stored["FEAT_B"]["synopsis"] == "Sinossi AI della seconda feature."


def test_synopsis_edit_follows_path_when_feature_ids_are_swapped(sync, tmp_path: Path) -> None:
    """Reused ids cannot extend a manual synopsis override to another feature path."""
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    repo = make_repo(tmp_path, ["alpha"], [
        ("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A")),
        ("alpha", "FEAT_B", "b.feature", feature_text("FEAT_B")),
    ])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
    pr_changes(repo)
    write(repo / a, feature_text("FEAT_B", 2))
    write(repo / b, feature_text("FEAT_A", 2))
    manifest = yaml.safe_load((repo / MANIFEST).read_text(encoding="utf-8"))
    manifest["suites"][0]["features"][0]["id"] = "FEAT_B"
    manifest["suites"][0]["features"][1]["id"] = "FEAT_A"
    write(repo / MANIFEST, yaml.safe_dump(manifest))
    data = read_synopses(repo)
    entries = data["suites"]["alpha"]
    entries["FEAT_A"], entries["FEAT_B"] = entries["FEAT_B"], entries["FEAT_A"]
    entries["FEAT_B"]["synopsis"] = "Correzione per il primo percorso."
    write(repo / SYNOPSES, json.dumps(data))
    gen = FakeGenerator(["Nuova sinossi del secondo percorso."])
    assert sync.main(args(repo, *pr_changes(repo, a, b, MANIFEST, SYNOPSES)), generator=gen) == 0
    stored = read_synopses(repo)["suites"]["alpha"]
    assert len(gen.prompts) == 1
    assert stored["FEAT_B"]["synopsis"] == "Correzione per il primo percorso."
    assert stored["FEAT_A"]["synopsis"] == "Nuova sinossi del secondo percorso."


@pytest.mark.parametrize("remove", [False, True])
def test_empty_or_removed_synopsis_is_not_recreated_in_same_pr(sync, tmp_path: Path, remove: bool) -> None:
    """An explicit removal or empty text wins over missing-synopsis generation for that PR."""
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    data = read_synopses(repo)
    if remove:
        del data["suites"]["alpha"]["FEAT_A"]
    else:
        data["suites"]["alpha"]["FEAT_A"]["synopsis"] = ""
    write(repo / SYNOPSES, json.dumps(data))
    assert sync.main(args(repo, *pr_changes(repo, SYNOPSES)), generator=FakeGenerator([])) == 0
    stored = read_synopses(repo)["suites"].get("alpha", {})
    assert "FEAT_A" not in stored if remove else stored["FEAT_A"]["synopsis"] == ""


def test_metadata_only_synopsis_edit_does_not_prevent_generation(sync, tmp_path: Path) -> None:
    """Changing JSON metadata without changing synopsis text does not suppress a feature update."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    write(repo / path, feature_text("FEAT_A", 2))
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["model"] = "metadata-only"
    write(repo / SYNOPSES, json.dumps(data))
    assert sync.main(
        args(repo, *pr_changes(repo, path, SYNOPSES)), generator=FakeGenerator(["Nuova sinossi."])
    ) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Nuova sinossi."


def test_queued_manual_edit_does_not_consume_a_later_feature_change(sync, tmp_path: Path) -> None:
    """Keep the manual PR's hash baseline so a later feature-only PR still generates its synopsis."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Sinossi della PR Hub."
    write(repo / SYNOPSES, json.dumps(data))
    manual_pr = pr_changes(repo, SYNOPSES)
    write(repo / path, feature_text("FEAT_A", 2))
    feature_pr = pr_changes(repo, path)
    assert sync.main(args(repo, *manual_pr), generator=FakeGenerator([])) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Sinossi della PR Hub."
    assert sync.main(args(repo, *feature_pr), generator=FakeGenerator(["Sinossi del feature aggiornato."])) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Sinossi del feature aggiornato."


def test_queued_feature_pr_preserves_later_published_edit(sync, tmp_path: Path) -> None:
    """A later human edit beats a stale queued PR without blocking another changed feature."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    pr_changes(repo)
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    write(repo / a, feature_text("FEAT_A", 2))
    write(repo / b, feature_text("FEAT_B", 2))
    source = pr_changes(repo, a, b)
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione pubblicata."
    write(repo / SYNOPSES, json.dumps(data))
    published = pr_changes(repo, SYNOPSES)[-1]
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Sinossi AI ancora nella PR cumulativa."
    write(repo / SYNOPSES, json.dumps(data))

    gen = FakeGenerator(["Sinossi aggiornata per la seconda feature."])
    assert sync.main(
        args(repo, *source, "--pr-merge", source[-1], "--published-base", published), generator=gen
    ) == 0
    entries = read_synopses(repo)["suites"]["alpha"]
    assert len(gen.prompts) == 1
    assert entries["FEAT_A"]["synopsis"] == "Correzione pubblicata."
    assert entries["FEAT_B"]["synopsis"] == "Sinossi aggiornata per la seconda feature."


def test_reverted_published_edit_still_protects_queued_pr(sync, tmp_path: Path) -> None:
    """An intervening human edit followed by a revert still beats an older queued generation."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    write(repo / path, feature_text("FEAT_A", 2))
    source = pr_changes(repo, path)
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Modifica successiva."
    write(repo / SYNOPSES, json.dumps(data))
    pr_changes(repo, SYNOPSES)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = SHORT
    write(repo / SYNOPSES, json.dumps(data))
    published = pr_changes(repo, SYNOPSES)[-1]

    gen = FakeGenerator([])
    assert sync.main(
        args(repo, *source, "--pr-merge", source[-1], "--published-base", published), generator=gen
    ) == 0
    assert gen.prompts == []
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == SHORT


@pytest.mark.parametrize("reviewed", [False, True])
def test_later_squashed_sync_pr_distinguishes_ai_and_review_edits(
    sync, tmp_path: Path, reviewed: bool,
) -> None:
    """A later AI update does not suppress generation; a reviewer correction in it does."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    write(repo / path, feature_text("FEAT_A", 2))
    source = pr_changes(repo, path)
    main_branch = run_git(repo, "branch", "--show-current")
    run_git(repo, "switch", "-c", "older-sync")
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Sinossi AI precedente."
    write(repo / SYNOPSES, json.dumps(data))
    pr_changes(repo, SYNOPSES)
    reviewer_commits = []
    if reviewed:
        data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione del revisore."
        write(repo / SYNOPSES, json.dumps(data))
        reviewer_commits.append(pr_changes(repo, SYNOPSES)[-1])
    run_git(repo, "switch", main_branch)
    run_git(repo, "merge", "--squash", "older-sync")
    run_git(repo, "commit", "-m", "Squash sync PR")
    published = run_git(repo, "rev-parse", "HEAD")
    metadata = write(repo / ".git" / "published-reviews.json", json.dumps({published: reviewer_commits}))

    gen = FakeGenerator([] if reviewed else ["Sinossi della nuova feature."])
    assert sync.main(
        args(
            repo, *source, "--pr-merge", source[-1], "--published-base", published,
            "--published-reviews", str(metadata),
        ),
        generator=gen,
    ) == 0
    assert len(gen.prompts) == (0 if reviewed else 1)
    expected = "Correzione del revisore." if reviewed else "Sinossi della nuova feature."
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == expected


@pytest.mark.parametrize("removed", [False, True])
def test_published_manual_pr_overrides_pending_branch(sync, tmp_path: Path, removed: bool) -> None:
    """The published correction or deletion replaces the same entry in the cumulative PR branch."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    data = read_synopses(repo)
    pending = dict(data["suites"]["alpha"]["FEAT_A"])
    if removed:
        del data["suites"]["alpha"]["FEAT_A"]
    else:
        data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione pubblicata."
    write(repo / SYNOPSES, json.dumps(data))
    source = pr_changes(repo, SYNOPSES)
    data["suites"]["alpha"]["FEAT_A"] = pending
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Sinossi AI in attesa."
    write(repo / SYNOPSES, json.dumps(data))

    assert sync.main(
        args(repo, *source, "--pr-merge", source[-1], "--published-base", source[-1]),
        generator=FakeGenerator([]),
    ) == 0
    entries = read_synopses(repo)["suites"].get("alpha", {})
    assert "FEAT_A" not in entries if removed else entries["FEAT_A"]["synopsis"] == "Correzione pubblicata."


def test_published_override_is_applied_without_api_key(sync, tmp_path: Path, monkeypatch) -> None:
    """A missing AI key cannot leave stale pending text that overrides a published correction."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione pubblicata."
    write(repo / SYNOPSES, json.dumps(data))
    source = pr_changes(repo, SYNOPSES)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Sinossi AI in attesa."
    write(repo / SYNOPSES, json.dumps(data))
    monkeypatch.delenv("GEMINI_API_KEY")

    assert sync.main(
        args(repo, *source, "--pr-merge", source[-1], "--published-base", source[-1]),
        generator=FakeGenerator([]),
    ) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Correzione pubblicata."


def test_older_events_keep_synopsis_generated_for_a_later_feature_change(sync, tmp_path: Path) -> None:
    """A late older event must not discard an already-generated synopsis for a newer feature PR."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    write(repo / path, feature_text("FEAT_A", 2))
    older_feature = pr_changes(repo, path)
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione pubblicata."
    write(repo / SYNOPSES, json.dumps(data))
    manual = pr_changes(repo, SYNOPSES)
    write(repo / path, feature_text("FEAT_A", 3))
    newer_feature = pr_changes(repo, path)
    published = newer_feature[-1]
    assert sync.main(
        args(repo, *newer_feature, "--pr-merge", published, "--published-base", published),
        generator=FakeGenerator(["Sinossi della feature successiva."]),
    ) == 0

    for source in (older_feature, manual):
        assert sync.main(
            args(repo, *source, "--pr-merge", source[-1], "--published-base", published),
            generator=FakeGenerator([]),
        ) == 0
        assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Sinossi della feature successiva."


def test_later_manual_edit_beats_pending_synopsis_for_current_feature(sync, tmp_path: Path) -> None:
    """A matching feature hash cannot override a human correction published after that feature."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    pr_changes(repo)
    write(repo / path, feature_text("FEAT_A", 2))
    feature = pr_changes(repo, path)
    original = read_synopses(repo)
    assert sync.main(args(repo, *feature), generator=FakeGenerator(["Sinossi AI in attesa."])) == 0
    pending = read_synopses(repo)
    original["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione pubblicata dopo la feature."
    write(repo / SYNOPSES, json.dumps(original))
    manual = pr_changes(repo, SYNOPSES)
    write(repo / SYNOPSES, json.dumps(pending))

    assert sync.main(
        args(repo, *manual, "--pr-merge", manual[-1], "--published-base", manual[-1]),
        generator=FakeGenerator([]),
    ) == 0
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["synopsis"] == "Correzione pubblicata dopo la feature."


def test_pending_review_edit_is_not_overwritten(sync, tmp_path: Path) -> None:
    """Keep a reviewer's pending text while regenerating a different changed feature."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    pr_changes(repo)
    main_branch = run_git(repo, "branch", "--show-current")
    run_git(repo, "switch", "-c", "pending")
    data = read_synopses(repo)
    data["suites"]["alpha"]["FEAT_A"]["synopsis"] = "Correzione del revisore."
    write(repo / SYNOPSES, json.dumps(data))
    pr_changes(repo, SYNOPSES)
    run_git(repo, "switch", main_branch)
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    write(repo / a, feature_text("FEAT_A", 2))
    write(repo / b, feature_text("FEAT_B", 2))
    source = pr_changes(repo, a, b)
    run_git(repo, "switch", "pending")
    run_git(repo, "merge", "--no-edit", main_branch)
    pending = run_git(repo, "rev-parse", "HEAD")

    gen = FakeGenerator(["Sinossi aggiornata per la seconda feature."])
    assert sync.main(
        args(repo, *source, "--pr-merge", source[-1], "--published-base", source[-1], "--pending-head", pending),
        generator=gen,
    ) == 0
    entries = read_synopses(repo)["suites"]["alpha"]
    assert len(gen.prompts) == 1
    assert entries["FEAT_A"]["synopsis"] == "Correzione del revisore."
    assert entries["FEAT_B"]["synopsis"] == "Sinossi aggiornata per la seconda feature."


def test_conflicting_pending_and_published_manual_edits_stop(sync, tmp_path: Path) -> None:
    """Do not choose silently between different published and pending human corrections."""
    path = "src/e2e/alpha/features/a.feature"
    write(tmp_path / path, feature_text("FEAT_A"))
    key = ("alpha", "FEAT_A")
    feature = sync.ManifestFeature("alpha", "FEAT_A", path)
    pending = old_entry(path, "Correzione in revisione.")
    published = old_entry(path, "Correzione pubblicata.")
    with pytest.raises(sync.SynopsisError, match="published and pending manual synopsis edits differ"):
        sync.plan_work(
            tmp_path, [feature], sync.SynopsisDocument("1", {key: pending}), set(),
            edited_synopses={key: "testo"}, published_overrides={key: published},
            published_prompt_version="1", pending_manual={key},
        )


def test_completion_marker_only_records_a_completed_run(sync, tmp_path: Path) -> None:
    """A handled generation failure writes a marker; invalid inputs cannot authorize publication."""
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    completed = tmp_path / "completed.txt"
    assert sync.main(
        args(repo, "--completion-marker", str(completed)), generator=FakeGenerator([RuntimeError("model failed")])
    ) == 1
    assert completed.read_text(encoding="utf-8") == "1\n"
    invalid = tmp_path / "invalid.txt"
    assert sync.main(
        args(repo, "--completion-marker", str(invalid), "--pr-merge", "bad"), generator=FakeGenerator([])
    ) == 2
    assert not invalid.exists()


def test_legacy_lock_does_not_prevent_generation(sync, tmp_path: Path) -> None:
    """A legacy lock is ignored and removed rather than becoming a permanent override."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    entry = old_entry(path, "Sinossi precedente.")
    entry["locked"] = True
    write(repo / SYNOPSES, json.dumps({"version": 1, "prompt_version": "1", "suites": {"alpha": {"FEAT_A": entry}}}))
    assert sync.main(args(repo, *pr_changes(repo, path)), generator=FakeGenerator([SHORT])) == 0
    stored = read_synopses(repo)["suites"]["alpha"]["FEAT_A"]
    assert stored["synopsis"] == SHORT
    assert "locked" not in stored


def test_id_change_rekeys_synopsis_by_path(sync, tmp_path: Path) -> None:
    """A header-driven id change keeps the old synopsis under the new id when the path is stable."""
    path = "src/e2e/alpha/features/a.feature"
    write(tmp_path / path, feature_text("FEAT_NEW"))
    old = old_entry(path, "Correzione manuale.")
    existing = sync.SynopsisDocument(
        prompt_version=sync.PROMPT_VERSION,
        entries={("alpha", "FEAT_OLD"): old},
    )
    feature = sync.ManifestFeature("alpha", "FEAT_NEW", path)

    plan = sync.plan_work(tmp_path, [feature], existing, changed_features=set())

    assert plan.targets == []
    assert plan.removed == []
    assert plan.entries == {("alpha", "FEAT_NEW"): old}


def test_reused_ids_do_not_swap_synopses_between_paths(sync, tmp_path):
    """Rekey by path before id when two features exchange their ids."""
    a = "src/e2e/alpha/features/a.feature"
    b = "src/e2e/alpha/features/b.feature"
    write(tmp_path / a, feature_text("FEAT_B"))
    write(tmp_path / b, feature_text("FEAT_A"))
    old_a = old_entry(a, "Sinossi A.")
    old_b = old_entry(b, "Sinossi B.")
    existing = sync.SynopsisDocument("1", {("alpha", "FEAT_A"): old_a, ("alpha", "FEAT_B"): old_b})
    features = [
        sync.ManifestFeature("alpha", "FEAT_B", a),
        sync.ManifestFeature("alpha", "FEAT_A", b),
    ]

    plan = sync.plan_work(tmp_path, features, existing, set())

    assert plan.targets == []
    assert plan.entries == {("alpha", "FEAT_B"): old_a, ("alpha", "FEAT_A"): old_b}


def test_duplicate_old_paths_fail_without_overwriting_synopses(sync, tmp_path: Path) -> None:
    """Ambiguous old entries cannot be silently assigned to the same feature."""
    path = "src/e2e/alpha/features/a.feature"
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    entry = old_entry(path, "Sinossi precedente.")
    write(repo / SYNOPSES, json.dumps({
        "version": 1,
        "prompt_version": "1",
        "suites": {"alpha": {"FEAT_A": entry, "FEAT_OLD": entry}},
    }))
    before = (repo / SYNOPSES).read_bytes()
    assert sync.main(args(repo), generator=FakeGenerator([])) == 2
    assert (repo / SYNOPSES).read_bytes() == before


def test_rename_keeps_existing_synopsis_when_text_is_unchanged(sync, tmp_path):
    """A PR rename updates the stored path without regenerating unchanged text."""
    repo = make_repo(tmp_path, ["alpha"], [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    assert sync.main(args(repo), generator=FakeGenerator([SHORT])) == 0
    source = repo / "src/e2e/alpha/features/a.feature"
    new_path = "src/e2e/alpha/features/renamed.feature"
    source.rename(repo / new_path)
    manifest = yaml.safe_load((repo / MANIFEST).read_text(encoding="utf-8"))
    manifest["suites"][0]["features"][0]["path"] = "features/renamed.feature"
    write(repo / MANIFEST, yaml.safe_dump(manifest, sort_keys=False))
    gen = FakeGenerator([])
    assert sync.main(args(repo, *pr_changes(repo, new_path)), generator=gen) == 0
    assert gen.prompts == []
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"]["path"] == new_path


def test_existing_entries_are_kept_and_dead_entries_removed(sync, tmp_path):
    """Entries still in the manifest stay, and entries for deleted features are removed."""
    repo = standard_repo(tmp_path)
    beta = old_entry("src/e2e/beta/features/c.feature", "Sinossi precedente.")
    gone = old_entry("src/e2e/gone/features/x.feature", "Feature rimossa.")
    write(repo / SYNOPSES, json.dumps({
        "version": 1,
        "prompt_version": "1",
        "suites": {"beta": {"FEAT_C": beta}, "gone": {"FEAT_X": gone}},
    }))
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
    stored = read_synopses(repo)["suites"]
    assert stored["beta"]["FEAT_C"] == beta
    assert "gone" not in stored
    assert set(stored["alpha"]) == {"FEAT_A", "FEAT_B"}


def test_missing_feature_file_is_skipped_and_its_entry_kept(sync, tmp_path, capsys):
    """A feature whose file is gone makes no call, is reported, and keeps the entry it had."""
    repo = standard_repo(tmp_path)
    kept = old_entry("src/e2e/alpha/features/b.feature", "Sinossi precedente.")
    write(repo / SYNOPSES, json.dumps({"version": 1, "prompt_version": "1", "suites": {"alpha": {"FEAT_B": kept}}}))
    (repo / "src/e2e/alpha/features/b.feature").unlink()
    gen = FakeGenerator([SHORT, SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 2
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_B"] == kept
    assert "not found" in capsys.readouterr().out


def test_legacy_enabled_flags_do_not_prevent_synopses(sync, tmp_path):
    """Legacy suite and feature flags do not exclude any feature from synopsis generation."""
    repo = tmp_path
    write(repo / MANIFEST, yaml.safe_dump({
        "version": 1,
        "suites": [{
            "id": "alpha",
            "root": "src/e2e/alpha",
            "enabled": False,
            "features": [
                {"id": "FEAT_A", "path": "features/a.feature"},
                {"id": "FEAT_B", "path": "features/b.feature", "enabled": False},
            ],
        }],
    }, sort_keys=False, allow_unicode=True))
    write(repo / TEMPLATE, TEST_TEMPLATE)
    write(repo / "src/e2e/alpha/features/a.feature", feature_text("FEAT_A", 1))
    write(repo / "src/e2e/alpha/features/b.feature", feature_text("FEAT_B", 1))
    gen = FakeGenerator([SHORT, SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 2
    assert set(read_synopses(repo)["suites"]["alpha"]) == {"FEAT_A", "FEAT_B"}


def test_api_key_is_hidden_from_settings_repr(sync):
    """The generation settings hold the key for the call but never show it in their text form."""
    settings = sync.GenerationSettings(models=["m"], base_url="https://example.invalid", api_key="secret-key-x")
    assert "secret-key-x" not in repr(settings)


# ---------------------------------------------------------------- exit codes and configuration


@pytest.mark.parametrize("payload", ["{bad json", "{}", '[[{"filename": "src/example.feature"}]]', "[[null]]"])
def test_invalid_pr_file_list_stops_without_writing(sync, tmp_path: Path, payload: str) -> None:
    """An invalid PR file list cannot authorize generation or overwrite synopses."""
    repo = standard_repo(tmp_path)
    changed = pr_changes(repo, "README.md")
    write(Path(changed[1]), payload)
    gen = FakeGenerator([])
    assert sync.main(args(repo, *changed), generator=gen) == 2
    assert gen.prompts == []
    assert not (repo / SYNOPSES).exists()


def test_incomplete_pr_file_list_stops_without_writing(sync, tmp_path):
    """A truncated GitHub response is rejected rather than treating missing paths as unchanged."""
    repo = standard_repo(tmp_path)
    changed = pr_changes(repo, "README.md", "other.md")
    write(Path(changed[1]), json.dumps([[{"filename": "README.md", "status": "modified"}]]))
    assert sync.main(args(repo, *changed), generator=FakeGenerator([])) == 2
    assert not (repo / SYNOPSES).exists()


def test_unavailable_pr_revision_is_an_error_not_an_empty_snapshot(sync, tmp_path: Path) -> None:
    """An unavailable commit cannot silently authorize AI generation or overwrite existing text."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT, SHORT])) == 0
    changed = pr_changes(repo, "README.md")
    changed[-1] = "f" * 40
    before = (repo / SYNOPSES).read_bytes()
    assert sync.main(args(repo, *changed), generator=FakeGenerator([])) == 2
    assert (repo / SYNOPSES).read_bytes() == before


def test_no_key_exits_zero_without_writing(sync, tmp_path, monkeypatch, capsys):
    """Without GEMINI_API_KEY the run prints the skipped line, exits 0 and writes nothing."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    repo = standard_repo(tmp_path)
    gen = FakeGenerator([])
    assert sync.main(args(repo), generator=gen) == 0
    assert gen.prompts == []
    assert not (repo / SYNOPSES).exists()
    assert "skipped: no GEMINI_API_KEY" in capsys.readouterr().out


def test_dry_run_selects_without_calls_or_writes(sync, tmp_path, capsys):
    """A dry run reports the features to generate, makes no call and writes no file, with or without a key."""
    repo = standard_repo(tmp_path)
    gen = FakeGenerator([])
    assert sync.main(args(repo, "--dry-run"), generator=gen) == 0
    assert gen.prompts == []
    assert not (repo / SYNOPSES).exists()
    assert "to generate: 3" in capsys.readouterr().out


def test_dry_run_without_key_exits_zero(sync, tmp_path, monkeypatch):
    """A dry run exits 0 when GEMINI_API_KEY is not set."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo, "--dry-run"), generator=FakeGenerator([])) == 0
    assert not (repo / SYNOPSES).exists()


def test_invalid_json_synopses_file_exits_two_and_is_untouched(sync, tmp_path):
    """A synopses file that is not JSON stops the run with exit 2 and is never overwritten."""
    repo = standard_repo(tmp_path)
    write(repo / SYNOPSES, "{non json")
    gen = FakeGenerator([])
    assert sync.main(args(repo), generator=gen) == 2
    assert gen.prompts == []
    assert (repo / SYNOPSES).read_text(encoding="utf-8") == "{non json"


@pytest.mark.parametrize(
    "payload",
    [
        {"version": 2, "prompt_version": "1", "suites": {}},
        {"version": 1, "prompt_version": "1", "suites": {"alpha": {"FEAT_A": {"path": "x"}}}},
    ],
)
def test_wrong_shape_synopses_file_exits_two(sync, tmp_path, payload):
    """A synopses file with another version or another shape stops the run with exit 2 and stays untouched."""
    repo = standard_repo(tmp_path)
    write(repo / SYNOPSES, json.dumps(payload))
    before = (repo / SYNOPSES).read_bytes()
    assert sync.main(args(repo), generator=FakeGenerator([])) == 2
    assert (repo / SYNOPSES).read_bytes() == before


def test_template_without_placeholders_exits_two(sync, tmp_path):
    """A prompt template without both placeholders is a configuration error."""
    repo = standard_repo(tmp_path)
    write(repo / TEMPLATE, "Solo {max_words} parole.")
    assert sync.main(args(repo), generator=FakeGenerator([])) == 2


def test_missing_manifest_exits_two(sync, tmp_path):
    """A missing manifest is a configuration error: exit 2 and nothing is written."""
    repo = standard_repo(tmp_path)
    (repo / MANIFEST).unlink()
    assert sync.main(args(repo), generator=FakeGenerator([])) == 2
    assert not (repo / SYNOPSES).exists()


def test_missing_model_list_with_key_exits_two(sync, tmp_path, monkeypatch):
    """With a key present, a missing or empty AVAILABLE_MODELS is a configuration error and no call is made."""
    monkeypatch.delenv("AVAILABLE_MODELS", raising=False)
    repo = standard_repo(tmp_path)
    gen = FakeGenerator([])
    assert sync.main(args(repo), generator=gen) == 2
    assert gen.prompts == []
    assert not (repo / SYNOPSES).exists()


def test_real_template_has_both_placeholders(sync):
    """The shipped prompt template loads and contains both placeholders."""
    template = sync.load_prompt_template(REPO_ROOT / TEMPLATE)
    assert "{feature_text}" in template and "{max_words}" in template


# ---------------------------------------------------------------- real repository data


@pytest.mark.skipif(
    not (REPO_ROOT / "src").is_dir() or not (REPO_ROOT / MANIFEST).is_file(),
    reason="needs the repository sources and the generated manifest",
)
def test_real_manifest_selects_all_clean_entries(sync, tmp_path):
    """Every real feature receives a target when the synopses file is missing."""
    features = sync.load_manifest_features(REPO_ROOT / MANIFEST)
    plan = sync.plan_work(REPO_ROOT, features, sync.load_synopses_file(tmp_path / "missing.json"), set())
    assert len(plan.targets) == 57
    assert len({target.key[0] for target in plan.targets}) == 13
    for target in plan.targets:
        assert not any(line.startswith(("@", "#")) for line in target.cleaned.split("\n")), target.key


@pytest.mark.skipif(
    not (REPO_ROOT / "src").is_dir() or not (REPO_ROOT / MANIFEST).is_file(),
    reason="needs the repository sources and the generated manifest",
)
def test_real_manifest_dry_run_exits_zero_without_calls(sync, tmp_path):
    """The dry run on the real repository exits 0, makes no AI call and writes nothing."""
    synopses = tmp_path / "synopses.json"
    gen = FakeGenerator([])
    code = sync.main(
        ["--repo-root", str(REPO_ROOT), "--synopses", str(synopses), "--dry-run"], generator=gen
    )
    assert code == 0
    assert gen.prompts == []
    assert not synopses.exists()
