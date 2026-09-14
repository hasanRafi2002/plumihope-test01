import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    entity_id: uuid.UUID
    reason: str = Field(min_length=1, max_length=128)
    description: str | None = None


class ReportPublic(BaseModel):
    id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    reason: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportDetail(ReportPublic):
    description: str | None
    resolution_notes: str | None
    resolved_at: datetime | None


class ReportResolution(BaseModel):
    notes: str = Field(min_length=1)
