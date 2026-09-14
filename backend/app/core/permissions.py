from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users import repository as users_repository
from app.modules.users.models import User


def require_role(role_name: str):
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        role_names = users_repository.get_user_role_names(db, current_user.id)
        if role_name not in role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {role_name}",
            )
        return current_user

    return dependency


def require_permission(permission_code: str):
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        permission_codes = users_repository.get_user_permission_codes(db, current_user.id)
        if permission_code not in permission_codes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires permission: {permission_code}",
            )
        return current_user

    return dependency


def require_agent_verified(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    from app.modules.agents.models import AgentProfile

    profile = db.query(AgentProfile).filter(AgentProfile.user_id == current_user.id).first()

    if not profile or profile.status != "VERIFIED":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires verified Agent status",
        )
    return current_user


def require_object_owner(owner_id, current_user_id) -> None:
    if owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource",
        )


def require_state(current_state: str, allowed_states: set[str]) -> None:
    if current_state not in allowed_states:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Action not allowed in current state: {current_state}",
        )
