from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.payments import service
from app.modules.payments.schemas import PaymentInitiateRequest, PaymentInitiateResponse, WebhookPayload
from app.modules.users.models import User

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/initiate", response_model=PaymentInitiateResponse, status_code=201)
def initiate_payment(
    payload: PaymentInitiateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.initiate_payment(db, payload.donation_id, current_user.id)


@router.post("/webhooks/{provider}")
def payment_webhook(
    provider: str,
    payload: WebhookPayload,
    db: Session = Depends(get_db),
):
    return service.process_webhook(db, payload.provider_reference)
