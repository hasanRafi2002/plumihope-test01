from fastapi import HTTPException, status

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "SUBMITTED": {"AVAILABLE", "CANCELLED"},
    "AVAILABLE": {"CLAIMED", "CANCELLED"},
    "CLAIMED": {"INVESTIGATING", "AVAILABLE"},
    "INVESTIGATING": {"ELIGIBLE", "NOT_ELIGIBLE"},
    "ELIGIBLE": {"CONVERTED_TO_CAMPAIGN", "CLOSED"},
    "NOT_ELIGIBLE": {"CLOSED"},
    "CONVERTED_TO_CAMPAIGN": set(),
    "CLOSED": set(),
    "CANCELLED": set(),
}


def validate_transition(current_state: str, target_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if target_state not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition help request from {current_state} to {target_state}",
        )
