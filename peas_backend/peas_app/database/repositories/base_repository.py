from typing import Callable, Generic, Optional, Type, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from peas_app.api.exceptions.exception_handler import DatabaseException
from peas_app.database.models.models import BaseEntity

T = TypeVar("T", bound=BaseEntity)
R = TypeVar("R")


# https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-20-query-usage
class BaseRepository(Generic[T]):
    def __init__(self, session: Session, entity_class: Type[T]) -> None:
        self.session = session
        self.entity_class = entity_class

    def get_by_id(self, _id: int) -> Optional[T]:
        return self._safe_execute(self.session.get, self.entity_class, _id)

    def get_by_ids(self, _ids: list[int]) -> list[T]:
        return self._safe_execute(
            self.session.query(self.entity_class)
            .filter(self.entity_class.id.in_(_ids))
            .all
        )

    def add(self, entity: T) -> T:
        return self._safe_execute(self._add_and_commit, entity)

    def update(self, entity: T) -> T:
        return self._safe_execute(self._update_and_commit, entity)

    def delete(self, entity: T) -> None:
        return self._safe_execute(self._delete_and_commit, entity)

    def get_all(self, page_number, page_size) -> list[T]:
        page_number = (page_number - 1) * page_size

        return (
            self.session.query(self.entity_class)
            .order_by(self.entity_class.id)
            .offset(page_number)
            .limit(page_size)
            .all()
        )

    def get_total_rows_count(self) -> int:
        return self.session.query(func.count(self.entity_class.id)).scalar()

    def _add_and_commit(self, entity: T) -> T:
        self.session.add(entity)
        self._commit()
        return entity

    def _update_and_commit(self, entity: T) -> T:
        self.session.merge(entity)
        self._commit()
        return entity

    def _delete_and_commit(self, entity: T) -> None:
        self.session.delete(entity)
        self._commit()

    def _rollback(self) -> None:
        self.session.rollback()

    def _commit(self) -> None:
        self.session.commit()

    def _safe_execute(self, f: Callable[..., R], *args, **kwargs) -> R:
        try:
            return f(*args, **kwargs)
        except SQLAlchemyError as e:
            self._rollback()
            raise DatabaseException(
                details={"entity": self.entity_class.__name__, "error": str(e)}
            ) from e
