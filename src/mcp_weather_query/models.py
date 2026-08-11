"""Validated input and structured-output models for F-001."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

CountryCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{2}$")]


class ContractModel(BaseModel):
    """Base model that rejects undeclared fields at every trust boundary."""

    model_config = ConfigDict(extra="forbid")


class LocationQuery(ContractModel):
    """Normalized user input for a location-based current weather query."""

    location: str = Field(min_length=2, max_length=100)
    country_code: CountryCode | None = None

    @field_validator("location", mode="before")
    @classmethod
    def strip_location(cls, value: object) -> object:
        """Trim text before length constraints are evaluated."""
        return value.strip() if isinstance(value, str) else value

    @field_validator("country_code", mode="before")
    @classmethod
    def normalize_country_code(cls, value: object) -> object:
        """Accept lower-case ISO alpha-2 input and store its upper-case form."""
        return value.strip().upper() if isinstance(value, str) else value


class ResolvedLocation(ContractModel):
    """The actual best-ranked place selected by the geocoding provider."""

    name: str = Field(min_length=1)
    country: str = Field(min_length=1)
    country_code: CountryCode
    admin1: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1)


class CurrentConditions(ContractModel):
    """Current model-based conditions with explicit semantic field names."""

    time: str = Field(min_length=1)
    interval_seconds: int = Field(gt=0)
    is_day: bool
    temperature_c: float = Field(ge=-150, le=70)
    apparent_temperature_c: float = Field(ge=-200, le=100)
    relative_humidity_percent: int = Field(ge=0, le=100)
    precipitation_mm: float = Field(ge=0)
    weather_code: int = Field(ge=0, le=99)
    condition: str = Field(min_length=1)
    wind_speed_kmh: float = Field(ge=0)
    wind_direction_degrees: float = Field(ge=0, le=360)

    @field_validator("time")
    @classmethod
    def require_iso_8601_time(cls, value: str) -> str:
        """Reject upstream timestamps that are not valid ISO 8601 values."""
        try:
            datetime.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("time must be an ISO 8601 timestamp") from exc
        return value


class WeatherUnits(ContractModel):
    """Units fixed by the approved Open-Meteo request contract."""

    temperature_c: Literal["°C"]
    apparent_temperature_c: Literal["°C"]
    relative_humidity_percent: Literal["%"]
    precipitation_mm: Literal["mm"]
    wind_speed_kmh: Literal["km/h"]
    wind_direction_degrees: Literal["°"]


class WeatherMetadata(ContractModel):
    """Provider, model-origin and attribution metadata."""

    units: WeatherUnits
    provider: Literal["Open-Meteo"]
    model_based_current_conditions: Literal[True]
    attribution: Literal["Weather data by Open-Meteo.com"]
    license_url: Literal["https://creativecommons.org/licenses/by/4.0/"]


class CurrentWeatherResult(ContractModel):
    """Structured result exposed by the future MCP Tool."""

    requested_location: str = Field(min_length=2, max_length=100)
    country_code: CountryCode | None
    resolved_location: ResolvedLocation
    current: CurrentConditions
    metadata: WeatherMetadata
