"""init

Revision ID: dc4fba89f119
Revises: 
Create Date: 2024-08-18 17:45:42.745662

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc4fba89f119"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("proteins", sa.Float(), nullable=False),
        sa.Column("fats", sa.Float(), nullable=False),
        sa.Column("carbohydrates", sa.Float(), nullable=False),
        sa.Column("sodium", sa.Float(), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "recipe",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("servings", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_recipe_association",
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column(
            "unit", sa.Enum("GRAMS", "MILLILITERS", name="unit"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipe.id"],
        ),
        sa.PrimaryKeyConstraint("product_id", "recipe_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("product_recipe_association")
    op.drop_table("recipe")
    op.drop_table("product")
    # ### end Alembic commands ###
