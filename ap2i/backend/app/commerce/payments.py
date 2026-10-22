"""Payment-provider abstraction (Master prompt §26).

Payment processing is NOT active: no provider is implemented with verified credentials and
compliance review. Subscriptions are granted by an AP²I administrator (offline invoicing) until a
provider (e.g. a card or mobile-money processor) is implemented, reviewed and configured.
"""

from __future__ import annotations

from decimal import Decimal

from app.config import get_settings


class PaymentsNotActivated(Exception):
    pass


class PaymentProvider:
    name = "abstract"

    def create_checkout(self, subscription_id: int, amount: Decimal, currency: str, customer_email: str) -> dict:
        raise NotImplementedError

    def verify_webhook(self, payload: bytes, signature: str) -> dict:
        raise NotImplementedError


class NullPaymentProvider(PaymentProvider):
    name = "none"

    def create_checkout(self, subscription_id, amount, currency, customer_email):
        raise PaymentsNotActivated("Online payment is not activated. Contact AP²I for an invoice.")

    def verify_webhook(self, payload, signature):
        raise PaymentsNotActivated("Online payment is not activated.")


def get_payment_provider() -> PaymentProvider:
    s = get_settings()
    if s.payment_provider != "none":
        # Deliberately refuse: a provider must be implemented and compliance-reviewed first.
        raise PaymentsNotActivated(f"Payment provider '{s.payment_provider}' is configured but no reviewed implementation exists.")
    return NullPaymentProvider()
