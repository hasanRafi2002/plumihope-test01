import uuid

from sqlalchemy.orm import Session

from app.modules.users.models import User, Role, Permission, UserRole, RolePermission


def get_user_role_names(db: Session, user_id: uuid.UUID) -> set[str]:
    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return {row[0] for row in rows}


def get_user_permission_codes(db: Session, user_id: uuid.UUID) -> set[str]:
    rows = (
        db.query(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(Role, Role.id == RolePermission.role_id)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return {row[0] for row in rows}


def update_user(db: Session, user: User, updates: dict) -> User:
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
