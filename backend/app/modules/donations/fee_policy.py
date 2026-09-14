from decimal import Decimal, ROUND_HALF_UP

# Explicit fee policy configuration (version 1).
# TODO(Phase 20 - Admin Settings): move to a database-backed policy table
# so historical donations retain the policy version used at the time.
FEE_POLICY_VERSION = "v1"
PAYMENT_FEE_PERCENT = Decimal("1.5")
PLATFORM_FEE_PERCENT = Decimal("2.0")


def _round(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_fee_breakdown(donation_amount: Decimal) -> dict:
    payment_fee = _round(donation_amount * PAYMENT_FEE_PERCENT / Decimal("100"))
    platform_fee = _round(donation_amount * PLATFORM_FEE_PERCENT / Decimal("100"))
    net_amount = donation_amount - payment_fee - platform_fee

    return {
        "donation_amount": donation_amount,
        "payment_fee": payment_fee,
        "platform_fee": platform_fee,
        "net_amount": net_amount,
        "total_charged": donation_amount,
        "policy_version": FEE_POLICY_VERSION,
    }
