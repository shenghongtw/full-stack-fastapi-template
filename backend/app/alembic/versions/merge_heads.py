"""merge heads

Revision ID: merge_heads
Revises: update_user_table, add_phone_field
Create Date: 2024-02-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'merge_heads'
down_revision = ('update_user_table', 'add_phone_field')  # 指向所有未合併的 head
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
