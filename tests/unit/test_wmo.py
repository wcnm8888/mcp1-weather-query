"""Unit tests for the official WMO interpretation mapping."""

from __future__ import annotations

import pytest

from mcp_weather_query.errors import WeatherErrorCode, WeatherServiceError
from mcp_weather_query.wmo import WMO_CONDITIONS, condition_for_weather_code


@pytest.mark.parametrize(
    ("code", "condition"),
    [
        (0, "Clear sky"),
        (1, "Mainly clear"),
        (48, "Depositing rime fog"),
        (65, "Heavy rain"),
        (77, "Snow grains"),
        (82, "Violent rain showers"),
        (99, "Thunderstorm with heavy hail"),
    ],
)
def test_known_wmo_code_has_stable_condition(code: int, condition: str) -> None:
    assert condition_for_weather_code(code) == condition


def test_all_documented_wmo_codes_are_mapped() -> None:
    assert set(WMO_CONDITIONS) == {
        0,
        1,
        2,
        3,
        45,
        48,
        51,
        53,
        55,
        56,
        57,
        61,
        63,
        65,
        66,
        67,
        71,
        73,
        75,
        77,
        80,
        81,
        82,
        85,
        86,
        95,
        96,
        99,
    }


def test_unknown_wmo_code_is_invalid_upstream_data() -> None:
    with pytest.raises(WeatherServiceError) as captured:
        condition_for_weather_code(4)

    assert captured.value.error.code is WeatherErrorCode.UPSTREAM_INVALID_RESPONSE
    assert captured.value.error.retryable is False
