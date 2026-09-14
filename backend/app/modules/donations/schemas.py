import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    campaign_id: uuid.UUID
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="BDT", max_length=8)


class FeeBreakdown(BaseModel):
    donation_amount: Decimal
    payment_fee: Decimal
    platform_fee: Decimal
    net_amount: Decimal
    total_charged: Decimal
    policy_version: str


class DonationPublic(BaseModel):
    id: uuid.UUID
    campaign_id: uuid.UUID
    amount: Decimal
    currency: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DonationDetail(DonationPublic):
    fee_breakdown: FeeBreakdown
