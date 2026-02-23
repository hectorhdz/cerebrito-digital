"""add manager mapping to users

Revision ID: 0002_bl008_user_manager_mapping
Revises: 0001_bl002_initial_auth_tables
Create Date: 2026-02-23
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0002_bl008_user_manager_mapping"
down_revision: str | None = "0001_bl002_initial_auth_tables"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("manager_id", sa.String(length=36), nullable=True))
    op.create_index(op.f("ix_users_manager_id"), "users", ["manager_id"], unique=False)
    op.create_foreign_key(
        "fk_users_manager_id_users",
        "users",
        "users",
        ["manager_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_users_manager_id_users", "users", type_="foreignkey")
    op.drop_index(op.f("ix_users_manager_id"), table_name="users")
    op.drop_column("users", "manager_id")
