"""Run local secret cutover regression tests with synthetic credentials."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.conf import configuration
from nrt_secret_configs import SUITE_ROOTS, config_placeholders, environment_configs


SPEC = importlib.util.spec_from_file_location(
    "nrt_prepare_secrets", Path(".github/scripts/nrt-prepare-secrets.py")
)
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)

SYNC_SPEC = importlib.util.spec_from_file_location(
    "nrt_sync_secrets", Path(".github/scripts/nrt-sync-secrets.py")
)
SYNC = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(SYNC)


class NrtSecretsTests(unittest.TestCase):
    def setUp(self):
        self.bundle = {}
        for environment in ("dev", "uat"):
            names = set()
            for directory in SUITE_ROOTS:
                for config_path in environment_configs(directory, environment):
                    names.update(config_placeholders(config_path))
            self.bundle[environment] = {name: "synthetic-value" for name in names}

    def test_current_suite_placeholders_are_resolvable(self):
        for environment in ("dev", "uat"):
            for suite in ("src/integration/wisp", "src/integration/fdr", "src/integration/fdr3", "src/e2e/checkout", "src/api/cart"):
                with self.subTest(environment=environment, suite=suite):
                    PREPARE.validate_bundle(json.dumps({environment: self.bundle[environment]}), environment, Path(suite))

    def test_missing_secret_is_rejected(self):
        self.bundle["uat"].pop("tas-nodo-subscription-key")
        with self.assertRaisesRegex(RuntimeError, "missing from bundle"):
            PREPARE.validate_bundle(json.dumps({"uat": self.bundle["uat"]}), "uat", Path("src/integration/wisp"))

    def test_invalid_bundle_is_rejected(self):
        for raw in ("", "{invalid", "[]", '{"dev": {"key": "value"}}', '{"uat": {}}', '{"uat": {"key": null}}'):
            with self.subTest(raw=raw), self.assertRaises(RuntimeError):
                PREPARE.validate_bundle(raw, "uat", Path("src/integration/wisp"))

    def test_path_outside_src_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "inside src"):
            PREPARE.validate_bundle(json.dumps({"uat": self.bundle["uat"]}), "uat", Path("config"))

    def test_nested_placeholders(self):
        self.assertEqual(PREPARE._placeholders({"items": [{"token": "$tas-key"}, "literal"]}), {"tas-key"})

    def test_sync_discovers_yaml_secrets_without_manifests(self):
        with tempfile.TemporaryDirectory() as directory:
            suite_roots = tuple(Path(directory) / category for category in ("integration", "e2e", "api"))
            for suite_root in suite_roots:
                suite_path = suite_root / "suite"
                suite_path.mkdir(parents=True)
                (suite_path / "uat.yaml").write_text('token: "$Shared-Key"\nnested:\n  items:\n    - password: "$nested-key"\nurl: "https://example.test"\ncount: 2\nenabled: true\n')
                (suite_path / "dev.yaml").write_text('token: "$dev-only"\n')
                (suite_path / "uat.json").write_text('{"token": "$json-only"}')
            (suite_roots[2] / "suite" / "uat.yml").write_text('token: "$api-key"\n')
            resolver = Mock()
            resolver.resolve.side_effect = lambda name: f"synthetic-{name}"
            with patch.object(SYNC, "SUITE_ROOTS", suite_roots):
                bundle = SYNC._resolve_bundle(resolver, "uat", {"api-key": "cached-value"})
            self.assertEqual(bundle, {
                "Shared-Key": "synthetic-shared-key",
                "nested-key": "synthetic-nested-key",
                "api-key": "cached-value",
            })
            self.assertEqual(resolver.resolve.call_count, 2)
            resolver.resolve.assert_any_call("shared-key")
            resolver.resolve.assert_any_call("nested-key")

    def test_prepare_accepts_new_suite_without_manifest(self):
        original_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                suite_path = Path("src/api/new-suite")
                suite_path.mkdir(parents=True)
                (suite_path / "uat.yml").write_text('auth:\n  token: "$new-secret"\n')
                bundle = {"uat": {"new-secret": "synthetic-value"}}
                self.assertEqual(PREPARE.validate_bundle(json.dumps(bundle), "uat", suite_path), bundle)
            finally:
                os.chdir(original_directory)

    def test_sync_rejects_missing_environment_configs(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(SYNC, "SUITE_ROOTS", (Path(directory),)):
                with self.assertRaisesRegex(RuntimeError, "No suite YAML configs"):
                    SYNC._resolve_bundle(Mock(), "uat", {})

    def test_verify_uses_suite_yaml_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            suite_path = Path(directory)
            (suite_path / "uat.yaml").write_text('token: "$new-secret"\n')
            resolver = Mock()
            resolver.resolve.return_value = "synthetic-value"
            with (
                patch.object(SYNC, "SUITE_ROOTS", (suite_path,)),
                patch.object(SYNC, "get_secrets_resolver", return_value=resolver),
                patch.dict(os.environ, {"NRT_SECRETS_BUNDLE": json.dumps({"uat": {"new-secret": "synthetic-value"}})}, clear=True),
            ):
                SYNC._verify_environment_bundle("uat")
                with patch.dict(os.environ, {"NRT_SECRETS_BUNDLE": json.dumps({"uat": {"new-secret": "different-value"}})}):
                    with self.assertRaisesRegex(RuntimeError, "different_values=1"):
                        SYNC._verify_environment_bundle("uat")
            self.assertEqual(resolver.close_client.call_count, 2)

    def test_empty_placeholder_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Empty secret placeholder"):
            PREPARE._placeholders({"token": "$"})

    def test_dict_mode_overrides_key_vault_and_preserves_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle_path = Path(directory) / "bundle.yaml"
            bundle_path.write_text(json.dumps({"uat": self.bundle["uat"]}))
            with (
                patch.object(configuration, "SECRETS_PATH", str(bundle_path)),
                patch.dict(os.environ, {
                    "TARGET_ENV": "uat", "SECRETS_RESOLVER": "dict",
                    "AZURE_KEY_VAULT_URL": "https://unused.vault.azure.net/",
                }),
                patch.object(configuration.AzureKeyVaultSecretResolver, "__init__", side_effect=AssertionError("Azure must not be initialized")),
            ):
                self.assertEqual(configuration.load_configurations("src/integration/wisp").NODO_SUBSCRIPTION_KEY, "synthetic-value")
                self.assertEqual(configuration.load_configurations("src/integration/fdr").fdr.key_value, "synthetic-value")
                self.assertEqual(configuration.load_secrets({"nested": {"key": "$tas-nodo-subscription-key"}})["nested"]["key"], "synthetic-value")

    def test_no_secret_configuration_does_not_initialize_resolver(self):
        with patch.object(configuration, "get_secrets_resolver", side_effect=AssertionError("No resolver required")), patch.dict(os.environ, {"TARGET_ENV": "uat"}):
            configuration.load_configurations("src/e2e/checkout")

    def test_materialized_bundle_has_restrictive_permissions(self):
        original_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                Path("config").mkdir()
                destination = Path("config/.secrets.yaml")
                destination.write_text("old content")
                destination.chmod(0o644)
                expected = {"uat": self.bundle["uat"]}
                with patch.object(PREPARE, "validate_bundle", return_value=expected), patch.object(sys, "argv", ["nrt-prepare-secrets.py", "src/integration/wisp"]):
                    PREPARE.main()
                self.assertEqual(json.loads(destination.read_text()), expected)
                self.assertEqual(destination.stat().st_mode & 0o777, 0o600)
            finally:
                os.chdir(original_directory)

    def test_local_yaml_secrets_remain_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle_path = Path(directory) / "local.yaml"
            bundle_path.write_text("uat:\n  tas-nodo-subscription-key: synthetic-local\n")
            with patch.object(configuration, "SECRETS_PATH", str(bundle_path)), patch.dict(os.environ, {"TARGET_ENV": "uat", "SECRETS_RESOLVER": "auto", "AZURE_KEY_VAULT_URL": ""}):
                self.assertEqual(configuration.get_secrets_resolver().resolve("tas-nodo-subscription-key"), "synthetic-local")


if __name__ == "__main__":
    unittest.main()