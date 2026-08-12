"""Executable R-001 contract for a least-privilege PyPI release workflow.

The contract preserves the approved least-privilege workflow and final release
metadata through the exact tag gate. It performs static, offline checks and never
contacts PyPI.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "release.yml"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
README_PATH = PROJECT_ROOT / "README.md"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
RELEASE_PLAN_PATH = PROJECT_ROOT / "docs" / "release-plan.md"

DISTRIBUTION_NAME = "mcp-weather-query"
IMPORT_PACKAGE = "mcp_weather_query"
CONSOLE_COMMAND = "mcp-weather-query"
CONSOLE_TARGET = "mcp_weather_query.__main__:main"
VERSION = "0.1.0"
RELEASE_TAG = "v0.1.0"
PYPI_ENVIRONMENT = "pypi"
REPOSITORY_OWNER = "wcnm8888"
REPOSITORY_NAME = "mcp1-weather-query"

# Resolved from the official repositories on 2026-08-12.  Full commit SHAs are
# immutable; the readable release refs belong in workflow comments, not in `uses`.
APPROVED_ACTIONS = {
    "actions/checkout": "d23441a48e516b6c34aea4fa41551a30e30af803",  # v6
    "actions/setup-python": "ece7cb06caefa5fff74198d8649806c4678c61a1",  # v6
    "astral-sh/setup-uv": "c771a70e6277c0a99b617c7a806ffedaca235ff9",  # v9.0.0
    "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",  # v7.0.1
    "actions/download-artifact": "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",  # v8.0.1
    "pypa/gh-action-pypi-publish": "dc37677b2e1c63e2034f94d8a5b11f265b73ba33",  # release/v1
}


def read_text(path: Path) -> str:
    """Read one UTF-8 project file."""
    return path.read_text(encoding="utf-8")


def load_pyproject() -> dict[str, Any]:
    """Read package metadata without invoking a build backend."""
    return tomllib.loads(read_text(PYPROJECT_PATH))


def read_release_workflow() -> str:
    """Read the future dedicated release workflow with a useful red-state message."""
    assert WORKFLOW_PATH.is_file(), (
        "R-001 Step 2 must create the dedicated Trusted Publisher workflow at "
        ".github/workflows/release.yml"
    )
    return read_text(WORKFLOW_PATH)


def job_block(workflow: str, job_name: str) -> str:
    """Extract one canonical two-space-indented job block for static checks."""
    match = re.search(
        rf"(?ms)^  {re.escape(job_name)}:\s*$\n(?P<body>.*?)(?=^  [A-Za-z0-9_-]+:\s*$|\Z)",
        workflow,
    )
    assert match is not None, f"release workflow must define a {job_name!r} job"
    return match.group("body")


def test_public_release_identity_remains_exactly_the_approved_package() -> None:
    """R-001 must not rename or version-bump the D-001 candidate."""
    project = load_pyproject()["project"]

    assert project["name"] == DISTRIBUTION_NAME
    assert project["version"] == VERSION
    assert project["scripts"] == {CONSOLE_COMMAND: CONSOLE_TARGET}
    assert (PROJECT_ROOT / "src" / IMPORT_PACKAGE / "__init__.py").is_file()


def test_changelog_freezes_the_approved_initial_release_before_the_tag_gate() -> None:
    """The tag must contain dated release metadata without stale pre-release wording."""
    changelog = read_text(CHANGELOG_PATH)

    assert "## [0.1.0] - 2026-08-12" in changelog
    assert "Unreleased" not in changelog
    assert "公开可用性、文件和 attestation 以 PyPI 官方项目页" in changelog
    assert "io.github.wcnm8888/mcp1-weather-query" in changelog
    assert "已登记到 Official MCP Registry" in changelog
    assert "MCP Registry 尚未登记" not in changelog


def test_dedicated_release_workflow_exists_at_the_publisher_identity_path() -> None:
    """The PyPI publisher tuple will trust this exact workflow filename."""
    workflow = read_release_workflow()

    assert workflow.strip(), "release.yml must not be empty"


def test_workflow_entrypoints_are_pr_checks_and_the_exact_release_tag_only() -> None:
    """Ordinary pushes and manual dispatch must not gain a path to publishing."""
    workflow = read_release_workflow()

    assert re.search(r"(?m)^on:\s*$", workflow)
    assert re.search(r"(?m)^  pull_request:\s*$", workflow)
    assert re.search(r"(?m)^  push:\s*$", workflow)
    assert re.search(r"(?m)^    tags:\s*$", workflow)
    assert re.search(r'(?m)^      - ["\']v0\.1\.0["\']\s*$', workflow)
    assert "workflow_dispatch" not in workflow
    assert "tags-ignore" not in workflow
    assert not re.search(r"(?m)^    branches(?:-ignore)?:", workflow)


def test_build_job_runs_quality_and_build_without_oidc_publish_privilege() -> None:
    """Untrusted build/test code must not run in the OIDC-enabled publish job."""
    workflow = read_release_workflow()
    build = job_block(workflow, "build")

    assert re.search(r"(?m)^permissions:\s*$\n  contents: read\s*$", workflow)
    assert "id-token: write" not in build
    assert "uv lock --check" in build
    assert "uv run ruff format --check ." in build
    assert "uv run ruff check ." in build
    assert "uv run mypy" in build
    assert "uv run pytest -q --tb=short" in build
    assert "git diff --check" in build
    assert "uv build --no-sources" in build
    assert "uv run python tests/packaging/inspect_artifacts.py dist" in build
    assert "actions/upload-artifact@" in build
    assert (
        build.index("uv build --no-sources")
        < build.index("uv run python tests/packaging/inspect_artifacts.py dist")
        < build.index("actions/upload-artifact@")
    )
    assert "MCP_WEATHER_RUN_LIVE" in build


def test_publish_job_has_exact_tag_guard_environment_and_minimum_oidc_permissions() -> None:
    """Only the artifact-only publish job may request a short-lived PyPI identity."""
    workflow = read_release_workflow()
    publish = job_block(workflow, "publish")

    assert re.search(r"(?m)^    needs: build\s*$", publish)
    assert "github.event_name == 'push'" in publish
    assert "github.ref == 'refs/tags/v0.1.0'" in publish
    assert re.search(r"(?m)^      name: pypi\s*$", publish)
    assert re.search(r"(?m)^      contents: read\s*$", publish)
    assert re.search(r"(?m)^      id-token: write\s*$", publish)
    assert "actions/download-artifact@" in publish
    assert "pypa/gh-action-pypi-publish@" in publish
    assert re.search(r"(?m)^          packages-dir: dist/?\s*$", publish)

    folded = publish.casefold()
    assert "uv build" not in folded
    assert "pytest" not in folded
    assert "password:" not in folded
    assert "username:" not in folded
    assert "repository-url:" not in folded
    assert "test.pypi.org" not in folded
    assert "skip-existing:" not in folded
    assert "attestations: false" not in folded
    assert "secrets." not in folded


def test_every_external_action_is_allowlisted_and_pinned_to_the_approved_commit() -> None:
    """Mutable tags and unapproved actions are not acceptable in a release workflow."""
    workflow = read_release_workflow()
    usages = re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", workflow)

    assert usages, "release workflow must use the approved build and publish actions"
    observed: dict[str, str] = {}
    for usage in usages:
        action, separator, revision = usage.partition("@")
        assert separator == "@", f"action reference has no revision: {usage}"
        assert action in APPROVED_ACTIONS, f"unapproved action: {action}"
        assert re.fullmatch(r"[0-9a-f]{40}", revision), f"action is not SHA-pinned: {usage}"
        assert revision == APPROVED_ACTIONS[action], f"unexpected revision for {action}"
        observed[action] = revision

    assert observed == APPROVED_ACTIONS


def test_release_plan_records_the_approved_trusted_publisher_and_recovery_contract() -> None:
    """A maintainer must have the exact future publisher tuple without logging in now."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    for value in (
        "Pending Trusted Publisher",
        REPOSITORY_OWNER,
        REPOSITORY_NAME,
        WORKFLOW_PATH.name,
        PYPI_ENVIRONMENT,
        RELEASE_TAG,
        "id-token: write",
        "attestation",
        "yank",
    ):
        assert value in release_plan
    assert "生产 PyPI" in release_plan
    assert "不使用 TestPyPI" in release_plan
    assert "不使用长期" in release_plan


def test_readme_exposes_the_noncommercial_open_meteo_limits_to_public_users() -> None:
    """The package README must disclose the approved upstream service boundary."""
    readme = read_text(README_PATH)

    assert "Open-Meteo" in readme
    assert "非商业" in readme
    assert "10,000" in readme
    assert "5,000" in readme
    assert "600" in readme
    assert "无 SLA" in readme or "没有项目自有 SLA" in readme
    assert "CC BY 4.0" in readme
