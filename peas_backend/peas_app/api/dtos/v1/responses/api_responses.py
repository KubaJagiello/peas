from pydantic import BaseModel, Field

from peas_app.api.dtos.v1.unit import Unit


class ProductResponse(BaseModel):
    id: int = Field(description="The unique identifier of the product")
    name: str = Field(description="The name of the product")
    proteins: float = Field(description="Protein content in grams per 100g")
    fats: float = Field(description="Fat content in grams per 100g")
    carbohydrates: float = Field(
        description="Carbohydrate content in grams per 100g"
    )
    salt: float = Field(description="salt content in grams per 100g")
    calories: float = Field(description="Caloric content in kcal per 100g")


class RecipeProductResponse(BaseModel):
    product: ProductResponse = Field(
        description="The product that is part of the recipe"
    )
    quantity: float = Field(description="Quantity of the product")
    unit: Unit = Field(description="Unit of measurement for the product")


class RecipeResponse(BaseModel):
    id: int = Field(description="The unique identifier of the recipe")
    name: str = Field(description="The name of the recipe")
    description: str = Field(description="The description of the recipe")
    servings: int = Field(description="The number of servings the recipe")
    products: list[RecipeProductResponse] = Field(
        description="List of products that are part of the recipe"
    )
