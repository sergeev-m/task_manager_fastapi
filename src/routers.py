from fastapi import APIRouter


from src.core.config.settings import settings
from src.users.router import router as user_router
from src.auth.router import router as auth_router
from src.task.router import router as task_router, websocket_router as ws_task_router


v1 = APIRouter(prefix=settings.API_V1_STR)

ws_router = APIRouter()
ws_router.include_router(ws_task_router, prefix='/tasks')


v1.include_router(ws_router, prefix='/ws')
v1.include_router(auth_router, prefix='/auth', tags=['Auth'])
v1.include_router(user_router, prefix='/users', tags=['User'])
v1.include_router(task_router, prefix='/tasks', tags=['Task'])

v1.add_api_route('/', lambda: sorted({route.path for route in vars(v1)['routes']}))
