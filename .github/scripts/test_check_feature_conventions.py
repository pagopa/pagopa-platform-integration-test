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

from check_feature_conventions import check_file, main  # noqa: E402

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
    def test_unmanaged_file_skipped(self):
        text = "# language: it\nFunzionalità: x\n\n  Scenario: senza tag\n    Dato a\n"
        self.assertEqual(check_file("src/a.feature", text), [])

    def test_valid_file_passes(self):
        self.assertEqual(check_file("src/a.feature", VALID), [])

    def test_missing_language(self):
        text = VALID.replace("# language: it\n", "")
        errors = check_file("src/a.feature", text)
        self.assertEqual(len(errors), 1)
        self.assertIn("src/a.feature:2:", errors[0])
        self.assertIn("language: it", errors[0])

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
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def test_main_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = self._write(tmp, "good.feature", VALID)
            bad = self._write(tmp, "bad.feature", VALID.replace("# language: it\n", ""))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main([good]), 0)
                self.assertEqual(main([good, bad]), 1)
            self.assertIn("bad.feature:2:", out.getvalue())

    def test_main_ignores_missing_files(self):
        self.assertEqual(main(["does/not/exist.feature"]), 0)


if __name__ == "__main__":
    unittest.main()
