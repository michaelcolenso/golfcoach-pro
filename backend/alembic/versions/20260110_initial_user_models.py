"""Initial user models

Revision ID: 001_initial
Revises:
Create Date: 2026-01-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users and user_profiles tables."""

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('handicap', sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()'),
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()'),
            server_onupdate=sa.text('NOW()'),
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('handicap >= 0.0 AND handicap <= 54.0', name='ck_users_handicap_range'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('height_cm', sa.Integer(), nullable=True),
        sa.Column('weight_kg', sa.Integer(), nullable=True),
        sa.Column('dominant_hand', sa.String(length=10), nullable=True),
        sa.Column('primary_miss', sa.String(length=20), nullable=True),
        sa.Column('goals', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column(
            'physical_limitations',
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'[]'::json"),
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('NOW()'),
            server_onupdate=sa.text('NOW()'),
        ),
        sa.CheckConstraint('height_cm >= 50 AND height_cm <= 300', name='ck_user_profiles_height_cm_range'),
        sa.CheckConstraint('weight_kg >= 20 AND weight_kg <= 300', name='ck_user_profiles_weight_kg_range'),
        sa.CheckConstraint(
            "dominant_hand IN ('left', 'right')",
            name='ck_user_profiles_dominant_hand',
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id')
    )


def downgrade() -> None:
    """Drop users and user_profiles tables."""
    op.drop_table('user_profiles')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
