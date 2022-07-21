"""add_user_table

Revision ID: bf1b1739b27a
Revises: 1fdd92301509
Create Date: 2022-07-19 12:57:33.866047

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import String
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'bf1b1739b27a'
down_revision = '1fdd92301509'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('usermodel',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('roles', sa.types.ARRAY(String), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_totp_enabled', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )

def downgrade() -> None:
    op.drop_table('usermodel')