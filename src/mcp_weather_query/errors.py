"""Stable, sanitized error semantics shared by the domain and adapter layers."""

from __future__ import annotations

from enum import StrEnum
from typing import Final

from pydantic import BaseModel, ConfigDict, Field, model_validator


class WeatherErrorCode(StrEnum):
    """Caller-visible error codes approved by the F-001 task card."""

    INVALID_LOCATION = "INVALID_LOCATION"
    LOCATION_NOT_FOUND = "LOCATION_NOT_FOUND"
    UPSTREAM_TIMEOUT = "UPSTREAM_TIMEOUT"
    UPSTREAM_RATE_LIMITED = "UPSTREAM_RATE_LIMITED"
    UPSTREAM_UNAVAILABLE = "UPSTREAM_UNAVAILABLE"
    UPSTREAM_INVALID_RESPONSE = "UPSTREAM_INVALID_RESPONSE"


ERROR_RETRYABILITY: Final[dict[WeatherErrorCode, bool]] = {
    WeatherErrorCode.INVALID_LOCATION: False,
    WeatherErrorCode.LOCATION_NOT_FOUND: False,
    WeatherErrorCode.UPSTREAM_TIMEOUT: True,
    WeatherErrorCode.UPSTREAM_RATE_LIMITED: True,
    WeatherErrorCode.UPSTREAM_UNAVAILABLE: True,
    WeatherErrorCode.UPSTREAM_INVALID_RESPONSE: False,
}

ERROR_MESSAGES: Final[dict[WeatherErrorCode, str]] = {
    WeatherErrorCode.INVALID_LOCATION: "The location input is invalid.",
    WeatherErrorCode.LOCATION_NOT_FOUND: "No matching location was found.",
    WeatherErrorCode.UPSTREAM_TIMEOUT: "The weather provider timed out.",
    WeatherErrorCode.UPSTREAM_RATE_LIMITED: "The weather provider rate limit was reached.",
    WeatherErrorCode.UPSTREAM_UNAVAILABLE: "The weather provider is temporarily unavailable.",
    WeatherErrorCode.UPSTREAM_INVALID_RESPONSE: "The weather provider returned invalid data.",
}

ERROR_HINTS: Final[dict[WeatherErrorCode, str]] = {
    WeatherErrorCode.INVALID_LOCATION: (
        "Use a 2-100 character location and an optional two-letter country code."
    ),
    WeatherErrorCode.LOCATION_NOT_FOUND: (
        "Use a more specific place name or add a two-letter country code."
    ),
    WeatherErrorCode.UPSTREAM_TIMEOUT: "Wait briefly, then retry a limited number of times.",
    WeatherErrorCode.UPSTREAM_RATE_LIMITED: "Back off before retrying.",
    WeatherErrorCode.UPSTREAM_UNAVAILABLE: "Try again later.",
    WeatherErrorCode.UPSTREAM_INVALID_RESPONSE: "Report the provider issue without retrying.",
}


class WeatherError(BaseModel):
    """Safe error payload intended for a future MCP Tool execution error."""

    model_config = ConfigDict(extra="forbid")

    code: WeatherErrorCode
    message: str = Field(min_length=1, max_length=200)
    retryable: bool
    hint: str = Field(min_length=1, max_length=300)

    @model_validator(mode="after")
    def retryability_matches_code(self) -> WeatherError:
        """Prevent contradictory retry advice from crossing the Tool boundary."""
        if self.retryable is not ERROR_RETRYABILITY[self.code]:
            raise ValueError("retryable must match the stable error code")
        return self


def create_weather_error(code: WeatherErrorCode) -> WeatherError:
    """Create the canonical, sanitized payload for a stable error code."""
    return WeatherError(
        code=code,
        message=ERROR_MESSAGES[code],
        retryable=ERROR_RETRYABILITY[code],
        hint=ERROR_HINTS[code],
    )


class WeatherServiceError(RuntimeError):
    """Internal control-flow exception carrying only a sanitized error payload."""

    def __init__(self, error: WeatherError) -> None:
        self.error = error
        super().__init__(f"{error.code.value}: {error.message}")

    @classmethod
    def from_code(cls, code: WeatherErrorCode) -> WeatherServiceError:
        """Build an exception without embedding upstream bodies or local details."""
        return cls(create_weather_error(code))
