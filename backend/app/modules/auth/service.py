import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.modules.auth import repository
from app.modules.auth.schemas import RegisterRequest, LoginRequest, TokenResponse


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _issue_tokens(db: Session, user_id) -> TokenResponse:
    access_token = create_access_token(user_id)

    raw_refresh_token = secrets.token_urlsafe(64)
    token_hash = _hash_token(raw_refresh_token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_expire_days)

    repository.store_refresh_token(db, user_id, token_hash, expires_at)

    return TokenResponse(access_token=access_token, refresh_token=raw_refresh_token)


def register(db: Session, payload: RegisterRequest) -> TokenResponse:
    existing = repository.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    password_hash = hash_password(payload.password)
    user = repository.create_user(db, payload.full_name, payload.email, password_hash)

    return _issue_tokens(db, user.id)


def login(db: Session, payload: LoginRequest) -> TokenResponse:
    user = repository.get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if user.status != "ACTIVE":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active")

    return _issue_tokens(db, user.id)


def refresh(db: Session, refresh_token: str) -> TokenResponse:
    token_hash = _hash_token(refresh_token)
    stored = repository.get_refresh_token(db, token_hash)

    if not stored or stored.revoked or stored.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    repository.revoke_refresh_token(db, token_hash)

    return _issue_tokens(db, stored.user_id)


def logout(db: Session, refresh_token: str) -> None:
    token_hash = _hash_token(refresh_token)
    repository.revoke_refresh_token(db, token_hash)
