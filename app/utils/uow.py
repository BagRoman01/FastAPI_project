from abc import ABC, abstractmethod
from app.database.db import async_session_maker
from app.database.repositories.session_repo import SessionRepository
from app.database.repositories.user_repo import UserRepository


class IUnitOfWork(ABC):
    user_repos: UserRepository
    session_repos: SessionRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_creator = async_session_maker

    async def __aenter__(self):
        self.session = self.session_creator()

        self.user_repos = UserRepository(self.session)
        self.session_repos = SessionRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
