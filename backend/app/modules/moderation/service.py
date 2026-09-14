import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.campaigns import repository as campaigns_repository
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.state_machine import validate_transition
from app.modules.reports.models import Review


def _notify_campaign_owner(db: Session, campaign: Campaign, notification_type: str, title: str, body: str) -> None:
    from app.modules.notifications.service import notify
    from app.modules.agents.models import AgentProfile

    agent_profile = db.query(AgentProfile).filter(AgentProfile.id == campaign.agent_profile_id).first()
    if agent_profile:
        notify(db, agent_profile.user_id, notification_type, title, body)


def _create_review(db: Session, reviewer_id: uuid.UUID, entity_id: uuid.UUID, decision: str, notes: str | None) -> None:
    review = Review(
        reviewer_id=reviewer_id,
        entity_type="campaign",
        entity_id=entity_id,
        decision=decision,
        notes=notes,
    )
    db.add(review)
    db.commit()


def list_campaign_queue(db: Session) -> list[Campaign]:
    return campaigns_repository.list_campaigns(db, status="SUBMITTED")


def _get_campaign_under_review(db: Session, campaign_id: uuid.UUID) -> Campaign:
    campaign = campaigns_repository.get_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign


def approve_campaign(db: Session, campaign_id: uuid.UUID, reviewer_id: uuid.UUID, notes: str | None) -> Campaign:
    campaign = _get_campaign_under_review(db, campaign_id)

    if campaign.status == "SUBMITTED":
        validate_transition(campaign.status, "UNDER_REVIEW")
        campaign = campaigns_repository.update_status(db, campaign, "UNDER_REVIEW")

    validate_transition(campaign.status, "APPROVED")
    campaign = campaigns_repository.update_status(db, campaign, "APPROVED")
    _create_review(db, reviewer_id, campaign_id, "APPROVED", notes)

    validate_transition(campaign.status, "ACTIVE")
    campaign = campaigns_repository.update_status(db, campaign, "ACTIVE")

    _notify_campaign_owner(db, campaign, "CAMPAIGN_APPROVED", "Campaign approved", f'Your campaign "{campaign.title}" was approved and is now active.')

    return campaign


def reject_campaign(db: Session, campaign_id: uuid.UUID, reviewer_id: uuid.UUID, notes: str) -> Campaign:
    campaign = _get_campaign_under_review(db, campaign_id)

    if campaign.status == "SUBMITTED":
        validate_transition(campaign.status, "UNDER_REVIEW")
        campaign = campaigns_repository.update_status(db, campaign, "UNDER_REVIEW")

    validate_transition(campaign.status, "REJECTED")
    campaign = campaigns_repository.update_status(db, campaign, "REJECTED")
    _create_review(db, reviewer_id, campaign_id, "REJECTED", notes)

    _notify_campaign_owner(db, campaign, "CAMPAIGN_REJECTED", "Campaign rejected", f'Your campaign "{campaign.title}" was rejected: {notes}')

    return campaign


def request_more_info(db: Session, campaign_id: uuid.UUID, reviewer_id: uuid.UUID, notes: str) -> Campaign:
    campaign = _get_campaign_under_review(db, campaign_id)

    if campaign.status != "SUBMITTED" and campaign.status != "UNDER_REVIEW":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Can only request more information while campaign is SUBMITTED or UNDER_REVIEW",
        )

    if campaign.status == "SUBMITTED":
        validate_transition(campaign.status, "UNDER_REVIEW")
        campaign = campaigns_repository.update_status(db, campaign, "UNDER_REVIEW")

    _create_review(db, reviewer_id, campaign_id, "MORE_INFO_REQUESTED", notes)
    return campaign


def approve_final_review(db: Session, campaign_id: uuid.UUID, reviewer_id: uuid.UUID, notes: str | None) -> Campaign:
    campaign = _get_campaign_under_review(db, campaign_id)

    if campaign.status != "FINAL_REVIEW":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Campaign must be in FINAL_REVIEW before final approval",
        )

    validate_transition(campaign.status, "SUCCESSFUL")
    campaign = campaigns_repository.update_status(db, campaign, "SUCCESSFUL")
    _create_review(db, reviewer_id, campaign_id, "FINAL_APPROVED", notes)

    return campaign
