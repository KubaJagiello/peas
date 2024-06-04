from enum import Enum, unique

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.types import Enum as SQLEnum

from peas_app.database.db_config import Base


class BaseEntity(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )


@unique
class Unit(Enum):
    GRAM = "g"
    MILLILITER = "ml"


# Many-to-Many association table between Products and Recipes
class ProductRecipeAssociation(Base):
    __tablename__ = "product_recipe_association"

    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product.id"), primary_key=True
    )
    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Unit] = mapped_column(SQLEnum(Unit), nullable=False)

    product: Mapped["Product"] = relationship(
        "Product", back_populates="recipe_associations"
    )
    recipe: Mapped["Recipe"] = relationship(
        "Recipe", back_populates="product_associations"
    )

    @validates("unit")
    def validate_unit(self, key, unit):
        if not isinstance(unit, Unit):
            try:
                unit = Unit(unit)
            except ValueError:
                raise ValueError(f"Invalid value for unit: {unit}") from None
        return unit


class Product(BaseEntity):
    __tablename__ = "product"

    # native columns
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    proteins: Mapped[float] = mapped_column(Float, nullable=False)
    fats: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrates: Mapped[float] = mapped_column(Float, nullable=False)
    sodium: Mapped[float] = mapped_column(Float, nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)

    # many-to-many relation
    recipe_associations: Mapped[list["ProductRecipeAssociation"]] = (
        relationship("ProductRecipeAssociation", back_populates="product")
    )


class Recipe(BaseEntity):
    __tablename__ = "recipe"

    # native columns
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)

    # many-to-many relation
    product_associations: Mapped[list["ProductRecipeAssociation"]] = (
        relationship("ProductRecipeAssociation", back_populates="recipe")
    )
