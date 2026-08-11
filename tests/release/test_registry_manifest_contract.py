"""Static D-001 contract for the local-only MCP Registry draft."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any, cast

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = PROJECT_ROOT / "server.json"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
README_PATH = PROJECT_ROOT / "README.md"

SCHEMA_URL = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"
SERVER_NAME = "io.github.wcnm8888/mcp1-weather-query"
DISTRIBUTION_NAME = "mcp-weather-query"
VERSION = "0.1.0"
REPOSITORY_URL = "https://github.com/wcnm8888/mcp1-weather-query"


def load_manifest() -> dict[str, Any]:
    """Load the Registry draft without calling a registry or publisher."""
    return cast(dict[str, Any], json.loads(MANIFEST_PATH.read_text(encoding="utf-8")))


def load_pyproject() -> dict[str, Any]:
    """Load package identity for cross-document checks."""
    return tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))


def test_registry_manifest_has_the_approved_server_identity() -> None:
    manifest = load_manifest()

    assert manifest["$schema"] == SCHEMA_URL
    assert manifest["name"] == SERVER_NAME
    assert manifest["title"] == "MCP1 Weather Query"
    assert manifest["version"] == VERSION
    assert manifest["description"] == (
        "Read-only current weather lookup by place name using Open-Meteo."
    )


def test_registry_manifest_references_one_fixed_pypi_stdio_package() -> None:
    manifest = load_manifest()

    assert manifest["packages"] == [
        {
            "registryType": "pypi",
            "identifier": DISTRIBUTION_NAME,
            "version": VERSION,
            "runtimeHint": "uvx",
            "transport": {"type": "stdio"},
        }
    ]


def test_registry_manifest_matches_package_readme_and_repository() -> None:
    manifest = load_manifest()
    project = load_pyproject()["project"]
    readme = README_PATH.read_text(encoding="utf-8")

    assert project["name"] == DISTRIBUTION_NAME
    assert project["version"] == VERSION
    assert f"mcp-name: {SERVER_NAME}" in readme
    assert manifest["repository"] == {"url": REPOSITORY_URL, "source": "github"}


def test_registry_manifest_does_not_expand_transport_or_secret_scope() -> None:
    manifest = load_manifest()
    serialized = json.dumps(manifest, ensure_ascii=False).casefold()

    assert "remotes" not in manifest
    assert "environmentvariables" not in serialized
    assert "packagearguments" not in serialized
    assert "runtimearguments" not in serialized
    assert "streamable-http" not in serialized
    assert '"sse"' not in serialized
    assert "api_key" not in serialized
    assert "apikey" not in serialized
    assert "token" not in serialized
    assert "password" not in serialized
    assert "secret" not in serialized
