"""Executable specification for the structured weather output."""

from __future__ import annotations

from typing import Any, cast

import pytest

from mcp_weather_query import models

EXPECTED_RESULT_FIELDS = {
    "requested_location",
    "country_code",
    "resolved_location",
    "current",
    "metadata",
}


def require_result_model() -> type[Any]:
    """Return the required result model with a focused contract failure."""
    model = cast(type[Any] | None, getattr(models, "CurrentWeatherResult", None))
    assert model is not None, "CurrentWeatherResult contract is missing"
    return model


@pytest.mark.contract
def test_structured_weather_fixture_validates(
    current_weather_payload: dict[str, Any],
) -> None:
    result_model = require_result_model()

    result = result_model.model_validate(current_weather_payload)

    assert result.requested_location == "北京"
    assert result.country_code == "CN"
    assert result.resolved_location.timezone == "Asia/Shanghai"
    assert result.current.temperature_c == pytest.approx(31.2)
    assert result.metadata.model_based_current_conditions is True
    assert result.metadata.provider == "Open-Meteo"


@pytest.mark.contract
def test_output_schema_exposes_only_approved_top_level_groups() -> None:
    result_model = require_result_model()

    schema = result_model.model_json_schema()

    assert set(schema["properties"]) == EXPECTED_RESULT_FIELDS
    assert set(schema["required"]) == EXPECTED_RESULT_FIELDS
