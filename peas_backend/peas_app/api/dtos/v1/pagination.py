from typing import Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    page: int
    page_size: int
    pages: int
    total: int
    items: list[T]
