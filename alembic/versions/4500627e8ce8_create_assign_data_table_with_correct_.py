"""Create assign_data table with correct name

Revision ID: 4500627e8ce8
Revises: 6bb3b09b77d3
Create Date: 2025-07-17 07:37:43.209807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4500627e8ce8'
down_revision: Union[str, Sequence[str], None] = '6bb3b09b77d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
