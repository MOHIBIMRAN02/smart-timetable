from __future__ import annotations

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.utils.enums import UserRole
from app.utils.exceptions import AppError
from app.utils.security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # If no token, create a default admin user for public access
    if not token:
        # Create or get default public user
        user = db.query(User).filter(User.username == "public").first()
        if not user:
            user = User(name="Public User", username="public", password_hash="", role=UserRole.admin, is_active=True)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    
    credentials_error = AppError(
        message="Could not validate credentials",
        error_code="INVALID_AUTH",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = db.query(User).filter(User.username == username, User.is_active.is_(True)).first()
    if not user:
        raise credentials_error
    return user


def require_roles(*roles: UserRole):
    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise AppError(
                message="You are not authorized for this action",
                error_code="FORBIDDEN",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return current_user

    return role_dependency

