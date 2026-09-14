import uuid

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin, TimestampMixin


class Payment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "payments"

    donation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("donations.id", name="fk_payments_donations"), unique=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    provider_reference: Mapped[str] = mapped_column(String(255), unique=True)
    amount: Mapped[Numeric] = mapped_column(Numeric(14, 2))
    status: Mapped[str] = mapped_column(String(32), default="INITIATED")

    donation: Mapped["Donation"] = relationship(back_populates="payment")
