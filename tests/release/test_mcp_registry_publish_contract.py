"""Executable R-002 contract for a least-privilege MCP Registry registration.

These checks are static and offline.  They define the approved public identity,
authorization separation, immutable-version recovery, and CI boundaries without
running mcp-publisher or contacting the Registry.
"""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
from pathlib import Path
from typing import Any, cast

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = PROJECT_ROOT / "server.json"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
README_PATH = PROJECT_ROOT / "README.md"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
RELEASE_PLAN_PATH = PROJECT_ROOT / "docs" / "release-plan.md"
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "release.yml"

SCHEMA_URL = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"
SERVER_NAME = "io.github.wcnm8888/mcp1-weather-query"
DISTRIBUTION_NAME = "mcp-weather-query"
VERSION = "0.1.0"
REPOSITORY_URL = "https://github.com/wcnm8888/mcp1-weather-query"
PUBLISHER_VERSION = "v1.8.1"
PUBLISHER_SHA256 = "399ad0d6e00a50812b563a71d8bfbff5160c085e6b13aac6ec083d98d5ff7c45"
MANIFEST_CANONICAL_SHA256 = "7363235e462331ea3ea12914eacd959a43bb6fb556caad35ff087983d5e39f0d"


def read_text(path: Path) -> str:
    """Read one UTF-8 project file without invoking external tooling."""
    return path.read_text(encoding="utf-8")


def load_manifest() -> dict[str, Any]:
    """Load the Registry manifest without validating or publishing it."""
    return cast(dict[str, Any], json.loads(read_text(MANIFEST_PATH)))


def load_pyproject() -> dict[str, Any]:
    """Load package metadata for identity cross-checks."""
    return tomllib.loads(read_text(PYPROJECT_PATH))


def canonical_manifest_sha256(manifest: dict[str, Any]) -> str:
    """Hash semantic JSON content independently of indentation and line endings."""
    payload = json.dumps(
        manifest,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def test_registry_identity_matches_the_public_pypi_release() -> None:
    """The Registry record must describe the already-published 0.1.0 package."""
    manifest = load_manifest()
    project = load_pyproject()["project"]
    readme = read_text(README_PATH)

    assert manifest["$schema"] == SCHEMA_URL
    assert manifest["name"] == SERVER_NAME
    assert manifest["version"] == VERSION
    assert manifest["repository"] == {"url": REPOSITORY_URL, "source": "github"}
    assert project["name"] == DISTRIBUTION_NAME
    assert project["version"] == VERSION
    assert f"mcp-name: {SERVER_NAME}" in readme
    assert canonical_manifest_sha256(manifest) == MANIFEST_CANONICAL_SHA256


def test_registry_manifest_has_one_minimal_pypi_stdio_package() -> None:
    """Registration must not add another package, version, transport, or runtime."""
    manifest = load_manifest()

    assert set(manifest) == {
        "$schema",
        "name",
        "title",
        "description",
        "version",
        "repository",
        "packages",
    }
    assert manifest["packages"] == [
        {
            "registryType": "pypi",
            "identifier": DISTRIBUTION_NAME,
            "version": VERSION,
            "runtimeHint": "uvx",
            "transport": {"type": "stdio"},
        }
    ]
    assert "remotes" not in manifest


def test_public_readme_records_the_verified_registry_registration() -> None:
    """Public users must see the exact active Registry identity and verification state."""
    readme = read_text(README_PATH)

    assert SERVER_NAME in readme
    assert "已登记到 Official MCP Registry" in readme
    assert "active" in readme
    assert "官方 API" in readme
    assert "尚未登记 MCP Registry" not in readme
    assert "尚未执行 Registry publish" not in readme


def test_post_publish_docs_record_registry_success_and_credential_disposal() -> None:
    """Release docs must preserve publication evidence and the official logout boundary."""
    changelog = read_text(CHANGELOG_PATH)
    release_plan = read_text(RELEASE_PLAN_PATH)

    for value in (SERVER_NAME, "Official MCP Registry", "已登记"):
        assert value in changelog
    for value in (
        "Step 8",
        "仅执行一次",
        "Step 9",
        "active",
        "mcp-publisher logout",
        "认证文件",
    ):
        assert value in release_plan


def test_release_plan_discloses_registry_preview_and_public_data_terms() -> None:
    """A maintainer must understand the public and preview boundaries before login."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    for value in (
        "preview",
        "CC0 1.0",
        "GitHub 用户名",
        "仓库保持 private",
        "公开 PyPI",
    ):
        assert value in release_plan


def test_release_plan_freezes_manual_github_oauth_and_separate_authorizations() -> None:
    """Login must be manual and must never imply permission to publish."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    for value in (
        "GitHub OAuth",
        "device flow",
        SERVER_NAME,
        "login 不授权 publish",
        "不配置 Registry GitHub Actions",
    ):
        assert value in release_plan


def test_release_plan_separates_validate_login_publish_and_public_verification() -> None:
    """The four network gates must remain distinct and ordered."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    required_steps = {
        "Step 3": "validate",
        "Step 7": "login",
        "Step 8": "publish",
        "Step 9": "官方 API",
    }
    positions: list[int] = []
    for step, action in required_steps.items():
        match = re.search(rf"(?is){re.escape(step)}.*?{re.escape(action)}", release_plan)
        assert match is not None, f"release plan must bind {step} to {action}"
        positions.append(match.start())
    assert positions == sorted(positions), "Registry network gates must remain ordered"


def test_release_plan_defines_immutable_version_and_uncertain_publish_recovery() -> None:
    """An ambiguous publish result must be queried, never blindly retried or overwritten."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    for value in (
        "同版本不可原地覆盖",
        "不得盲目重试",
        "官方 API 精确查询",
        "完全一致",
        "不一致",
        "deprecated",
        "deleted",
    ):
        assert value in release_plan


def test_release_plan_keeps_the_verified_publisher_binary_outside_project_path() -> None:
    """R-002 reuses the already-verified publisher and must not replace or install it."""
    release_plan = read_text(RELEASE_PLAN_PATH)

    assert PUBLISHER_VERSION in release_plan
    assert PUBLISHER_SHA256 in release_plan
    assert "未加入 PATH" in release_plan
    assert "不下载" in release_plan or "不得下载" in release_plan


def test_github_workflow_cannot_validate_login_or_publish_the_registry() -> None:
    """R-002 is manual; existing CI must not gain a Registry authentication path."""
    workflow = read_text(WORKFLOW_PATH)
    folded = workflow.casefold()

    assert "mcp-publisher" not in folded
    assert "registry.modelcontextprotocol.io" not in folded
    assert "server.json" not in folded
    assert "workflow_dispatch" not in folded


def test_manifest_contains_no_credentials_or_remote_transport_configuration() -> None:
    """The public manifest must remain credential-free and stdio-only."""
    serialized = json.dumps(load_manifest(), ensure_ascii=False).casefold()

    for forbidden in (
        "environmentvariables",
        "runtimearguments",
        "packagearguments",
        "streamable-http",
        '"sse"',
        "api_key",
        "apikey",
        "authorization",
        "password",
        "secret",
        "token",
    ):
        assert forbidden not in serialized
