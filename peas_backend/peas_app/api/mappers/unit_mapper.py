from peas_app.api.dtos.v1.unit import Unit
from peas_app.database.models.models import Unit as SqlUnit


class UnitMapper:
    @staticmethod
    def to_sql_unit(unit: Unit) -> SqlUnit:
        match unit:
            case Unit.gram:
                return SqlUnit.GRAM
            case Unit.milliliter:
                return SqlUnit.MILLILITER
            case _:
                raise ValueError(f"Unknown unit: {unit}")

    @staticmethod
    def to_unit(sql_unit: SqlUnit) -> Unit:
        match sql_unit:
            case SqlUnit.GRAM:
                return Unit.gram
            case SqlUnit.MILLILITER:
                return Unit.milliliter
            case _:
                raise ValueError(f"Unknown unit: {sql_unit}")
