import uuid
from datetime import datetime

from pydantic import BaseModel, Field

VALID_OUTCOMES = {
    "NO_ISSUE", "REFUND", "PARTIAL_REFUND", "CAMPAIGN_SUSPENDED",
    "AGENT_RESTRICTED", "PAYMENT_INVESTIGATION", "ESCALATED",
}


class DisputeCreate(BaseModel):
    campaign_id: uuid.UUID | None = None
    donation_id: uuid.UUID | None = None
    issue: str = Field(min_length=1)


class DisputePublic(BaseModel):
    id: uuid.UUID
    campaign_id: uuid.UUID | None
    donation_id: uuid.UUID | None
    issue: str
    status: str
    outcome: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DisputeResolution(BaseModel):
    outcome: str = Field(pattern="^(NO_ISSUE|REFUND|PARTIAL_REFUND|CAMPAIGN_SUSPENDED|AGENT_RESTRICTED|PAYMENT_INVESTIGATION|ESCALATED)$")
    notes: str | None = None
