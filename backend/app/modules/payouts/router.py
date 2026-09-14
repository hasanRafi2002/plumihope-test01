import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_permission
from app.modules.payouts import service
from app.modules.payouts.schemas import PayoutPublic, PayoutInitiateRequest
from app.modules.users.models import User

router = APIRouter(prefix="/payouts", tags=["payouts"])


@router.post("/initiate", response_model=PayoutPublic, status_code=201)
def initiate_payout(
    payload: PayoutInitiateRequest,
    current_user: User = Depends(require_permission("finance:manage")),
    db: Session = Depends(get_db),
):
    return service.initiate_payout(db, payload.campaign_id, current_user.id)


@router.post("/{payout_id}/complete", response_model=PayoutPublic)
def complete_payout(
    payout_id: uuid.UUID,
    current_user: User = Depends(require_permission("finance:manage")),
    db: Session = Depends(get_db),
):
    return service.process_payout(db, payout_id, current_user.id, succeed=True)


@router.post("/{payout_id}/fail", response_model=PayoutPublic)
def fail_payout(
    payout_id: uuid.UUID,
    current_user: User = Depends(require_permission("finance:manage")),
    db: Session = Depends(get_db),
):
    return service.process_payout(db, payout_id, current_user.id, succeed=False)


@router.post("/{payout_id}/retry", response_model=PayoutPublic, status_code=201)
def retry_payout(
    payout_id: uuid.UUID,
    current_user: User = Depends(require_permission("finance:manage")),
    db: Session = Depends(get_db),
):
    return service.retry_failed_payout(db, payout_id, current_user.id)


@router.get("/campaign/{campaign_id}", response_model=list[PayoutPublic])
def list_campaign_payouts(
    campaign_id: uuid.UUID,
    current_user: User = Depends(require_permission("finance:view")),
    db: Session = Depends(get_db),
):
    return service.list_payouts_for_campaign(db, campaign_id)
