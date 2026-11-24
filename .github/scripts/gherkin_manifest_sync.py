#!/usr/bin/env python3
"""Keep .github/gherkin-manifest.yml aligned with the feature files under src/.

The manifest tells QA Central Hub which suites and feature files to show. This
script regenerates it from the repository tree: it discovers the .feature files
under src/<type>/<suite>/ that sit in a folder named exactly 'features', keeps the
hand-written data of entries already listed (ids, estimates, enabled flags), drops
dead entries, validates the result before writing it, and writes the file only
when its content changed.

Exit codes: 0 success or nothing to change; 1 with --check when the manifest is
out of date; 2 on error (invalid existing manifest, invalid result, I/O failure).
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

SOURCE_TYPES = ("api", "integration", "e2e")
FEATURE_SUFFIX = ".feature"
FEATURES_FOLDER = "features"
DEFAULT_MANIFEST = ".github/gherkin-manifest.yml"
DEFAULT_REGISTRY = ".github/nrt-suites.json"
MANIFEST_MAX_BYTES = 256 * 1024
MAX_ESTIMATE_DAYS = 365

SUITE_ID_PATTERN = re.compile(r"[a-z0-9_-]{1,64}")
FEATURE_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,80}")
FEATURE_KEYWORD_PATTERN = re.compile(r"(funzionalità|funzionalita|feature)\s*:", re.IGNORECASE)

ALLOWED_ROOT_KEYS = {"version", "suites"}
ALLOWED_SUITE_KEYS = {"id", "label", "root", "enabled", "features"}
ALLOWED_FEATURE_KEYS = {"id", "path", "estimate_days", "enabled"}

HEADER_LINES = [
    "# Gherkin manifest: the suites and feature files that QA Central Hub shows under",
    "# Knowledge Base > Gherkin Feature Files, with the data that only this repository can give.",
    "#",
    "# GENERATED FILE: .github/scripts/gherkin_manifest_sync.py rewrites it (workflow",
    "# .github/workflows/gherkin-manifest-sync.yml). Comments written here are lost on the next run.",
    "# Hand-editable fields: suites[].label, suites[].enabled, features[].estimate_days and",
    "# features[].enabled. Never change or reuse an id: the portal ties the data typed by hand to it.",
    "# 'enabled' is written only when it is false: a missing 'enabled' means true (the default),",
    "# for suites and for features alike. 'enabled: false' hides the suite or the single feature.",
    "# Field rules: docs/gherkin-feature-files/reference/manifest/gherkin-manifest.template.yml",
    "# in the pagopa-qa-centralhub repository.",
    "",
]


class ManifestError(Exception):
    """Invalid input, an invalid result or an unusable file; the manifest must not be written."""


@dataclass(frozen=True)
class DiscoveredSuite:
    """A suite folder under src/ that holds at least one feature file in a features folder."""

    suite_type: str
    name: str
    root: str
    directory: Path
    feature_paths: tuple[str, ...]


class _StrictLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects aliases and repeated keys, which the portal rejects too."""

    def compose_node(self, parent, index):
        """Refuse YAML aliases before composing the node."""
        if self.check_event(yaml.AliasEvent):
            raise ManifestError("YAML aliases are not allowed")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        """Refuse a mapping that repeats a key."""
        seen: set[str] = set()
        for key_node, _value_node in node.value:
            if isinstance(key_node, yaml.ScalarNode):
                if key_node.value in seen:
                    raise ManifestError(
                        f"repeated key '{key_node.value}' at line {key_node.start_mark.line + 1}"
                    )
                seen.add(key_node.value)
        return super().construct_mapping(node, deep=deep)


def _info(message: str) -> None:
    """Print an informational line in the format used by the job summary."""
    print(f"[INFO] {message}")


def _warn(message: str) -> None:
    """Print a warning that does not stop the run."""
    print(f"[WARN] {message}")


def _is_ignored_name(name: str) -> bool:
    """Tell whether a folder name is hidden or a Python cache that must not be scanned."""
    return name.startswith(".") or name == "__pycache__"


def _suite_id_from_name(name: str) -> str:
    """Turn a folder name into a suite id: lowercase, unsafe characters become '-', at most 64 characters."""
    return re.sub(r"[^a-z0-9_-]", "-", name.lower())[:64]


def _normalize_root(value: Any) -> str:
    """Return a suite root without trailing slashes; a missing root means the repository root ('')."""
    if not isinstance(value, str):
        return ""
    return value.rstrip("/")


def _join_root(root: str, path: str) -> str:
    """Join a suite root and a feature path into the full path relative to the repository root."""
    return f"{root}/{path}" if root else path


def _folder_exists(repo_root: Path, root: str) -> bool:
    """Tell whether a suite root exists on disk; the repository root always exists."""
    return True if not root else (repo_root / root).is_dir()


def _find_feature_files(suite_dir: Path) -> list[str]:
    """List the .feature files below suite_dir that have an ancestor folder named exactly 'features'.

    The result holds POSIX paths relative to suite_dir, sorted without regard to case.
    Hidden folders and __pycache__ are skipped at every depth.
    """
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(suite_dir):
        dirnames[:] = [name for name in dirnames if not _is_ignored_name(name)]
        relative_dir = Path(dirpath).relative_to(suite_dir)
        for filename in filenames:
            if not filename.endswith(FEATURE_SUFFIX):
                continue
            relative = relative_dir / filename
            if FEATURES_FOLDER in relative.parts[:-1]:
                found.append(relative.as_posix())
    return sorted(found, key=str.casefold)


def discover_suites(repo_root: Path) -> list[DiscoveredSuite]:
    """Return the suites src/<type>/<name> that hold feature files; folders without any are not suites."""
    suites: list[DiscoveredSuite] = []
    for suite_type in SOURCE_TYPES:
        type_dir = repo_root / "src" / suite_type
        if not type_dir.is_dir():
            continue
        for suite_dir in sorted(type_dir.iterdir(), key=lambda item: item.name.casefold()):
            if not suite_dir.is_dir() or _is_ignored_name(suite_dir.name):
                continue
            feature_paths = _find_feature_files(suite_dir)
            if feature_paths:
                suites.append(
                    DiscoveredSuite(
                        suite_type=suite_type,
                        name=suite_dir.name,
                        root=f"src/{suite_type}/{suite_dir.name}",
                        directory=suite_dir,
                        feature_paths=tuple(feature_paths),
                    )
                )
    return suites


def _tag_candidate(feature_file: Path) -> str | None:
    """Return the first tag before the Feature keyword, without '@', when it is a valid feature id.

    Blank and comment lines before the keyword are skipped, and only the first tag
    line counts. Returns None when there is no such tag or its first token is not a
    valid id. A file that is not UTF-8 raises ManifestError, because it cannot be
    identified reliably.
    """
    try:
        text = feature_file.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ManifestError(f"{feature_file}: not valid UTF-8 ({exc.reason})") from exc
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if FEATURE_KEYWORD_PATTERN.match(line):
            return None
        if line.startswith("@"):
            token = line.split()[0][1:]
            return token if FEATURE_ID_PATTERN.fullmatch(token) else None
    return None


def _fallback_feature_id(file_name: str) -> str:
    """Build a feature id from a file name: no extension, unsafe runs become '_', at most 80 characters."""
    stem = file_name[: -len(FEATURE_SUFFIX)] if file_name.endswith(FEATURE_SUFFIX) else file_name
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", stem).strip("_")[:80].strip("_")
    return cleaned or "feature"


def _unique_feature_id(base: str, taken: set[str]) -> str:
    """Return base, or base with a numeric suffix, that is not in taken; taken holds casefolded ids."""
    if base.casefold() not in taken:
        return base
    number = 2
    while True:
        suffix = f"_{number}"
        candidate = base[: 80 - len(suffix)] + suffix
        if candidate.casefold() not in taken:
            return candidate
        number += 1


def _assign_feature_ids(
    new_paths: list[str], candidates: dict[str, str | None], reserved: set[str]
) -> dict[str, str]:
    """Give every new feature path an id: its tag candidate when usable, otherwise the file-name fallback.

    A candidate is used only when no other new file shares it (compared without
    case) and no live entry of the suite already holds it. Fallback ids get a
    numeric suffix on collision. Ids of existing entries are never changed here.
    """
    counts = Counter(candidates[path].casefold() for path in new_paths if candidates[path])
    taken = {item.casefold() for item in reserved}
    assigned: dict[str, str] = {}
    for path in new_paths:
        candidate = candidates[path]
        if candidate and counts[candidate.casefold()] == 1 and candidate.casefold() not in taken:
            assigned[path] = candidate
            taken.add(candidate.casefold())
    for path in new_paths:
        if path not in assigned:
            assigned[path] = _unique_feature_id(_fallback_feature_id(PurePosixPath(path).name), taken)
            taken.add(assigned[path].casefold())
    return assigned


def load_registry(registry_path: Path) -> dict[str, dict[str, Any]]:
    """Read the NRT suite registry keyed by normalized behave_path.

    A missing or unreadable registry is treated as empty and reported as a warning,
    because it only decides the label and the activation of new suites.
    """
    if not registry_path.is_file():
        _warn(f"registry {registry_path} not found: new suites are added disabled")
        return {}
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        _warn(f"registry {registry_path} unreadable ({exc}): new suites are added disabled")
        return {}
    suites = data.get("suites") if isinstance(data, dict) else None
    if not isinstance(suites, list):
        _warn(f"registry {registry_path} has no 'suites' list: new suites are added disabled")
        return {}
    registry: dict[str, dict[str, Any]] = {}
    for item in suites:
        if not isinstance(item, dict):
            continue
        suite_id = item.get("id")
        behave_path = item.get("behave_path")
        label = item.get("label")
        if not isinstance(suite_id, str) or not SUITE_ID_PATTERN.fullmatch(suite_id):
            continue
        if not isinstance(behave_path, str):
            continue
        registry[_normalize_root(behave_path)] = {
            "id": suite_id,
            "label": label if isinstance(label, str) and 1 <= len(label) <= 100 else None,
        }
    return registry


def _drop_retired_keys(data: Any) -> None:
    """Remove the retired test_type key from loaded features; the manifest no longer carries it (D26)."""
    if not isinstance(data, dict) or not isinstance(data.get("suites"), list):
        return
    for suite in data["suites"]:
        if isinstance(suite, dict) and isinstance(suite.get("features"), list):
            for feature in suite["features"]:
                if isinstance(feature, dict):
                    feature.pop("test_type", None)


def read_manifest(manifest_path: Path) -> dict[str, Any] | None:
    """Parse and validate an existing manifest. Returns None when the file is missing.

    Raises ManifestError for oversized, non-UTF-8, invalid YAML or rule-breaking
    content, so that an invalid file is never overwritten.
    """
    if not manifest_path.exists():
        return None
    raw = manifest_path.read_bytes()
    if len(raw) > MANIFEST_MAX_BYTES:
        raise ManifestError(f"{manifest_path}: larger than {MANIFEST_MAX_BYTES} bytes")
    try:
        data = yaml.load(raw.decode("utf-8-sig"), Loader=_StrictLoader)
    except UnicodeDecodeError as exc:
        raise ManifestError(f"{manifest_path}: not valid UTF-8") from exc
    except yaml.YAMLError as exc:
        raise ManifestError(f"{manifest_path}: invalid YAML: {exc}") from exc
    except ManifestError as exc:
        raise ManifestError(f"{manifest_path}: {exc}") from exc
    _drop_retired_keys(data)
    errors = validate_manifest(data)
    if errors:
        raise ManifestError(f"{manifest_path}: {'; '.join(errors[:3])}")
    return data


def _relative_path_problem(value: Any) -> str | None:
    """Return why value is not a safe relative path, or None when it is one."""
    if not isinstance(value, str) or not value:
        return "must be a non-empty text"
    if value != value.strip():
        return "must not start or end with spaces"
    if value.startswith("/"):
        return "must be relative (no leading '/')"
    if "\\" in value:
        return "must not contain a backslash"
    if "//" in value:
        return "must not contain '//'"
    if ".." in value.split("/"):
        return "must not contain '..'"
    return None


def _feature_path_problem(value: Any) -> str | None:
    """Return why a feature path is invalid, or None when it is valid."""
    problem = _relative_path_problem(value)
    if problem:
        return problem
    if not value.endswith(FEATURE_SUFFIX):
        return "must end with '.feature'"
    return None


def _estimate_problem(value: Any) -> str | None:
    """Return why an estimate is invalid: a finite number from 0 to 365 with at most 2 decimals."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return "must be a number"
    if isinstance(value, float) and not math.isfinite(value):
        return "must be a finite number"
    if value < 0 or value > MAX_ESTIMATE_DAYS:
        return f"must be between 0 and {MAX_ESTIMATE_DAYS}"
    if isinstance(value, float) and Decimal(repr(value)).as_tuple().exponent < -2:
        return "must have at most 2 decimals"
    return None


def _is_exact_int(value: Any, expected: int) -> bool:
    """Tell whether value is the integer expected; booleans are not accepted as integers."""
    return isinstance(value, int) and not isinstance(value, bool) and value == expected


def _describe_suite(suite: dict[str, Any], position: int) -> str:
    """Name a suite in an error message by its id, or by its position when the id is unusable."""
    suite_id = suite.get("id")
    return f"suite '{suite_id}'" if isinstance(suite_id, str) else f"suite #{position}"


def validate_manifest(data: Any) -> list[str]:
    """Return the rule violations of a manifest structure; an empty list means it is valid.

    The rules follow the QA Central Hub manifest contract: strict keys, id patterns,
    safe relative paths, unique ids and paths, estimates, and at least one enabled suite.
    """
    if not isinstance(data, dict):
        return ["the manifest must be a mapping"]
    errors: list[str] = [
        f"unknown top-level key '{key}'" for key in data if key not in ALLOWED_ROOT_KEYS
    ]
    if not _is_exact_int(data.get("version"), 1):
        errors.append("version must be the integer 1")
    suites = data.get("suites")
    if not isinstance(suites, list) or not suites:
        errors.append("suites must be a non-empty list")
        return errors

    suite_ids: set[str] = set()
    full_paths: set[str] = set()
    enabled_suites = 0
    for position, suite in enumerate(suites, start=1):
        if not isinstance(suite, dict):
            errors.append(f"suite #{position} must be a mapping")
            continue
        where = _describe_suite(suite, position)
        errors.extend(
            f"{where}: unknown key '{key}'" for key in suite if key not in ALLOWED_SUITE_KEYS
        )

        suite_id = suite.get("id")
        if not isinstance(suite_id, str) or not SUITE_ID_PATTERN.fullmatch(suite_id):
            errors.append(f"{where}: id must be 1-64 characters of lowercase letters, digits, '-' or '_'")
        elif suite_id.casefold() in suite_ids:
            errors.append(f"{where}: the suite id is used twice")
        else:
            suite_ids.add(suite_id.casefold())

        if "label" in suite and not (
            isinstance(suite["label"], str) and 1 <= len(suite["label"]) <= 100
        ):
            errors.append(f"{where}: label must be a text of 1 to 100 characters")

        root = ""
        if "root" in suite:
            if not isinstance(suite["root"], str):
                errors.append(f"{where}: root must be a text")
            else:
                root = _normalize_root(suite["root"])
                problem = _relative_path_problem(root)
                if problem:
                    errors.append(f"{where}: root {problem}")

        enabled = suite.get("enabled", True)
        if not isinstance(enabled, bool):
            errors.append(f"{where}: enabled must be true or false")
        elif enabled:
            enabled_suites += 1

        features = suite.get("features")
        if not isinstance(features, list):
            errors.append(f"{where}: features must be a list")
            continue
        feature_ids: set[str] = set()
        for feature_position, feature in enumerate(features, start=1):
            if not isinstance(feature, dict):
                errors.append(f"{where}: feature #{feature_position} must be a mapping")
                continue
            here = f"{where}, feature #{feature_position}"
            errors.extend(
                f"{here}: unknown key '{key}'"
                for key in feature
                if key not in ALLOWED_FEATURE_KEYS
            )

            feature_id = feature.get("id")
            if not isinstance(feature_id, str) or not FEATURE_ID_PATTERN.fullmatch(feature_id):
                errors.append(f"{here}: id must be 1-80 characters of letters, digits, '-' or '_'")
            elif feature_id.casefold() in feature_ids:
                errors.append(f"{where}: the feature id '{feature_id}' appears twice")
            else:
                feature_ids.add(feature_id.casefold())

            path_problem = _feature_path_problem(feature.get("path"))
            if path_problem:
                errors.append(f"{here}: path {path_problem}")
            else:
                full_path = _join_root(root, feature["path"])
                if full_path in full_paths:
                    errors.append(f"{here}: the path '{full_path}' appears twice")
                full_paths.add(full_path)

            if "estimate_days" in feature:
                problem = _estimate_problem(feature["estimate_days"])
                if problem:
                    errors.append(f"{here}: estimate_days {problem}")
            if "enabled" in feature and not isinstance(feature["enabled"], bool):
                errors.append(f"{here}: enabled must be true or false")

    if enabled_suites == 0:
        errors.append("at least one suite must be enabled")
    return errors


def reconcile_features(
    suite_id: str,
    root: str,
    entries: list[dict[str, Any]],
    discovered_suite: DiscoveredSuite | None,
    repo_root: Path,
    claimed: dict[str, str],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Reconcile the feature entries of one suite with the files on disk.

    Live entries (file present) keep every field. Dead entries are removed, except
    when a new file has the same tag id, in which case the entry moves to the new
    path. Managed suites (discovered_suite given) get entries for new files, skipping
    paths claimed by other suites; manual suites only lose their dead entries.
    Returns the sorted entries and the change messages.
    """
    live: list[dict[str, Any]] = []
    dead: list[dict[str, Any]] = []
    for entry in entries:
        target = repo_root / _join_root(root, entry["path"])
        (live if target.is_file() else dead).append(entry)
    changes: list[str] = []

    if discovered_suite is None:
        for entry in dead:
            changes.append(
                f"feature '{suite_id}/{entry['id']}' removed: '{entry['path']}' not found"
            )
        return sorted(live, key=lambda item: item["path"].casefold()), changes

    listed = {entry["path"] for entry in entries}
    new_paths = [
        path
        for path in discovered_suite.feature_paths
        if path not in listed and _join_root(root, path) not in claimed
    ]
    candidates = {path: _tag_candidate(discovered_suite.directory / path) for path in new_paths}

    still_dead: list[dict[str, Any]] = []
    for entry in dead:
        key = entry["id"].casefold()
        matches = [path for path in new_paths if candidates[path] and candidates[path].casefold() == key]
        if len(matches) == 1:
            changes.append(
                f"feature '{suite_id}/{entry['id']}' moved: '{entry['path']}' -> '{matches[0]}'"
            )
            entry["path"] = matches[0]
            live.append(entry)
            new_paths.remove(matches[0])
        else:
            still_dead.append(entry)
    for entry in still_dead:
        changes.append(f"feature '{suite_id}/{entry['id']}' removed: '{entry['path']}' not found")

    reserved = {entry["id"] for entry in live}
    assigned = _assign_feature_ids(new_paths, {path: candidates[path] for path in new_paths}, reserved)
    for path in new_paths:
        live.append({"id": assigned[path], "path": path})
        changes.append(f"feature '{suite_id}/{assigned[path]}' added: '{path}'")
    return sorted(live, key=lambda item: item["path"].casefold()), changes


def reconcile_suites(
    existing_suites: list[dict[str, Any]],
    discovered: list[DiscoveredSuite],
    repo_root: Path,
    registry: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Build the new suite list from the existing manifest and the discovered tree.

    Existing suites keep their ids and labels. Suites whose folder is gone, or that
    end up with no feature, are removed. Discovered suites that are not in the
    manifest are appended in root order: enabled when listed in the NRT registry,
    disabled otherwise. Raises ManifestError when two suites cannot get distinct ids.
    """
    discovered_by_root = {suite.root: suite for suite in discovered}
    claimed: dict[str, str] = {}
    for suite in existing_suites:
        root = _normalize_root(suite.get("root"))
        for feature in suite["features"]:
            claimed[_join_root(root, feature["path"])] = root

    changes: list[str] = []
    kept: list[dict[str, Any]] = []
    matched_roots: set[str] = set()
    for suite in existing_suites:
        suite_id = suite["id"]
        root = _normalize_root(suite.get("root"))
        if not _folder_exists(repo_root, root):
            changes.append(f"suite '{suite_id}' removed: folder '{root}' not found")
            continue
        discovered_suite = discovered_by_root.get(root)
        if discovered_suite is not None:
            matched_roots.add(root)
        features, feature_changes = reconcile_features(
            suite_id, root, suite["features"], discovered_suite, repo_root, claimed
        )
        changes.extend(feature_changes)
        if not features:
            changes.append(f"suite '{suite_id}' removed: no feature files left")
            continue
        kept_suite = dict(suite)
        if root:
            kept_suite["root"] = root
        else:
            kept_suite.pop("root", None)
        kept_suite["features"] = features
        kept.append(kept_suite)

    taken = {suite["id"].casefold(): _normalize_root(suite.get("root")) for suite in kept}
    name_counts = Counter(_suite_id_from_name(suite.name) for suite in discovered)
    new_discovered = [suite for suite in discovered if suite.root not in matched_roots]
    new_discovered.sort(key=lambda suite: (suite.root not in registry, suite.root.casefold()))

    created: list[dict[str, Any]] = []
    for suite in new_discovered:
        base = _suite_id_from_name(suite.name)
        prefixed = _suite_id_from_name(f"{suite.suite_type}-{suite.name}")
        registry_entry = registry.get(suite.root)
        if registry_entry is not None:
            proposed = registry_entry["id"]
        elif name_counts[base] > 1:
            proposed = prefixed
        else:
            proposed = base
        suite_id = proposed if proposed.casefold() not in taken else prefixed
        if suite_id.casefold() in taken:
            raise ManifestError(
                f"suite id collision between '{taken[suite_id.casefold()]}' and '{suite.root}'"
            )
        features, feature_changes = reconcile_features(
            suite_id, suite.root, [], suite, repo_root, claimed
        )
        if not features:
            continue
        taken[suite_id.casefold()] = suite.root
        new_suite: dict[str, Any] = {"id": suite_id, "root": suite.root, "features": features}
        if registry_entry is not None:
            if registry_entry["label"]:
                new_suite["label"] = registry_entry["label"]
            status = "enabled"
        else:
            new_suite["enabled"] = False
            status = "disabled, not in the NRT registry"
        created.append(new_suite)
        changes.append(f"suite '{suite_id}' added: {len(features)} features, {status}")
        changes.extend(feature_changes)

    created.sort(key=lambda item: item["root"].casefold())
    return kept + created, changes


def _quote(value: str) -> str:
    """Return a YAML double-quoted scalar; backslashes and double quotes are escaped, other text is kept."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _number(value: int | float) -> str:
    """Render an estimate without quotes, keeping floats with a decimal point."""
    return repr(value) if isinstance(value, float) else str(value)


def render_manifest(suites: list[dict[str, Any]]) -> str:
    """Write the manifest text by hand so that quoting, field order and blank lines stay stable.

    Only 'enabled: false' is written, because true is the default. The 'test_type'
    key is never written.
    """
    lines = list(HEADER_LINES)
    lines += ["version: 1", "", "suites:"]
    for position, suite in enumerate(suites):
        if position:
            lines.append("")
        lines.append(f"  - id: {_quote(suite['id'])}")
        if "label" in suite:
            lines.append(f"    label: {_quote(suite['label'])}")
        if suite.get("root"):
            lines.append(f"    root: {_quote(suite['root'])}")
        if suite.get("enabled", True) is False:
            lines.append("    enabled: false")
        features = suite["features"]
        if not features:
            lines.append("    features: []")
            continue
        lines.append("    features:")
        for feature in features:
            lines.append(f"      - id: {_quote(feature['id'])}")
            lines.append(f"        path: {_quote(feature['path'])}")
            if "estimate_days" in feature:
                lines.append(f"        estimate_days: {_number(feature['estimate_days'])}")
            if feature.get("enabled", True) is False:
                lines.append("        enabled: false")
    return "\n".join(lines) + "\n"


def run(repo_root: Path, manifest: str, registry: str, check: bool, dry_run: bool) -> int:
    """Regenerate the manifest for repo_root and write it when needed. Returns the exit code.

    Nothing is written when validation of the existing or the rendered manifest fails.
    """
    manifest_path = repo_root / manifest
    registry_map = load_registry(repo_root / registry)
    existing = read_manifest(manifest_path)
    existing_suites = existing["suites"] if existing is not None else []
    discovered = discover_suites(repo_root)
    suites, changes = reconcile_suites(existing_suites, discovered, repo_root, registry_map)

    errors = validate_manifest({"version": 1, "suites": suites})
    if errors:
        raise ManifestError(f"generated manifest is invalid: {'; '.join(errors[:3])}")
    text = render_manifest(suites)
    encoded = text.encode("utf-8")
    if len(encoded) > MANIFEST_MAX_BYTES:
        raise ManifestError(f"generated manifest is larger than {MANIFEST_MAX_BYTES} bytes")
    try:
        rendered = yaml.load(text, Loader=_StrictLoader)
    except yaml.YAMLError as exc:
        raise ManifestError(f"generated manifest does not parse: {exc}") from exc
    errors = validate_manifest(rendered)
    if errors:
        raise ManifestError(f"rendered manifest does not validate: {'; '.join(errors[:3])}")

    old_bytes = manifest_path.read_bytes() if manifest_path.exists() else None
    changed = old_bytes != encoded
    feature_total = sum(len(suite["features"]) for suite in suites)
    enabled_total = sum(1 for suite in suites if suite.get("enabled", True))
    _info(f"suites: {len(suites)} ({enabled_total} enabled), features: {feature_total}")
    for change in changes:
        _info(change)
    if not changed:
        _info("manifest unchanged")

    if check:
        if changed:
            _info(f"{manifest} is out of date: run the script without --check")
            return 1
        _info("manifest is up to date")
        return 0
    if dry_run:
        _info("dry run: nothing written")
        return 0
    if changed:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("wb") as handle:
            handle.write(encoded)
        _info(f"written {manifest}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse the command line, run the sync and return the exit code (0, 1 or 2)."""
    parser = argparse.ArgumentParser(description="Regenerate the Gherkin manifest from src/.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="repository root (default: current folder)")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="manifest path relative to the root")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY, help="NRT suite registry relative to the root")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="do not write; exit 1 if the manifest would change")
    mode.add_argument("--dry-run", action="store_true", help="do not write; print the summary only")
    args = parser.parse_args(argv)
    try:
        return run(args.repo_root.resolve(), args.manifest, args.registry, args.check, args.dry_run)
    except (ManifestError, OSError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
