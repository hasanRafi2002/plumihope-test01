from pydantic import BaseModel, Field


class ApprovalRequest(BaseModel):
    notes: str | None = None


class RejectionRequest(BaseModel):
    notes: str = Field(min_length=1)


class MoreInfoRequest(BaseModel):
    notes: str = Field(min_length=1)
