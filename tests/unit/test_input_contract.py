"""Executable specification for the approved Tool input boundary."""

from __future__ import annotations

from typing import Any, cast

import pytest
from pydantic import ValidationError

from mcp_weather_query import models


def require_location_query() -> type[Any]:
    """Return the required input model with a focused contract failure."""
    model = cast(type[Any] | None, getattr(models, "LocationQuery", None))
    assert model is not None, "LocationQuery contract is missing"
    return model


@pytest.mark.contract
def test_location_and_country_code_are_normalized() -> None:
    location_query = require_location_query()

    query = location_query(location="  北京  ", country_code="cn")

    assert query.location == "北京"
    assert query.country_code == "CN"


@pytest.mark.contract
@pytest.mark.parametrize("location", ["", " ", "A", "北" * 101])
def test_invalid_location_is_rejected_before_io(location: str) -> None:
    location_query = require_location_query()

    with pytest.raises(ValidationError):
        location_query(location=location)


@pytest.mark.contract
@pytest.mark.parametrize("country_code", ["C", "CHN", "1N", "中国"])
def test_invalid_country_code_is_rejected(country_code: str) -> None:
    location_query = require_location_query()

    with pytest.raises(ValidationError):
        location_query(location="北京", country_code=country_code)
