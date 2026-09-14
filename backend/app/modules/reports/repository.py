import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.reports.models import Report


def create_report(db: Session, reporter_id: uuid.UUID, data: dict) -> Report:
    report = Report(reporter_id=reporter_id, status="OPEN", **data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_by_id(db: Session, report_id: uuid.UUID) -> Report | None:
    return db.query(Report).filter(Report.id == report_id).first()


def list_reports(db: Session, status: str | None = None) -> list[Report]:
    query = db.query(Report)
    if status:
        query = query.filter(Report.status == status)
    return query.order_by(Report.created_at.desc()).all()


def update_status(db: Session, report: Report, new_status: str, resolution_notes: str | None = None, resolved_by: uuid.UUID | None = None) -> Report:
    report.status = new_status
    if resolution_notes is not None:
        report.resolution_notes = resolution_notes
    if new_status in {"RESOLVED", "DISMISSED"}:
        report.resolved_by = resolved_by
        report.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(report)
    return report
