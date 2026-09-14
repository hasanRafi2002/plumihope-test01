import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_permission
from app.modules.auth.dependencies import get_current_user
from app.modules.disputes import service
from app.modules.disputes.schemas import DisputeCreate, DisputePublic, DisputeResolution
from app.modules.users.models import User

router = APIRouter(prefix="/disputes", tags=["disputes"])


@router.post("", response_model=DisputePublic, status_code=201)
def create_dispute(
    payload: DisputeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.create_dispute(db, current_user.id, payload)


@router.get("", response_model=list[DisputePublic])
def list_disputes(
    status: str | None = Query(default=None),
    current_user: User = Depends(require_permission("dispute:resolve")),
    db: Session = Depends(get_db),
):
    return service.list_disputes(db, status)


@router.get("/{dispute_id}", response_model=DisputePublic)
def get_dispute(
    dispute_id: uuid.UUID,
    current_user: User = Depends(require_permission("dispute:resolve")),
    db: Session = Depends(get_db),
):
    return service.get_dispute_or_404(db, dispute_id)


@router.post("/{dispute_id}/start-review", response_model=DisputePublic)
def start_review(
    dispute_id: uuid.UUID,
    current_user: User = Depends(require_permission("dispute:resolve")),
    db: Session = Depends(get_db),
):
    return service.start_review(db, dispute_id)


@router.post("/{dispute_id}/resolve", response_model=DisputePublic)
def resolve_dispute(
    dispute_id: uuid.UUID,
    payload: DisputeResolution,
    current_user: User = Depends(require_permission("dispute:resolve")),
    db: Session = Depends(get_db),
):
    return service.resolve_dispute(db, dispute_id, current_user.id, payload.outcome)
