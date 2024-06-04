from typing import Generator

import pytest
from sqlalchemy.orm import Session

from peas_app.database.db_config import DatabaseConfig
from peas_app.database.models.models import Product, Recipe
from peas_app.database.repositories.product_repository import ProductRepository
from peas_app.database.repositories.recipe_repository import RecipeRepository


@pytest.fixture(scope="function")
def db_config() -> Generator[DatabaseConfig, None, None]:
    config = DatabaseConfig(database_url="sqlite:///:memory:")
    config.create_all_tables()
    yield config
    config.drop_all_tables()


@pytest.fixture(scope="function")
def session(db_config: DatabaseConfig) -> Generator[Session, None, None]:
    session = db_config.get_session()
    yield session
    session.rollback()
    db_config.close_session()


@pytest.fixture(scope="function")
def product_repository(session: Session) -> ProductRepository:
    return ProductRepository(session)


@pytest.fixture(scope="function")
def recipe_repository(session: Session) -> RecipeRepository:
    return RecipeRepository(session)


@pytest.fixture(scope="function")
def product_1() -> Product:
    return Product(
        id=123,
        name="Test Product 2",
        proteins=2.0,
        fats=2.0,
        carbohydrates=2.0,
        sodium=2.0,
        calories=34.0,
    )


@pytest.fixture(scope="function")
def product_2() -> Product:
    return Product(
        id=456,
        name="Test Product 3",
        proteins=3.0,
        fats=3.0,
        carbohydrates=3.0,
        sodium=3.0,
        calories=51.0,
    )


@pytest.fixture(scope="function")
def product_3() -> Product:
    return Product(
        id=789,
        name="Test Product 4",
        proteins=4.0,
        fats=4.0,
        carbohydrates=4.0,
        sodium=4.0,
        calories=68.0,
    )


@pytest.fixture(scope="function")
def recipe_1() -> Recipe:
    return Recipe(
        id=123,
        name="Test Recipe 1",
        description="Test Description 1",
        servings=4,
    )


@pytest.fixture(scope="function")
def recipe_2() -> Recipe:
    return Recipe(
        id=456,
        name="Test Recipe 2",
        description="Test Description 2",
        servings=4,
    )
