import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.disputes import repository
from app.modules.disputes.models import Dispute
from app.modules.disputes.schemas import DisputeCreate
from app.modules.disputes.state_machine import validate_transition


def create_dispute(db: Session, raised_by: uuid.UUID, payload: DisputeCreate) -> Dispute:
    return repository.create_dispute(db, raised_by, payload.model_dump())


def get_dispute_or_404(db: Session, dispute_id: uuid.UUID) -> Dispute:
    dispute = repository.get_by_id(db, dispute_id)
    if not dispute:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispute not found")
    return dispute


def list_disputes(db: Session, status: str | None = None) -> list[Dispute]:
    return repository.list_disputes(db, status)


def start_review(db: Session, dispute_id: uuid.UUID) -> Dispute:
    dispute = get_dispute_or_404(db, dispute_id)
    validate_transition(dispute.status, "UNDER_REVIEW")
    return repository.update_status(db, dispute, "UNDER_REVIEW")


def resolve_dispute(db: Session, dispute_id: uuid.UUID, resolver_id: uuid.UUID, outcome: str) -> Dispute:
    dispute = get_dispute_or_404(db, dispute_id)
    validate_transition(dispute.status, "RESOLVED")

    dispute = repository.resolve(db, dispute, resolver_id, outcome)

    if outcome == "CAMPAIGN_SUSPENDED" and dispute.campaign_id:
        from app.modules.campaigns import repository as campaigns_repository
        from app.modules.campaigns.state_machine import validate_transition as validate_campaign_transition
        campaign = campaigns_repository.get_by_id(db, dispute.campaign_id)
        if campaign:
            validate_campaign_transition(campaign.status, "SUSPENDED")
            campaigns_repository.update_status(db, campaign, "SUSPENDED")

    return dispute
