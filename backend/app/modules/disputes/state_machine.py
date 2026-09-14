from fastapi import HTTPException, status

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "OPEN": {"UNDER_REVIEW"},
    "UNDER_REVIEW": {"RESOLVED"},
    "RESOLVED": set(),
}


def validate_transition(current_state: str, target_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if target_state not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition dispute from {current_state} to {target_state}",
        )
