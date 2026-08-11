"""In-memory protocol tests for the single F-001 MCP Tool."""

from __future__ import annotations

from typing import Any, cast

import httpx
import pytest
from mcp import Client, MCPError
from mcp.types import TextContent

from mcp_weather_query.errors import WeatherErrorCode, WeatherServiceError
from mcp_weather_query.models import CurrentWeatherResult, LocationQuery
from mcp_weather_query.server import TOOL_NAME, create_server, query_open_meteo


def result_from_payload(payload: dict[str, Any]) -> CurrentWeatherResult:
    return CurrentWeatherResult.model_validate(payload)


@pytest.mark.asyncio
async def test_discovery_exposes_exactly_one_approved_tool() -> None:
    async def unused_handler(query: LocationQuery) -> CurrentWeatherResult:
        raise AssertionError("discovery must not execute the Tool")

    server = create_server(unused_handler)
    async with Client(server, raise_exceptions=True) as client:
        listed = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

    assert len(listed.tools) == 1
    assert resources.resources == []
    assert prompts.prompts == []
    tool = listed.tools[0]
    assert tool.name == TOOL_NAME
    assert tool.title == "Get current weather"
    assert tool.description is not None
    assert "postal-code-like" in tool.description
    assert "model-based current conditions" in tool.description
    assert "read-only" in tool.description
    assert "forecasts, alerts, advice, or arbitrary URL" in tool.description
    assert "resolved_location" in tool.description
    assert tool.annotations is not None
    assert tool.annotations.read_only_hint is True
    assert tool.annotations.destructive_hint is False
    assert tool.annotations.idempotent_hint is True
    assert tool.annotations.open_world_hint is True


@pytest.mark.asyncio
async def test_discovery_exposes_approved_input_and_output_schema() -> None:
    async def unused_handler(query: LocationQuery) -> CurrentWeatherResult:
        raise AssertionError("discovery must not execute the Tool")

    server = create_server(unused_handler)
    async with Client(server, raise_exceptions=True) as client:
        listed = await client.list_tools()

    tool = listed.tools[0]
    input_properties = tool.input_schema["properties"]
    assert set(input_properties) == {"location", "country_code"}
    assert tool.input_schema["required"] == ["location"]
    assert input_properties["location"]["type"] == "string"
    assert input_properties["location"]["minLength"] == 2
    assert input_properties["location"]["maxLength"] == 100
    assert input_properties["country_code"]["pattern"] == "^[A-Za-z]{2}$"

    assert tool.output_schema is not None
    assert tool.output_schema["type"] == "object"
    assert set(tool.output_schema["properties"]) == {
        "requested_location",
        "country_code",
        "resolved_location",
        "current",
        "metadata",
    }
    assert set(tool.output_schema["required"]) == {
        "requested_location",
        "country_code",
        "resolved_location",
        "current",
        "metadata",
    }


@pytest.mark.asyncio
async def test_success_returns_structured_content_without_result_wrapper(
    current_weather_payload: dict[str, Any],
) -> None:
    expected = result_from_payload(current_weather_payload)
    received_queries: list[LocationQuery] = []

    async def success_handler(query: LocationQuery) -> CurrentWeatherResult:
        received_queries.append(query)
        return expected

    server = create_server(success_handler)
    async with Client(server, raise_exceptions=True) as client:
        result = await client.call_tool(
            TOOL_NAME,
            {"location": "  北京  ", "country_code": "cn"},
        )

    assert not result.is_error
    assert result.structured_content == expected.model_dump(mode="json")
    assert "result" not in result.structured_content
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)
    assert received_queries == [LocationQuery(location="北京", country_code="CN")]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arguments",
    [
        {"location": "A"},
        {"location": "北京", "country_code": "CHN"},
    ],
)
async def test_invalid_input_returns_stable_tool_execution_error(
    arguments: dict[str, Any],
) -> None:
    calls = 0

    async def must_not_run(query: LocationQuery) -> CurrentWeatherResult:
        nonlocal calls
        calls += 1
        raise AssertionError("invalid input must not reach the weather service")

    server = create_server(must_not_run)
    async with Client(server, raise_exceptions=True) as client:
        result = await client.call_tool(TOOL_NAME, arguments)

    assert result.is_error is True
    assert result.structured_content is None
    assert calls == 0
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)
    text = result.content[0].text
    assert "code=INVALID_LOCATION" in text
    assert "retryable=false" in text
    assert "hint=" in text


@pytest.mark.asyncio
async def test_service_error_returns_sanitized_tool_execution_error() -> None:
    async def missing_handler(query: LocationQuery) -> CurrentWeatherResult:
        raise WeatherServiceError.from_code(WeatherErrorCode.LOCATION_NOT_FOUND)

    server = create_server(missing_handler)
    async with Client(server, raise_exceptions=True) as client:
        result = await client.call_tool(TOOL_NAME, {"location": "not-a-place"})

    assert result.is_error is True
    assert result.structured_content is None
    assert len(result.content) == 1
    assert isinstance(result.content[0], TextContent)
    text = result.content[0].text
    assert "code=LOCATION_NOT_FOUND" in text
    assert "retryable=false" in text
    assert "more specific place name" in text
    assert "Traceback" not in text
    assert "E:\\" not in text


@pytest.mark.asyncio
async def test_unexpected_exception_becomes_generic_protocol_error() -> None:
    async def broken_handler(query: LocationQuery) -> CurrentWeatherResult:
        raise RuntimeError("private failure at E:\\private\\weather.json")

    server = create_server(broken_handler)
    async with Client(server, raise_exceptions=True) as client:
        with pytest.raises(MCPError) as captured:
            await client.call_tool(TOOL_NAME, {"location": "Beijing"})

    assert "Internal server error" in str(captured.value)
    assert "private" not in str(captured.value)


@pytest.mark.asyncio
async def test_default_query_does_not_inherit_environment_proxies(
    monkeypatch: pytest.MonkeyPatch,
    current_weather_payload: dict[str, Any],
) -> None:
    """Keep production weather traffic on the two fixed direct endpoints."""
    expected = result_from_payload(current_weather_payload)
    client_kwargs: dict[str, object] = {}

    class FakeAsyncClient:
        def __init__(self, **kwargs: object) -> None:
            client_kwargs.update(kwargs)

        async def __aenter__(self) -> httpx.AsyncClient:
            return cast(httpx.AsyncClient, self)

        async def __aexit__(
            self,
            exc_type: object,
            exc_value: object,
            traceback: object,
        ) -> None:
            return None

    async def return_expected(
        service: object,
        query: LocationQuery,
    ) -> CurrentWeatherResult:
        return expected

    monkeypatch.setattr("mcp_weather_query.server.httpx.AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(
        "mcp_weather_query.server.WeatherService.get_current_weather", return_expected
    )

    actual = await query_open_meteo(LocationQuery(location="Beijing", country_code="CN"))

    assert actual == expected
    assert client_kwargs == {"trust_env": False}
