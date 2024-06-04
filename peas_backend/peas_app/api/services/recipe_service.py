import logging

from sqlalchemy.exc import IntegrityError

from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import RecipeRequest
from peas_app.api.dtos.v1.responses.api_responses import RecipeResponse
from peas_app.api.exceptions.exception_handler import (
    NotFoundException,
    UnableToSaveException,
)
from peas_app.api.mappers.pagination_mapper import PaginationMapper
from peas_app.api.mappers.recipe_mapper import RecipeMapper
from peas_app.database.repositories.product_repository import ProductRepository
from peas_app.database.repositories.recipe_repository import RecipeRepository

logger = logging.getLogger(__name__)


class RecipeService:
    def __init__(
        self,
        recipe_repository: RecipeRepository,
        product_repository: ProductRepository,
    ):
        self.recipe_repository: RecipeRepository = recipe_repository
        self.product_repository: ProductRepository = product_repository

    def search_product_by_name(
        self, page_number: int, page_size: int, name: str
    ) -> Pagination[RecipeResponse]:
        recipes = self.recipe_repository.get_by_name(
            name, page_number, page_size
        )
        total_count = self.recipe_repository.get_total_rows_count_by_name(name)

        recipe_responses = [
            RecipeMapper.to_recipe_response_with_products(recipe)
            for recipe in recipes
        ]

        return PaginationMapper.to_paginated_response(
            page_number=page_number,
            page_size=page_size,
            total_items=total_count,
            items=recipe_responses,
        )

    def get_all_recipes(
        self, page_number: int, page_size: int
    ) -> Pagination[RecipeResponse]:
        recipes = self.recipe_repository.get_all(
            page_number=page_number, page_size=page_size
        )
        total_number_of_recipes = self.recipe_repository.get_total_rows_count()

        recipe_responses = [
            RecipeMapper.to_recipe_response_with_products(recipe)
            for recipe in recipes
        ]

        return PaginationMapper.to_paginated_response(
            page_number=page_number,
            page_size=page_size,
            total_items=total_number_of_recipes,
            items=recipe_responses,
        )

    def get_recipe_by_id(self, recipe_id: int) -> RecipeResponse:
        recipe = self.recipe_repository.get_by_id(recipe_id)
        if not recipe:
            raise NotFoundException("Did not find recipe")
        return RecipeMapper.to_recipe_response_with_products(recipe)

    def add_recipe(self, recipe_request: RecipeRequest) -> RecipeResponse:
        product_ids = [product.id for product in recipe_request.products]
        products = self.product_repository.get_by_ids(product_ids)

        if len(products) != len(product_ids):
            raise NotFoundException("Some products were not found")

        recipe = RecipeMapper.to_recipe(recipe_request)
        recipe = self.recipe_repository.add(recipe)
        return RecipeMapper.to_recipe_response_with_products(recipe)

    def update_recipe(
        self, recipe_id: int, recipe_request: RecipeRequest
    ) -> RecipeResponse:
        recipe = self.recipe_repository.get_by_id(recipe_id)

        if not recipe:
            raise NotFoundException("Did not find recipe")

        product_ids = [product.id for product in recipe_request.products]
        recipe_request_products = self.product_repository.get_by_ids(
            product_ids
        )
        updated_recipe = RecipeMapper.update_recipe(
            recipe, recipe_request, recipe_request_products
        )
        self.recipe_repository.update(updated_recipe)
        return RecipeMapper.to_recipe_response_with_products(updated_recipe)

    def delete_recipe(self, recipe_id: int) -> None:
        recipe = self.recipe_repository.get_by_id(recipe_id)
        if recipe:
            self.recipe_repository.delete(recipe)
