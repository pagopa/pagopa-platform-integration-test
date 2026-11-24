"""Unit tests for gherkin_manifest_sync.py: ids, discovery, reconciliation, validation and CLI."""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "gherkin_manifest_sync.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ".github/gherkin-manifest.yml"
REGISTRY = ".github/nrt-suites.json"


@pytest.fixture(scope="module")
def sync():
    """Load gherkin_manifest_sync.py as a module without running its main()."""
    spec = importlib.util.spec_from_file_location("gherkin_manifest_sync", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gherkin_manifest_sync"] = module
    spec.loader.exec_module(module)
    return module


def write(path: Path, text: str) -> Path:
    """Create a UTF-8 file with the given text, creating its parent folders first."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def feature(tag: str | None = None, keyword: str = "Funzionalità:") -> str:
    """Return a minimal feature file text, with an optional first tag."""
    head = f"@{tag}\n" if tag else ""
    return f"{head}{keyword} Esempio\n\n  Scenario: uno\n    Given qualcosa\n"


def write_registry(repo: Path, entries: list[dict]) -> None:
    """Write the NRT registry with the given suite entries."""
    write(repo / REGISTRY, json.dumps({"suites": entries}))


def base_repo(repo: Path) -> Path:
    """Create a repository with one enabled suite (checkout, listed in the registry) and one feature."""
    write(repo / "src/e2e/checkout/features/login.feature", feature("FEAT_001_Checkout"))
    write_registry(repo, [{"id": "checkout", "label": "Checkout E2E", "behave_path": "src/e2e/checkout"}])
    return repo


def run_sync(sync, repo: Path, *extra: str) -> int:
    """Run the command-line entry point against repo and return its exit code."""
    return sync.main(["--repo-root", str(repo), *extra])


def read_manifest(repo: Path) -> dict:
    """Parse the manifest written in repo with the standard YAML loader."""
    return yaml.safe_load((repo / MANIFEST).read_text(encoding="utf-8"))


def edit_manifest(repo: Path, mutate) -> None:
    """Load the manifest, apply mutate to it and write it back as test setup."""
    data = read_manifest(repo)
    mutate(data)
    write(repo / MANIFEST, yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def suite_by_id(manifest: dict, suite_id: str) -> dict:
    """Return the suite with the given id from a parsed manifest."""
    return next(suite for suite in manifest["suites"] if suite["id"] == suite_id)


# ---------------------------------------------------------------- candidate id from tags


def test_candidate_is_first_tag_before_keyword(sync, tmp_path):
    """The first tag before the Feature keyword is the candidate id, without '@'."""
    path = write(tmp_path / "a.feature", "@FEAT_001_X @runnable\nFunzionalità: x\n")
    assert sync._tag_candidate(path) == "FEAT_001_X"


@pytest.mark.parametrize("keyword", ["Feature:", "Funzionalita:", "funzionalità :"])
def test_candidate_accepts_supported_keywords(sync, tmp_path, keyword):
    """Feature keywords are recognised in English and Italian, with or without accents and case."""
    path = write(tmp_path / "a.feature", f"@TAG_OK\n{keyword} x\n")
    assert sync._tag_candidate(path) == "TAG_OK"


def test_candidate_skips_language_comments_and_blank_lines(sync, tmp_path):
    """Comment lines and blank lines before the first tag do not stop the search."""
    path = write(tmp_path / "a.feature", "# language: en\n#<123456>\n\n@EN_TAG\nFeature: x\n")
    assert sync._tag_candidate(path) == "EN_TAG"


def test_candidate_ignores_scenario_tags_after_keyword(sync, tmp_path):
    """Tags that appear after the Feature keyword belong to scenarios and give no candidate."""
    path = write(tmp_path / "a.feature", "Funzionalità: x\n\n  @scenario_tag\n  Scenario: s\n")
    assert sync._tag_candidate(path) is None


def test_candidate_rejected_when_first_tag_is_not_a_valid_id(sync, tmp_path):
    """A first tag with parentheses or quotes is discarded instead of being used as id."""
    path = write(tmp_path / "a.feature", '@Crea_FdR(id_fdr="x")\nFunzionalità: x\n')
    assert sync._tag_candidate(path) is None


def test_candidate_reads_file_with_byte_order_mark(sync, tmp_path):
    """A UTF-8 byte order mark at the start of the file does not hide the first tag."""
    path = tmp_path / "a.feature"
    path.write_bytes(b"\xef\xbb\xbf@BOM_TAG\nFeature: x\n")
    assert sync._tag_candidate(path) == "BOM_TAG"


# ---------------------------------------------------------------- fallback id from file name


def test_fallback_replaces_unsafe_runs_with_single_underscore(sync):
    """Spaces and apostrophes in the file name collapse into single underscores."""
    name = "FEAT_005_FdR3_Recupero degli fdR da parte dell'EC.feature"
    assert sync._fallback_feature_id(name) == "FEAT_005_FdR3_Recupero_degli_fdR_da_parte_dell_EC"


def test_fallback_is_at_most_80_characters_and_never_empty(sync):
    """The fallback is truncated to 80 characters and becomes 'feature' when nothing is left."""
    assert len(sync._fallback_feature_id("a" * 120 + ".feature")) == 80
    assert sync._fallback_feature_id("é.feature") == "feature"


# ---------------------------------------------------------------- id collisions


def test_identical_candidates_all_fall_back_to_file_names(sync):
    """Files that share a tag all use their file-name fallback, so no id is chosen by order."""
    paths = ["features/citizen_buys_ebollo.feature", "features/reporting.feature", "features/other.feature"]
    assigned = sync._assign_feature_ids(paths, {path: "eBollo" for path in paths}, set())
    assert assigned == {
        "features/citizen_buys_ebollo.feature": "citizen_buys_ebollo",
        "features/reporting.feature": "reporting",
        "features/other.feature": "other",
    }


def test_reserved_candidate_is_skipped_and_unique_one_is_used(sync):
    """A candidate equal to a reserved id (ignoring case) falls back; a free candidate is used."""
    assigned = sync._assign_feature_ids(
        ["features/a.feature", "features/b.feature"],
        {"features/a.feature": "TAG", "features/b.feature": "tag_b"},
        {"tag"},
    )
    assert assigned == {"features/a.feature": "a", "features/b.feature": "tag_b"}


def test_fallback_collision_gets_numeric_suffix(sync):
    """A fallback that is already taken receives the suffix _2."""
    assigned = sync._assign_feature_ids(["features/dup.feature"], {"features/dup.feature": None}, {"DUP"})
    assert assigned == {"features/dup.feature": "dup_2"}


# ---------------------------------------------------------------- discovery


def test_discovery_keeps_only_files_below_a_features_folder(sync, tmp_path):
    """Files under a features folder at any depth are found; singular, outside, hidden and cache folders are not."""
    base = tmp_path / "src/integration/wisp"
    write(base / "features/a.feature", feature())
    write(base / "features/sub/b/c.feature", feature())
    write(base / "feature/single.feature", feature())
    write(base / "other/d.feature", feature())
    write(base / "features/.hidden/e.feature", feature())
    write(base / "features/__pycache__/f.feature", feature())
    suites = sync.discover_suites(tmp_path)
    assert [(suite.root, suite.feature_paths) for suite in suites] == [
        ("src/integration/wisp", ("features/a.feature", "features/sub/b/c.feature"))
    ]


def test_discovery_ignores_unknown_types_and_folders_without_features(sync, tmp_path):
    """Only api, integration and e2e folders are scanned, and a folder with no feature is not a suite."""
    write(tmp_path / "src/other/x/features/a.feature", feature())
    write(tmp_path / "src/api/empty/README.md", "no features here")
    assert sync.discover_suites(tmp_path) == []


# ---------------------------------------------------------------- suites and registry


def test_suite_id_is_sanitized_folder_name(sync):
    """Folder names are lowercased and unsafe characters become '-'."""
    assert sync._suite_id_from_name("My Suite") == "my-suite"


def test_colliding_folder_names_use_type_prefix(sync, tmp_path):
    """Two folders with the same name in different types both take the <type>-<name> id."""
    base_repo(tmp_path)
    write(tmp_path / "src/api/wisp/features/a.feature", feature("A_1"))
    write(tmp_path / "src/integration/wisp/features/b.feature", feature("B_1"))
    assert run_sync(sync, tmp_path) == 0
    ids = {suite["id"] for suite in read_manifest(tmp_path)["suites"]}
    assert {"api-wisp", "integration-wisp"} <= ids


def test_registry_decides_label_and_activation(sync, tmp_path):
    """A suite in the NRT registry gets its label and is enabled; other new suites are disabled."""
    base_repo(tmp_path)
    write(tmp_path / "src/api/cart/features/cart.feature", feature("FEAT_007"))
    assert run_sync(sync, tmp_path) == 0
    manifest = read_manifest(tmp_path)
    checkout = suite_by_id(manifest, "checkout")
    cart = suite_by_id(manifest, "cart")
    assert checkout["label"] == "Checkout E2E" and "enabled" not in checkout
    assert cart["enabled"] is False and "label" not in cart


def test_missing_or_broken_registry_is_tolerated_with_warning(sync, tmp_path, capsys):
    """A missing or non-JSON registry is read as empty and reported as a warning, not an error."""
    assert sync.load_registry(tmp_path / "missing.json") == {}
    write(tmp_path / "broken.json", "{not json")
    assert sync.load_registry(tmp_path / "broken.json") == {}
    assert "[WARN]" in capsys.readouterr().out


# ---------------------------------------------------------------- reconciliation


def test_missing_manifest_is_created_with_all_features(sync, tmp_path):
    """Without a manifest the script creates one listing every discovered feature."""
    base_repo(tmp_path)
    assert run_sync(sync, tmp_path) == 0
    checkout = suite_by_id(read_manifest(tmp_path), "checkout")
    assert [feature_entry["id"] for feature_entry in checkout["features"]] == ["FEAT_001_Checkout"]


def test_added_file_appears_and_deleted_file_is_removed(sync, tmp_path):
    """New feature files are added on the next run and deleted ones disappear."""
    base_repo(tmp_path)
    run_sync(sync, tmp_path)
    write(tmp_path / "src/e2e/checkout/features/new_one.feature", feature("FEAT_002_Checkout"))
    assert run_sync(sync, tmp_path) == 0
    ids = [entry["id"] for entry in suite_by_id(read_manifest(tmp_path), "checkout")["features"]]
    assert "FEAT_002_Checkout" in ids
    (tmp_path / "src/e2e/checkout/features/login.feature").unlink()
    assert run_sync(sync, tmp_path) == 0
    ids = [entry["id"] for entry in suite_by_id(read_manifest(tmp_path), "checkout")["features"]]
    assert ids == ["FEAT_002_Checkout"]


def test_disabled_entry_is_removed_when_its_file_is_gone(sync, tmp_path):
    """A hand-disabled entry whose file was deleted is removed, like any dead entry."""
    base_repo(tmp_path)
    run_sync(sync, tmp_path)
    edit_manifest(tmp_path, lambda data: suite_by_id(data, "checkout")["features"][0].update(enabled=False))
    (tmp_path / "src/e2e/checkout/features/login.feature").unlink()
    write(tmp_path / "src/e2e/checkout/features/other.feature", feature("FEAT_009_Checkout"))
    assert run_sync(sync, tmp_path) == 0
    ids = [entry["id"] for entry in suite_by_id(read_manifest(tmp_path), "checkout")["features"]]
    assert ids == ["FEAT_009_Checkout"]


def test_renamed_file_keeps_id_estimate_and_enabled(sync, tmp_path):
    """A file moved to another folder with the same tag keeps its id, estimate and enabled flag."""
    base_repo(tmp_path)
    run_sync(sync, tmp_path)

    def hand_edit(data):
        """Give the feature an estimate and disable it, as a person would."""
        entry = suite_by_id(data, "checkout")["features"][0]
        entry.update(estimate_days=0.5, enabled=False)

    edit_manifest(tmp_path, hand_edit)
    source = tmp_path / "src/e2e/checkout/features/login.feature"
    target = tmp_path / "src/e2e/checkout/features/moved/login_renamed.feature"
    target.parent.mkdir(parents=True)
    source.rename(target)
    assert run_sync(sync, tmp_path) == 0
    entry = suite_by_id(read_manifest(tmp_path), "checkout")["features"][0]
    assert entry == {
        "id": "FEAT_001_Checkout",
        "path": "features/moved/login_renamed.feature",
        "estimate_days": 0.5,
        "enabled": False,
    }


def test_test_type_is_dropped_and_second_run_is_stable(sync, tmp_path):
    """A test_type key added by hand disappears on the next run, and a further run changes nothing."""
    base_repo(tmp_path)
    run_sync(sync, tmp_path)
    edit_manifest(tmp_path, lambda data: suite_by_id(data, "checkout")["features"][0].update(test_type="AUTOMATICO"))
    assert run_sync(sync, tmp_path) == 0
    assert "test_type" not in (tmp_path / MANIFEST).read_text(encoding="utf-8")
    before = (tmp_path / MANIFEST).read_bytes()
    assert run_sync(sync, tmp_path) == 0
    assert (tmp_path / MANIFEST).read_bytes() == before


def test_suite_without_feature_files_is_removed(sync, tmp_path):
    """When every feature of a suite is gone and its folder is deleted, the suite leaves the manifest."""
    base_repo(tmp_path)
    write(tmp_path / "src/api/cart/features/cart.feature", feature("FEAT_007"))
    run_sync(sync, tmp_path)
    assert {suite["id"] for suite in read_manifest(tmp_path)["suites"]} >= {"cart", "checkout"}
    shutil.rmtree(tmp_path / "src/api/cart")
    assert run_sync(sync, tmp_path) == 0
    assert "cart" not in {suite["id"] for suite in read_manifest(tmp_path)["suites"]}


def test_manual_suite_is_only_pruned_and_does_not_claim_files(sync, tmp_path):
    """A suite with a root that is not a discovered suite keeps its entries, loses dead ones, and gets no new files."""
    base_repo(tmp_path)
    write(tmp_path / "src/e2e/checkout/features/nested.feature", feature("NESTED_1"))

    def move_nested_to_manual(data):
        """Move the nested file from the discovered suite to a manual suite rooted in a sub-folder, with one dead entry."""
        checkout = suite_by_id(data, "checkout")
        checkout["features"] = [entry for entry in checkout["features"] if entry["path"] != "features/nested.feature"]
        data["suites"].append(
            {
                "id": "manual",
                "root": "src/e2e/checkout/features",
                "features": [
                    {"id": "NESTED_1", "path": "nested.feature"},
                    {"id": "GONE_1", "path": "gone.feature"},
                ],
            }
        )

    run_sync(sync, tmp_path)
    edit_manifest(tmp_path, move_nested_to_manual)
    assert run_sync(sync, tmp_path) == 0
    manifest = read_manifest(tmp_path)
    assert [entry["id"] for entry in suite_by_id(manifest, "manual")["features"]] == ["NESTED_1"]
    checkout_paths = [entry["path"] for entry in suite_by_id(manifest, "checkout")["features"]]
    assert "features/nested.feature" not in checkout_paths


def test_hand_written_label_and_feature_order_are_preserved(sync, tmp_path):
    """A label typed by hand survives regeneration, and features are sorted by path ignoring case."""
    base_repo(tmp_path)
    write(tmp_path / "src/e2e/checkout/features/Zeta.feature", feature("Z_1"))
    write(tmp_path / "src/e2e/checkout/features/alfa.feature", feature("A_1"))
    run_sync(sync, tmp_path)
    edit_manifest(tmp_path, lambda data: suite_by_id(data, "checkout").update(label="Custom"))
    assert run_sync(sync, tmp_path) == 0
    checkout = suite_by_id(read_manifest(tmp_path), "checkout")
    assert checkout["label"] == "Custom"
    paths = [entry["path"] for entry in checkout["features"]]
    assert paths == sorted(paths, key=str.casefold)


def test_invalid_existing_manifest_fails_and_is_not_overwritten(sync, tmp_path):
    """A manifest that breaks the rules stops the run with exit code 2 and stays untouched."""
    base_repo(tmp_path)
    write(tmp_path / MANIFEST, "version: 2\nsuites: []\n")
    assert run_sync(sync, tmp_path) == 2
    assert (tmp_path / MANIFEST).read_text(encoding="utf-8") == "version: 2\nsuites: []\n"


def test_repeated_key_in_existing_manifest_is_rejected(sync, tmp_path):
    """A repeated key in the existing manifest is refused rather than silently merged."""
    base_repo(tmp_path)
    write(tmp_path / MANIFEST, "version: 1\nversion: 1\nsuites: []\n")
    assert run_sync(sync, tmp_path) == 2


# ---------------------------------------------------------------- emission


def test_paths_with_spaces_apostrophes_and_accents_round_trip(sync, tmp_path):
    """Paths are double-quoted, keep accents and apostrophes, and parse back to the same value."""
    name = "FEAT_005 - Checkout dell'EC è più.feature"
    base_repo(tmp_path)
    write(tmp_path / "src/e2e/checkout/features" / name, feature("FEAT_005_Checkout"))
    assert run_sync(sync, tmp_path) == 0
    text = (tmp_path / MANIFEST).read_text(encoding="utf-8")
    assert f'path: "features/{name}"' in text
    paths = [entry["path"] for entry in read_manifest(tmp_path)["suites"][0]["features"]]
    assert f"features/{name}" in paths


def test_quote_escapes_backslash_and_double_quote(sync):
    """Backslashes and double quotes are escaped inside the YAML double-quoted scalar."""
    assert sync._quote('a"b\\c') == '"a\\"b\\\\c"'


def test_render_writes_enabled_only_when_false_and_no_test_type(sync):
    """Only 'enabled: false' is written, estimates keep their decimal point, and no test_type appears."""
    suites = [
        {"id": "a", "root": "src/x", "features": [{"id": "F", "path": "features/f.feature"}]},
        {
            "id": "b",
            "root": "src/y",
            "enabled": False,
            "features": [{"id": "G", "path": "features/g.feature", "enabled": False, "estimate_days": 1.5}],
        },
    ]
    text = sync.render_manifest(suites)
    assert text.endswith("\n") and not text.endswith("\n\n")
    assert "\r" not in text
    yaml_lines = [line for line in text.splitlines() if not line.lstrip().startswith("#")]
    assert sum(1 for line in yaml_lines if line.strip() == "enabled: false") == 2
    assert "estimate_days: 1.5" in text
    assert "test_type" not in text
    assert sync.validate_manifest(yaml.safe_load(text)) == []


# ---------------------------------------------------------------- validation


def valid_manifest() -> dict:
    """Return a minimal manifest that passes every rule, as a fresh dictionary."""
    return {
        "version": 1,
        "suites": [
            {"id": "wisp", "root": "src/integration/wisp", "features": [{"id": "F_1", "path": "features/a.feature"}]}
        ],
    }


def test_valid_manifest_has_no_errors(sync):
    """The baseline manifest used by the validation cases is itself valid."""
    assert sync.validate_manifest(valid_manifest()) == []


VALIDATION_CASES = [
    ("unknown top-level key", lambda d: d.update(extra=1)),
    ("version other than 1", lambda d: d.update(version=2)),
    ("suite id with uppercase", lambda d: d["suites"][0].update(id="Wisp")),
    ("suite id duplicated ignoring case", lambda d: d["suites"].append(
        {"id": "WISP", "root": "src/other", "features": [{"id": "X", "path": "features/x.feature"}]})),
    ("feature id with a dot", lambda d: d["suites"][0]["features"][0].update(id="F.1")),
    ("feature id duplicated ignoring case", lambda d: d["suites"][0]["features"].append(
        {"id": "f_1", "path": "features/b.feature"})),
    ("path with '..'", lambda d: d["suites"][0]["features"][0].update(path="features/../a.feature")),
    ("path with a backslash", lambda d: d["suites"][0]["features"][0].update(path="features\\a.feature")),
    ("path with '//'", lambda d: d["suites"][0]["features"][0].update(path="features//a.feature")),
    ("path without .feature", lambda d: d["suites"][0]["features"][0].update(path="features/a.txt")),
    ("path with a leading slash", lambda d: d["suites"][0]["features"][0].update(path="/features/a.feature")),
    ("test_type present", lambda d: d["suites"][0]["features"][0].update(test_type="AUTOMATICO")),
    ("estimate above 365", lambda d: d["suites"][0]["features"][0].update(estimate_days=365.01)),
    ("estimate with 3 decimals", lambda d: d["suites"][0]["features"][0].update(estimate_days=1.234)),
    ("negative estimate", lambda d: d["suites"][0]["features"][0].update(estimate_days=-1)),
    ("enabled given as text", lambda d: d["suites"][0].update(enabled="false")),
    ("no enabled suite", lambda d: d["suites"][0].update(enabled=False)),
    ("full path repeated in another suite", lambda d: d["suites"].append(
        {"id": "other", "root": "src/integration/wisp", "features": [{"id": "Y", "path": "features/a.feature"}]})),
]


@pytest.mark.parametrize("mutate", [case[1] for case in VALIDATION_CASES], ids=[case[0] for case in VALIDATION_CASES])
def test_each_rule_violation_is_reported(sync, mutate):
    """Every rule of the manifest contract produces at least one error when broken."""
    data = valid_manifest()
    mutate(data)
    assert sync.validate_manifest(data) != []


# ---------------------------------------------------------------- command line


def test_check_reports_drift_without_writing(sync, tmp_path):
    """--check returns 0 when the manifest matches, and 1 after a new feature appears, without writing."""
    base_repo(tmp_path)
    assert run_sync(sync, tmp_path) == 0
    assert run_sync(sync, tmp_path, "--check") == 0
    write(tmp_path / "src/e2e/checkout/features/extra.feature", feature("FEAT_004_Checkout"))
    before = (tmp_path / MANIFEST).read_bytes()
    assert run_sync(sync, tmp_path, "--check") == 1
    assert (tmp_path / MANIFEST).read_bytes() == before


def test_dry_run_does_not_write(sync, tmp_path):
    """--dry-run prints the summary and leaves no manifest behind."""
    base_repo(tmp_path)
    assert run_sync(sync, tmp_path, "--dry-run") == 0
    assert not (tmp_path / MANIFEST).exists()


def test_second_consecutive_run_does_not_modify_the_file(sync, tmp_path, capsys):
    """Running twice in a row writes the same bytes and reports the manifest as unchanged the second time."""
    base_repo(tmp_path)
    run_sync(sync, tmp_path)
    first = (tmp_path / MANIFEST).read_bytes()
    capsys.readouterr()
    assert run_sync(sync, tmp_path) == 0
    assert (tmp_path / MANIFEST).read_bytes() == first
    assert "manifest unchanged" in capsys.readouterr().out


# ---------------------------------------------------------------- real repository


@pytest.mark.skipif(not (REPO_ROOT / "src").is_dir(), reason="src/ is not part of this checkout")
def test_real_repository_produces_the_expected_manifest_in_memory(sync):
    """On the real src/ tree the result has 13 suites, 57 features, 3 enabled suites and valid unique ids."""
    discovered = sync.discover_suites(REPO_ROOT)
    registry = sync.load_registry(REPO_ROOT / REGISTRY)
    suites, _changes = sync.reconcile_suites([], discovered, REPO_ROOT, registry)
    assert len(suites) == 13
    assert sum(len(suite["features"]) for suite in suites) == 57
    assert sorted(suite["id"] for suite in suites if suite.get("enabled", True)) == ["checkout", "fdr3", "wisp"]
    assert sync.validate_manifest({"version": 1, "suites": suites}) == []
    for suite in suites:
        ids = [entry["id"].casefold() for entry in suite["features"]]
        assert len(ids) == len(set(ids))
        for entry in suite["features"]:
            assert (REPO_ROOT / suite["root"] / entry["path"]).is_file()
