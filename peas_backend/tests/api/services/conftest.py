from unittest.mock import MagicMock

import pytest

from peas_app.api.dtos.v1.requests.api_requests import ProductRequest
from peas_app.api.dtos.v1.responses.api_responses import ProductResponse
from peas_app.api.services.product_service import ProductService
from peas_app.database.models.models import Product
from peas_app.database.repositories.product_repository import ProductRepository


@pytest.fixture
def mock_product_repository():
    return MagicMock(spec=ProductRepository)


@pytest.fixture
def product_service(mock_product_repository) -> ProductService:
    return ProductService(mock_product_repository)


@pytest.fixture
def product_request():
    return ProductRequest(
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        salt=1.0,
    )


@pytest.fixture
def product():
    return Product(
        id=123,
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        salt=1.0,
        calories=17.0,
    )


@pytest.fixture
def product_response():
    return ProductResponse(
        id=123,
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        salt=1.0,
        calories=17.0,
    )
