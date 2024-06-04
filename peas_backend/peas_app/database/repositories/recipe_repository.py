from pydantic.v1 import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from peas_app.api.exceptions.exception_handler import DatabaseException
from peas_app.database.models.models import Recipe
from peas_app.database.repositories.base_repository import BaseRepository


class RecipeRepository(BaseRepository[Recipe]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Recipe)

    def get_by_name(self, name, page_number, page_size) -> list[Recipe]:
        page_number = (page_number - 1) * page_size
        try:
            return list(
                self.session.scalars(
                    select(Recipe)
                    .order_by(Recipe.id)
                    .filter(Recipe.name.like(f"%{name}%"))
                    .offset(page_number)
                    .limit(page_size)
                )
            )
        except SQLAlchemyError as e:
            self._rollback()
            raise DatabaseException(
                details={"entity": self.entity_class.__name__, "error": str(e)}
            )

    def get_total_rows_count_by_name(self, name: str) -> int:
        return (
            self.session.query(func.count(Recipe.id))
            .filter(Recipe.name.like(f"%{name}%"))
            .scalar()
        )

    def remove_product(self, recipe: Recipe, product_id: int) -> None:
        association_to_remove = next(
            (
                assoc
                for assoc in recipe.product_associations
                if assoc.product_id == product_id
            ),
            None,
        )
        if association_to_remove:
            self.delete(association_to_remove)
            self._commit()
