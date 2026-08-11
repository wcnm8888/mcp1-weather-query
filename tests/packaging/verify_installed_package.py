"""Verify one installed F-002/D-001 artifact outside the source tree.

The default mode checks import provenance, the production console entry point,
and a deterministic test-only MCP child.  ``serve-fixed`` is deliberately not a
published entry point and never performs network I/O.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast
from urllib.parse import unquote, urlparse

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp_types.version import LATEST_HANDSHAKE_VERSION, LATEST_MODERN_VERSION

import mcp_weather_query
from mcp_weather_query.models import CurrentWeatherResult, LocationQuery
from mcp_weather_query.server import TOOL_NAME, create_server

DISTRIBUTION_NAME = "mcp-weather-query"
DISTRIBUTION_VERSION = "0.1.0"
CONSOLE_NAME = "mcp-weather-query"
CONSOLE_TARGET = "mcp_weather_query.__main__:main"
ARTIFACT_FILENAMES = {
    "wheel": "mcp_weather_query-0.1.0-py3-none-any.whl",
    "sdist": "mcp_weather_query-0.1.0.tar.gz",
}
PROCESS_TIMEOUT_SECONDS = 10.0
DIAGNOSTIC_MARKER = "release candidate installed fixed stdio server ready"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src"


def clean_child_environment() -> dict[str, str]:
    """Return a small environment with no source or active-venv injection."""
    inherited_names = (
        "APPDATA",
        "COMSPEC",
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
            "PYTHONUNBUFFERED": "1",
            "PYTHONUTF8": "1",
        }
    )
    return environment


def require(condition: bool, message: str) -> None:
    """Raise an explicit verification failure."""
    if not condition:
        raise AssertionError(message)


def is_within(path: Path, parent: Path) -> bool:
    """Compare resolved Windows paths without depending on path-case spelling."""
    path_text = os.path.normcase(str(path.resolve()))
    parent_text = os.path.normcase(str(parent.resolve()))
    return os.path.commonpath((path_text, parent_text)) == parent_text


def verify_install_provenance(
    expected_environment: Path, console: Path, artifact_kind: str
) -> dict[str, str]:
    """Prove imports and the console script come from the requested clean env."""
    module_name = mcp_weather_query.__file__
    require(module_name is not None, "installed package has no import origin")
    module_path = Path(module_name).resolve()
    interpreter = Path(sys.executable).resolve()
    expected_environment = expected_environment.resolve()
    console = console.resolve()

    require(is_within(interpreter, expected_environment), "verifier is not using the clean env")
    require(is_within(module_path, expected_environment), "package import did not use clean env")
    require(not is_within(module_path, SOURCE_ROOT), "package import leaked from project src")
    require(is_within(console, expected_environment), "console script is outside clean env")
    require(console.is_file(), "installed console script is missing")

    for entry in sys.path:
        if not entry:
            continue
        candidate = Path(entry)
        if candidate.exists():
            require(
                not is_within(candidate, SOURCE_ROOT),
                "project src is unexpectedly present on sys.path",
            )

    distribution = importlib.metadata.distribution(DISTRIBUTION_NAME)
    require(distribution.version == DISTRIBUTION_VERSION, "installed version is incorrect")
    console_entries = [
        entry
        for entry in distribution.entry_points
        if entry.group == "console_scripts" and entry.name == CONSOLE_NAME
    ]
    require(len(console_entries) == 1, "installed console entry point is not unique")
    require(console_entries[0].value == CONSOLE_TARGET, "installed console target is incorrect")

    direct_url_text = distribution.read_text("direct_url.json")
    if direct_url_text is None:
        raise AssertionError("installed distribution has no direct_url provenance")
    direct_url = json.loads(direct_url_text)
    if not isinstance(direct_url, dict):
        raise AssertionError("installed direct_url provenance is not an object")
    url = direct_url.get("url")
    if not isinstance(url, str):
        raise AssertionError("installed direct_url provenance has no URL")
    require(urlparse(url).scheme == "file", "installed artifact did not come from a local file")
    artifact_filename = Path(unquote(urlparse(url).path)).name
    require(
        artifact_filename == ARTIFACT_FILENAMES[artifact_kind],
        "installed artifact filename differs from the requested wheel/sdist",
    )
    require("dir_info" not in direct_url, "installed distribution is editable or directory-based")

    return {
        "artifact_origin": artifact_filename,
        "distribution": f"{DISTRIBUTION_NAME}=={distribution.version}",
        "module_origin": str(module_path.relative_to(expected_environment)),
        "console_origin": str(console.relative_to(expected_environment)),
    }


async def send_message(process: asyncio.subprocess.Process, payload: dict[str, Any]) -> None:
    """Write one newline-delimited JSON-RPC message."""
    if process.stdin is None:
        raise AssertionError("child stdin is unavailable")
    wire = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    process.stdin.write(wire.encode("utf-8"))
    await process.stdin.drain()


async def read_message(process: asyncio.subprocess.Process) -> dict[str, Any]:
    """Read one complete protocol response within the bounded timeout."""
    if process.stdout is None:
        raise AssertionError("child stdout is unavailable")
    line = await asyncio.wait_for(process.stdout.readline(), timeout=PROCESS_TIMEOUT_SECONDS)
    require(bool(line), "stdio child closed before returning a response")
    decoded = json.loads(line.decode("utf-8"))
    require(isinstance(decoded, dict), "stdio child returned a non-object JSON message")
    return cast(dict[str, Any], decoded)


async def verify_raw_console(console: Path, work_directory: Path) -> dict[str, Any]:
    """Inspect the real console process streams, handshake, discovery, and exit."""
    process = await asyncio.create_subprocess_exec(
        str(console),
        cwd=work_directory,
        env=clean_child_environment(),
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
                    "clientInfo": {"name": "f-002-installed-raw", "version": "0.0.0"},
                },
            },
        )
        initialized = await read_message(process)
        require(initialized.get("id") == 1, "initialize response id is incorrect")
        result = initialized.get("result")
        if not isinstance(result, dict):
            raise AssertionError("initialize response has no result")
        require(
            result.get("protocolVersion") == LATEST_HANDSHAKE_VERSION,
            "raw handshake negotiated an unexpected version",
        )

        await send_message(process, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        await send_message(
            process,
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        listed = await read_message(process)
        require(listed.get("id") == 2, "tools/list response id is incorrect")
        listed_result = listed.get("result")
        if not isinstance(listed_result, dict):
            raise AssertionError("tools/list response has no result")
        tools = listed_result.get("tools")
        if not isinstance(tools, list):
            raise AssertionError("tools/list did not return a list")
        names = [tool.get("name") for tool in tools if isinstance(tool, dict)]
        require(names == [TOOL_NAME], "installed console exposed an unexpected Tool set")

        if process.stdin is None:
            raise AssertionError("child stdin disappeared")
        process.stdin.close()
        await process.stdin.wait_closed()
        return_code = await asyncio.wait_for(process.wait(), timeout=PROCESS_TIMEOUT_SECONDS)
        require(return_code == 0, f"installed console exited with {return_code}")

        if process.stdout is None:
            raise AssertionError("child stdout disappeared")
        remaining_stdout = await asyncio.wait_for(
            process.stdout.read(), timeout=PROCESS_TIMEOUT_SECONDS
        )
        require(remaining_stdout == b"", "stdout contains text outside MCP protocol responses")

        if process.stderr is None:
            raise AssertionError("child stderr disappeared")
        stderr = (
            await asyncio.wait_for(process.stderr.read(), timeout=PROCESS_TIMEOUT_SECONDS)
        ).decode("utf-8")
        require("Traceback" not in stderr, "installed console emitted a traceback")
        return {
            "exit_code": return_code,
            "handshake_protocol": LATEST_HANDSHAKE_VERSION,
            "stderr_traceback": False,
            "stdout_protocol_only": True,
            "tools": names,
        }
    finally:
        if process.returncode is None:
            process.kill()
            await asyncio.wait_for(process.wait(), timeout=PROCESS_TIMEOUT_SECONDS)


def server_parameters(
    command: Path, args: list[str], work_directory: Path
) -> StdioServerParameters:
    """Create official-SDK parameters with the same source-free environment."""
    return StdioServerParameters(
        command=str(command),
        args=args,
        env=clean_child_environment(),
        cwd=work_directory,
        encoding="utf-8",
        encoding_error_handler="strict",
    )


async def verify_modern_console(
    console: Path, work_directory: Path, stderr_path: Path
) -> dict[str, Any]:
    """Use the official v2 Client to prove modern discovery from the console."""
    with stderr_path.open("w+", encoding="utf-8") as errlog:
        async with Client(
            stdio_client(server_parameters(console, [], work_directory), errlog=errlog),
            mode="auto",
            raise_exceptions=True,
        ) as client:
            listed = await asyncio.wait_for(client.list_tools(), timeout=PROCESS_TIMEOUT_SECONDS)
            protocol_version = client.protocol_version
            discover_result = client.session.discover_result
            initialize_result = client.session.initialize_result

        errlog.seek(0)
        stderr = errlog.read()

    names = [tool.name for tool in listed.tools]
    require(names == [TOOL_NAME], "modern Client discovered an unexpected Tool set")
    require(protocol_version == LATEST_MODERN_VERSION, "modern protocol version is incorrect")
    if discover_result is None:
        raise AssertionError("modern discovery result is missing")
    require(
        LATEST_MODERN_VERSION in discover_result.supported_versions,
        "Server did not advertise the current modern protocol",
    )
    require(initialize_result is None, "modern v2 Client unexpectedly used legacy initialize")
    require("Traceback" not in stderr, "modern console child emitted a traceback")
    return {"protocol": protocol_version, "tools": names}


async def fixed_weather(query: LocationQuery) -> CurrentWeatherResult:
    """Return synthetic conditions without reading project fixtures or using HTTP."""
    return CurrentWeatherResult.model_validate(
        {
            "requested_location": query.location,
            "country_code": query.country_code,
            "resolved_location": {
                "name": "北京市",
                "country": "中国",
                "country_code": "CN",
                "admin1": "北京市",
                "latitude": 39.9042,
                "longitude": 116.4074,
                "timezone": "Asia/Shanghai",
            },
            "current": {
                "time": "2026-08-11T14:00:00+08:00",
                "interval_seconds": 900,
                "is_day": True,
                "temperature_c": 31.2,
                "apparent_temperature_c": 34.1,
                "relative_humidity_percent": 61,
                "precipitation_mm": 0.0,
                "weather_code": 1,
                "condition": "Mainly clear",
                "wind_speed_kmh": 8.4,
                "wind_direction_degrees": 170,
            },
            "metadata": {
                "units": {
                    "temperature_c": "°C",
                    "apparent_temperature_c": "°C",
                    "relative_humidity_percent": "%",
                    "precipitation_mm": "mm",
                    "wind_speed_kmh": "km/h",
                    "wind_direction_degrees": "°",
                },
                "provider": "Open-Meteo",
                "model_based_current_conditions": True,
                "attribution": "Weather data by Open-Meteo.com",
                "license_url": "https://creativecommons.org/licenses/by/4.0/",
            },
        }
    )


async def verify_deterministic_call(
    interpreter: Path, work_directory: Path, stderr_path: Path
) -> dict[str, Any]:
    """Call a test-only child that imports the installed package implementation."""
    parameters = server_parameters(
        interpreter,
        [str(Path(__file__).resolve()), "serve-fixed"],
        work_directory,
    )
    with stderr_path.open("w+", encoding="utf-8") as errlog:
        async with Client(
            stdio_client(parameters, errlog=errlog), mode="auto", raise_exceptions=True
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

        errlog.seek(0)
        stderr = errlog.read()

    names = [tool.name for tool in listed.tools]
    require(names == [TOOL_NAME], "fixed installed child exposed an unexpected Tool set")
    require(listed.tools[0].output_schema is not None, "installed Tool lost outputSchema")
    require(protocol_version == LATEST_MODERN_VERSION, "fixed child protocol is incorrect")
    require(result.is_error is False, "deterministic installed Tool call failed")
    require(result.structured_content is not None, "Tool call has no structuredContent")
    validated = CurrentWeatherResult.model_validate(result.structured_content)
    require(validated.requested_location == "北京", "Tool input normalization changed")
    require(validated.country_code == "CN", "country code normalization changed")
    require(validated.resolved_location.name == "北京市", "fixed resolved location changed")
    require("result" not in result.structured_content, "structuredContent gained a wrapper")
    require(DIAGNOSTIC_MARKER in stderr, "test diagnostic did not use stderr")
    require("Traceback" not in stderr, "fixed installed child emitted a traceback")
    return {
        "protocol": protocol_version,
        "structured_content": True,
        "stderr_diagnostic": True,
        "tools": names,
    }


async def verify(args: argparse.Namespace) -> dict[str, Any]:
    """Run all installed-artifact checks and return a path-minimized summary."""
    expected_environment = cast(Path, args.expected_environment).resolve()
    console = cast(Path, args.console).resolve()
    work_directory = cast(Path, args.work_directory).resolve()
    require(work_directory.is_dir(), "external work directory does not exist")
    require(not is_within(work_directory, PROJECT_ROOT), "work directory is inside project")
    require("PYTHONPATH" not in clean_child_environment(), "clean child leaked PYTHONPATH")
    require("VIRTUAL_ENV" not in clean_child_environment(), "clean child leaked VIRTUAL_ENV")

    provenance = verify_install_provenance(
        expected_environment, console, cast(str, args.artifact_kind)
    )
    raw = await verify_raw_console(console, work_directory)
    modern = await verify_modern_console(
        console, work_directory, work_directory / "production-modern-stderr.log"
    )
    deterministic = await verify_deterministic_call(
        Path(sys.executable), work_directory, work_directory / "fixed-stderr.log"
    )
    return {
        "artifact_kind": args.artifact_kind,
        "clean_environment": expected_environment.name,
        "provenance": provenance,
        "production_console": raw,
        "modern_discovery": modern,
        "deterministic_call": deterministic,
    }


def parse_args() -> argparse.Namespace:
    """Parse verification or test-only Server mode arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("verify", "serve-fixed"), default="verify")
    parser.add_argument("--artifact-kind", choices=("wheel", "sdist"))
    parser.add_argument("--expected-environment", type=Path)
    parser.add_argument("--console", type=Path)
    parser.add_argument("--work-directory", type=Path)
    return parser.parse_args()


def main() -> None:
    """Run one mode; only the parent verifier prints a safe summary."""
    args = parse_args()
    if args.mode == "serve-fixed":
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).info(DIAGNOSTIC_MARKER)
        create_server(fixed_weather).run()
        return

    missing = [
        name
        for name in ("artifact_kind", "expected_environment", "console", "work_directory")
        if getattr(args, name) is None
    ]
    require(not missing, f"verify mode is missing arguments: {', '.join(missing)}")
    summary = asyncio.run(verify(args))
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
