import httpx
from httpx import AsyncClient
from main import app
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://api") as ac:
        yield ac


