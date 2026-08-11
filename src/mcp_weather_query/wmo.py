"""WMO weather interpretation codes exposed by Open-Meteo."""

from __future__ import annotations

from typing import Final

from mcp_weather_query.errors import WeatherErrorCode, WeatherServiceError

WMO_CONDITIONS: Final[dict[int, str]] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Slight or moderate thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def condition_for_weather_code(code: int) -> str:
    """Translate a supported WMO code or reject unknown upstream data."""
    try:
        return WMO_CONDITIONS[code]
    except KeyError:
        raise WeatherServiceError.from_code(WeatherErrorCode.UPSTREAM_INVALID_RESPONSE) from None
