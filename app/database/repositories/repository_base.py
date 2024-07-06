from abc import ABC, abstractmethod

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryBase(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, find_id: int):
        raise NotImplementedError


class Repository(RepositoryBase):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        query_exec = await self.session.execute(insert(self.model).values(**data).returning(self.model))
        return query_exec.scalar()

    async def get_by_id(self, find_id: int) -> model:
        model = self.model
        query_exec = await self.session.execute(select(model).where(model.get_primary_key() == find_id))
        result: model = query_exec.scalars().first()
        return result
