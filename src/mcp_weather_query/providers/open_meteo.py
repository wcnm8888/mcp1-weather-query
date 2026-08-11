"""Fixed-endpoint, read-only Open-Meteo HTTP adapter."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final, Literal, cast

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from mcp_weather_query.errors import WeatherErrorCode, WeatherServiceError
from mcp_weather_query.models import (
    CountryCode,
    CurrentConditions,
    LocationQuery,
    ResolvedLocation,
)
from mcp_weather_query.wmo import condition_for_weather_code

GEOCODING_ENDPOINT: Final = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_ENDPOINT: Final = "https://api.open-meteo.com/v1/forecast"

CURRENT_VARIABLES: Final = ",".join(
    (
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "is_day",
        "precipitation",
        "weather_code",
        "wind_speed_10m",
        "wind_direction_10m",
    )
)
REQUEST_TIMEOUT: Final = httpx.Timeout(10.0, connect=5.0, pool=5.0)
REQUEST_HEADERS: Final = {"Accept": "application/json"}


class _UpstreamModel(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)


class _GeocodingCandidate(_UpstreamModel):
    name: str = Field(min_length=1)
    country: str = Field(min_length=1)
    country_code: CountryCode
    admin1: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1)


class _GeocodingResponse(_UpstreamModel):
    results: list[_GeocodingCandidate] = Field(default_factory=list)


class _CurrentUnits(_UpstreamModel):
    temperature_2m: Literal["°C"]
    relative_humidity_2m: Literal["%"]
    apparent_temperature: Literal["°C"]
    precipitation: Literal["mm"]
    wind_speed_10m: Literal["km/h"]
    wind_direction_10m: Literal["°"]


class _CurrentPayload(_UpstreamModel):
    time: str = Field(min_length=1)
    interval: int = Field(gt=0)
    temperature_2m: float = Field(ge=-150, le=70)
    relative_humidity_2m: int = Field(ge=0, le=100)
    apparent_temperature: float = Field(ge=-200, le=100)
    is_day: Literal[0, 1]
    precipitation: float = Field(ge=0)
    weather_code: int = Field(ge=0, le=99)
    wind_speed_10m: float = Field(ge=0)
    wind_direction_10m: float = Field(ge=0, le=360)


class _ForecastResponse(_UpstreamModel):
    timezone: str = Field(min_length=1)
    current_units: _CurrentUnits
    current: _CurrentPayload


class OpenMeteoProvider:
    """Convert fixed Open-Meteo JSON responses into trusted domain models."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def resolve_location(self, query: LocationQuery) -> ResolvedLocation:
        """Resolve the first ranked geocoding result for normalized input."""
        params: dict[str, str | int] = {
            "name": query.location,
            "count": 1,
            "format": "json",
        }
        if query.country_code is not None:
            params["countryCode"] = query.country_code

        payload = await self._get_json(GEOCODING_ENDPOINT, params)
        try:
            response = _GeocodingResponse.model_validate(payload)
        except ValidationError:
            raise WeatherServiceError.from_code(
                WeatherErrorCode.UPSTREAM_INVALID_RESPONSE
            ) from None

        if not response.results:
            raise WeatherServiceError.from_code(WeatherErrorCode.LOCATION_NOT_FOUND)

        candidate = response.results[0]
        return ResolvedLocation(
            name=candidate.name,
            country=candidate.country,
            country_code=candidate.country_code,
            admin1=candidate.admin1 or None,
            latitude=candidate.latitude,
            longitude=candidate.longitude,
            timezone=candidate.timezone,
        )

    async def fetch_current(self, location: ResolvedLocation) -> CurrentConditions:
        """Fetch and validate model-based current conditions for a resolved place."""
        params: dict[str, str | float] = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": CURRENT_VARIABLES,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
            "timezone": location.timezone,
        }
        payload = await self._get_json(FORECAST_ENDPOINT, params)
        try:
            response = _ForecastResponse.model_validate(payload)
            if response.timezone != location.timezone:
                raise ValueError("provider timezone did not match the request")
            current = response.current
            return CurrentConditions(
                time=current.time,
                interval_seconds=current.interval,
                is_day=bool(current.is_day),
                temperature_c=current.temperature_2m,
                apparent_temperature_c=current.apparent_temperature,
                relative_humidity_percent=current.relative_humidity_2m,
                precipitation_mm=current.precipitation,
                weather_code=current.weather_code,
                condition=condition_for_weather_code(current.weather_code),
                wind_speed_kmh=current.wind_speed_10m,
                wind_direction_degrees=current.wind_direction_10m,
            )
        except (ValidationError, ValueError):
            raise WeatherServiceError.from_code(
                WeatherErrorCode.UPSTREAM_INVALID_RESPONSE
            ) from None

    async def _get_json(
        self,
        endpoint: str,
        params: Mapping[str, str | int | float],
    ) -> dict[str, Any]:
        """Read JSON from an approved endpoint and map transport failures safely."""
        try:
            response = await self._client.get(
                endpoint,
                params=params,
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT,
                follow_redirects=False,
            )
        except httpx.TimeoutException:
            raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_TIMEOUT) from None
        except httpx.RequestError:
            raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_UNAVAILABLE) from None

        if response.status_code == 429:
            raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_RATE_LIMITED)
        if response.status_code >= 500:
            raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_UNAVAILABLE)
        if response.status_code < 200 or response.status_code >= 300:
            raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_INVALID_RESPONSE)

        try:
            payload = response.json()
        except ValueError:
            raise WeatherServiceError.from_code(
                WeatherErrorCode.UPSTREAM_INVALID_RESPONSE
            ) from None
        if not isinstance(payload, dict):
            raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_INVALID_RESPONSE)
        return cast(dict[str, Any], payload)
