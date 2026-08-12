"""Executable release-candidate contract for D-001.

The documentation checks preserve the approved Step 2 requirements after they turn
green.  The remaining matrices keep the Step 3-5 Registry, artifact, and installation
boundaries explicit without performing those side effects during the default test run.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
README_PATH = PROJECT_ROOT / "README.md"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
RELEASE_PLAN_PATH = PROJECT_ROOT / "docs" / "release-plan.md"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"

DISTRIBUTION_NAME = "mcp-weather-query"
IMPORT_PACKAGE = "mcp_weather_query"
CONSOLE_COMMAND = "mcp-weather-query"
CONSOLE_TARGET = "mcp_weather_query.__main__:main"
VERSION = "0.1.0"
LICENSE_EXPRESSION = "MIT"
REGISTRY_SERVER_NAME = "io.github.wcnm8888/mcp1-weather-query"
REGISTRY_SCHEMA = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"


@dataclass(frozen=True)
class RegistryValidationCase:
    """A required Step 3 local-only Registry validation boundary."""

    manifest_name: str
    schema: str
    registry_type: str
    transport: str
    validation_step: int
    permits_login: bool = False
    permits_publish: bool = False


@dataclass(frozen=True)
class CandidateArtifactCase:
    """A required Step 4 release-candidate artifact."""

    kind: str
    suffix: str
    build_step: int
    committed_to_git: bool = False


@dataclass(frozen=True)
class CandidateInstallCase:
    """A required Step 5 project-external clean installation."""

    artifact_kind: str
    environment_name: str
    verification_step: int
    allows_pythonpath: bool = False
    allows_editable_install: bool = False
    permits_live_weather_request: bool = False


REGISTRY_VALIDATION_CASE = RegistryValidationCase(
    manifest_name="server.json",
    schema=REGISTRY_SCHEMA,
    registry_type="pypi",
    transport="stdio",
    validation_step=3,
)

CANDIDATE_ARTIFACT_CASES = (
    CandidateArtifactCase(kind="wheel", suffix=".whl", build_step=4),
    CandidateArtifactCase(kind="sdist", suffix=".tar.gz", build_step=4),
)

CANDIDATE_INSTALL_CASES = (
    CandidateInstallCase(artifact_kind="wheel", environment_name="wheel-env", verification_step=5),
    CandidateInstallCase(artifact_kind="sdist", environment_name="sdist-env", verification_step=5),
)


def read_text(path: Path) -> str:
    """Read one UTF-8 release document."""
    return path.read_text(encoding="utf-8")


def load_pyproject() -> dict[str, Any]:
    """Read static package metadata without invoking a build backend."""
    return tomllib.loads(read_text(PYPROJECT_PATH))


def test_existing_distribution_identity_remains_the_approved_release_identity() -> None:
    """D-001 must not rename or version-bump the F-002 package."""
    project = load_pyproject()["project"]

    assert project["name"] == DISTRIBUTION_NAME
    assert project["version"] == VERSION
    assert project["license"] == LICENSE_EXPRESSION
    assert project["scripts"] == {CONSOLE_COMMAND: CONSOLE_TARGET}
    assert (PROJECT_ROOT / "src" / IMPORT_PACKAGE / "__init__.py").is_file()


def test_changelog_records_the_frozen_initial_release_and_registry_boundary() -> None:
    """The initial release must have a fixed date and its verified Registry status."""
    assert CHANGELOG_PATH.is_file(), "D-001 requires a root CHANGELOG.md"

    changelog = read_text(CHANGELOG_PATH)
    assert "0.1.0" in changelog
    assert "get_current_weather" in changelog
    assert "## [0.1.0] - 2026-08-12" in changelog
    assert "Unreleased" not in changelog
    assert "PyPI" in changelog
    assert REGISTRY_SERVER_NAME in changelog
    assert "已登记到 Official MCP Registry" in changelog


def test_readme_documents_installation_from_the_local_candidate_wheel() -> None:
    """A reviewer must be able to install the candidate without editable/source shortcuts."""
    readme = read_text(README_PATH)

    assert "uv tool install ./dist/mcp_weather_query-0.1.0-py3-none-any.whl" in readme
    assert "PYTHONPATH" in readme
    assert "不需要" in readme or "无需" in readme


def test_readme_documents_the_version_pinned_public_pypi_command() -> None:
    """Document the public command while making availability externally verifiable."""
    readme = read_text(README_PATH)

    assert "uvx --from mcp-weather-query==0.1.0 mcp-weather-query" in readme
    assert "从 PyPI 运行固定版本" in readme
    assert "PyPI 官方项目页" in readme


def test_readme_has_a_source_independent_stdio_host_configuration() -> None:
    """The Host example must invoke the installed console command directly."""
    readme = read_text(README_PATH)

    assert '"command": "mcp-weather-query"' in readme
    assert '"args": []' in readme


def test_readme_contains_registry_marker_and_stable_publication_boundaries() -> None:
    """Keep PyPI verification external while recording the active Registry identity."""
    readme = read_text(README_PATH)

    assert f"mcp-name: {REGISTRY_SERVER_NAME}" in readme
    assert "当前尚未发布到 PyPI" not in readme
    assert "公开可用性、文件和 attestation" in readme
    assert "已登记到 Official MCP Registry" in readme
    assert "active" in readme
    assert "尚未登记 MCP Registry" not in readme


def test_release_plan_defines_reproducible_candidate_commands_without_publish_actions() -> None:
    """The release plan must separate local validation from external writes."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    assert "uv build --no-sources" in release_plan
    assert "mcp-publisher validate" in release_plan
    assert "mcp-publisher login" in release_plan
    assert "mcp-publisher publish" in release_plan
    assert "禁止" in release_plan or "不得" in release_plan


def test_later_registry_validation_matrix_is_local_only_and_fixed_scope() -> None:
    """Define Step 3 without creating or validating a manifest during Step 1."""
    case = REGISTRY_VALIDATION_CASE

    assert case.manifest_name == "server.json"
    assert case.schema == REGISTRY_SCHEMA
    assert case.registry_type == "pypi"
    assert case.transport == "stdio"
    assert case.validation_step == 3
    assert not case.permits_login
    assert not case.permits_publish


def test_later_candidate_artifact_matrix_requires_wheel_and_sdist_outside_git() -> None:
    """Define both Step 4 candidate artifacts without running a build."""
    assert {(case.kind, case.suffix, case.build_step) for case in CANDIDATE_ARTIFACT_CASES} == {
        ("wheel", ".whl", 4),
        ("sdist", ".tar.gz", 4),
    }
    assert all(not case.committed_to_git for case in CANDIDATE_ARTIFACT_CASES)


def test_later_dual_install_matrix_forbids_source_and_live_shortcuts() -> None:
    """Define Step 5 isolation without creating environments or starting subprocesses."""
    assert {case.artifact_kind for case in CANDIDATE_INSTALL_CASES} == {"wheel", "sdist"}
    assert len({case.environment_name for case in CANDIDATE_INSTALL_CASES}) == 2
    assert all(case.verification_step == 5 for case in CANDIDATE_INSTALL_CASES)
    assert all(not case.allows_pythonpath for case in CANDIDATE_INSTALL_CASES)
    assert all(not case.allows_editable_install for case in CANDIDATE_INSTALL_CASES)
    assert all(not case.permits_live_weather_request for case in CANDIDATE_INSTALL_CASES)
