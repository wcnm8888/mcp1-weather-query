"""Official MCP Python SDK v2 server for the single F-001 weather Tool."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Annotated

import httpx
from mcp import MCPError
from mcp.server import MCPServer
from mcp.types import INTERNAL_ERROR, ToolAnnotations
from pydantic import Field, ValidationError

from mcp_weather_query.errors import (
    WeatherError,
    WeatherErrorCode,
    WeatherServiceError,
    create_weather_error,
)
from mcp_weather_query.models import CurrentWeatherResult, LocationQuery
from mcp_weather_query.providers.open_meteo import OpenMeteoProvider
from mcp_weather_query.service import WeatherService

SERVER_NAME = "mcp-weather-query"
SERVER_TITLE = "MCP1 Weather Query"
TOOL_NAME = "get_current_weather"
TOOL_TITLE = "Get current weather"
TOOL_DESCRIPTION = (
    "Resolve a city or postal-code-like location and return read-only, model-based current "
    "conditions. This Tool does not provide forecasts, alerts, advice, or arbitrary URL content. "
    "Always inspect resolved_location because place names can be ambiguous."
)

LocationArgument = Annotated[
    str,
    Field(
        description=(
            "City, place name, or postal-code-like text. Trimmed length must be 2-100 characters; "
            "the value is never interpreted as a URL."
        ),
        json_schema_extra={"minLength": 2, "maxLength": 100},
    ),
]
CountryCodeArgument = Annotated[
    str | None,
    Field(
        description=(
            "Optional ISO 3166-1 alpha-2 country code. Lower-case input is accepted and normalized "
            "to upper-case."
        ),
        json_schema_extra={"pattern": "^[A-Za-z]{2}$"},
    ),
]

WeatherQueryHandler = Callable[[LocationQuery], Awaitable[CurrentWeatherResult]]


class ToolExecutionError(RuntimeError):
    """Ordinary exception rendered by MCPServer as an ``is_error`` Tool result."""

    def __init__(self, error: WeatherError) -> None:
        self.error = error
        retryable = str(error.retryable).lower()
        super().__init__(
            f"code={error.code.value}; message={error.message}; "
            f"retryable={retryable}; hint={error.hint}"
        )


async def query_open_meteo(query: LocationQuery) -> CurrentWeatherResult:
    """Execute one read-only query with a short-lived async HTTP client."""
    async with httpx.AsyncClient(trust_env=False) as client:
        service = WeatherService(OpenMeteoProvider(client))
        return await service.get_current_weather(query)


def create_server(query_weather: WeatherQueryHandler = query_open_meteo) -> MCPServer:
    """Create an MCPServer with exactly one injectable, read-only weather Tool."""
    server = MCPServer(
        name=SERVER_NAME,
        title=SERVER_TITLE,
        description="A local MCP server exposing one read-only current weather query Tool.",
    )

    @server.tool(
        name=TOOL_NAME,
        title=TOOL_TITLE,
        description=TOOL_DESCRIPTION,
        annotations=ToolAnnotations(
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
    )
    async def get_current_weather(
        location: LocationArgument,
        country_code: CountryCodeArgument = None,
    ) -> CurrentWeatherResult:
        """Return validated model-based current conditions for a resolved location."""
        try:
            query = LocationQuery(location=location, country_code=country_code)
        except ValidationError:
            raise ToolExecutionError(
                create_weather_error(WeatherErrorCode.INVALID_LOCATION)
            ) from None

        try:
            return await query_weather(query)
        except WeatherServiceError as exc:
            raise ToolExecutionError(exc.error) from None
        except Exception:
            raise MCPError(code=INTERNAL_ERROR, message="Internal server error") from None

    return server


mcp = create_server()
