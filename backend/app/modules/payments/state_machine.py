from fastapi import HTTPException, status

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "INITIATED": {"PROCESSING", "FAILED", "CANCELLED"},
    "PROCESSING": {"VERIFIED", "FAILED"},
    "VERIFIED": set(),
    "FAILED": set(),
    "CANCELLED": set(),
}


def validate_transition(current_state: str, target_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if target_state not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition payment from {current_state} to {target_state}",
        )
