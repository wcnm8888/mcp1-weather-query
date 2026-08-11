"""Offline HTTP adapter tests using httpx.MockTransport."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx
import pytest

from mcp_weather_query.errors import WeatherErrorCode, WeatherServiceError
from mcp_weather_query.models import LocationQuery, ResolvedLocation
from mcp_weather_query.providers.open_meteo import (
    CURRENT_VARIABLES,
    FORECAST_ENDPOINT,
    GEOCODING_ENDPOINT,
    OpenMeteoProvider,
)


def resolved_beijing() -> ResolvedLocation:
    return ResolvedLocation(
        name="Beijing",
        country="China",
        country_code="CN",
        admin1="Beijing",
        latitude=39.9075,
        longitude=116.3972,
        timezone="Asia/Shanghai",
    )


@pytest.mark.asyncio
async def test_success_uses_only_fixed_hosts_and_query_parameters(
    geocoding_payload: dict[str, Any],
    forecast_payload: dict[str, Any],
) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.host == "geocoding-api.open-meteo.com":
            return httpx.Response(200, json=geocoding_payload)
        if request.url.host == "api.open-meteo.com":
            return httpx.Response(200, json=forecast_payload)
        raise AssertionError(f"unexpected host: {request.url.host}")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        query = LocationQuery(location="https://evil.example/a?x=1", country_code="cn")
        location = await provider.resolve_location(query)
        current = await provider.fetch_current(location)

    assert len(requests) == 2
    geocoding_request, forecast_request = requests
    assert str(geocoding_request.url.copy_with(query=None)) == GEOCODING_ENDPOINT
    assert geocoding_request.url.params["name"] == "https://evil.example/a?x=1"
    assert geocoding_request.url.params["countryCode"] == "CN"
    assert geocoding_request.url.params["count"] == "1"
    assert str(forecast_request.url.copy_with(query=None)) == FORECAST_ENDPOINT
    assert forecast_request.url.params["current"] == CURRENT_VARIABLES
    assert forecast_request.url.params["timezone"] == "Asia/Shanghai"
    assert forecast_request.url.params["temperature_unit"] == "celsius"
    assert forecast_request.url.params["wind_speed_unit"] == "kmh"
    assert forecast_request.url.params["precipitation_unit"] == "mm"
    assert {request.url.scheme for request in requests} == {"https"}
    assert location.country_code == "CN"
    assert current.condition == "Mainly clear"
    assert current.is_day is True


@pytest.mark.asyncio
async def test_no_geocoding_result_maps_to_location_not_found() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json={})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        with pytest.raises(WeatherServiceError) as captured:
            await provider.resolve_location(LocationQuery(location="not-a-place"))

    assert calls == 1
    assert captured.value.error.code is WeatherErrorCode.LOCATION_NOT_FOUND
    assert captured.value.error.retryable is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "expected_code"),
    [
        (400, WeatherErrorCode.UPSTREAM_INVALID_RESPONSE),
        (429, WeatherErrorCode.UPSTREAM_RATE_LIMITED),
        (503, WeatherErrorCode.UPSTREAM_UNAVAILABLE),
    ],
)
async def test_http_status_maps_to_stable_error(
    status_code: int,
    expected_code: WeatherErrorCode,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json={"secret-upstream-body": "not exposed"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        with pytest.raises(WeatherServiceError) as captured:
            await provider.resolve_location(LocationQuery(location="Beijing"))

    assert captured.value.error.code is expected_code
    assert "secret-upstream-body" not in str(captured.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception_factory", "expected_code"),
    [
        (
            lambda request: httpx.ReadTimeout("private timeout detail", request=request),
            WeatherErrorCode.UPSTREAM_TIMEOUT,
        ),
        (
            lambda request: httpx.ConnectError("private network detail", request=request),
            WeatherErrorCode.UPSTREAM_UNAVAILABLE,
        ),
    ],
)
async def test_transport_failure_maps_to_stable_error(
    exception_factory: Callable[[httpx.Request], httpx.RequestError],
    expected_code: WeatherErrorCode,
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise exception_factory(request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        with pytest.raises(WeatherServiceError) as captured:
            await provider.resolve_location(LocationQuery(location="Beijing"))

    assert captured.value.error.code is expected_code
    assert "private" not in str(captured.value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_factory",
    [
        lambda: httpx.Response(200, text="not-json"),
        lambda: httpx.Response(200, json={"results": [{"name": "Incomplete"}]}),
        lambda: httpx.Response(200, json=[]),
    ],
)
async def test_invalid_geocoding_payload_is_rejected(
    response_factory: Callable[[], httpx.Response],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return response_factory()

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        with pytest.raises(WeatherServiceError) as captured:
            await provider.resolve_location(LocationQuery(location="Beijing"))

    assert captured.value.error.code is WeatherErrorCode.UPSTREAM_INVALID_RESPONSE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mutation", ["missing_current", "wrong_units", "wrong_timezone", "unknown_wmo"]
)
async def test_invalid_forecast_payload_is_rejected(
    forecast_payload: dict[str, Any],
    mutation: str,
) -> None:
    if mutation == "missing_current":
        forecast_payload.pop("current")
    elif mutation == "wrong_units":
        forecast_payload["current_units"]["temperature_2m"] = "°F"
    elif mutation == "wrong_timezone":
        forecast_payload["timezone"] = "UTC"
    else:
        forecast_payload["current"]["weather_code"] = 4

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=forecast_payload)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        with pytest.raises(WeatherServiceError) as captured:
            await provider.fetch_current(resolved_beijing())

    assert captured.value.error.code is WeatherErrorCode.UPSTREAM_INVALID_RESPONSE


@pytest.mark.asyncio
async def test_forecast_timeout_uses_same_sanitized_mapping() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("private forecast timeout", request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = OpenMeteoProvider(client)
        with pytest.raises(WeatherServiceError) as captured:
            await provider.fetch_current(resolved_beijing())

    assert captured.value.error.code is WeatherErrorCode.UPSTREAM_TIMEOUT
    assert "private" not in str(captured.value)
