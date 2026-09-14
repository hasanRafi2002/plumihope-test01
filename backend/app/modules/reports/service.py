import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.reports import repository
from app.modules.reports.models import Report
from app.modules.reports.schemas import ReportCreate
from app.modules.reports.state_machine import validate_transition


def create_report(db: Session, reporter_id: uuid.UUID, payload: ReportCreate) -> Report:
    return repository.create_report(db, reporter_id, payload.model_dump())


def get_report_or_404(db: Session, report_id: uuid.UUID) -> Report:
    report = repository.get_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report


def list_reports(db: Session, status: str | None = None) -> list[Report]:
    return repository.list_reports(db, status)


def start_review(db: Session, report_id: uuid.UUID) -> Report:
    report = get_report_or_404(db, report_id)
    validate_transition(report.status, "UNDER_REVIEW")
    return repository.update_status(db, report, "UNDER_REVIEW")


def request_more_information(db: Session, report_id: uuid.UUID, notes: str) -> Report:
    report = get_report_or_404(db, report_id)
    validate_transition(report.status, "MORE_INFORMATION_REQUIRED")
    return repository.update_status(db, report, "MORE_INFORMATION_REQUIRED", resolution_notes=notes)


def resolve_report(db: Session, report_id: uuid.UUID, resolver_id: uuid.UUID, notes: str) -> Report:
    report = get_report_or_404(db, report_id)
    validate_transition(report.status, "RESOLVED")
    return repository.update_status(db, report, "RESOLVED", resolution_notes=notes, resolved_by=resolver_id)


def dismiss_report(db: Session, report_id: uuid.UUID, resolver_id: uuid.UUID, notes: str) -> Report:
    report = get_report_or_404(db, report_id)
    validate_transition(report.status, "DISMISSED")
    return repository.update_status(db, report, "DISMISSED", resolution_notes=notes, resolved_by=resolver_id)


def escalate_report(db: Session, report_id: uuid.UUID, notes: str) -> Report:
    report = get_report_or_404(db, report_id)
    validate_transition(report.status, "ESCALATED")
    return repository.update_status(db, report, "ESCALATED", resolution_notes=notes)
