from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from core.errors import CustomError
from src.users.router import user_router
from src.auth.router import auth_router
from src.task.router import task_router


app = FastAPI()


app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)


@app.exception_handler(CustomError)
async def custom_exception_handler_a(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.__dict__
    )
