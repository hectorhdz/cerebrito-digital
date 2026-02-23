"""create leave_types table

Revision ID: 0003_bl011_leave_types
Revises: 0002_bl008_user_manager_mapping
Create Date: 2026-02-23
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0003_bl011_leave_types"
down_revision: str | None = "0002_bl008_user_manager_mapping"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "leave_types",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_leave_types_code"), "leave_types", ["code"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_leave_types_code"), table_name="leave_types")
    op.drop_table("leave_types")
