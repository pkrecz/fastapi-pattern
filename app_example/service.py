from typing import Type, TypeVar
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.orm import Session
from fastapi_filter.contrib.sqlalchemy import Filter
from .models import AuthorModel
from .repository import CrudOperationRepository


Model = TypeVar("Model", bound=SQLModel)


class AuthorService:

    def __init__(self, db: Session):
        self.db = db
        self.model = AuthorModel
        self.crud = CrudOperationRepository(self.db, self.model)

    def author_create(self, data: Type[BaseModel]) -> Type[Model]:
        instance = self.model(**data.model_dump())
        return self.crud.create(instance)

    def author_update(self, id: int, data: Type[BaseModel]) -> Type[Model]:
        instance = self.crud.get_by_id(id)
        return self.crud.update(instance, data)

    def author_delete(self, id: int) -> bool:
        instance = self.crud.get_by_id(id)
        return self.crud.delete(instance)

    def author_retrieve(self, id: int) -> Type[Model]:
        instance = self.crud.get_by_id(id)
        return self.crud.retrieve(instance)

    def author_list(self, filter: Filter = None) -> Type[Model]:
        instances = self.crud.get_all(filter)
        return self.crud.list(instances)
