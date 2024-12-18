import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from functools import cache
from dotenv import load_dotenv


class Base(DeclarativeBase):
    pass


load_dotenv()
url = os.getenv("DATABASE_URL")


@cache
def get_engine(db_url: str = url):
    return create_engine(db_url, pool_pre_ping=True)


def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return session()


class DatabaseSessionClass:

    def __enter__(self):
        self.db = get_session()
        return self.db

    def __exit__(self, exc_type, exc_value: str, exc_traceback: str) -> None:
        try:
            if any([exc_type, exc_value, exc_traceback]):
                raise
            self.db.commit()
        except (SQLAlchemyError, DatabaseError, Exception) as exception:
            self.db.rollback()
            raise exception
        finally:
            self.db.close()


def get_db():
    with DatabaseSessionClass() as db:
        yield db
