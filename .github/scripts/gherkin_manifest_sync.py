#!/usr/bin/env python3
"""Keep .github/gherkin-manifest.yml aligned with the feature files under src/.

The manifest describes suites and feature files for QA Central Hub. This
script regenerates it from the repository tree: it discovers the .feature files
under src/<type>/<suite>/features/, keeps
suite labels, derives feature ids from QA Hub headers when present and otherwise
from legacy feature tags or filenames, drops dead entries, and validates the
result before writing it only when its content changed.

Exit codes: 0 success or nothing to change; 1 with --check when the manifest is
out of date; 2 on error (invalid existing manifest, invalid result, I/O failure).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SOURCE_TYPES = ("api", "integration", "e2e")
FEATURE_SUFFIX = ".feature"
FEATURES_FOLDER = "features"
DEFAULT_MANIFEST = ".github/gherkin-manifest.yml"
DEFAULT_REGISTRY = ".github/nrt-suites.json"
MANIFEST_MAX_BYTES = 256 * 1024

SUITE_ID_PATTERN = re.compile(r"[a-z0-9_-]{1,64}")
FEATURE_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,80}")
FEATURE_CODE_PATTERN = re.compile(r"FEAT_(?!000)[0-9]{3}_[A-Za-z][A-Za-z0-9]{1,19}")
FEATURE_CODE_HEADER_PATTERN = re.compile(r"#\s*qa-hub:\s*(\S+)\s*")
QA_HUB_HEADER_MARKER_PATTERN = re.compile(r"^#\s*qa-hub\b", re.IGNORECASE)
FEATURE_KEYWORD_PATTERN = re.compile(r"^\s*(?:Feature|Funzionalità|Funzionalita)\s*:", re.IGNORECASE)
FEATURE_TAG_PATTERN = re.compile(r"@([A-Za-z0-9_-]+)")
LEGACY_FEATURE_ID_TAG_PATTERN = re.compile(r"_[0-9]{3}(?:_|$)")

ALLOWED_ROOT_KEYS = {"version", "suites"}
ALLOWED_SUITE_KEYS = {"id", "label", "root", "test_type", "nrt", "features"}
ALLOWED_FEATURE_KEYS = {"id", "path"}

HEADER_LINES = [
    "# Gherkin manifest: suites and feature files for QA Central Hub's",
    "# Knowledge Base > Gherkin Feature Files, with repository-owned data.",
    "#",
    "# GENERATED FILE: .github/scripts/gherkin_manifest_sync.py rewrites it (workflow",
    "# .github/workflows/gherkin-manifest-sync.yml). Comments written here are lost on the next run.",
    "# The only hand-editable field is suites[].label. Feature ids come from a QA Hub",
    "# header when present; otherwise the legacy feature tag or filename is used.",
    "# Suite test_type comes from its source folder (tas_* suites are TAS);",
    "# nrt comes from membership in .github/nrt-suites.json by behave_path.",
    "# QA Central Hub owns feature status and estimates.",
    "# See the README section 'Manifest Gherkin' for field ownership.",
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
    """List feature files under the suite's canonical features directory.

    The result holds POSIX paths relative to suite_dir, sorted without regard to case.
    Hidden folders and __pycache__ are skipped at every depth.
    """
    found: list[str] = []
    features_dir = suite_dir / FEATURES_FOLDER
    if not features_dir.is_dir():
        return found
    for dirpath, dirnames, filenames in os.walk(features_dir):
        dirnames[:] = [name for name in dirnames if not _is_ignored_name(name)]
        relative_dir = Path(dirpath).relative_to(suite_dir)
        for filename in filenames:
            if not filename.endswith(FEATURE_SUFFIX):
                continue
            relative = relative_dir / filename
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


def _feature_id_from_file(feature_file: Path) -> str:
    """Resolve a feature id from its QA Hub header or legacy tag/filename."""
    try:
        text = feature_file.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ManifestError(f"{feature_file}: not valid UTF-8 ({exc.reason})") from exc
    lines = text.splitlines()
    first_line = lines[0].strip() if lines else ""
    header_lines = [
        (position, line.strip())
        for position, line in enumerate(lines, start=1)
        if QA_HUB_HEADER_MARKER_PATTERN.match(line.strip())
    ]
    if header_lines:
        if len(header_lines) != 1 or header_lines[0][0] != 1:
            raise ManifestError(f"{feature_file}: the QA Hub header must appear once on the first line")
        match = FEATURE_CODE_HEADER_PATTERN.fullmatch(first_line)
        if match is None or not FEATURE_CODE_PATTERN.fullmatch(match.group(1)):
            raise ManifestError(
                f"{feature_file}: first line must be '# qa-hub: FEAT_<NNN>_<Scope>' "
                "with a non-zero three-digit number and a 2-20 character scope"
            )
        return match.group(1)

    feature_tags: list[str] = []
    feature_keyword_found = False
    for line in lines:
        if FEATURE_KEYWORD_PATTERN.match(line):
            feature_keyword_found = True
            break
        stripped = line.strip()
        if stripped.startswith("#") or not stripped.startswith("@"):
            continue
        feature_tags.extend(token for token in stripped.split() if token.startswith("@"))

    if feature_keyword_found:
        for feature_tag in feature_tags:
            if not LEGACY_FEATURE_ID_TAG_PATTERN.search(feature_tag):
                continue
            tag = FEATURE_TAG_PATTERN.fullmatch(feature_tag)
            if tag is None:
                raise ManifestError(f"{feature_file}: invalid legacy feature tag '{feature_tag}'")
            return tag.group(1)

    filename_id = re.sub(r"[^A-Za-z0-9_-]+", "_", feature_file.stem).strip("_-")[:80].rstrip("_-")
    if not FEATURE_ID_PATTERN.fullmatch(filename_id):
        raise ManifestError(f"{feature_file}: filename cannot be converted to a valid feature id")
    return filename_id


def load_registry(registry_path: Path) -> dict[str, dict[str, Any]]:
    """Read the NRT suite registry keyed by normalized behave_path.

    Missing, unreadable or invalid membership data stops generation to avoid
    reporting registered suites as non-NRT.
    """
    if not registry_path.is_file():
        raise ManifestError(f"registry {registry_path} not found: NRT membership is unavailable")
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ManifestError(f"registry {registry_path} unreadable: {exc}") from exc
    suites = data.get("suites") if isinstance(data, dict) else None
    if not isinstance(suites, list):
        raise ManifestError(f"registry {registry_path} has no 'suites' list")
    registry: dict[str, dict[str, Any]] = {}
    for item in suites:
        if not isinstance(item, dict):
            raise ManifestError(f"registry {registry_path}: suite must be a mapping")
        suite_id = item.get("id")
        behave_path = item.get("behave_path")
        label = item.get("label")
        if not isinstance(suite_id, str) or not SUITE_ID_PATTERN.fullmatch(suite_id):
            raise ManifestError(f"registry {registry_path}: invalid suite id")
        if _relative_path_problem(behave_path):
            raise ManifestError(f"registry {registry_path}: invalid behave_path for '{suite_id}'")
        root = _normalize_root(behave_path)
        if root in registry:
            raise ManifestError(f"registry {registry_path}: repeated behave_path '{root}'")
        registry[root] = {
            "id": suite_id,
            "label": label if isinstance(label, str) and 1 <= len(label) <= 100 else None,
        }
    return registry


def _drop_retired_keys(data: Any) -> None:
    """Remove legacy fields now owned by the hub before validating an existing manifest."""
    if not isinstance(data, dict) or not isinstance(data.get("suites"), list):
        return
    removed = 0
    for suite in data["suites"]:
        if not isinstance(suite, dict):
            continue
        if "enabled" in suite:
            del suite["enabled"]
            removed += 1
        if isinstance(suite.get("features"), list):
            for feature in suite["features"]:
                if isinstance(feature, dict):
                    for key in ("test_type", "estimate_days", "enabled"):
                        if key in feature:
                            del feature[key]
                            removed += 1
    if removed:
        _info(f"retired manifest fields to remove: {removed}")


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
    errors = validate_manifest(data, allow_legacy=True)
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


def _is_exact_int(value: Any, expected: int) -> bool:
    """Tell whether value is the integer expected; booleans are not accepted as integers."""
    return isinstance(value, int) and not isinstance(value, bool) and value == expected


def _describe_suite(suite: dict[str, Any], position: int) -> str:
    """Name a suite in an error message by its id, or by its position when the id is unusable."""
    suite_id = suite.get("id")
    return f"suite '{suite_id}'" if isinstance(suite_id, str) else f"suite #{position}"


def validate_manifest(data: Any, *, allow_legacy: bool = False) -> list[str]:
    """Return the rule violations of a manifest structure; an empty list means it is valid.

    The rules check strict keys, id patterns, safe relative paths, and unique ids
    and paths, suite test types and boolean NRT membership. Legacy input may
    omit the new suite fields; generated output must include them.
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

        if "test_type" in suite or not allow_legacy:
            test_type = suite.get("test_type")
            if not isinstance(test_type, str) or test_type not in (*SOURCE_TYPES, "tas"):
                errors.append(f"{where}: test_type must be e2e, integration, api or tas")
        if "nrt" in suite or not allow_legacy:
            if not isinstance(suite.get("nrt"), bool):
                errors.append(f"{where}: nrt must be a boolean")

        root = ""
        if "root" in suite:
            if not isinstance(suite["root"], str):
                errors.append(f"{where}: root must be a text")
            else:
                root = _normalize_root(suite["root"])
                problem = _relative_path_problem(root)
                if problem:
                    errors.append(f"{where}: root {problem}")

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

    return errors


def _suite_metadata(
    root: str, features: list[dict[str, Any]], registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Derive suite type and NRT membership from canonical source paths, not ids."""
    source_roots: set[str] = set()
    for feature in features:
        parts = _join_root(root, feature["path"]).split("/")
        if len(parts) < 4 or parts[0] != "src" or parts[1] not in SOURCE_TYPES:
            raise ManifestError(f"cannot determine test_type for suite root '{root}'")
        source_roots.add("/".join(parts[:3]))
    if len(source_roots) != 1:
        raise ManifestError(f"suite root '{root}' spans multiple source suites")
    source_root = source_roots.pop()
    _, suite_type, name = source_root.split("/")
    test_type = "tas" if name == "tas" or name.startswith("tas_") else suite_type
    return {"test_type": test_type, "nrt": source_root in registry}


def reconcile_features(
    suite_id: str,
    root: str,
    entries: list[dict[str, Any]],
    discovered_suite: DiscoveredSuite | None,
    repo_root: Path,
    claimed: dict[str, str],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Reconcile the feature entries of one suite with the files on disk.

    Live entries follow the id resolved from each file. Dead entries are removed,
    except when a new file has the same id, in which case the entry moves to the new
    path. Manual suites only lose dead entries.
    Returns the sorted entries and the change messages.
    """
    live: list[dict[str, Any]] = []
    dead: list[dict[str, Any]] = []
    feature_ids = (
        {
            path: _feature_id_from_file(discovered_suite.directory / path)
            for path in discovered_suite.feature_paths
        }
        if discovered_suite is not None
        else {}
    )
    changes: list[str] = []
    for entry in entries:
        target = repo_root / _join_root(root, entry["path"])
        if not target.is_file():
            dead.append(entry)
            continue
        live_entry = dict(entry)
        new_id = feature_ids.get(entry["path"])
        if new_id is not None and live_entry["id"] != new_id:
            changes.append(
                f"feature '{suite_id}/{live_entry['id']}' id updated to '{new_id}' "
                f"from feature file at '{entry['path']}'"
            )
            live_entry["id"] = new_id
        live.append(live_entry)

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
    still_dead: list[dict[str, Any]] = []
    for entry in dead:
        key = entry["id"].casefold()
        matches = [path for path in new_paths if feature_ids[path].casefold() == key]
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

    for path in new_paths:
        feature_id = feature_ids[path]
        live.append({"id": feature_id, "path": path})
        changes.append(f"feature '{suite_id}/{feature_id}' added: '{path}'")
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
    manifest are appended in root order. Source paths and registry membership
    recompute test_type and nrt; the registry also supplies known ids and labels.
    Raises ManifestError when two suites cannot get distinct ids.
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
        metadata = _suite_metadata(root, features, registry)
        for key, value in metadata.items():
            if key not in suite or suite[key] != value:
                changes.append(f"suite '{suite_id}' {key} updated to {value}")
        kept_suite.update(metadata)
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
        new_suite.update(_suite_metadata(suite.root, features, registry))
        if registry_entry is not None and registry_entry["label"]:
            new_suite["label"] = registry_entry["label"]
        created.append(new_suite)
        changes.append(f"suite '{suite_id}' added: {len(features)} features")
        changes.extend(feature_changes)

    created.sort(key=lambda item: item["root"].casefold())
    return kept + created, changes


def _quote(value: str) -> str:
    """Return a YAML double-quoted scalar; backslashes and double quotes are escaped, other text is kept."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_manifest(suites: list[dict[str, Any]]) -> str:
    """Render the manifest with stable quoting, field order and blank lines."""
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
        lines.append(f"    test_type: {_quote(suite['test_type'])}")
        lines.append(f"    nrt: {'true' if suite['nrt'] else 'false'}")
        features = suite["features"]
        if not features:
            lines.append("    features: []")
            continue
        lines.append("    features:")
        for feature in features:
            lines.append(f"      - id: {_quote(feature['id'])}")
            lines.append(f"        path: {_quote(feature['path'])}")
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
    _info(f"suites: {len(suites)}, features: {feature_total}")
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
