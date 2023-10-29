from fastapi import APIRouter
from starlette.status import HTTP_204_NO_CONTENT

from src.task.schemas import Task
from src.task.service import task_service as ts


router = APIRouter()
websocket_router = APIRouter()

websocket_router.add_api_websocket_route('/{client_id}', ts.websocket_endpoint)

router.add_api_route('/', ts.create, response_model=Task, methods={'post'})
router.add_api_route('/', ts.all, response_model=list[Task], methods={'get'})
router.add_api_route('/{task_id}', ts.get_one, response_model=Task, methods={'get'})
router.add_api_route('/{task_id}', ts.update_task, response_model=Task, methods={'put'})
router.add_api_route(
    '/{task_id}', ts.delete_task, methods={'delete'}, status_code=HTTP_204_NO_CONTENT
)
