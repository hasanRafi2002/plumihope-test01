from fastapi import HTTPException, status

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "INITIATED": {"PENDING", "CANCELLED"},
    "PENDING": {"PAID", "FAILED", "CANCELLED"},
    "PAID": {"CONFIRMED"},
    "CONFIRMED": {"REFUNDED", "DISPUTED"},
    "FAILED": set(),
    "CANCELLED": set(),
    "REFUNDED": set(),
    "DISPUTED": {"CONFIRMED"},
}


def validate_transition(current_state: str, target_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if target_state not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition donation from {current_state} to {target_state}",
        )
