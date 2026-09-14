import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import UUIDPrimaryKeyMixin, TimestampMixin


class Follow(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint("user_id", "agent_profile_id", name="uq_follows_user_agent"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", name="fk_follows_users")
    )
    agent_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_profiles.id", name="fk_follows_agent_profiles")
    )
