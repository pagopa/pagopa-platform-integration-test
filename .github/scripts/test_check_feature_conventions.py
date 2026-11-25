"""Test del controllo convenzioni dei feature file gestiti da QA Hub.

Eseguire con: python .github/scripts/test_check_feature_conventions.py
"""

import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from check_feature_conventions import check_file, check_path, main  # noqa: E402

VALID = """\
# qa-hub: FEAT_001_FdR3
# language: it
@FDR3_001
Funzionalità: Pagamento
  Descrizione della funzionalità.

  Contesto:
    Dati un utente autenticato

  @runnable @positivo
  @FDR3_001_01
  #link:req-1|Requisito
  Scenario: Paga con successo
    Dato un carrello
    Quando paga
    Allora vede la conferma

  @negativo
  @FDR3_001_02
  Schema dello scenario: Paga con errore
    Dato un flusso <flowid>
    Allora riceve <esito>

    Esempi:
      | flowid | esito   |
      | a1     | errore  |
      | b22    | rifiuto |
"""


class CheckFileTest(unittest.TestCase):
    def test_unmanaged_file_is_skipped(self):
        """Do not impose hub conventions on a feature whose scope is not migrated."""
        text = "# language: it\nFunzionalità: x\n\n  Scenario: senza tag\n    Dato a\n"
        self.assertEqual(check_file("src/a.feature", text), [])

    def test_valid_file_passes(self):
        self.assertEqual(check_file("src/a.feature", VALID), [])

    def test_canonical_path_and_nested_feature_directory_pass(self):
        self.assertEqual(check_path("src/api/cart/features/refunds/refund.feature"), [])

    def test_path_outside_canonical_features_directory_fails(self):
        errors = check_path("src/api/cart/testdata/features/refund.feature")
        self.assertEqual(len(errors), 1)
        self.assertIn("features/**/*.feature", errors[0])

    def test_invalid_source_type_or_missing_suite_fails(self):
        for path in ("src/unit/cart/features/a.feature", "src/api/features/a.feature"):
            with self.subTest(path=path):
                self.assertEqual(len(check_path(path)), 1)

    def test_missing_language(self):
        text = VALID.replace("# language: it\n", "")
        errors = check_file("src/a.feature", text)
        self.assertEqual(len(errors), 1)
        self.assertIn("src/a.feature:2:", errors[0])
        self.assertIn("lingua Gherkin", errors[0])

    def test_english_feature_passes_with_explicit_language(self):
        text = VALID.replace("# language: it", "# language: en").replace(
            "Funzionalità: Pagamento", "Feature: Pagamento"
        )
        self.assertEqual(check_file("src/a.feature", text), [])

    def test_missing_feature_tag(self):
        errors = check_file("src/a.feature", VALID.replace("@FDR3_001\nFunz", "Funz"))
        self.assertTrue(any("tag di feature" in e for e in errors), errors)

    def test_scenario_without_identity_tag(self):
        text = VALID.replace("  @FDR3_001_02\n", "")
        errors = check_file("src/a.feature", text)
        self.assertEqual(len(errors), 1)
        self.assertIn("tag identità", errors[0])
        self.assertIn("Schema dello scenario", errors[0])

    def test_two_identity_tags_on_one_scenario(self):
        text = VALID.replace("  @FDR3_001_02\n", "  @FDR3_001_02 @FDR3_001_03\n")
        errors = check_file("src/a.feature", text)
        self.assertTrue(any("un solo tag identità" in e for e in errors), errors)

    def test_duplicate_identity_tag(self):
        text = VALID.replace("@FDR3_001_02", "@FDR3_001_01")
        errors = check_file("src/a.feature", text)
        self.assertTrue(any("duplicato" in e for e in errors), errors)

    def test_wrong_prefix(self):
        text = VALID.replace("@FDR3_001_02", "@CHK_001_02")
        errors = check_file("src/a.feature", text)
        self.assertTrue(any("@FDR3_001_" in e for e in errors), errors)

    def test_wrong_feature_number(self):
        text = VALID.replace("@FDR3_001_02", "@FDR3_002_02")
        errors = check_file("src/a.feature", text)
        self.assertTrue(any("@FDR3_001_" in e for e in errors), errors)

    def test_bad_header_code(self):
        text = VALID.replace("# qa-hub: FEAT_001_FdR3", "# qa-hub: FEAT_1_FdR3")
        errors = check_file("src/a.feature", text)
        self.assertEqual(len(errors), 1)
        self.assertIn("src/a.feature:1:", errors[0])

    def test_crlf_and_bom_are_tolerated(self):
        text = "﻿" + VALID.replace("\n", "\r\n")
        self.assertEqual(check_file("src/a.feature", text), [])


class MainTest(unittest.TestCase):
    def _write(self, folder, name, text):
        """Write a feature fixture under the canonical suite directory."""
        path = os.path.join(folder, "src", "api", "test-suite", "features", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def test_main_exit_code(self):
        """Return success for a valid path and failure for invalid feature content."""
        with tempfile.TemporaryDirectory() as tmp:
            good = self._write(tmp, "good.feature", VALID)
            bad = self._write(tmp, "bad.feature", VALID.replace("# language: it\n", ""))
            out = io.StringIO()
            current_dir = os.getcwd()
            os.chdir(tmp)
            try:
                good_relative = os.path.relpath(good)
                bad_relative = os.path.relpath(bad)
                with contextlib.redirect_stdout(out):
                    self.assertEqual(main([good_relative]), 0)
                    self.assertEqual(main([good_relative, bad_relative]), 1)
            finally:
                os.chdir(current_dir)
            self.assertIn("bad.feature:2:", out.getvalue())

    def test_main_accepts_unmanaged_feature_in_canonical_path(self):
        """Check the path but do not require Hub conventions before that scope migrates."""
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                tmp,
                "legacy.feature",
                "# language: it\nFunzionalità: legacy\n\n  Scenario: senza tag\n    Dato a\n",
            )
            current_dir = os.getcwd()
            os.chdir(tmp)
            try:
                self.assertEqual(main([os.path.relpath(path)]), 0)
            finally:
                os.chdir(current_dir)

    def test_main_ignores_missing_files(self):
        """Ignore deleted feature paths passed by a diff command."""
        self.assertEqual(main(["src/api/test-suite/features/missing.feature"]), 0)

    def test_main_rejects_feature_outside_canonical_path(self):
        """Reject an existing feature file outside the manifest discovery location."""
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "src", "api", "test-suite", "examples", "bad.feature")
            os.makedirs(os.path.dirname(path))
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(VALID)
            current_dir = os.getcwd()
            os.chdir(tmp)
            try:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(main([os.path.relpath(path)]), 1)
                self.assertIn("percorso non valido", output.getvalue())
            finally:
                os.chdir(current_dir)


if __name__ == "__main__":
    unittest.main()
