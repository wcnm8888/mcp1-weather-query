"""Real-process stdio checks for the F-001 MCP boundary."""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

import pytest
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp_types.version import LATEST_HANDSHAKE_VERSION, LATEST_MODERN_VERSION

from mcp_weather_query.models import CurrentWeatherResult
from mcp_weather_query.server import TOOL_NAME

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src"
FIXED_SERVER_SCRIPT = Path(__file__).with_name("stdio_fixed_server.py")
PRODUCTION_SERVER_MODULE = "mcp_weather_query"
PROCESS_TIMEOUT_SECONDS = 10.0
DIAGNOSTIC_MARKER = "f-001 fixed stdio server ready"


def child_environment() -> dict[str, str]:
    """Return a credential-free environment sufficient for the local child."""
    inherited_names = (
        "APPDATA",
        "HOMEDRIVE",
        "HOMEPATH",
        "LOCALAPPDATA",
        "PATH",
        "PATHEXT",
        "PROCESSOR_ARCHITECTURE",
        "SYSTEMDRIVE",
        "SYSTEMROOT",
        "TEMP",
        "TMP",
        "USERNAME",
        "USERPROFILE",
        "WINDIR",
    )
    environment = {
        name: value for name in inherited_names if (value := os.environ.get(name)) is not None
    }
    environment.update(
        {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONPATH": str(SOURCE_ROOT),
            "PYTHONUNBUFFERED": "1",
            "PYTHONUTF8": "1",
        }
    )
    return environment


def fixed_server_parameters() -> StdioServerParameters:
    """Launch the test-only server with the exact project interpreter."""
    return StdioServerParameters(
        command=sys.executable,
        args=[str(FIXED_SERVER_SCRIPT)],
        env=child_environment(),
        cwd=PROJECT_ROOT,
        encoding="utf-8",
        encoding_error_handler="strict",
    )


def production_server_parameters() -> StdioServerParameters:
    """Launch the production module with the exact project interpreter."""
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", PRODUCTION_SERVER_MODULE],
        env=child_environment(),
        cwd=PROJECT_ROOT,
        encoding="utf-8",
        encoding_error_handler="strict",
    )


async def send_message(process: asyncio.subprocess.Process, payload: dict[str, Any]) -> None:
    """Send one newline-delimited JSON-RPC message to a child process."""
    assert process.stdin is not None
    wire_message = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    process.stdin.write(wire_message.encode("utf-8"))
    await process.stdin.drain()


async def read_message(process: asyncio.subprocess.Process) -> dict[str, Any]:
    """Read and parse one protocol line, failing rather than hanging."""
    assert process.stdout is not None
    line = await asyncio.wait_for(process.stdout.readline(), timeout=PROCESS_TIMEOUT_SECONDS)
    assert line, "stdio server closed stdout before returning a response"
    decoded = json.loads(line.decode("utf-8"))
    assert isinstance(decoded, dict)
    return cast(dict[str, Any], decoded)


@pytest.mark.asyncio
async def test_production_entrypoint_handshake_discovery_and_clean_exit() -> None:
    """Exercise the production module over raw stdio and inspect its real streams."""
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        PRODUCTION_SERVER_MODULE,
        cwd=PROJECT_ROOT,
        env=child_environment(),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )

    try:
        await send_message(
            process,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": LATEST_HANDSHAKE_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "f-001-stdio-smoke", "version": "0.0.0"},
                },
            },
        )
        initialize_response = await read_message(process)
        assert initialize_response["id"] == 1
        assert "result" in initialize_response
        assert initialize_response["result"]["protocolVersion"] == LATEST_HANDSHAKE_VERSION

        await send_message(
            process,
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
        )
        await send_message(
            process,
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        tools_response = await read_message(process)
        assert tools_response["id"] == 2
        tools = tools_response["result"]["tools"]
        assert [tool["name"] for tool in tools] == [TOOL_NAME]

        assert process.stdin is not None
        process.stdin.close()
        await process.stdin.wait_closed()
        return_code = await asyncio.wait_for(process.wait(), timeout=PROCESS_TIMEOUT_SECONDS)
        assert return_code == 0

        assert process.stdout is not None
        remaining_stdout = await asyncio.wait_for(
            process.stdout.read(), timeout=PROCESS_TIMEOUT_SECONDS
        )
        assert remaining_stdout == b""

        assert process.stderr is not None
        stderr = (
            await asyncio.wait_for(process.stderr.read(), timeout=PROCESS_TIMEOUT_SECONDS)
        ).decode("utf-8")
        assert "Traceback" not in stderr
    finally:
        if process.returncode is None:
            process.kill()
            await asyncio.wait_for(process.wait(), timeout=PROCESS_TIMEOUT_SECONDS)


@pytest.mark.asyncio
async def test_official_v2_client_discovers_production_server_over_modern_stdio(
    tmp_path: Path,
) -> None:
    """Prove the production stdio entry serves MCP 2026 without a legacy handshake."""
    stderr_path = tmp_path / "production-modern-stderr.log"
    with stderr_path.open("w+", encoding="utf-8") as errlog:
        async with Client(
            stdio_client(production_server_parameters(), errlog=errlog),
            mode="auto",
            raise_exceptions=True,
        ) as client:
            listed = await asyncio.wait_for(client.list_tools(), timeout=PROCESS_TIMEOUT_SECONDS)
            protocol_version = client.protocol_version
            discover_result = client.session.discover_result
            initialize_result = client.session.initialize_result

        errlog.seek(0)
        stderr = errlog.read()

    assert protocol_version == LATEST_MODERN_VERSION
    assert discover_result is not None
    assert LATEST_MODERN_VERSION in discover_result.supported_versions
    assert initialize_result is None
    assert [tool.name for tool in listed.tools] == [TOOL_NAME]
    assert "Traceback" not in stderr


@pytest.mark.asyncio
async def test_official_v2_client_calls_deterministic_tool_over_modern_stdio(
    tmp_path: Path,
) -> None:
    """Use MCP 2026 against a test-only child without live HTTP."""
    stderr_path = tmp_path / "fixed-server-stderr.log"
    with stderr_path.open("w+", encoding="utf-8") as errlog:
        async with Client(
            stdio_client(fixed_server_parameters(), errlog=errlog),
            mode="auto",
            raise_exceptions=True,
        ) as client:
            listed = await asyncio.wait_for(client.list_tools(), timeout=PROCESS_TIMEOUT_SECONDS)
            result = await asyncio.wait_for(
                client.call_tool(
                    TOOL_NAME,
                    {"location": "  北京  ", "country_code": "cn"},
                ),
                timeout=PROCESS_TIMEOUT_SECONDS,
            )
            protocol_version = client.protocol_version
            discover_result = client.session.discover_result
            initialize_result = client.session.initialize_result

        errlog.seek(0)
        stderr = errlog.read()

    assert [tool.name for tool in listed.tools] == [TOOL_NAME]
    assert listed.tools[0].output_schema is not None
    assert protocol_version == LATEST_MODERN_VERSION
    assert discover_result is not None
    assert initialize_result is None
    assert result.is_error is False
    assert result.structured_content is not None
    validated = CurrentWeatherResult.model_validate(result.structured_content)
    assert validated.requested_location == "北京"
    assert validated.country_code == "CN"
    assert validated.resolved_location.name == "北京市"
    assert "result" not in result.structured_content
    assert DIAGNOSTIC_MARKER in stderr
    assert "Traceback" not in stderr
