"""Leave policy ORM model placeholder for entitlement/accrual rules."""

from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class LeavePolicy(Base):
    __tablename__ = "leave_policies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    leave_type_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("leave_types.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    leave_subtype_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("leave_subtypes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    entitlement_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    accrual_rate_per_month: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_carryover_days: Mapped[float | None] = mapped_column(Float, nullable=True)
    effective_from: Mapped[date | None] = mapped_column(Date, nullable=True)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)
    rules_json: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
