import uuid

from sqlalchemy.orm import Session

from app.modules.payouts.models import Payout


def create_payout(db: Session, campaign_id: uuid.UUID, amount) -> Payout:
    payout = Payout(campaign_id=campaign_id, amount=amount, status="PENDING")
    db.add(payout)
    db.commit()
    db.refresh(payout)
    return payout


def get_by_id(db: Session, payout_id: uuid.UUID) -> Payout | None:
    return db.query(Payout).filter(Payout.id == payout_id).first()


def list_by_campaign(db: Session, campaign_id: uuid.UUID) -> list[Payout]:
    return db.query(Payout).filter(Payout.campaign_id == campaign_id).order_by(Payout.created_at.desc()).all()


def get_active_payout_for_campaign(db: Session, campaign_id: uuid.UUID) -> Payout | None:
    return (
        db.query(Payout)
        .filter(Payout.campaign_id == campaign_id, Payout.status.in_(["PENDING", "PROCESSING", "COMPLETED"]))
        .first()
    )


def update_status(db: Session, payout: Payout, new_status: str) -> Payout:
    payout.status = new_status
    db.commit()
    db.refresh(payout)
    return payout
