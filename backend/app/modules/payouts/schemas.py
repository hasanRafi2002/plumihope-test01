import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PayoutPublic(BaseModel):
    id: uuid.UUID
    campaign_id: uuid.UUID
    amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PayoutInitiateRequest(BaseModel):
    campaign_id: uuid.UUID
