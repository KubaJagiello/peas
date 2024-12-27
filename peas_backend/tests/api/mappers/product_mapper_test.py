from peas_app.api.dtos.v1.requests.api_requests import ProductRequest
from peas_app.api.dtos.v1.responses.api_responses import ProductResponse
from peas_app.api.mappers.product_mapper import ProductMapper
from peas_app.database.models.models import Product


def test_to_product_response():
    product = Product(
        id=123,
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        salt=1.0,
        calories=17.0,
    )
    expected_product_response = ProductResponse(
        id=product.id,
        name=product.name,
        proteins=product.proteins,
        fats=product.fats,
        carbohydrates=product.carbohydrates,
        salt=product.salt,
        calories=product.calories,
    )

    actual_product_response = ProductMapper.to_product_response(product=product)

    assert actual_product_response == expected_product_response


def test_to_product():
    product_request = ProductRequest(
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        salt=1.0,
    )
    expected_product = Product(
        name=product_request.name.lower(),
        proteins=product_request.proteins,
        fats=product_request.fats,
        carbohydrates=product_request.carbohydrates,
        calories=17.0,
    )

    actual_product = ProductMapper.to_product(product_request=product_request)

    assert actual_product.name == expected_product.name
    assert actual_product.proteins == expected_product.proteins
    assert actual_product.fats == expected_product.fats
    assert actual_product.carbohydrates == expected_product.carbohydrates
    assert actual_product.calories == expected_product.calories


def test_calculate_calories():
    product_request = ProductRequest(
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        salt=1.0,
    )
    expected_calories = 17.0

    actual_calories = ProductMapper.calculate_calories(
        product_request=product_request
    )

    assert actual_calories == expected_calories
