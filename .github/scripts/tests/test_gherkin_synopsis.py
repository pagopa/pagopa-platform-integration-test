"""Unit tests for gherkin_synopsis.py: cleaning, hashing, selection, word limits, validation, retries and exit codes.

No test reaches the network: every generation uses FakeGenerator, and the API key is a fake value.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
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


def make_repo(root: Path, suites: dict[str, bool], features: list[tuple[str, str, str, str]]) -> Path:
    """Create a fake repository with a manifest, the prompt template and the feature files.

    suites maps a suite id to its enabled flag. features are (suite id, feature id, file name, text)
    tuples, listed in the manifest in the given order and written under src/e2e/<suite>/features/.
    """
    manifest_suites = []
    for suite_id, enabled in suites.items():
        listed = [
            {"id": feature_id, "path": f"features/{name}"}
            for owner, feature_id, name, _text in features
            if owner == suite_id
        ]
        manifest_suites.append(
            {"id": suite_id, "root": f"src/e2e/{suite_id}", "enabled": enabled, "features": listed}
        )
    write(root / MANIFEST, yaml.safe_dump({"version": 1, "suites": manifest_suites}, sort_keys=False, allow_unicode=True))
    write(root / TEMPLATE, TEST_TEMPLATE)
    for owner, _feature_id, name, text in features:
        write(root / f"src/e2e/{owner}/features/{name}", text)
    return root


def standard_repo(root: Path) -> Path:
    """Build the usual fixture: two active features in suite alpha (one and three scenarios) and one in a disabled suite beta."""
    return make_repo(
        root,
        {"alpha": True, "beta": False},
        [
            ("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A", 1)),
            ("alpha", "FEAT_B", "b.feature", feature_text("FEAT_B", 3)),
            ("beta", "FEAT_C", "c.feature", feature_text("FEAT_C", 1)),
        ],
    )


def args(repo: Path, *extra: str) -> list[str]:
    """Return the command-line arguments for a run in repo with no pause between calls."""
    return ["--repo-root", str(repo), "--pause-seconds", "0", *extra]


def read_synopses(repo: Path) -> dict:
    """Parse the synopses file written in repo."""
    return json.loads((repo / SYNOPSES).read_text(encoding="utf-8"))


def old_entry(path: str, synopsis: str, locked: bool = False) -> dict:
    """Return a synopsis entry with a fake hash, for files prepared as test setup."""
    entry = {"path": path, "content_hash": "sha256:" + "0" * 64, "model": "old-model", "synopsis": synopsis}
    if locked:
        entry["locked"] = True
    return entry


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
    gen = FakeGenerator([words(31), SHORT, SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 3
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
    gen = FakeGenerator([words(31), words(31), SHORT])
    assert sync.main(args(repo), generator=gen) == 1
    stored = read_synopses(repo)["suites"]
    assert stored["alpha"]["FEAT_A"]["synopsis"] == "Vecchia sinossi."
    assert stored["alpha"]["FEAT_B"]["synopsis"] == SHORT


def test_max_tokens_answer_is_rejected(sync, tmp_path):
    """An answer cut at the output limit is never stored, even when its text looks complete."""
    repo = make_repo(tmp_path, {"alpha": True}, [("alpha", "FEAT_A", "a.feature", feature_text("FEAT_A"))])
    gen = FakeGenerator([(SHORT, "MAX_TOKENS"), (SHORT, "MAX_TOKENS")])
    assert sync.main(args(repo), generator=gen) == 1
    assert read_synopses(repo)["suites"] == {}


def test_three_call_failures_in_a_row_stop_the_run_and_keep_progress(sync, tmp_path):
    """Three consecutive call failures stop the loop with exit 1; the synopsis already made is written."""
    features = [("alpha", f"FEAT_{index}", f"f{index}.feature", feature_text(f"FEAT_{index}")) for index in range(1, 6)]
    repo = make_repo(tmp_path, {"alpha": True}, features)
    gen = FakeGenerator([SHORT, RuntimeError("all models failed"), OSError("reset"), RuntimeError("quota")])
    assert sync.main(args(repo), generator=gen) == 1
    assert len(gen.prompts) == 4
    assert list(read_synopses(repo)["suites"]["alpha"]) == ["FEAT_1"]


def test_max_calls_defers_the_rest_and_next_run_continues(sync, tmp_path):
    """With --max-calls 1 only one feature is done; the next run does the remaining one and keeps the first."""
    repo = standard_repo(tmp_path)
    gen = FakeGenerator([SHORT])
    assert sync.main(args(repo, "--max-calls", "1"), generator=gen) == 0
    assert list(read_synopses(repo)["suites"]["alpha"]) == ["FEAT_A"]
    gen = FakeGenerator([SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 1
    assert list(read_synopses(repo)["suites"]["alpha"]) == ["FEAT_A", "FEAT_B"]


# ---------------------------------------------------------------- selection and schema


def test_output_follows_the_schema_and_keeps_accents(sync, tmp_path):
    """The file has version, prompt_version and suites; entries carry path, hash, model and synopsis; no date fields."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
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
    assert list(data["suites"]) == ["alpha"]


def test_second_run_without_changes_makes_no_call_and_no_write(sync, tmp_path):
    """Running twice without changes makes no AI call and leaves the file byte for byte identical."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
    first = (repo / SYNOPSES).read_bytes()
    gen = FakeGenerator([])
    assert sync.main(args(repo), generator=gen) == 0
    assert gen.prompts == []
    assert (repo / SYNOPSES).read_bytes() == first


def test_force_regenerates_unlocked_entries(sync, tmp_path):
    """With --force every unlocked entry is generated again even when its hash did not change."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
    gen = FakeGenerator([SHORT, SHORT])
    assert sync.main(args(repo, "--force"), generator=gen) == 0
    assert len(gen.prompts) == 2


def test_changed_text_regenerates_only_that_feature(sync, tmp_path):
    """Changing the content of one feature regenerates only that feature."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
    before = read_synopses(repo)["suites"]["alpha"]["FEAT_A"]
    write(repo / "src/e2e/alpha/features/b.feature", feature_text("FEAT_B", 2))
    gen = FakeGenerator(["Nuova sinossi di prova."])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 1
    stored = read_synopses(repo)["suites"]["alpha"]
    assert stored["FEAT_A"] == before
    assert stored["FEAT_B"]["synopsis"] == "Nuova sinossi di prova."


def test_tag_only_change_does_not_regenerate(sync, tmp_path):
    """Changing only the tag of a feature file makes no AI call."""
    repo = standard_repo(tmp_path)
    assert sync.main(args(repo), generator=FakeGenerator([SHORT, SHORT])) == 0
    write(repo / "src/e2e/alpha/features/a.feature", feature_text("ALTRO_TAG", 1))
    gen = FakeGenerator([])
    assert sync.main(args(repo), generator=gen) == 0
    assert gen.prompts == []


def test_locked_entry_is_never_regenerated_even_with_force(sync, tmp_path):
    """A locked entry keeps its synopsis and its hash, even when the text changed and --force is given."""
    repo = standard_repo(tmp_path)
    locked = old_entry("src/e2e/alpha/features/a.feature", "Correzione manuale.", locked=True)
    write(repo / SYNOPSES, json.dumps({"version": 1, "prompt_version": "1", "suites": {"alpha": {"FEAT_A": locked}}}))
    gen = FakeGenerator([SHORT])
    assert sync.main(args(repo, "--force"), generator=gen) == 0
    assert len(gen.prompts) == 1
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_A"] == locked


def test_disabled_entries_are_kept_and_dead_entries_removed(sync, tmp_path):
    """Entries of a disabled suite stay as they are, and entries missing from the manifest are removed."""
    repo = standard_repo(tmp_path)
    beta = old_entry("src/e2e/beta/features/c.feature", "Sinossi della suite spenta.")
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
    gen = FakeGenerator([SHORT])
    assert sync.main(args(repo), generator=gen) == 0
    assert len(gen.prompts) == 1
    assert read_synopses(repo)["suites"]["alpha"]["FEAT_B"] == kept
    assert "not found" in capsys.readouterr().out


def test_api_key_is_hidden_from_settings_repr(sync):
    """The generation settings hold the key for the call but never show it in their text form."""
    settings = sync.GenerationSettings(models=["m"], base_url="https://example.invalid", api_key="secret-key-x")
    assert "secret-key-x" not in repr(settings)


# ---------------------------------------------------------------- exit codes and configuration


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
    assert "to generate: 2" in capsys.readouterr().out


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
def test_real_manifest_selects_twenty_five_clean_entries(sync, tmp_path):
    """On the real manifest the dry run selects 25 features (wisp 7, checkout 7, fdr3 11) with clean texts."""
    features = sync.load_manifest_features(REPO_ROOT / MANIFEST)
    plan = sync.plan_work(REPO_ROOT, features, sync.load_synopses_file(tmp_path / "missing.json"), force=False)
    assert len(plan.targets) == 25
    assert Counter(target.key[0] for target in plan.targets) == Counter({"wisp": 7, "checkout": 7, "fdr3": 11})
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
