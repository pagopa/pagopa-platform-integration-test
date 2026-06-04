from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
FEATURE_ROOT = ROOT_DIR / "src" / "api"
OUTPUT_DIR = ROOT_DIR / "docs" / "confluence" / "api"

STEP_KEYWORDS = {
    "dato": "given",
    "data": "given",
    "date": "given",
    "dati": "given",
    "given": "given",
    "quando": "action",
    "when": "action",
    "allora": "expected",
    "then": "expected",
    "e": "same",
    "ed": "same",
    "and": "same",
}


@dataclass
class Step:
    keyword: str
    text: str
    phase: str


@dataclass
class Scenario:
    kind: str
    name: str
    tags: list[str]
    steps: list[Step] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)


@dataclass
class FeatureDocument:
    path: Path
    language: str = "it"
    tags: list[str] = field(default_factory=list)
    name: str = ""
    description: list[str] = field(default_factory=list)
    background: list[Step] = field(default_factory=list)
    scenarios: list[Scenario] = field(default_factory=list)


def extract_tags(line: str) -> list[str]:
    return [token for token in line.split() if token.startswith("@")]


def strip_step(line: str) -> tuple[str, str] | None:
    match = re.match(r"^(Dato|Data|Date|Dati|Given|Quando|When|Allora|Then|E|Ed|And)\b\s*(.*)$", line, re.IGNORECASE)
    if not match:
        return None
    return match.group(1), match.group(2).strip()


def step_phase(keyword: str, current_phase: str) -> str:
    normalized = keyword.lower()
    phase = STEP_KEYWORDS.get(normalized, current_phase)
    if phase == "same":
        return current_phase
    return phase


def parse_feature_file(path: Path) -> FeatureDocument:
    document = FeatureDocument(path=path)
    pending_tags: list[str] = []
    current_scenario: Scenario | None = None
    current_section = "header"
    current_phase = "given"

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# language:"):
            document.language = line.split(":", 1)[1].strip()
            continue

        if line.startswith("#"):
            continue

        if line.startswith("@"):
            pending_tags.extend(extract_tags(line))
            continue

        if line.startswith(("Funzionalità:", "Funzionalita:", "Feature:")):
            document.name = line.split(":", 1)[1].strip()
            document.tags = pending_tags
            pending_tags = []
            current_section = "feature_description"
            continue

        if line.startswith(("Contesto:", "Background:")):
            current_section = "background"
            current_phase = "given"
            continue

        if line.startswith(("Schema dello scenario:", "Scenario Outline:")):
            current_scenario = Scenario(
                kind="Schema dello scenario",
                name=line.split(":", 1)[1].strip(),
                tags=pending_tags,
            )
            document.scenarios.append(current_scenario)
            pending_tags = []
            current_section = "scenario"
            current_phase = "given"
            continue

        if line.startswith("Scenario:"):
            current_scenario = Scenario(
                kind="Scenario",
                name=line.split(":", 1)[1].strip(),
                tags=pending_tags,
            )
            document.scenarios.append(current_scenario)
            pending_tags = []
            current_section = "scenario"
            current_phase = "given"
            continue

        if line.startswith(("Esempi:", "Examples:")):
            current_section = "examples"
            continue

        if current_section == "examples" and current_scenario:
            current_scenario.examples.append(line)
            continue

        parsed_step = strip_step(line)
        if parsed_step:
            keyword, text = parsed_step
            current_phase = step_phase(keyword, current_phase)
            step = Step(keyword=keyword, text=text, phase=current_phase)
            if current_section == "background":
                document.background.append(step)
            elif current_scenario:
                current_scenario.steps.append(step)
            continue

        if current_section == "feature_description":
            document.description.append(line)

    return document


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def format_expected_html(text: str) -> str:
    """Format expected outcome text: bold HTTP status codes and mark uppercase tokens as code."""
    if not text:
        return ""
    # Match quoted uppercase tokens first, then HTTP codes, then bare uppercase tokens
    pattern = re.compile(r"([\"'])([A-Z][A-Z0-9_]{1,})\1|([1-5]\d{2})|([A-Z][A-Z0-9_]{1,})")
    parts: list[str] = []
    last = 0
    for m in pattern.finditer(text):
        start, end = m.start(), m.end()
        if start > last:
            parts.append(escape(text[last:start]))
        if m.group(3):
            # HTTP status code -> bold
            parts.append(f"<strong>{escape(m.group(3))}</strong>")
        elif m.group(4):
            # Bare uppercase token -> code
            parts.append(f"<code>{escape(m.group(4))}</code>")
        elif m.group(2):
            # Quoted uppercase token -> code (drop surrounding quotes)
            parts.append(f"<code>{escape(m.group(2))}</code>")
        last = end

    if last < len(text):
        parts.append(escape(text[last:]))

    return "".join(parts)


def format_precondition_html(text: str) -> str:
    """Wrap uppercase tokens (e.g. NOTICE_CODE_PREFIX, CARDS) in <code> tags for preconditions."""
    if not text:
        return ""
    # Match quoted uppercase tokens first so surrounding quotes are removed
    pattern = re.compile(r"([\"'])([A-Z][A-Z0-9_]{1,})\1|([A-Z][A-Z0-9_]{1,})")
    parts: list[str] = []
    last = 0
    for m in pattern.finditer(text):
        start, end = m.start(), m.end()
        if start > last:
            parts.append(escape(text[last:start]))
        if m.group(3):
            parts.append(f"<code>{escape(m.group(3))}</code>")
        elif m.group(2):
            parts.append(f"<code>{escape(m.group(2))}</code>")
        last = end

    if last < len(text):
        parts.append(escape(text[last:]))

    return "".join(parts)


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT_DIR).as_posix()


def document_id(document: FeatureDocument) -> str:
    for tag in document.tags:
        if re.match(r"@FEAT_\d+_Checkout$", tag):
            return tag[1:]
    for scenario in document.scenarios:
        for tag in scenario.tags:
            match = re.match(r"@(FEAT_\d+_Checkout)_SCENARIO_\d+$", tag)
            if match:
                return match.group(1)
    return document.path.stem


def scenario_id(scenario: Scenario, index: int) -> str:
    for tag in scenario.tags:
        match = re.match(r"@FEAT_\d+_Checkout_SCENARIO_(\d+)$", tag)
        if match:
            return f"SCENARIO {int(match.group(1)):02d}"
    return f"SCENARIO {index:02d}"


def suite_name(document: FeatureDocument) -> str:
    return document.path.relative_to(FEATURE_ROOT).parts[0]


def render_status(text: str) -> str:
    return f'<span class="status-macro aui-lozenge aui-lozenge-visual-refresh aui-lozenge-success">{escape(text)}</span>'


def render_info_table(document: FeatureDocument) -> str:
    doc_id = document_id(document)
    rows = [
        ("ID documento", doc_id),
        ("Nome documento", f"{doc_id} - {document.name}"),
        ("Ambito", f"API / {suite_name(document)}"),
        ("Stato del documento", render_status("TEST SUITE IMPLEMENTED"), True),
        ("Tipologia Test", render_status("AUTOMATICO"), True),
        ("Feature File", relative_path(document.path)),
        ("Lingua feature", document.language),
        ("Numero scenari", str(len(document.scenarios))),
    ]

    html_rows: list[str] = []
    for row in rows:
        label, value = row[0], row[1]
        value_is_html = len(row) > 2 and row[2]
        rendered_value = value if value_is_html else escape(value)
        html_rows.append(
            "<tr>"
            f'<td data-highlight-colour="#f4f5f7" class="confluenceTd"><p><strong>{escape(label)}</strong></p></td>'
            f'<td class="confluenceTd"><p>{rendered_value}</p></td>'
            "</tr>"
        )

    return """
<div class="plugin-tabmeta-details">
<div class="table-wrap">
<table data-table-width="760" data-layout="default" class="confluenceTable">
<tbody>
{rows}
</tbody>
</table>
</div>
</div>
""".format(rows="\n".join(html_rows))


def render_step_list(steps: list[Step], is_expected: bool = False, is_precondition: bool = False) -> str:
    if not steps:
        return "<p>&nbsp;</p>"
    # Render only the step text (no Gherkin keyword) inside table cells
    if is_expected:
        items = "\n".join(f"<li><p>{format_expected_html(step.text)}</p></li>" for step in steps)
    elif is_precondition:
        items = "\n".join(f"<li><p>{format_precondition_html(step.text)}</p></li>" for step in steps)
    else:
        items = "\n".join(f"<li><p>{escape(step.text)}</p></li>" for step in steps)
    return f"<ul>{items}</ul>"


def grouped_steps(scenario: Scenario) -> tuple[list[Step], list[Step], list[Step]]:
    return (
        [step for step in scenario.steps if step.phase == "given"],
        [step for step in scenario.steps if step.phase == "action"],
        [step for step in scenario.steps if step.phase == "expected"],
    )


def action_groups(scenario: Scenario) -> list[tuple[list[Step], list[Step]]]:
    """Split scenario steps (excluding given) into (action_steps, expected_steps) pairs.

    A new pair is started each time a new 'action' (Quando/When) step is encountered
    after at least one expected step has already been collected in the current pair.
    This produces one table row per Quando block.
    """
    groups: list[tuple[list[Step], list[Step]]] = []
    current_actions: list[Step] = []
    current_expected: list[Step] = []

    for step in scenario.steps:
        if step.phase == "given":
            continue
        if step.phase == "action":
            # If we already have expected steps, the previous action+expected block is complete
            if current_expected:
                groups.append((current_actions, current_expected))
                current_actions = []
                current_expected = []
            current_actions.append(step)
        elif step.phase == "expected":
            current_expected.append(step)

    if current_actions or current_expected:
        groups.append((current_actions, current_expected))

    return groups


def render_examples(scenario: Scenario) -> str:
    if not scenario.examples:
        return ""
    examples = "\n".join(escape(line) for line in scenario.examples)
    return f"""
<div class="code panel pdl">
<div class="codeContent panelContent pdl">
<pre class="syntaxhighlighter-pre">Esempi:
{examples}</pre>
</div>
</div>
"""


def render_scenario(scenario: Scenario, index: int) -> str:
    givens = [step for step in scenario.steps if step.phase == "given"]
    groups = action_groups(scenario)
    tags = " ".join(f"<code>{escape(tag)}</code>" for tag in scenario.tags)
    scenario_kind = f" ({escape(scenario.kind)})" if scenario.kind != "Scenario" else ""

    header = """\
<tr>
<th data-highlight-colour="#f0f1f2" class="confluenceTh"><p><strong>Precondizioni</strong></p><p><em>(Given)</em></p></th>
<th data-highlight-colour="#f0f1f2" class="confluenceTh"><p><strong>Step</strong></p><p>(Action/When)</p></th>
<th data-highlight-colour="#f0f1f2" class="confluenceTh"><p><em><strong>Esito atteso</strong></em></p><p><em>(Then)</em></p></th>
</tr>"""

    if not groups:
        # No action/expected steps at all (edge case)
        data_rows = (
            "<tr>\n"
            f'<td class="confluenceTd">{render_step_list(givens, is_precondition=True)}</td>\n'
            '<td class="confluenceTd"><p>&nbsp;</p></td>\n'
            '<td class="confluenceTd"><p>&nbsp;</p></td>\n'
            "</tr>"
        )
    elif len(groups) == 1:
        actions, expected = groups[0]
        data_rows = (
            "<tr>\n"
            f'<td class="confluenceTd">{render_step_list(givens, is_precondition=True)}</td>\n'
            f'<td class="confluenceTd">{render_step_list(actions)}</td>\n'
            f'<td class="confluenceTd">{render_step_list(expected, is_expected=True)}</td>\n'
            "</tr>"
        )
    else:
        # Multiple Quando blocks: first row has given cell with rowspan
        n = len(groups)
        rows: list[str] = []
        for i, (actions, expected) in enumerate(groups):
            if i == 0:
                given_cell = (
                    f'<td class="confluenceTd" rowspan="{n}">'
                    f"{render_step_list(givens, is_precondition=True)}</td>\n"
                )
            else:
                given_cell = ""
            rows.append(
                "<tr>\n"
                + given_cell
                + f'<td class="confluenceTd">{render_step_list(actions)}</td>\n'
                + f'<td class="confluenceTd">{render_step_list(expected, is_expected=True)}</td>\n'
                + "</tr>"
            )
        data_rows = "\n".join(rows)

    return f"""
<h2>{escape(scenario_id(scenario, index))} - {escape(scenario.name)}{scenario_kind}</h2>
<p><strong>Tag:</strong> {tags}</p>
<div class="table-wrap">
<table data-table-width="1158" data-layout="center" class="confluenceTable scenario-table">
<tbody>
{header}
{data_rows}
</tbody>
</table>
</div>
{render_examples(scenario)}
"""


def render_feature_description(document: FeatureDocument) -> str:
    if not document.description:
        return ""
    paragraphs = "\n".join(f"<p>{escape(line)}</p>" for line in document.description)
    return f"<h2>Descrizione</h2>\n{paragraphs}"


def render_background(document: FeatureDocument) -> str:
    if not document.background:
        return ""
    return f"<h2>Background</h2>\n{render_step_list(document.background, is_precondition=True)}"


def render_html(document: FeatureDocument) -> str:
    title = f"{document_id(document)} - {document.name}"
    scenarios = "\n".join(render_scenario(scenario, index) for index, scenario in enumerate(document.scenarios, start=1))
    return f"""<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns="w3-org-ns:HTML">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>{escape(title)}</title>
    <style>
        @page Section1 {{
            size: 8.5in 11.0in;
            margin: 1.0in;
            mso-header-margin: .5in;
            mso-footer-margin: .5in;
            mso-paper-source: 0;
        }}

        body {{
            color: #172b4d;
            background: #fff;
            font-family: Arial, Helvetica, FreeSans, sans-serif;
            font-size: 14px;
            line-height: 1.45;
            margin: 24px;
        }}

        div.Section1 {{ page: Section1; }}

        h1 {{
            color: #172b4d;
            font-size: 28px;
            font-weight: 500;
            margin: 0 0 24px;
        }}

        h2 {{
            color: #172b4d;
            font-size: 20px;
            font-weight: 500;
            margin: 28px 0 12px;
        }}

        hr {{
            border: 0;
            border-top: 1px solid #dfe1e6;
            margin: 24px 0;
        }}

        table {{
            border: solid 1px #c1c7d0;
            border-collapse: collapse;
        }}

        table td,
        table th {{
            border: solid 1px #c1c7d0;
            padding: 5px;
            vertical-align: top;
        }}

        td {{ page-break-inside: avoid; }}
        tr {{ page-break-after: avoid; }}

        .table-wrap {{
            margin: 8px 0 18px;
            overflow-x: auto;
        }}

        .confluenceTable {{
            background: #fff;
            width: 100%;
        }}

        .scenario-table th {{ width: 33.333%; }}

        .confluenceTh {{
            background: #f0f1f2;
            color: #172b4d;
            text-align: left;
        }}

        .confluenceTd[data-highlight-colour="#f4f5f7"] {{ background: #f4f5f7; }}

        .status-macro {{
            border-radius: 3px;
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            line-height: 1;
            padding: 3px 6px;
            text-transform: uppercase;
        }}

        .aui-lozenge-success {{
            background: #e3fcef;
            color: #006644;
        }}

        .code.panel.pdl {{
            border: 1px solid #dfe1e6;
            margin: 8px 0 20px;
        }}

        .codeContent.panelContent.pdl {{
            background: #f4f5f7;
            padding: 10px 12px;
        }}

        pre {{
            font-family: Monaco, "Courier New", monospace;
            font-size: 12px;
            margin: 0;
            white-space: pre-wrap;
        }}

        code {{
            background: #f4f5f7;
            border-radius: 3px;
            color: #172b4d;
            font-family: Monaco, "Courier New", monospace;
            font-size: 12px;
            padding: 1px 3px;
        }}

        ul {{ margin: 0; padding-left: 20px; }}
        p {{ margin: 0 0 8px; }}
        li p {{ margin: 0 0 4px; }}

        @media print {{
            body {{
                background: #fff !important;
                color: #000 !important;
                margin: 0 !important;
            }}

            h1, h2, h3, h4, h5, h6 {{ page-break-after: avoid; }}

            .table-wrap,
            p,
            .panel .codeContent,
            .panel .codeContent pre {{ overflow: visible !important; }}
        }}
    </style>
</head>
<body>
    <h1>{escape(title)}</h1>
    <div class="Section1">
        <h1>Informazioni generali</h1>
        {render_info_table(document)}
        <hr>
        {render_feature_description(document)}
        {render_background(document)}
        {scenarios}
    </div>
</body>
</html>
"""


def output_path_for(document: FeatureDocument) -> Path:
    return OUTPUT_DIR / f"{document.path.stem}.html"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    feature_paths = sorted(FEATURE_ROOT.glob("*/features/*.feature"))
    if not feature_paths:
        raise SystemExit(f"No feature files found under {FEATURE_ROOT}")

    for feature_path in feature_paths:
        document = parse_feature_file(feature_path)
        output_path = output_path_for(document)
        output_path.write_text(render_html(document), encoding="utf-8", newline="\n")
        print(f"Generated {relative_path(output_path)}")


if __name__ == "__main__":
    main()