import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_permission
from app.modules.moderation import service
from app.modules.moderation.schemas import ApprovalRequest, RejectionRequest, MoreInfoRequest
from app.modules.campaigns.schemas import CampaignDetail
from app.modules.users.models import User

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.get("/campaigns", response_model=list[CampaignDetail])
def list_campaign_queue(
    current_user: User = Depends(require_permission("campaign:review")),
    db: Session = Depends(get_db),
):
    return service.list_campaign_queue(db)


@router.post("/campaigns/{campaign_id}/approve", response_model=CampaignDetail)
def approve_campaign(
    campaign_id: uuid.UUID,
    payload: ApprovalRequest,
    current_user: User = Depends(require_permission("campaign:approve")),
    db: Session = Depends(get_db),
):
    return service.approve_campaign(db, campaign_id, current_user.id, payload.notes)


@router.post("/campaigns/{campaign_id}/reject", response_model=CampaignDetail)
def reject_campaign(
    campaign_id: uuid.UUID,
    payload: RejectionRequest,
    current_user: User = Depends(require_permission("campaign:reject")),
    db: Session = Depends(get_db),
):
    return service.reject_campaign(db, campaign_id, current_user.id, payload.notes)


@router.post("/campaigns/{campaign_id}/request-more-info", response_model=CampaignDetail)
def request_more_info(
    campaign_id: uuid.UUID,
    payload: MoreInfoRequest,
    current_user: User = Depends(require_permission("campaign:review")),
    db: Session = Depends(get_db),
):
    return service.request_more_info(db, campaign_id, current_user.id, payload.notes)


@router.post("/campaigns/{campaign_id}/final-approve", response_model=CampaignDetail)
def approve_final_review(
    campaign_id: uuid.UUID,
    payload: ApprovalRequest,
    current_user: User = Depends(require_permission("campaign:approve")),
    db: Session = Depends(get_db),
):
    return service.approve_final_review(db, campaign_id, current_user.id, payload.notes)
