"""Unit tests for the transport-independent weather application service."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from mcp_weather_query.errors import WeatherErrorCode, WeatherServiceError
from mcp_weather_query.models import CurrentConditions, LocationQuery, ResolvedLocation
from mcp_weather_query.service import WeatherService


@dataclass
class StubProvider:
    location: ResolvedLocation
    current: CurrentConditions
    resolve_error: WeatherServiceError | None = None
    fetch_calls: int = 0

    async def resolve_location(self, query: LocationQuery) -> ResolvedLocation:
        if self.resolve_error is not None:
            raise self.resolve_error
        return self.location

    async def fetch_current(self, location: ResolvedLocation) -> CurrentConditions:
        self.fetch_calls += 1
        return self.current


def resolved_location() -> ResolvedLocation:
    return ResolvedLocation(
        name="Beijing",
        country="China",
        country_code="CN",
        admin1="Beijing",
        latitude=39.9075,
        longitude=116.3972,
        timezone="Asia/Shanghai",
    )


def current_conditions() -> CurrentConditions:
    return CurrentConditions(
        time="2026-08-11T14:00",
        interval_seconds=900,
        is_day=True,
        temperature_c=31.2,
        apparent_temperature_c=34.1,
        relative_humidity_percent=61,
        precipitation_mm=0.0,
        weather_code=1,
        condition="Mainly clear",
        wind_speed_kmh=8.4,
        wind_direction_degrees=170,
    )


@pytest.mark.asyncio
async def test_service_builds_complete_structured_result() -> None:
    provider = StubProvider(location=resolved_location(), current=current_conditions())
    service = WeatherService(provider)

    result = await service.get_current_weather(
        LocationQuery(location="  北京  ", country_code="cn")
    )

    assert result.requested_location == "北京"
    assert result.country_code == "CN"
    assert result.resolved_location.name == "Beijing"
    assert result.current.condition == "Mainly clear"
    assert result.metadata.provider == "Open-Meteo"
    assert result.metadata.model_based_current_conditions is True
    assert result.metadata.units.temperature_c == "°C"
    assert result.metadata.license_url == "https://creativecommons.org/licenses/by/4.0/"
    assert provider.fetch_calls == 1


@pytest.mark.asyncio
async def test_service_does_not_fetch_weather_after_location_not_found() -> None:
    provider = StubProvider(
        location=resolved_location(),
        current=current_conditions(),
        resolve_error=WeatherServiceError.from_code(WeatherErrorCode.LOCATION_NOT_FOUND),
    )
    service = WeatherService(provider)

    with pytest.raises(WeatherServiceError) as captured:
        await service.get_current_weather(LocationQuery(location="not-a-place"))

    assert captured.value.error.code is WeatherErrorCode.LOCATION_NOT_FOUND
    assert provider.fetch_calls == 0
