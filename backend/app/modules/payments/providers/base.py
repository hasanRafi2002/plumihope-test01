from abc import ABC, abstractmethod


class PaymentProvider(ABC):
    """Abstract payment provider interface.

    All concrete providers (sandbox, real gateways) must implement this
    contract. The server never trusts client-reported payment status;
    only provider-verified results flow through these methods.
    """

    @abstractmethod
    def initiate_payment(self, payment_reference: str, amount, currency: str) -> dict:
        """Start a payment with the provider. Returns provider-specific
        initiation data (e.g. a redirect URL or a payment intent id)."""
        raise NotImplementedError

    @abstractmethod
    def verify_payment(self, provider_reference: str) -> dict:
        """Query the provider for the authoritative status of a payment.
        Returns a dict with at least: {"status": "VERIFIED" | "FAILED" | "PENDING"}."""
        raise NotImplementedError
