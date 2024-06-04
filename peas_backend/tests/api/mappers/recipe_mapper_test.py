import pytest

from peas_app.api.dtos.v1.requests.api_requests import (
    ProductDetail,
    RecipeRequest,
)
from peas_app.api.dtos.v1.responses.api_responses import (
    ProductResponse,
    RecipeProductResponse,
    RecipeResponse,
)
from peas_app.api.dtos.v1.unit import Unit
from peas_app.api.mappers.recipe_mapper import RecipeMapper
from peas_app.database.models.models import (
    Product,
    ProductRecipeAssociation,
    Recipe,
)
from peas_app.database.models.models import Unit as SqlUnit


@pytest.fixture(scope="function")
def product_1() -> Product:
    return Product(
        id=123,
        name="Test Product",
        proteins=1.0,
        fats=1.0,
        carbohydrates=1.0,
        sodium=1.0,
        calories=17.0,
    )


@pytest.fixture(scope="function")
def product_2() -> Product:
    return Product(
        id=456,
        name="Test Product 2",
        proteins=2.0,
        fats=2.0,
        carbohydrates=2.0,
        sodium=2.0,
        calories=34.0,
    )


@pytest.fixture(scope="function")
def recipe_product_association_1(
    product_1: Product,
) -> ProductRecipeAssociation:
    return ProductRecipeAssociation(
        product_id=product_1.id,
        quantity=100,
        unit=SqlUnit.GRAM,
        product=product_1,
    )


@pytest.fixture(scope="function")
def recipe_product_association_2(
    product_2: Product,
) -> ProductRecipeAssociation:
    return ProductRecipeAssociation(
        product_id=product_2.id,
        quantity=200,
        unit=SqlUnit.MILLILITER,
        product=product_2,
    )


@pytest.fixture(scope="function")
def recipe_1(
    recipe_product_association_1,
    recipe_product_association_2: ProductRecipeAssociation,
    product_1: Product,
    product_2: Product,
) -> Recipe:
    return Recipe(
        id=123,
        name="Test Recipe",
        product_associations=[
            recipe_product_association_1,
            recipe_product_association_2,
        ],
        description="Test Description",
        servings=4,
    )


@pytest.fixture(scope="function")
def recipe_request_1() -> RecipeRequest:
    return RecipeRequest(
        name="Test Recipe",
        products=[
            ProductDetail(id=123, quantity=100, unit=Unit.gram),
            ProductDetail(id=456, quantity=200, unit=Unit.milliliter),
        ],
        description="Test Description",
        servings=4,
    )


def test_to_recipe(recipe_request_1: RecipeRequest):
    expected_recipe = Recipe(
        name=recipe_request_1.name,
        description=recipe_request_1.description,
        servings=recipe_request_1.servings,
        product_associations=[
            ProductRecipeAssociation(
                product_id=recipe_request_1.products[0].id,
                quantity=recipe_request_1.products[0].quantity,
                unit=SqlUnit.GRAM,
            ),
            ProductRecipeAssociation(
                product_id=recipe_request_1.products[1].id,
                quantity=recipe_request_1.products[1].quantity,
                unit=SqlUnit.MILLILITER,
            ),
        ],
    )

    actual_recipe = RecipeMapper.to_recipe(recipe_request=recipe_request_1)

    assert expected_recipe.name == actual_recipe.name
    assert expected_recipe.description == actual_recipe.description
    assert expected_recipe.servings == actual_recipe.servings
    assert_product_recipe_association(
        expected_recipe.product_associations, actual_recipe.product_associations
    )


def test_to_recipe_response_with_no_products(recipe_1: Recipe):
    recipe_1.products = []
    recipe_1.product_associations = []
    expected_recipe_response = RecipeResponse(
        id=123,
        name=recipe_1.name,
        description=recipe_1.description,
        servings=recipe_1.servings,
        products=[],
    )

    actual_recipe_response = RecipeMapper.to_recipe_response_with_products(
        recipe=recipe_1
    )

    assert_recipe_response(expected_recipe_response, actual_recipe_response)


def test_to_recipe_response_with_products(
    recipe_1: Recipe, product_1: Product, product_2: Product
):
    expected_recipe_response = RecipeResponse(
        id=recipe_1.id,
        name=recipe_1.name,
        description=recipe_1.description,
        servings=recipe_1.servings,
        products=[
            RecipeProductResponse(
                product=ProductResponse(
                    id=product_1.id,
                    name=product_1.name,
                    proteins=product_1.proteins,
                    fats=product_1.fats,
                    carbohydrates=product_1.carbohydrates,
                    sodium=product_1.sodium,
                    calories=product_1.calories,
                ),
                quantity=recipe_1.product_associations[0].quantity,
                unit=Unit.gram,
            ),
            RecipeProductResponse(
                product=ProductResponse(
                    id=product_2.id,
                    name=product_2.name,
                    proteins=product_2.proteins,
                    fats=product_2.fats,
                    carbohydrates=product_2.carbohydrates,
                    sodium=product_2.sodium,
                    calories=product_2.calories,
                ),
                quantity=recipe_1.product_associations[1].quantity,
                unit=Unit.milliliter,
            ),
        ],
    )

    actual_recipe_response = RecipeMapper.to_recipe_response_with_products(
        recipe_1
    )

    assert_recipe_response(expected_recipe_response, actual_recipe_response)


def assert_product_recipe_association(
    expected_product_recipe_association: list[ProductRecipeAssociation],
    actual_product_recipe_association: list[ProductRecipeAssociation],
):
    for expected, actual in zip(
        expected_product_recipe_association, actual_product_recipe_association
    ):
        assert expected.product_id == actual.product_id
        assert expected.quantity == actual.quantity
        assert expected.unit == actual.unit


def assert_recipe_response(expected: RecipeResponse, actual: RecipeResponse):
    assert expected.id == actual.id
    assert expected.name == actual.name
    assert expected.description == actual.description
    assert expected.servings == actual.servings
    assert expected.products == actual.products
