"""Executable specification for stable, caller-visible error semantics."""

from __future__ import annotations

from typing import Any

import pytest

from mcp_weather_query import errors

EXPECTED_RETRYABILITY = {
    "INVALID_LOCATION": False,
    "LOCATION_NOT_FOUND": False,
    "UPSTREAM_TIMEOUT": True,
    "UPSTREAM_RATE_LIMITED": True,
    "UPSTREAM_UNAVAILABLE": True,
    "UPSTREAM_INVALID_RESPONSE": False,
}


def require_error_contract() -> tuple[type[Any], dict[Any, bool]]:
    """Return the required error types with focused contract failures."""
    error_code = getattr(errors, "WeatherErrorCode", None)
    retryability = getattr(errors, "ERROR_RETRYABILITY", None)
    assert error_code is not None, "WeatherErrorCode contract is missing"
    assert retryability is not None, "ERROR_RETRYABILITY contract is missing"
    return error_code, retryability


@pytest.mark.contract
def test_stable_error_codes_and_retryability_are_complete() -> None:
    error_code, retryability = require_error_contract()

    actual_codes = {member.value for member in error_code}
    actual_retryability = {member.value: retryability[member] for member in error_code}

    assert actual_codes == set(EXPECTED_RETRYABILITY)
    assert actual_retryability == EXPECTED_RETRYABILITY


@pytest.mark.contract
def test_structured_error_has_safe_caller_fields() -> None:
    weather_error = getattr(errors, "WeatherError", None)
    assert weather_error is not None, "WeatherError contract is missing"

    schema = weather_error.model_json_schema()

    assert set(schema["properties"]) == {"code", "message", "retryable", "hint"}
