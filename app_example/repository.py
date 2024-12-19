from typing import TypeVar, Annotated
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_filter.contrib.sqlalchemy import Filter
from config.database import Base


Model = TypeVar("Model", bound=Base)


class CrudOperationRepository:

    def __init__(self, db: Session, model: Model):
        self.db = db
        self.model = model


    def get_by_id(self, id: int) -> Model:
        return self.db.get(self.model, id)


    def get_all(self, filter: Filter = None) -> Model:
        query = select(self.model)
        if filter is not None:
            query = filter.filter(query)
            query = filter.sort(query)
        return self.db.scalars(query).all()


    def create(self, record: Model) -> Model:
        self.db.add(record)
        self.db.flush()
        self.db.refresh(record)
        return record


    def update(self, record: Model, data: Annotated[BaseModel, dict]) -> Model:
        if isinstance(data, BaseModel):
            data = data.model_dump(exclude_none=True)
        for key, value in data.items():
            setattr(record, key, value)
        self.db.flush()
        self.db.refresh(record)
        return record


    def delete(self, record: Model) -> bool:
        if record is not None:
            self.db.delete(record)
            self.db.flush()
            return True
        else:
            return False


    def retrieve(self, record: Model) -> Model:
        return record


    def list(self, record: Model) -> list[Model]:
        return record
