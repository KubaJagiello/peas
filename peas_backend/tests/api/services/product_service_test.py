from peas_app.api.dtos.v1.pagination import Pagination
from peas_app.api.services.product_service import ProductService
from peas_app.database.models.models import Product


def test_add_product(
    product_service: ProductService,
    mock_product_repository,
    product,
    product_response,
    product_request,
) -> None:
    # Given
    mock_product_repository.add.return_value = product

    # When
    actual_product_response = product_service.add_product(product_request)

    # Then
    assert actual_product_response == product_response
    mock_product_repository.add.assert_called_once()


def test_get_all_products(
    product_service, mock_product_repository, product, product_response
) -> None:
    # Given
    pagination = Pagination(
        page=1, page_size=5, pages=1, total=5, items=[product_response]
    )
    mock_product_repository.get_all.return_value = [product]
    mock_product_repository.get_total_rows_count.return_value = 5

    # When
    actual_product_responses = product_service.get_all_products(
        page_number=1, page_size=5
    )

    # Then
    assert actual_product_responses == pagination
    mock_product_repository.get_all.assert_called_once()
    mock_product_repository.get_total_rows_count.assert_called_once()


def test_get_product_by_id(
    product_service, mock_product_repository, product, product_response
) -> None:
    # Given
    mock_product_repository.get_by_id.return_value = product

    # When
    actual_product_response = product_service.get_product_by_id(product.id)

    # Then
    assert actual_product_response == product_response
    mock_product_repository.get_by_id.assert_called_once_with(_id=product.id)


def test_delete_product(
    product_service, mock_product_repository, product: Product
) -> None:
    # Given
    mock_product_repository.get_by_id.return_value = product

    # When
    product_service.delete_product(product.id)

    # Then
    mock_product_repository.get_by_id.assert_called_once_with(_id=product.id)
    mock_product_repository.delete.assert_called_once_with(product)


def test_update_product(
    product_service,
    mock_product_repository,
    product,
    product_request,
    product_response,
) -> None:
    # Given
    mock_product_repository.update.return_value = product

    # When
    actual_product_response = product_service.update_product(
        product.id, product_request
    )

    # Then
    assert actual_product_response == product_response
    mock_product_repository.update.assert_called()
