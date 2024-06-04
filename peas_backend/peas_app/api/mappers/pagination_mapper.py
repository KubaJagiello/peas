import math
from typing import TypeVar

from peas_app.api.dtos.v1.pagination import Pagination

T = TypeVar("T")


class PaginationMapper:
    @staticmethod
    def _get_total_pages(page_size: int, total_items: int) -> int:
        return math.ceil(total_items / page_size) if total_items > 0 else 0

    @staticmethod
    def to_paginated_response(
        page_number: int,
        page_size: int,
        total_items: int,
        items: list[T],
    ) -> Pagination[T]:
        return Pagination(
            page=page_number,
            page_size=page_size,
            pages=PaginationMapper._get_total_pages(
                page_size=page_size, total_items=total_items
            ),
            total=total_items,
            items=items,
        )
