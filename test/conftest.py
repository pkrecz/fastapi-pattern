import os
import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.database import Base, get_db
from main import app


engine = create_engine(os.getenv("DATABASE_URL_TEST"))


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logging.info("Configuration -----> Tables for testing has been created.")
    yield
    Base.metadata.drop_all(bind=engine)
    logging.info("Configuration -----> Tables for testing has been removed.")


@pytest.fixture(scope="session")
def db():
    connection = engine.connect()
    logging.info("Configuration -----> Connection established.")
    transaction = connection.begin()
    logging.info("Configuration -----> Transaction started.")
    session = sessionmaker(
                            autocommit=False,
                            autoflush=False,
                            bind=connection)()
    logging.info("Configuration -----> Session ready for running.")
    yield session
    session.close()
    logging.info("Configuration -----> Session closed.")
    transaction.rollback()
    logging.info("Configuration -----> Rollback executed.")
    connection.close()
    logging.info("Configuration -----> Connection closed.")


@pytest.fixture(scope="session")
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    logging.info("Configuration -----> Dependency overrided.")
    with TestClient(app) as cli:
        logging.info("Configuration -----> Client ready for running.")
        yield cli
        logging.info("Configuration -----> Client finished job.")


@pytest.fixture()
def data_test_create_author():
    return {
            "name": "JohnyG",
            "pseudo": "Walker",
            "city": "LA"}


@pytest.fixture()
def data_test_update_author():
    return {
            "pseudo": "Ranger"}
