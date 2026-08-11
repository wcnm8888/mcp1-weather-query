"""Shared deterministic fixtures for the offline F-001 test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest


def load_json_fixture(name: str) -> dict[str, Any]:
    """Load a synthetic JSON object from the fixture directory."""
    fixture_path = Path(__file__).parent / "fixtures" / name
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    return cast(dict[str, Any], payload)


@pytest.fixture
def current_weather_payload() -> dict[str, Any]:
    """Load the synthetic structured weather result used by model tests."""
    return load_json_fixture("current_weather_success.json")


@pytest.fixture
def geocoding_payload() -> dict[str, Any]:
    """Load a synthetic Open-Meteo geocoding response."""
    return load_json_fixture("open_meteo_geocoding_success.json")


@pytest.fixture
def forecast_payload() -> dict[str, Any]:
    """Load a synthetic Open-Meteo current weather response."""
    return load_json_fixture("open_meteo_forecast_success.json")
