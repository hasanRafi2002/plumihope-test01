from fastapi import HTTPException, status

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "DRAFT": {"SUBMITTED", "CANCELLED"},
    "SUBMITTED": {"UNDER_REVIEW", "CANCELLED"},
    "UNDER_REVIEW": {"APPROVED", "REJECTED"},
    "REJECTED": set(),
    "APPROVED": {"ACTIVE"},
    "ACTIVE": {"TARGET_REACHED", "EXPIRED", "SUSPENDED", "CANCELLED", "DISPUTED"},
    "TARGET_REACHED": {"PAYOUT_PENDING", "DISPUTED"},
    "PAYOUT_PENDING": {"ASSISTANCE_PENDING", "DISPUTED"},
    "ASSISTANCE_PENDING": {"ASSISTANCE_DELIVERED", "DISPUTED"},
    "ASSISTANCE_DELIVERED": {"FINAL_REVIEW", "DISPUTED"},
    "FINAL_REVIEW": {"SUCCESSFUL", "DISPUTED"},
    "SUCCESSFUL": {"CLOSED"},
    "EXPIRED": {"CLOSED"},
    "SUSPENDED": {"ACTIVE", "CANCELLED", "FRAUDULENT"},
    "DISPUTED": {"ACTIVE", "SUSPENDED", "CANCELLED", "FRAUDULENT"},
    "CANCELLED": set(),
    "FRAUDULENT": set(),
    "CLOSED": set(),
}


def validate_transition(current_state: str, target_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state, set())
    if target_state not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot transition campaign from {current_state} to {target_state}",
        )
