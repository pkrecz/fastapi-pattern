from fastapi import FastAPI
from config import registry
from config.settings import settings


def lifespan(app: FastAPI):
    registry.init_models()
    registry.init_routers(app)
    yield


app = FastAPI(
                lifespan=lifespan,
                title=settings.title,
                version=settings.version,
                docs_url=settings.docs_url,
                redoc_url=None,
                contact={
                            "name": "Piotr",
                            "email": "pkrecz@poczta.onet.pl"})
registry.init_middleware(app)
