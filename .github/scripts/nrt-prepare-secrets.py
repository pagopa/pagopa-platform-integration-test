"""Validate and materialize the environment bundle before running test suites."""

import argparse
import json
import os
from pathlib import Path

from nrt_secret_configs import config_placeholders, environment_configs, placeholders as _placeholders


def validate_bundle(raw_bundle: str, target_env: str, test_path: Path) -> dict:
    if target_env not in ("dev", "uat"):
        raise RuntimeError("Target environment must be dev or uat")
    try:
        bundle = json.loads(raw_bundle)
    except json.JSONDecodeError:
        raise RuntimeError("NRT_SECRETS_BUNDLE is empty or invalid JSON") from None
    if not isinstance(bundle, dict) or set(bundle) != {target_env}:
        raise RuntimeError("Bundle must contain only the selected environment")
    values = bundle[target_env]
    if not isinstance(values, dict) or not values:
        raise RuntimeError("Bundle must contain a non-empty secret map")
    if any(not isinstance(value, str) or not value for value in values.values()):
        raise RuntimeError("Bundle contains empty or non-string secret values")
    if not test_path.is_dir() or not test_path.resolve().is_relative_to(Path("src").resolve()):
        raise RuntimeError("Test path must be an existing suite directory inside src")

    required = set()
    for config_path in environment_configs(test_path, target_env):
        required.update(config_placeholders(config_path))

    missing = required - values.keys()
    if missing:
        raise RuntimeError("Suite secrets missing from bundle: " + ", ".join(sorted(missing)))
    print(f"Validated {len(required)} required secret(s) for {test_path} in {target_env}")
    return bundle


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("test_path", type=Path)
    args = parser.parse_args()
    bundle = validate_bundle(
        os.environ.get("NRT_SECRETS_BUNDLE", ""),
        os.environ.get("TARGET_ENV", ""),
        args.test_path,
    )
    destination = Path("config/.secrets.yaml")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as output:
        os.fchmod(output.fileno(), 0o600)
        json.dump(bundle, output)


if __name__ == "__main__":
    main()