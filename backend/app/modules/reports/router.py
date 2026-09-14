import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_permission
from app.modules.auth.dependencies import get_current_user
from app.modules.reports import service
from app.modules.reports.schemas import ReportCreate, ReportPublic, ReportDetail, ReportResolution
from app.modules.users.models import User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportDetail, status_code=201)
def create_report(
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.create_report(db, current_user.id, payload)


@router.get("", response_model=list[ReportPublic])
def list_reports(
    status: str | None = Query(default=None),
    current_user: User = Depends(require_permission("report:review")),
    db: Session = Depends(get_db),
):
    return service.list_reports(db, status)


@router.get("/{report_id}", response_model=ReportDetail)
def get_report(
    report_id: uuid.UUID,
    current_user: User = Depends(require_permission("report:review")),
    db: Session = Depends(get_db),
):
    return service.get_report_or_404(db, report_id)


@router.post("/{report_id}/start-review", response_model=ReportDetail)
def start_review(
    report_id: uuid.UUID,
    current_user: User = Depends(require_permission("report:review")),
    db: Session = Depends(get_db),
):
    return service.start_review(db, report_id)


@router.post("/{report_id}/request-more-info", response_model=ReportDetail)
def request_more_information(
    report_id: uuid.UUID,
    payload: ReportResolution,
    current_user: User = Depends(require_permission("report:review")),
    db: Session = Depends(get_db),
):
    return service.request_more_information(db, report_id, payload.notes)


@router.post("/{report_id}/resolve", response_model=ReportDetail)
def resolve_report(
    report_id: uuid.UUID,
    payload: ReportResolution,
    current_user: User = Depends(require_permission("report:resolve")),
    db: Session = Depends(get_db),
):
    return service.resolve_report(db, report_id, current_user.id, payload.notes)


@router.post("/{report_id}/dismiss", response_model=ReportDetail)
def dismiss_report(
    report_id: uuid.UUID,
    payload: ReportResolution,
    current_user: User = Depends(require_permission("report:resolve")),
    db: Session = Depends(get_db),
):
    return service.dismiss_report(db, report_id, current_user.id, payload.notes)


@router.post("/{report_id}/escalate", response_model=ReportDetail)
def escalate_report(
    report_id: uuid.UUID,
    payload: ReportResolution,
    current_user: User = Depends(require_permission("report:review")),
    db: Session = Depends(get_db),
):
    return service.escalate_report(db, report_id, payload.notes)
