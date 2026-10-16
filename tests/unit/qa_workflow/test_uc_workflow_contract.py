"""Static contract regressions and isolated syntax probes, not agent execution."""
import re
from pathlib import Path

import pytest
from behave.parser import parse_feature


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / '.github' / 'skills'
DOCS = ROOT / 'docs' / 'use-cases'
SKILL_NAMES = ('uc-to-feature', 'uc-scenario-context', 'uc-test-data')
REPORTS = {
    '00-run': ('run', None, []),
    '01-context': ('context', 'uc-scenario-context', []),
    '02-test-data': ('test-data', 'uc-test-data', ['01-context.md']),
    '03-feature-report': (
        'feature-report', 'uc-to-feature', ['01-context.md', '02-test-data.md']
    ),
}
HEADINGS = {
    '00-run': [
        'Agreed inputs', 'Scenario inventory', 'Artifacts', 'Questions', 'History'
    ],
    '01-context': [
        'Sources', 'Functional evidence', 'Mapping', 'Oracles',
        'Data requirements', 'Questions', 'Readiness',
    ],
    '02-test-data': [
        'Sources', 'Data resolution', 'Combinations', 'Decisions',
        'Scenario warnings', 'Optional catalogue', 'Readiness',
    ],
    '03-feature-report': [
        'Feature outputs', 'Mapping', 'Coverage', 'Data and oracles',
        'Questions', 'Checks', 'Engineer handoff', 'Readiness',
    ],
}


def _read(path: Path) -> str:
    """Read a repository document without modifying its contents."""
    return path.read_text(encoding='utf-8-sig')


def _table_rows(text: str, header: str) -> list[list[str]]:
    """Read one named Markdown table, rejecting malformed column counts."""
    lines = text.splitlines()
    start = lines.index(header)
    width = len(re.split(r'(?<!\\)\|', header)) - 2
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith('|'):
            break
        cells = [cell.strip() for cell in re.split(r'(?<!\\)\|', line)[1:-1]]
        assert len(cells) == width, line
        rows.append(cells)
    return rows


@pytest.mark.parametrize('name', SKILL_NAMES)
def test_skill_metadata_and_resume_gate(name: str) -> None:
    """Keep discoverable skill metadata and an explicit continuity gate."""
    text = _read(SKILLS / name / 'SKILL.md')
    assert text.startswith('---\n')
    metadata = text.split('---', 2)[1]
    assert f"name: {name}\n" in metadata
    description = metadata.split('description: >-', 1)[1].strip()
    assert 0 < len(description) <= 1024
    assert 'human continuity' in text
    assert 'ownership rules' in text


@pytest.mark.parametrize('name', REPORTS)
def test_report_schema_and_dependencies_remain_v1(name: str) -> None:
    """Preserve existing report fields, headings and acyclic dependencies."""
    text = _read(DOCS / 'workflow-templates' / f"{name}.template.md")
    metadata = text.split('---', 2)[1]
    assert set(re.findall(r'^([a-z_]+):', metadata, re.MULTILINE)) == {
        'schema', 'artifact', 'producer_skill', 'task_id', 'uc_id', 'run_id',
        'uc_input', 'uc_revision', 'environment', 'revision', 'status',
        'updated_at', 'inputs',
    }
    artifact, producer, dependencies = REPORTS[name]
    assert 'schema: uc-workflow/v1\n' in metadata
    assert f"artifact: {artifact}\n" in metadata
    if producer is not None:
        assert f"producer_skill: {producer}\n" in metadata
    actual_inputs = re.findall(r'^  - path: "\{run-directory\}/([^"]+)"', metadata, re.MULTILINE)
    assert actual_inputs == dependencies
    assert '00-run.md' not in metadata
    assert re.findall(r'^## (.+)$', text, re.MULTILINE) == HEADINGS[name]


def test_report_columns_remain_compatible() -> None:
    """Retain columns needed by existing v1 producers and consumers."""
    expected_headers = {
        '00-run': '| Artifact | Producer skill | Path | Revision | State |',
        '01-context': (
            '| Oracle id | Scenario id | AC or postcondition | Property and expected value '
            '| Timing semantics | Evidence ids | State |'
        ),
        '02-test-data': (
            '| Data id | Scenario id | Parameter and constraints | Value or TODO token '
            '| Source id and passage | Admission | Fitness | Availability evidence '
            '| Unresolved reason |'
        ),
        '03-feature-report': (
            '| UC element | Scenario id | Feature path | Scenario title '
            '| Examples row or not-applicable | Coverage and reason |'
        ),
    }
    for name, header in expected_headers.items():
        text = _read(DOCS / 'workflow-templates' / f"{name}.template.md")
        _table_rows(text, header)


def test_all_local_contract_links_and_tables() -> None:
    """Find broken local links and malformed tables across workflow assets."""
    paths = [
        path for name in SKILL_NAMES for path in (SKILLS / name).glob('*.md')
    ]
    paths.extend((DOCS / 'workflow-templates').glob('*.md'))
    paths.extend([
        DOCS / 'uc-workflow.md', DOCS / 'uc-workflow-validation.md',
        ROOT / 'docs' / 'agent-personas' / 'qa-analyst.md',
        ROOT / '.github' / 'agents' / 'QA-analyst.agent.md',
        ROOT / '.github' / 'instructions' / 'gherkin.instructions.md',
    ])
    for path in paths:
        text = _read(path)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'):
                continue
            assert (path.parent / target.split('#', 1)[0]).exists(), (path, target)
        width = None
        for line in text.splitlines():
            if not line.startswith('|'):
                width = None
                continue
            count = len(re.split(r'(?<!\\)\|', line)) - 2
            if width is None:
                width = count
            assert count == width, (path, line)
    assert not (DOCS / 'UC-template.md').exists()
    assert (SKILLS / 'uc-to-feature' / 'UC-template.md').is_file()


def test_registry_permissions_separate_production_and_invalidation() -> None:
    """Protect inventory ownership and forbid taking over other producers."""
    text = _read(DOCS / 'uc-workflow.md')
    rows = _table_rows(text, '| Sezione o operazione | Chi puo aggiornarla | Limite |')
    permissions = {row[0]: row[1:] for row in rows}
    assert len(permissions) == 6
    assert permissions['Scenario inventory'][0] == (
        'uc-to-feature (iniziale); uc-scenario-context'
    )
    assert 'senza registrarli autonomamente' in permissions['Scenario inventory'][1]
    assert permissions['Questions'][0] == 'Tutte e tre le skill'
    assert permissions['Artifacts: produzione'][0] == "Skill proprietaria dell'output"
    assert 'senza cambiare produttore, percorso o revisione' in (
        permissions['Artifacts: invalidazione'][1]
    )
    assert "update only this output's registry row" not in (
        _read(SKILLS / 'uc-scenario-context' / 'SKILL.md')
    )


def test_invalidation_reaches_features_without_registry_cycles() -> None:
    """Keep the documented invalidation graph and administrative no-op."""
    text = _read(DOCS / 'uc-workflow.md')
    rows = _table_rows(text, '| Contenuto cambiato | Output da invalidare nel registro |')
    actual = {row[0]: row[1] for row in rows}
    assert actual == {
        'UC, ambiente o decisione funzionale': 'context, test-data, feature-report, feature',
        '01-context.md': 'test-data, feature-report, feature',
        'Fonte o decisione solo dati': 'test-data, feature-report, feature',
        '02-test-data.md': 'feature-report, feature',
        'Feature registrata modificata manualmente': 'feature interessata, feature-report',
        '03-feature-report.md modificato manualmente': 'feature-report, feature',
        'History o sola conferma di continuita': 'Nessuno',
    }
    assert 'la run passa a `in_progress`' in text
    assert 'not_created` resta tale' in text
    assert 'Non creare cicli di auto-invalidazione' in text


def test_continuity_is_scoped_human_confirmation_not_integrity_proof() -> None:
    """Keep refusal, legacy handling and no automatic freshness guarantees."""
    text = _read(DOCS / 'uc-workflow.md')
    for clause in (
        'non una certificazione automatica di integrita',
        'una risposta generica non copre file non elencati',
        'Q di\nQuestions e in History',
        'bloccare la ripresa',
        'non approva nuovi candidati',
        'non rinnova la\ndisponibilita',
        'non una conversione silenziosa',
        'Non cancellare file o modifiche\nmanuali automaticamente',
    ):
        assert clause in text
    skill = _read(SKILLS / 'uc-to-feature' / 'SKILL.md')
    assert 'Missing confirmation blocks resumption even in assemble-only' in skill
    assert 'not new schema\nfields' in skill


def test_data_ids_describe_requirements_not_each_value() -> None:
    """Guard the requirement namespace while allowing per-case resolutions."""
    text = _read(SKILLS / 'uc-test-data' / 'SKILL.md')
    assert 'never allocate\n  new D ids here' in text
    assert 'A D identifies the requirement, not each selected value' in text
    assert 'Each resolution retains its own' in text
    assert 'Repeating\n  the token does not assert equal concrete values' in text
    assert 'Distinct values get distinct ids' not in text
    context = _read(SKILLS / 'uc-scenario-context' / 'SKILL.md')
    assert 'Only context allocates new D ids' in context
    assert 'explicit relationships' in context


def test_canonical_availability_and_catalogue_states() -> None:
    """Avoid synonyms that violate the fixed report vocabulary."""
    text = _read(SKILLS / 'uc-test-data' / 'SKILL.md')
    for value in (
        'documented-not-checked', 'user-confirmed', 'unknown-to-prepare',
        'not-requested', 'not-saved', 'pending-confirmation',
    ):
        assert f"`{value}`" in text
    for obsolete in (
        '`documented, not checked in environment`', '`confirmed by user`',
        '`unknown/to prepare`', '`not requested`', '`not saved`',
        '`pending confirmation`',
    ):
        assert obsolete not in text


def test_intermediate_checks_use_real_functional_evidence() -> None:
    """Allow required documented responses without manufacturing AC ids."""
    text = _read(SKILLS / 'uc-to-feature' / 'SKILL.md')
    assert 'supported by the UC or admitted documentation, including ACs' in text
    assert 'internal check alone never justifies it' in text
    assert 'Intermediate checks need not have an invented AC' in text
    assert 'only when an AC or a postcondition' not in text
    context = _read(SKILLS / 'uc-scenario-context' / 'SKILL.md')
    assert 'do not invent an AC to fit the template' in context


def test_many_ac_to_one_case_and_flow_alias_examples_are_preserved() -> None:
    """Preserve cardinality and alias examples without inventing a matcher."""
    text = _read(SKILLS / 'uc-to-feature' / 'ac-flow-references.md')
    groups = _table_rows(text, '| Criteria and target | Gherkin grouping |')
    assert groups == [
        ['AC01 and AC02 both reference FP', 'One main-flow scenario/outline checking both'],
        ['AC03 and AC04 both reference AF02', 'One AF02 scenario/outline checking both'],
        ['AC05 and AC06 both reference EF01', 'One negative EF01 scenario/outline checking both'],
    ]
    assert 'not individual ACs' in text
    references = dict(_table_rows(text, '| AC reference fragment | Resolution |'))
    for alias, target in (
        ('`(f . p .)`', 'FP'), ('`(a . f . 02)`', 'AF-02'),
        ('`(E . F . 1)`', 'EF-01'), ('`(AF 99)`', 'Unresolved: target absent'),
    ):
        assert references[alias] == target
    assert references['`non si applica ad AF02`'].startswith('Excludes AF-02')
    assert 'an executable parser' not in text


def test_acceptance_matrix_covers_all_contract_cases_without_claiming_runs() -> None:
    """Keep expected agent checks distinct from observed execution results."""
    text = _read(DOCS / 'uc-workflow-validation.md')
    rows = _table_rows(
        text,
        '| Caso | Preparazione astratta | Risultato atteso '
        '| Evidenza da controllare nella prova agente |',
    )
    assert [row[0] for row in rows] == [f"V-{number:02d}" for number in range(1, 27)]
    assert all(all(cell for cell in row) for row in rows)
    assert "non un motore sostitutivo che simula l'agente" in text
    assert 'non risultati osservati' in text


@pytest.mark.parametrize('label', ['FP', 'AF', 'EF'])
def test_gherkin_allows_multiple_checks_in_one_scenario(label: str) -> None:
    """Parse multiple assertions in one abstract positive or negative case."""
    polarity = 'negative' if label == 'EF' else 'positive'
    feature = parse_feature(
        '#0000000000\n# language: it\n@contract_probe_001\n'
        'Funzionalit\u00e0: Prova sintattica astratta\n'
        f"  @{polarity}\n  @contract_probe_001_01\n  Scenario: Caso {label}\n"
        '    Dato lo stato prescritto\n'
        "    Quando l'attore compie l'azione prescritta\n"
        '    Allora il sistema espone la prima propriet\u00e0 prescritta\n'
        '    E il sistema espone la seconda propriet\u00e0 prescritta\n'
    )
    assert len(feature.scenarios) == 1
    assert [step.step_type for step in feature.scenarios[0].steps] == [
        'given', 'when', 'then', 'then'
    ]


def test_partial_outline_keeps_todo_in_cell_and_both_assertions() -> None:
    """Parse an unresolved outline row without confusing null and missing data."""
    fragment = (
        '#0000000000\n# language: it\n@contract_probe_001\n'
        'Funzionalit\u00e0: Prova sintattica astratta\n'
        "  # Dati irrisolti: D-001; riga 2; scenario non pronto all'esecuzione\n"
        '  @positive\n  @contract_probe_001_01\n'
        '  Schema dello scenario: Caso con dati variabili\n'
        '    Quando l\'attore usa il valore "<valore>"\n'
        '    Allora il sistema espone la prima propriet\u00e0 prescritta\n'
        '    E il sistema espone la seconda propriet\u00e0 prescritta\n'
        '    Esempi:\n      | valore |\n'
        '      | valore-astratto |\n      | __TODO_D001__ |\n'
    )
    feature = parse_feature(fragment)
    outline = feature.scenarios[0]
    assert outline.examples[0].table.headings == ['valore']
    assert outline.examples[0].table.rows[1].cells == ['__TODO_D001__']
    assert len(outline.scenarios) == 2
    assert '__TODO_D001__' in outline.scenarios[1].steps[0].name
    assert all(
        [step.step_type for step in scenario.steps] == ['when', 'then', 'then']
        for scenario in outline.scenarios
    )
    assert fragment.index('# Dati irrisolti') < fragment.index('  @positive')


def test_background_todo_has_warning_before_each_scenario_tags() -> None:
    """Parse shared unresolved data with an explicit warning on each case."""
    fragment = (
        '#0000000000\n# language: it\n@contract_probe_001\n'
        'Funzionalit\u00e0: Prova sintattica astratta\n'
        '  Contesto:\n    Dato lo stato identificato da __TODO_D001__\n'
    )
    for index in (1, 2):
        fragment += (
            "  # Dati irrisolti: D-001; scenario non pronto all'esecuzione\n"
            f"  @positive\n  @contract_probe_001_0{index}\n"
            f"  Scenario: Caso astratto {index}\n"
            "    Quando l'attore compie l'azione prescritta\n"
            '    Allora il sistema espone la propriet\u00e0 prescritta\n'
        )
    feature = parse_feature(fragment)
    assert len(feature.scenarios) == 2
    assert '__TODO_D001__' in feature.background.steps[0].name
    assert fragment.count('# Dati irrisolti: D-001') == len(feature.scenarios)
    assert re.search(r'# Dati irrisolti:.*\n  @positive', fragment)
