#!/usr/bin/env python3
"""Utility to fetch files from a GitHub repo using a PAT stored in a YAML secret.

This script reads `config/github.bot.cd.pat.secrets.yaml` (by default), extracts a GitHub PAT,
and attempts to download specified files from a repository using the GitHub API.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import List, Optional


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


def get_default_branch(owner: str, repo: str, token: Optional[str]) -> str:
    """Query GitHub API to determine the repository's default branch.

    Falls back to 'main' if the API call fails.
    """
    url = f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}"
    try:
        data = api_get(url, token)
        info = json.loads(data.decode("utf-8"))
        return info.get("default_branch", "main")
    except Exception:
        return "main"


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
    `pagopa/pagopa-api` into `tmp_fetched/`.
    """
    parser = argparse.ArgumentParser(description="Fetch files from GitHub using PAT from a YAML secret.")
    parser.add_argument("--secret", default="config/github.bot.cd.pat.secrets.yaml", help="Path to YAML secret file containing the PAT")
    parser.add_argument("--owner", default="pagopa", help="GitHub owner/org")
    parser.add_argument("--repo", default="pagopa-api", help="GitHub repo name")
    parser.add_argument("--paths", nargs="*", default=["openapi/fdr_organization.json", "openapi/fdr_psp.json"], help="Paths to fetch from the repo")
    parser.add_argument("--outdir", default="tmp_fetched", help="Output directory to save downloaded files")
    args = parser.parse_args(argv)

    try:
        token = extract_token_from_yaml(args.secret)
    except Exception as e:
        print(f"ERROR: could not extract token from {args.secret}: {e}")
        return 2

    branch = get_default_branch(args.owner, args.repo, token)
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
