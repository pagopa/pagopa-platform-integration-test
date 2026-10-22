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
        ROOT / 'docs' / 'agent-personas' / 'qa-orchestrator.md',
        ROOT / 'docs' / 'agent-personas' / 'qa-closer.md',
        ROOT / '.github' / 'agents' / 'QA-analyst.agent.md',
        ROOT / '.github' / 'agents' / 'QA-orchestrator.agent.md',
        ROOT / '.github' / 'agents' / 'Qa-closer.agent.md',
        SKILLS / 'review-feature-files' / 'SKILL.md',
        SKILLS / 'ppa-readme' / 'SKILL.md',
        SKILLS / 'ppa-commit' / 'SKILL.md',
        SKILLS / 'ppa-pr' / 'SKILL.md',
        ROOT / '.github' / 'instructions' / 'gherkin.instructions.md',
    ])
    paths.extend((ROOT / 'docs' / 'workflows' / 'qa-analyst').glob('*.md'))
    paths.extend((ROOT / 'docs' / 'workflows' / 'qa-closer').glob('*.md'))
    paths.extend((ROOT / 'docs' / 'adr').glob('ADR-*.md'))
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
    assert [row[0] for row in rows] == [f"V-{number:02d}" for number in range(1, 37)]
    assert all(all(cell for cell in row) for row in rows)
    assert "non un motore sostitutivo che simula l'agente" in text
    assert 'non risultati osservati' in text


def test_data_comments_are_limited_to_unresolved_placeholders() -> None:
    """Keep concrete-data uncertainties in reports without feature noise."""
    data = _read(SKILLS / 'uc-test-data' / 'SKILL.md')
    instructions = _read(ROOT / '.github' / 'instructions' / 'gherkin.instructions.md')
    workflow = _read(DOCS / 'uc-workflow.md')
    template = _read(DOCS / 'workflow-templates' / '02-test-data.template.md')
    assert 'every Scenario or Scenario Outline with an unresolved\n  placeholder' in data
    assert 'not in feature comments' in data
    assert 'remove the data-warning comment when its last placeholder' in data
    assert 'Retain all unresolved report warnings and `bozza` reasons' in data
    assert 'A comment is also required for concrete candidates' not in data
    assert 'Data-warning comments are only for unresolved placeholders' in instructions
    assert 'solo i TODO richiedono commenti nelle feature' in workflow
    assert '`not-applicable`' in data and '`not-applicable`' in template


def test_deployment_locators_do_not_become_functional_step_parameters() -> None:
    """Preserve run configuration and explicit functional-locator exceptions."""
    instructions = _read(ROOT / '.github' / 'instructions' / 'gherkin.instructions.md')
    context = _read(SKILLS / 'uc-scenario-context' / 'SKILL.md')
    translation = _read(SKILLS / 'uc-to-feature' / 'SKILL.md')
    assert 'Keep deployment configuration out of steps and Examples' in instructions
    assert 'Python/Behave implementation from the run configuration' in instructions
    assert 'an explicit functional requirement' in instructions
    assert 'not\nweaken an external-domain check' in instructions
    assert 'Distinguish deployment locators from functional requirements' in context
    assert 'Deployment locators from source documents stay in reports' in translation


def test_readme_consultation_is_scoped_operational_context() -> None:
    """Bound README use without granting execution or functional admission."""
    instructions = _read(ROOT / '.github' / 'instructions' / 'gherkin.instructions.md')
    translation = _read(SKILLS / 'uc-to-feature' / 'SKILL.md')
    assert '## Project operational context' in instructions
    assert '[README](../../README.md)' in instructions
    assert 'Consult only the relevant sections' in instructions
    assert 'only to the suite type they describe' in instructions
    assert 'does not authorize executing its commands' in instructions
    assert 'links into excluded paths' in instructions
    assert "active workflow's source-admission policy" in instructions
    assert '[README](../../../README.md)' in translation
    assert 'not the whole document by default' in translation
    assert 'report Mapping/Checks sections, separately from functional evidence' in translation
    assert "do not generalize another suite's defaults" in translation
    assert 'record an open\noperational question' in translation
    assert 'test values from the README still require admission' in translation


def test_given_requires_supported_state_not_assumed_data_fitness() -> None:
    """Separate supported setup, unknown preparation and functional rules."""
    instructions = _read(ROOT / '.github' / 'instructions' / 'gherkin.instructions.md')
    context = _read(SKILLS / 'uc-scenario-context' / 'SKILL.md')
    translation = _read(SKILLS / 'uc-to-feature' / 'SKILL.md')
    data = _read(SKILLS / 'uc-test-data' / 'SKILL.md')
    assert 'Every Given must have a supported way to verify or establish its state' in instructions
    assert 'It need not perform an assertion' in instructions
    assert 'invent a preliminary business operation' in instructions
    assert 'Missing preparation evidence is not automatically' in instructions
    assert 'Distinguish a missing setup/observation capability' in context
    assert 'Preserve an explicit UC precondition as an unresolved' in context
    assert 'A data-fitness constraint alone does not supply that' in translation
    assert 'Keep data-fitness requirements distinct from guaranteed initial states' in data
    assert 'a preliminary payment' in data


def test_analyst_activity_routing_separates_review_edit_and_creation() -> None:
    """Keep activity selection independent of input format and branch routing."""
    routing = _read(ROOT / 'docs' / 'workflows' / 'qa-analyst' / 'activity-routing.md')
    rows = _table_rows(routing, '| Activity | Procedure | Allowed output |')
    assert [row[0] for row in rows] == [
        'Review', 'Edit or correct', 'Create from a team-template UC',
        'Create from other documentation or an explicitly supplied migration suite',
    ]
    assert 'Supplied feature files alone do\nnot authorize editing' in routing
    assert 'without a second generic permission question' in routing
    persona = _read(ROOT / 'docs' / 'agent-personas' / 'qa-analyst.md')
    assert 'directly from the user or from the orchestrator' in persona
    assert '../workflows/qa-analyst/activity-routing.md' in persona
    assert '../workflows/qa-analyst/feature-editing.md' in persona
    assert 'ask the user before updating or reworking' not in persona


def test_feature_editing_preserves_scope_and_uc_reconciliation() -> None:
    """Require evidence, scoped writes and honest partial UC reconciliation."""
    editing = _read(ROOT / 'docs' / 'workflows' / 'qa-analyst' / 'feature-editing.md')
    for clause in (
        'Preserve\n  pre-existing changes',
        '**Syntax/style:** preserve functional meaning',
        '**Functional:**',
        'require admitted evidence',
        'through `uc-to-feature`',
        'Unchanged context/data need not be retrieved again',
        'mark the feature and final report\n  `stale`',
        'move the run to `in_progress`',
        'If the registry cannot be updated, report the actual failure',
        'Show old/new step wording or parameter changes',
        'not parser commands',
    ):
        assert clause in editing


def test_generic_documentation_uses_evidence_without_fabricating_uc() -> None:
    """Bound migration evidence while preserving the strict UC source rule."""
    routing = _read(ROOT / 'docs' / 'workflows' / 'qa-analyst' / 'activity-routing.md')
    policy = _read(SKILLS / 'uc-scenario-context' / 'source-policy.md')
    assert '## Common evidence rules (ADR-04)' in routing
    assert 'No feature creation or modification' in routing
    assert 'no invented UC or mandatory UC registry' in routing
    assert 'never input-data placeholders' in routing
    assert 'questions, not proven defects' in routing
    assert 'In the UC workflow, do not use feature files' in policy
    assert 'For non-UC migration only, explicitly supplied executable suites' in policy
    assert 'never applies to UC translation' in policy
    assert 'not as proof of requirements' in policy


def test_review_allows_only_requested_reports_without_self_delegation() -> None:
    """Preserve feature immutability, direct invocation and ACE writer ownership."""
    review = _read(SKILLS / 'review-feature-files' / 'SKILL.md')
    routing = _read(ROOT / 'docs' / 'workflows' / 'qa-analyst' / 'activity-routing.md')
    assert 'never delegate to yourself' in review
    assert 'including a corrected copy at another path' in review
    assert 'Only an explicitly requested Markdown' in review
    assert 'A chat-only request writes no report' in review
    assert 'review report' in routing
    assert 'No generic permission to create other file types' in review
    assert 'never trace files' in routing
    assert 'The orchestrator owns ACE capture, privacy' in routing
    assert 'requested Markdown review or' in _read(
        ROOT / 'docs' / 'agent-personas' / 'qa-analyst.md'
    )


def test_implementation_delegation_requires_orchestrator_readiness_gate() -> None:
    """Remove analyst handoffs and prevent activity completion from opening gates."""
    wrapper = _read(ROOT / '.github' / 'agents' / 'QA-analyst.agent.md')
    metadata = wrapper.split('---', 2)[1]
    assert 'handoffs:' not in metadata
    assert 'Never delegate to yourself or start implementation agents' in wrapper
    routing = _read(ROOT / 'docs' / 'workflows' / 'qa-analyst' / 'activity-routing.md')
    rows = _table_rows(routing, '| Result | Meaning |')
    assert [row[0] for row in rows] == [
        '`review-complete`', '`changes-complete`', '`draft`',
        '`ready-for-development`', '`blocked`',
    ]
    assert 'never introduce these activity labels as new UC schema enums' in routing
    orchestrator = _read(ROOT / 'docs' / 'agent-personas' / 'qa-orchestrator.md')
    assert '## Analyst-result gate (ADR-05)' in orchestrator
    assert 'Require explicit `ready-for-development`' in orchestrator
    assert 'the user explicitly\n  authorizes that partial implementation scope' in orchestrator
    assert 'the final report says `pronta per lo sviluppo`' in orchestrator
    assert 'requested boundary' in orchestrator
    assert 'diagnostic\n  permission for existing tests' in orchestrator


def test_uc_identity_survives_new_ace_requests_without_schema_migration() -> None:
    """Keep stable UC report identity separate from Jira and per-request traces."""
    workflow = _read(DOCS / 'uc-workflow.md')
    for clause in (
        '### Identita distinte (ADR-07)',
        'resta stabile quando si riprende la stessa run',
        "ne l'ACE `task_id` della particolare richiesta",
        'non rinominare directory',
        'senza nuovi campi o invalidazioni',
        'template e report storici mantengono i campi e i valori esistenti',
    ):
        assert clause in workflow


@pytest.mark.parametrize('number', range(2, 14))
def test_qa_decisions_are_recorded_as_accepted(number: int) -> None:
    """Keep each agreed ADR discoverable with a link to its operational owner."""
    matches = list((ROOT / 'docs' / 'adr').glob(f"ADR-{number:02d}-*.md"))
    assert len(matches) == 1
    text = _read(matches[0])
    assert '- Status: Accepted' in text
    assert '## Decision' in text
    assert '## Consequences' in text
    assert re.search(r'\[[^\]]+\]\(\.\./', text)


def test_readme_skill_is_discoverable_scoped_and_non_recursive() -> None:
    """Keep README maintenance reusable without forced edits or execution."""
    text = _read(SKILLS / 'ppa-readme' / 'SKILL.md')
    metadata = text.split('---', 2)[1]
    assert 'name: ppa-readme\n' in metadata
    assert 0 < len(metadata.split('description: >-', 1)[1].strip()) <= 1024
    assert 'once per coherent change set' in text
    assert 'staged, unstaged and intended untracked files' in text
    assert 'A broad restructuring' in text
    assert 'requires explicit confirmation' in text
    assert 'current relevant\ncontents and scope' in text
    assert 'does not recursively trigger another full assessment' in text
    assert '`updated`, `no-update-needed` or `blocked`' in text
    assert 'Do not run tests' in text
    assert 'return the assessment and required changes to the orchestrator' in text
    instructions = _read(ROOT / 'AGENTS.md')
    assert '## README maintenance gate (ADR-11)' in instructions
    assert 'before an eventual commit' in instructions
    assert 'does not expand permissions' in instructions
    assert '.github/skills/ppa-readme/SKILL.md' in instructions
    readme = _read(ROOT / 'README.md')
    assert '[`/ppa-readme`](.github/skills/ppa-readme/SKILL.md)' in readme
    assert 'docs/workflows/qa-closer/closure.md' in readme


def test_closure_verification_is_current_scoped_runner_evidence() -> None:
    """Require real execution evidence without count growth or closer reruns."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    inputs = _table_rows(workflow, '| Input | Required content |')
    assert [row[0] for row in inputs] == [
        'Identity and scope', 'Verification', 'Evidence', 'Documentation',
        'Publication plan', 'Prior closure state',
    ]
    assert 'working-tree contents verified' in inputs[1][1]
    assert 'A larger test count' in workflow
    assert 'A matching HEAD\nalone does not establish freshness' in workflow
    assert 'zero executed tests' in workflow
    assert 'If relevant contents changed after verification, stop publication' in workflow
    assert 'do not rerun tests' in workflow
    runner = _read(ROOT / 'docs' / 'agent-personas' / 'qa-runner.md')
    assert '## Verification handoff (ADR-08)' in runner
    assert 'passed/failed/error/skipped/undefined counts' in runner
    assert 'Return any existing failure-report path' in runner


def test_closure_staging_and_outgoing_commits_preserve_authorized_scope() -> None:
    """Block wrong-branch or unrelated publication without automatic repair."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    assert 'Detached HEAD,\n   `main`, the repository default branch' in workflow
    assert 'do not checkout, switch, create a branch' in workflow
    assert 'Unrelated staged\n   content blocks a commit' in workflow
    assert 'do not include it or\n   unstage it silently' in workflow
    assert 'inspect outgoing commits as well as the current index' in workflow
    assert 'No merge, force push, amend' in workflow
    persona = _read(ROOT / 'docs' / 'agent-personas' / 'qa-closer.md')
    assert 'stage all changes' not in persona
    assert 'Do NOT edit feature files, test code' in persona
    assert 'Do NOT run tests' in persona


def test_closure_approvals_are_independent_and_refusals_win() -> None:
    """Prevent green results or a skill default from inventing publication consent."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    decisions = _table_rows(workflow, '| Decision | Meaning |')
    assert [row[0] for row in decisions] == [
        '`commit: true`', '`push: true`', '`create_pr: true`',
        'Any explicit `false`', 'Unresolved decision',
    ]
    assert 'test success does not supply consent' in decisions[-1][1]
    assert 'do not ask again to override a refusal' in decisions[-2][1]
    assert 'no-push/commit-only restriction\nmust be passed explicitly' in workflow
    assert 'If a PR needs an unpublished commit but push is forbidden' in workflow
    orchestrator = _read(ROOT / 'docs' / 'agent-personas' / 'qa-orchestrator.md')
    assert '## Closure handoff (ADR-08 through ADR-13)' in orchestrator
    assert 'No success condition sets `create_pr: true` implicitly' in orchestrator
    assert 'independent `commit`, `push` and `create_pr` decisions' in orchestrator
    assert 'or **ALL** tests pass' not in _read(
        ROOT / 'docs' / 'agent-personas' / 'qa-closer.md'
    )


def test_closure_documentation_and_ignore_are_conditional() -> None:
    """Reuse current README assessments and avoid mandatory ignore churn."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    assert 'reuse an assessment that actually covers its current\ncontents' in workflow
    assert 'Report `no-update-needed` when appropriate' in workflow
    assert 'Do not create or edit `.gitignore` merely because closure ran' in workflow
    assert 'Local ignored reports remain local' in workflow
    assert 'without a new commit or push' in workflow


def test_closer_reports_only_markdown_for_unresolved_suite_errors() -> None:
    """Keep success, non-suite work and publication failures out of suite reporting."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    assert '**only for work on test suites with\nunresolved errors' in workflow
    assert 'Earlier failures resolved by current verified results' in workflow
    assert 'a Git/PR/tool failure alone does not' in workflow
    assert 'no commit, push\n  or PR through this path' in workflow
    assert "reuse the runner's relevant Markdown failure report" in workflow
    assert 'Unknown values remain unknown' in workflow
    assert 'No HTML/Allure generation or serving, Confluence templates/API' in workflow
    assert 'GitHub PR template\n  remains mandatory' in workflow
    wrapper = _read(ROOT / '.github' / 'agents' / 'Qa-closer.agent.md')
    description = wrapper.split('---', 2)[1].splitlines()[1]
    assert 'HTML report' not in description
    assert 'report-only closure' in description
    assert 'Standalone reports are Markdown only' in wrapper


def test_closure_ace_capture_has_one_owner_and_no_recursive_commit() -> None:
    """Allow only explicitly scoped sanitized traces and defer closer capture."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    assert 'Do not create or edit ACE files here' in workflow
    assert 'ACE files are excluded from closure scope by default' in workflow
    assert 'evidence of successful privacy finalization' in workflow
    assert 'Raw or uncertain trace contents must not be' in workflow
    assert "closer's own trace is captured after its result by the orchestrator" in workflow
    assert 'There is no recursive commit' in workflow
    orchestrator = _read(ROOT / 'docs' / 'agent-personas' / 'qa-orchestrator.md')
    assert 'privacy-finalize\nthose through the existing ACE lifecycle afterward' in orchestrator
    assert 'automatically\npublish newly captured traces' in orchestrator


def test_closure_recovery_reuses_verified_publication_state() -> None:
    """Resume the failed action rather than duplicating commits or PRs."""
    workflow = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'closure.md')
    states = _table_rows(workflow, '| Last verified state | Resume behavior |')
    assert len(states) == 5
    assert 'not a new commit' in states[1][1]
    assert 'only the needed PR step' in states[2][1]
    assert 'do not duplicate it' in states[3][1]
    assert 'ask before any potentially duplicate write' in states[4][1]
    assert "use only\n   the skill's push procedure" in workflow
    assert 'Actual actions, checks, lesson IDs and friction' in workflow
    assert '`completed`, `report-only`, `partial` or `blocked`' in workflow


def test_closure_acceptance_matrix_distinguishes_expectations_from_runs() -> None:
    """Retain closure trial cases without pretending static checks ran an agent."""
    text = _read(ROOT / 'docs' / 'workflows' / 'qa-closer' / 'validation.md')
    cases = _table_rows(text, '| Case | Input or state | Expected result |')
    assert [row[0] for row in cases] == [f"C-{number:02d}" for number in range(1, 17)]
    assert all(all(cell for cell in row) for row in cases)
    assert 'not evidence that these scenarios have been executed' in text
    assert 'not a simulated\nagent or real publication' in text


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
