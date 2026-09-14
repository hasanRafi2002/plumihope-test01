import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin, TimestampMixin


class HelpRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "help_requests"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_help_requests_users")
    )
    category: Mapped[str] = mapped_column(String(64))
    subcategory: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_info: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="SUBMITTED")

    agents: Mapped[list["HelpRequestAgent"]] = relationship(back_populates="help_request")
    events: Mapped[list["HelpRequestEvent"]] = relationship(back_populates="help_request")


class HelpRequestAgent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "help_request_agents"

    help_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("help_requests.id", name="fk_help_request_agents_help_requests"),
    )
    agent_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agent_profiles.id", name="fk_help_request_agents_agent_profiles"),
    )
    role: Mapped[str] = mapped_column(String(32), default="CLAIMANT")

    help_request: Mapped["HelpRequest"] = relationship(back_populates="agents")


class HelpRequestEvent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "help_request_events"

    help_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("help_requests.id", name="fk_help_request_events_help_requests"),
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_help_request_events_users"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    help_request: Mapped["HelpRequest"] = relationship(back_populates="events")
