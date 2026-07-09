#!/usr/bin/env python3
"""Utility to fetch files from a GitHub repo using a PAT stored in a YAML secret.

This script reads `config/github.bot.cd.pat.secrets.yaml` (by default), extracts a GitHub PAT,
and attempts to download specified files from a repository using the GitHub API.
The branch is resolved by target environment:
    - PROD -> master
    - UAT -> develop
    - DEV -> latest SANPx.y.z branch
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.conf.configuration import secrets


def extract_token_from_text(text: str) -> Optional[str]:
    """Extract a likely GitHub PAT from the provided text.

    This uses heuristic regexes to find tokens such as `github_pat_...` or `ghp_...`.
    Returns the first match or None if none found.
    """
    patterns = [r"github_pat_[A-Za-z0-9_]+", r"ghp_[A-Za-z0-9_]+", r"[A-Za-z0-9_-]{36,255}"]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(0)
    return None


def extract_token_from_yaml(path: str) -> str:
    """Read the yaml file at `path` and extract a PAT token.

    The function will not print the token. It raises RuntimeError if no token
    is found.
    """
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    token = extract_token_from_text(txt)
    if not token:
        raise RuntimeError(f"No GitHub PAT found in {path}")
    return token


def api_get(url: str, token: Optional[str] = None, accept_raw: bool = False) -> bytes:
    """Perform a GET request to `url` with optional Authorization header.

    Returns the response body as bytes. Raises urllib.error.HTTPError on non-200.
    """
    headers = {
        "User-Agent": "fetch-github-files-script/1.0",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    if accept_raw:
        headers["Accept"] = "application/vnd.github.v3.raw"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def list_repo_branches(owner: str, repo: str, token: Optional[str]) -> List[str]:
    """Retrieve all branch names from a GitHub repository.

    This function uses paginated GitHub API calls and returns branch names.
    It raises RuntimeError if no branches can be read.
    """
    branches: List[str] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{urllib.parse.quote(owner)}/"
            f"{urllib.parse.quote(repo)}/branches?per_page=100&page={page}"
        )
        data = api_get(url, token=token)
        payload = json.loads(data.decode("utf-8"))
        if not isinstance(payload, list):
            raise RuntimeError("Unexpected branches response format from GitHub API")
        if not payload:
            break

        for item in payload:
            name = item.get("name") if isinstance(item, dict) else None
            if isinstance(name, str):
                branches.append(name)

        if len(payload) < 100:
            break
        page += 1

    if not branches:
        raise RuntimeError("No branches found in the target repository")
    return branches


def parse_sanp_version(branch_name: str) -> Optional[Tuple[int, int, int]]:
    """Parse SANP branch names in the format SANPx.y.z.

    Returns a semantic version tuple if the branch name is valid, otherwise None.
    """
    match = re.fullmatch(r"SANP(\d+)\.(\d+)\.(\d+)", branch_name)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def get_latest_sanp_branch(branches: List[str]) -> Optional[str]:
    """Return the SANP branch with the highest x.y.z value.

    Returns None when no branch follows the SANPx.y.z naming convention.
    """
    candidates: List[Tuple[Tuple[int, int, int], str]] = []
    for branch in branches:
        version = parse_sanp_version(branch)
        if version is not None:
            candidates.append((version, branch))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def inspect_branch_catalog(branches: List[str]) -> Optional[str]:
    """Validate required branches and return the latest SANP branch if available.

    This enforces the presence of master and develop branches, then detects
    the highest SANPx.y.z branch for DEV mapping.
    """
    missing = [required for required in ("master", "develop") if required not in branches]
    if missing:
        raise RuntimeError(f"Required branch(es) missing: {', '.join(missing)}")
    return get_latest_sanp_branch(branches)


def resolve_branch_for_target_env(target_env: str, latest_sanp_branch: Optional[str]) -> str:
    """Resolve the source branch from the selected target environment.

    Mapping rules:
            - PROD -> master
      - UAT -> develop
      - DEV -> latest SANPx.y.z
    """
    if target_env == "PROD":
                return "master"
    if target_env == "UAT":
        return "develop"
    if target_env == "DEV":
        if latest_sanp_branch is None:
            raise RuntimeError("No SANPx.y.z branch found while DEV environment was requested")
        return latest_sanp_branch
    raise RuntimeError(f"Unsupported target environment: {target_env}")


def fetch_file_from_repo(owner: str, repo: str, path: str, branch: str, token: Optional[str]) -> bytes:
    """Fetch file `path` from the given repo and branch. Try GitHub API raw endpoint first,
    then fall back to raw.githubusercontent.com.

    Returns the raw file bytes on success, raises on failure.
    """
    # Try GitHub API content endpoint with raw accept header
    api_url = f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/contents/{urllib.parse.quote(path)}?ref={urllib.parse.quote(branch)}"
    try:
        return api_get(api_url, token=token, accept_raw=True)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    # Fallback to raw.githubusercontent URL
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    return api_get(raw_url, token=token, accept_raw=False)


def is_valid_json_bytes(b: bytes) -> bool:
    """Return True if bytes `b` decode to valid JSON, False otherwise."""
    try:
        json.loads(b.decode("utf-8"))
        return True
    except Exception:
        return False


def write_file(out_path: str, content: bytes) -> None:
    """Write bytes `content` to `out_path`, creating parent directories as needed."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(content)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entrypoint.

    Example usage (from repo root):
      python scripts/fetch_github_files.py

    By default it reads the PAT from `config/github.bot.cd.pat.secrets.yaml` and downloads
    `openapi/fdr_organization.json` and `openapi/fdr_psp.json` from
    `pagopa/pagopa-api` into `tmp_fetched/`, using UAT branch mapping.
    """
    parser = argparse.ArgumentParser(description="Fetch files from GitHub using PAT from a YAML secret.")
    parser.add_argument("--owner", default="pagopa", help="GitHub owner/org")
    parser.add_argument("--repo", default="pagopa-api", help="GitHub repo name")
    parser.add_argument(
        "--target-env",
        default="UAT",
        choices=["PROD", "UAT", "DEV"],
        help="Branch mapping selector: PROD->master, UAT->develop, DEV->latest SANPx.y.z",
    )
    parser.add_argument("--paths", nargs="*", default=["openapi/fdr_organization.json", "openapi/fdr_psp.json"], help="Paths to fetch from the repo")
    parser.add_argument("--outdir", default="tmp_fetched", help="Output directory to save downloaded files")
    args = parser.parse_args(argv)

    try:
        token = secrets.gh_token
    except Exception as e:
        print(f"ERROR: could not extract token from {args.secret}: {e}")
        return 2

    try:
        branches = list_repo_branches(args.owner, args.repo, token)
        latest_sanp_branch = inspect_branch_catalog(branches)
        if latest_sanp_branch is not None:
            print(f"Latest SANP branch detected: {latest_sanp_branch}")
        else:
            print("No SANPx.y.z branches detected")
        branch = resolve_branch_for_target_env(args.target_env, latest_sanp_branch)
    except Exception as e:
        print(f"ERROR: could not resolve source branch: {e}")
        return 3

    print(f"Target environment: {args.target_env}")
    print(f"Using branch: {branch}")

    results = []
    for p in args.paths:
        try:
            raw = fetch_file_from_repo(args.owner, args.repo, p, branch, token)
            out_path = os.path.join(args.outdir, os.path.basename(p))
            write_file(out_path, raw)
            valid = is_valid_json_bytes(raw)
            results.append((p, True, out_path, valid, None))
            print(f"OK: {p} -> {out_path} (valid_json={valid})")
        except Exception as e:
            results.append((p, False, None, False, str(e)))
            print(f"FAIL: {p} : {e}")

    # Summarize
    success = all(r[1] for r in results)
    if success:
        print("All files fetched successfully.")
        return 0
    else:
        print("Some files failed to fetch.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
