from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from peas_app.api.dtos.v1.unit import Unit


class ProductRequest(BaseModel):
    name: str = Field(description="The name of the product")
    proteins: float = Field(
        ge=0.0, le=100.0, description="Protein content in grams"
    )
    fats: float = Field(ge=0.0, le=100.0, description="Fat content in grams")
    carbohydrates: float = Field(
        ge=0.0, le=100.0, description="Carbohydrate content in grams"
    )
    sodium: float = Field(
        ge=0.0, le=100.0, description="Sodium content in grams per 100g"
    )

    @model_validator(mode="after")
    def check_total_nutrient_values(self) -> Self:
        if self.proteins + self.fats + self.carbohydrates + self.sodium > 100:
            raise ValueError(
                "The sum of proteins, fats, and carbohydrates cannot exceed 100g"
            )
        return self


class ProductDetail(BaseModel):
    id: int = Field(description="The ID of the product")
    quantity: int = Field(ge=1, description="Quantity of the product")
    unit: Unit = Field(
        description="Unit of measurement for the product, using standard units"
    )


class RecipeRequest(BaseModel):
    name: str = Field(description="The name of the recipe")
    description: str = Field(description="The description of the recipe")
    servings: int = Field(description="The number of servings the recipe")
    products: list[ProductDetail] = Field(
        description="List of products with quantities and units that are part of the recipe",
    )
