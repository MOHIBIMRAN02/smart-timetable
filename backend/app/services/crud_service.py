from __future__ import annotations

from typing import Any, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.database import Base
from app.utils.exceptions import AppError

ModelT = TypeVar("ModelT", bound=Base)


class CRUDService:
    def __init__(self, model: type[ModelT], entity_name: str):
        self.model = model
        self.entity_name = entity_name

    def list(self, db: Session, stmt: Select[Any] | None = None) -> list[ModelT]:
        target_stmt = stmt if stmt is not None else select(self.model)
        return list(db.scalars(target_stmt).all())

    def get(self, db: Session, entity_id: int) -> ModelT:
        entity = db.get(self.model, entity_id)
        if not entity:
            raise AppError(f"{self.entity_name} not found", "NOT_FOUND", 404)
        return entity

    def create(self, db: Session, payload: dict[str, Any]) -> ModelT:
        entity = self.model(**payload)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db: Session, entity_id: int, payload: dict[str, Any]) -> ModelT:
        entity = self.get(db, entity_id)
        for key, value in payload.items():
            setattr(entity, key, value)
        db.commit()
        db.refresh(entity)
        return entity

    def delete(self, db: Session, entity_id: int) -> None:
        entity = self.get(db, entity_id)
        db.delete(entity)
        db.commit()
