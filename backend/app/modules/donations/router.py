import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.donations import service
from app.modules.donations.schemas import DonationCreate, DonationPublic, DonationDetail
from app.modules.users.models import User

router = APIRouter(prefix="/donations", tags=["donations"])


@router.post("", response_model=DonationDetail, status_code=201)
def create_donation(
    payload: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    donation = service.create_donation(db, current_user.id, payload)
    return service.get_donation_detail(db, donation.id, current_user.id)


@router.get("/me", response_model=list[DonationPublic])
def list_my_donations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.list_my_donations(db, current_user.id)


@router.get("/{donation_id}", response_model=DonationDetail)
def get_donation(
    donation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_donation_detail(db, donation_id, current_user.id)
