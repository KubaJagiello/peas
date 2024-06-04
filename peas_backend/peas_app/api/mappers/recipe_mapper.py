from typing import List

from peas_app.api.dtos.v1.requests.api_requests import RecipeRequest
from peas_app.api.dtos.v1.responses.api_responses import (
    RecipeProductResponse,
    RecipeResponse,
)
from peas_app.api.mappers.product_mapper import ProductMapper
from peas_app.api.mappers.unit_mapper import UnitMapper
from peas_app.database.models.models import (
    Product,
    ProductRecipeAssociation,
    Recipe,
)


class RecipeMapper:
    @staticmethod
    def update_recipe(
        recipe_to_update: Recipe,
        recipe_request: RecipeRequest,
        products: List[Product],
    ) -> Recipe:
        recipe_to_update.name = recipe_request.name
        recipe_to_update.description = recipe_request.description
        recipe_to_update.servings = recipe_request.servings
        recipe_to_update.products = products
        return recipe_to_update

    @staticmethod
    def to_recipe_with_id(
        recipe_request: RecipeRequest, products: List[Product], recipe_id: int
    ) -> Recipe:
        return Recipe(
            id=recipe_id,
            name=recipe_request.name,
            description=recipe_request.description,
            servings=recipe_request.servings,
            products=products,
        )

    @staticmethod
    def to_recipe(recipe_request: RecipeRequest) -> Recipe:
        return Recipe(
            name=recipe_request.name,
            description=recipe_request.description,
            servings=recipe_request.servings,
            product_associations=RecipeMapper.to_product_associations(
                recipe_request
            ),
        )

    @staticmethod
    def to_product_associations(
        recipe_request: RecipeRequest,
    ) -> List[ProductRecipeAssociation]:
        return [
            ProductRecipeAssociation(
                product_id=product.id,
                quantity=product.quantity,
                unit=UnitMapper.to_sql_unit(product.unit),
            )
            for product in recipe_request.products
        ]

    @staticmethod
    def to_recipe_response_with_products(recipe: Recipe) -> RecipeResponse:
        return RecipeResponse(
            id=recipe.id,
            name=recipe.name,
            description=recipe.description,
            servings=recipe.servings,
            products=RecipeMapper._get_recipe_product_responses(recipe),
        )

    @staticmethod
    def _get_recipe_product_responses(
        recipe: Recipe,
    ) -> list[RecipeProductResponse]:
        return [
            RecipeProductResponse(
                product=ProductMapper.to_product_response(
                    product_association.product
                ),
                quantity=product_association.quantity,
                unit=UnitMapper.to_unit(product_association.unit),
            )
            for product_association in recipe.product_associations
        ]
