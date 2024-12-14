from fastapi import FastAPI
from config import registry
from config.settings import settings


def init_app():
    app = FastAPI(
                    title=settings.title,
                    version=settings.version,
                    docs_url=settings.docs_url,
                    redoc_url=None,
                    contact={
                                "name": "Piotr",
                                "email": "pkrecz@poczta.onet.pl"})
    registry.create_tables()
    registry.load_routers(app)
    registry.load_middleware(app)
    return app


app = init_app()
