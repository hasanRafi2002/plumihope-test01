import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentProfile, AgentVerification


def get_by_user_id(db: Session, user_id: uuid.UUID) -> AgentProfile | None:
    return db.query(AgentProfile).filter(AgentProfile.user_id == user_id).first()


def get_by_id(db: Session, agent_profile_id: uuid.UUID) -> AgentProfile | None:
    return db.query(AgentProfile).filter(AgentProfile.id == agent_profile_id).first()


def create_profile(db: Session, user_id: uuid.UUID, data: dict) -> AgentProfile:
    profile = AgentProfile(user_id=user_id, status="PENDING", **data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def list_by_status(db: Session, status: str | None = None) -> list[AgentProfile]:
    query = db.query(AgentProfile)
    if status:
        query = query.filter(AgentProfile.status == status)
    return query.order_by(AgentProfile.created_at.desc()).all()


def update_status(db: Session, profile: AgentProfile, new_status: str) -> AgentProfile:
    profile.status = new_status
    db.commit()
    db.refresh(profile)
    return profile


def create_verification_record(
    db: Session, agent_profile_id: uuid.UUID, reviewer_id: uuid.UUID, decision: str, notes: str | None
) -> AgentVerification:
    record = AgentVerification(
        agent_profile_id=agent_profile_id,
        reviewer_id=reviewer_id,
        decision=decision,
        notes=notes,
        reviewed_at=datetime.now(timezone.utc),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
