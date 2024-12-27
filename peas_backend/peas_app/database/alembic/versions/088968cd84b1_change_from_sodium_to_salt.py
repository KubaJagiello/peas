"""change from sodium to salt

Revision ID: 088968cd84b1
Revises: 2b70eefd6bcd
Create Date: 2024-12-27 23:06:47.913108

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "088968cd84b1"
down_revision: Union[str, None] = "2b70eefd6bcd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new column
    with op.batch_alter_table("product", schema=None) as batch_op:
        # start as nullable
        batch_op.add_column(sa.Column("salt", sa.Float(), nullable=True))

    # Migrate data from sodium to salt
    op.execute("UPDATE product SET salt = sodium")

    # Set the salt column to not null
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.alter_column("salt", nullable=False)

    # Drop the sodium column
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.drop_column("sodium")


def downgrade() -> None:
    # Add the old column back
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("sodium", sa.Float(), nullable=True)
        )  # Start as nullable

    # Migrate data back from 'salt' to 'sodium'
    op.execute("UPDATE product SET sodium = salt")

    # Set the 'sodium' column to NOT NULL
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.alter_column("sodium", nullable=False)

    # Drop the 'salt' column
    with op.batch_alter_table("product", schema=None) as batch_op:
        batch_op.drop_column("salt")
