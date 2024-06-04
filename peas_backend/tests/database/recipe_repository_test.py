from sqlalchemy.orm import Session

from peas_app.database.models.models import (
    Product,
    ProductRecipeAssociation,
    Recipe,
    Unit,
)
from peas_app.database.repositories.product_repository import ProductRepository
from peas_app.database.repositories.recipe_repository import RecipeRepository


def test_add_recipe(
    recipe_repository: RecipeRepository, recipe_1: Recipe
) -> None:
    recipe_repository.add(recipe_1)

    retrieved_recipe = recipe_repository.get_by_id(_id=123)

    assert_recipe(expected_recipe=recipe_1, actual_recipe=retrieved_recipe)


def test_add_recipe_with_product(
    recipe_1: Recipe,
    product_1: Product,
    product_repository: ProductRepository,
    recipe_repository: RecipeRepository,
) -> None:
    product_repository.add(product_1)
    product_recipe_association = ProductRecipeAssociation(
        product_id=product_1.id,
        recipe_id=recipe_1.id,
        quantity=200.0,
        unit=Unit.GRAM,
    )
    recipe_1.product_associations.append(product_recipe_association)
    recipe_repository.add(recipe_1)

    actual_recipe = recipe_repository.get_by_id(_id=123)

    assert_recipe(expected_recipe=recipe_1, actual_recipe=actual_recipe)


def test_add_recipe_with_multiple_products(
    product_repository: ProductRepository,
    recipe_repository: RecipeRepository,
    recipe_1: Recipe,
    product_1: Product,
    product_2: Product,
) -> None:
    product_repository.add(product_1)
    product_repository.add(product_2)

    recipe_repository.add(recipe_1)

    expected_product_recipe_association_1 = ProductRecipeAssociation(
        product_id=product_1.id,
        recipe_id=recipe_1.id,
        quantity=200.0,
        unit=Unit.GRAM,
    )

    expected_product_recipe_association_2 = ProductRecipeAssociation(
        product_id=product_2.id,
        recipe_id=recipe_1.id,
        quantity=300.0,
        unit=Unit.GRAM,
    )

    recipe_1.product_associations.append(expected_product_recipe_association_1)
    recipe_1.product_associations.append(expected_product_recipe_association_2)
    actual_retrieved_recipe = recipe_repository.get_by_id(_id=123)

    assert_recipe(
        expected_recipe=recipe_1, actual_recipe=actual_retrieved_recipe
    )


def test_remove_products_from_recipe(
    product_repository: ProductRepository,
    recipe_repository: RecipeRepository,
    recipe_1: Recipe,
    product_1: Product,
    product_2: Product,
) -> None:
    product_repository.add(product_1)
    product_repository.add(product_2)
    recipe_repository.add(recipe_1)

    retrieved_recipe = recipe_repository.get_by_id(_id=recipe_1.id)
    recipe_repository.remove_product(retrieved_recipe, product_1.id)
    retrieved_recipe = recipe_repository.get_by_id(_id=recipe_1.id)

    assert_recipe(expected_recipe=recipe_1, actual_recipe=retrieved_recipe)


def test_add_recipe_with_non_existent_product(
    recipe_repository: RecipeRepository, recipe_1: Recipe, product_1: Product
) -> None:
    recipe_repository.add(recipe_1)

    retrieved_recipe = recipe_repository.get_by_id(_id=123)

    assert_recipe(expected_recipe=recipe_1, actual_recipe=retrieved_recipe)


def test_get_all_recipes(
    product_repository: ProductRepository,
    recipe_repository: RecipeRepository,
    recipe_1: Recipe,
    recipe_2: Recipe,
    product_1: Product,
    product_2: Product,
) -> None:

    product_1 = product_repository.add(product_1)
    product_2 = product_repository.add(product_2)
    product_repository._commit()

    recipe_repository.add(recipe_1)
    recipe_repository.add(recipe_2)
    recipe_repository._commit()

    product_recipe_association_1 = ProductRecipeAssociation(
        product_id=product_1.id,
        recipe_id=recipe_1.id,
        quantity=200.0,
        unit=Unit.GRAM,
    )
    product_recipe_association_2 = ProductRecipeAssociation(
        product_id=product_2.id,
        recipe_id=recipe_1.id,
        quantity=200.0,
        unit=Unit.GRAM,
    )

    recipe_1.product_associations.append(product_recipe_association_1)
    recipe_2.product_associations.append(product_recipe_association_2)

    retrieved_recipes = recipe_repository.get_all(0, 10)
    retrieved_recipes.sort(key=lambda repo: repo.id)

    assert len(retrieved_recipes) == 2
    assert_recipe(expected_recipe=recipe_1, actual_recipe=retrieved_recipes[0])
    assert_recipe(expected_recipe=recipe_2, actual_recipe=retrieved_recipes[1])


def assert_recipe(expected_recipe: Recipe, actual_recipe: Recipe) -> None:
    assert actual_recipe.id == expected_recipe.id
    assert actual_recipe.name == expected_recipe.name
    assert actual_recipe.description == expected_recipe.description
    assert actual_recipe.servings == expected_recipe.servings
    assert set(actual_recipe.product_associations) == set(
        expected_recipe.product_associations
    )
    for expected_association, actual_association in zip(
        expected_recipe.product_associations, actual_recipe.product_associations
    ):
        assert_recipe_association(expected_association, actual_association)


def assert_recipe_association(
    expected_association: ProductRecipeAssociation,
    actual_association: ProductRecipeAssociation,
) -> None:
    assert actual_association.product_id == expected_association.product_id
    assert actual_association.recipe_id == expected_association.recipe_id
    assert actual_association.quantity == expected_association.quantity
    assert actual_association.unit == expected_association.unit
    assert actual_association.product == expected_association.product
