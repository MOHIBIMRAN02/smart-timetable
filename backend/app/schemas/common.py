from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class APIError(BaseModel):
    success: bool = False
    message: str
    error_code: str


class APIMessage(BaseModel):
    success: bool = True
    message: str


class TimestampedSchema(ORMBase):
    created_at: datetime | None = None
    updated_at: datetime | None = None
