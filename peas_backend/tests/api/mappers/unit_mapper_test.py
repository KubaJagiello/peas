import pytest

from peas_app.api.dtos.v1.unit import Unit
from peas_app.api.mappers.unit_mapper import UnitMapper
from peas_app.database.models.models import Unit as SqlUnit


@pytest.mark.parametrize(
    "unit, expected_sql_unit",
    [
        (Unit.gram, SqlUnit.GRAM),
        (Unit.milliliter, SqlUnit.MILLILITER),
    ],
)
def test_to_sql_unit_valid(unit: Unit, expected_sql_unit: SqlUnit) -> None:
    assert UnitMapper.to_sql_unit(unit) == expected_sql_unit


@pytest.mark.parametrize("unit", ["unknown_unit", 123, None])
def test_to_sql_unit_invalid(unit: Unit) -> None:
    with pytest.raises(ValueError, match=f"Unknown unit: {unit}"):
        UnitMapper.to_sql_unit(unit)


@pytest.mark.parametrize(
    "sql_unit, expected_unit",
    [
        (SqlUnit.GRAM, Unit.gram),
        (SqlUnit.MILLILITER, Unit.milliliter),
    ],
)
def test_to_unit_valid(sql_unit, expected_unit):
    assert UnitMapper.to_unit(sql_unit) == expected_unit


@pytest.mark.parametrize("sql_unit", ["UNKNOWN_SQL_UNIT", 456, None])
def test_to_unit_invalid(sql_unit: SqlUnit) -> None:
    with pytest.raises(ValueError, match=f"Unknown unit: {sql_unit}"):
        UnitMapper.to_unit(sql_unit)
