from app.core.config import settings
from app.modules.payments.providers.base import PaymentProvider
from app.modules.payments.providers.sandbox import SandboxPaymentProvider


def get_payment_provider() -> PaymentProvider:
    if settings.payment_provider == "sandbox":
        return SandboxPaymentProvider()
    raise NotImplementedError(f"Unsupported payment provider: {settings.payment_provider}")
