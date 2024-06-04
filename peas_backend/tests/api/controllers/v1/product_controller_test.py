from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import ProductRequest
from peas_app.api.dtos.v1.responses.api_responses import ProductResponse


def test_search_products(
    product_client: TestClient, product_response: ProductResponse
) -> None:
    # Given
    expected_response = product_response
    expected_json = jsonable_encoder(
        Pagination(
            page=1, page_size=5, pages=1, total=5, items=[expected_response]
        )
    )

    # When
    actual_response = product_client.get(
        "api/v1/products/search?name=cheese&page=1&size=5"
    )

    # Then
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_get_all_products(
    product_client: TestClient, product_response: ProductResponse
) -> None:
    # Given
    expected_response = product_response
    expected_json = jsonable_encoder(
        Pagination(
            page=1, page_size=5, pages=1, total=5, items=[expected_response]
        )
    )

    # When
    actual_response = product_client.get("api/v1/products")

    # Then
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_get_product_by_id(
    product_client: TestClient, product_response: ProductResponse
) -> None:
    # Given
    product_id = product_response.id
    expected_json = jsonable_encoder(product_response)

    # When
    actual_response = product_client.get(f"api/v1/products/{product_id}")

    # Then
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_add_product(
    product_client: TestClient,
    product_request: ProductRequest,
    product_response: ProductResponse,
) -> None:
    # Given
    expected_response = product_response
    expected_json = jsonable_encoder(expected_response)

    # When
    actual_response = product_client.post(
        "api/v1/products", json=product_request.model_dump()
    )

    # THen
    assert actual_response.status_code == 201
    assert actual_response.json() == expected_json


def test_update_product(
    product_client: TestClient,
    product_request: ProductRequest,
    product_response: ProductResponse,
) -> None:
    # Given
    product_id = product_response.id
    expected_json = jsonable_encoder(product_response)

    # When
    actual_response = product_client.put(
        f"api/v1/products/{product_id}",
        json=product_request.model_dump(),
    )

    # Actual
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_delete_product(
    product_client: TestClient, product_response: ProductResponse
) -> None:
    # Given
    product_id = product_response.id

    # When
    actual_response = product_client.delete(f"api/v1/products/{product_id}")

    # Then
    assert actual_response.status_code == 204
