"""Explicit opt-in contract check against the real Open-Meteo free API."""

from __future__ import annotations

import os

import httpx
import pytest

from mcp_weather_query.models import CurrentWeatherResult, LocationQuery
from mcp_weather_query.providers.open_meteo import (
    FORECAST_ENDPOINT,
    GEOCODING_ENDPOINT,
    OpenMeteoProvider,
)
from mcp_weather_query.service import WeatherService

LIVE_OPT_IN_VARIABLE = "MCP_WEATHER_RUN_LIVE"
RUN_LIVE = os.environ.get(LIVE_OPT_IN_VARIABLE) == "1"

pytestmark = [
    pytest.mark.contract,
    pytest.mark.skipif(
        not RUN_LIVE,
        reason=f"set {LIVE_OPT_IN_VARIABLE}=1 to run the real Open-Meteo contract",
    ),
]


@pytest.mark.asyncio
async def test_real_open_meteo_current_weather_contract() -> None:
    """Validate both approved endpoints without asserting dynamic weather values."""
    observed_urls: list[str] = []

    async def record_request(request: httpx.Request) -> None:
        observed_urls.append(str(request.url.copy_with(query=None)))

    async with httpx.AsyncClient(
        event_hooks={"request": [record_request]}, trust_env=False
    ) as client:
        result = await WeatherService(OpenMeteoProvider(client)).get_current_weather(
            LocationQuery(location="Beijing", country_code="CN")
        )

    validated = CurrentWeatherResult.model_validate(result)
    assert observed_urls == [GEOCODING_ENDPOINT, FORECAST_ENDPOINT]
    assert validated.requested_location == "Beijing"
    assert validated.country_code == "CN"
    assert validated.resolved_location.country_code == "CN"
    assert validated.resolved_location.name
    assert validated.resolved_location.country
    assert validated.resolved_location.timezone
    assert -90 <= validated.resolved_location.latitude <= 90
    assert -180 <= validated.resolved_location.longitude <= 180
    assert validated.current.time
    assert validated.current.interval_seconds > 0
    assert validated.metadata.provider == "Open-Meteo"
    assert validated.metadata.model_based_current_conditions is True
    assert validated.metadata.attribution == "Weather data by Open-Meteo.com"
    assert validated.metadata.license_url == "https://creativecommons.org/licenses/by/4.0/"
