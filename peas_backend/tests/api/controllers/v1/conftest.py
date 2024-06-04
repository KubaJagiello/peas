from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from peas_app.api.app import app
from peas_app.api.dependencies import get_product_service, get_recipe_service
from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import (
    ProductDetail,
    ProductRequest,
    RecipeRequest,
    Unit,
)
from peas_app.api.dtos.v1.responses.api_responses import (
    ProductResponse,
    RecipeProductResponse,
    RecipeResponse,
)
from peas_app.api.services.product_service import ProductService
from peas_app.api.services.recipe_service import RecipeService


@pytest.fixture
def mock_product_service(product_response: ProductResponse):
    product_service = MagicMock(spec=ProductService)
    pagination = Pagination(
        page=1, page_size=5, pages=1, total=5, items=[product_response]
    )
    product_service.search_product_by_name.return_value = pagination
    product_service.get_all_products.return_value = pagination
    product_service.get_product_by_id.return_value = product_response
    product_service.add_product.return_value = product_response
    product_service.update_product.return_value = product_response
    product_service.delete_product.return_value = None
    return product_service


@pytest.fixture
def product_client(mock_product_service):
    app.dependency_overrides[get_product_service] = lambda: mock_product_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def product_request() -> ProductRequest:
    return ProductRequest(
        name="Cheese",
        proteins=1.0,
        carbohydrates=1.0,
        fats=1.0,
        sodium=1.0,
    )


@pytest.fixture
def product_response() -> ProductResponse:
    return ProductResponse(
        id=123,
        name="Cheese",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        sodium=1.0,
        calories=17.0,
    )


@pytest.fixture
def recipe_request() -> RecipeRequest:
    return RecipeRequest(
        name="Cheese",
        description="Some description",
        servings=1,
        products=[ProductDetail(id=1, quantity=100, unit=Unit.milliliter)],
    )


@pytest.fixture
def recipe_response() -> RecipeResponse:
    return RecipeResponse(
        id=123,
        name="Cheese",
        description="Some description",
        servings=1,
        products=[
            RecipeProductResponse(
                product=ProductResponse(
                    id=1,
                    name="Cheese",
                    proteins=1.0,
                    fats=1.0,
                    carbohydrates=1.0,
                    sodium=1.0,
                    calories=17.0,
                ),
                quantity=100,
                unit=Unit.milliliter,
            ),
            RecipeProductResponse(
                product=ProductResponse(
                    id=2,
                    name="Cheese",
                    proteins=2.0,
                    fats=2.0,
                    carbohydrates=2.0,
                    sodium=2.0,
                    calories=34.0,
                ),
                quantity=200,
                unit=Unit.gram,
            ),
        ],
    )


@pytest.fixture
def mock_recipe_service(recipe_response: RecipeResponse):
    recipe_service = MagicMock(spec=RecipeService)
    pagination = Pagination(
        page=1, page_size=5, pages=1, total=5, items=[recipe_response]
    )
    recipe_service.search_product_by_name.return_value = pagination
    recipe_service.get_all_recipes.return_value = pagination
    recipe_service.get_recipe_by_id.return_value = recipe_response
    recipe_service.add_recipe.return_value = recipe_response
    recipe_service.update_recipe.return_value = recipe_response
    recipe_service.delete_recipe.return_value = None
    return recipe_service


@pytest.fixture
def recipe_client(mock_recipe_service):
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
