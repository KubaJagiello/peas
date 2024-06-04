from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Params

from peas_app.api.dependencies import get_recipe_service
from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import RecipeRequest
from peas_app.api.dtos.v1.responses.api_responses import RecipeResponse
from peas_app.api.services.recipe_service import RecipeService

router = APIRouter()


@router.get("/recipes/search", status_code=status.HTTP_200_OK, tags=["Recipes"])
def search_recipes(
    product_service: Annotated[RecipeService, Depends(get_recipe_service)],
    name: str = Query(description="Search term for product name"),
    params: Params = Depends(),
) -> Pagination[RecipeResponse]:
    return product_service.search_product_by_name(
        params.page, params.size, name
    )


@router.get("/recipes", status_code=status.HTTP_200_OK, tags=["Recipes"])
def get_all_recipes(
    product_service: Annotated[RecipeService, Depends(get_recipe_service)],
    params: Params = Depends(),
) -> Pagination[RecipeResponse]:
    return product_service.get_all_recipes(params.page, params.size)


@router.get(
    "/recipes/{recipe_id}", status_code=status.HTTP_200_OK, tags=["Recipes"]
)
def get_recipe_by_id(
    recipe_id: str,
    recipe_service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> RecipeResponse:
    return recipe_service.get_recipe_by_id(int(recipe_id))


@router.post("/recipes", status_code=status.HTTP_201_CREATED, tags=["Recipes"])
def create_recipe(
    recipe_request: RecipeRequest,
    recipe_service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> RecipeResponse:
    return recipe_service.add_recipe(recipe_request)


@router.put(
    "/recipes/{recipe_id}", status_code=status.HTTP_200_OK, tags=["Recipes"]
)
def update_recipe(
    recipe_id: str,
    recipe_request: RecipeRequest,
    recipe_service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> RecipeResponse:
    return recipe_service.update_recipe(int(recipe_id), recipe_request)


@router.delete(
    "/recipes/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Recipes"],
)
def delete_recipe(
    recipe_id: str,
    recipe_service: Annotated[RecipeService, Depends(get_recipe_service)],
):
    recipe_service.delete_recipe(int(recipe_id))
