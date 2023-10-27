from fastapi import APIRouter

from src.task.schemas import Task
from src.task.service import task_service as ts


task_router = APIRouter(tags=['Task'])


task_router.add_api_websocket_route('/ws/tasks/{client_id}', ts.websocket_endpoint)
task_router.add_api_route('/tasks/', ts.create, response_model=Task, methods={'post'})
task_router.add_api_route('/tasks/', ts.all, response_model=list[Task], methods={'get'})
task_router.add_api_route('/tasks/{task_id}', ts.retrieve, response_model=Task, methods={'get'})
task_router.add_api_route('/tasks/{task_id}', ts.update_task, response_model=Task, methods={'put'})
task_router.add_api_route('/tasks/{task_id}', ts.delete_task, response_model=Task, methods={'delete'})
