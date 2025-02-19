"""Add phone field to user table

Revision ID: add_phone_field
Revises: 1a31ce608336
Create Date: 2024-03-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_phone_field'
down_revision: Union[str, None] = '1a31ce608336'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加 phone 字段
    op.add_column('user', sa.Column('phone', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # 删除 phone 字段
    op.drop_column('user', 'phone') 