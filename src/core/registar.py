from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.core.log import log
from src.routers import v1
from src.core.middleware.access_middleware import AccessMiddleware
from src.core.config.settings import settings
from src.core.errors import CustomError


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
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log.exception("Alarm! Global exception!")
        return JSONResponse(
            status_code=500,
            content={"error": "O-o-o-ps! Internal server error"}
        )

    @app.exception_handler(CustomError)
    async def custom_exception_handler_a(request: Request, exc: CustomError):
        log.info(str(exc))
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.__dict__
        )
