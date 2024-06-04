from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from peas_app.database.models.models import Product
from peas_app.database.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Product)

    def get_by_name(self, page_number: str, page_size, limit) -> list[Product]:
        page_size = (page_size - 1) * limit
        try:
            return list(
                self.session.scalars(
                    select(Product)
                    .order_by(Product.id)
                    .filter(Product.name.like(f"%{page_number}%"))
                    .offset(page_size)
                    .limit(limit)
                )
            )
        except SQLAlchemyError as e:
            self._rollback()
            raise e

    def get_total_rows_count_by_name(self, name: str) -> int:
        return (
            self.session.query(func.count(Product.id))
            .filter(Product.name.like(f"%{name}%"))
            .scalar()
        )
