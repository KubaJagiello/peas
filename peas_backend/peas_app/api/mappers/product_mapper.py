from peas_app.api.dtos.v1.requests.api_requests import ProductRequest
from peas_app.api.dtos.v1.responses.api_responses import ProductResponse
from peas_app.database.models.models import Product


class ProductMapper:

    @staticmethod
    def to_product_response(product: Product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name,
            proteins=product.proteins,
            fats=product.fats,
            carbohydrates=product.carbohydrates,
            salt=product.salt,
            calories=product.calories,
        )

    @staticmethod
    def to_product(product_request: ProductRequest) -> Product:
        return Product(
            name=product_request.name.lower(),
            proteins=product_request.proteins,
            fats=product_request.fats,
            carbohydrates=product_request.carbohydrates,
            salt=product_request.salt,
            calories=ProductMapper.calculate_calories(product_request),
        )

    @staticmethod
    def calculate_calories(product_request: ProductRequest) -> float:
        return round(
            (product_request.fats * 9.0)
            + (product_request.proteins * 4.0)
            + (product_request.carbohydrates * 4.0),
            1,
        )
