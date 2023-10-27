from typing import Annotated

from fastapi import APIRouter, Depends
from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect

from src.task.schemas import Task, TaskCreate, TaskUpdate
from src.users.schemas import UserCreate, User
from src.users.service import UserService, user_service
from src.task.service import task_service as ts
from src.auth.service import auth_service
task_router = APIRouter(tags=['Task'])


task_router.add_api_websocket_route('/ws/tasks/{client_id}', ts.websocket_endpoint)

task_router.add_api_route('/tasks/', ts.create, response_model=Task, methods={'post'})

task_router.add_api_route('/tasks/', ts.all, response_model=list[Task], methods={'get'})

task_router.add_api_route('/tasks/{task_id}', ts.retrieve, response_model=Task, methods={'get'})

task_router.add_api_route('/tasks/{task_id}', ts.update_task, response_model=Task, methods={'put'})

task_router.add_api_route('/tasks/{task_id}', ts.delete_task, response_model=Task, methods={'delete'})
