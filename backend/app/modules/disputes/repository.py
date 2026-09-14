import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.disputes.models import Dispute


def create_dispute(db: Session, raised_by: uuid.UUID, data: dict) -> Dispute:
    dispute = Dispute(raised_by=raised_by, status="OPEN", **data)
    db.add(dispute)
    db.commit()
    db.refresh(dispute)
    return dispute


def get_by_id(db: Session, dispute_id: uuid.UUID) -> Dispute | None:
    return db.query(Dispute).filter(Dispute.id == dispute_id).first()


def list_disputes(db: Session, status: str | None = None) -> list[Dispute]:
    query = db.query(Dispute)
    if status:
        query = query.filter(Dispute.status == status)
    return query.order_by(Dispute.created_at.desc()).all()


def update_status(db: Session, dispute: Dispute, new_status: str) -> Dispute:
    dispute.status = new_status
    db.commit()
    db.refresh(dispute)
    return dispute


def resolve(db: Session, dispute: Dispute, resolver_id: uuid.UUID, outcome: str) -> Dispute:
    dispute.status = "RESOLVED"
    dispute.outcome = outcome
    dispute.resolved_by = resolver_id
    dispute.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(dispute)
    return dispute
