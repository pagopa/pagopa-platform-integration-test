"""Discover secret placeholders in suite environment YAML files."""

from pathlib import Path

from dynaconf import Dynaconf


SUITE_ROOTS = tuple(Path("src") / category for category in ("integration", "e2e", "api"))


def placeholders(value) -> set[str]:
    if isinstance(value, dict):
        return set().union(*(placeholders(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(placeholders(item) for item in value))
    if isinstance(value, str) and value.startswith("$"):
        if len(value) == 1:
            raise RuntimeError("Empty secret placeholder in suite configuration")
        return {value[1:]}
    return set()


def environment_configs(directory: Path, target_env: str) -> list[Path]:
    return sorted(
        config_path
        for extension in ("yaml", "yml")
        for config_path in directory.rglob(f"{target_env}.{extension}")
    )


def config_placeholders(config_path: Path) -> set[str]:
    config = Dynaconf(
        settings_files=[str(config_path.resolve())], environments=False
    ).as_dict()
    return placeholders(config)