from typing import Annotated

from fastapi import Depends

from peas_app.api.services.product_service import ProductService
from peas_app.api.services.recipe_service import RecipeService
from peas_app.database.db_config import DatabaseConfig
from peas_app.database.repositories.product_repository import ProductRepository
from peas_app.database.repositories.recipe_repository import RecipeRepository

db_config_instance = None


def get_db_config() -> DatabaseConfig:
    global db_config_instance
    if db_config_instance is None:
        db_config_instance = DatabaseConfig()
    return db_config_instance


def get_product_repository(
    db_config: Annotated[DatabaseConfig, Depends(get_db_config)],
) -> ProductRepository:
    return ProductRepository(db_config.get_session())


def get_product_service(
    product_repository: Annotated[
        ProductRepository, Depends(get_product_repository)
    ],
) -> ProductService:
    return ProductService(product_repository)


def get_recipe_repository(
    db_config: Annotated[DatabaseConfig, Depends(get_db_config)],
) -> RecipeRepository:
    return RecipeRepository(db_config.get_session())


def get_recipe_service(
    recipe_repository: Annotated[
        RecipeRepository, Depends(get_recipe_repository)
    ],
    product_repository: Annotated[
        ProductRepository, Depends(get_product_repository)
    ],
) -> RecipeService:
    return RecipeService(recipe_repository, product_repository)
