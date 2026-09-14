from sqlalchemy.orm import Session

from app.modules.users import repository
from app.modules.users.models import User
from app.modules.users.schemas import UserProfileUpdate


def update_profile(db: Session, user: User, payload: UserProfileUpdate) -> User:
    updates = payload.model_dump(exclude_unset=True, exclude_none=True)
    if not updates:
        return user
    return repository.update_user(db, user, updates)
