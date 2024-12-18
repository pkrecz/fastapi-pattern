from typing import Type, TypeVar
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_filter.contrib.sqlalchemy import Filter
from config.database import Base


Model = TypeVar("Model", bound=Base)


class CrudOperationRepository:

    def __init__(self, db: Session, model: type[Model]):
        self.db = db
        self.model = model


    def get_by_id(self, id: int) -> Type[Model]:
        return self.db.get(self.model, id)


    def get_all(self, filter: Type[Filter] = None) -> Type[Model]:
        query = select(self.model)
        if filter is not None:
            query = filter.filter(query)
            query = filter.sort(query)
        return self.db.scalars(query).all()


    def create(self, record: Type[Model]) -> Type[Model]:
        self.db.add(record)
        self.db.flush()
        self.db.refresh(record)
        return record


    def update(self, record: Type[Model], data: Type[BaseModel]) -> Type[Model]:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(record, key, value)
        self.db.flush()
        self.db.refresh(record)
        return record


    def delete(self, record: Type[Model]) -> bool:
        if record is not None:
            self.db.delete(record)
            self.db.flush()
            return True
        else:
            return False


    def retrieve(self, record: Type[Model]) -> Type[Model]:
        return record


    def list(self, record: Type[Model]) -> list[Type[Model]]:
        return record
