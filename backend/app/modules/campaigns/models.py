import uuid
from datetime import datetime, date

from sqlalchemy import String, Text, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin, TimestampMixin


class CampaignCategory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "campaign_categories"

    name: Mapped[str] = mapped_column(String(128), unique=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("campaign_categories.id", name="fk_campaign_categories_parent"),
        nullable=True,
    )


class Campaign(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "campaigns"

    help_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("help_requests.id", name="fk_campaigns_help_requests")
    )
    agent_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_profiles.id", name="fk_campaigns_agent_profiles")
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("campaign_categories.id", name="fk_campaigns_categories")
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    target_amount: Mapped[Numeric] = mapped_column(Numeric(14, 2))
    raised_amount: Mapped[Numeric] = mapped_column(Numeric(14, 2), default=0)
    currency: Mapped[str] = mapped_column(String(8), default="BDT")
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")
    verification_status: Mapped[str] = mapped_column(String(32), default="UNVERIFIED")
    recipient_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipient_relationship: Mapped[str | None] = mapped_column(String(128), nullable=True)
    payout_destination_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)

    evidence: Mapped[list["CampaignEvidence"]] = relationship(back_populates="campaign")
    updates: Mapped[list["CampaignUpdate"]] = relationship(back_populates="campaign")


class CampaignEvidence(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "campaign_evidence"

    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("campaigns.id", name="fk_campaign_evidence_campaigns")
    )
    uploader_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_campaign_evidence_users")
    )
    evidence_type: Mapped[str] = mapped_column(String(64))
    media_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media.id", name="fk_campaign_evidence_media"), nullable=True
    )
    visibility: Mapped[str] = mapped_column(String(32), default="RESTRICTED")
    verification_status: Mapped[str] = mapped_column(String(32), default="UPLOADED")
    verified_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_campaign_evidence_verified_by"), nullable=True
    )
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    campaign: Mapped["Campaign"] = relationship(back_populates="evidence")


class CampaignUpdate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "campaign_updates"

    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("campaigns.id", name="fk_campaign_updates_campaigns")
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_campaign_updates_users")
    )
    content: Mapped[str] = mapped_column(Text)

    campaign: Mapped["Campaign"] = relationship(back_populates="updates")
