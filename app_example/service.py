from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi_filter.contrib.sqlalchemy import Filter
from config.database import Base
from .models import AuthorModel
from .repository import CrudOperationRepository


Model = TypeVar("Model", bound=Base)


class AuthorService:

    def __init__(self, db: Session):
        self.db = db
        self.model = AuthorModel
        self.crud = CrudOperationRepository(self.db, self.model)


    def author_create(self, data: BaseModel) -> Model:
        instance = self.model(**data.model_dump())
        return self.crud.create(instance)


    def author_update(self, id: int, data: BaseModel) -> Model:
        instance = self.crud.get_by_id(id)
        return self.crud.update(instance, data)


    def author_delete(self, id: int) -> bool:
        instance = self.crud.get_by_id(id)
        return self.crud.delete(instance)


    def author_retrieve(self, id: int) -> Model:
        instance = self.crud.get_by_id(id)
        return self.crud.retrieve(instance)


    def author_list(self, filter: Filter = None) -> Model:
        instance = self.crud.get_all(filter)
        return self.crud.list(instance)
