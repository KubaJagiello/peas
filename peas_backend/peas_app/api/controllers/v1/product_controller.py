from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Params

from peas_app.api.dependencies import get_product_service
from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.dtos.v1.requests.api_requests import ProductRequest
from peas_app.api.dtos.v1.responses.api_responses import ProductResponse
from peas_app.api.services.product_service import ProductService

router = APIRouter()


@router.get(
    "/products/search", status_code=status.HTTP_200_OK, tags=["Products"]
)
def search_products(
    product_service: Annotated[ProductService, Depends(get_product_service)],
    name: str = Query(description="Search term for product name"),
    params: Params = Depends(),
) -> Pagination[ProductResponse]:
    return product_service.search_product_by_name(
        params.page, params.size, name
    )


@router.get("/products", status_code=status.HTTP_200_OK, tags=["Products"])
def get_all_products(
    product_service: Annotated[ProductService, Depends(get_product_service)],
    params: Params = Depends(),
) -> Pagination[ProductResponse]:
    return product_service.get_all_products(params.page, params.size)


@router.get(
    "/products/{product_id}", status_code=status.HTTP_200_OK, tags=["Products"]
)
def get_product_by_id(
    product_id: str,
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    return product_service.get_product_by_id(int(product_id))


@router.post(
    "/products", status_code=status.HTTP_201_CREATED, tags=["Products"]
)
def create_product(
    product_request: ProductRequest,
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    return product_service.add_product(product_request)


@router.put(
    "/products/{product_id}", status_code=status.HTTP_200_OK, tags=["Products"]
)
def update_product(
    product_id: str,
    product_request: ProductRequest,
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    return product_service.update_product(int(product_id), product_request)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
)
def delete_product(
    product_id: str,
    product_service: Annotated[ProductService, Depends(get_product_service)],
):
    product_service.delete_product(int(product_id))
