import uuid

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin, TimestampMixin


class Donation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "donations"

    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("campaigns.id", name="fk_donations_campaigns")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_donations_users")
    )
    amount: Mapped[Numeric] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(8), default="BDT")
    status: Mapped[str] = mapped_column(String(32), default="INITIATED")

    payment: Mapped["Payment"] = relationship(back_populates="donation", uselist=False)
