"""Controllo delle convenzioni dei feature file gestiti da QA Hub.

Ogni feature file deve iniziare con `# qa-hub: FEAT_<NNN>_<Ambito>`. Regole:

- percorso `src/<tipo>/<suite>/features/**/*.feature`, dove tipo è `api`, `integration` o `e2e`;
- seconda riga con la dichiarazione di lingua Gherkin (`it` o `en`);
- un tag di feature `@<AMBITO>_<NNN>` coerente con l'header;
- ogni `Scenario:` / `Schema dello scenario:` preceduto da esattamente un tag identità
  `@<AMBITO>_<NNN>_<NN>` con ambito e numero di feature dell'header;
- tag identità univoci nel file.

Solo libreria standard. Uso: python check_feature_conventions.py <file.feature>...
Esce con 1 se trova errori (stampati come `percorso:riga: messaggio`).
"""

from __future__ import annotations

import os
import re
import sys

HEADER_RE = re.compile(r"^#\s*qa-hub:\s*(\S+)\s*$")
CODE_RE = re.compile(r"^FEAT_(?!000)(\d{3})_([A-Za-z][A-Za-z0-9]{1,19})$")
LANGUAGE_RE = re.compile(r"^#\s*language:\s*(it|en)\s*$")
SCENARIO_RE = re.compile(r"^\s*(Scenario|Schema dello scenario|Esempio)\s*:")
FEATURE_RE = re.compile(r"^\s*(Funzionalità|Feature)\s*:")
IDENTITY_RE = re.compile(r"^@([A-Z0-9]+)_(\d{3})_(\d{2})$")
FEATURE_TAG_RE = re.compile(r"^@([A-Z0-9]+)_(\d{3})$")
SOURCE_TYPES = {"api", "integration", "e2e"}


def check_path(path: str) -> list[str]:
    """Require a repository-relative feature path under the canonical suite features directory."""
    normalized = path.replace("\\", "/")
    parts = normalized.split("/")
    if (
        len(parts) < 5
        or parts[0] != "src"
        or parts[1] not in SOURCE_TYPES
        or not parts[2]
        or parts[3] != "features"
        or any(part in {"", ".", ".."} for part in parts)
        or not parts[-1].endswith(".feature")
    ):
        return [
            f"{path}: percorso non valido: atteso "
            "src/<api|integration|e2e>/<suite>/features/**/*.feature"
        ]
    return []


def _normalize(text: str) -> list[str]:
    return text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n").split("\n")


def _tags(line: str) -> list[str]:
    return [t for t in line.split() if t.startswith("@")]


def check_file(path: str, text: str) -> list[str]:
    lines = _normalize(text)
    header = HEADER_RE.match(lines[0]) if lines else None
    if header is None:
        return [f"{path}:1: la prima riga deve essere '# qa-hub: FEAT_<NNN>_<Ambito>'"]

    def err(lineno: int, message: str) -> str:
        return f"{path}:{lineno}: {message}"

    code = CODE_RE.match(header.group(1))
    if code is None:
        return [err(1, f"codice '{header.group(1)}' non valido: atteso FEAT_<NNN>_<Ambito>")]
    number, scope = code.group(1), code.group(2).upper()
    errors: list[str] = []

    if len(lines) < 2 or not LANGUAGE_RE.match(lines[1]):
        errors.append(err(2, "la seconda riga deve dichiarare la lingua Gherkin ('it' o 'en')"))

    pending: list[tuple[int, list[str]]] = []  # righe di tag accumulate prima di un elemento
    seen: dict[str, int] = {}
    feature_tag_ok = False

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue  # commenti (#link, header) e righe vuote non interrompono i tag
        if line.startswith("@"):
            pending.append((idx, _tags(line)))
            continue
        tags = [t for _, tags_ in pending for t in tags_]
        if FEATURE_RE.match(raw):
            feature_tag_ok = any(
                (m := FEATURE_TAG_RE.match(t)) and m.group(1) == scope and m.group(2) == number
                for t in tags
            )
            if not feature_tag_ok:
                errors.append(err(idx, f"manca il tag di feature @{scope}_{number}"))
        elif SCENARIO_RE.match(raw):
            keyword = SCENARIO_RE.match(raw).group(1)
            identities = [t for t in tags if IDENTITY_RE.match(t)]
            if not identities:
                errors.append(err(idx, f"'{keyword}' senza tag identità @{scope}_{number}_<NN>"))
            elif len(identities) > 1:
                errors.append(err(idx, f"'{keyword}' deve avere un solo tag identità"))
            for tag in identities:
                m = IDENTITY_RE.match(tag)
                if m.group(1) != scope or m.group(2) != number:
                    errors.append(
                        err(idx, f"tag identità {tag} non coerente: atteso @{scope}_{number}_<NN>")
                    )
                if tag in seen:
                    errors.append(err(idx, f"tag identità {tag} duplicato (già alla riga {seen[tag]})"))
                else:
                    seen[tag] = idx
        pending = []
    return errors


def main(argv: list[str]) -> int:
    """Validate changed feature paths and contents, returning one when any error is found."""
    errors: list[str] = []
    for path in argv:
        if not path.endswith(".feature") or not os.path.isfile(path):
            continue  # file rimossi o non feature: niente da controllare
        relative_path = os.path.relpath(path) if os.path.isabs(path) else path
        errors.extend(check_path(relative_path))
        with open(path, encoding="utf-8") as fh:
            errors.extend(check_file(path, fh.read()))
    for line in errors:
        print(line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
