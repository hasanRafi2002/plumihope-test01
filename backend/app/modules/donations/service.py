import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.donations import repository
from app.modules.donations.fee_policy import calculate_fee_breakdown
from app.modules.donations.models import Donation
from app.modules.donations.schemas import DonationCreate
from app.modules.campaigns import repository as campaigns_repository

DONATABLE_CAMPAIGN_STATES = {"ACTIVE", "TARGET_REACHED"}


def create_donation(db: Session, user_id: uuid.UUID, payload: DonationCreate) -> Donation:
    campaign = campaigns_repository.get_by_id(db, payload.campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    if campaign.status not in DONATABLE_CAMPAIGN_STATES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Campaign is not currently accepting donations (status: {campaign.status})",
        )

    donation = repository.create_donation(db, user_id, payload.campaign_id, payload.amount, payload.currency)
    return donation


def get_donation_detail(db: Session, donation_id: uuid.UUID, user_id: uuid.UUID) -> dict:
    donation = repository.get_by_id(db, donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

    if donation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this donation")

    fee_breakdown = calculate_fee_breakdown(donation.amount)

    return {
        "id": donation.id,
        "campaign_id": donation.campaign_id,
        "amount": donation.amount,
        "currency": donation.currency,
        "status": donation.status,
        "created_at": donation.created_at,
        "fee_breakdown": fee_breakdown,
    }


def list_my_donations(db: Session, user_id: uuid.UUID) -> list[Donation]:
    return repository.list_by_user(db, user_id)
