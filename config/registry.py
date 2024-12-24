import logging
from config.database import Base, get_engine
from config.middleware import CustomMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app_example import controlers as example_controlers


logger = logging.getLogger("uvicorn.error")


def init_models():
    Base.metadata.create_all(bind=get_engine())
    logger.info("Tables has been created.")


def init_routers(app):
    app.include_router(
                        router=example_controlers.router,
                        prefix="",
                        tags=["Example"])
    logger.info("Routers has been loaded.")


def init_middleware(app):
    app.add_middleware(CustomMiddleware)
    app.add_middleware(
                        CORSMiddleware,
                        allow_origins=["*"],
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"])
    logger.info("Middleware has been added.")
