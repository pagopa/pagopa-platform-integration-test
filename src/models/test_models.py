import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

ENV_VALUES = ("DEV", "UAT", "PROD")
TRIGGER_TYPE_VALUES = ("MANUAL", "CRON", "CI_PIPELINE")
SCENARIO_STATUS_VALUES = ("PASSED", "FAILED", "BROKEN", "SKIPPED")


@dataclass
class Test_suites:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    test_object: str = ""
    test_type: str = ""
    suite_version: str = ""
    owner_team: Optional[str] = None
    runs: list["Test_runs"] = field(default_factory=list)


@dataclass
class Test_runs:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    suite_id: uuid.UUID = field(default_factory=uuid.uuid4)
    scenario_qty: Optional[int] = None
    passed_scenario: Optional[int] = None
    failed_scenario: Optional[int] = None
    broken_scenario: Optional[int] = None
    skipped_scenario: Optional[int] = None
    timestamp_start: Optional[datetime] = None
    timestamp_end: Optional[datetime] = None
    duration_ms: Optional[int] = None
    env: Optional[str] = None
    trigger_type: Optional[str] = None
    test_version: Optional[str] = None


@dataclass
class Test_executions:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    run_id: uuid.UUID = field(default_factory=uuid.uuid4)
    allure_id: Optional[str] = None
    status: Optional[str] = None
    scenario_name: Optional[str] = None
    allure_report: Optional[dict[str, Any]] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    retries: Optional[int] = None


__all__ = [
    "Test_suites",
    "Test_runs",
    "Test_executions",
    "ENV_VALUES",
    "TRIGGER_TYPE_VALUES",
    "SCENARIO_STATUS_VALUES",
]

