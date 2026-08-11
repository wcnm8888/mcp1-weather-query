"""Test-only stdio Server with a deterministic result and no network access."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, cast

from mcp_weather_query.models import CurrentWeatherResult, LocationQuery
from mcp_weather_query.server import create_server

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "current_weather_success.json"
DIAGNOSTIC_MARKER = "f-001 fixed stdio server ready"


def load_fixed_result() -> dict[str, Any]:
    """Read the synthetic fixture owned by the offline test suite."""
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return cast(dict[str, Any], payload)


async def query_fixed_weather(query: LocationQuery) -> CurrentWeatherResult:
    """Return a fresh validated result while preserving normalized request input."""
    payload = load_fixed_result()
    payload["requested_location"] = query.location
    payload["country_code"] = query.country_code
    return CurrentWeatherResult.model_validate(payload)


mcp = create_server(query_fixed_weather)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(__name__).info(DIAGNOSTIC_MARKER)
    mcp.run()
