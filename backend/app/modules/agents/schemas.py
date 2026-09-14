import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AgentApplicationCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = Field(default=None, max_length=32)
    location: str | None = Field(default=None, max_length=255)
    experience: str | None = None
    facebook_url: str | None = Field(default=None, max_length=512)
    youtube_url: str | None = Field(default=None, max_length=512)
    other_url: str | None = Field(default=None, max_length=512)


class AgentProfilePublic(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    full_name: str
    location: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AgentProfileDetail(AgentProfilePublic):
    phone: str | None
    experience: str | None
    facebook_url: str | None
    youtube_url: str | None
    other_url: str | None


class AgentReviewDecision(BaseModel):
    decision: str = Field(pattern="^(VERIFIED|REJECTED)$")
    notes: str | None = None
