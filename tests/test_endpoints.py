from httpx import AsyncClient

from tests.conftest import client
from src.users.service import user_service


jwt_token = None
task_id = None
user_id = None

auth_header = lambda: {"Authorization": 'Bearer %s' % jwt_token}


def test_read_root():
    response = client.get("api/v1/")
    assert response.status_code == 200


async def test_create_user(ac: AsyncClient):
    global user_id
    response = await ac.post(
        '/api/v1/users/register',
        json={"username": "test", "password": "password", "email": "test@test.com"}
        )
    assert response.status_code == 201
    assert "id" in response.json()
    user_id = response.json()['id']
    assert "username" in response.json()
    assert "email" in response.json()


async def test_login(ac: AsyncClient):
    global jwt_token
    response = await ac.post('/api/v1/auth/login',
                             json={'email': 'test@test.com', 'password': 'password'})
    jwt_token = response.json().get('access')
    assert response.status_code == 200
    assert 'access' in response.json()
    assert 'refresh' in response.json()


async def test_create_task(ac: AsyncClient):
    global task_id
    response = await ac.post("/api/v1/tasks/", headers=auth_header(),
                             json={"title": "New Task", "description": "some_text"})
    assert response.status_code == 201
    task = response.json()
    assert "id" in task
    task_id = task['id']
    assert task["title"] == "New Task"
    assert task["completed"] is False


async def test_read_tasks(ac: AsyncClient):
    response = await ac.get('api/v1/tasks/', headers=auth_header())
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0


async def test_read_task(ac: AsyncClient):
    global task_id
    response = await ac.get(f'/api/v1/tasks/{task_id}', headers=auth_header())
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == task_id


async def test_read_invalid_task(ac: AsyncClient):
    invalid_task_id = '3b37e798-b020-49b5-bb53-417a63d3f5a1'
    response = await ac.get(f'/api/v1/tasks/{invalid_task_id}', headers=auth_header())
    assert response.status_code == 404


async def test_update_task(ac: AsyncClient):
    response = await ac.put(
        f'api/v1/tasks/{task_id}',
        headers=auth_header(),
        json={'title': 'Change_title', 'completed': True},
    )
    assert response.status_code == 200
    assert response.json()['title'] == 'Change_title'
    assert response.json()['completed'] is True


async def test_delete_task(ac: AsyncClient):
    response = await ac.delete(f'api/v1/tasks/{task_id}', headers=auth_header())
    assert response.status_code == 204

    await user_service.delete(user_id)
