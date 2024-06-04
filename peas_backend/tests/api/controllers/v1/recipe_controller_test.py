from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import RecipeRequest
from peas_app.api.dtos.v1.responses.api_responses import RecipeResponse


def test_search_products(
    recipe_client: TestClient, recipe_response: RecipeResponse
) -> None:
    # Given
    expected_response = recipe_response
    expected_json = jsonable_encoder(
        Pagination(
            page=1, page_size=5, pages=1, total=5, items=[expected_response]
        )
    )

    # When
    actual_response = recipe_client.get(
        "api/v1/recipes/search?name=pizza&page=1&size=5"
    )

    # Then
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_get_all_recipes(
    recipe_client: TestClient, recipe_response: RecipeResponse
) -> None:
    # Given
    expected_json = jsonable_encoder(
        Pagination(
            page=1, page_size=5, pages=1, total=5, items=[recipe_response]
        )
    )

    # When
    response = recipe_client.get("api/v1/recipes")

    # Then
    assert response.status_code == 200
    assert response.json() == expected_json


def test_get_recipe_by_id(
    recipe_client: TestClient,
    recipe_response: RecipeResponse,
) -> None:
    # Given
    recipe_id = recipe_response.id
    expected_json = jsonable_encoder(recipe_response)

    # When
    actual_response = recipe_client.get(f"api/v1/recipes/{recipe_id}")

    # Then
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_add_recipe(
    recipe_client: TestClient,
    recipe_request: RecipeRequest,
    recipe_response: RecipeResponse,
) -> None:
    # Given
    expected_json = jsonable_encoder(recipe_response)

    # When
    actual_response = recipe_client.post(
        "api/v1/recipes", json=recipe_request.model_dump()
    )

    # Then
    assert actual_response.status_code == 201
    assert actual_response.json() == expected_json


def test_update_recipe(
    recipe_client: TestClient,
    recipe_request: RecipeRequest,
    recipe_response: RecipeResponse,
) -> None:
    # Given
    expected_json = jsonable_encoder(recipe_response)

    # When
    actual_response = recipe_client.put(
        f"api/v1/recipes/{recipe_response.id}", json=recipe_request.model_dump()
    )

    # Then
    assert actual_response.status_code == 200
    assert actual_response.json() == expected_json


def test_delete_recipe(
    recipe_client: TestClient, recipe_response: RecipeResponse
) -> None:
    # When
    response = recipe_client.delete(f"api/v1/recipes/{recipe_response.id}")

    # Then
    assert response.status_code == 204
