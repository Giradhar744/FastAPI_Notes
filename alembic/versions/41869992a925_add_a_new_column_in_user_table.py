"""Add a new column in User table

Revision ID: 41869992a925
Revises: 
Create Date: 2026-03-22 01:25:44.460266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41869992a925'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('Age', sa.Integer(), nullable=False, server_default="18"))


def downgrade() -> None:
    op.drop_column('users','Age')
    pass
