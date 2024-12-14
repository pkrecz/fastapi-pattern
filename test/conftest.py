import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from config.database import get_engine, get_db
from main import app


@pytest.fixture(scope="session")
def db_test():
    session_local = sessionmaker(
                                    autocommit=False,
                                    autoflush=False)
    logging.info("Configuration -----> Session local created.")
    connection = get_engine().connect()
    logging.info("Configuration -----> Connection established.")
    transaction = connection.begin()
    logging.info("Configuration -----> Transaction started.")
    session = session_local(bind=connection)
    logging.info("Configuration -----> Session ready for running.")
    yield session
    session.close()
    logging.info("Configuration -----> Session closed.")
    transaction.rollback()
    logging.info("Configuration -----> Rollback executed.")
    connection.close()
    logging.info("Configuration -----> Connection closed.")


@pytest.fixture(scope="session")
def client_test(db_test):

    def override_get_db():
        try:
            yield db_test
        finally:
            db_test.close()

    app.dependency_overrides[get_db] = override_get_db
    logging.info("Configuration -----> Dependency overrided.")
    with TestClient(app) as client_test:
        logging.info("Configuration -----> Client ready for running.")
        yield client_test
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
