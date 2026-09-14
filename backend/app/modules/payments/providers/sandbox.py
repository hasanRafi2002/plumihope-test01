import uuid

from app.modules.payments.providers.base import PaymentProvider


class SandboxPaymentProvider(PaymentProvider):
    """Local development/testing provider. Never use in production.

    Simulates a payment gateway: initiation always succeeds and returns
    a fake reference; verification always reports VERIFIED. This lets us
    exercise the full server-side verification pipeline without a real
    payment gateway integration.
    """

    def initiate_payment(self, payment_reference: str, amount, currency: str) -> dict:
        provider_reference = f"SANDBOX-{uuid.uuid4()}"
        return {
            "provider_reference": provider_reference,
            "redirect_url": f"https://sandbox.plumihope.local/pay/{provider_reference}",
            "status": "INITIATED",
        }

    def verify_payment(self, provider_reference: str) -> dict:
        return {"status": "VERIFIED", "provider_reference": provider_reference}
