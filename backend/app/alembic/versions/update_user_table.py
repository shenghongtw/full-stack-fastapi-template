"""Update user table for Google OAuth

Revision ID: update_user_table
Revises: add_phone_field
Create Date: 2024-02-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'update_user_table'
down_revision: Union[str, None] = 'add_phone_field'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加 google_id 字段
    op.add_column('user', sa.Column('google_id', sa.String(length=255), nullable=True))
    # 添加唯一索引
    op.create_index('ix_user_google_id', 'user', ['google_id'], unique=True)
    
    # 如果 hashed_password 列還存在，就刪除它
    try:
        op.drop_column('user', 'hashed_password')
    except Exception:
        pass


def downgrade() -> None:
    # 刪除 google_id 索引
    op.drop_index('ix_user_google_id')
    # 刪除 google_id 字段
    op.drop_column('user', 'google_id')
    
    # 添加回 hashed_password 列
    op.add_column('user', sa.Column('hashed_password', sa.String(length=255), nullable=True))
