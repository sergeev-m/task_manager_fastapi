from fastapi import FastAPI

from core.errors import CustomError
from core.log import log
from core.routers import v1
from core.middleware.access_middleware import AccessMiddleware
from core.config.settings import settings


def register_app():
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
    )
    register_middleware(app)
    register_router(app)
    register_exception(app)
    return app


def register_middleware(app: FastAPI):
    app.add_middleware(AccessMiddleware)


def register_router(app: FastAPI):
    app.include_router(v1)


def register_exception(app: FastAPI):
    pass
