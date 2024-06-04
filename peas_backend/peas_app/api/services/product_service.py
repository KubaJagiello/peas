from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import ProductRequest
from peas_app.api.dtos.v1.responses.api_responses import ProductResponse
from peas_app.api.exceptions.exception_handler import NotFoundException
from peas_app.api.mappers.pagination_mapper import PaginationMapper
from peas_app.api.mappers.product_mapper import ProductMapper
from peas_app.database.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository: ProductRepository = product_repository

    def search_product_by_name(
        self, page_number: int, page_size: int, name: str
    ) -> Pagination[ProductResponse]:
        products = self.product_repository.get_by_name(
            name, page_number, page_size
        )
        total_count = self.product_repository.get_total_rows_count_by_name(name)

        product_responses = [
            ProductMapper.to_product_response(product) for product in products
        ]

        return PaginationMapper.to_paginated_response(
            page_number=page_number,
            page_size=page_size,
            total_items=total_count,
            items=product_responses,
        )

    def get_all_products(
        self, page_number: int, page_size: int
    ) -> Pagination[ProductResponse]:
        products = self.product_repository.get_all(
            page_number=page_number, page_size=page_size
        )
        total_number_of_products = (
            self.product_repository.get_total_rows_count()
        )

        product_responses = [
            ProductMapper.to_product_response(product) for product in products
        ]

        return PaginationMapper.to_paginated_response(
            page_number=page_number,
            page_size=page_size,
            total_items=total_number_of_products,
            items=product_responses,
        )

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(_id=product_id)
        if not product:
            raise NotFoundException("Did not find product")
        product_response = ProductMapper.to_product_response(product)
        return product_response

    def add_product(self, product_request: ProductRequest) -> ProductResponse:
        product = ProductMapper.to_product(product_request=product_request)
        product = self.product_repository.add(product)
        return ProductMapper.to_product_response(product)

    def update_product(
        self, product_id: int, product_request: ProductRequest
    ) -> ProductResponse:
        product = ProductMapper.to_product(product_request=product_request)
        product.id = product_id
        product = self.product_repository.update(product)
        return ProductMapper.to_product_response(product)

    def delete_product(self, product_id: int) -> None:
        product = self.product_repository.get_by_id(_id=product_id)
        if product:
            self.product_repository.delete(product)
