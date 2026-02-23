"""create leave_policies table

Revision ID: 0005_bl013_leave_policies
Revises: 0004_bl012_leave_subtypes
Create Date: 2026-02-23
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0005_bl013_leave_policies"
down_revision: str | None = "0004_bl012_leave_subtypes"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "leave_policies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("leave_type_id", sa.String(length=36), nullable=False),
        sa.Column("leave_subtype_id", sa.String(length=36), nullable=True),
        sa.Column("entitlement_days", sa.Float(), nullable=True),
        sa.Column("accrual_rate_per_month", sa.Float(), nullable=True),
        sa.Column("max_carryover_days", sa.Float(), nullable=True),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("rules_json", sa.String(length=2000), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["leave_type_id"], ["leave_types.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["leave_subtype_id"], ["leave_subtypes.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_leave_policies_code"), "leave_policies", ["code"], unique=True)
    op.create_index(op.f("ix_leave_policies_leave_subtype_id"), "leave_policies", ["leave_subtype_id"], unique=False)
    op.create_index(op.f("ix_leave_policies_leave_type_id"), "leave_policies", ["leave_type_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_leave_policies_leave_type_id"), table_name="leave_policies")
    op.drop_index(op.f("ix_leave_policies_leave_subtype_id"), table_name="leave_policies")
    op.drop_index(op.f("ix_leave_policies_code"), table_name="leave_policies")
    op.drop_table("leave_policies")
