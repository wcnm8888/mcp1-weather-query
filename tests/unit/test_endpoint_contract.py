"""Executable specification for Open-Meteo's fixed HTTPS endpoints."""

from __future__ import annotations

from urllib.parse import urlparse

import pytest

from mcp_weather_query.providers import open_meteo

EXPECTED_ENDPOINTS = {
    "GEOCODING_ENDPOINT": "https://geocoding-api.open-meteo.com/v1/search",
    "FORECAST_ENDPOINT": "https://api.open-meteo.com/v1/forecast",
}


@pytest.mark.contract
@pytest.mark.parametrize(("name", "expected_url"), EXPECTED_ENDPOINTS.items())
def test_provider_endpoint_is_fixed_https(name: str, expected_url: str) -> None:
    endpoint = getattr(open_meteo, name, None)
    assert endpoint is not None, f"{name} contract is missing"

    parsed = urlparse(endpoint)

    assert endpoint == expected_url
    assert parsed.scheme == "https"
    assert parsed.hostname in {"geocoding-api.open-meteo.com", "api.open-meteo.com"}
    assert parsed.username is None
    assert parsed.password is None
    assert parsed.query == ""
