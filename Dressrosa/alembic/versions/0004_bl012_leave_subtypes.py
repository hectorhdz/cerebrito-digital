"""create leave_subtypes table

Revision ID: 0004_bl012_leave_subtypes
Revises: 0003_bl011_leave_types
Create Date: 2026-02-23
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0004_bl012_leave_subtypes"
down_revision: str | None = "0003_bl011_leave_types"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "leave_subtypes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("leave_type_id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["leave_type_id"], ["leave_types.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("leave_type_id", "code", name="uq_leave_subtypes_leave_type_code"),
    )
    op.create_index(op.f("ix_leave_subtypes_leave_type_id"), "leave_subtypes", ["leave_type_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_leave_subtypes_leave_type_id"), table_name="leave_subtypes")
    op.drop_table("leave_subtypes")
