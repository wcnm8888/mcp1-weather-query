"""Executable packaging contract for F-002.

Step 1 intentionally leaves the production packaging configuration unchanged. The
configuration and legal-file tests in this module must therefore fail until Step 2.
The artifact and clean-install matrices define the later Step 3/4 verification shape
without building or installing anything during this step.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"

EXPECTED_DISTRIBUTION_NAME = "mcp-weather-query"
EXPECTED_IMPORT_PACKAGE = "mcp_weather_query"
EXPECTED_CONSOLE_COMMAND = "mcp-weather-query"
EXPECTED_CONSOLE_TARGET = "mcp_weather_query.__main__:main"
EXPECTED_VERSION = "0.1.0"
EXPECTED_LICENSE_EXPRESSION = "MIT"
EXPECTED_LEGAL_FILES = frozenset({"LICENSE", "NOTICE"})
UV_BUILD_REQUIREMENT = re.compile(r"uv_build>=0\.11\.\d+,<0\.12")


@dataclass(frozen=True)
class ArtifactCase:
    """A required distribution artifact and its later verification step."""

    kind: str
    suffix: str
    verification_step: int


@dataclass(frozen=True)
class CleanInstallCase:
    """A required isolated installation path for a built artifact."""

    artifact_kind: str
    environment_name: str
    allows_pythonpath: bool = False
    allows_editable_install: bool = False


@dataclass(frozen=True)
class InstalledPackageCheck:
    """A required Step 4 behavior of the installed distribution."""

    name: str
    uses_production_console_command: bool
    permits_live_weather_request: bool = False


ARTIFACT_CASES = (
    ArtifactCase(kind="wheel", suffix=".whl", verification_step=3),
    ArtifactCase(kind="sdist", suffix=".tar.gz", verification_step=3),
)

CLEAN_INSTALL_CASES = (
    CleanInstallCase(artifact_kind="wheel", environment_name="wheel-env"),
    CleanInstallCase(artifact_kind="sdist", environment_name="sdist-env"),
)

INSTALLED_PACKAGE_CHECKS = (
    InstalledPackageCheck(name="module-origin", uses_production_console_command=False),
    InstalledPackageCheck(name="modern-discovery", uses_production_console_command=True),
    InstalledPackageCheck(name="unique-tool", uses_production_console_command=True),
    InstalledPackageCheck(name="stdio-streams-and-exit", uses_production_console_command=True),
    InstalledPackageCheck(name="synthetic-tool-call", uses_production_console_command=False),
)


def load_pyproject() -> dict[str, Any]:
    """Load project metadata without invoking a build backend."""
    return tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))


def test_distribution_and_import_names_are_stable() -> None:
    """Keep distribution and import names distinct but deterministic."""
    pyproject = load_pyproject()

    assert pyproject["project"]["name"] == EXPECTED_DISTRIBUTION_NAME
    assert (PROJECT_ROOT / "src" / EXPECTED_IMPORT_PACKAGE / "__init__.py").is_file()


def test_project_is_enabled_as_an_installable_package() -> None:
    """A packaged project must not retain the source-only uv override."""
    pyproject = load_pyproject()
    package_setting = pyproject.get("tool", {}).get("uv", {}).get("package")

    assert package_setting is not False, (
        "F-002 requires an installable package; remove tool.uv.package=false"
    )


def test_build_system_uses_a_bounded_uv_build_backend() -> None:
    """Use the approved pure-Python backend with a bounded compatible series."""
    pyproject = load_pyproject()
    build_system = pyproject.get("build-system")

    assert isinstance(build_system, dict), "F-002 requires an explicit [build-system]"
    assert build_system.get("build-backend") == "uv_build"

    requirements = build_system.get("requires")
    assert isinstance(requirements, list)
    assert len(requirements) == 1
    assert isinstance(requirements[0], str)
    assert UV_BUILD_REQUIREMENT.fullmatch(requirements[0]), (
        "uv_build must stay in the approved >=0.11.x,<0.12 compatibility line"
    )


def test_initial_distribution_version_is_approved_value() -> None:
    """Replace the F-001 placeholder before producing local artifacts."""
    pyproject = load_pyproject()

    assert pyproject["project"]["version"] == EXPECTED_VERSION


def test_console_command_targets_the_existing_stdio_entrypoint() -> None:
    """Installation must expose the same production stdio server entrypoint."""
    pyproject = load_pyproject()
    scripts = pyproject["project"].get("scripts")

    assert isinstance(scripts, dict), "F-002 requires [project.scripts]"
    assert scripts == {EXPECTED_CONSOLE_COMMAND: EXPECTED_CONSOLE_TARGET}


def test_license_metadata_covers_code_license_and_legal_notice() -> None:
    """Use modern SPDX metadata and include both required legal files."""
    pyproject = load_pyproject()
    project = pyproject["project"]

    assert project.get("license") == EXPECTED_LICENSE_EXPRESSION
    license_files = project.get("license-files")
    assert isinstance(license_files, list)
    assert set(license_files) == EXPECTED_LEGAL_FILES


def test_required_legal_files_exist_at_project_root() -> None:
    """Keep the MIT code license separate from Open-Meteo attribution."""
    missing = sorted(name for name in EXPECTED_LEGAL_FILES if not (PROJECT_ROOT / name).is_file())

    assert not missing, f"missing required legal files: {', '.join(missing)}"


def test_later_artifact_matrix_requires_wheel_and_sdist() -> None:
    """Define the Step 3 artifact cases without building them in Step 1."""
    assert {(case.kind, case.suffix, case.verification_step) for case in ARTIFACT_CASES} == {
        ("wheel", ".whl", 3),
        ("sdist", ".tar.gz", 3),
    }


def test_later_clean_install_matrix_forbids_source_path_shortcuts() -> None:
    """Define separate Step 4 installs that cannot fall back to source imports."""
    assert {case.artifact_kind for case in CLEAN_INSTALL_CASES} == {"wheel", "sdist"}
    assert len({case.environment_name for case in CLEAN_INSTALL_CASES}) == 2
    assert all(not case.allows_pythonpath for case in CLEAN_INSTALL_CASES)
    assert all(not case.allows_editable_install for case in CLEAN_INSTALL_CASES)


def test_later_installed_stdio_matrix_covers_approved_offline_behaviors() -> None:
    """Define Step 4 installed-package checks without starting a child in Step 1."""
    assert {check.name for check in INSTALLED_PACKAGE_CHECKS} == {
        "module-origin",
        "modern-discovery",
        "unique-tool",
        "stdio-streams-and-exit",
        "synthetic-tool-call",
    }
    assert all(not check.permits_live_weather_request for check in INSTALLED_PACKAGE_CHECKS)
