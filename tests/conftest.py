import asyncio
import pytest

from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app


client = TestClient(app)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        yield ac
