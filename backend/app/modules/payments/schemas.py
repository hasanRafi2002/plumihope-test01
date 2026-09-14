import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PaymentInitiateRequest(BaseModel):
    donation_id: uuid.UUID


class PaymentInitiateResponse(BaseModel):
    payment_id: uuid.UUID
    provider: str
    provider_reference: str
    redirect_url: str
    status: str


class PaymentPublic(BaseModel):
    id: uuid.UUID
    donation_id: uuid.UUID
    provider: str
    amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class WebhookPayload(BaseModel):
    provider_reference: str
