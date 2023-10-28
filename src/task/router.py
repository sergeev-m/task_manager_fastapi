from fastapi import APIRouter

from starlette.status import HTTP_204_NO_CONTENT

from src.task.schemas import Task
from src.task.service import task_service as ts


task_router = APIRouter(tags=['Task'])


task_router.add_api_websocket_route('/ws/tasks/{client_id}', ts.websocket_endpoint)
task_router.add_api_route('/tasks/', ts.create, response_model=Task, methods={'post'})
task_router.add_api_route('/tasks/', ts.all, response_model=list[Task], methods={'get'})
task_router.add_api_route('/tasks/{task_id}', ts.get_one, response_model=Task, methods={'get'})
task_router.add_api_route('/tasks/{task_id}', ts.update_task, response_model=Task, methods={'put'})
task_router.add_api_route('/tasks/{task_id}', ts.delete_task, methods={'delete'}, status_code=HTTP_204_NO_CONTENT)
