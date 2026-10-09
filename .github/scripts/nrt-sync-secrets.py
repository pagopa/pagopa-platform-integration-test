"""Sync suite YAML Key Vault secrets into an environment-scoped GitHub Actions secret."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

import requests
from nacl.public import PublicKey, SealedBox

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.conf.configuration import get_secrets_resolver
from nrt_secret_configs import SUITE_ROOTS, config_placeholders, environment_configs


GITHUB_PAT_SECRET_NAME = "pagopa-platform-domain-github-bot-cd-pat"
MAX_GITHUB_SECRET_BYTES = 48 * 1024


def _mask_secret(value: str) -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::add-mask::{value}")


def _required_environment_value(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


def _github_headers(token: str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }


def _key_vault_secret_name(placeholder_name: str) -> str:
    return placeholder_name.lower()


def _resolve_bundle(resolver, target_env: str, resolved_values: dict[str, str]) -> dict[str, str]:
    config_files = sorted(
        config_path
        for directory in SUITE_ROOTS
        for config_path in environment_configs(directory, target_env)
    )
    if not config_files:
        raise RuntimeError(f"No suite YAML configs found for environment {target_env}")

    resolved_values = dict(resolved_values)
    bundle: dict[str, str] = {}
    for config_path in config_files:
        for placeholder_name in sorted(config_placeholders(config_path)):
            value = resolved_values.get(placeholder_name)
            if value is None:
                vault_secret_name = _key_vault_secret_name(placeholder_name)
                try:
                    value = resolver.resolve(vault_secret_name)
                except Exception as exc:
                    raise RuntimeError(
                        f"Failed to resolve {vault_secret_name} for "
                        f"{config_path}"
                    ) from exc
                if not value:
                    raise RuntimeError(
                        f"Key Vault secret {vault_secret_name} is empty or unavailable "
                        f"({config_path})"
                    )
                _mask_secret(value)
                resolved_values[placeholder_name] = value

            bundle[placeholder_name] = value

    if not bundle:
        raise RuntimeError(f"No secret placeholders found for environment {target_env}")

    return bundle


def _publish_environment_secret(
    api_url: str,
    repository: str,
    target_env: str,
    secret_name: str,
    token: str,
    value: str,
) -> None:
    environment = quote(target_env, safe="")
    secret = quote(secret_name, safe="")
    base_url = f"{api_url}/repos/{repository}/environments/{environment}/secrets"
    headers = _github_headers(token)

    key_response = requests.get(f"{base_url}/public-key", headers=headers, timeout=30)
    if key_response.status_code == 404:
        raise RuntimeError(
            f"GitHub Environment {target_env} does not exist; create it before syncing secrets"
        )
    key_response.raise_for_status()
    public_key_data = key_response.json()

    public_key = PublicKey(base64.b64decode(public_key_data["key"]))
    encrypted_value = SealedBox(public_key).encrypt(value.encode("utf-8"))
    payload = {
        "encrypted_value": base64.b64encode(encrypted_value).decode("ascii"),
        "key_id": public_key_data["key_id"],
    }
    if len(value.encode("utf-8")) > MAX_GITHUB_SECRET_BYTES:
        raise RuntimeError(f"Secret {secret_name} exceeds GitHub's 48 KB secret limit")

    response = requests.put(
        f"{base_url}/{secret}",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if response.status_code not in (201, 204):
        raise RuntimeError(
            f"GitHub Environment secret update failed for {target_env}: HTTP {response.status_code}"
        )


def _verify_environment_bundle(target_env: str) -> None:
    raw_bundle = _required_environment_value("NRT_SECRETS_BUNDLE")
    try:
        published = json.loads(raw_bundle)
    except json.JSONDecodeError:
        raise RuntimeError("GitHub Environment bundle is not valid JSON") from None
    if not isinstance(published, dict) or set(published) != {target_env}:
        raise RuntimeError("GitHub Environment bundle must contain only the selected environment")
    actual = published[target_env]
    if not isinstance(actual, dict) or not actual:
        raise RuntimeError("GitHub Environment bundle must contain a non-empty secret map")
    if any(not isinstance(value, str) or not value for value in actual.values()):
        raise RuntimeError("GitHub Environment bundle contains empty or non-string values")

    resolver = get_secrets_resolver()
    try:
        expected = _resolve_bundle(resolver, target_env, {})
        missing_count = len(expected.keys() - actual.keys())
        unexpected_count = len(actual.keys() - expected.keys())
        mismatch_count = sum(
            actual[key] != expected[key] for key in expected.keys() & actual.keys()
        )
        if missing_count or unexpected_count or mismatch_count:
            raise RuntimeError(
                "Bundle verification failed: "
                f"missing={missing_count}, unexpected={unexpected_count}, "
                f"different_values={mismatch_count}"
            )
        message = f"Verified {len(expected)} secret(s) for environment {target_env}: all values match Key Vault."
        print(message)
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            with open(summary_path, "a", encoding="utf-8") as summary:
                summary.write(f"## NRT secret verification\n\n{message}\n")
    finally:
        close_client = getattr(resolver, "close_client", None)
        if close_client:
            close_client()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Compare the published bundle with Key Vault without updating it")
    args = parser.parse_args()
    target_env = _required_environment_value("TARGET_ENV").lower()
    if target_env not in ("dev", "uat"):
        raise RuntimeError(f"Unsupported NRT target environment {target_env}")

    key_vault_url = _required_environment_value("AZURE_KEY_VAULT_URL")
    if args.verify:
        _verify_environment_bundle(target_env)
        return

    repository = _required_environment_value("NRT_GITHUB_REPOSITORY")
    api_url = _required_environment_value("NRT_GITHUB_API_URL").rstrip("/")
    bundle_secret_name = _required_environment_value("NRT_BUNDLE_SECRET_NAME")

    resolver = get_secrets_resolver()
    try:
        github_token = resolver.resolve(GITHUB_PAT_SECRET_NAME)
        if not github_token:
            raise RuntimeError(f"Key Vault secret {GITHUB_PAT_SECRET_NAME} is empty or unavailable")
        _mask_secret(github_token)

        bundle = _resolve_bundle(
            resolver,
            target_env,
            {GITHUB_PAT_SECRET_NAME: github_token},
        )
        bundle_json = json.dumps({target_env: bundle}, separators=(",", ":"))
        if len(bundle_json.encode("utf-8")) > MAX_GITHUB_SECRET_BYTES:
            raise RuntimeError("NRT environment secret bundle exceeds GitHub's 48 KB secret limit")

        _publish_environment_secret(
            api_url,
            repository,
            target_env,
            bundle_secret_name,
            github_token,
            bundle_json,
        )
        print(
            f"Published {len(bundle)} mapped secret(s) to GitHub Environment "
            f"{target_env} as {bundle_secret_name}; Key Vault: {key_vault_url}"
        )
    finally:
        close_client = getattr(resolver, "close_client", None)
        if close_client:
            close_client()


if __name__ == "__main__":
    main()