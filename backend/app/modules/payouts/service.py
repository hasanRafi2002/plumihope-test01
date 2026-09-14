import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.payouts import repository
from app.modules.payouts.models import Payout
from app.modules.payouts.state_machine import validate_transition
from app.modules.campaigns import repository as campaigns_repository
from app.modules.campaigns.state_machine import validate_transition as validate_campaign_transition
from app.modules.audit import repository as audit_repository


def initiate_payout(db: Session, campaign_id: uuid.UUID, actor_id: uuid.UUID) -> Payout:
    campaign = campaigns_repository.get_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.status != "TARGET_REACHED":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Campaign must be TARGET_REACHED before payout can be initiated",
        )

    existing = repository.get_active_payout_for_campaign(db, campaign_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An active payout already exists for this campaign")

    payout = repository.create_payout(db, campaign_id, campaign.raised_amount)

    validate_campaign_transition(campaign.status, "PAYOUT_PENDING")
    campaigns_repository.update_status(db, campaign, "PAYOUT_PENDING")

    audit_repository.create_log(
        db, actor_id, "PAYOUT_INITIATED", "payout", payout.id,
        after={"status": payout.status, "amount": str(payout.amount)},
    )

    return payout


def process_payout(db: Session, payout_id: uuid.UUID, actor_id: uuid.UUID, succeed: bool) -> Payout:
    payout = repository.get_by_id(db, payout_id)
    if not payout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payout not found")

    validate_transition(payout.status, "PROCESSING")
    payout = repository.update_status(db, payout, "PROCESSING")

    target_status = "COMPLETED" if succeed else "FAILED"
    validate_transition(payout.status, target_status)
    payout = repository.update_status(db, payout, target_status)

    audit_repository.create_log(
        db, actor_id, f"PAYOUT_{target_status}", "payout", payout.id,
        after={"status": payout.status},
    )

    if succeed:
        campaign = campaigns_repository.get_by_id(db, payout.campaign_id)
        validate_campaign_transition(campaign.status, "ASSISTANCE_PENDING")
        campaigns_repository.update_status(db, campaign, "ASSISTANCE_PENDING")

    return payout


def retry_failed_payout(db: Session, failed_payout_id: uuid.UUID, actor_id: uuid.UUID) -> Payout:
    failed_payout = repository.get_by_id(db, failed_payout_id)
    if not failed_payout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payout not found")

    if failed_payout.status != "FAILED":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only FAILED payouts can be retried")

    # Original failed row remains as historical evidence; create a new row.
    new_payout = repository.create_payout(db, failed_payout.campaign_id, failed_payout.amount)

    audit_repository.create_log(
        db, actor_id, "PAYOUT_RETRY_CREATED", "payout", new_payout.id,
        before={"original_failed_payout_id": str(failed_payout_id)},
        after={"status": new_payout.status},
    )

    return new_payout


def list_payouts_for_campaign(db: Session, campaign_id: uuid.UUID) -> list[Payout]:
    return repository.list_by_campaign(db, campaign_id)
