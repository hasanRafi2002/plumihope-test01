from fastapi import HTTPException, status

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "PENDING": {"UNDER_REVIEW"},
    "UNDER_REVIEW": {"VERIFIED", "REJECTED"},
    "VERIFIED": {"RESTRICTED", "SUSPENDED", "REVOKED"},
    "RESTRICTED": {"VERIFIED", "SUSPENDED", "REVOKED"},
    "SUSPENDED": {"VERIFIED", "REVOKED"},
    "REJECTED": set(),
    "REVOKED": set(),
}

# REVOKED may only be reached by ADMIN role, never by MODERATOR permission alone.
ADMIN_ONLY_TARGET_STATES: set[str] = {"REVOKED"}


def validate_transition(current_state: str, target_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if target_state not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition agent from {current_state} to {target_state}",
        )
