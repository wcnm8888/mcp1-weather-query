"""Application service for the single F-001 weather use case."""

from __future__ import annotations

from typing import Protocol

from mcp_weather_query.models import (
    CurrentConditions,
    CurrentWeatherResult,
    LocationQuery,
    ResolvedLocation,
    WeatherMetadata,
    WeatherUnits,
)


class WeatherProvider(Protocol):
    """Provider behavior required by the application service."""

    async def resolve_location(self, query: LocationQuery) -> ResolvedLocation:
        """Return the provider's best matching location."""
        ...

    async def fetch_current(self, location: ResolvedLocation) -> CurrentConditions:
        """Return validated current conditions for a resolved location."""
        ...


class WeatherService:
    """Orchestrate location resolution and current-condition retrieval."""

    def __init__(self, provider: WeatherProvider) -> None:
        self._provider = provider

    async def get_current_weather(self, query: LocationQuery) -> CurrentWeatherResult:
        """Execute the only application use case without MCP transport concerns."""
        resolved_location = await self._provider.resolve_location(query)
        current = await self._provider.fetch_current(resolved_location)
        return CurrentWeatherResult(
            requested_location=query.location,
            country_code=query.country_code,
            resolved_location=resolved_location,
            current=current,
            metadata=WeatherMetadata(
                units=WeatherUnits(
                    temperature_c="°C",
                    apparent_temperature_c="°C",
                    relative_humidity_percent="%",
                    precipitation_mm="mm",
                    wind_speed_kmh="km/h",
                    wind_direction_degrees="°",
                ),
                provider="Open-Meteo",
                model_based_current_conditions=True,
                attribution="Weather data by Open-Meteo.com",
                license_url="https://creativecommons.org/licenses/by/4.0/",
            ),
        )
