#!/usr/bin/env python3
"""Generate and maintain the AI synopses of the Gherkin feature files.

The script reads the manifest written by gherkin_manifest_sync.py and cleans each
feature file (tags and comments are never sent to the model). It asks Gemini for
missing synopses and for changed feature text when the feature belongs to the
merged PR. Results go to .github/gherkin-synopses.json, keyed by suite id and
feature id. Explicit published and pending-review edits take precedence over AI generation.

Exit codes: 0 success, nothing to do, or no GEMINI_API_KEY (AI generation is skipped);
1 when at least one feature failed (the file still holds the progress made);
2 on an input, configuration or file error; publication must not proceed.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Callable

import yaml

SCHEMA_VERSION = 1
PROMPT_VERSION = "1"
DEFAULT_MANIFEST = ".github/gherkin-manifest.yml"
DEFAULT_SYNOPSES = ".github/gherkin-synopses.json"
DEFAULT_PROMPT_TEMPLATE = ".github/templates/feature-synopsis-prompt.txt"
DEFAULT_MAX_CALLS = 60
DEFAULT_PAUSE_SECONDS = 2.0
DEFAULT_MAX_OUTPUT_TOKENS = 1024
DEFAULT_THINKING_LEVEL = "low"
DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MAX_WORDS_CAP = 80
MAX_CONSECUTIVE_FAILURES = 3
REQUIRED_PLACEHOLDERS = ("{feature_text}", "{max_words}")
ENGINE_MODULE_NAME = "gemini_analysis"
ENGINE_PATH = Path(__file__).resolve().parent / "gemini_analysis.py"

EXIT_OK = 0
EXIT_FAILURES = 1
EXIT_CONFIG = 2

DOCSTRING_DELIMITERS = ('"""', "```")
LABEL_PATTERN = re.compile(r"^\*{0,2}sinossi\*{0,2}\s*:\*{0,2}\s*", re.IGNORECASE)
NUMBERED_LINE_PATTERN = re.compile(r"\d+\.")
LIST_MARKERS = ("-", "*", "#")
SCENARIO_PATTERN = re.compile(
    r"^\s*(?:scenario(?:\s+(?:outline|template))?|schema\s+dello\s+scenario|esempio|example)\s*:",
    re.IGNORECASE,
)
HASH_PATTERN = re.compile(r"sha256:[0-9a-f]{64}")
QUOTE_PAIRS = {'"': '"', "'": "'", "«": "»", "“": "”", "‘": "’", "`": "`"}

Generator = Callable[..., tuple[str, dict[str, Any], str]]


class SynopsisError(Exception):
    """A configuration or input problem: the run stops with exit code 2 and no file is overwritten."""


class SynopsisRejected(ValueError):
    """A generated text that breaks a synopsis rule; the message names the rule."""


@dataclass(frozen=True)
class Engine:
    """The functions of gemini_analysis.py that this script reuses; `generate` can be replaced in tests."""

    generate: Generator
    finish_reason: Callable[[dict[str, Any]], str]
    format_usage: Callable[[dict[str, Any]], str]
    parse_model_limits: Callable[[str], dict[str, dict[str, int]]]


@dataclass(frozen=True)
class ManifestFeature:
    """A feature listed in the manifest, with its full repository path."""

    suite_id: str
    feature_id: str
    path: str


@dataclass(frozen=True)
class SynopsisDocument:
    """The synopses already stored in the synopses file, keyed by (suite id, feature id)."""

    prompt_version: str | None
    entries: dict[tuple[str, str], dict[str, Any]]


@dataclass(frozen=True)
class Target:
    """A feature that needs a new synopsis, with the cleaned text and the word limit for its prompt."""

    key: tuple[str, str]
    path: str
    cleaned: str
    scenarios: int
    max_words: int
    content_hash: str
    reason: str


@dataclass
class Plan:
    """What a run decides before any AI call: targets, entries to keep, and the notes to print."""

    feature_total: int
    prompt_version: str
    targets: list[Target]
    entries: dict[tuple[str, str], dict[str, Any]]
    removed: list[tuple[str, str]]
    kept: int
    edited_in_pr: int
    newer_published: int
    pending_manual: int
    skipped: list[str]


@dataclass(frozen=True)
class GenerationSettings:
    """Model chain and limits read from the environment; the API key is kept out of repr output."""

    models: list[str]
    base_url: str
    api_key: str = field(repr=False)
    max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS
    thinking_level: str = DEFAULT_THINKING_LEVEL
    model_limits: dict[str, dict[str, int]] = field(default_factory=dict)


@dataclass
class RunState:
    """Counters of the generation loop: calls made, failures in a row, usage and the reason for an early stop."""

    max_calls: int
    pause_seconds: float
    calls: int = 0
    consecutive_failures: int = 0
    last_usage: str = ""
    stop_reason: str = ""

    def has_budget(self) -> bool:
        """Tell whether one more AI call is allowed under the --max-calls cap."""
        return self.calls < self.max_calls


@dataclass(frozen=True)
class Outcome:
    """Result of one generation attempt: ok, invalid (answered but rejected), error (call failed) or deferred."""

    status: str
    synopsis: str = ""
    model: str = ""
    detail: str = ""


@dataclass(frozen=True)
class RunOptions:
    """Command-line options after parsing; relative paths are resolved against the repository root."""

    repo_root: Path
    manifest: Path
    synopses: Path
    prompt_template: Path
    max_calls: int
    pause_seconds: float
    max_output_tokens: int
    thinking_level: str
    pr_files_file: Path | None
    pr_files_count: int | None
    pr_base: str | None
    pr_head: str | None
    pr_merge: str | None
    published_base: str | None
    pending_head: str | None
    published_reviews: Path | None
    dry_run: bool


def _info(message: str) -> None:
    """Print an informational line in the format used by the job summary."""
    print(f"[INFO] {message}")


def _warn(message: str) -> None:
    """Print a warning that does not stop the run."""
    print(f"[WARN] {message}")


def _is_exact_int(value: Any, expected: int) -> bool:
    """Tell whether value is the integer expected; booleans are not accepted as integers."""
    return isinstance(value, int) and not isinstance(value, bool) and value == expected


def _split_lines(text: str) -> list[str]:
    """Split text on any line ending, normalized to LF first, so that line numbers and flags agree."""
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def load_engine() -> Engine:
    """Import gemini_analysis.py from this script's folder by file path and expose the functions used here.

    The module is registered in sys.modules before it runs, because its dataclasses resolve string
    annotations through sys.modules. sys.path is not changed. Any failure raises SynopsisError.
    """
    spec = importlib.util.spec_from_file_location(ENGINE_MODULE_NAME, ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise SynopsisError(f"cannot load {ENGINE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[ENGINE_MODULE_NAME] = module
    try:
        spec.loader.exec_module(module)
        return Engine(
            generate=module.generate_analysis,
            finish_reason=module.finish_reason,
            format_usage=module.format_usage,
            parse_model_limits=module.parse_model_limits,
        )
    except Exception as exc:  # boundary: any import-time or missing-name failure is a configuration error
        sys.modules.pop(ENGINE_MODULE_NAME, None)
        raise SynopsisError(f"cannot import {ENGINE_PATH.name}: {exc}") from exc


def _docstring_flags(lines: list[str]) -> list[bool]:
    """Mark, for each line, whether it lies in a docstring block, delimiter lines included.

    A block opens on a line that starts with a docstring delimiter and closes on the next line
    that starts with the same delimiter. Lines inside a block are content, even when they start
    with '#' or '@'. A delimiter pair on one line opens and closes the block at once.
    """
    flags: list[bool] = []
    open_delimiter: str | None = None
    for line in lines:
        stripped = line.strip()
        if open_delimiter is not None:
            flags.append(True)
            if stripped.startswith(open_delimiter):
                open_delimiter = None
            continue
        for delimiter in DOCSTRING_DELIMITERS:
            if stripped.startswith(delimiter):
                flags.append(True)
                open_delimiter = None if delimiter in stripped[len(delimiter):] else delimiter
                break
        else:
            flags.append(False)
    return flags


def clean_feature_text(raw: str) -> str:
    """Return the text sent to the model: no tag lines, no comment lines, tidy blank lines, LF endings.

    Lines whose first non-blank character is '#' or '@' are dropped unless they lie in a docstring
    block. Trailing spaces go, runs of blank lines become one, leading and trailing blank lines are
    removed. Comments after code are kept, because they are rare and not requested to go.
    """
    text = raw[1:] if raw.startswith("﻿") else raw
    lines = _split_lines(text)
    kept: list[str] = []
    for line, in_docstring in zip(lines, _docstring_flags(lines)):
        if not in_docstring and line.lstrip().startswith(("#", "@")):
            continue
        kept.append(line.rstrip())
    collapsed: list[str] = []
    for line in kept:
        if line == "" and (not collapsed or collapsed[-1] == ""):
            continue
        collapsed.append(line)
    while collapsed and collapsed[-1] == "":
        collapsed.pop()
    while collapsed and collapsed[0] == "":
        collapsed.pop(0)
    return "\n".join(collapsed)


def count_scenarios(cleaned: str) -> int:
    """Count the scenarios of a feature text: Scenario, Scenario Outline (once), Esempio and Example lines outside docstrings.

    Example rows ('Esempi:' and '|' lines) are not counted, so an outline counts as one scenario.
    Commented-out lines are not counted either, because they have no scenario keyword at the start.
    """
    lines = _split_lines(cleaned)
    return sum(
        1
        for line, in_docstring in zip(lines, _docstring_flags(lines))
        if not in_docstring and SCENARIO_PATTERN.match(line)
    )


def max_words_for(scenario_count: int) -> int:
    """Return the word limit P(n) = min(80, (330 + 50 * (n - 1)) // 11) for n scenarios.

    Integer arithmetic gives the same result as the rounded-down formula 30 + 50/11 * (n - 1).
    A count of 0 is treated as 1; a negative count is an error.
    """
    if scenario_count < 0:
        raise ValueError(f"the scenario count cannot be negative: {scenario_count}")
    scenarios = scenario_count if scenario_count > 0 else 1
    return min(MAX_WORDS_CAP, (330 + 50 * (scenarios - 1)) // 11)


def compute_content_hash(cleaned: str, prompt_version: str) -> str:
    """Return 'sha256:' and the hex digest of the prompt version, an empty line and the cleaned text, in UTF-8."""
    payload = f"{prompt_version}\n\n{cleaned}".encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def build_prompt(template: str, cleaned: str, max_words: int) -> str:
    """Fill both placeholders of the prompt template; the word limit goes first so feature text is never rescanned."""
    return template.replace("{max_words}", str(max_words)).replace("{feature_text}", cleaned)


def retry_instruction(max_words: int) -> str:
    """Return the line appended to the prompt after an invalid answer, with a limit tighter than the first one."""
    limit = max(20, max_words - 10)
    return (
        f"Il tentativo precedente superava il limite o il formato: scrivi al massimo {limit} parole "
        "in un solo paragrafo, senza elenchi."
    )


def _strip_enclosing_quotes(text: str) -> str:
    """Remove one pair of quotes only when it wraps the whole text; otherwise return the text unchanged."""
    if len(text) >= 2 and text[0] in QUOTE_PAIRS and text[-1] == QUOTE_PAIRS[text[0]]:
        return text[1:-1].strip()
    return text


def _unwrap_lines(raw: str) -> list[str]:
    """Remove the 'Sinossi:' label and enclosing quotes, then return the non-blank stripped lines."""
    text = LABEL_PATTERN.sub("", raw.strip(), count=1).strip()
    text = _strip_enclosing_quotes(text)
    return [line.strip() for line in text.splitlines() if line.strip()]


def normalize_synopsis(raw: str) -> str:
    """Return the synopsis as a single line of single-spaced text, without label, quotes or line breaks."""
    return " ".join(" ".join(_unwrap_lines(raw)).split())


def validate_synopsis(raw: str, max_words: int) -> str:
    """Return the normalized synopsis, or raise SynopsisRejected when the text breaks a rule.

    Rules: the text is not empty; no line starts like a list item or heading ('-', '*', '#' or 'N.');
    no '@' appears anywhere (tags); the text has at most max_words words. Text is never truncated.
    """
    lines = _unwrap_lines(raw)
    if not lines:
        raise SynopsisRejected("the answer is empty")
    for line in lines:
        if line.startswith(LIST_MARKERS) or NUMBERED_LINE_PATTERN.match(line):
            raise SynopsisRejected("the answer contains a list or heading line")
    if any("@" in line for line in lines):
        raise SynopsisRejected("the answer contains '@'")
    text = normalize_synopsis(raw)
    words = len(text.split())
    if words > max_words:
        raise SynopsisRejected(f"the answer has {words} words, the limit is {max_words}")
    return text


def read_feature_text(path: Path) -> str:
    """Read a feature file as UTF-8 (a byte order mark is tolerated) and return its cleaned text."""
    return clean_feature_text(path.read_text(encoding="utf-8-sig"))


def _text_field(mapping: dict[str, Any], key: str, where: str) -> str:
    """Return a required non-empty text field, or raise SynopsisError naming where it was expected."""
    value = mapping.get(key)
    if not isinstance(value, str) or not value:
        raise SynopsisError(f"{where}: '{key}' must be a non-empty text")
    return value


def load_manifest_features(manifest_path: Path) -> list[ManifestFeature]:
    """Read the manifest with yaml.safe_load and list each feature with its full path.

    The checks are defensive only (the manifest sync script validates the file in
    depth). Raises SynopsisError when the file is missing, unreadable, not YAML,
    has duplicate paths, or has an unexpected shape.
    """
    if not manifest_path.is_file():
        raise SynopsisError(f"manifest not found: {manifest_path}")
    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise SynopsisError(f"manifest unreadable: {manifest_path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise SynopsisError(f"manifest is not valid YAML: {manifest_path}: {exc}") from exc
    suites = data.get("suites") if isinstance(data, dict) else None
    if not isinstance(suites, list):
        raise SynopsisError(f"manifest has no 'suites' list: {manifest_path}")
    features: list[ManifestFeature] = []
    seen: set[tuple[str, str]] = set()
    seen_paths: set[str] = set()
    for position, suite in enumerate(suites, start=1):
        if not isinstance(suite, dict):
            raise SynopsisError(f"manifest suite #{position} is not a mapping")
        suite_id = _text_field(suite, "id", f"manifest suite #{position}")
        where_suite = f"manifest suite '{suite_id}'"
        root = suite.get("root", "")
        if not isinstance(root, str):
            raise SynopsisError(f"{where_suite}: 'root' must be a text")
        root = root.rstrip("/")
        suite_features = suite.get("features")
        if not isinstance(suite_features, list):
            raise SynopsisError(f"{where_suite}: 'features' must be a list")
        for feature in suite_features:
            if not isinstance(feature, dict):
                raise SynopsisError(f"{where_suite}: a feature is not a mapping")
            feature_id = _text_field(feature, "id", where_suite)
            where_feature = f"{where_suite}, feature '{feature_id}'"
            key = (suite_id, feature_id)
            if key in seen:
                raise SynopsisError(f"{where_feature}: listed twice")
            seen.add(key)
            relative = _text_field(feature, "path", where_feature)
            full_path = f"{root}/{relative}" if root else relative
            if full_path in seen_paths:
                raise SynopsisError(f"{where_feature}: path '{full_path}' listed twice")
            seen_paths.add(full_path)
            features.append(ManifestFeature(suite_id, feature_id, full_path))
    return features


def load_changed_features(path: Path | None, expected_count: int | None) -> dict[str, str]:
    """Map current feature paths to their previous paths from complete GitHub PR metadata."""
    if path is None:
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise SynopsisError(f"PR file list unreadable or invalid: {path}: {exc}") from exc
    if not isinstance(data, list) or any(not isinstance(page, list) for page in data):
        raise SynopsisError(f"PR file list must be an array of pages: {path}")
    files = [item for page in data for item in page]
    if len(files) != expected_count:
        raise SynopsisError(f"PR file list is incomplete: expected {expected_count}, got {len(files)}")
    changed: dict[str, str] = {}
    for item in files:
        if not isinstance(item, dict):
            raise SynopsisError(f"PR file list contains a non-object entry: {path}")
        filename = item.get("filename")
        status = item.get("status")
        if not isinstance(filename, str) or not filename or not isinstance(status, str) or not status:
            raise SynopsisError(f"PR file list contains an entry without filename or status: {path}")
        if status != "removed" and filename.startswith("src/") and filename.endswith(".feature"):
            previous = item.get("previous_filename", filename)
            if not isinstance(previous, str) or not previous:
                raise SynopsisError(f"PR file list contains an invalid previous filename: {path}")
            changed[filename] = previous
    return changed


def _check_entry(entry: Any, where: str) -> dict[str, Any]:
    """Validate one synopsis entry against the schema, or raise SynopsisError."""
    if not isinstance(entry, dict):
        raise SynopsisError(f"{where}: the entry is not a mapping")
    for key in ("path", "content_hash", "model", "synopsis"):
        if not isinstance(entry.get(key), str):
            raise SynopsisError(f"{where}: '{key}' must be a text")
    if not HASH_PATTERN.fullmatch(entry["content_hash"]):
        raise SynopsisError(f"{where}: 'content_hash' must be 'sha256:' and 64 hexadecimal digits")
    if "prompt_version" in entry and not (
        isinstance(entry["prompt_version"], str) and entry["prompt_version"]
    ):
        raise SynopsisError(f"{where}: 'prompt_version' must be a non-empty text")
    return entry


def load_synopses_file(path: Path) -> SynopsisDocument:
    """Read the synopses file: a missing file gives an empty document, an invalid one raises SynopsisError.

    An invalid file is never rewritten; the caller stops with exit code 2 and leaves it as it is.
    """
    if not path.is_file():
        return SynopsisDocument(prompt_version=None, entries={})
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, ValueError) as exc:
        raise SynopsisError(f"synopses file is not valid JSON, left untouched: {path}: {exc}") from exc
    return parse_synopses(text, str(path))


def parse_synopses(text: str, source: str) -> SynopsisDocument:
    """Parse and validate a current or historical synopsis document without writing it."""
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise SynopsisError(f"synopses file is not valid JSON, left untouched: {source}: {exc}") from exc
    if not isinstance(data, dict) or not _is_exact_int(data.get("version"), SCHEMA_VERSION):
        raise SynopsisError(f"synopses file has an unknown 'version', left untouched: {source}")
    prompt_version = data.get("prompt_version")
    suites = data.get("suites")
    if not isinstance(prompt_version, str) or not prompt_version or not isinstance(suites, dict):
        raise SynopsisError(f"synopses file has an invalid shape, left untouched: {source}")
    entries: dict[tuple[str, str], dict[str, Any]] = {}
    for suite_id, features in suites.items():
        if not isinstance(features, dict):
            raise SynopsisError(f"synopses suite '{suite_id}' is not a mapping, left untouched: {source}")
        for feature_id, entry in features.items():
            where = f"synopsis '{suite_id}/{feature_id}'"
            entries[(suite_id, feature_id)] = _check_entry(entry, where)
    return SynopsisDocument(prompt_version=prompt_version, entries=entries)


def read_revision_file(repo_root: Path, revision: str, path: str) -> str | None:
    """Read a Git blob without changing the worktree; only a genuinely absent path returns None."""
    try:
        listed = subprocess.run(
            ["git", "--no-pager", "ls-tree", "-z", "--name-only", revision, "--", path],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True,
        )
        if not listed.stdout:
            return None
        blob = subprocess.run(
            ["git", "--no-pager", "show", f"{revision}:{path}"],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8-sig", check=True,
        )
    except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        raise SynopsisError(f"cannot read PR snapshot {revision}:{path}") from exc
    return blob.stdout


def index_synopses_by_path(
    document: SynopsisDocument,
) -> dict[tuple[str, str], tuple[tuple[str, str], dict[str, Any]]]:
    """Index entries by suite and path, rejecting ambiguous identities."""
    indexed: dict[tuple[str, str], tuple[tuple[str, str], dict[str, Any]]] = {}
    for key, entry in document.entries.items():
        path_key = (key[0], entry["path"])
        if path_key in indexed:
            raise SynopsisError(f"multiple synopses for suite '{key[0]}' and path '{entry['path']}'")
        indexed[path_key] = (key, entry)
    return indexed


def synopsis_text_changes(
    before: SynopsisDocument, after: SynopsisDocument, features: list[ManifestFeature],
) -> dict[tuple[str, str], str]:
    """Map synopsis text edits to current features and the paths in the later snapshot."""
    before_by_path = index_synopses_by_path(before)
    after_by_path = index_synopses_by_path(after)
    changed_keys: dict[tuple[str, str], str] = {}
    changed_paths: set[tuple[str, str]] = set()
    matched: set[tuple[str, str]] = set()
    for key, entry in after.entries.items():
        previous = before_by_path.get((key[0], entry["path"]))
        if previous is None:
            same_id = before.entries.get(key)
            if same_id is not None and (key[0], same_id["path"]) not in after_by_path:
                previous = (key, same_id)
        if previous is not None:
            matched.add(previous[0])
            if previous[1]["synopsis"] == entry["synopsis"]:
                continue
        changed_keys[key] = entry["path"]
        changed_paths.add((key[0], entry["path"]))
    for key, entry in before.entries.items():
        if key not in matched:
            changed_keys[key] = entry["path"]
            changed_paths.add((key[0], entry["path"]))
    edited: dict[tuple[str, str], str] = {}
    manifest_paths = {(feature.suite_id, feature.path) for feature in features}
    for feature in features:
        key = (feature.suite_id, feature.feature_id)
        path_key = (feature.suite_id, feature.path)
        if path_key not in changed_paths and (
            key not in changed_keys or (feature.suite_id, changed_keys[key]) in manifest_paths
        ):
            continue
        head_match = after_by_path.get(path_key)
        head_entry = head_match[1] if head_match is not None else after.entries.get(key)
        edited[key] = head_entry["path"] if head_entry is not None else feature.path
    return edited


def load_revision_synopses(repo_root: Path, revision: str, path: str) -> SynopsisDocument:
    """Read and validate a synopsis document at a commit, allowing an absent file."""
    text = read_revision_file(repo_root, revision, path)
    return SynopsisDocument(None, {}) if text is None else parse_synopses(text, f"{revision}:{path}")


def load_pr_changes(
    repo_root: Path, options: RunOptions, features: list[ManifestFeature],
) -> tuple[set[str], dict[tuple[str, str], str | None]]:
    """Compare PR snapshots and retain edited features' PR-head text as the hash baseline."""
    metadata = (
        _resolve(repo_root, options.pr_files_file)
        if options.pr_files_file is not None else None
    )
    paths = load_changed_features(metadata, options.pr_files_count)
    if options.pr_base is None or options.pr_head is None:
        return set(), {}
    try:
        synopsis_path = _resolve(repo_root, options.synopses).relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise SynopsisError("the PR synopses file must be inside the repository") from exc
    before = load_revision_synopses(repo_root, options.pr_base, synopsis_path)
    after = load_revision_synopses(repo_root, options.pr_head, synopsis_path)
    edited: dict[tuple[str, str], str | None] = {}
    for key, head_path in synopsis_text_changes(before, after, features).items():
        text = read_revision_file(repo_root, options.pr_head, head_path)
        edited[key] = clean_feature_text(text) if text is not None else None
    changed_features: set[str] = set()
    for path, previous in paths.items():
        old_text = read_revision_file(repo_root, options.pr_base, previous)
        new_text = read_revision_file(repo_root, options.pr_head, path)
        if new_text is None:
            raise SynopsisError(f"PR head does not contain listed feature: {path}")
        if old_text is None or clean_feature_text(old_text) != clean_feature_text(new_text):
            changed_features.add(path)
    return changed_features, edited


def load_published_overrides(
    repo_root: Path,
    options: RunOptions,
    features: list[ManifestFeature],
    edited_synopses: dict[tuple[str, str], str | None],
) -> tuple[
    dict[tuple[str, str], dict[str, Any] | None],
    set[tuple[str, str]],
    str | None,
    dict[tuple[str, str], tuple[str, str]],
]:
    """Protect published text edits after the triggering merge, including edits later reverted."""
    if options.pr_merge is None or options.published_base is None:
        return {}, set(), None, {}
    try:
        synopsis_path = _resolve(repo_root, options.synopses).relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise SynopsisError("the published synopses file must be inside the repository") from exc
    try:
        ancestor = subprocess.run(
            ["git", "--no-pager", "merge-base", "--is-ancestor", options.pr_merge, options.published_base],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=False,
        )
        if ancestor.returncode == 1:
            raise SynopsisError("the triggering PR merge is not an ancestor of the published base")
        if ancestor.returncode != 0:
            raise SynopsisError("cannot verify the triggering PR merge against the published base")
        history = subprocess.run(
            [
                "git", "--no-pager", "rev-list", "--first-parent", "--reverse", "--ancestry-path",
                f"{options.pr_merge}..{options.published_base}", "--", synopsis_path,
            ],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True,
        )
    except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        raise SynopsisError("cannot inspect published synopsis history") from exc
    reviews: dict[str, list[str]] = {}
    if options.published_reviews is not None:
        path = _resolve(repo_root, options.published_reviews)
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as exc:
            raise SynopsisError(f"published review metadata unreadable or invalid: {path}") from exc
        revisions = set(history.stdout.splitlines())
        if not isinstance(data, dict) or any(
            revision not in revisions
            or not isinstance(commits, list)
            or any(
                not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit)
                for commit in commits
            )
            for revision, commits in data.items()
        ):
            raise SynopsisError("published review metadata contains invalid revisions or commits")
        reviews = data
    source = load_revision_synopses(repo_root, options.pr_merge, synopsis_path)
    previous = source
    newer: set[tuple[str, str]] = set()
    references: dict[tuple[str, str], tuple[str, str]] = {}
    for revision in history.stdout.splitlines():
        current = load_revision_synopses(repo_root, revision, synopsis_path)
        changes: dict[tuple[str, str], str] = {}
        if revision in reviews:
            for commit in reviews[revision]:
                before_review = load_revision_synopses(repo_root, f"{commit}^1", synopsis_path)
                after_review = load_revision_synopses(repo_root, commit, synopsis_path)
                changes.update(synopsis_text_changes(before_review, after_review, features))
        else:
            changes = synopsis_text_changes(previous, current, features)
        newer.update(changes)
        references.update({key: (revision, path) for key, path in changes.items()})
        previous = current
    published = load_revision_synopses(repo_root, options.published_base, synopsis_path)
    published_by_path = index_synopses_by_path(published)
    source_by_path = index_synopses_by_path(source)
    manifest_paths = {(feature.suite_id, feature.path) for feature in features}
    overrides: dict[tuple[str, str], dict[str, Any] | None] = {}
    for feature in features:
        key = (feature.suite_id, feature.feature_id)
        if key not in newer and key not in edited_synopses:
            continue
        if key not in references:
            source_match = source_by_path.get((feature.suite_id, feature.path))
            if source_match is None:
                same_id = source.entries.get(key)
                if same_id is not None and (feature.suite_id, same_id["path"]) not in manifest_paths:
                    source_match = (key, same_id)
            source_path = source_match[1]["path"] if source_match is not None else feature.path
            references[key] = (options.pr_merge, source_path)
        match = published_by_path.get((feature.suite_id, feature.path))
        if match is None:
            same_id = published.entries.get(key)
            if same_id is not None and (feature.suite_id, same_id["path"]) not in manifest_paths:
                match = (key, same_id)
        overrides[key] = match[1] if match is not None else None
    return overrides, newer, published.prompt_version, references


def load_pending_manual_edits(
    repo_root: Path, options: RunOptions, features: list[ManifestFeature],
) -> set[tuple[str, str]]:
    """Find synopsis texts edited by non-bot commits on the cumulative PR branch."""
    if options.published_base is None or options.pending_head is None:
        return set()
    try:
        synopsis_path = _resolve(repo_root, options.synopses).relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise SynopsisError("the pending synopses file must be inside the repository") from exc
    try:
        ancestor = subprocess.run(
            ["git", "--no-pager", "merge-base", "--is-ancestor", options.published_base, options.pending_head],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=False,
        )
        if ancestor.returncode == 1:
            raise SynopsisError("the published base is not an ancestor of the pending branch")
        if ancestor.returncode != 0:
            raise SynopsisError("cannot verify the pending branch against the published base")
        history = subprocess.run(
            [
                "git", "--no-pager", "rev-list", "--first-parent", "--reverse",
                f"{options.published_base}..{options.pending_head}", "--", synopsis_path,
            ],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True,
        )
        manual: set[tuple[str, str]] = set()
        for revision in history.stdout.splitlines():
            author = subprocess.run(
                ["git", "--no-pager", "show", "-s", "--format=%an%x00%ae", revision],
                cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True,
            ).stdout.rstrip("\n")
            if author == "github-actions[bot]\0github-actions[bot]@users.noreply.github.com":
                continue
            before = load_revision_synopses(repo_root, f"{revision}^1", synopsis_path)
            after = load_revision_synopses(repo_root, revision, synopsis_path)
            manual.update(synopsis_text_changes(before, after, features))
    except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        raise SynopsisError("cannot inspect pending synopsis review edits") from exc
    return manual


def load_prompt_template(path: Path) -> str:
    """Read the prompt template and check that it has both placeholders; raise SynopsisError otherwise."""
    if not path.is_file():
        raise SynopsisError(f"prompt template not found: {path}")
    try:
        template = path.read_text(encoding="utf-8-sig")
    except (OSError, ValueError) as exc:
        raise SynopsisError(f"prompt template unreadable: {path}: {exc}") from exc
    missing = [placeholder for placeholder in REQUIRED_PLACEHOLDERS if placeholder not in template]
    if missing:
        raise SynopsisError(f"prompt template {path} lacks the placeholders {', '.join(missing)}")
    return template


def make_entry(
    path: str,
    content_hash: str,
    model: str,
    synopsis: str,
    prompt_version: str | None = None,
) -> dict[str, Any]:
    """Build one synopsis entry, including a prompt version override when needed."""
    entry: dict[str, Any] = {"path": path, "content_hash": content_hash, "model": model, "synopsis": synopsis}
    if prompt_version is not None:
        entry["prompt_version"] = prompt_version
    return entry


def _carry_over(current: dict[str, Any], path: str) -> dict[str, Any]:
    """Copy an existing entry to a path, keeping its synopsis, hash and prompt version."""
    return make_entry(
        path,
        current["content_hash"],
        current["model"],
        current["synopsis"],
        prompt_version=current.get("prompt_version"),
    )


def plan_work(
    repo_root: Path,
    features: list[ManifestFeature],
    existing: SynopsisDocument,
    changed_features: set[str],
    edited_synopses: dict[tuple[str, str], str | None] | None = None,
    published_overrides: dict[tuple[str, str], dict[str, Any] | None] | None = None,
    newer_published: set[tuple[str, str]] | None = None,
    published_prompt_version: str | None = None,
    pending_manual: set[tuple[str, str]] | None = None,
    override_references: dict[tuple[str, str], tuple[str, str]] | None = None,
) -> Plan:
    """Decide which features need a new synopsis and which entries stay, without any AI call.

    Missing synopses are generated for every suite. Existing ones are regenerated
    only when their feature's cleaned text changed in the PR. A synopsis edited
    in that PR always takes precedence. Missing or unreadable files keep old entries.
    """
    manifest_paths = {(feature.suite_id, feature.path) for feature in features}
    existing_by_path = index_synopses_by_path(existing)
    if edited_synopses is None:
        edited_synopses = {}
    if published_overrides is None:
        published_overrides = {}
    if newer_published is None:
        newer_published = set()
    if pending_manual is None:
        pending_manual = set()
    if override_references is None:
        override_references = {}
    prompt_version = existing.prompt_version if existing.prompt_version is not None else PROMPT_VERSION
    matched: set[tuple[str, str]] = set()
    entries: dict[tuple[str, str], dict[str, Any]] = {}
    targets: list[Target] = []
    skipped: list[str] = []
    kept = edited_in_pr = newer_count = pending_count = 0
    for feature in features:
        key = (feature.suite_id, feature.feature_id)
        label = f"'{feature.suite_id}/{feature.feature_id}'"
        match = existing_by_path.get((feature.suite_id, feature.path))
        if match is None:
            same_id = existing.entries.get(key)
            if same_id is not None and (feature.suite_id, same_id["path"]) not in manifest_paths:
                match = (key, same_id)
        current = match[1] if match is not None else None
        if match is not None:
            matched.add(match[0])
        if key in edited_synopses or key in newer_published or key in pending_manual:
            edited_in_pr += int(key in edited_synopses)
            newer_count += int(key in newer_published)
            pending_count += int(key in pending_manual)
            if key in published_overrides:
                published = published_overrides[key]
                if key in pending_manual and (
                    (current["synopsis"] if current is not None else None)
                    != (published["synopsis"] if published is not None else None)
                ):
                    raise SynopsisError(
                        f"feature {label}: published and pending manual synopsis edits differ; resolve them first"
                    )
                reference = override_references.get(key)
                feature_path = repo_root / feature.path
                if reference is not None and current is not None and feature_path.is_file():
                    old_text = read_revision_file(repo_root, *reference)
                    if old_text is not None:
                        try:
                            latest_text = read_feature_text(feature_path)
                        except (OSError, ValueError) as exc:
                            raise SynopsisError(f"feature {label}: cannot verify the pending synopsis") from exc
                        version = current.get("prompt_version", prompt_version)
                        if (
                            latest_text
                            and clean_feature_text(old_text) != latest_text
                            and current["content_hash"] == compute_content_hash(latest_text, version)
                        ):
                            entries[key] = _carry_over(current, feature.path)
                            continue
                current = published_overrides[key]
            if current is not None:
                entry = _carry_over(current, feature.path)
                if key in published_overrides:
                    version = current.get("prompt_version", published_prompt_version)
                    if version is not None and version != prompt_version:
                        entry["prompt_version"] = version
                pr_text = edited_synopses.get(key) if key not in newer_published else None
                if pr_text is not None:
                    entry["content_hash"] = compute_content_hash(
                        pr_text, entry.get("prompt_version", prompt_version)
                    )
                entries[key] = entry
            continue
        file_path = repo_root / feature.path
        cleaned = ""
        if not file_path.is_file():
            skipped.append(f"feature {label}: file '{feature.path}' not found, skipped")
        else:
            try:
                cleaned = read_feature_text(file_path)
            except (OSError, ValueError) as exc:
                skipped.append(f"feature {label}: file unreadable ({exc}), skipped")
            else:
                if not cleaned:
                    skipped.append(f"feature {label}: no text left after cleaning, skipped")
        if not cleaned:
            if current is not None:
                entries[key] = _carry_over(current, current["path"])
            continue
        content_hash = compute_content_hash(cleaned, PROMPT_VERSION)
        if current is None:
            reason = "new"
        elif not current["synopsis"].strip():
            reason = "empty synopsis"
        elif (
            feature.path in changed_features
            and current["content_hash"]
            != compute_content_hash(cleaned, current.get("prompt_version", prompt_version))
        ):
            reason = "text changed in PR"
        else:
            kept += 1
            entries[key] = _carry_over(current, feature.path)
            continue
        if current is not None:
            # A failed or deferred target keeps the old entry for a rerun of the same PR.
            entries[key] = _carry_over(current, feature.path)
        scenarios = count_scenarios(cleaned)
        targets.append(
            Target(
                key=key,
                path=feature.path,
                cleaned=cleaned,
                scenarios=scenarios,
                max_words=max_words_for(scenarios),
                content_hash=content_hash,
                reason=reason,
            )
        )
    return Plan(
        feature_total=len(features),
        prompt_version=prompt_version,
        targets=targets,
        entries=entries,
        removed=sorted(key for key in existing.entries if key not in matched),
        kept=kept,
        edited_in_pr=edited_in_pr,
        newer_published=newer_count,
        pending_manual=pending_count,
        skipped=skipped,
    )


def build_document(prompt_version: str, entries: dict[tuple[str, str], dict[str, Any]]) -> dict[str, Any]:
    """Assemble the schema of the synopses file, with suites and features in sorted order."""
    suites: dict[str, dict[str, dict[str, Any]]] = {}
    for suite_id, feature_id in sorted(entries):
        suites.setdefault(suite_id, {})[feature_id] = entries[(suite_id, feature_id)]
    return {"version": SCHEMA_VERSION, "prompt_version": prompt_version, "suites": suites}


def write_if_changed(path: Path, document: dict[str, Any]) -> bool:
    """Write the document as UTF-8 JSON (2-space indent, LF, final newline) only when the bytes differ.

    Returns True when the file was written. Write failures raise OSError to the caller.
    """
    encoded = (json.dumps(document, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    current = path.read_bytes() if path.is_file() else None
    if current == encoded:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        handle.write(encoded)
    return True


def load_generation_settings(
    options: RunOptions, api_key: str, engine: Engine
) -> GenerationSettings:
    """Read AVAILABLE_MODELS, MODEL_LIMITS and BASE_URL from the environment; the model list is required.

    Raises SynopsisError when AVAILABLE_MODELS is missing, empty or not a JSON array of names, or when
    MODEL_LIMITS is not a JSON object of limits. The API key is passed in and never printed.
    """
    raw_models = os.environ.get("AVAILABLE_MODELS", "")
    if not raw_models.strip():
        raise SynopsisError("AVAILABLE_MODELS is missing or empty")
    try:
        models = json.loads(raw_models)
    except ValueError as exc:
        raise SynopsisError(f"AVAILABLE_MODELS is not valid JSON: {exc}") from exc
    if not isinstance(models, list) or not models or not all(isinstance(m, str) and m for m in models):
        raise SynopsisError("AVAILABLE_MODELS must be a non-empty JSON array of model names")
    try:
        model_limits = engine.parse_model_limits(os.environ.get("MODEL_LIMITS", ""))
    except RuntimeError as exc:
        raise SynopsisError(str(exc)) from exc
    raw_base_url = os.environ.get("BASE_URL", "").strip()
    base_url = raw_base_url if raw_base_url else DEFAULT_BASE_URL
    return GenerationSettings(
        models=models,
        base_url=base_url,
        api_key=api_key,
        max_output_tokens=options.max_output_tokens,
        thinking_level=options.thinking_level,
        model_limits=model_limits,
    )


def _ask(
    prompt: str,
    max_words: int,
    settings: GenerationSettings,
    engine: Engine,
    state: RunState,
) -> Outcome:
    """Make one generator call and classify the answer as ok, invalid or error.

    Only a call that raised (every model failed, network trouble) counts toward the consecutive-failure
    stop; an answer that was received resets that counter, even when the answer is rejected.
    """
    if state.calls and state.pause_seconds > 0:
        time.sleep(state.pause_seconds)
    state.calls += 1
    try:
        model, response, text = engine.generate(
            prompt,
            settings.models,
            settings.max_output_tokens,
            settings.base_url,
            settings.api_key,
            thinking_level=settings.thinking_level,
            model_limits=settings.model_limits,
        )
    except (RuntimeError, OSError, http.client.HTTPException) as exc:
        state.consecutive_failures += 1
        return Outcome(status="error", detail=str(exc))
    state.consecutive_failures = 0
    usage = engine.format_usage(response)
    if usage:
        state.last_usage = usage
    if engine.finish_reason(response) == "MAX_TOKENS":
        return Outcome(status="invalid", model=model, detail="the answer was cut at the output token limit")
    try:
        synopsis = validate_synopsis(text, max_words)
    except SynopsisRejected as exc:
        return Outcome(status="invalid", model=model, detail=str(exc))
    return Outcome(status="ok", synopsis=synopsis, model=model)


def produce_synopsis(
    target: Target,
    template: str,
    settings: GenerationSettings,
    engine: Engine,
    state: RunState,
) -> Outcome:
    """Generate the synopsis of one target: one attempt, then one retry with a tighter limit if the answer is invalid.

    Returns 'deferred' without a call when the --max-calls budget is used up, before the attempt or
    before the retry. A failed retry returns the retry's outcome.
    """
    if not state.has_budget():
        return Outcome(status="deferred", detail="max-calls reached")
    prompt = build_prompt(template, target.cleaned, target.max_words)
    outcome = _ask(prompt, target.max_words, settings, engine, state)
    if outcome.status != "invalid":
        return outcome
    if not state.has_budget():
        return Outcome(status="deferred", detail="max-calls reached before the retry")
    retry_prompt = f"{prompt}\n{retry_instruction(target.max_words)}"
    return _ask(retry_prompt, target.max_words, settings, engine, state)


def generate_targets(
    plan: Plan,
    template: str,
    settings: GenerationSettings,
    engine: Engine,
    state: RunState,
    synopses_path: Path,
) -> tuple[int, int]:
    """Run the AI calls for the planned targets in manifest order; return (generated, failed) counts.

    Each success is stored in plan.entries and written at once, so progress survives a later failure.
    The loop stops at the --max-calls cap, and after MAX_CONSECUTIVE_FAILURES call failures in a row.
    Targets not reached keep their old entries; rerun the same PR to retry changes.
    """
    generated = 0
    failed = 0
    for target in plan.targets:
        label = f"'{target.key[0]}/{target.key[1]}'"
        outcome = produce_synopsis(target, template, settings, engine, state)
        if outcome.status == "deferred":
            state.stop_reason = f"max-calls ({state.max_calls}) reached"
            break
        if outcome.status == "ok":
            plan.entries[target.key] = make_entry(
                target.path,
                target.content_hash,
                outcome.model,
                outcome.synopsis,
                prompt_version=PROMPT_VERSION if PROMPT_VERSION != plan.prompt_version else None,
            )
            generated += 1
            _info(
                f"generated {label} with {outcome.model}: "
                f"{len(outcome.synopsis.split())} words, limit {target.max_words}"
            )
            write_if_changed(synopses_path, build_document(plan.prompt_version, plan.entries))
            continue
        failed += 1
        _warn(f"feature {label} not generated ({outcome.status}): {outcome.detail}")
        if state.consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            state.stop_reason = f"{MAX_CONSECUTIVE_FAILURES} call failures in a row"
            break
    return generated, failed


def report_plan(plan: Plan) -> None:
    """Print targets, retained and removed entries, and skipped files."""
    per_suite = Counter(target.key[0] for target in plan.targets)
    by_suite = ", ".join(f"{suite} {count}" for suite, count in sorted(per_suite.items()))
    suffix = f" ({by_suite})" if by_suite else ""
    _info(f"features: {plan.feature_total}; to generate: {len(plan.targets)}{suffix}")
    _info(
        f"kept: {plan.kept}; edited in PR: {plan.edited_in_pr}; "
        f"newer published edits: {plan.newer_published}; "
        f"pending review edits: {plan.pending_manual}; to remove: {len(plan.removed)}"
    )
    for target in plan.targets:
        _info(
            f"to generate '{target.key[0]}/{target.key[1]}' ({target.reason}): "
            f"up to {target.max_words} words, {target.scenarios} scenario{'' if target.scenarios == 1 else 's'}"
        )
    for suite_id, feature_id in plan.removed:
        _info(f"to remove '{suite_id}/{feature_id}': no longer in the manifest")
    for message in plan.skipped:
        _warn(message)


def print_dry_run(plan: Plan, max_calls: int) -> None:
    """Print the plan and the cleaned text of the first target; nothing is called or written."""
    report_plan(plan)
    if len(plan.targets) > max_calls:
        _info(f"only the first {max_calls} targets are generated in one run")
    if plan.targets:
        _info("cleaned text of the first feature, as sent to the model:")
        print(plan.targets[0].cleaned)
    _info("dry run: no API call, nothing written")


def validate_options(options: RunOptions) -> None:
    """Reject option values that the run cannot use, before any file is read."""
    if options.max_calls < 0:
        raise SynopsisError("--max-calls must be 0 or more")
    if options.pause_seconds < 0:
        raise SynopsisError("--pause-seconds must be 0 or more")
    if options.max_output_tokens < 1:
        raise SynopsisError("--max-output-tokens must be at least 1")
    if (options.pr_files_file is None) != (options.pr_files_count is None):
        raise SynopsisError("--pr-files-file and --pr-files-count must be supplied together")
    if options.pr_files_count is not None and options.pr_files_count < 0:
        raise SynopsisError("--pr-files-count must be 0 or more")
    if any(value is not None for value in (options.pr_base, options.pr_head, options.pr_files_file)):
        if options.pr_base is None or options.pr_head is None or options.pr_files_file is None:
            raise SynopsisError("--pr-base, --pr-head and PR file metadata must be supplied together")
        if any(not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", ref) for ref in (options.pr_base, options.pr_head)):
            raise SynopsisError("--pr-base and --pr-head must be full Git commit hashes")
    if options.pr_merge is not None and (options.published_base is None or options.pr_base is None):
        raise SynopsisError("--pr-merge requires --published-base and complete PR snapshot options")
    if options.published_reviews is not None and options.pr_merge is None:
        raise SynopsisError("--published-reviews requires --pr-merge")
    if options.pending_head is not None and options.published_base is None:
        raise SynopsisError("--pending-head requires --published-base")
    if options.published_base is not None and options.pr_merge is None and options.pending_head is None:
        raise SynopsisError("--published-base requires --pr-merge or --pending-head")
    refs = (options.pr_merge, options.published_base, options.pending_head)
    if any(ref is not None and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", ref) for ref in refs):
        raise SynopsisError("--pr-merge, --published-base and --pending-head must be full Git commit hashes")


def _resolve(repo_root: Path, value: Path) -> Path:
    """Return value unchanged when it is absolute, otherwise value relative to the repository root."""
    return value if value.is_absolute() else repo_root / value


def run(options: RunOptions, generator: Generator | None = None) -> int:
    """Run one synchronization of the synopses file and return the exit code (0, 1 or 2).

    The generator argument replaces gemini_analysis.generate_analysis (used by the tests); when it is
    None the real function is used. Nothing is called without GEMINI_API_KEY, and nothing is written
    in dry-run mode.
    """
    validate_options(options)
    engine = load_engine()
    if generator is not None:
        engine = replace(engine, generate=generator)
    repo_root = options.repo_root.resolve()
    manifest_path = _resolve(repo_root, options.manifest)
    synopses_path = _resolve(repo_root, options.synopses)
    template = load_prompt_template(_resolve(repo_root, options.prompt_template))
    features = load_manifest_features(manifest_path)
    existing = load_synopses_file(synopses_path)
    changed_features, edited_synopses = load_pr_changes(repo_root, options, features)
    overrides, newer_published, published_version, override_references = load_published_overrides(
        repo_root, options, features, edited_synopses
    )
    pending_manual = load_pending_manual_edits(repo_root, options, features)
    plan = plan_work(
        repo_root, features, existing, changed_features, edited_synopses,
        overrides, newer_published, published_version, pending_manual, override_references,
    )
    if options.dry_run:
        print_dry_run(plan, options.max_calls)
        return EXIT_OK
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key.strip():
        if overrides:
            written = write_if_changed(synopses_path, build_document(plan.prompt_version, plan.entries))
            _info(f"written {options.synopses}" if written else "synopses file unchanged")
        _info("skipped: no GEMINI_API_KEY")
        return EXIT_OK
    settings = load_generation_settings(options, api_key, engine)
    report_plan(plan)
    state = RunState(max_calls=options.max_calls, pause_seconds=options.pause_seconds)
    generated, failed = generate_targets(plan, template, settings, engine, state, synopses_path)
    deferred = len(plan.targets) - generated - failed
    written = write_if_changed(synopses_path, build_document(plan.prompt_version, plan.entries))
    _info(
        f"summary: generated {generated}, failed {failed}, deferred {deferred}, "
        f"kept {plan.kept}, edited in PR {plan.edited_in_pr}, "
        f"newer published edits {plan.newer_published}, pending review edits {plan.pending_manual}, "
        f"removed {len(plan.removed)}, AI calls {state.calls}"
    )
    if state.stop_reason:
        _warn(f"stopped early: {state.stop_reason}; rerun the same PR to retry changed features")
    if state.last_usage:
        _info(f"token usage of the last call: {state.last_usage}")
    _info(f"written {options.synopses}" if written else "synopses file unchanged")
    return EXIT_FAILURES if failed else EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser with the options of the synopsis step."""
    parser = argparse.ArgumentParser(description="Generate AI synopses for the Gherkin feature files.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="repository root (default: current folder)")
    parser.add_argument("--manifest", type=Path, default=Path(DEFAULT_MANIFEST), help="manifest to read")
    parser.add_argument("--synopses", type=Path, default=Path(DEFAULT_SYNOPSES), help="synopses file to write")
    parser.add_argument(
        "--prompt-template", type=Path, default=Path(DEFAULT_PROMPT_TEMPLATE), help="prompt template"
    )
    parser.add_argument("--max-calls", type=int, default=DEFAULT_MAX_CALLS, help="AI calls allowed per run")
    parser.add_argument(
        "--pause-seconds", type=float, default=DEFAULT_PAUSE_SECONDS, help="pause between two AI calls"
    )
    parser.add_argument(
        "--max-output-tokens", type=int, default=DEFAULT_MAX_OUTPUT_TOKENS, help="output limit, thinking included"
    )
    parser.add_argument(
        "--thinking-level", default=DEFAULT_THINKING_LEVEL, help="Gemini thinkingLevel; empty keeps the default"
    )
    parser.add_argument(
        "--pr-files-file",
        type=Path,
        help="paginated JSON from 'gh api --paginate --slurp' for the merged PR",
    )
    parser.add_argument("--pr-files-count", type=int, help="expected number of files changed by the merged PR")
    parser.add_argument("--pr-base", help="full merge-base commit hash of the PR")
    parser.add_argument("--pr-head", help="full head commit hash of the PR")
    parser.add_argument("--pr-merge", help="full commit hash produced by merging the PR")
    parser.add_argument("--published-base", help="full commit hash of main used for this run")
    parser.add_argument("--pending-head", help="full commit hash of the prepared cumulative PR branch")
    parser.add_argument("--published-reviews", type=Path, help="verified sync-PR revisions and reviewer commits as JSON")
    parser.add_argument("--completion-marker", type=Path, help="write the completed run's exit code to this file")
    parser.add_argument("--dry-run", action="store_true", help="print the plan; no API call, no write")
    return parser


def main(argv: list[str] | None = None, generator: Generator | None = None) -> int:
    """Parse the command line, run the synchronization and return the exit code.

    The generator parameter exists so that tests can avoid the network; leave it None in production.
    Configuration errors and file errors print one [ERROR] line and return 2.
    """
    args = build_parser().parse_args(argv)
    options = RunOptions(
        repo_root=args.repo_root,
        manifest=args.manifest,
        synopses=args.synopses,
        prompt_template=args.prompt_template,
        max_calls=args.max_calls,
        pause_seconds=args.pause_seconds,
        max_output_tokens=args.max_output_tokens,
        thinking_level=args.thinking_level,
        pr_files_file=args.pr_files_file,
        pr_files_count=args.pr_files_count,
        pr_base=args.pr_base,
        pr_head=args.pr_head,
        pr_merge=args.pr_merge,
        published_base=args.published_base,
        pending_head=args.pending_head,
        published_reviews=args.published_reviews,
        dry_run=args.dry_run,
    )
    try:
        result = run(options, generator=generator)
        if args.completion_marker is not None:
            args.completion_marker.write_text(f"{result}\n", encoding="utf-8")
        return result
    except (SynopsisError, OSError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return EXIT_CONFIG


if __name__ == "__main__":
    sys.exit(main())
