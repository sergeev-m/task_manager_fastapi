from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from core.errors import AlreadyExistError
from core.service import BaseService
from src.auth.service import auth_service
from src.task.repository import task_repository
from core.service import PyModel
from src.task.schemas import TaskCreate, TaskUpdate


class TaskService(BaseService):
    def __init__(self, *args, **kwargs):
        self.active_connections: set[WebSocket] = set()
        super().__init__(*args, **kwargs)

    async def websocket_endpoint(self, client_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                for connection in self.active_connections:
                    await connection.send_text(f'Client with {client_id} wrote {message}!')
        except WebSocketDisconnect:
            self.active_connections.remove(websocket)

    async def create(
            self, model: TaskCreate, owner_id: UUID = Depends(auth_service.get_user_id_by_token)
    ):
        data = model.model_dump()
        data.update({"owner_id": owner_id})
        try:
            db_task = await self.repository.create(data)
        except AlreadyExistError as e:
            raise HTTPException(HTTP_400_BAD_REQUEST, str(e))

        for connection in self.active_connections:
            await connection.send_text(f'New task created: {db_task.title}')
        return db_task

    async def all(self, skip: int = 0, limit: int = 10):
        return await self.repository.filter(offset=skip, limit=limit)

    async def update_task(self, task_id: UUID, task_update: TaskUpdate):
        task = await self.update(task_id, task_update)
        for connection in self.active_connections:
            await connection.send_text(f'Task {task.id} updated')
        return task

    async def delete_task(self, task_id: UUID):
        await self.delete(task_id)
        for connection in self.active_connections:
            await connection.send_text(f'Task {task_id} deleted')
        return

    async def get_one(self, task_id: UUID):
        return await self.retrieve(task_id)


task_service = TaskService(repository=task_repository)
