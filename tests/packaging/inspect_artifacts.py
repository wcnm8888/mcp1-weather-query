"""Inspect real F-002 wheel and sdist artifacts without installing them."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import tarfile
import zipfile
from email.message import Message
from email.parser import BytesParser
from email.policy import default
from pathlib import Path
from typing import Any, cast

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIST_DIRECTORY = PROJECT_ROOT / "dist"
EXPECTED_README = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

DISTRIBUTION_BASENAME = "mcp_weather_query"
DISTRIBUTION_NAME = "mcp-weather-query"
VERSION = "0.1.0"
WHEEL_NAME = f"{DISTRIBUTION_BASENAME}-{VERSION}-py3-none-any.whl"
SDIST_NAME = f"{DISTRIBUTION_BASENAME}-{VERSION}.tar.gz"
SDIST_ROOT = f"{DISTRIBUTION_BASENAME}-{VERSION}"
DIST_INFO = f"{DISTRIBUTION_BASENAME}-{VERSION}.dist-info"

PRODUCTION_FILES = frozenset(
    {
        "mcp_weather_query/__init__.py",
        "mcp_weather_query/__main__.py",
        "mcp_weather_query/errors.py",
        "mcp_weather_query/models.py",
        "mcp_weather_query/providers/__init__.py",
        "mcp_weather_query/providers/open_meteo.py",
        "mcp_weather_query/server.py",
        "mcp_weather_query/service.py",
        "mcp_weather_query/wmo.py",
    }
)

EXPECTED_WHEEL_FILES = PRODUCTION_FILES | {
    f"{DIST_INFO}/licenses/LICENSE",
    f"{DIST_INFO}/licenses/NOTICE",
    f"{DIST_INFO}/WHEEL",
    f"{DIST_INFO}/entry_points.txt",
    f"{DIST_INFO}/METADATA",
    f"{DIST_INFO}/RECORD",
}

EXPECTED_SDIST_FILES = {
    f"{SDIST_ROOT}/PKG-INFO",
    f"{SDIST_ROOT}/LICENSE",
    f"{SDIST_ROOT}/NOTICE",
    f"{SDIST_ROOT}/README.md",
    f"{SDIST_ROOT}/pyproject.toml",
} | {f"{SDIST_ROOT}/src/{name}" for name in PRODUCTION_FILES}

EXPECTED_REQUIRES_DIST = {
    "httpx>=0.28,<1",
    "mcp>=2,<3",
    "pydantic>=2.12,<3",
}

FORBIDDEN_CONTENT_MARKERS = (
    b"E:\\Agent",
    b"E:/Agent",
    b"C:\\Users",
    b"C:/Users",
    b".runtime/",
    b".runtime\\",
    b".venv/",
    b".venv\\",
)
SECRET_ASSIGNMENT = re.compile(
    rb"(?i)(api[_-]?key|authorization|password|secret|token)\s*[:=]\s*[\"'][^\"']{4,}[\"']"
)


class ArtifactContractError(AssertionError):
    """Raised when a built distribution violates the approved contract."""


def require(condition: bool, message: str) -> None:
    """Raise a focused artifact error instead of a bare assertion."""
    if not condition:
        raise ArtifactContractError(message)


def parse_metadata(payload: bytes) -> Message:
    """Parse Core Metadata headers and the embedded long description."""
    return BytesParser(policy=default).parsebytes(payload)


def parse_description(payload: bytes) -> str:
    """Decode the UTF-8 description without email's ASCII payload fallback."""
    normalized = payload.replace(b"\r\n", b"\n")
    parts = normalized.split(b"\n\n", maxsplit=1)
    require(len(parts) == 2, "Core Metadata has no long-description separator")
    return parts[1].decode("utf-8")


def metadata_values(message: Message, name: str) -> list[str]:
    """Return a typed list for a repeatable metadata field."""
    values = message.get_all(name, failobj=[])
    return [str(value) for value in values]


def validate_metadata(message: Message, description: str, *, source: str) -> None:
    """Validate identity, compatibility, dependencies, and legal metadata."""
    require(message.get("Metadata-Version") == "2.4", f"{source}: unexpected metadata version")
    require(message.get("Name") == DISTRIBUTION_NAME, f"{source}: wrong distribution name")
    require(message.get("Version") == VERSION, f"{source}: wrong distribution version")
    require(message.get("License-Expression") == "MIT", f"{source}: missing MIT expression")
    require(
        set(metadata_values(message, "License-File")) == {"LICENSE", "NOTICE"},
        f"{source}: wrong License-File values",
    )
    require(
        message.get("Requires-Python") == ">=3.12, <3.13",
        f"{source}: wrong Requires-Python",
    )
    require(
        set(metadata_values(message, "Requires-Dist")) == EXPECTED_REQUIRES_DIST,
        f"{source}: wrong runtime dependency metadata",
    )
    require("Open-Meteo" in description, f"{source}: README attribution is missing")
    require("CC BY 4.0" in description, f"{source}: data license link text is missing")
    require("wheel/sdist" in description, f"{source}: local artifact state is missing")
    require(
        description.replace("\r\n", "\n") == EXPECTED_README.replace("\r\n", "\n"),
        f"{source}: embedded README differs from the current project README",
    )


def scan_payload(name: str, payload: bytes) -> None:
    """Reject local paths, runtime directories, and obvious credential assignments."""
    for marker in FORBIDDEN_CONTENT_MARKERS:
        require(marker not in payload, f"{name}: contains forbidden local marker {marker!r}")
    require(SECRET_ASSIGNMENT.search(payload) is None, f"{name}: contains a secret-like assignment")


def normalized_text(payload: bytes) -> str:
    """Compare UTF-8 project text independently of Git's checkout line endings."""
    return payload.decode("utf-8").replace("\r\n", "\n")


def validate_record(archive: zipfile.ZipFile, file_names: set[str]) -> None:
    """Check RECORD coverage, sizes, and SHA-256 hashes."""
    record_name = f"{DIST_INFO}/RECORD"
    rows = list(csv.reader(io.StringIO(archive.read(record_name).decode("utf-8"))))
    require(all(len(row) == 3 for row in rows), "wheel RECORD has a malformed row")
    by_name = {row[0]: row for row in rows}
    require(set(by_name) == file_names, "wheel RECORD does not exactly cover archive files")

    for name in sorted(file_names):
        recorded_hash, recorded_size = by_name[name][1:]
        if name == record_name:
            require(not recorded_hash and not recorded_size, "RECORD must not hash itself")
            continue
        payload = archive.read(name)
        digest = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b"=").decode()
        require(recorded_hash == f"sha256={digest}", f"{name}: RECORD hash mismatch")
        require(recorded_size == str(len(payload)), f"{name}: RECORD size mismatch")


def inspect_wheel(path: Path) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Inspect exact wheel contents and metadata without installing it."""
    with zipfile.ZipFile(path) as archive:
        file_names = {name for name in archive.namelist() if not name.endswith("/")}
        require(file_names == EXPECTED_WHEEL_FILES, "wheel file list differs from the contract")
        payloads = {name: archive.read(name) for name in sorted(file_names)}

        for name, payload in payloads.items():
            scan_payload(name, payload)

        metadata_payload = payloads[f"{DIST_INFO}/METADATA"]
        metadata = parse_metadata(metadata_payload)
        validate_metadata(metadata, parse_description(metadata_payload), source="wheel METADATA")
        entry_points = payloads[f"{DIST_INFO}/entry_points.txt"].decode("utf-8")
        require(
            entry_points.replace("\r\n", "\n").rstrip("\n")
            == "[console_scripts]\nmcp-weather-query = mcp_weather_query.__main__:main",
            "wheel console entry point differs from the approved target",
        )
        wheel_text = payloads[f"{DIST_INFO}/WHEEL"].decode("utf-8")
        require("Root-Is-Purelib: true" in wheel_text, "wheel is not marked pure Python")
        require("Tag: py3-none-any" in wheel_text, "wheel platform tag is not portable")
        validate_record(archive, file_names)

    return payloads, {"files": len(file_names), "metadata_version": metadata["Metadata-Version"]}


def inspect_sdist(path: Path) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Inspect exact sdist contents and metadata without extracting it."""
    with tarfile.open(path, mode="r:gz") as archive:
        file_members = {member.name: member for member in archive.getmembers() if member.isfile()}
        require(
            set(file_members) == EXPECTED_SDIST_FILES, "sdist file list differs from the contract"
        )

        payloads: dict[str, bytes] = {}
        for name, member in sorted(file_members.items()):
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ArtifactContractError(f"sdist member cannot be read: {name}")
            payload = extracted.read()
            payloads[name] = payload
            scan_payload(name, payload)

        metadata_payload = payloads[f"{SDIST_ROOT}/PKG-INFO"]
        metadata = parse_metadata(metadata_payload)
        validate_metadata(metadata, parse_description(metadata_payload), source="sdist PKG-INFO")
        require(
            payloads[f"{SDIST_ROOT}/README.md"].decode("utf-8").replace("\r\n", "\n")
            == EXPECTED_README.replace("\r\n", "\n"),
            "sdist README differs from the current project README",
        )
        pyproject = payloads[f"{SDIST_ROOT}/pyproject.toml"].decode("utf-8")
        require('build-backend = "uv_build"' in pyproject, "sdist lost the build backend")
        require(
            'mcp-weather-query = "mcp_weather_query.__main__:main"' in pyproject,
            "sdist lost the console entry point",
        )

    return payloads, {"files": len(file_members), "metadata_version": metadata["Metadata-Version"]}


def sha256_file(path: Path) -> str:
    """Return a lowercase SHA-256 digest for evidence."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_artifacts(dist_directory: Path) -> dict[str, Any]:
    """Validate the two required artifacts and return a safe summary."""
    require(dist_directory.is_dir(), "dist directory does not exist")
    wheels = sorted(dist_directory.glob("*.whl"))
    sdists = sorted(dist_directory.glob("*.tar.gz"))
    require([path.name for path in wheels] == [WHEEL_NAME], "expected exactly the approved wheel")
    require([path.name for path in sdists] == [SDIST_NAME], "expected exactly the approved sdist")

    wheel = wheels[0]
    sdist = sdists[0]
    wheel_payloads, wheel_summary = inspect_wheel(wheel)
    sdist_payloads, sdist_summary = inspect_sdist(sdist)

    for production_name in PRODUCTION_FILES:
        source_payload = (PROJECT_ROOT / "src" / production_name).read_bytes()
        require(
            normalized_text(wheel_payloads[production_name]) == normalized_text(source_payload),
            f"wheel drift: {production_name}",
        )
        sdist_name = f"{SDIST_ROOT}/src/{production_name}"
        require(
            normalized_text(sdist_payloads[sdist_name]) == normalized_text(source_payload),
            f"sdist drift: {production_name}",
        )

    for legal_name in ("LICENSE", "NOTICE"):
        source_payload = (PROJECT_ROOT / legal_name).read_bytes()
        require(
            normalized_text(wheel_payloads[f"{DIST_INFO}/licenses/{legal_name}"])
            == normalized_text(source_payload),
            f"wheel legal file drift: {legal_name}",
        )
        require(
            normalized_text(sdist_payloads[f"{SDIST_ROOT}/{legal_name}"])
            == normalized_text(source_payload),
            f"sdist legal file drift: {legal_name}",
        )

    return {
        "wheel": {
            "name": wheel.name,
            "size": wheel.stat().st_size,
            "sha256": sha256_file(wheel),
            **wheel_summary,
        },
        "sdist": {
            "name": sdist.name,
            "size": sdist.stat().st_size,
            "sha256": sha256_file(sdist),
            **sdist_summary,
        },
    }


def parse_args() -> argparse.Namespace:
    """Parse an optional artifact directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist_directory", nargs="?", type=Path, default=DEFAULT_DIST_DIRECTORY)
    return parser.parse_args()


def main() -> None:
    """Run the artifact contract and print only a safe summary."""
    args = parse_args()
    summary = inspect_artifacts(cast(Path, args.dist_directory).resolve())
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
