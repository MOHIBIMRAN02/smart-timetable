from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import ORMBase
from app.utils.enums import UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=60)
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(ORMBase):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    name: str
