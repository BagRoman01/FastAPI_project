import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from app.database.db import Base
from app.core.config import settings
from main import app
import httpx

engine_test = create_async_engine(settings.ASYNC_DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


@pytest.fixture(autouse=True, scope='session')
async def setup_database():
    print(f'database_name: {settings.DB_NAME}')
    assert settings.MODE == "TEST"
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1") as async_client:
        yield async_client

